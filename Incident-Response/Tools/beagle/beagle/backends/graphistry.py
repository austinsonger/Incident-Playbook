import os

import graphistry
import networkx as nx
from beagle.backends.networkx import NetworkX
from beagle.common import logger
from beagle.config import Config


class Graphistry(NetworkX):
    """Visualizes the graph using the graphistry platform (https://www.graphistry.com/).

    Examples
    --------
    >>> SysmonEVTX('sysmon_evtx_file.evtx').to_graph(Graphistry, render=True)


    Parameters
    ----------
    anonymize : bool, optional
        Should the data be anonymized before sending to graphistry?
        (the default is False, which does not.)
    render : bool, optional
        Should the result of :py:meth:`graph` be a IPython widget?
        (default value is False, which returns the URL).

    """

    def __init__(self, anonymize: bool = False, render: bool = False, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        self.anonymize = anonymize
        self.render = render

        logger.info("Initialized Graphistry Backend")

        self.key = self._get_key()
        if self.key is None:
            raise RuntimeError(
                f"Please set the graphistry API key in either the GRAPHISTRY_API_KEY"
                + " or BEAGLE__GRAPHISTRY__API_KEY enviroment variables"
            )

    def _get_key(self) -> str:  # pragma: no cover
        """Gets the graphistry API key from the enviroment variables or config.

        Returns
        -------
        str
            The graphistry API key.
        """

        if "GRAPHISTRY_API_KEY" in os.environ:
            return os.environ["GRAPHISTRY_API_KEY"]
        else:
            return Config.get("graphistry", "api_key")

    def anonymize_graph(self) -> "nx.MultiDiGraph":
        """Anonymizes the underlying graph before sending to Graphistry.

        Returns
        -------
        nx.MultiDiGraph
            The same graph structure, but without attributes.
        """

        json_graph = self.to_json()

        # Remove all properties from nodes, leave only IDs

        json_graph["nodes"] = [{"id": node["id"]} for node in json_graph["nodes"]]
        json_graph["links"] = [
            {"source": edge["source"], "target": edge["target"]} for edge in json_graph["links"]
        ]

        return nx.readwrite.json_graph.node_link_graph(json_graph)

    def graph(self):
        """Return the Graphistry URL for the graph, or an IPython Widget

        Parameters
        ----------
        render : bool, optional
            Should the result be a IPython widget? (default value is False, which returns the URL).
        Returns
        -------
        Union[str, IPython.core.display.HTML]
            str with URL to graphistry object when render if False, otherwise HTML widget for IPython.

        """

        super().graph()
        graphistry.register(self.key)

        # Convert to JSON for graphistry due to node data being objects.

        if self.anonymize:
            G = self.anoynmize_graph()
            return graphistry.bind(
                source="src", destination="dst", point_label="_id", edge_label="type"
            ).plot(G, render=self.render)

        else:
            G = nx.readwrite.json_graph.node_link_graph(self.to_json())

            return graphistry.bind(
                source="src", destination="dst", point_label="_display", edge_label="type"
            ).plot(G, render=self.render)
