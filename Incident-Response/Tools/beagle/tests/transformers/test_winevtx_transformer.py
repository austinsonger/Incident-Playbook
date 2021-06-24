import pytest

from beagle.nodes import File, Process
from beagle.transformers.evtx_transformer import WinEVTXTransformer


@pytest.fixture
def transformer() -> WinEVTXTransformer:
    return WinEVTXTransformer(None)


def test_process_creation(transformer):
    input_event = {
        "provider_name": "Microsoft-Windows-Security-Auditing",
        "provider_guid": "{54849625-5478-4994-a5ba-3e3b0328c30d}",
        "eventid_qualifiers": "4688",
        "version": "1",
        "level": "0",
        "task": "13312",
        "opcode": "0",
        "keywords": "0x8020000000000000",
        "timecreated_systemtime": 1_474_410_459,
        "eventrecordid": "13344",
        "correlation_activityid": "",
        "correlation_relatedactivityid": "",
        "execution_processid": "4",
        "execution_threadid": "60",
        "channel": "Security",
        "computer": "IE10Win7",
        "security_userid": "",
        "system": None,
        "data_name_subjectusersid": "S-1-5-18",
        "data_name_subjectusername": "IE10WIN7$",
        "data_name_subjectdomainname": "WORKGROUP",
        "data_name_subjectlogonid": "0x00000000000003e7",
        "data_name_newprocessid": "0x00000dec",
        "data_name_newprocessname": "C:\\Windows\\System32\\dllhost.exe",
        "data_name_tokenelevationtype": "%%1938",
        "data_name_processid": "0x00000248",
        "data_name_commandline": "C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}",
        "eventdata": None,
        "event": None,
    }

    nodes = transformer.transform(input_event)

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    parent: Process = nodes[2]

    assert proc.process_id == 3564
    assert proc.process_image == "dllhost.exe"
    assert proc.process_image_path == "C:\\Windows\\System32"
    assert (
        proc.command_line
        == "C:\\Windows\\system32\\DllHost.exe /Processid:{AB8902B4-09CA-4BB6-B78D-A8F59079A8D5}"
    )
    assert proc.host == "IE10Win7"

    assert parent.process_id == 584
    assert proc_file.file_name == "dllhost.exe"

    assert {"timestamp": 1_474_410_459} in parent.launched[proc]
