import time
import ssl
import urllib
from typing import Generator

from beagle.common.logging import logger
from beagle.config import Config
from beagle.datasources.base_datasource import ExternalDataSource
from beagle.transformers.generic_transformer import GenericTransformer


def request(url, message, **kwargs):  # pragma: no cover
    method = message["method"].lower()
    data = message.get("body", "") if method == "post" else None

    if isinstance(data, str):
        data = data.encode("utf-8")

    headers = dict(message.get("headers", []))

    req = urllib.request.Request(url, data, headers)
    try:
        response = urllib.request.urlopen(req, context=ssl._create_unverified_context())
    except urllib.error.HTTPError as response:
        return {
            "status": response.code,
            "reason": response.msg,
            "headers": dict(response.info()),
            "body": response,
        }

    return {
        "status": response.code,
        "reason": response.msg,
        "headers": dict(response.info()),
        "body": response,
    }


def handler():  # pragma: no cover
    return request


class SplunkSPLSearch(ExternalDataSource):
    """Datasource which allows transforming the results of a Splunk search into a
    graph.

    Parameters
    ----------
    spl : str
        The splunk search to transform

    Raises
    ------
    RuntimeError
        If there are no Splunk credentials configured.
    """

    name = "Splunk SPL Search"
    transformers = [GenericTransformer]
    category = "Splunk"

    def __init__(self, spl: str, earliest: str = "-24h@h", latest: str = "now"):
        """Creates a splunk query to pull data from

        Parameters
        ----------
        spl : str
            The SPL to run
        earilest : str, optional
            The earliest time modifier, by default "24h@h"
        latest : str, optional
            The latest time modifier, by default "now"
        """

        self.earliest = earliest
        self.latest = latest
        self.spl = self.patch_spl(spl)
        self.client = self.setup_session()

    def patch_spl(self, spl: str) -> str:
        """Ensures `search ` is the first command in the SPL.
        """
        if spl[0] == "|":
            return spl
        elif spl[0:6] == "search":
            return spl
        else:
            return "search " + spl

    def setup_session(self):  # pragma: no cover
        import splunklib.client as client

        client_kwargs = {
            "host": Config.get("splunk", "host"),
            "username": Config.get("splunk", "username"),
            "password": Config.get("splunk", "password"),
            "port": int(Config.get("splunk", "port", fallback=8089)),
        }

        logger.info(f"Creating Splunk client for host={client_kwargs['host']}")

        return client.connect(sharing="global", **client_kwargs, handler=handler())

    def events(self) -> Generator[dict, None, None]:
        from splunklib.client import Job

        job: Job = self.create_search(
            self.spl,
            query_kwargs={
                "exec_mode": "normal",
                "earliest_time": self.earliest,
                "latest_time": self.latest,
            },
        )

        self.sid = job.sid

        logger.info(f"Creating splunk search with sid={self.sid}, waiting for job=Done")

        while not job.is_done():
            logger.debug("Job not done, sleeping")
            time.sleep(5)

        logger.info(f"Job is done, getting results")
        count = 0
        for result in self.get_results(job, count=100000000):
            count += 1
            yield result
        logger.info(f"Processed {count} splunk results")

    def metadata(self) -> dict:  # pragma: no cover
        return {"spl": self.spl}

    def create_search(self, query: str, query_kwargs: dict):
        """Creates a splunk search with `query` and `query_kwargs` using `splunk_client`

        Returns
        -------
        Job
            A splunk Job object.
        """

        return self.client.jobs.create(query, **query_kwargs)

    def get_results(self, job, count: int) -> list:  # pragma: no cover
        """Return events from a finished Job as an array of dictionaries.

        Parameters
        ----------
        job : Job
            Job object to pull results from.

        Returns
        -------
        list
            The results of the search.
        """
        import splunklib.results as results

        out = [result for result in results.ResultsReader(job.results(count=count))]
        job.cancel()
        return out
