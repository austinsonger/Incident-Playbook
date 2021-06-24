from typing import Optional, Tuple, Union

from beagle.common import logger, split_path
from beagle.nodes import Domain, File, IPAddress, Process, RegistryKey, SysMonProc
from beagle.transformers.base_transformer import Transformer


class SysmonTransformer(Transformer):
    name = "Sysmon"

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        logger.info("Created Sysmon Transformer.")

    def transform(self, event: dict) -> Optional[Tuple]:

        # Get the sysmon event ID
        event_id = int(event["EventID"])
        if event_id == 1:
            return self.process_creation(event)
        elif event_id == 3:
            return self.network_connection(event)
        elif event_id in [13, 14, 15]:
            return self.registry_creation(event)
        elif event_id == 22:
            return self.dns_lookup(event)
        elif event_id == 11:
            return self.file_created(event)
        return None

    def process_creation(self, event: dict) -> Tuple[Process, File, Process, File]:

        # Make the parent process
        parent_image, parent_path = split_path(event["EventData_ParentImage"])

        parent = SysMonProc(
            host=event["Computer"],
            process_id=int(event["EventData_ParentProcessId"]),
            process_guid=event["EventData_ParentProcessGuid"],
            process_image=parent_image,
            process_image_path=parent_path,
        )

        parent_file = parent.get_file_node()
        parent_file.file_of[parent]

        process_image, process_path = split_path(event["EventData_Image"])

        proc = SysMonProc(
            host=event["Computer"],
            user=event["EventData_User"],
            process_guid=event["EventData_ProcessGuid"],
            process_id=int(event["EventData_ProcessId"]),
            process_image=process_image,
            process_image_path=process_path,
            command_line=event["EventData_CommandLine"],
            hashes={
                val.split("=")[0].lower(): val.split("=")[1]
                for val in event["EventData_Hashes"].split(",")
            },
        )

        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        parent.launched[proc].append(timestamp=event["EventData_UtcTime"])

        return (parent, parent_file, proc, proc_file)

    def network_connection(
        self, event: dict
    ) -> Union[Tuple[Process, File, IPAddress], Tuple[Process, File, IPAddress, Domain]]:
        process_image, process_path = split_path(event["EventData_Image"])

        proc = SysMonProc(
            host=event["Computer"],
            user=event["EventData_User"],
            process_guid=event["EventData_ProcessGuid"],
            process_id=int(event["EventData_ProcessId"]),
            process_image=process_image,
            process_image_path=process_path,
        )
        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        dest_addr = IPAddress(ip_address=event["EventData_DestinationIp"])

        proc.connected_to[dest_addr].append(
            timestamp=event["EventData_UtcTime"],
            port=event["EventData_DestinationPort"],
            protocol=event["EventData_Protocol"],
        )

        if event.get("EventData_DestinationHostname"):
            hostname = Domain(event["EventData_DestinationHostname"])
            hostname.resolves_to[dest_addr].append(timestamp=event["EventData_UtcTime"])
            return (proc, proc_file, dest_addr, hostname)

        return (proc, proc_file, dest_addr)

    def file_created(self, event: dict) -> Tuple[Process, File, File]:

        process_image, process_path = split_path(event["EventData_Image"])

        proc = SysMonProc(
            host=event["Computer"],
            user=event.get("EventData_User"),
            process_guid=event["EventData_ProcessGuid"],
            process_id=int(event["EventData_ProcessId"]),
            process_image=process_image,
            process_image_path=process_path,
        )
        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        file_image, file_path = split_path(event["EventData_TargetFilename"])

        file_node = File(file_name=file_image, file_path=file_path)

        proc.accessed[file_node].append(timestamp=event["EventData_UtcTime"])

        return (proc, proc_file, file_node)

    def registry_creation(self, event: dict) -> Optional[Tuple[Process, File, RegistryKey]]:

        if "EventData_TargetObject" not in event:
            return None

        process_image, process_path = split_path(event["EventData_Image"])

        proc = SysMonProc(
            host=event["Computer"],
            user=event.get("EventData_User"),
            process_guid=event["EventData_ProcessGuid"],
            process_id=int(event["EventData_ProcessId"]),
            process_image=process_image,
            process_image_path=process_path,
        )
        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        key_path = event["EventData_TargetObject"]
        hive = key_path.split("\\")[1]
        key = key_path.split("\\")[-1]
        # Always has a leading \\ so split from 2:
        key_path = "\\".join(key_path.split("\\")[2:-1])

        key = RegistryKey(
            hive=hive,
            key=key,
            key_path=key_path,
            value=event.get("EventData_Details"),
            value_type="DWORD",
        )

        event_type = event["EventData_EventType"]
        if event_type == "SetValue":
            proc.changed_value[key].append(
                value=event.get("EventData_Details"), timestamp=event["EventData_UtcTime"]
            )
        elif event_type == "DeleteValue":
            proc.deleted_value[key].append(timestamp=event["EventData_UtcTime"])
        elif event_type == "CreateKey":
            proc.created_key[key].append(timestamp=event["EventData_UtcTime"])
        elif event_type == "DeleteKey":
            proc.deleted_key[key].append(timestamp=event["EventData_UtcTime"])

        return (proc, proc_file, key)

    def dns_lookup(self, event: dict) -> Tuple[Process, File, Domain]:
        process_image, process_path = split_path(event["EventData_Image"])

        proc = SysMonProc(
            host=event["Computer"],
            user=event.get("EventData_User"),
            process_guid=event["EventData_ProcessGuid"],
            process_id=int(event["EventData_ProcessId"]),
            process_image=process_image,
            process_image_path=process_path,
        )
        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        # TODO: Parse out EventData_QueryResults and add resolutions
        domain = Domain(domain=event["EventData_QueryName"])

        proc.dns_query_for[domain].append(timestamp=event["EventData_UtcTime"])

        return (proc, proc_file, domain)
