import mock
from beagle.backends.graphistry import Graphistry


class MockGraphistry(Graphistry):
    def __init__(self):
        pass


def test_anonymize_graph():
    graphistry = MockGraphistry()
    graphistry.to_json = mock.MagicMock()

    graphistry.to_json.return_value = {
        "nodes": [{"id": 1, "properties": 4}, {"id": 2, "properties": 3}],
        "links": [{"source": 2, "target": 1, "data": "foo"}],
    }

    G = graphistry.anonymize_graph()

    for node in G.nodes(data=True):
        # tuple of id, data
        assert "properties" not in node[1]
