from abc import ABCMeta
from collections import defaultdict
from typing import Any, Dict, List, Tuple


class Node(object, metaclass=ABCMeta):
    """Base Node class. Provides an interface which each Node must implement"""

    __name__ = "Node"
    __color__ = "#FFFFFF"

    key_fields: List[str] = []

    def __init_subclass__(cls, **kwargs):
        if "key_fields" not in cls.__annotations__:
            raise RuntimeError(f"A Node sublcass **must** contain the key_fields annotation")

    @property
    def __key(self) -> Tuple[str, ...]:
        """The __key is a tuple which contains the elements which make this Node unique.

        For example, for a process, this could be the process_image and process_id fields,
        which mean that two nodes with the same process_image and process_id fields are equal.

        The fields which compose the `__key` are defined by each class using the `key_fields`
        annotation


        Returns
        -------
        Tuple[str, ...]
            A tuple containing the values corresponding to the key_fields.

        Examples
        -------

        Sample node class::

            class AnnotatedNode(Node):
                x: str
                y: int
                z: bool
                key_fields = ["x", "y"]

                def __init__(self, x: str, y: int, z: bool):
                    self.x = x
                    self.y = y
                    self.z = z

                @property
                def _display(self) -> str:
                    return self.x



        >>> n = AnnotatedNode("1", 1, True)
        >>> n.__key
        ("1", 1)

        """
        return tuple(getattr(self, val) for val in self.key_fields)

    def __eq__(self, other: object) -> bool:
        """Two Node objects are equal if their __key tuple are equal"""

        return isinstance(other, self.__class__) and self.__key == other.__key

    def __hash__(self) -> int:
        """The hashcode of a Node is the hash of its __key tuple, and it's class.

        The __name__ param is injected into the hash so that if two Nodes from two
        different classes happen to have the same __key value, they are do not have
        a colliding hash.
        """
        return hash(self.__key + (self.__class__.__name__,))

    def __repr__(self) -> str:
        return (
            f"(<{self.__class__.__name__}> "
            + " ".join([f"{key}={getattr(self, key, None)}" for key in self.key_fields])
            + ")"
        )

    def merge_with(self, node: "Node") -> None:
        """Merge the current node with the destination node. After a call to `merge_with` the
        calling node will be updated with the information from the passed in node. This
        is similar to a dict `update` call.

        Parameters
        ----------
        node : Node
            The node to use to update the current node.

        Raises
        ------
        TypeError
            Passed in node does not represent the same entity represented by the current node.
        """

        if hash(self) != hash(node):
            raise TypeError(f"Argument {node} must represent same node object")

        # Otherwise, update the node

        for key, value in node.__dict__.items():

            # NOTE: Skips edge combination because edge data is
            # added anyway in self.insert_node()
            if isinstance(value, defaultdict):

                for dest_node, edge_data in value.items():

                    events = edge_data._events

                    relationship = getattr(self, key)[dest_node]

                    for event in events:
                        event.pop("edge_name")
                        relationship.append(**event)

            # Always use the latest value.
            elif value:
                setattr(self, key, value)

    @property
    def edges(self) -> List:
        """Returns an empty list, so that all nodes can have their
        edges iterated on, even if they have no outgoing edges.

        Returns
        -------
        List
            []
        """

        return [attr for attr in self.__dict__.values() if isinstance(attr, defaultdict)]

    @property
    def _display(self) -> str:
        """The value which should be used when displaying this node.

        Instead of displaying all fields of the node, _display can be used to
        return a string which conveys the most important property for this node.

        For example, for a process this could be the process_name only, and for a file
        it could be the file_name only.

        Returns
        -------
        str
            Value to use when displaying node.
        """

        return "NO_DISPLAY_VALUE"

    def to_dict(self) -> Dict[str, Any]:
        """Converts a Node object to a dictionary without its edge objects.

        Returns
        -------
        dict
            A dict representation of a node.

        Examples
        --------

        Sample node::

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

        >>> AnnotatedNode("1", 1).to_dict()
        {"x": "1", "y": 1}
        """

        return {
            key: value for key, value in self.__dict__.items() if not isinstance(value, defaultdict)
        }
