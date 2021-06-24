import json
import re
from typing import Generator, List
from urllib import parse
from random import sample

from beagle.common import split_path
from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames, HashAlgos, HTTPMethods, Protocols
from beagle.datasources import DataSource
from beagle.transformers.generic_transformer import GenericTransformer

PROC_PATH_REX = re.compile(
    r"^(?:[a-zA-Z]\:|\\\\[\w\.]+\\[\w.$]+)?\\?(?:[<>%\(\) \w]+\\)*\w([\w.])+"
)


class GenericVTSandbox(DataSource):
    """Converts a Virustotal V3 API behavior report to a Beagle graph.

    This DataSource outputs data in the schema accepted by `GenericTransformer`.

    Providing the hash's metadata JSON allows for proper creation of a metadata object.
    * This can be fetched from https://www.virustotal.com/api/v3/files/{id}

    Behavior reports come from https://www.virustotal.com/api/v3/files/{id}/behaviours
    * Beagle generates one graph **per** report in the `attributes` array.

    Where {id} is the sha256 of the file.

    Parameters
    ----------
    behaviour_report : str
        File containing A **single** behaviour report from one of the virustotal linked sandboxes.
    hash_metadata : str
        File containing the hashes metadata, containing its detections.

    """

    name = "VirusTotal v3 API Sandbox Report Files"
    transformers = [GenericTransformer]
    category = "VT Sandbox"

    KNOWN_ATTRIBUTES: List[str] = [
        "files_deleted",
        "processes_tree",
        "files_opened",
        "files_written",
        "modules_loaded",
        "files_attribute_changed",
        "files_dropped",
        "has_html_report",
        "analysis_date",
        "sandbox_name",
        "http_conversations",
        "ip_traffic",
        "dns_lookups",
        "registry_keys_opened",
        "registry_keys_deleted",
        "registry_keys_set",
    ]

    def __init__(self, behaviour_report_file: str, hash_metadata_file: str = None) -> None:

        behaviour_report = json.load(open(behaviour_report_file, "r", encoding="utf8"))

        if "attributes" not in behaviour_report:
            raise AttributeError(f"Supplied behaviour report does not contain any data")

        hash_metadata = None
        if hash_metadata_file:
            hash_metadata = json.load(open(hash_metadata_file, "r"))

        self.hash_metadata = hash_metadata
        self.behaviour_report = behaviour_report["attributes"]

        logger.info(f"Finished setting up GenericVTSandbox")

        for key in self.behaviour_report.keys():
            if key not in self.KNOWN_ATTRIBUTES:
                logger.debug(f"Unknown key {key} found in VirusTotal sandbox report")

    def _convert_to_parent_fields(self, process: dict) -> dict:
        output = {}
        for left, right in [
            (FieldNames.PROCESS_IMAGE, FieldNames.PARENT_PROCESS_IMAGE),
            (FieldNames.PROCESS_ID, FieldNames.PARENT_PROCESS_ID),
            (FieldNames.COMMAND_LINE, FieldNames.PARENT_COMMAND_LINE),
            (FieldNames.PROCESS_IMAGE_PATH, FieldNames.PARENT_PROCESS_IMAGE_PATH),
        ]:
            output[right] = process[left]

        return output

    def _parse_process_name(self, proc_string: str) -> dict:
        """Pulls out the comand line, process name, and process path out of a string, if possible"""

        # NOTE: Case not handeled by the regex, hardcoded result:

        # Tencent
        if proc_string == "****.exe":
            proc_path = "****.exe"

        # Sometimes, "****.exe --local-service" shows up.
        elif proc_string.startswith("****.exe"):
            proc_path = "****.exe"

        # Dr.web
        elif proc_string == "<PATH_SAMPLE.EXE>":
            proc_path = "<PATH_SAMPLE.EXE>"

        # Manually introduced.
        elif proc_string == "<SUBMITTED_FILE>":
            proc_path = "<SUBMITTED_FILE>"

        # Try and parse the path.
        else:
            match = PROC_PATH_REX.match(proc_string)
            if match:
                proc_path = match.group()
            else:
                logger.critical(f"Could not parse {proc_string}")

        # Leave only the command line
        command_line = proc_string.replace(proc_path, "")

        # Remove leading whitespace.
        command_line = command_line.lstrip()

        proc_name, proc_path = split_path(proc_path)

        return {
            FieldNames.PROCESS_IMAGE: proc_name,
            FieldNames.PROCESS_IMAGE_PATH: proc_path,
            FieldNames.COMMAND_LINE: command_line,
        }

    def _get_root_proc(self) -> dict:
        """Returns the root process. This will be the first process in the
        process_tree entry.

        Returns
        -------
        dict
            [description]
        """

        if "processes_tree" in self.behaviour_report:
            proc_tree = self.behaviour_report["processes_tree"]

            first_process: dict = proc_tree[0].copy()
            # Pop children if possible
            first_process.pop("children", None)

            process_dict = self._parse_process_name(first_process["name"])
            process_dict[FieldNames.PROCESS_ID] = first_process.get("process_id", 0)

        else:
            process_dict = self._parse_process_name("<SUBMITTED_FILE>")
            process_dict[FieldNames.PROCESS_ID] = 0

        return process_dict

    def metadata(self) -> dict:
        """Generates the metadata based on the provided hash_metadata file.

        Returns
        -------
        dict
            Name, number of malicious detections, AV results, and common_name from VT.
        """

        if self.hash_metadata is None:
            return {}

        # Otherwise pull out the attributes
        meta = self.hash_metadata["data"]["attributes"]

        possible_detection = [
            {engine: engine_data["result"]}
            for engine, engine_data in meta["last_analysis_results"].items()
            if engine_data["result"]
        ]
        if len(possible_detection) > 0:
            key, value = next(iter(sample(possible_detection, 1)[0].items()))  # type: ignore
            random_key = f"{key}: {value}"
        else:
            random_key = "Clean!"

        return {
            "name": meta.get("meaningful_name", ""),
            "malicious": meta["last_analysis_stats"]["malicious"],
            "results": random_key,
            "sandbox_name": self.behaviour_report["sandbox_name"],
            "sha256": meta["sha256"],
        }

    def events(self) -> Generator[dict, None, None]:

        self.parent_process = self._get_root_proc()

        for function in [
            self._proc_tree,
            self._basic_file_events,
            self._complex_file_events,
            self._network_events,
            self._basic_registry_events,
            self._complex_registry_events,
        ]:
            yield from function()

    def _proc_tree(self) -> Generator[dict, None, None]:
        """Yields every entry in the processes_tree key as a dict
        containing the parent and child information

        Example
        --------

        The following entry:
        >>> {
            "children": [
                {
                    "name": "%WINDIR%\\syswow64\\cscript.exe",
                    "process_id": "2268",
                    "time_offset": 3
                }
            ],
            "name": "%WINDIR%\\syswow64\\cmd.exe",
            "process_id": "2764",
            "time_offset": 3
        },

        Would be transformed into

        >>> {
            "parent_process": "<PATH_SAMPLE.EXE>",
            "parent_process_id": "3420",
            "process_id": "3712",
            "time_offset": 5,
            "name": "<SYSTEM32>\\cmd.exe",
              FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
        }

        Returns
        -------
        Generator[dict, None, None]
            All parent and child combinations from the processes_tree entry.
        """

        # These can be nested. See `tests/datasources/virustotal/test_files/example_drweb_nested_children.json`
        def process_entry(entry: dict) -> Generator[dict, None, None]:
            # No need to send something that has no children
            # as it will be included in whatever launched it

            # Get the current process, and convert the fields
            parent_proc = self._parse_process_name(entry["name"])
            parent_proc[FieldNames.PROCESS_ID] = entry["process_id"]
            parent_proc = self._convert_to_parent_fields(parent_proc)

            if "children" in entry:
                for child in entry["children"]:

                    _child = child.copy()

                    if "children" in _child:
                        _child.pop("children")

                    child_proc = self._parse_process_name(_child["name"])
                    child_proc[FieldNames.PROCESS_ID] = _child["process_id"]

                    output = {**parent_proc, **child_proc}
                    output[FieldNames.EVENT_TYPE] = EventTypes.PROCESS_LAUNCHED

                    if "time_offset" in _child:
                        output[FieldNames.TIMESTAMP] = _child["time_offset"]

                    yield output
                    yield from process_entry(child)

        for entry in self.behaviour_report.get("processes_tree", []):
            yield from process_entry(entry)

    def _basic_file_events(self) -> Generator[dict, None, None]:

        event_type_mappings = {
            "files_deleted": EventTypes.FILE_DELETED,
            "files_opened": EventTypes.FILE_OPENED,
            "files_written": EventTypes.FILE_WRITTEN,
            "modules_loaded": EventTypes.LOADED_MODULE,
            "files_attribute_changed": EventTypes.FILE_OPENED,
        }

        for entry_key, event_type in event_type_mappings.items():

            for file_path in self.behaviour_report.get(entry_key, []):

                file_name, file_path = split_path(file_path)

                yield {
                    FieldNames.FILE_NAME: file_name,
                    FieldNames.FILE_PATH: file_path,
                    FieldNames.EVENT_TYPE: event_type,
                    **self.parent_process,
                }

    def _complex_file_events(self) -> Generator[dict, None, None]:
        """Generator over files_dropped and files_copied events"""

        for copied_file in self.behaviour_report.get("files_copied", []):

            dst_file_name, dst_file_path = split_path(copied_file["destination"])
            src_file_name, src_file_path = split_path(copied_file["source"])

            yield {
                FieldNames.EVENT_TYPE: EventTypes.FILE_COPIED,
                FieldNames.SRC_FILE: {
                    FieldNames.FILE_NAME: src_file_name,
                    FieldNames.FILE_PATH: src_file_path,
                },
                FieldNames.DEST_FILE: {
                    FieldNames.FILE_NAME: dst_file_name,
                    FieldNames.FILE_PATH: dst_file_path,
                },
                **self.parent_process,
            }

        for dropped_file in self.behaviour_report.get("files_dropped", []):

            file_name, file_path = split_path(dropped_file["path"])

            yield {
                FieldNames.EVENT_TYPE: EventTypes.FILE_WRITTEN,
                FieldNames.FILE_NAME: file_name,
                FieldNames.FILE_PATH: file_path,
                FieldNames.HASHES: {HashAlgos.SHA256: dropped_file["sha256"]},
                **self.parent_process,
            }

    def _network_events(self) -> Generator[dict, None, None]:

        for http_request in self.behaviour_report.get("http_conversations", []):
            yield {
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
                FieldNames.HTTP_METHOD: http_request.get("request_method", HTTPMethods.GET),
                FieldNames.HTTP_HOST: parse.urlparse(http_request["url"]).netloc,
                FieldNames.URI: parse.urlparse(http_request["url"]).path,
                **self.parent_process,
            }

        for connection in self.behaviour_report.get("ip_traffic", []):
            yield {
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.IP_ADDRESS: connection["destination_ip"],
                FieldNames.PORT: connection["destination_port"],
                FieldNames.PROTOCOL: connection.get("transport_layer_protocol", Protocols.TCP),
                **self.parent_process,
            }

        for dnslookup in self.behaviour_report.get("dns_lookups", []):
            for ip in dnslookup.get("resolved_ips", []):
                yield {
                    FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                    FieldNames.HTTP_HOST: dnslookup["hostname"],
                    FieldNames.IP_ADDRESS: ip,
                    **self.parent_process,
                }
            # If no IPs
            else:
                yield {
                    FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                    FieldNames.HTTP_HOST: dnslookup["hostname"],
                    **self.parent_process,
                }

    def _basic_registry_events(self) -> Generator[dict, None, None]:

        mapping = {
            "registry_keys_opened": EventTypes.REG_KEY_OPENED,
            "registry_keys_deleted": EventTypes.REG_KEY_DELETED,
        }

        for key, event_type in mapping.items():
            for reg_path in self.behaviour_report.get(key, []):

                # RegistryKey Node Creation
                hive = reg_path.split("\\")[0]
                reg_key = "\\".join(reg_path.split("\\")[1:-1])
                reg_key_path = reg_path.split("\\")[-1]

                yield {
                    FieldNames.EVENT_TYPE: event_type,
                    FieldNames.HIVE: hive,
                    FieldNames.REG_KEY_PATH: reg_key,
                    FieldNames.REG_KEY: reg_key_path,
                    **self.parent_process,
                }

    def _complex_registry_events(self) -> Generator[dict, None, None]:

        for reg_key_set in self.behaviour_report.get("registry_keys_set", []):

            reg_path = reg_key_set["key"]

            # RegistryKey Node Creation
            hive = reg_path.split("\\")[0]
            reg_key = "\\".join(reg_path.split("\\")[1:-1])
            reg_key_path = reg_path.split("\\")[-1]

            yield {
                FieldNames.EVENT_TYPE: EventTypes.REG_KEY_SET,
                FieldNames.HIVE: hive,
                FieldNames.REG_KEY_PATH: reg_key,
                FieldNames.REG_KEY: reg_key_path,
                FieldNames.REG_KEY_VALUE: reg_key_set.get("value"),
                **self.parent_process,
            }
