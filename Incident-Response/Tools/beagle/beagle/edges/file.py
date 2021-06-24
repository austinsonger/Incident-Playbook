# File based edges
from beagle.edges import Edge
from typing import Optional


class FileOf(Edge):
    __name__ = "File Of"


class CopiedTo(Edge):
    __name__ = "Copied To"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class Wrote(Edge):
    __name__ = "Wrote"

    contents: Optional[str]  # Array of contents of writes
    timestamp: int  # Array of timestamps of writes

    def __init__(self) -> None:
        super().__init__()


class Accessed(Edge):
    __name__ = "Accessed"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class Deleted(Edge):
    __name__ = "Deleted"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class Copied(Edge):
    __name__ = "Copied"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class Loaded(Edge):
    __name__ = "Loaded"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()
