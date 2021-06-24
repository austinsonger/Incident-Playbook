from collections import defaultdict
from typing import TYPE_CHECKING, DefaultDict, Dict, List, Optional

from beagle.nodes.node import Node
from beagle.edges import FileOf, CopiedTo

# mypy type hinting
if TYPE_CHECKING:
    from beagle.nodes import Process  # noqa: F401


class File(Node):
    __name__ = "File"
    __color__ = "#3CB371"

    host: Optional[str]
    full_path: Optional[str]
    file_path: Optional[str]
    file_name: Optional[str]
    extension: Optional[str]
    timestamp: Optional[int]
    hashes: Optional[Dict[str, str]] = {}

    file_of: DefaultDict["Process", FileOf]
    copied_to: DefaultDict["File", CopiedTo]

    key_fields: List[str] = ["host", "full_path"]

    def __init__(
        self,
        host: str = None,
        file_path: str = None,
        file_name: str = None,
        full_path: str = None,
        extension: str = None,
        hashes: Optional[Dict[str, str]] = {},
    ) -> None:
        self.host = host
        self.file_path = file_path
        self.file_name = file_name

        if full_path:
            self.full_path = full_path
        elif file_path and file_name:
            if file_path[-1] == "\\":
                self.full_path = f"{file_path}{file_name}"
            else:
                self.full_path = f"{file_path}\\{file_name}"
        else:
            # Fixes bug where we don't know the path of a process
            self.full_path = ""

        self.extension = extension
        self.hashes = hashes

        self.file_of = defaultdict(FileOf)
        self.copied_to = defaultdict(CopiedTo)

    def set_extension(self) -> None:
        if self.full_path:
            self.extension = self.full_path.split(".")[-1]

    @property
    def edges(self) -> List[DefaultDict]:
        return [self.file_of, self.copied_to]

    @property
    def _display(self) -> str:
        return self.file_name or super()._display
