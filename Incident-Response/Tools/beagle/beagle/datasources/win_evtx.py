import datetime
from typing import TYPE_CHECKING, Generator

import Evtx.Evtx as evtx
from lxml import etree

from beagle.common.logging import logger
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.evtx_transformer import WinEVTXTransformer

if TYPE_CHECKING:
    from beagle.transformer.base_transformer import Transformer
    from typing import List


class WinEVTX(DataSource):
    """Parses Windows .evtx files. Yields events one by one using the `python-evtx` library.

    Parameters
    ----------
    evtx_log_file : str
        The path to the windows evtx file to parse.
    """

    name = "Windows EVTX File"
    transformers = [WinEVTXTransformer]  # type: List[Transformer]
    category = "Windows Event Logs"

    def __init__(self, evtx_log_file: str) -> None:

        self.file_path = evtx_log_file

        logger.info(f"Setting up WinEVTX for {self.file_path}")

    def events(self) -> Generator[dict, None, None]:
        with evtx.Evtx(self.file_path) as log:
            for record in log.records():
                # Get the lxml object
                yield self.parse_record(record.lxml())

    def metadata(self) -> dict:
        """Get the hostname by inspecting the first record.

        Returns
        -------
        dict
            >>> {"hostname": str}
        """

        with evtx.Evtx(self.file_path) as log:
            for record in log.records():
                # Get the lxml object
                event = self.parse_record(record.lxml())
                break

        return {"hostname": event["computer"]}

    def parse_record(self, record: etree.ElementTree, name="") -> dict:
        """Recursivly converts a etree.ElementTree record to a JSON dictionary
        with one level.


        Parameters
        ----------
        record : etree.ElementTree
            Current record to parse
        name : str, optional
            Name of the current key we are at.

        Returns
        -------
        dict
            JSON represntation of the event
        """

        data = {}

        for node in record:
            next_name = node.tag.split("}")[-1]
            # Recurse
            data.update(self.parse_record(node, next_name))

        if record.attrib and record.text:

            key = f"{name}_{record.keys()[0]}".lower()

            # Use attributes if we're in EventData
            if "EventData" in record.getparent().tag:
                key += f"_{record.values()[0]}".lower()

            data[key] = record.text
        elif record.attrib:
            for k, val in record.attrib.items():
                key = f"{name}_{k}".lower()
                data[key] = val
        else:
            curr_name = record.tag.split("}")[-1]
            key = f"{curr_name}".lower()
            data[key] = record.text

        if key == "timecreated_systemtime":
            time = datetime.datetime.strptime(
                data["timecreated_systemtime"], "%Y-%m-%d %H:%M:%S.%f"
            )

            epoch = int(time.strftime("%s"))

            data["timecreated_systemtime"] = epoch

        return data
