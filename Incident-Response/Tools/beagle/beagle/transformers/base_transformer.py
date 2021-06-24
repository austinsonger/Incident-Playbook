import multiprocessing as mp
from abc import ABCMeta, abstractmethod
from queue import Queue
from threading import Thread, current_thread
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Any


from beagle.backends.networkx import NetworkX
from beagle.common import logger
from beagle.datasources import DataSource
from beagle.nodes import Node

_THREAD_COUNT = mp.cpu_count()

# Object to signal termination of processing.
_SENTINEL = object()


if TYPE_CHECKING:
    from beagle.backends.base_backend import Backend


class Transformer(object, metaclass=ABCMeta):
    """Base Transformer class. This class implements a producer/consumer queue
    from the datasource to the :py:meth:`transform` method. Producing the list
    of nodes is done via :py:meth:`run`

    Parameters
    ----------
    datasource : DataSource
        The `DataSource` to get events from.

    """

    def __init__(self, datasource: DataSource) -> None:

        self.count = 0
        self._queue: Queue = Queue()
        self.datasource = datasource
        self.nodes: List[Node] = []
        self.errors: Dict[Thread, List[Exception]] = {}

    def to_graph(self, backend: "Backend" = NetworkX, *args, **kwargs) -> Any:
        """Graphs the nodes created by :py:meth:`run`. If no backend is specific,
        the default used is NetworkX.

        Parameters
        ----------
        backend : [type], optional
            [description] (the default is NetworkX, which [default_description])

        Returns
        -------
        [type]
            [description]
        """

        nodes = self.run()

        backend = backend(nodes=nodes, metadata=self.datasource.metadata(), *args, **kwargs)
        return backend.graph()

    def run(self) -> List[Node]:
        """Generates the list of nodes from the datasource.

        This methods kicks off a producer/consumer queue. The producer grabs events
        one by one from the datasource by iterating over the events from the `events`
        generator. Each event is then sent to the :py:meth:`transformer` function to be
        transformer into one or more `Node` objects.

        Returns
        -------
        List[Node]
            All Nodes created from the data source.
        """

        logger.debug("Launching transformer")

        threads: List[Thread] = []

        producer_thread = Thread(target=self._producer_thread)
        producer_thread.start()
        threads.append(producer_thread)
        self.errors[producer_thread] = []

        logger.debug("Started producer thread")

        consumer_count = _THREAD_COUNT - 1
        if consumer_count == 0:
            consumer_count = 1

        for i in range(consumer_count):
            t = Thread(target=self._consumer_thread)
            self.errors[t] = []
            t.start()
            threads.append(t)

        logger.debug(f"Started {_THREAD_COUNT-1} consumer threads")

        # Wait for the producer to finish
        producer_thread.join()
        self._queue.join()

        # Stop the threads
        for i in range(consumer_count):
            self._queue.put(_SENTINEL)

        for thread in threads:
            thread.join()

        logger.info(f"Finished processing of events, created {len(self.nodes)} nodes.")

        if any([len(x) > 0 for x in self.errors.values()]):
            logger.warning(f"Parsing finished with errors.")
            logger.debug(self.errors)

        return self.nodes

    def _producer_thread(self) -> None:
        i = 0
        for element in self.datasource.events():
            self._queue.put(element, block=True)
            i += 1

        logger.debug(f"Producer Thread {current_thread().name} finished after {i} events")
        return

    def _consumer_thread(self) -> None:
        processed = 0
        while True:
            event = self._queue.get()
            processed += 1

            if event is _SENTINEL:
                logger.debug(
                    f"Consumer Thread {current_thread().name} finished after processing {processed} events"
                )
                return

            try:
                nodes = self.transform(event)
            except Exception as e:
                logger.warning(f"Error when parsing event, recieved exception {e}")
                logger.debug(event)
                self.errors[current_thread()].append(e)
                nodes = []

            if nodes:
                self.nodes += nodes

            self._queue.task_done()

    @abstractmethod
    def transform(self, event: dict) -> Optional[Iterable[Node]]:
        raise NotImplementedError("Transformers must implement transform!")
