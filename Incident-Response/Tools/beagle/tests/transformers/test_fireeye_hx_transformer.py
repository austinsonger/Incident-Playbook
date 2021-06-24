import pytest

from beagle.constants import Protocols
from beagle.nodes import URI, Alert, Domain, File, IPAddress, Process, RegistryKey
from beagle.transformers.fireeye_hx_transformer import FireEyeHXTransformer


def test_process_event_start_with_parent():
    input_event = {
        "eventType": "start",
        "pid": "4024",
        "processPath": "C:\\Windows\\System32\\find.exe",
        "process": "find.exe",
        "parentPid": "6036",
        "parentProcessPath": "C:\\Windows\\System32\\cmd.exe",
        "parentProcess": "cmd.exe",
        "username": "NT AUTHORITY\\SYSTEM",
        "startTime": "2018-05-24T18:00:30.041Z",
        "md5": "84f50f355a74df0fb58b8d6edd2bc197",
        "processCmdLine": 'find  /i "Listening"   ',
        "event_type": "processEvent",
        "event_time": 1_527_199_230,
    }
    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    parent: Process = nodes[0]
    parent_file_node: File = nodes[1]
    child: Process = nodes[2]
    child_file_node: File = nodes[3]

    assert {"timestamp": 1_527_199_230} in parent.launched[child]

    assert child.process_id == 4024
    assert parent.process_id == 6036
    assert child.process_image == "find.exe"
    assert child.process_image_path == child_file_node.file_path == "C:\\Windows\\System32"
    assert parent.process_image == "cmd.exe"
    assert parent.process_image_path == parent_file_node.file_path == "C:\\Windows\\System32"

    assert child.command_line == 'find  /i "Listening"   '
    assert child.hashes["md5"] == "84f50f355a74df0fb58b8d6edd2bc197"


def test_process_event_start_without():
    input_event = {
        "eventType": "start",
        "pid": "4024",
        "processPath": "C:\\Windows\\System32\\find.exe",
        "process": "find.exe",
        "username": "NT AUTHORITY\\SYSTEM",
        "startTime": "2018-05-24T18:00:30.041Z",
        "md5": "84f50f355a74df0fb58b8d6edd2bc197",
        "processCmdLine": 'find  /i "Listening"   ',
        "event_type": "processEvent",
        "event_time": 1_527_199_230,
    }
    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    assert len(nodes) == 2

    child: Process = nodes[0]
    child_file: File = nodes[1]

    assert child.process_id == 4024
    assert child.process_image == child_file.file_name == "find.exe"
    assert child.process_image_path == child_file.file_path == "C:\\Windows\\System32"

    assert child.command_line == 'find  /i "Listening"   '
    assert child.hashes["md5"] == "84f50f355a74df0fb58b8d6edd2bc197"


def test_process_event_not_start():
    input_event = {
        "eventType": "end",
        "pid": "4024",
        "processPath": "C:\\Windows\\System32\\find.exe",
        "process": "find.exe",
        "parentPid": "6036",
        "parentProcessPath": "C:\\Windows\\System32\\cmd.exe",
        "parentProcess": "cmd.exe",
        "username": "NT AUTHORITY\\SYSTEM",
        "startTime": "2018-05-24T18:00:30.041Z",
        "md5": "84f50f355a74df0fb58b8d6edd2bc197",
        "processCmdLine": 'find  /i "Listening"   ',
        "event_type": "processEvent",
        "event_time": 1_527_199_230,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    assert None is transformer.transform(input_event)


def test_file_event():
    input_event = {
        "fullPath": "C:\\Users\\abcd.txt",
        "filePath": "Users\\",
        "drive": "C",
        "fileName": "abcd.txt",
        "fileExtension": "txt",
        "devicePath": "\\Device\\HarddiskVolume3",
        "pid": "8060",
        "process": "outlook.exe",
        "processPath": "C:\\Program Files\\Microsoft Office 15\\root\\office15",
        "writes": "290",
        "numBytesSeenWritten": "25602",
        "lowestFileOffsetSeen": "5684961",
        "dataAtLowestOffset": "VmFsdWVFcnJvcjogd3JhcHBlcigpIHJlcXVpcmVzIGEgY29kZQ==",
        "textAtLowestOffset": "ValueError: wrapper() requires a code",
        "closed": "false",
        "size": "0",
        "username": "Bob\\Schmob",
        "event_type": "fileWriteEvent",
        "event_time": 1_527_195_775,
        "md5": "not_a_real_md5",
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    file_node: File = nodes[0]

    assert file_node.__name__ == "File"
    assert file_node.full_path == "C:\\Users\\abcd.txt"
    assert file_node.extension == "txt"
    assert file_node.hashes["md5"] == "not_a_real_md5"

    proc_node = nodes[1]
    proc_file_node: File = nodes[2]

    assert proc_node.__name__ == "Process"
    assert (
        proc_node.process_image_path
        == proc_file_node.file_path
        == "C:\\Program Files\\Microsoft Office 15\\root\\office15"
    )
    assert proc_node.process_id == 8060


def test_file_event_invalid_types():
    input_event = {
        "drive": "C",
        "fileName": "abcd.txt",
        "fileExtension": "txt",
        "devicePath": "\\Device\\HarddiskVolume3",
        "pid": "8060",
        "process": "outlook.exe",
        "processPath": "C:\\Program Files\\Microsoft Office 15\\root\\office15",
        "writes": "290",
        "numBytesSeenWritten": "25602",
        "lowestFileOffsetSeen": "5684961",
        "dataAtLowestOffset": "VmFsdWVFcnJvcjogd3JhcHBlcigpIHJlcXVpcmVzIGEgY29kZQ==",
        "textAtLowestOffset": "ValueError: wrapper() requires a code",
        "closed": False,
        "size": "0",
        "username": "Bob\\Schmob",
        "event_type": "fileWriteEvent",
        "event_time": 1_527_195_775,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    assert nodes is None


def test_file_event_no_drive():
    input_event = {
        "fullPath": "C:\\Users\\abcd.txt",
        "filePath": "Users\\",
        "fileName": "abcd.txt",
        "fileExtension": "txt",
        "devicePath": "\\Device\\HarddiskVolume3",
        "pid": "8060",
        "process": "outlook.exe",
        "processPath": "C:\\Program Files\\Microsoft Office 15\\root\\office15",
        "writes": "290",
        "numBytesSeenWritten": "25602",
        "lowestFileOffsetSeen": "5684961",
        "dataAtLowestOffset": "VmFsdWVFcnJvcjogd3JhcHBlcigpIHJlcXVpcmVzIGEgY29kZQ==",
        "textAtLowestOffset": "ValueError: wrapper() requires a code",
        "closed": "false",
        "size": "0",
        "username": "Bob\\Schmob",
        "event_type": "fileWriteEvent",
        "event_time": 1_527_195_775,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    assert nodes[0].file_path == "Users\\"


def test_url_event_with_ip():
    input_event = {
        "hostname": "crl.usertrust.com",
        "requestUrl": "/foobar",
        "urlMethod": "GET",
        "userAgent": "Microsoft-CryptoAPI/6.1",
        "httpHeader": "GET /foobar",
        "remoteIpAddress": "123.456.789.1",
        "remotePort": "80",
        "localPort": "58357",
        "pid": "1220",
        "process": "svchost.exe",
        "processPath": "C:\\Windows\\System32",
        "username": "NT AUTHORITY\\NETWORK SERVICE",
        "event_type": "urlMonitorEvent",
        "event_time": 1_527_627_063,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    uri_node: URI = nodes[0]
    domain_node: Domain = nodes[1]
    proc_node: Process = nodes[2]
    file_node: File = nodes[3]
    ip_node: IPAddress = nodes[4]

    assert uri_node.__name__ == "URI"
    assert proc_node.__name__ == "Process"
    assert domain_node.__name__ == "Domain"
    assert ip_node.__name__ == "IP Address"
    assert file_node.__name__ == "File"

    assert uri_node.uri == "/foobar"
    assert domain_node.domain == "crl.usertrust.com"
    assert ip_node.ip_address == "123.456.789.1"
    assert file_node.file_name == proc_node.process_image == "svchost.exe"
    assert file_node.file_path == proc_node.process_image_path == "C:\\Windows\\System32"

    # Process - (Connected To) -> IP Address
    assert {"port": 80, "protocol": Protocols.HTTP} in proc_node.connected_to[ip_node]

    # URI - (URI Of) -> Domain
    assert {"timestamp": 1_527_627_063} in uri_node.uri_of[domain_node]

    # Domain - (Resolves To) -> IP Address
    assert {"timestamp": 1_527_627_063} in domain_node.resolves_to[ip_node]

    # Proc - (HTTP Request) -> URI
    assert {
        "method": "GET",
        "user_agent": "Microsoft-CryptoAPI/6.1",
        "header": "GET /foobar",
        "timestamp": 1_527_627_063,
    } in proc_node.http_request_to[uri_node]


def test_network_event():
    input_event = {
        "remoteIP": "123.456.789.1",
        "remotePort": "443",
        "localIP": "10.0.0.1",
        "localPort": "53978",
        "protocol": "TCP",
        "pid": "7932",
        "process": "chrome.exe",
        "processPath": "C:\\Program Files (x86)\\Google\\Chrome\\Application",
        "username": "Bob\\Schmob",
        "event_type": "ipv4NetworkEvent",
        "event_time": 1_527_119_745,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    addr_node: IPAddress = nodes[0]
    proc_node: Process = nodes[1]
    proc_file_node: File = nodes[2]

    assert proc_file_node.file_name == proc_node.process_image == "chrome.exe"
    assert (
        proc_file_node.file_path
        == proc_node.process_image_path
        == "C:\\Program Files (x86)\\Google\\Chrome\\Application"
    )
    assert proc_node.process_id == 7932

    assert addr_node.ip_address == "123.456.789.1"

    assert {"port": 443, "timestamp": 1_527_119_745, "protocol": "TCP"} in proc_node.connected_to[
        addr_node
    ]


def test_dns_lookup():
    input_event = {
        "hostname": "www.google-analytics.com",
        "pid": "1608",
        "process": "chrome.exe",
        "processPath": "C:\\HarddiskVolume3\\Program Files (x86)\\Google\\Chrome\\Application",
        "username": "Bob\\Schmob",
        "event_type": "dnsLookupEvent",
        "event_time": 1_527_286_118,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    domain_node: Domain = nodes[0]
    proc_node: Process = nodes[1]
    proc_file_node: File = nodes[2]

    assert proc_file_node.file_name == proc_node.process_image == "chrome.exe"
    assert (
        proc_file_node.file_path
        == proc_node.process_image_path
        == "C:\\HarddiskVolume3\\Program Files (x86)\\Google\\Chrome\\Application"
    )
    assert proc_node.process_id == 1608

    assert domain_node.domain == "www.google-analytics.com"

    assert {"timestamp": 1_527_286_118, "record_type": None} in proc_node.dns_query_for[domain_node]
    assert {"timestamp": 1_527_286_118} in proc_node.dns_query_for[domain_node]


def test_module_load():
    input_event = {
        "fullPath": "C:\\Windows\\System32\\kernel32.dll",
        "filePath": "Windows\\System32",
        "drive": "C",
        "fileName": "kernel32.dll",
        "fileExtension": "dll",
        "devicePath": "\\Device\\HarddiskVolume3",
        "pid": "5820",
        "process": "cmd.exe",
        "processPath": "C:\\Windows\\System32",
        "username": "NT AUTHORITY\\SYSTEM",
        "event_type": "imageLoadEvent",
        "event_time": 1_527_293_887,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    loaded_file: File = nodes[0]
    proc_node: Process = nodes[1]
    proc_file_node: File = nodes[2]

    assert proc_file_node.file_name == proc_node.process_image == "cmd.exe"
    assert proc_file_node.file_path == proc_node.process_image_path == "C:\\Windows\\System32"
    assert proc_node.process_id == 5820

    assert loaded_file.file_name == "kernel32.dll"
    assert loaded_file.extension == "dll"
    assert loaded_file.file_path == "C:\\Windows\\System32"

    assert {"timestamp": 1_527_293_887} in proc_node.loaded[loaded_file]


def test_no_process_path():
    input_event = {
        "fullPath": "C:\\Windows\\System32\\cryptbase.dll",
        "filePath": "Windows\\System32",
        "drive": "C",
        "fileName": "cryptbase.dll",
        "fileExtension": "dll",
        "devicePath": "\\Device\\HarddiskVolume3",
        "pid": "1368",
        "process": "cmd.exe",
        "processPath": None,
        "username": "NT AUTHORITY\\SYSTEM",
        "event_type": "imageLoadEvent",
        "event_time": 1_530_167_081,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    assert nodes is None


def test_process_equal_processpath():
    input_event = {
        "eventType": "running",
        "pid": "1056",
        "processPath": "audiodg.exe",
        "process": "audiodg.exe",
        "parentPid": "800",
        "parentProcessPath": "\\Device\\HarddiskVolume3\\Windows\\System32\\svchost.exe",
        "parentProcess": "svchost.exe",
        "event_type": "processEvent",
        "event_time": 1_530_167_081,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    assert nodes is None


@pytest.mark.parametrize(
    "eventtype,attribute",
    [("1", "changed_value"), ("2", "deleted_value"), ("3", "created_key"), ("4", "deleted_key")],
)
def test_registry_event(eventtype, attribute):
    input_event = {
        "hive": "HKEY_USERS\\S-1",
        "keyPath": "Software\\Microsoft\\Internet Explorer\\Toolbar",
        "path": "HKEY_USERS\\S-1\\Software\\Microsoft\\Internet Explorer\\Toolbar\\Locked",
        "eventType": eventtype,
        "pid": "3592",
        "process": "explorer.exe",
        "processPath": "C:\\Windows",
        "valueName": "Locked",
        "valueType": "REG_DWORD",
        "value": "AAAAAA==",
        "text": "....",
        "username": "Bob\\Schmob",
        "event_type": "regKeyEvent",
        "event_time": 1_526_942_280,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    reg_node: RegistryKey = nodes[0]
    proc_node: Process = nodes[1]

    assert reg_node.hive == "HKEY_USERS\\S-1"
    assert reg_node.key == "Locked"
    assert reg_node.key_path == "Software\\Microsoft\\Internet Explorer\\Toolbar"
    assert reg_node.value == "...."
    assert reg_node.value_type == "REG_DWORD"

    assert proc_node.process_id == 3592

    assert {"timestamp": 1_526_942_280} in getattr(proc_node, attribute)[reg_node]


def test_alert_creation():

    input_event = {
        "_id": 1234,
        "event_type": "alertEvent",
        "agent_id": "1234",
        "condition_id": "1234==",
        "threat_id": "threat_id_uid",
        "marker": "2",
        "match_hash": "1",
        "event_at": "2018-06-28T07:54:40.741Z",
        "matched_at": "2018-06-28T07:54:55.000Z",
        "reported_at": "2018-06-28T07:55:05.800Z",
        "deleted": False,
        "source": "IOC",
        "resolution": "ALERT",
        "data": {
            "values": {
                "fullPath": "C:\\Users\\abcd.txt",
                "filePath": "Users\\",
                "drive": "C",
                "fileName": "abcd.txt",
                "fileExtension": "txt",
                "devicePath": "\\Device\\HarddiskVolume3",
                "pid": "8060",
                "process": "outlook.exe",
                "processPath": "C:\\Program Files\\Microsoft Office 15\\root\\office15",
                "writes": "290",
                "numBytesSeenWritten": "25602",
                "lowestFileOffsetSeen": "5684961",
                "dataAtLowestOffset": "VmFsdWVFcnJvcjogd3JhcHBlcigpIHJlcXVpcmVzIGEgY29kZQ==",
                "textAtLowestOffset": "ValueError: wrapper() requires a code",
                "closed": "false",
                "size": "0",
                "username": "Bob\\Schmob",
                "event_type": "fileWriteEvent",
                "event_time": 1_527_195_775,
                "md5": "not_a_real_md5",
            },
            "key": {
                "event_id": 1234,
                "indicator_id": "1234",
                "match_timestamp": "2018-06-28T07:54:55Z",
                "event_type": "fileWriteEvent",
                "condition_id": "1234",
            },
        },
        "_threat_data": {
            "_id": "threat_id_uid",
            "uri_name": None,
            "display_name": "Some.Alert.Name",
            "sub_type": None,
            "signature": "malware-object",
            "intel_version": None,
            "meta": None,
            "active_since": "2016-01-01T13:18:24.266Z",
            "update_time": "2016-01-01T20:30:23.957Z",
            "create_text": "1234",
            "create_actor_id": 1,
            "pending_changes": 0,
            "_revision": "1234",
            "input_type": "local",
            "category_id": 5,
            "update_actor_id": 1,
            "description": None,
            "supports_win": True,
            "supports_osx": False,
            "tags": None,
            "supports_linux": False,
            "category": "FireEye-CMS",
            "create_actor": "fireeye",
            "update_actor": "fireeye",
            "origin": "1234",
        },
        "event_time": 1_527_195_775,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    alert: Alert = nodes[0]

    assert alert.alert_name == "Some.Alert.Name"

    try:
        assert alert.alert_data == input_event
    except AssertionError:
        assert alert.alert_data == "No data"

    # Since this is a file event. We should have 3 additional nodes.

    assert len(nodes) == 4  # alert + 3 nodes

    file_node: File = nodes[1]

    assert file_node.__name__ == "File"
    assert file_node.full_path == "C:\\Users\\abcd.txt"
    assert file_node.extension == "txt"
    assert file_node.hashes["md5"] == "not_a_real_md5"

    proc_node = nodes[2]
    proc_file_node: File = nodes[3]

    assert proc_node.__name__ == "Process"
    assert (
        proc_node.process_image_path
        == proc_file_node.file_path
        == "C:\\Program Files\\Microsoft Office 15\\root\\office15"
    )
    assert proc_node.process_id == 8060

    for node in [file_node, proc_node, proc_file_node]:
        assert {"timestamp": 1_527_195_775} in alert.alerted_on[node]


def test_alert_creation_uri_only():

    input_event = {
        "_id": 1234,
        "event_type": "alertEvent",
        "agent_id": "1234",
        "condition_id": "1234==",
        "threat_id": "threat_id_uid",
        "marker": "2",
        "match_hash": "1",
        "event_at": "2018-06-28T07:54:40.741Z",
        "matched_at": "2018-06-28T07:54:55.000Z",
        "reported_at": "2018-06-28T07:55:05.800Z",
        "deleted": False,
        "source": "IOC",
        "resolution": "ALERT",
        "data": {
            "values": {
                "fullPath": "C:\\Users\\abcd.txt",
                "filePath": "Users\\",
                "drive": "C",
                "fileName": "abcd.txt",
                "fileExtension": "txt",
                "devicePath": "\\Device\\HarddiskVolume3",
                "pid": "8060",
                "process": "outlook.exe",
                "processPath": "C:\\Program Files\\Microsoft Office 15\\root\\office15",
                "writes": "290",
                "numBytesSeenWritten": "25602",
                "lowestFileOffsetSeen": "5684961",
                "dataAtLowestOffset": "VmFsdWVFcnJvcjogd3JhcHBlcigpIHJlcXVpcmVzIGEgY29kZQ==",
                "textAtLowestOffset": "ValueError: wrapper() requires a code",
                "closed": "false",
                "size": "0",
                "username": "Bob\\Schmob",
                "event_type": "fileWriteEvent",
                "event_time": 1_527_195_775,
                "md5": "not_a_real_md5",
            },
            "key": {
                "event_id": 1234,
                "indicator_id": "1234",
                "match_timestamp": "2018-06-28T07:54:55Z",
                "event_type": "fileWriteEvent",
                "condition_id": "1234",
            },
        },
        "_threat_data": {
            "_id": "threat_id_uid",
            "uri_name": "Some.Alert.Name",
            "display_name": None,
            "sub_type": None,
            "signature": "malware-object",
            "intel_version": None,
            "meta": None,
            "active_since": "2016-01-01T13:18:24.266Z",
            "update_time": "2016-01-01T20:30:23.957Z",
            "create_text": "1234",
            "create_actor_id": 1,
            "pending_changes": 0,
            "_revision": "1234",
            "input_type": "local",
            "category_id": 5,
            "update_actor_id": 1,
            "description": None,
            "supports_win": True,
            "supports_osx": False,
            "tags": None,
            "supports_linux": False,
            "category": "FireEye-CMS",
            "create_actor": "fireeye",
            "update_actor": "fireeye",
            "origin": "1234",
        },
        "event_time": 1_527_195_775,
    }

    transformer = FireEyeHXTransformer(datasource=None)
    nodes = transformer.transform(input_event)

    alert: Alert = nodes[0]

    assert alert.alert_name == "Some.Alert.Name"

    try:
        assert alert.alert_data == input_event
    except AssertionError:
        assert alert.alert_data == "No data"

    # Since this is a file event. We should have 3 additional nodes.

    assert len(nodes) == 4  # alert + 3 nodes

    file_node: File = nodes[1]

    assert file_node.__name__ == "File"
    assert file_node.full_path == "C:\\Users\\abcd.txt"
    assert file_node.extension == "txt"
    assert file_node.hashes["md5"] == "not_a_real_md5"

    proc_node = nodes[2]
    proc_file_node: File = nodes[3]

    assert proc_node.__name__ == "Process"
    assert (
        proc_node.process_image_path
        == proc_file_node.file_path
        == "C:\\Program Files\\Microsoft Office 15\\root\\office15"
    )
    assert proc_node.process_id == 8060

    for node in [file_node, proc_node, proc_file_node]:
        assert {"timestamp": 1_527_195_775} in alert.alerted_on[node]
