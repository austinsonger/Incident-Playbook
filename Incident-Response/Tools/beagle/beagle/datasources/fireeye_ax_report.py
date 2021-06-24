import datetime
import json
from typing import Generator

from beagle.common.logging import logger
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.fireeye_ax_transformer import FireEyeAXTransformer


class FireEyeAXReport(DataSource):
    """Yields events one by one from a FireEyeAX Report and sends them
    to the generic transformer.

    The JSON report should look something like this::

        {
            "alert": [
                {
                    "explanation": {
                        "malwareDetected": {
                            ...
                        },
                        "cncServices": {
                            "cncService": [
                                ...
                        },
                        "osChanges": [
                            {
                                "process": [...],
                                "registry": [...],
                                ...
                        }
                    }
                }
            ]
        }

    Beagle looks at the *first* `alert` in the `alerts` array.

    Parameters
    ----------
    ax_report : str
        File path to the JSON AX Report, see class description for expected format.
    """

    name = "FireEye AX Report"
    category = "FireEye AX"
    transformers = [FireEyeAXTransformer]

    def __init__(self, ax_report: str):

        data = json.load(open(ax_report, "r"))

        self.version: str = data.get("version", "8.1.0")

        self.appliance = data.get("appliance", "Unknown")

        if "alert" not in data or len(data["alert"]) == 0:
            self.alert = {}  # type: ignore
        else:
            self.alert = data["alert"][0]

            occured = self.alert["occurred"].replace(" +0000", "")
            # Multiple possible timestamp string.
            for fmt_string in ["%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                try:
                    self.base_timestamp = int(
                        datetime.datetime.strptime(occured, fmt_string).timestamp()
                    )
                    break  # break if succesfully parsed.
                except ValueError:
                    continue

            # If break not reached.
            else:
                raise ValueError(
                    f"{self.alert['occurred']} did not match any known time format strings for AX"
                )

        logger.info("Set up FireEyeAX Report")

    def metadata(self) -> dict:

        if self.version.startswith("8.2.0"):
            base_meta = {
                "hostname": self.appliance,
                "analyzed_on": self.alert["occurred"],
                "severity": self.alert["severity"],
                "alert_url": self.alert.get("alert-url"),
                "alert": self.alert["explanation"]["malware-detected"]["malware"][0]["name"]
                if self.alert != {}
                else "",
            }
        else:
            base_meta = {
                "hostname": self.appliance,
                "analyzed_on": self.alert["occurred"],
                "severity": self.alert["severity"],
                "alert_url": self.alert.get("alertUrl"),
                "alert": self.alert["explanation"]["malwareDetected"]["malware"][0]["name"]
                if self.alert != {}
                else "",
            }

        return base_meta

    def events(self) -> Generator[dict, None, None]:

        if self.version.startswith("8.2.0"):
            # os-changes is a dict in 8.2
            os_changes = self.alert.get("explanation", {}).get("os-changes", {})
        else:
            os_changes = self.alert.get("explanation", {}).get("osChanges", [{}])

        if (len(os_changes)) == 0:
            return
        else:
            if isinstance(os_changes, list):
                os_changes = os_changes[0]

            for change_type, events in os_changes.items():

                if not isinstance(events, list):
                    events = [events]

                for event in events:

                    if not isinstance(event, dict):
                        continue

                    event["event_type"] = change_type
                    if "timestamp" in event:
                        event["timestamp"] = float(int(event["timestamp"]) + self.base_timestamp)

                    yield event
