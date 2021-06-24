import pytest

from beagle import transformers
from beagle.constants import EventTypes, FieldNames, Protocols
from beagle.nodes import URI, Domain, File, IPAddress, Process, RegistryKey
from beagle.transformers import ProcmonTransformer

# Schema for inputs

"""
{
    "event_time": epoch,
    "event_type": row["Operation"],
    "process_name": row["Process Name"],
    "path": row["Path"],
    "process_id": int(row["PID"]),
    "params": row["Detail"],
}
"""


@pytest.fixture
def transformer() -> ProcmonTransformer:
    return ProcmonTransformer(datasource=None)  # type: ignore


def test_init(transformer):
    assert isinstance(transformer, ProcmonTransformer)


def test_process_created(transformer):
    input_event = {
        "event_time": 1,
        "event_type": "Process Create",
        "process_name": "svchost.exe",
        "path": "C:\\Windows\\system32\\DllHost.exe",
        "process_id": "1234",
        "params": "PID: 4844, Command line: C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}",
    }

    nodes = transformer.transform(input_event)
    assert len(nodes) == 3
    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    parent: Process = nodes[2]

    assert proc.process_id == 4844
    assert (
        proc.command_line
        == "C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}"
    )

    assert proc_file.file_name == proc.process_image == "DllHost.exe"
    assert parent.process_id == 1234
    assert parent.process_image == "svchost.exe"


@pytest.mark.parametrize("event_type", ["CreateFile", "WriteFile"])
def test_write_file(transformer, event_type):
    input_event = {
        "event_time": 1,
        "event_type": event_type,
        "process_name": "svchost.exe",
        "path": "C:\\Windows\\system32\\DllHost.exe",
        "process_id": "1234",
    }
    nodes = transformer.transform(input_event)
    assert len(nodes) == 2
    proc: Process = nodes[0]
    file_node: File = nodes[1]

    assert file_node.file_name == "DllHost.exe"
    assert file_node.file_path == "C:\\Windows\\system32"
    assert file_node in proc.wrote


@pytest.mark.parametrize("event_type", ["ReadFile", "CloseFile"])
def test_access_file(transformer, event_type):
    input_event = {
        "event_time": 1,
        "event_type": event_type,
        "process_name": "svchost.exe",
        "path": "C:\\Windows\\system32\\DllHost.exe",
        "process_id": "1234",
    }
    nodes = transformer.transform(input_event)
    assert len(nodes) == 2
    proc: Process = nodes[0]
    file_node: File = nodes[1]

    assert file_node.file_name == "DllHost.exe"
    assert file_node.file_path == "C:\\Windows\\system32"
    assert file_node in proc.accessed


@pytest.mark.parametrize(
    "event_type", ["RegOpenKey", "RegQueryKey", "RegQueryValue", "RegCloseKey"]
)
def test_regopenkey(event_type, transformer):
    input_event = {
        "event_time": 1,
        "event_type": event_type,
        "process_name": "svchost.exe",
        "path": "HKCU\\Software\\Classes\\CLSID\\{56AD4C5D-B908-4F85-8FF1-7940C29B3BCF}\\Instance",
        "process_id": "1234",
    }
    nodes = transformer.transform(input_event)
    assert len(nodes) == 2
    proc: Process = nodes[0]
    reg_key: RegistryKey = nodes[1]

    assert proc.process_id == 1234
    assert proc.process_image == "svchost.exe"
    assert reg_key.hive == "HKCU"
    assert reg_key.key_path == "Software\\Classes\\CLSID\\{56AD4C5D-B908-4F85-8FF1-7940C29B3BCF}"
    assert reg_key.key == "Instance"
    assert reg_key in proc.read_key


@pytest.mark.parametrize(
    "event_type", ["TCP Send", "TCP Receive", "TCP Connect", "UDP Connect", "UDP Receive"]
)
def test_connectin(event_type, transformer):
    input_event = {
        "event_time": 1,
        "event_type": event_type,
        "process_name": "svchost.exe",
        "path": "192.168.10.1:1234 -> 127.0.0.1:1337",
        "process_id": "1234",
    }
    nodes = transformer.transform(input_event)
    assert len(nodes) == 2
    proc: Process = nodes[0]
    addr: IPAddress = nodes[1]

    assert proc.process_id == 1234
    assert proc.process_image == "svchost.exe"
    assert addr.ip_address == "127.0.0.1"
    assert {
        "port": 1337,
        "timestamp": 1,
        "protocol": event_type.split(" ")[0],
    } in proc.connected_to[addr]
