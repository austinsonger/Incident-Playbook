from typing import Any, Dict, List


class Edge(object):
    __name__ = "Edge"

    """The base Edge class.

    An edge simply stores metadata about interaction between two nodes. Each
    Edge object is simply meant to store the metadata **on that Edge**. For example,
    for a file write event, it may want to store the time of the write, and the contents
    written.

    Since a write by Process A to File B may occur multiple times, all the properties
    stored on the edge must be arrays. When generating the graph, Beagle will either unpack
    all N properties into N edges or create a single edge with all the metadata. This will
    depend on the configuration for that run.


    Examples
    --------

    The below shows an Edge which represents a process launch. The edge contains
    a list of timestamps at which the parent process launched the child process::

        class Launched(Edge):
            __name__ = "Launched"

            timestamp: int

            def __init__(self) -> None:
                super().__init__()

    The edge would be used in the Process class as follows::

        class Process(Node):
            ...
            # List of launched processes
            launched: DefaultDict["Process", Launched]

    This would allow a process `parent` to add that it launched `child` at time 145:

    >>> proc.launched[child].append(timestamp=145)

    You can also add edges without explicitly adding data:

    >>> proc.launched[child]

    """

    _events: List[dict] = []

    def __init__(self) -> None:
        self._events = []

    def __add__(self, data: Dict[Any, Any]) -> "Edge":
        for key, value in data.items():
            if key not in self.__annotations__:
                raise RuntimeError(
                    f"{key} is not a valid field for a {self.__class__.__name__} edge. "
                    + f"Valid fields are {self.__annotations__}"
                )

        entry = {k: None for k, _ in self.__annotations__.items()}
        entry.update(data)
        entry["edge_name"] = self.get_name(entry)

        self._events.append(entry)

        return self

    def get_name(self, entry: dict):
        return self.__name__

    @property
    def _display(self):
        return self.__name__

    def append(self, **kwargs) -> None:
        """Appends the keyword arguments as an entry on the edge

        Examples
        --------

        >>> proc.launched[child].append(timestamp=145)

        >>> proc.launched[child].append(**{"timestamp": 145})

        """

        for key, value in kwargs.items():
            if key not in self.__annotations__:
                raise RuntimeError(
                    f"{key} is not a valid field for a {self.__class__.__name__} edge."
                    + f"Valid fields are {self.__annotations__}"
                )

        entry = {k: None for k, _ in self.__annotations__.items()}
        entry.update(kwargs)
        entry["edge_name"] = self.get_name(entry)

        self._events.append(entry)

    def __contains__(self, data: Dict[Any, Any]):

        found = {k: False for k in data.keys()}

        for event in self._events:
            for key, value in data.items():
                if event[key] == value:
                    found[key] = True

        return all(found.values())

    def __len__(self) -> int:
        return len(self._events)
