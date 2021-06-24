# Datasource to support the "Transparent Computing Engagement" dataset
# https://github.com/darpa-i2o/Transparent-Computing
from typing import Generator

from beagle.datasources.json_data import JSONFile
from beagle.transformers import DRAPATCTransformer


class DARPATCJson(JSONFile):
    name = "Darpa TC3 JSON"
    transformers = [DRAPATCTransformer]  # type: ignore
    category = "Darpa TC3"

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        super().__init__(self.file_path)

    def events(self) -> Generator[dict, None, None]:
        """Events are in the format:

        "datum": {
            "com.bbn.tc.schema.avro.cdm18.Subject": {
             ...
        }

        This pops out the relevant info under the first key.
        """
        for event in super().events():
            event = event["datum"]

            for key, data in event.items():
                if "com.bbn.tc.schema.avro.cdm18." in key:
                    data["event_type"] = key.split("com.bbn.tc.schema.avro.cdm18.")[-1].lower()
                    yield data
                    break
