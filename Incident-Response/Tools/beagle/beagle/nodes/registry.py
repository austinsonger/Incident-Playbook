from typing import List, Optional

from beagle.nodes.node import Node


class RegistryKey(Node):

    __name__ = "Registry Key"
    __color__ = "#808000"

    host: Optional[str]
    hive: Optional[str]
    key_path: Optional[str]
    key: Optional[str]
    value: Optional[str]
    value_type: Optional[str]

    key_fields: List[str] = ["hive", "key_path", "key"]

    def __init__(
        self,
        host: str = None,
        hive: str = None,
        key_path: str = None,
        key: str = None,
        value: str = None,
        value_type: str = None,
    ) -> None:
        self.host = host
        self.hive = hive
        self.key_path = key_path
        self.key = key
        self.value = value
        self.value_type = value_type

    @property
    def _display(self) -> str:
        return self.key or super()._display
