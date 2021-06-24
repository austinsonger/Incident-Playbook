from beagle.edges import Edge
import pytest


def make_edge_obj():
    class DummyEdge(Edge):
        __name__ = "dummy"

        field1: str
        field2: bool

    def __init__(self):
        super().__init__()

    return DummyEdge()


def test_edge_class():

    edge = make_edge_obj()

    edge.append(field1="blah", field2=True)

    assert {"field1": "blah", "field2": True} in edge


def test_multiple_appends():
    edge = make_edge_obj()

    edge.append(field1="blah", field2=True)

    assert {"field1": "blah", "field2": True} in edge

    edge.append(field1="blah2", field2=False)

    assert {"field1": "blah2", "field2": False} in edge

    assert len(edge) == 2


def test_invalid_keys_error():
    with pytest.raises(RuntimeError):
        edge = make_edge_obj()

        edge.append(notafield="foo")


def test_invalid_keys_error_add():
    with pytest.raises(RuntimeError):
        edge = make_edge_obj()

        edge += {"notafield": "123"}


def test_display():
    edge = make_edge_obj()
    assert edge._display == "dummy"
