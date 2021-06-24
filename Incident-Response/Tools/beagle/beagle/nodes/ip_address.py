from collections import defaultdict
from typing import DefaultDict, List, Optional, TYPE_CHECKING

from beagle.nodes.node import Node
from beagle.edges import ConnectedTo, DNSQueryFor, HTTPRequestTo

if TYPE_CHECKING:
    from beagle.nodes import URI, Domain  # noqa


class IPAddress(Node):

    __name__ = "IP Address"
    __color__ = "#87CEEB"

    ip_address: Optional[str]
    mac: Optional[str]

    key_fields: List[str] = ["ip_address"]

    connected_to: DefaultDict["IPAddress", ConnectedTo]
    http_request_to: DefaultDict["URI", HTTPRequestTo]
    dns_query_for: DefaultDict["Domain", DNSQueryFor]  # List of DNS Lookups

    def __init__(self, ip_address: str = None, mac: str = None):
        self.ip_address = ip_address
        self.mac = mac

        self.connected_to = defaultdict(ConnectedTo)

        self.http_request_to = defaultdict(HTTPRequestTo)
        self.dns_query_for = defaultdict(DNSQueryFor)

    @property
    def _display(self) -> str:
        return self.ip_address or super()._display
