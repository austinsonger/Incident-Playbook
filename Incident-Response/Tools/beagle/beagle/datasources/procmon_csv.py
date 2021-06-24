import datetime
import os
from typing import Generator

import pandas as pd

from beagle.common.logging import logger
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.procmon_transformer import ProcmonTransformer


class ProcmonCSV(DataSource):
    """Reads events in one by one from a ProcMon CSV, and parses them into the GenericTransformer"""

    name = "Procmon CSV"  # The name as it'll appear in the web GUI
    category = "Procmon"  # The category this will output to.
    transformers = [ProcmonTransformer]  # The transformer this will send events to

    def __init__(self, procmon_csv: str) -> None:

        self._df = pd.read_csv(procmon_csv)

        # Procmon doesn't have dates time.
        self.now = datetime.datetime.now()
        logger.info("Set up ProcmonCSVs")

    def metadata(self) -> dict:
        return {}

    def events(self) -> Generator[dict, None, None]:

        for _, row in self._df.iterrows():
            # Get times
            hr_min_sec = row["Time of Day"].split(".")[0]

            # Check if AM
            in_am = "AM" in row["Time of Day"]

            # set the hours/min/sec
            date = self.now.replace(
                second=int(hr_min_sec.split(":")[-1]),
                hour=int(hr_min_sec.split(":")[0]) + (0 if in_am else 12),
                minute=int(hr_min_sec.split(":")[1]),
            )

            epoch = int(date.strftime("%s"))

            yield {
                "event_time": epoch,
                "event_type": row["Operation"],
                "process_name": row["Process Name"],
                "path": row["Path"],
                "process_id": int(row["PID"]),
                "params": row["Detail"],
            }

