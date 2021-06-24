from collections import defaultdict
from typing import DefaultDict, List, Optional

from beagle.nodes.node import Node
from beagle.edges import AlertedOn


class Alert(Node):

    __name__ = "Alert"
    __color__ = "#FFFF00"

    alert_data: Optional[str]
    alert_name: Optional[str]

    key_fields: List[str] = ["alert_name", "alert_data"]

    alerted_on: DefaultDict[Node, AlertedOn]  # Things this alert alerted on.

    def __init__(self, alert_name: str = None, alert_data: str = None):

        self.alert_data = alert_data
        self.alert_name = alert_name

        self.alerted_on = defaultdict(AlertedOn)

    @property
    def _display(self) -> str:
        return self.alert_name or super()._display

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.alerted_on]
