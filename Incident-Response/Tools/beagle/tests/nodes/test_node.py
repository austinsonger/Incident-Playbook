from collections import defaultdict
from typing import List, DefaultDict

import pytest

from beagle.nodes import Node
from beagle.edges import Edge


def testNoKeyFields():
    """A class without the key_fields annotation should raise a RuntimeError"""

    with pytest.raises(RuntimeError):

        class AnnotatedNode(Node):
            x: str
            y: int

            def __init__(self, x: str, y: int):
                self.x = x
                self.y = y

            @property
            def _display(self) -> str:
                return self.x


def testEquals():
    class AnnotatedNode(Node):

        x: str
        y: int
        key_fields: List[str] = ["x", "y"]

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    n1 = AnnotatedNode("1", 1)
    n2 = AnnotatedNode("1", 1)

    assert n1 == n2


def test_tojson():
    class AnnotatedNode(Node):
        x: str
        y: int
        key_fields: List[str] = ["x", "y"]
        foo = defaultdict(str)

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    n1 = AnnotatedNode("1", 1)
    assert n1.to_dict() == {"x": "1", "y": 1}


def testNotEquals():
    class AnnotatedNode(Node):
        x: str
        y: int
        key_fields: List[str] = ["x", "y"]

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    n1 = AnnotatedNode("1", 1)
    n2 = AnnotatedNode("1", 2)

    assert n1 != n2


def testNotEqualsTwoClasses():
    class AnnotatedNode(Node):
        x: str
        y: int
        key_fields: List[str] = ["x", "y"]

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    class OtherAnnotatedNode(Node):
        x: str
        y: int
        key_fields: List[str] = ["x", "y"]

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    n1 = AnnotatedNode("1", 1)
    n2 = OtherAnnotatedNode("1", 1)

    assert n1 != n2


def testHash():
    class AnnotatedNode(Node):
        x: str
        y: int
        key_fields: List[str] = ["x", "y"]

        def __init__(self, x: str, y: int):
            self.x = x
            self.y = y

        @property
        def _display(self) -> str:
            return self.x

    n1 = AnnotatedNode("1", 1)
    n2 = AnnotatedNode("1", 1)

    assert hash(n1) == hash(n2)

    n3 = AnnotatedNode("1", 21)
    assert hash(n1) != hash(n3)


class DummyEdge(Edge):
    __name__ = "dummy"

    field1: str
    field2: bool

    def __init__(self):
        super().__init__()


class DummyNode(Node):
    x: str
    y: int
    z: int

    key_fields: List[str] = ["x", "y"]

    dummyedge: DefaultDict["DummyNode", DummyEdge]  # List of Resolution

    def __init__(self, x: str, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
        self.dummyedge = defaultdict(DummyEdge)

    @property
    def _display(self) -> str:
        return self.x


def testMergeRejectsUnequalNodes():
    """First node's fields should be updated with the second nodes"""

    n1 = DummyNode(x=1, y=2, z=4)
    n2 = DummyNode(x=1, y=3, z=3)

    with pytest.raises(TypeError):
        n1.merge_with(n2)


def testMergeNoEdges():
    """First node's fields should be updated with the second nodes"""

    n1 = DummyNode(x=1, y=2, z=4)
    n2 = DummyNode(x=1, y=2, z=3)

    assert n1.z == 4

    n1.merge_with(n2)

    assert n1.z == 3


def testMergesEdgesAdded():

    # n1 == n2
    n1 = DummyNode(x=1, y=2, z=1)
    n2 = DummyNode(x=1, y=2, z=1)

    # third node
    n3 = DummyNode(x=2, y=3, z=3)

    # Make an edge from n2 -> n3
    n2.dummyedge[n3].append(field1="foo", field2="bar")

    assert n3 not in n1.dummyedge

    # Update n1 with n2
    n1.merge_with(n2)
    assert n3 in n1.dummyedge
    assert {"field1": "foo", "field2": "bar"} in n1.dummyedge[n3]


def testMergesMultipleEdges():

    # n1 == n2
    n1 = DummyNode(x=1, y=2, z=1)
    n2 = DummyNode(x=1, y=2, z=1)

    # third node
    n3 = DummyNode(x=2, y=3, z=3)

    # Fourth node
    n4 = DummyNode(x=3, y=4, z=3)

    n1.dummyedge[n4].append(field1="bar", field2="foo")

    # Make an edge from n2 -> n3
    n2.dummyedge[n3].append(field1="foo", field2="bar")

    assert n3 not in n1.dummyedge
    assert n4 in n1.dummyedge
    assert n4 not in n2.dummyedge
    assert n3 in n2.dummyedge

    # Update n1 with n2
    n1.merge_with(n2)

    # N1 should contain everything
    assert n3 in n1.dummyedge
    assert n4 in n1.dummyedge

    assert {"field1": "foo", "field2": "bar"} in n1.dummyedge[n3]
    assert {"field1": "bar", "field2": "foo"} in n1.dummyedge[n4]
