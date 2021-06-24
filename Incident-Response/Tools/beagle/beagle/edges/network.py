# Network connection edges
from beagle.edges import Edge
from typing import Optional


class ConnectedTo(Edge):

    __name__ = "Connected To"
    port: int
    protocol: Optional[str]
    timestamp: int
    payload: Optional[str]

    def get_name(self, entry) -> str:
        return entry.get("protocol") or self.__name__

    def __init__(self) -> None:
        super().__init__()


class HTTPRequestTo(Edge):
    __name__ = "HTTP Request To"

    user_agent: Optional[str]
    method: Optional[str]
    header: Optional[str]
    timestamp: int

    def __init__(self) -> None:
        super().__init__()

    @property
    def _display(self):
        return self.method or super()._display()


class DNSQueryFor(Edge):
    __name__ = "DNS Query For"

    timestamp: int
    record_type: Optional[str]

    def __init__(self) -> None:
        super().__init__()


class URIOf(Edge):
    __name__ = "URI Of"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class ResolvesTo(Edge):
    __name__ = "Resolves To"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()
