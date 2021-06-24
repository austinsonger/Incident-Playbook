from typing import Dict, Optional, Tuple, Union

from beagle.common import logger, split_path
from beagle.constants import Protocols
from beagle.nodes import URI, Domain, File, IPAddress, Node, Process, RegistryKey, Alert
from beagle.transformers.base_transformer import Transformer


class FireEyeHXTransformer(Transformer):

    name = "FireEye HX"

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        logger.info("Created FireEyeHX Transformer.")

    def transform(self, event: dict) -> Optional[Tuple[Node, ...]]:
        """Sends each event from the FireEye HX Triage to the appropriate
        node creation function.

        Parameters
        ----------
        event : dict
            The source event from the HX Triage

        Returns
        -------
        Optional[Tuple[Node, ...]]
            The results of the transforming function
        """

        # NOTE: Manually created event_type in HXTriage
        # Check happens before the process path because
        # we don't expect these events to have that.
        if event["event_type"] == "alertEvent":
            return self.make_alert(event)

        # If there's no value in processPath, we can't create the process node properly.
        if "processPath" in event and not event["processPath"]:
            return None

        # Event types from the agent events.
        if event["event_type"] == "processEvent":
            return self.make_process(event)
        elif event["event_type"] == "fileWriteEvent":
            return self.make_file(event)
        elif event["event_type"] == "urlMonitorEvent":
            return self.make_url(event)
        elif event["event_type"] == "ipv4NetworkEvent":
            return self.make_network(event)
        elif event["event_type"] == "dnsLookupEvent":
            return self.make_dnslookup(event)
        elif event["event_type"] == "imageLoadEvent":
            return self.make_imageload(event)
        elif event["event_type"] == "regKeyEvent":
            return self.make_registry(event)
        else:
            return None

    def make_process(
        self, event: dict
    ) -> Optional[Union[Tuple[Process, File], Tuple[Process, File, Process, File]]]:
        """Converts a processEvent into either one Process node, or two Process nodes with a
        parent - (Launched) -> child relationship.
        Additionally, creats File nodes for the images of both of the Processe's identified.

        Parameters
        ----------
        event : dict
            The processEvent event

        Returns
        -------
        Optional[Union[Tuple[Process, File], Tuple[Process, File, Process, File]]]
            Returns either a single process node, or a (parent, child) tuple
            where the parent has a launched edge to the child.
        """

        # Only look at start or already running event types.
        if event["eventType"] not in ["start", "running"]:
            return None

        # Sometimes a process in a `running` state doens't properly identify the path
        # which causes a case where processPath == process.
        # For example {"process": "cmd.exe", "processPath": "cmd.exe"}

        # See: test_process_equal_processpath
        if event["processPath"] == event["process"]:
            return None

        process_image, process_image_path = split_path(event["processPath"])

        # Pull out the hashes
        hashes: Dict[str, str] = {}
        if event.get("md5"):
            hashes = {"md5": event["md5"]}

        # Create the "child" process. This is the process who this event
        # belongs to.
        child = Process(
            process_image=process_image,
            process_image_path=process_image_path,
            command_line=event.get("processCmdLine"),
            process_id=int(event["pid"]),
            hashes=hashes,
            user=event.get("username", None),
        )

        # Pull out the image of the child process
        child_proc_file_node = child.get_file_node()

        # File - (File Of) -> Process
        child_proc_file_node.file_of[child]

        # If there is no parent field, return just the child
        if "parentProcessPath" not in event:

            return (child, child_proc_file_node)

        parent_process_image, parent_process_image_path = split_path(event["parentProcessPath"])

        # Create the parent process
        parent = Process(
            process_id=int(event["parentPid"]),
            process_image=parent_process_image,
            process_image_path=parent_process_image_path,
        )

        # Create a parent - (launched) -> child edge.
        parent.launched[child].append(timestamp=event["event_time"])

        # Pull out the image of the parent process
        parent_proc_file_node = child.get_file_node()

        # File - (File Of) -> Process
        parent_proc_file_node.file_of[child]

        return (parent, parent_proc_file_node, child, child_proc_file_node)

    def make_file(self, event: dict) -> Optional[Tuple[File, Process, File]]:
        """Converts a fileWriteEvent to two nodes, a file and the process manipulated the file.
        Generates a process - (Wrote) -> File edge.

        Parameters
        ----------
        event : dict
            The fileWriteEvent event.

        Returns
        -------
        Optional[Tuple[File, Process, File]]
            Returns a tuple contaning the File that this event is focused on, and the process
            which manipulated the file. The process has a Wrote edge to the file. Also contains
            the file that the process belongs to.
        """

        if "filePath" not in event:
            return None

        # Add the drive where possible.
        if event.get("drive"):
            file_path = f"{event['drive']}:\\{event['filePath']}"
        else:
            file_path = event["filePath"]

        hashes: Dict[str, str] = {}
        if event.get("md5"):
            hashes = {"md5": event["md5"]}

        # Create the file node.
        file_node = File(file_path=file_path, file_name=event["fileName"], hashes=hashes)

        # Set the extension
        file_node.set_extension()

        # Set the process node
        process = Process(
            process_id=int(event["pid"]),
            process_image=event["process"],
            process_image_path=event["processPath"],
            user=event.get("username"),
        )

        # Add a wrote edge with the contents of the file write.
        process.wrote[file_node].append(
            timestamp=int(event["event_time"]), contents=event.get("textAtLowestOffset")
        )

        # Pull out the image of the process
        proc_file_node = process.get_file_node()

        # File - (File Of) -> Process
        proc_file_node.file_of[process]

        return (file_node, process, proc_file_node)

    def make_url(self, event: dict) -> Optional[Tuple[URI, Domain, Process, File, IPAddress]]:
        """Converts a URL access event and returns 5 nodes with 4 different relationships.

        Nodes created:

        1. URI Accessed (e.g /foobar)

        2. Domain Accessed (e.g omer.com)

        3. Process performing URL request.

        4. File object for the Process image.

        5. IP Address the domain resolves to.

        Relationships created:

        1. URI - (URI Of) -> Domain

        2. Domain - (Resolves To) -> IP Address

        3. Process - (`http method of event`) -> URI

        4. Process - (Connected To) -> IP Address

        5. File - (File Of) -> Process

        Parameters
        ----------
        event : dict
            The urlMonitorEvent events

        Returns
        -------
        Optional[Tuple[URI, Domain, Process, File, IPAddress]]
            5 tuple of the nodes pulled out of the event (see function description).
        """

        uri = URI(uri=event["requestUrl"])
        domain = Domain(domain=event["hostname"])
        ip_address = IPAddress(ip_address=event["remoteIpAddress"])

        # Pull out the process fields.
        process = Process(
            process_image=event["process"],
            process_image_path=event["processPath"],
            command_line=event.get("processCmdLine"),
            process_id=int(event["pid"]),
            user=event.get("username", None),
        )

        # Pull out the image of the process
        file_node = process.get_file_node()

        # File - (File Of) -> Process
        file_node.file_of[process]

        # Link up the URI and the domain
        # URI - (URI Of) -> Domain
        uri.uri_of[domain].append(timestamp=event["event_time"])

        # HTTP Request to the URL from the process
        # Proc - (HTTP Request) -> URI
        process.http_request_to[uri].append(
            method=event.get("urlMethod"),
            user_agent=event.get("userAgent"),
            header=event.get("httpHeader"),
            timestamp=event["event_time"],
        )

        # TCP Communication from process to IP of domain
        # Process - (Connected To) -> IP Address
        process.connected_to[ip_address].append(
            port=int(event["remotePort"]), protocol=Protocols.HTTP, timestamp=event["event_time"]
        )

        # Domain resolving to that IP
        # Domain - (Resolves To) -> IP Address
        domain.resolves_to[ip_address].append(timestamp=event["event_time"])

        return (uri, domain, process, file_node, ip_address)

    def make_network(self, event: dict) -> Optional[Tuple[IPAddress, Process, File]]:
        """Converts a network connection event into a Process, File and IP Address node.

        Nodes:

        1. IP Address communicated to.

        2. Process contacting IP.

        3. File process launched from.

        Edges:

        1. Process - (Connected To) -> IP Address

        2. File - (File Of) -> Process

        Parameters
        ----------
        event : dict
            The ipv4NetworkEvent

        Returns
        -------
        Optional[Tuple[IPAddress, Process, File]]
            The IP Address, Process, and Process's File object.
        """

        # Pull out the process fields.
        process = Process(
            process_image=event["process"],
            process_image_path=event["processPath"],
            process_id=int(event["pid"]),
            user=event.get("username", None),
        )

        # Pull out the image of the process
        file_node = process.get_file_node()

        # File - (File Of) -> Process
        file_node.file_of[process]

        # Create the network node
        ip_address = IPAddress(event["remoteIP"])

        # Create the connection edge
        # Process - (Connected To) -> IP Address
        process.connected_to[ip_address].append(
            timestamp=event["event_time"], protocol=event["protocol"], port=int(event["remotePort"])
        )

        return (ip_address, process, file_node)

    def make_dnslookup(self, event: dict) -> Optional[Tuple[Domain, Process, File]]:
        """Converts a dnsLookupEvent into a Domain, Process, and Process's File node.

        Nodes:
        1. Domain looked up.

        2. Process performing the lookup.

        3. File the Process was launched from.

        Edges:

        1. Process - (DNS Lookup For) -> Domain.

        2. File - (FileOf) -> Process.

        Parameters
        ----------
        event : dict
            A dnsLookupEvent

        Returns
        -------
        Optional[Tuple[Domain, Process, File]]
            The Domain, Process, and File nodes.
        """

        # Pull out the process fields.
        process = Process(
            process_image=event["process"],
            process_image_path=event["processPath"],
            process_id=int(event["pid"]),
            user=event.get("username", None),
        )

        # Pull out the image of the process
        file_node = process.get_file_node()

        # File - (File Of) -> Process
        file_node.file_of[process]

        domain = Domain(event["hostname"])

        process.dns_query_for[domain].append(timestamp=event["event_time"])

        return (domain, process, file_node)

    def make_imageload(self, event: dict) -> Optional[Tuple[File, Process, File]]:
        # Pull out the process fields.
        process = Process(
            process_image=event["process"],
            process_image_path=event["processPath"],
            process_id=int(event["pid"]),
            user=event.get("username", None),
        )

        # Pull out the image of the process
        file_node = process.get_file_node()

        # File - (File Of) -> Process
        file_node.file_of[process]

        # Add the drive where possible.
        if event.get("drive"):
            file_path = f"{event['drive']}:\\{event['filePath']}"
        else:
            file_path = event["filePath"]

        loaded_file = File(file_path=file_path, file_name=event["fileName"])

        loaded_file.set_extension()

        process.loaded[loaded_file].append(timestamp=event["event_time"])

        return (loaded_file, process, file_node)

    def make_registry(self, event: dict) -> Optional[Tuple[RegistryKey, Process, File]]:
        # Pull out the process fields.
        process = Process(
            process_image=event["process"],
            process_image_path=event["processPath"],
            process_id=int(event["pid"]),
            user=event.get("username", None),
        )

        # Pull out the image of the process
        file_node = process.get_file_node()

        # File - (File Of) -> Process
        file_node.file_of[process]

        # RegistryKey Node Creation
        reg_node = RegistryKey(
            hive=event["hive"],
            key_path=event["keyPath"],
            key=event.get("valueName"),
            value=event.get("text"),
            value_type=event.get("valueType"),
        )

        # Space shuttle code for the edge setting
        #
        # EventType Mappings:
        #     1: Value Changed
        #     2: Value Deleted
        #     3: Key Created
        #     4: Key Deleted
        #
        reg_event_type = str(event["eventType"])
        if reg_event_type == "1":
            process.changed_value[reg_node].append(timestamp=event["event_time"])
        elif reg_event_type == "2":
            process.deleted_value[reg_node].append(timestamp=event["event_time"])
        elif reg_event_type == "3":
            process.created_key[reg_node].append(timestamp=event["event_time"])
        elif reg_event_type == "4":
            process.deleted_key[reg_node].append(timestamp=event["event_time"])
        else:
            logger.warn(
                f"Found a new registry event type with a value of {reg_event_type}: {event}"
            )

        return (reg_node, process, file_node)

    def make_alert(self, event: dict) -> Optional[Tuple[Alert, ...]]:

        # Fixes issue where no event metadata in the Triage.
        if "_threat_data" not in event:
            alert_name = event["match_hash"]
        else:
            uri_name = event["_threat_data"].get("uri_name")
            display_name = event["_threat_data"].get("display_name")

            alert_name = display_name or uri_name

        alert = Alert(alert_name=alert_name, alert_data="No data")

        alerting_event_type = event["data"]["key"]["event_type"]

        # Strip the event type
        alerting_event = event["data"]["values"]

        alerting_event["event_type"] = alerting_event_type

        # Create all nodes from the alerted on event
        alerted_on_nodes = self.transform(alerting_event)

        if not alerted_on_nodes:
            return (alert,)

        # Set edges from the alert node to all alerted on nodes.
        for node in alerted_on_nodes:
            alert.alerted_on[node].append(timestamp=event["event_time"])

        # This returns a tuple compromise of the alert node, and all alerted nodes
        return (alert,) + alerted_on_nodes  # type: ignore

