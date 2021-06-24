from beagle.edges import Edge
from typing import Optional


class ChangedValue(Edge):
    __name__ = "Changed Value"

    value: Optional[str]
    timestamp: int

    def __init__(self) -> None:
        super().__init__()


class CreatedKey(Edge):
    __name__ = "Created Key"

    timestamp: int
    value: Optional[str]

    def __init__(self) -> None:
        super().__init__()


class ReadKey(Edge):
    __name__ = "Read Key"

    timestamp: int
    value: Optional[str]

    def __init__(self) -> None:
        super().__init__()


class DeletedValue(Edge):
    __name__ = "Deleted Value"

    timestamp: int
    value: Optional[str]

    def __init__(self) -> None:
        super().__init__()


class DeletedKey(Edge):
    __name__ = "Deleted Key"

    timestamp: int
    value: Optional[str]

    def __init__(self) -> None:
        super().__init__()
