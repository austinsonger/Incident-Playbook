from beagle.edges import Edge


class AlertedOn(Edge):
    __name__ = "Alerted On"

    timestamp: int

    def __init__(self) -> None:
        super().__init__()
