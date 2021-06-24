from collections import defaultdict
from typing import DefaultDict, List, Optional

from beagle.nodes.node import Node
from beagle.nodes.ip_address import IPAddress

from beagle.edges import URIOf, ResolvesTo


class Domain(Node):

    __name__ = "Domain"
    __color__ = "#A52A2A"

    domain: Optional[str]

    key_fields: List[str] = ["domain"]

    resolves_to: DefaultDict[IPAddress, ResolvesTo]  # List of Resolution

    def __init__(self, domain: str = None):
        self.domain = domain
        self.resolves_to = defaultdict(ResolvesTo)

    @property
    def _display(self) -> str:
        return self.domain or super()._display

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.resolves_to]


class URI(Node):

    __name__ = "URI"
    __color__ = "#FF00FF"

    uri: Optional[str]

    uri_of: DefaultDict[Domain, URIOf] = defaultdict(URIOf)

    key_fields: List[str] = ["uri"]

    def __init__(self, uri: str = None):
        self.uri = uri

    @property
    def _display(self) -> str:
        return self.uri or super()._display

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.uri_of]
