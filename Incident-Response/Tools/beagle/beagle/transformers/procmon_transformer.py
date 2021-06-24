import re
from typing import Optional, Tuple

from beagle.common import split_path
from beagle.nodes import File, Process, RegistryKey
from beagle.nodes.ip_address import IPAddress
from beagle.transformers.base_transformer import Transformer


class ProcmonTransformer(Transformer):
    name = "Procmon"

    def transform(self, event: dict) -> Optional[Tuple]:

        operation = event["event_type"]
        if operation == "Process Create":
            return self.process_create(event)
        elif operation in ["WriteFile", "CreateFile"]:
            return self.write_file(event)
        elif operation in ["CloseFile", "ReadFile"]:
            return self.access_file(event)
        elif operation in ["RegOpenKey", "RegQueryKey", "RegQueryValue", "RegCloseKey"]:
            return self.access_reg_key(event)
        elif operation in ["TCP Send", "TCP Receive", "TCP Connect", "UDP Connect", "UDP Receive"]:
            return self.connection(event)
        return None

    def process_create(self, event) -> Tuple[Process, File, Process]:

        pid = -1
        command_line = None
        match = re.match(r"PID: (\d*), Command line: (.*)", event["params"])
        if match:
            pid, command_line = match.groups()

        process_image, process_image_path = split_path(event["path"])

        proc = Process(
            process_id=int(pid),
            process_image=process_image,
            process_image_path=process_image_path,
            command_line=command_line,
        )
        proc_file = proc.get_file_node()
        proc_file.file_of[proc]

        parent = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

        parent.launched[proc].append(timestamp=event["event_time"])

        return (proc, proc_file, parent)

    def write_file(self, event) -> Tuple[Process, File]:

        proc = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

        file_name, file_path = split_path(event["path"])
        target_file = File(file_name=file_name, file_path=file_path)

        proc.wrote[target_file].append(timestamp=event["event_time"])

        return (proc, target_file)

    def access_file(self, event) -> Tuple[Process, File]:
        proc = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

        file_name, file_path = split_path(event["path"])
        target_file = File(file_name=file_name, file_path=file_path)

        proc.accessed[target_file].append(timestamp=event["event_time"])

        return (proc, target_file)

    def access_reg_key(self, event) -> Tuple[Process, RegistryKey]:

        proc = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

        reg_key, reg_path = split_path(event["path"])

        hive = reg_path.split("\\")[0]
        reg_path = "\\".join(reg_path.split("\\")[1:])

        reg_node = RegistryKey(hive=hive, key_path=reg_path, key=reg_key)

        proc.read_key[reg_node].append(timestamp=event["event_time"])

        return (proc, reg_node)

    def connection(self, event) -> Tuple[Process, IPAddress]:
        proc = Process(process_id=int(event["process_id"]), process_image=event["process_name"])

        dest_addr = event["path"].split("->")[-1].lstrip()
        colons = dest_addr.split(":")
        if len(colons) > 2:
            ip_addr = ":".join(colons[:-1])
            port = colons[-1]
        else:
            ip_addr, port = colons

        addr = IPAddress(ip_addr)
        proc.connected_to[addr].append(
            timestamp=event["event_time"],
            port=int(port),
            protocol=event["event_type"].split(" ")[0],  # Extract protocol from event type
        )

        return (proc, addr)
