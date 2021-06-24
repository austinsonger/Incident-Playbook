import pytest

from beagle.constants import EventTypes, FieldNames, Protocols
from beagle.nodes import URI, Domain, File, IPAddress, Process, RegistryKey, Alert
from beagle.transformers import GenericTransformer


@pytest.fixture
def transformer() -> GenericTransformer:
    return GenericTransformer(datasource=None)


def test_init():
    GenericTransformer(datasource=None)


def test_make_process(transformer):
    input_event = {
        FieldNames.PARENT_PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
        FieldNames.PARENT_PROCESS_ID: "3420",
        FieldNames.PARENT_COMMAND_LINE: "",
        FieldNames.PROCESS_IMAGE: "cmd.exe",
        FieldNames.PROCESS_IMAGE_PATH: "<SYSTEM32>",
        FieldNames.COMMAND_LINE: "",
        FieldNames.PROCESS_ID: "3712",
        FieldNames.TIMESTAMP: 5,
        FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    parent: Process = nodes[0]
    parent_file: File = nodes[1]

    child: Process = nodes[2]
    child_file: File = nodes[3]

    assert parent in parent_file.file_of

    assert child in child_file.file_of

    assert parent.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert parent.process_image_path == "\\"
    assert parent.command_line == ""

    assert parent.process_path == "\\<PATH_SAMPLE.EXE>"

    assert child.process_image == "cmd.exe"
    assert child.process_image_path == "<SYSTEM32>"
    assert child.command_line == ""

    assert {"timestamp": 5} in parent.launched[child]


def test_make_process_no_timestamp(transformer):
    input_event = {
        FieldNames.PARENT_PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
        FieldNames.PARENT_PROCESS_ID: "3420",
        FieldNames.PARENT_COMMAND_LINE: "",
        FieldNames.PROCESS_IMAGE: "cmd.exe",
        FieldNames.PROCESS_IMAGE_PATH: "<SYSTEM32>",
        FieldNames.COMMAND_LINE: "",
        FieldNames.PROCESS_ID: "3712",
        FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 4

    parent: Process = nodes[0]

    child: Process = nodes[2]

    assert {"timestamp": 5} not in parent.launched[child]
    assert len(parent.launched[child]) == 0


@pytest.mark.parametrize(
    "event_type, attribute",
    [
        (EventTypes.FILE_OPENED, "accessed"),
        (EventTypes.FILE_WRITTEN, "wrote"),
        (EventTypes.FILE_DELETED, "deleted"),
        (EventTypes.LOADED_MODULE, "loaded"),
    ],
)
def test_make_file(transformer, event_type: str, attribute: str):

    input_event = {
        FieldNames.FILE_NAME: "svhost.exe",
        FieldNames.FILE_PATH: "%TEMP%",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "3852",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: event_type,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3
    parent: Process = nodes[0]
    parent_file: File = nodes[1]
    file_node: File = nodes[2]

    assert parent in parent_file.file_of

    assert parent.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert parent.process_image_path == "\\"
    assert parent.command_line == ""

    assert parent.process_path == "\\<PATH_SAMPLE.EXE>"

    assert file_node.file_name == "svhost.exe"
    assert file_node.full_path == "%TEMP%\\svhost.exe"
    assert file_node.file_path == "%TEMP%"

    assert file_node in getattr(parent, attribute)


def test_file_copy(transformer):

    input_event = {
        FieldNames.SRC_FILE: {
            FieldNames.FILE_NAME: "msbuild.exe ",
            FieldNames.FILE_PATH: "C:\\WINDOWS\\Microsoft.NET\\Framework\\v3.5",
        },
        FieldNames.DEST_FILE: {
            FieldNames.FILE_NAME: "svhost.exe ",
            FieldNames.FILE_PATH: "C:\\Documents and Settings\\Administrator\\Local Settings\\Temp",
        },
        FieldNames.PROCESS_IMAGE: "****.exe",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "716",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.FILE_COPIED,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 4

    process: Process = nodes[0]
    process_file: File = nodes[1]
    src_file_node: File = nodes[2]
    dst_file_node: File = nodes[3]

    assert src_file_node in process.copied
    assert dst_file_node in src_file_node.copied_to

    assert process in process_file.file_of


def test_connection(transformer):
    input_event = {
        FieldNames.IP_ADDRESS: "24.151.31.150",
        FieldNames.PROTOCOL: Protocols.TCP,
        FieldNames.PORT: 465,
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3

    process: Process = nodes[0]
    process_file: File = nodes[1]
    address: IPAddress = nodes[2]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    assert process.process_image_path == "\\"

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert process in process_file.file_of

    assert address in process.connected_to
    assert {"port": 465} in process.connected_to[address]


def test_make_http(transformer):
    input_event = {
        FieldNames.HTTP_HOST: "107.10.49.252",
        FieldNames.URI: "/",
        FieldNames.HTTP_METHOD: "GET",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
    }
    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 4

    process: Process = nodes[0]
    process_file: File = nodes[1]
    uri: URI = nodes[2]
    domain: Domain = nodes[3]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert process.process_image_path == "\\"

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert domain in uri.uri_of
    assert uri in process.http_request_to
    assert {"method": "GET"} in process.http_request_to[uri]


def test_make_http_with_ip_address(transformer):
    input_event = {
        FieldNames.HTTP_HOST: "google.com",
        FieldNames.IP_ADDRESS: "127.0.0.1",
        FieldNames.URI: "/",
        FieldNames.HTTP_METHOD: "GET",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
    }
    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 5

    process: Process = nodes[0]
    uri: URI = nodes[2]
    domain: Domain = nodes[3]
    ip_address: IPAddress = nodes[4]

    assert {"method": "GET"} in process.http_request_to[uri]
    assert ip_address in domain.resolves_to
    assert ip_address in process.connected_to


def test_dnslookup(transformer):

    input_event = {
        FieldNames.HTTP_HOST: "www.google-analytics.com",
        FieldNames.IP_ADDRESS: "172.217.168.238",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 4

    process: Process = nodes[0]
    process_file: File = nodes[1]
    dom: Domain = nodes[2]
    addr: IPAddress = nodes[3]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert process.process_image_path == "\\"

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert addr in dom.resolves_to
    assert dom in process.dns_query_for

    assert dom.domain == "www.google-analytics.com"
    assert addr.ip_address == "172.217.168.238"


def test_dns_lookup_no_addr(transformer):
    input_event = {
        FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
        FieldNames.HTTP_HOST: "a.applovin.com",
        FieldNames.PROCESS_IMAGE: "zygote",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.COMMAND_LINE: "",
        FieldNames.PROCESS_ID: "8145",
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3


@pytest.mark.parametrize(
    "event_type, attribute",
    [(EventTypes.REG_KEY_OPENED, "read_key"), (EventTypes.REG_KEY_DELETED, "deleted_key")],
)
def test_make_reg_basic(transformer, event_type: str, attribute: str):

    input_event = {
        FieldNames.HIVE: "<HKLM>",
        FieldNames.REG_KEY_PATH: "System\\CurrentControlSet\\Control",
        FieldNames.REG_KEY: "Session Manager",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: event_type,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3
    process: Process = nodes[0]
    process_file: File = nodes[1]
    regkey: RegistryKey = nodes[2]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert process.process_image_path == "\\"
    assert process.process_id == 1748

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert regkey.hive == "<HKLM>"
    assert regkey.key_path == "System\\CurrentControlSet\\Control"
    assert regkey.key == "Session Manager"

    assert regkey in getattr(process, attribute)


def test_make_reg_set(transformer):

    input_event = {
        FieldNames.HIVE: "<HKLM>",
        FieldNames.REG_KEY_PATH: "System\\CurrentControlSet\\Services\\wordpadmouse",
        FieldNames.REG_KEY: "Type",
        FieldNames.REG_KEY_VALUE: "0x00000010",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.REG_KEY_SET,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3
    process: Process = nodes[0]
    process_file: File = nodes[1]
    regkey: RegistryKey = nodes[2]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    assert process.process_id == 1748
    # NOTE: Expected to be false
    assert process.process_image_path == "\\"

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert regkey.hive == "<HKLM>"
    assert regkey.key_path == "System\\CurrentControlSet\\Services\\wordpadmouse"
    assert regkey.key == "Type"
    assert regkey.value == "0x00000010"

    assert regkey in process.changed_value
    assert {"value": "0x00000010"} in process.changed_value[regkey]


def test_make_reg_set_no_value(transformer):

    input_event = {
        FieldNames.HIVE: "<HKLM>",
        FieldNames.REG_KEY_PATH: "System\\CurrentControlSet\\Services\\wordpadmouse",
        FieldNames.REG_KEY: "Type",
        FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PROCESS_IMAGE_PATH: "\\",
        FieldNames.PROCESS_ID: "1748",
        FieldNames.COMMAND_LINE: "",
        FieldNames.EVENT_TYPE: EventTypes.REG_KEY_SET,
    }

    nodes = transformer.transform(input_event)

    assert nodes is not None

    assert len(nodes) == 3
    process: Process = nodes[0]
    process_file: File = nodes[1]
    regkey: RegistryKey = nodes[2]

    assert process.process_image == "<PATH_SAMPLE.EXE>"
    assert process.process_id == 1748
    # NOTE: Expected to be false
    assert process.process_image_path == "\\"

    assert process.process_path == "\\<PATH_SAMPLE.EXE>"

    assert process_file.file_path == "\\"
    assert process_file.file_name == "<PATH_SAMPLE.EXE>"

    assert regkey.hive == "<HKLM>"
    assert regkey.key_path == "System\\CurrentControlSet\\Services\\wordpadmouse"
    assert regkey.key == "Type"

    assert regkey in process.changed_value


def test_make_alert(transformer):
    input_event = {
        FieldNames.PARENT_PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
        FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
        FieldNames.PARENT_PROCESS_ID: "3420",
        FieldNames.PARENT_COMMAND_LINE: "",
        FieldNames.PROCESS_IMAGE: "cmd.exe",
        FieldNames.PROCESS_IMAGE_PATH: "<SYSTEM32>",
        FieldNames.COMMAND_LINE: "",
        FieldNames.PROCESS_ID: "3712",
        FieldNames.TIMESTAMP: 5,
        FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
        FieldNames.ALERTED_ON: True,
        FieldNames.ALERT_NAME: "Malicious CMD Line",
        FieldNames.ALERT_DATA: "Bad CMD line detected",
    }

    nodes = transformer.transform(input_event)

    assert len(nodes) == 5

    alert: Alert = nodes[0]
    parent: Process = nodes[1]
    parent_file: File = nodes[2]

    child: Process = nodes[3]
    child_file: File = nodes[4]

    for node in [parent, parent_file, child, child_file]:
        assert node in alert.alerted_on

    assert parent in parent_file.file_of

    assert child in child_file.file_of

    assert parent.process_image == "<PATH_SAMPLE.EXE>"
    # NOTE: Expected to be false
    assert parent.process_image_path == "\\"
    assert parent.command_line == ""

    assert parent.process_path == "\\<PATH_SAMPLE.EXE>"

    assert child.process_image == "cmd.exe"
    assert child.process_image_path == "<SYSTEM32>"
    assert child.command_line == ""

    assert {"timestamp": 5} in parent.launched[child]
