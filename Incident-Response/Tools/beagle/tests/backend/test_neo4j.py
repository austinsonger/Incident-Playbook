import pytest
from beagle.backends.neo4j import Neo4J
from beagle.nodes import Process


class MockNeo4j(Neo4J):
    # Wipes init.
    def __init__(self):
        pass


@pytest.mark.parametrize(
    "node,keys",
    [
        (
            # Regular node
            Process(process_id=10, process_image="test.exe"),
            ["process_id: '10'", "process_image: 'test.exe'"],
        ),
        (
            # Backslashes
            Process(process_id=10, process_image="test.exe", process_image_path="c:\\users"),
            ["process_id: '10'", "process_image: 'test.exe'", "process_image_path: 'c:\\\\users'"],
        ),
        (
            # commas
            Process(
                process_id=10,
                process_image="test.exe",
                process_image_path="c:\\users",
                command_line="hello chap's",
            ),
            ["command_line: 'hello chap\\'s'"],
        ),
        (
            # Dict values
            Process(process_id=10, process_image="test.exe", hashes={"md5": "1"}),
            ["process_id: '10'", "process_image: 'test.exe'", "md5: '1'"],
        ),
    ],
)
def test_node_as_cypher(node, keys):
    neo4j = MockNeo4j()
    cypher = neo4j._node_as_cypher(node)
    for key in keys:
        assert key in cypher


def test_edge_as_cypher():
    neo4j = MockNeo4j()

    assert neo4j._edge_as_cypher((123, 456)) == "{src: '123', dst: '456'}"
