import requests

from beagle.common.logging import logger
from beagle.config import Config
from beagle.datasources.base_datasource import ExternalDataSource
from beagle.transformers.generic_transformer import GenericTransformer
from beagle.datasources.virustotal import GenericVTSandbox


class GenericVTSandboxAPI(ExternalDataSource, GenericVTSandbox):
    """A class which provides an easy way to fetch VT v3 API sandbox data.
    This can be used to directly pull sandbox data from VT.

    Parameters
    ----------
    file_hash : str
        The hash of the file you want to graph.
    sandbox_name : str, optional
        The name of the sandbox you want to pull from VT (there may be multiple available).
        (the default is None, which picks the first one)

    Raises
    ------
    RuntimeError
        If there is not virustotal API key defined.

    Examples
    ---------
    >>> datasource = GenericVTSandboxAPI(
        file_hash="ed01ebfbc9eb5bbea545af4d01bf5f1071661840480439c6e5babe8e080e41aa',
        sandbox_name="Dr.Web vxCube"
    )

    """

    name = "VirusTotal v3 API Sandbox Report"
    transformers = [GenericTransformer]
    category = "VT Sandbox"

    def __init__(self, file_hash: str, sandbox_name: str = None):
        api_key = Config.get("virustotal", "api_key")

        if not api_key:
            logger.critical(
                f"BEAGLE__VIRUSTOTAL__API_KEY not found in enviroment variables or beagle.config object"
            )
            raise RuntimeError(
                "BEAGLE__VIRUSTOTAL__API_KEY not found in enviroment variables or beagle.config object"
            )

        logger.info(f"Grabbing metadata and sandbox reports for {file_hash}")

        headers = {"x-apikey": api_key}

        self.hash_metadata = requests.get(
            f"https://www.virustotal.com/api/v3/files/{file_hash}", headers=headers
        ).json()
        behaviour_reports = requests.get(
            f"https://www.virustotal.com/api/v3/files/{file_hash}/behaviours", headers=headers
        ).json()

        # Get the sandbox we want, or the first one.
        if sandbox_name:
            possible_sandboxes = [
                report["attributes"]["sandbox_name"] for report in behaviour_reports["data"]
            ]
            logger.info(f"Sample has reports from {','.join(possible_sandboxes)}")
            if sandbox_name in possible_sandboxes:
                logger.info(f"Requested sandbox {sandbox_name} availble, using it.")
                behaviour_report = list(
                    filter(
                        lambda val: val["attributes"]["sandbox_name"] == sandbox_name,
                        behaviour_reports["data"],
                    )
                )[0]
            else:
                logger.info(f"Requested sandbox {sandbox_name} not found, using first sandbox.")
                behaviour_report = behaviour_reports["data"][0]
        else:

            behaviour_report = behaviour_reports["data"][0]
            logger.info(
                f"No sandbox specified, using {behaviour_report['attributes']['sandbox_name']}"
            )

        self.behaviour_report = behaviour_report[
            "attributes"
        ]  # Set up same way as GenericVTSandbox

