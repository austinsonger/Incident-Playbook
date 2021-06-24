import datetime
from typing import TYPE_CHECKING

import Evtx.Evtx as evtx
from lxml import etree

from beagle.datasources.win_evtx import WinEVTX
from beagle.transformers.sysmon_transformer import SysmonTransformer

if TYPE_CHECKING:
    from beagle.transformer.base_transformer import Transformer
    from typing import List


class SysmonEVTX(WinEVTX):
    """Parses SysmonEVTX files, see :py:class:`beagle.datasources.win_evtx.WinEVTX`
    """

    name = "Sysmon EVTX File"
    transformers = [SysmonTransformer]  # type: List[Transformer]
    category = "SysMon"

    def __init__(self, sysmon_evtx_log_file: str) -> None:
        super().__init__(sysmon_evtx_log_file)

    def metadata(self) -> dict:
        """Returns the Hostname by inspecting the `Computer` entry of the
        first record.

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

        return {"hostname": event["Computer"]}

    def parse_record(self, record: etree.ElementTree, name="") -> dict:
        """Parse a single record recursivly into a JSON file with a single level.

        Parameters
        ----------
        record : etree.ElementTree
            The current record.
        name : str, optional
            Last records name. (the default is "", which [default_description])

        Returns
        -------
        dict
            dict representation of record.
        """

        out = {}
        for node in record:
            parent = node.tag.split("}")[-1]
            for child in node:
                if parent == "EventData":
                    event_data_type = child.attrib["Name"]
                    out[parent + "_" + event_data_type] = child.text
                else:
                    child_name = child.tag.split("}")[-1]
                    if child.attrib:
                        for key, value in child.attrib.items():
                            out[child_name + "_" + key] = value
                        out[child_name] = child.text
                    else:
                        out[child_name] = child.text

        # Convert UTC to epoch
        time = datetime.datetime.strptime(out["EventData_UtcTime"], "%Y-%m-%d %H:%M:%S.%f")

        out["EventData_UtcTime"] = int(time.strftime("%s"))
        return out
