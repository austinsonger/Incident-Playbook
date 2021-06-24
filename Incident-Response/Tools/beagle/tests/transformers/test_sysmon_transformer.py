import pytest

from beagle.nodes import File, Process, Domain, IPAddress, RegistryKey
from beagle.transformers.sysmon_transformer import SysmonTransformer


@pytest.fixture
def transformer() -> SysmonTransformer:
    return SysmonTransformer(None)


def test_dns_event(transformer):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "22",
        "Version": "5",
        "Level": "4",
        "Task": "22",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2019-08-03 14:31:49.660530",
        "TimeCreated": None,
        "EventRecordID": "295",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "7176",
        "Execution_ThreadID": "4604",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-3KI19E0",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_RuleName": None,
        "EventData_UtcTime": 1564857108,
        "EventData_ProcessGuid": "{8eb9d026-9ad2-5d45-0000-0010b7760001}",
        "EventData_ProcessId": "4776",
        "EventData_QueryName": "share.microsoft.com",
        "EventData_QueryStatus": "0",
        "EventData_QueryResults": "type:  5 share.microsoft.com.edgekey.net;type:  5 e11095.dscd.akamaiedge.net;::ffff:23.32.80.227;",
        "EventData_Image": "C:\\Windows\\System32\\AppHostRegistrationVerifier.exe",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 3
    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    domain: Domain = nodes[2]

    assert domain in proc.dns_query_for
    assert domain.domain == "share.microsoft.com"
    assert proc in proc_file.file_of


def test_process_creation(transformer):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "1",
        "Version": "5",
        "Level": "4",
        "Task": "1",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2019-08-03 14:24:22.586109",
        "TimeCreated": None,
        "EventRecordID": "3",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "7176",
        "Execution_ThreadID": "4528",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-3KI19E0",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_RuleName": None,
        "EventData_UtcTime": 1564856662,
        "EventData_ProcessGuid": "{8eb9d026-9916-5d45-0000-001020f6b700}",
        "EventData_ProcessId": "7176",
        "EventData_Image": "C:\\Windows\\Sysmon64.exe",
        "EventData_FileVersion": "10.2",
        "EventData_Description": "System activity monitor",
        "EventData_Product": "Sysinternals Sysmon",
        "EventData_Company": "Sysinternals - www.sysinternals.com",
        "EventData_OriginalFileName": "?",
        "EventData_CommandLine": "C:\\Windows\\Sysmon64.exe",
        "EventData_CurrentDirectory": "C:\\Windows\\system32\\",
        "EventData_User": "NT AUTHORITY\\SYSTEM",
        "EventData_LogonGuid": "{8eb9d026-bb89-5ca7-0000-0020e7030000}",
        "EventData_LogonId": "0x00000000000003e7",
        "EventData_TerminalSessionId": "0",
        "EventData_IntegrityLevel": "System",
        "EventData_Hashes": "SHA1=751602F5D1F36C594196BEF744E32983F5291E49",
        "EventData_ParentProcessGuid": "{8eb9d026-bb89-5ca7-0000-001014a20000}",
        "EventData_ParentProcessId": "616",
        "EventData_ParentImage": "C:\\Windows\\System32\\services.exe",
        "EventData_ParentCommandLine": "C:\\Windows\\system32\\services.exe",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 4
    parent_proc: Process = nodes[0]
    proc: Process = nodes[2]

    assert parent_proc.launched[proc]


def test_network_connection_no_hostname(transformer):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "3",
        "Version": "5",
        "Level": "4",
        "Task": "3",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2015-10-08 14:14:14.747887",
        "TimeCreated": None,
        "EventRecordID": "990",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "4072",
        "Execution_ThreadID": "4620",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-OALUEJ1",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_UtcTime": 1444328053,
        "EventData_ProcessGuid": "{90e22fd2-8107-5615-0000-001090bd0100}",
        "EventData_ProcessId": "1704",
        "EventData_Image": "C:\\Windows\\System32\\svchost.exe",
        "EventData_User": "NT AUTHORITY\\SYSTEM",
        "EventData_Protocol": "tcp",
        "EventData_Initiated": "True",
        "EventData_SourceIsIpv6": "False",
        "EventData_SourceIp": "192.168.191.148",
        "EventData_SourceHostname": "DESKTOP-OALUEJ1.localdomain",
        "EventData_SourcePort": "1735",
        "EventData_SourcePortName": None,
        "EventData_DestinationIsIpv6": "False",
        "EventData_DestinationIp": "111.221.29.254",
        "EventData_DestinationHostname": None,
        "EventData_DestinationPort": "443",
        "EventData_DestinationPortName": "https",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 3
    proc: Process = nodes[0]
    address: IPAddress = nodes[2]

    assert proc.connected_to[address]
    assert address.ip_address == "111.221.29.254"


def test_network_connection_with_hostname(transformer):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "3",
        "Version": "5",
        "Level": "4",
        "Task": "3",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2015-10-08 14:14:14.747887",
        "TimeCreated": None,
        "EventRecordID": "990",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "4072",
        "Execution_ThreadID": "4620",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-OALUEJ1",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_UtcTime": 1444328053,
        "EventData_ProcessGuid": "{90e22fd2-8107-5615-0000-001090bd0100}",
        "EventData_ProcessId": "1704",
        "EventData_Image": "C:\\Windows\\System32\\svchost.exe",
        "EventData_User": "NT AUTHORITY\\SYSTEM",
        "EventData_Protocol": "tcp",
        "EventData_Initiated": "True",
        "EventData_SourceIsIpv6": "False",
        "EventData_SourceIp": "192.168.191.148",
        "EventData_SourceHostname": "DESKTOP-OALUEJ1.localdomain",
        "EventData_SourcePort": "1735",
        "EventData_SourcePortName": None,
        "EventData_DestinationIsIpv6": "False",
        "EventData_DestinationIp": "111.221.29.254",
        "EventData_DestinationHostname": "google.com",
        "EventData_DestinationPort": "443",
        "EventData_DestinationPortName": "https",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 4
    proc: Process = nodes[0]
    address: IPAddress = nodes[2]
    domain: Domain = nodes[3]

    assert address in proc.connected_to
    assert {"timestamp": 1444328053} in proc.connected_to[address]
    assert address in domain.resolves_to

    assert address.ip_address == "111.221.29.254"


def test_filecreate_event(transformer):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "11",
        "Version": "2",
        "Level": "4",
        "Task": "11",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2017-09-24 20:54:55.222649",
        "TimeCreated": None,
        "EventRecordID": "16",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "1812",
        "Execution_ThreadID": "4000",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-2C3IQHO",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_UtcTime": 1506300895,
        "EventData_ProcessGuid": "{0ad3e319-1b11-59c8-0000-0010054f3100}",
        "EventData_ProcessId": "3344",
        "EventData_Image": "C:\\Windows\\system32\\msiexec.exe",
        "EventData_TargetFilename": "C:\\Program Files\\SplunkUniversalForwarder\\bin\\splunkd.exe",
        "EventData_CreationUtcTime": "2017-09-24 20:54:55.023",
    }
    nodes = transformer.transform(event)
    assert len(nodes) == 3
    proc: Process = nodes[0]
    written: File = nodes[2]

    assert proc.accessed[written]

    assert written.file_name == "splunkd.exe"


@pytest.mark.parametrize(
    "event_type,edge_type",
    [
        ("SetValue", "changed_value"),
        ("DeleteValue", "deleted_value"),
        ("CreateKey", "created_key"),
        ("DeleteKey", "deleted_key"),
    ],
)
def test_registry(transformer, event_type, edge_type):
    event = {
        "Provider_Name": "Microsoft-Windows-Sysmon",
        "Provider_Guid": "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
        "Provider": None,
        "EventID_Qualifiers": "",
        "EventID": "13",
        "Version": "2",
        "Level": "4",
        "Task": "13",
        "Opcode": "0",
        "Keywords": "0x8000000000000000",
        "TimeCreated_SystemTime": "2017-09-24 20:54:56.862953",
        "TimeCreated": None,
        "EventRecordID": "56",
        "Correlation_ActivityID": "",
        "Correlation_RelatedActivityID": "",
        "Correlation": None,
        "Execution_ProcessID": "1812",
        "Execution_ThreadID": "4000",
        "Execution": None,
        "Channel": "Microsoft-Windows-Sysmon/Operational",
        "Computer": "DESKTOP-2C3IQHO",
        "Security_UserID": "S-1-5-18",
        "Security": None,
        "EventData_EventType": event_type,
        "EventData_UtcTime": 1506300896,
        "EventData_ProcessGuid": "{0ad3e319-0c16-59c8-0000-0010d47d0000}",
        "EventData_ProcessId": "532",
        "EventData_Image": "C:\\Windows\\system32\\services.exe",
        "EventData_TargetObject": "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\splunkdrv\\Start",
        "EventData_Details": "DWORD (0x00000003)",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 3
    proc: Process = nodes[0]
    key: RegistryKey = nodes[2]

    assert key in getattr(proc, edge_type)
    if event_type == "SetValue":
        assert {"value": "DWORD (0x00000003)", "timestamp": 1506300896} in getattr(proc, edge_type)[
            key
        ]
    else:
        assert {"timestamp": 1506300896} in getattr(proc, edge_type)[key]
    assert key.key == "Start"
