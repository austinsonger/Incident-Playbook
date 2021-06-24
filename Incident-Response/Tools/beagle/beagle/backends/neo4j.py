import itertools
from typing import Any

from neo4j import GraphDatabase

from beagle.common import logger
from beagle.config import Config
from beagle.nodes import Node
from beagle.backends.networkx import NetworkX
import networkx as nx


class Neo4J(NetworkX):
    """Neo4J backend. Converts each node and edge to a Cypher and uses BATCH UNWIND queries to
    push nodes at once.

    Parameters
    ----------
    uri : str, optional
        Neo4J Hostname (the default is Config.get("neo4j", "host"), which pulls from the configuration file)
    username : str, optional
        Neo4J Username (the default is Config.get("neo4j", "username"), which pulls from the configuration file)
    password : str, optional
        Neo4J Password (the default is Config.get("neo4j", "password"), which pulls from the configuration file)
    clear_database: bool, optional
        Should the database be cleared before populating? (the default is False)
    """

    def __init__(
        self,
        uri: str = Config.get("neo4j", "host"),
        username: str = Config.get("neo4j", "username"),
        password: str = Config.get("neo4j", "password"),
        clear_database: bool = False,
        *args,
        **kwargs,
    ):

        logger.info(f"Connecting to neo4j server at {uri}")

        self.neo4j = GraphDatabase.driver(uri, auth=(username, password))

        super().__init__(*args, **kwargs)

        logger.info("Initialized Neo4j Backend")
        self.batch_size = int(Config.get("neo4j", "batch_size"))
        self.uri = uri

        if clear_database:
            logger.info("Wiping database")
            with self.neo4j.session() as session:
                session.write_transaction(lambda tx: tx.run("MATCH (n) DETACH DELETE n"))

    def graph(self) -> str:

        logger.info(f"Generating graph using NetworkX")

        nx_graph = super().graph()

        logger.info(f"Migrating graph to Neo4j")

        logger.info(f"Inserting nodes into Neo4J in batches of {self.batch_size}")

        self._make_nodes(nx_graph)

        logger.info(f"Inserting edges into Neo4J in batches of {self.batch_size}")

        self._make_edges(nx_graph)

        logger.info("All data inserted into Neo4J")
        return self.uri.replace("bolt", "http")

    def _make_nodes(self, source_graph: nx.Graph) -> None:

        logger.info("Grouping Nodes by type")

        # Group nodes by class
        sorted_nodes = sorted(
            [node["data"] for _, node in source_graph.nodes(data=True)],
            key=lambda node: node.__name__,
            reverse=True,
        )

        nodes_by_type = itertools.groupby(sorted_nodes, key=lambda node: node.__name__)

        for node_type, nodes in nodes_by_type:

            # remove whitespaces
            node_type = node_type.replace(" ", "_")

            self._create_constraint(node_type)

            cypher_nodes = list(map(self._node_as_cypher, nodes))

            logger.debug(f"Inserting {len(cypher_nodes)} {node_type} nodes into Neo4J")

            for i in range(0, len(cypher_nodes), self.batch_size):

                start = i
                end = i + self.batch_size

                cypher = f"UNWIND [{', '.join(cypher_nodes[start: end])}] as row\n"

                cypher += f"CREATE (node:{node_type} {{_key: row._key}}) SET node = row"

                with self.neo4j.session() as session:
                    session.write_transaction(lambda tx: tx.run(cypher))

                logger.debug(f"Finished batch {i+1} ({start} -> {end})")

    def _make_edges(self, source_graph: nx.Graph) -> None:

        logger.info("Grouping Edges by type")

        sorted_edges = sorted(
            source_graph.edges(data=True, keys=True), key=lambda edge: edge[3]["edge_name"]
        )

        edges_by_type = itertools.groupby(sorted_edges, key=lambda edge: edge[3]["edge_name"])

        for edge_type, edges in edges_by_type:

            # Remove white spaces
            edge_type = edge_type.replace(" ", "_")

            cypher_edges = list(map(self._edge_as_cypher, edges))

            logger.debug(f"Inserting {len(cypher_edges)} {edge_type} edges into Neo4J")

            for i in range(0, len(cypher_edges), self.batch_size):

                start = i
                end = i + self.batch_size

                cypher = f"UNWIND [{', '.join(cypher_edges[start: end])}] as row\n"
                cypher += "MATCH (src {_key: row.src}), (dst {_key: row.dst})"
                cypher += f" CREATE (src)-[:`{edge_type}`]->(dst)"

                with self.neo4j.session() as session:
                    session.write_transaction(lambda tx: tx.run(cypher))

                logger.debug(f"Finished batch {i+1} ({start} -> {end})")

    def _create_constraint(self, node_type: str) -> None:
        constraint_format = "CREATE CONSTRAINT ON (n:{name}) ASSERT n._key is UNIQUE"

        logger.debug(f"Creating _key constraint for {node_type}")
        with self.neo4j.session() as session:
            session.run(constraint_format.format(name=node_type))

    def _node_as_cypher(self, node: Node) -> str:

        # Convert the node to a dictionary
        node_props = node.to_dict()
        node_props["_key"] = hash(node)

        def fix_value(value: Any) -> str:
            return str(value).replace("\\", "\\\\").replace("'", "\\'")

        kv_pairs = []
        for key, value in node_props.items():
            if isinstance(value, dict):
                for _key, _value in value.items():
                    kv_pairs.append(f"{_key}: '{fix_value(_value)}'")
            else:
                kv_pairs.append(f"{key}: '{fix_value(value)}'")

        return "{" + ", ".join(kv_pairs) + "}"

    def _edge_as_cypher(self, edge: tuple) -> str:
        # TODO: Add edge data.

        return f"{{src: '{edge[0]}', dst: '{edge[1]}'}}"
