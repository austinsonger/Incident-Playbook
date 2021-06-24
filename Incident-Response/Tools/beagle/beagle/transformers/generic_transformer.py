from typing import Optional, Tuple, Union

from beagle.common.logging import logger
from beagle.constants import EventTypes, FieldNames
from beagle.nodes import URI, Alert, Domain, File, IPAddress, Node, Process, RegistryKey
from beagle.transformers.base_transformer import Transformer

# TODO: Add Timestamps to everything, if possible.


class GenericTransformer(Transformer):
    """This transformer will properly create graphs for any datasource
    that outputs data in the pre-defined schema."""

    name = "Generic"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        logger.info("Created Generic Transformer.")

    def transform(self, event: dict) -> Optional[Tuple]:

        event_type = event.get(FieldNames.EVENT_TYPE)

        if event.get(FieldNames.ALERTED_ON):
            return self.make_alert(event)

        if event_type == EventTypes.PROCESS_LAUNCHED:
            return self.make_process(event)
        elif event_type in [
            EventTypes.FILE_DELETED,
            EventTypes.FILE_OPENED,
            EventTypes.FILE_WRITTEN,
            EventTypes.LOADED_MODULE,
        ]:
            return self.make_basic_file(event)
        elif event_type == EventTypes.FILE_COPIED:
            return self.make_file_copy(event)
        elif event_type == EventTypes.CONNECTION:
            return self.make_connection(event)
        elif event_type == EventTypes.HTTP_REQUEST:
            return self.make_http_req(event)
        elif event_type == EventTypes.DNS_LOOKUP:
            return self.make_dnslookup(event)
        elif event_type in [EventTypes.REG_KEY_OPENED, EventTypes.REG_KEY_DELETED]:
            return self.make_basic_regkey(event)
        elif event_type in [EventTypes.REG_KEY_SET]:
            return self.make_regkey_set_value(event)
        else:
            return None

    def make_alert(self, event: dict) -> Tuple[Alert, ...]:
        event.pop(FieldNames.ALERTED_ON)
        alert = Alert(
            alert_name=event.pop(FieldNames.ALERT_NAME),
            alert_data=event.pop(FieldNames.ALERT_DATA, None),
        )

        nodes = self.transform(event)

        if not nodes:
            return (alert,)

        for node in nodes:
            if FieldNames.TIMESTAMP in event:
                alert.alerted_on[node].append(timestamp=event[FieldNames.TIMESTAMP])
            else:
                alert.alerted_on[node]

        return (alert,) + nodes

    def make_process(self, event: dict) -> Tuple[Process, File, Process, File]:
        """Accepts a process with the `EventTypes.PROCESS_LAUNCHED` event_type.

        For example::

            {
                FieldNames.PARENT_PROCESS_IMAGE: "cmd.exe",
                FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
                FieldNames.PARENT_PROCESS_ID: "2568",
                FieldNames.PARENT_COMMAND_LINE: '/K name.exe"',
                FieldNames.PROCESS_IMAGE: "find.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: 'find /i "svhost.exe"',
                FieldNames.PROCESS_ID: "3144",
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            }

        Parameters
        ----------
        event : dict
            [description]

        Returns
        -------
        Tuple[Process, File, Process, File]
            [description]
        """

        parent = Process(
            process_image=event[FieldNames.PARENT_PROCESS_IMAGE],
            process_image_path=event[FieldNames.PARENT_PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PARENT_PROCESS_ID]),
            command_line=event[FieldNames.PARENT_COMMAND_LINE],
        )

        # Create the file node.
        # TODO: Integrate into the Process() init function?
        parent_file = parent.get_file_node()
        parent_file.file_of[parent]

        child = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        child_file = child.get_file_node()
        child_file.file_of[child]

        if FieldNames.TIMESTAMP in event:
            parent.launched[child].append(timestamp=int(event[FieldNames.TIMESTAMP]))
        else:
            parent.launched[child]

        return (parent, parent_file, child, child_file)

    def make_basic_file(self, event: dict) -> Tuple[Process, File, File]:
        """Transforms a file based event.

        Support events:

        1. EventTypes.FILE_DELETED

        2. EventTypes.FILE_OPENED

        3. EventTypes.FILE_WRITTEN

        4. EventTypes.LOADED_MODULE


        Parameters
        ----------
        event : dict
            [description]

        Returns
        -------
        Tuple[Process, File, File]
            [description]
        """

        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        file_node = File(
            file_path=event[FieldNames.FILE_PATH],
            file_name=event[FieldNames.FILE_NAME],
            hashes=event.get(FieldNames.HASHES),
        )

        file_node.set_extension()

        # Switch based on the event type
        event_type = event[FieldNames.EVENT_TYPE]

        if event_type == EventTypes.FILE_OPENED:
            process.accessed[file_node]
        elif event_type == EventTypes.FILE_WRITTEN:
            process.wrote[file_node]
        elif event_type == EventTypes.LOADED_MODULE:
            process.loaded[file_node]
        else:
            process.deleted[file_node]

        return (process, proc_file, file_node)

    def make_file_copy(self, event: dict) -> Tuple[Process, File, File, File]:
        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        # Source file
        src_file = File(
            file_path=event[FieldNames.SRC_FILE][FieldNames.FILE_PATH],
            file_name=event[FieldNames.SRC_FILE][FieldNames.FILE_NAME],
            hashes=event[FieldNames.SRC_FILE].get(FieldNames.HASHES),
        )

        # Dest file
        src_file.set_extension()

        dest_file = File(
            file_path=event[FieldNames.DEST_FILE][FieldNames.FILE_PATH],
            file_name=event[FieldNames.DEST_FILE][FieldNames.FILE_NAME],
            hashes=event[FieldNames.DEST_FILE].get(FieldNames.HASHES),
        )

        dest_file.set_extension()

        src_file.copied_to[dest_file]

        process.copied[src_file]

        return (process, proc_file, src_file, dest_file)

    def make_connection(self, event: dict) -> Tuple[Process, File, IPAddress]:
        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        addr = IPAddress(ip_address=event[FieldNames.IP_ADDRESS])

        if FieldNames.PORT in event and FieldNames.PROTOCOL in event:
            process.connected_to[addr].append(
                port=int(event[FieldNames.PORT]), protocol=event[FieldNames.PROTOCOL]
            )
        elif FieldNames.PORT in event:
            process.connected_to[addr].append(port=int(event[FieldNames.PORT]))
        elif FieldNames.PROTOCOL in event:
            process.connected_to[addr].append(protocol=event[FieldNames.PROTOCOL])
        else:
            process.connected_to[addr]

        return (process, proc_file, addr)

    def make_http_req(
        self, event: dict
    ) -> Union[Tuple[Process, File, URI, Domain], Tuple[Process, File, URI, Domain, IPAddress]]:
        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        dom = Domain(event[FieldNames.HTTP_HOST])
        uri = URI(uri=event[FieldNames.URI])

        uri.uri_of[dom]

        process.http_request_to[uri].append(method=event[FieldNames.HTTP_METHOD])

        if FieldNames.IP_ADDRESS in event:
            ip = IPAddress(event[FieldNames.IP_ADDRESS])
            dom.resolves_to[ip]
            process.connected_to[ip]
            return (process, proc_file, uri, dom, ip)
        else:
            return (process, proc_file, uri, dom)

    def make_dnslookup(
        self, event: dict
    ) -> Union[Tuple[Process, File, Domain, IPAddress], Tuple[Process, File, Domain]]:
        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        dom = Domain(event[FieldNames.HTTP_HOST])

        process.dns_query_for[dom]

        # Sometimes we don't know what the domain resolved to.
        if FieldNames.IP_ADDRESS in event:
            addr = IPAddress(ip_address=event[FieldNames.IP_ADDRESS])

            dom.resolves_to[addr]

            return (process, proc_file, dom, addr)
        else:
            return (process, proc_file, dom)

    def make_basic_regkey(self, event: dict) -> Tuple[Process, File, RegistryKey]:

        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        # RegistryKey Node Creation
        reg_node = RegistryKey(
            hive=event[FieldNames.HIVE],
            key_path=event[FieldNames.REG_KEY_PATH],
            key=event[FieldNames.REG_KEY],
        )

        if event["event_type"] == EventTypes.REG_KEY_OPENED:
            process.read_key[reg_node]
        else:
            process.deleted_key[reg_node]

        return (process, proc_file, reg_node)

    def make_regkey_set_value(self, event: dict) -> Tuple[Process, File, RegistryKey]:

        process = Process(
            process_image=event[FieldNames.PROCESS_IMAGE],
            process_image_path=event[FieldNames.PROCESS_IMAGE_PATH],
            process_id=int(event[FieldNames.PROCESS_ID]),
            command_line=event[FieldNames.COMMAND_LINE],
        )

        proc_file = process.get_file_node()
        proc_file.file_of[process]

        # RegistryKey Node Creation
        reg_node = RegistryKey(
            hive=event[FieldNames.HIVE],
            key_path=event[FieldNames.REG_KEY_PATH],
            key=event[FieldNames.REG_KEY],
            value=event.get(FieldNames.REG_KEY_VALUE),
        )

        if reg_node.value:
            process.changed_value[reg_node].append(value=reg_node.value)
        else:
            process.changed_value[reg_node]

        return (process, proc_file, reg_node)
