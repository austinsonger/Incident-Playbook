from typing import Dict, Optional, Tuple, Union

from beagle.common import logger, split_path
from beagle.constants import Protocols
from beagle.nodes import URI, Domain, File, IPAddress, Node, Process, RegistryKey, Alert
from beagle.transformers.base_transformer import Transformer


class WinEVTXTransformer(Transformer):

    name = "Win EVTX"

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

        logger.info("Created Windows EVTX Transformer.")

    def transform(self, event: dict) -> Optional[Tuple]:

        # Track which processese we've seen
        self.seen_procs: Dict[int, Process] = {}

        event_id = int(event["eventid_qualifiers"])

        if event_id == 4688:
            return self.process_creation(event)

        return None

    def process_creation(self, event: dict) -> Tuple[Process, File, Process]:
        """Transformers a process creation (event ID 4688) into a set of nodes.

        https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventID=4688

        Parameters
        ----------
        event : dict
            [description]

        Returns
        -------
        Optional[Tuple[Process, File, Process, File]]
            [description]
        """

        # Get the parent PID
        parent_pid = int(event["data_name_processid"], 16)

        # Child PID
        child_pid = int(event["data_name_newprocessid"], 16)

        proc_name, proc_path = split_path(event["data_name_newprocessname"])

        child = Process(
            host=event["computer"],
            process_id=child_pid,
            user=event["data_name_subjectusername"],
            process_image=proc_name,
            process_image_path=proc_path,
            command_line=event.get("data_name_commandline"),
        )

        child_file = child.get_file_node()
        child_file.file_of[child]

        # Map the process for later
        self.seen_procs[child_pid] = child

        parent = self.seen_procs.get(parent_pid)

        if parent is None:
            # Create a dummy proc. If we haven't already seen the parent
            parent = Process(host=event["computer"], process_id=parent_pid)

        parent.launched[child].append(timestamp=event["timecreated_systemtime"])

        # Don't need to pull out the parent's file, as it will have always
        # been created before being put into seen_procs

        return (child, child_file, parent)
