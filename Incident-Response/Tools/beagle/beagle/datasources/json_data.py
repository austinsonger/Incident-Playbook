import os
import json
from typing import Dict, Generator, List

from beagle.datasources.base_datasource import DataSource
from beagle.transformers import GenericTransformer


class JSONFile(DataSource):

    name = "JSON File"
    transformers = [GenericTransformer]
    category = "Generic Data"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def metadata(self) -> dict:
        return {"filename": os.path.basename(self.file_path)}

    def events(self) -> Generator[dict, None, None]:

        handle = open(self.file_path)

        first_char = handle.read(1)

        handle.seek(0)

        if first_char == "[":
            data: List[Dict] = json.load(handle)
            for event in data:
                yield event
        else:
            for line in handle.readlines():
                yield json.loads(line)


class JSONData(DataSource):
    """A generic data source which returns events one by one
    """

    name = "JSON Data"
    transformers = [GenericTransformer]
    category = "Generic Data"

    def __init__(self, events: List[Dict]) -> None:
        self._events = events

    def events(self) -> Generator[dict, None, None]:
        for event in self._events:
            yield event

    def metadata(self) -> dict:
        return {}
