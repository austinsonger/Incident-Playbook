from typing import List, Optional, Tuple, Union

from beagle.common import logger, split_path, split_reg_path
from beagle.nodes import File, Process, RegistryKey, IPAddress
from beagle.transformers.base_transformer import Transformer


# Custom Node classes to use the UUID in TC
class TCProcess(Process):
    key_fields: List[str] = ["uuid"]
    uuid: Optional[str]

    def __init__(self, uuid: str = None, *args, **kwargs) -> None:
        self.uuid = uuid
        super().__init__(*args, **kwargs)


class TCFile(File):
    key_fields: List[str] = ["uuid"]
    uuid: Optional[str]

    def __init__(self, uuid: str = None, *args, **kwargs) -> None:
        self.uuid = uuid
        super().__init__(*args, **kwargs)


class TCRegistryKey(RegistryKey):
    key_fields: List[str] = ["uuid"]
    uuid: Optional[str]

    def __init__(self, uuid: str = None, *args, **kwargs) -> None:
        self.uuid = uuid
        super().__init__(*args, **kwargs)


class TCIPAddress(IPAddress):
    key_fields: List[str] = ["uuid"]
    uuid: Optional[str]

    def __init__(self, uuid: str = None, *args, **kwargs) -> None:
        self.uuid = uuid
        super().__init__(*args, **kwargs)


class DRAPATCTransformer(Transformer):

    name = "DARPA TC"

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        logger.info("Created Darpa Transperant Computing Transformer.")

    def transform(self, event: dict) -> Optional[Tuple]:
        event_type = event["event_type"]

        if event_type == "subject" and event["type"] == "SUBJECT_PROCESS":
            return self.make_process(event)
        elif event_type == "fileobject" and event["type"] in [
            "FILE_OBJECT_BLOCK",
            "FILE_OBJECT_PEFILE",
        ]:
            return self.make_file(event)
        elif event_type == "registrykeyobject":
            return self.make_registrykey(event)
        elif event_type == "netflowobject":
            return self.make_addr(event)
        elif event_type == "event" and event["type"] in [
            "EVENT_READ",
            "EVENT_OPEN",
            "EVENT_WRITE",
            "EVENT_WRITE_APPEND",
            "EVENT_MODIFY_FILE_ATTRIBUTES",
            "EVENT_CREATE_OBJECT",
            "EVENT_LOAD_LIBRARY",
        ]:
            return self.file_events(event)
        elif event_type == "event" and event["type"] == "EVENT_EXECUTE":
            return self.execute_events(event)
        elif event_type == "event" and event["type"] in ["EVENT_CONNECT"]:
            return self.conn_events(event)

        return tuple()

    def make_process(self, event: dict) -> Union[Tuple[TCProcess], Tuple[TCProcess, TCProcess]]:
        if event.get("cmdLine"):
            proc_cmdline = event["cmdLine"]["string"]
        else:
            proc_cmdline = None

        path = None
        image = None
        if event.get("properties"):
            path = event["properties"]["map"].get("path")
            if "/" in path:
                # Swap the path directions
                path = path.replace("/", "\\")
            image, path = split_path(path)

        proc = TCProcess(
            uuid=event["uuid"],
            process_image=image or proc_cmdline,
            process_image_path=path or proc_cmdline,
            command_line=proc_cmdline,
            host=event["hostId"],
        )
        if event.get("parentSubject"):

            parent = TCProcess(
                uuid=event["parentSubject"]["com.bbn.tc.schema.avro.cdm18.UUID"],
                host=event["hostId"],
            )

            parent.launched[proc]

            return (proc, parent)
        else:
            return (proc,)

    def make_file(self, event: dict) -> Tuple[TCFile]:

        base_obj = event["baseObject"]

        file_node = TCFile(uuid=event["uuid"], host=base_obj["hostId"])

        # Since not everything has a full path, and this is multiple different systems,
        # this is the best try for this.
        if base_obj.get("properties"):
            full_path = base_obj["properties"]["map"].get("filename", "")
            full_path = full_path.replace("/", "\\")
            file_name, file_path = split_path(full_path)

            file_node.full_path = full_path
            file_node.file_path = file_path
            file_node.file_name = file_name

        return (file_node,)

    def make_registrykey(self, event: dict) -> Tuple[TCRegistryKey]:

        if event["key"].startswith("\\REGISTRY\\"):
            event["key"] = event["key"].replace("\\REGISTRY\\", "", 1)

        hive, key, path = split_reg_path(event["key"])
        base_obj = event["baseObject"]

        value = event["value"]["com.bbn.tc.schema.avro.cdm18.Value"]

        regkey = TCRegistryKey(
            uuid=event["uuid"],
            host=base_obj["hostId"],
            value_type=value["valueDataType"],
            value=value["name"],
            hive=hive,
            key_path=path,
            key=key,
        )

        return (regkey,)

    def make_addr(self, event: dict) -> Tuple[TCIPAddress]:
        addr = TCIPAddress(uuid=event["uuid"], ip_address=event["remoteAddress"])
        # TODO: Add port data somehow
        return (addr,)

    def file_events(self, event: dict) -> Tuple[TCProcess, TCFile]:

        proc = TCProcess(uuid=event["subject"]["com.bbn.tc.schema.avro.cdm18.UUID"])
        target = TCFile(uuid=event["predicateObject"]["com.bbn.tc.schema.avro.cdm18.UUID"])

        if event["type"] in ["EVENT_READ", "EVENT_MODIFY_FILE_ATTRIBUTES", "EVENT_OPEN"]:
            proc.accessed[target].append(timestamp=event["timestampNanos"])
        elif event["type"] in ["EVENT_WRITE", "EVENT_WRITE_APPEND", "EVENT_CREATE_OBJECT"]:
            proc.wrote[target].append(timestamp=event["timestampNanos"])
        elif event["type"] in ["EVENT_LOAD_LIBRARY"]:
            proc.loaded[target].append(timestamp=event["timestampNanos"])

        return (proc, target)

    def execute_events(self, event: dict) -> Tuple[TCProcess, TCProcess]:

        proc = TCProcess(uuid=event["subject"]["com.bbn.tc.schema.avro.cdm18.UUID"])
        target = TCProcess(
            uuid=event["predicateObject"]["com.bbn.tc.schema.avro.cdm18.UUID"],
            process_image=event.get("predicateObjectPath", {}).get("string"),
        )

        proc.launched[target].append(timestamp=event["timestampNanos"])

        return (proc, target)

    def conn_events(self, event: dict) -> Tuple[TCProcess, TCIPAddress]:
        proc = TCProcess(uuid=event["subject"]["com.bbn.tc.schema.avro.cdm18.UUID"])
        addr = TCIPAddress(uuid=event["predicateObject"]["com.bbn.tc.schema.avro.cdm18.UUID"])

        # TODO: Need to add the port data on the edge somehow
        proc.connected_to[addr].append(timestamp=event["timestampNanos"])

        return (proc, addr)
