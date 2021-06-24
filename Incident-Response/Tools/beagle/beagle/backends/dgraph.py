import inspect
import json
import sys
from typing import DefaultDict, Dict, Union

import pydgraph

from beagle.backends.networkx import NetworkX
from beagle.common import logger
from beagle.config import Config
from beagle.nodes import Node
from beagle.edges import Edge


class DGraph(NetworkX):
    """DGraph backend (https://dgraph.io). This backend builds a schema using the `_setup_schema` function.
    It then pushes each node and retrieves it's assigned UID. Once all nodes are pushed, edges are pushed
    to the graph by mapping the node IDs to the assigned UIDs

    Parameters
    ----------
    host : str, optional
        The hostname of the DGraph instance
        (the default is Config.get("dgraph", "host"), which pulls from the configuration file)
    batch_size : int, optional
        The number of edges and nodes to push in to the database at a time.
        (the default is int(Config.get("dgraph", "batch_size")), which pulls from the configuration file)
    wipe_db : bool, optional
        Wipe the Database before inserting new data. (the default is False)

    """

    def __init__(
        self,
        host: str = Config.get("dgraph", "host"),
        batch_size: int = int(Config.get("dgraph", "batch_size")),
        wipe_db: bool = False,
        *args,
        **kwargs,
    ):

        logger.info(f"Connecting to Dgraph server at {host}")

        client_stub = pydgraph.DgraphClientStub(host)

        self.dgraph = pydgraph.DgraphClient(client_stub)
        self.host = host

        super().__init__(*args, **kwargs)

        if wipe_db:
            logger.info("Wiping existing database due to wipe_db=True")
            self.dgraph.alter(pydgraph.Operation(drop_all=True))

        self.batch_size = 1000
        logger.info("Initialized Dgraph Backend")

    def setup_schema(self) -> None:
        """Sets up the DGraph schema based on the nodes. This inspect all attributes of all nodes,
        and generates a schema for them. Each schema entry has the format `{node_type}.{field}`. If a
        field is a string field, it has the `@index(exact)` predicate added to it.

        An example output schema::

            process.process_image string @index(exact)
            process.process_id int

        """

        all_node_types = inspect.getmembers(
            sys.modules["beagle.nodes"],
            lambda cls: inspect.isclass(cls)
            and not inspect.isabstract(cls)
            and issubclass(cls, Node)
            and cls != Node,
        )

        schema = ""

        for cls_name, node_class in all_node_types:
            for attr, attr_type in node_class.__annotations__.items():
                if attr == "key_fields":
                    continue

                # https://github.com/python/typing/issues/528#issuecomment-357751667
                if type(attr_type) == type(Union):
                    attr_type = attr_type.__args__[0]

                if attr_type == int:
                    attr_type = "int"
                elif type(attr_type) == type(DefaultDict) and issubclass(
                    attr_type.__args__[1], Edge
                ):
                    # Don't need this, get built automatically
                    continue
                else:
                    attr_type = "string @index(exact)"

                # Remove spaces, lowercase
                schema += f"{node_class.__name__.lower().replace(' ', '_')}.{attr}: {attr_type} .\n"

        schema += "<type>: string @index(exact) .\n"
        logger.debug(schema)
        self.dgraph.alter(pydgraph.Operation(schema=schema))

    def graph(self):
        """Pushes the nodes and edges into DGraph."""

        logger.info(f"Generating base graph using NetworkX")

        nx_graph = super().graph()

        logger.info(f"Migrating graph to DGraph")

        logger.info(f"Setting up schema")

        self.setup_schema()

        logger.info(f"Created schema")

        uids_to_nodes: Dict[str, int] = {}
        nodes_to_uids: Dict[int, int] = {}

        current_id = 0

        def _node_to_dgraph_dict(node: Node) -> dict:
            return {
                f"{node.__name__.lower().replace(' ', '_')}.{k}": (
                    json.dumps(v) if isinstance(v, dict) else v
                )
                for k, v in node.to_dict().items()
                if v
            }

        logger.info(f"Inserting nodes")

        nodes_txn = []

        all_nodes = [node["data"] for _, node in nx_graph.nodes(data=True)]
        for i in range(0, len(all_nodes), self.batch_size):
            for node in all_nodes[i : i + self.batch_size]:
                txn = self.dgraph.txn()

                # Remove spaces, lowercase and escape
                node_data = _node_to_dgraph_dict(node)

                node_data["uid"] = f"_:node_{current_id}"

                uids_to_nodes[node_data["uid"]] = hash(node)
                current_id += 1
                node_data["type"] = node.__name__.lower().replace(" ", "_")

                nodes_txn.append(node_data)

            assigned = txn.mutate(set_obj=nodes_txn)

            for uid, assigned_uid in assigned.uids.items():
                nodes_to_uids[uids_to_nodes[f"_:{uid}"]] = assigned_uid

            txn.commit()
            logger.info(
                f"Inserted nodes batch {i} -> {i+self.batch_size}, Total UIDs: {len(nodes_to_uids.keys())} UIDs"
            )

        logger.info(f"Inserting edges")

        all_edges = nx_graph.edges(data=True, keys=True)
        for i in range(0, len(all_edges), self.batch_size):
            edge_nquads = ""
            for edge in all_edges[i : i + self.batch_size]:

                edge_nquads += f"<{nodes_to_uids[edge[0]]}> <{edge[2].lower().replace(' ', '_')}> <{nodes_to_uids[edge[1]]}> .\n"

            txn = self.dgraph.txn()

            assigned = txn.mutate(set_nquads=edge_nquads)

            logger.info(
                f"Inserted edges batch {i} -> {i+self.batch_size}, got back {len(assigned.context.keys)} UIDs"
            )

            txn.commit()

        return self.host
