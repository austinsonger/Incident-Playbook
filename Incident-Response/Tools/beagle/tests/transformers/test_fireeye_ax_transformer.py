import pytest

from beagle.constants import HashAlgos
from beagle.nodes import URI, Domain, File, IPAddress, Process
from beagle.nodes.registry import RegistryKey
from beagle.transformers.fireeye_ax_transformer import FireEyeAXTransformer


@pytest.fixture
def transformer() -> FireEyeAXTransformer:
    return FireEyeAXTransformer(datasource=None)  # type: ignore


def test_init(transformer):
    assert transformer is not None


def test_not_started(transformer):
    assert transformer.process_events({"mode": "not_started"}) is None


def test_process(transformer):
    input_event = {
        "mode": "started",
        "fid": {"ads": "", "content": 1234},
        "parentname": "C:\\Windows\\explorer.exe",
        "cmdline": '"C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe"',
        "sha1sum": "123",
        "md5sum": "345",
        "sha256sum": "678",
        "pid": 1700,
        "filesize": 1,
        "event_type": "process",
        "value": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
        "timestamp": 18552,
        "ppid": 4668,
    }
    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    parent: Process = nodes[2]
    parent_proc_file: File = nodes[3]

    assert proc in parent.launched
    assert {"timestamp": 18552} in parent.launched[proc]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )

    assert parent.process_image == "explorer.exe"
    assert parent in parent_proc_file.file_of

    assert proc in proc_file.file_of
    assert proc.process_id == 1700
    assert parent.process_id == 4668

    assert proc.hashes[HashAlgos.SHA1] == "123"
    assert proc.hashes[HashAlgos.MD5] == "345"
    assert proc.hashes[HashAlgos.SHA256] == "678"


def test_dns_event_noanswer(transformer):
    input_event = {
        "mode": "dns_query",
        "protocol_type": "udp",
        "hostname": "foobar",
        "event_type": "network",
        "qtype": "Host Address",
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    domain: Domain = nodes[2]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert {"timestamp": 27648} in proc.dns_query_for[domain]


def test_dns_event_answer(transformer):
    input_event = {
        "mode": "dns_query_answer",
        "protocol_type": "udp",
        "hostname": "foobar",
        "ipaddress": "127.0.0.1",
        "event_type": "network",
        "qtype": "Host Address",
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    domain: Domain = nodes[2]
    ip_addr: IPAddress = nodes[3]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert {"timestamp": 27648} in proc.dns_query_for[domain]
    assert {"timestamp": 27648} in domain.resolves_to[ip_addr]
    assert ip_addr.ip_address == "127.0.0.1"


def test_conn_event(transformer):
    input_event = {
        "mode": "connect",
        "event_type": "network",
        "protocol_type": "tcp",
        "ipaddress": "199.168.199.123",
        "destination_port": 3333,
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    ip_addr: IPAddress = nodes[2]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert ip_addr.ip_address == "199.168.199.123"
    assert {"timestamp": 27648, "port": 3333, "protocol": "tcp"} in proc.connected_to[ip_addr]


def test_http_request(transformer):
    input_event = {
        "mode": "http_request",
        "protocol_type": "tcp",
        "event_type": "network",
        "ipaddress": "199.168.199.123",
        "destination_port": 3333,
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
        "http_request": "GET /some_route.crl HTTP/1.1~~Cache-Control: max-age = 900~~User-Agent: Microsoft-CryptoAPI/10.0~~Host: crl.microsoft.com~~~~",
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 5

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    ip_addr: IPAddress = nodes[2]
    uri: URI = nodes[3]
    domain: Domain = nodes[4]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert ip_addr.ip_address == "199.168.199.123"
    assert {"timestamp": 27648, "port": 3333, "protocol": "tcp"} in proc.connected_to[ip_addr]

    assert uri.uri == "/some_route.crl"
    assert {"method": "GET", "timestamp": 27648} in proc.http_request_to[uri]
    assert domain in uri.uri_of


def test_http_request_no_headers(transformer):
    input_event = {
        "mode": "http_request",
        "protocol_type": "tcp",
        "event_type": "network",
        "ipaddress": "199.168.199.123",
        "destination_port": 3333,
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    ip_addr: IPAddress = nodes[2]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert ip_addr.ip_address == "199.168.199.123"
    assert {"timestamp": 27648, "port": 3333, "protocol": "tcp"} in proc.connected_to[ip_addr]


def test_http_request_no_hostin_headers(transformer):
    input_event = {
        "mode": "http_request",
        "protocol_type": "tcp",
        "event_type": "network",
        "ipaddress": "199.168.199.123",
        "destination_port": 3333,
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "timestamp": 27648,
        "http_request": "GET /some_route.crl HTTP/1.1~~Cache-Control: max-age = 900~~User-Agent: Microsoft-CryptoAPI/10.0",
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    ip_addr: IPAddress = nodes[2]
    uri: URI = nodes[3]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert ip_addr.ip_address == "199.168.199.123"
    assert {"timestamp": 27648, "port": 3333, "protocol": "tcp"} in proc.connected_to[ip_addr]

    assert uri.uri == "/some_route.crl"
    assert {"method": "GET", "timestamp": 27648} in proc.http_request_to[uri]


@pytest.mark.parametrize(
    "mode,edge", [("created", "wrote"), ("deleted", "deleted"), ("accessed", "accessed")]
)
def test_file_events(transformer, mode, edge):
    input_event = {
        "mode": mode,
        "event_type": "file",
        "fid": {"ads": "", "content": 2533274790555891},
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "ntstatus": "0x0",
        "value": "C:\\Users\\admin\\AppData\\Local\\Temp\\sy24ttkc.k25.ps1",
        "CreateOptions": "0x400064",
        "timestamp": 9494,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    file_node: File = nodes[2]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert file_node.file_name == "sy24ttkc.k25.ps1"
    assert file_node.extension == "ps1"

    assert {"timestamp": 9494} in getattr(proc, edge)[file_node]


def test_file_copy_events(transformer):
    input_event = {
        "mode": "CopyFile",
        "event_type": "file",
        "fid": {"ads": "", "content": 2533274790555891},
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "ntstatus": "0x0",
        "value": "C:\\Users\\admin\\AppData\\Local\\Temp\\sy24ttkc.k25.ps1",
        "source": "C:\\Users\\admin\\AppData\\Local\\Temp\\123456.ps1",
        "CreateOptions": "0x400064",
        "timestamp": 9494,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    file_node: File = nodes[2]
    src_node: File = nodes[3]
    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert file_node.file_name == "sy24ttkc.k25.ps1"
    assert file_node.extension == "ps1"

    assert src_node.file_name == "123456.ps1"
    assert src_node.extension == "ps1"
    assert {"timestamp": 9494} in proc.copied[src_node]
    assert {"timestamp": 9494} in src_node.copied_to[file_node]


def test_reg_key_no_value(transformer):
    input_event = {
        "mode": "queryvalue",
        "event_type": "regkey",
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "value": '\\REGISTRY\\USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings\\"ProxyOverride"',
        "timestamp": 6203,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    proc_file: File = nodes[1]
    regkey: RegistryKey = nodes[2]

    assert proc.process_image == proc_file.file_name == "bar.exe"
    assert (
        proc.process_image_path == proc_file.file_path == "C:\\Users\\admin\\AppData\\Local\\Temp"
    )
    assert proc in proc_file.file_of

    assert regkey.key == "ProxyOverride"
    assert regkey.hive == "USER"
    assert regkey.key_path == "Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings"
    assert regkey.value == None
    assert regkey in proc.read_key


def test_reg_key_value(transformer):
    input_event = {
        "mode": "queryvalue",
        "event_type": "regkey",
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "value": '\\REGISTRY\\USER\\Software\\Microsoft\\Internet Explorer\\Main\\"FullScreen" = no"',
        "timestamp": 6203,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    regkey: RegistryKey = nodes[2]

    assert regkey.key == "FullScreen"
    assert regkey.hive == "USER"
    assert regkey.key_path == "Software\\Microsoft\\Internet Explorer\\Main"
    assert regkey.value == "no"
    assert {"timestamp": 6203, "value": "no"} in proc.read_key[regkey]


@pytest.mark.parametrize(
    "mode,edge",
    [
        ("added", "created_key"),
        ("setval", "changed_value"),
        ("deleteval", "deleted_key"),
        ("deleted", "deleted_key"),
        ("queryvalue", "read_key"),
    ],
)
def test_reg_key_edge_types(transformer, mode, edge):
    input_event = {
        "mode": mode,
        "event_type": "regkey",
        "processinfo": {
            "imagepath": "C:\\Users\\admin\\AppData\\Local\\Temp\\bar.exe",
            "tainted": True,
            "md5sum": "....",
            "pid": 1700,
        },
        "value": '\\REGISTRY\\USER\\Software\\Microsoft\\Internet Explorer\\Main\\"FullScreen" = no"',
        "timestamp": 6203,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 3

    proc: Process = nodes[0]
    regkey: RegistryKey = nodes[2]

    assert regkey.key == "FullScreen"
    assert regkey.hive == "USER"
    assert regkey.key_path == "Software\\Microsoft\\Internet Explorer\\Main"
    assert regkey.value == "no"

    assert {"timestamp": 6203, "value": "no"} in getattr(proc, edge)[regkey]

