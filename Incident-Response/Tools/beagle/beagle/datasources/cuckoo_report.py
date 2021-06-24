import json
from typing import Dict, Generator
from urllib import parse

from beagle.common import split_path, split_reg_path
from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames, HTTPMethods, Protocols
from beagle.datasources.base_datasource import DataSource
from beagle.transformers import GenericTransformer


class CuckooReport(DataSource):
    """Yields events from a cuckoo sandbox report.

    Cuckoo now provides a nice summary for each process under the "generic" summary tab::

        {
            "behavior": {
                "generic": [
                    {
                        'process_path': 'C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe',
                        'process_name': 'It6QworVAgY.exe',
                        'pid': 2548,
                        'ppid': 2460,
                        'summary': {
                            "directory_created" : [...],
                            "dll_loaded" : [...],
                            "file_opened" : [...],
                            "regkey_opened" : [...],
                            "file_moved" : [...],
                            "file_deleted" : [...],
                            "file_exists" : [...],
                            "mutex" : [...],
                            "file_failed" : [...],
                            "guid" : [...],
                            "file_read" : [...],
                            "regkey_re" : [...]
                            ...
                        },

                    }
                ]
            }
        }

    Using this, we can crawl and extract out all activity for a specific process.

    Notes
    ---------
    This is based on the output of the following reporting module:
    https://github.com/cuckoosandbox/cuckoo/blob/master/cuckoo/processing/platform/windows.py



    Parameters
    ----------
    cuckoo_report : str
        The file path to the cuckoo sandbox report.
    """

    name = "Cuckoo Sandbox Report"
    category = "Cuckoo Sandbox"  # The category this will output to.

    # The events object yields both the API calls and the prettified version.
    transformers = [GenericTransformer]

    def __init__(self, cuckoo_report: str) -> None:
        self.report = json.load(open(cuckoo_report, "r"))
        self.behavior = self.report["behavior"]

        self.processes: Dict[int, dict] = {}
        logger.info("Set up Cuckoo Sandbox")

    def metadata(self) -> dict:
        return {
            "machine": self.report["info"]["machine"]["name"],
            "package": self.report["info"]["package"],
            "score": self.report["info"]["score"],
            "report_id": self.report["info"]["id"],
            "name": self.report["target"].get("file", {"name": ""})["name"],
            "category": self.report["target"]["category"],
            "type": self.report["target"].get("file", {"type": ""})["type"],
        }

    def events(self) -> Generator[dict, None, None]:

        self.processes: Dict[int, dict] = self.identify_processes()

        # First, do process launching.
        yield from self.process_tree()

        # for each process, iterate over it's summary
        for process_summary in self.behavior["generic"]:

            # get the parent
            process = self.processes[int(process_summary["pid"])]

            # Yield strucutred events.
            for func in [
                self._basic_file_events,
                self._summary_network_connections,
                self._regkey_events,
            ]:
                yield from func(process_summary["summary"], process)

        # Finall, yield from global process events:
        yield from self.global_network_events()

    def identify_processes(self) -> Dict[int, dict]:
        """The `generic` tab contains an array of processes. We can iterate over it to quickly generate
        `Process` entries for later. After grabbing all processes, we can walk the "processtree" entry
        to update them with the command lines.


        Returns
        -------
        None
        """

        processes = {}

        for process in self.behavior["generic"]:

            proc_name, proc_path = split_path(process["process_path"])

            processes[int(process["pid"])] = {
                FieldNames.PROCESS_IMAGE: proc_name,
                FieldNames.PROCESS_IMAGE_PATH: proc_path,
                FieldNames.PROCESS_ID: int(process["pid"]),
            }

        return processes

    def process_tree(self) -> Generator[dict, None, None]:
        def process_single_entry(entry: dict) -> Generator[dict, None, None]:

            current_proc = self.processes[int(entry["pid"])]
            current_proc[FieldNames.COMMAND_LINE] = entry["command_line"]
            self.processes[int(entry["pid"])] = current_proc.copy()

            children = entry.get("children", [])

            # If the parent pid is not in the processes, then we need to make an artifical node.
            if entry["ppid"] not in self.processes:
                yield {
                    FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
                    FieldNames.TIMESTAMP: entry["first_seen"],
                    FieldNames.PARENT_PROCESS_ID: entry["ppid"],
                    FieldNames.PARENT_PROCESS_IMAGE: "Unknown",
                    FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
                    FieldNames.PARENT_COMMAND_LINE: "",
                    **current_proc,
                }

            if len(children) > 0:

                for child in children:

                    child_proc = self.processes[int(child["pid"])]
                    child_proc[FieldNames.COMMAND_LINE] = child["command_line"]
                    self.processes[int(child["pid"])] = child_proc.copy()

                    current_as_parent = self._convert_to_parent_fields(current_proc.copy())

                    yield {
                        FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
                        FieldNames.TIMESTAMP: child["first_seen"],
                        **current_as_parent,
                        **child_proc,
                    }

                    yield from process_single_entry(child)

        for entry in self.behavior.get("processtree", []):
            yield from process_single_entry(entry)

    def _basic_file_events(
        self, process_summary: dict, process: dict
    ) -> Generator[dict, None, None]:

        event_type_mappings = {
            "file_deleted": EventTypes.FILE_DELETED,
            "file_opened": EventTypes.FILE_OPENED,
            "file_failed": EventTypes.FILE_OPENED,
            "file_read": EventTypes.FILE_OPENED,
            "file_written": EventTypes.FILE_WRITTEN,
            "dll_loaded": EventTypes.LOADED_MODULE,
            "file_attribute_changed": EventTypes.FILE_OPENED,
            "file_exists": EventTypes.FILE_OPENED,
        }

        for entry_key, event_type in event_type_mappings.items():

            for file_path in process_summary.get(entry_key, []):

                # Ignore directorys
                if file_path.endswith("\\"):
                    continue

                file_name, file_path = split_path(file_path)

                yield {
                    FieldNames.FILE_NAME: file_name,
                    FieldNames.FILE_PATH: file_path,
                    FieldNames.EVENT_TYPE: event_type,
                    **process,
                }

    def _summary_network_connections(
        self, process_summary: dict, process: dict
    ) -> Generator[dict, None, None]:

        for dest_hostname in process_summary.get("connects_host", []):

            yield {
                FieldNames.IP_ADDRESS: dest_hostname,
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                **process,
            }

        for ip_address in process_summary.get("connects_ip", []):

            yield {
                FieldNames.IP_ADDRESS: ip_address,
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                **process,
            }

        for domain in process_summary.get("resolves_host", []):

            yield {
                FieldNames.HTTP_HOST: domain,
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                **process,
            }

        for key in ["fetches_url", "downloads_file"]:
            for url in process_summary.get(key, []):

                yield {
                    FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
                    FieldNames.HTTP_METHOD: HTTPMethods.GET,
                    FieldNames.HTTP_HOST: parse.urlparse(url).netloc,
                    FieldNames.URI: parse.urlparse(url).path,
                    **process,
                }

    def _regkey_events(self, process_summary: dict, process: dict) -> Generator[dict, None, None]:

        mapping = {
            "regkey_written": EventTypes.REG_KEY_SET,
            "regkey_deleted": EventTypes.REG_KEY_DELETED,
            "regkey_opened": EventTypes.REG_KEY_OPENED,
            "regkey_read": EventTypes.REG_KEY_OPENED,
        }

        for key, event_type in mapping.items():
            for reg_path in process_summary.get(key, []):

                # RegistryKey Node Creation
                hive, reg_key_path, reg_key = split_reg_path(reg_path)

                yield {
                    FieldNames.EVENT_TYPE: event_type,
                    FieldNames.HIVE: hive,
                    FieldNames.REG_KEY_PATH: reg_key,
                    FieldNames.REG_KEY: reg_key_path,
                    **process,
                }

    def global_network_events(self) -> Generator[dict, None, None]:

        root_proc_name = self.report.get("target", {}).get("file", {"name": ""})["name"]
        root_proc = None
        if root_proc_name:
            process_entries = list(self.processes.values())

            # Get the submitted sample to match to the network events.
            for proc in process_entries:
                if proc[FieldNames.PROCESS_IMAGE] == root_proc_name:
                    root_proc = proc
                    break

        if not root_proc_name or not root_proc:
            root_proc = list(self.processes.values())[0]

        logger.debug(f"Found root process as {root_proc}")

        network_connections = self.report.get("network", {})

        # Connections
        # Example entry:
        # {
        #     "src": "192.168.168.201",
        #     "dst": "192.168.168.229",
        #     "offset": 299,
        #     "time": 11.827166080474854,
        #     "dport": 55494,
        #     "sport": 5355,
        # },
        for udp_conn in network_connections.get("udp", []):

            yield {
                FieldNames.IP_ADDRESS: udp_conn["dst"],
                FieldNames.PORT: udp_conn["dport"],
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.PROTOCOL: Protocols.UDP,
                **root_proc,
            }

        # tcp connections
        for tcp_conn in network_connections.get("tcp", []):

            yield {
                FieldNames.IP_ADDRESS: tcp_conn["dst"],
                FieldNames.PORT: tcp_conn["dport"],
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.PROTOCOL: Protocols.TCP,
                **root_proc,
            }

        # icmp connections
        for icmp_conn in network_connections.get("icmp", []):

            yield {
                FieldNames.IP_ADDRESS: icmp_conn["dst"],
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.PROTOCOL: Protocols.ICMP,
                **root_proc,
            }

        for dns_request in network_connections.get("dns", []):

            # If answers, this will make the resolved to edge from the generic transformer.
            if "answers" in dns_request and dns_request["answers"]:
                for answer in dns_request["answers"]:
                    yield {
                        FieldNames.HTTP_HOST: dns_request["request"],
                        FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                        FieldNames.IP_ADDRESS: answer["data"],
                        **root_proc,
                    }
            else:
                # Otherwise, only add the DNS request
                yield {
                    FieldNames.HTTP_HOST: dns_request["request"],
                    FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                    **root_proc,
                }

        for http_request in network_connections.get("http_ex", []):
            yield {
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
                FieldNames.HTTP_METHOD: http_request["method"],
                FieldNames.HTTP_HOST: http_request["host"],
                FieldNames.IP_ADDRESS: http_request["dst"],
                FieldNames.URI: http_request["uri"],
                **root_proc,
            }
