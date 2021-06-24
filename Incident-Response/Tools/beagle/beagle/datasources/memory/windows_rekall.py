import logging
from typing import Dict, Generator


from beagle.common import split_path, logger
from beagle.constants import EventTypes, FieldNames
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.generic_transformer import GenericTransformer


class WindowsMemory(DataSource):
    """Yields events from a raw memory file by leveraging Rekall plugins.

    This DataSource converts the outputs of the plugins to the schema provided by
    GenericTransformer.

    Parameters
    ----------
    memory_image : str
        File path to the memory image.
    """

    name = "Windows Memory"
    transformers = [GenericTransformer]
    category = "Windows Memory"

    def __init__(self, memory_image: str) -> None:

        self.memory_image = memory_image
        self._imported_rekall = False
        self.session = self._setup_session()

        # Map PID to parsed process objects.
        self.processes: Dict[int, dict] = {}

    def metadata(self) -> dict:
        return {}

    def _setup_session(self):
        # Import rekall on first load.
        if not self._imported_rekall:  # noqa
            from rekall import session, plugins  # noqa

            self._imported_rekall = True  # noqa

        return session.Session(
            filename=self.memory_image,
            autodetect=["rsds"],
            logger=logging.getLogger("loguru"),  # Get the loguru logger
            autodetect_scan_length=18_446_744_073_709_551_616,
            profile_path=["http://profiles.rekall-forensic.com"],
        )

    def events(self) -> Generator[dict, None, None]:
        for func in [self.pslist, self.handles, self.connscan]:
            yield from func()

    def pslist(self) -> Generator[dict, None, None]:
        """Converts the output of rekall's `pslist` plugin to a series of dictionaries
        that represent a process getting launched.

        Returns
        -------
        Generator[dict, None, None]
            Yields one process launch event
        """

        # Function to switch fields to represent a parent
        def _convert_to_parent_fields(process: dict) -> dict:
            output = {}
            for left, right in [
                (FieldNames.PROCESS_IMAGE, FieldNames.PARENT_PROCESS_IMAGE),
                (FieldNames.PROCESS_ID, FieldNames.PARENT_PROCESS_ID),
                (FieldNames.COMMAND_LINE, FieldNames.PARENT_COMMAND_LINE),
                (FieldNames.PROCESS_IMAGE_PATH, FieldNames.PARENT_PROCESS_IMAGE_PATH),
            ]:
                output[right] = process[left]

            return output

        # Use the pstree dict output to get a mapping from pid -> proc
        procs = self.session.plugins.pstree()._make_process_dict()

        parent_procs: Dict[int, dict] = {}

        # Add the system idle process
        parent_procs[0] = {
            FieldNames.PARENT_PROCESS_ID: 0,
            FieldNames.PARENT_COMMAND_LINE: "",
            FieldNames.PARENT_PROCESS_IMAGE: "System Idle Process",
            FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
        }

        for proc in procs.values():

            parent_pid = proc.InheritedFromUniqueProcessId

            # Get the current processes info
            command_line = str(proc.Peb.ProcessParameters.CommandLine)
            image_path = str(proc.Peb.ProcessParameters.ImagePathName)

            if int(proc.pid) == 4:
                process_image = "SYSTEM"
                process_image_path = "\\"
            else:
                process_image, process_image_path = split_path(image_path)

            current_proc = {
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
                FieldNames.PROCESS_ID: int(proc.pid),
                FieldNames.COMMAND_LINE: command_line,
                FieldNames.PROCESS_IMAGE: process_image,
                FieldNames.PROCESS_IMAGE_PATH: process_image_path,
            }

            # Keep track of the processes.
            self.processes[int(proc.pid)] = current_proc

            current_as_parent = _convert_to_parent_fields(current_proc)
            parent_procs[int(proc.pid)] = current_as_parent

            # Parse the parent process
            if parent_pid not in parent_procs:

                # Do we the _EPROCESS for this process?
                if int(parent_pid) in procs:
                    parent = procs[int(parent_pid)]
                    parent_image_path = parent.Peb.ProcessParameters.ImagePathName

                    parent_process_image, parent_process_image_path = split_path(
                        str(parent_image_path)
                    )

                    parent_proc = {
                        FieldNames.PARENT_PROCESS_ID: int(parent.pid),
                        FieldNames.PARENT_COMMAND_LINE: parent.Peb.ProcessParameters.CommandLine,
                        FieldNames.PARENT_PROCESS_IMAGE: parent_process_image,
                        FieldNames.PARENT_PROCESS_IMAGE_PATH: parent_process_image_path,
                    }

                # If not, make a dummy one with the PID
                else:
                    parent_proc = {
                        FieldNames.PARENT_PROCESS_ID: int(parent_pid),
                        FieldNames.PARENT_COMMAND_LINE: "",
                        FieldNames.PARENT_PROCESS_IMAGE: "",
                        FieldNames.PARENT_PROCESS_IMAGE_PATH: "",
                    }

                parent_procs[int(parent_pid)] = parent_proc

            yield {**current_proc, **parent_procs[int(parent_pid)]}

    def handles(self) -> Generator[dict, None, None]:
        """Converts the output of the rekall `handles` plugin to a series
        of events which represent accessing registry keys or file.

        Yields
        -------
        Generator[dict, None, None]
            One file or registry key access event a time.
        """

        for handle in self.session.plugins.handles().collect():

            # Regardless of if we use this handle or not, can make a process node
            # if this is a process that wasnt in pslist/pstree.
            e_proc = handle["_EPROCESS"]
            pid = int(e_proc.pid)

            if pid in self.processes:
                proc_data = self.processes[pid]
            else:
                logger.warn(f"Previously unseen PID={pid} showed up in handles")

            if handle["obj_type"] == "File":

                full_file_path = handle["details"]

                if full_file_path.startswith("\\"):
                    full_file_path = full_file_path[1:]

                file_path, file_name = split_path(full_file_path)
                yield {
                    FieldNames.FILE_PATH: file_path,
                    FieldNames.FILE_NAME: file_name,
                    **proc_data,
                    FieldNames.EVENT_TYPE: EventTypes.FILE_OPENED,
                }
            elif handle["obj_type"] == "Key":

                key_path = handle["details"]
                if key_path.startswith("MACHINE\\"):
                    start_indx = len("MACHINE\\")
                    key_path = key_path[start_indx:]

                hive = key_path.split("\\")[0]
                key = key_path.split("\\")[-1]
                key_path = key_path[len(hive) : len(key)]

                yield {
                    FieldNames.HIVE: hive,
                    FieldNames.REG_KEY: key,
                    FieldNames.REG_KEY_PATH: key_path,
                    **proc_data,
                    FieldNames.EVENT_TYPE: EventTypes.REG_KEY_OPENED,
                }

    def connscan(self) -> Generator[dict, None, None]:
        # TODO: Requires getting my hands on a memory image that outputs
        # data from connscan.
        yield {}

        # for tcp_obj, _, _, _ in self.session.plugins.connscan().collect():
        #     TOOD: Process
