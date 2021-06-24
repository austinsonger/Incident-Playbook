import pytest

from beagle.transformers import DRAPATCTransformer
from beagle.transformers.darpa_tc_transformer import TCFile, TCIPAddress, TCProcess, TCRegistryKey


@pytest.fixture
def transformer() -> DRAPATCTransformer:
    return DRAPATCTransformer(datasource=None)  # type: ignore


def test_unknown_event(transformer):
    assert transformer.transform({"event_type": "foooo"}) == ()


def test_make_process(transformer):
    test_event = {
        "event_type": "subject",
        "uuid": "B80F3806-0000-0000-0000-000000000020",
        "type": "SUBJECT_PROCESS",
        "cid": 4024,
        "parentSubject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "52071700-0000-0000-0000-000000000020"
        },
        "hostId": "0A00063C-5254-00F0-0D60-000000000070",
        "localPrincipal": "EC000000-0000-0000-0000-000000000060",
        "startTimestampNanos": 1522943310819901200,
        "unitId": None,
        "iteration": None,
        "count": None,
        "cmdLine": {"string": "/usr/bin/firefox"},
        "privilegeLevel": None,
        "importedLibraries": None,
        "exportedLibraries": None,
        "properties": {
            "map": {"tgid": "3934", "path": "/home/admin/Downloads/firefox/firefox", "ppid": "1874"}
        },
    }

    nodes = transformer.transform(test_event)

    proc: TCProcess = nodes[0]
    parent: TCProcess = nodes[1]
    assert proc.uuid == "B80F3806-0000-0000-0000-000000000020"
    assert proc.command_line == "/usr/bin/firefox"
    assert proc.process_image == "firefox"
    assert parent.uuid == "52071700-0000-0000-0000-000000000020"


def test_make_process_no_cmdline(transformer):
    test_event = {
        "event_type": "subject",
        "uuid": "B80F3806-0000-0000-0000-000000000020",
        "type": "SUBJECT_PROCESS",
        "cid": 4024,
        "parentSubject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "52071700-0000-0000-0000-000000000020"
        },
        "hostId": "0A00063C-5254-00F0-0D60-000000000070",
        "localPrincipal": "EC000000-0000-0000-0000-000000000060",
        "startTimestampNanos": 1522943310819901200,
        "unitId": None,
        "iteration": None,
        "count": None,
        "cmdLine": None,
        "privilegeLevel": None,
        "importedLibraries": None,
        "exportedLibraries": None,
        "properties": {
            "map": {"tgid": "3934", "path": "/home/admin/Downloads/firefox/firefox", "ppid": "1874"}
        },
    }

    nodes = transformer.transform(test_event)

    proc: TCProcess = nodes[0]
    parent: TCProcess = nodes[1]
    assert proc.uuid == "B80F3806-0000-0000-0000-000000000020"
    assert proc.command_line == None
    assert proc.process_image == "firefox"
    assert parent.uuid == "52071700-0000-0000-0000-000000000020"


def test_make_process_no_properties(transformer):
    test_event = {
        "event_type": "subject",
        "uuid": "B80F3806-0000-0000-0000-000000000020",
        "type": "SUBJECT_PROCESS",
        "cid": 4024,
        "parentSubject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "52071700-0000-0000-0000-000000000020"
        },
        "hostId": "0A00063C-5254-00F0-0D60-000000000070",
        "localPrincipal": "EC000000-0000-0000-0000-000000000060",
        "startTimestampNanos": 1522943310819901200,
        "unitId": None,
        "iteration": None,
        "count": None,
        "cmdLine": {"string": "/usr/bin/firefox"},
        "privilegeLevel": None,
        "importedLibraries": None,
        "exportedLibraries": None,
        "properties": None,
    }

    nodes = transformer.transform(test_event)

    proc: TCProcess = nodes[0]
    parent: TCProcess = nodes[1]
    assert proc.uuid == "B80F3806-0000-0000-0000-000000000020"
    assert proc.command_line == "/usr/bin/firefox"
    assert proc.process_image == "/usr/bin/firefox"
    assert parent.uuid == "52071700-0000-0000-0000-000000000020"


def test_make_process_no_parent(transformer):
    test_event = {
        "event_type": "subject",
        "uuid": "B80F3806-0000-0000-0000-000000000020",
        "type": "SUBJECT_PROCESS",
        "cid": 4024,
        "parentSubject": None,
        "hostId": "0A00063C-5254-00F0-0D60-000000000070",
        "localPrincipal": "EC000000-0000-0000-0000-000000000060",
        "startTimestampNanos": 1522943310819901200,
        "unitId": None,
        "iteration": None,
        "count": None,
        "cmdLine": {"string": "/usr/bin/firefox"},
        "privilegeLevel": None,
        "importedLibraries": None,
        "exportedLibraries": None,
        "properties": None,
    }

    nodes = transformer.transform(test_event)
    assert len(nodes) == 1


def test_make_file(transformer):
    test_event = {
        "uuid": "0100D00F-1400-2E00-0000-00004FA79C38",
        "event_type": "fileobject",
        "baseObject": {
            "hostId": "0A00063C-5254-00F0-0D60-000000000070",
            "permission": None,
            "epoch": None,
            "properties": {
                "map": {
                    "dev": "265289729",
                    "inode": "3014676",
                    "filename": "/home/admin/.cache/mozilla/firefox/pe11scpa.default/thumbnails/31017840be38acf6baf0e8f850d5c94b.png",
                }
            },
        },
        "type": "FILE_OBJECT_BLOCK",
        "fileDescriptor": None,
        "localPrincipal": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "EC000000-0000-0000-0000-000000000060"
        },
        "size": None,
        "peInfo": None,
        "hashes": None,
    }
    nodes = transformer.transform(test_event)
    assert len(nodes) == 1

    fnode: TCFile = nodes[0]
    assert fnode.uuid == "0100D00F-1400-2E00-0000-00004FA79C38"
    assert fnode.host == "0A00063C-5254-00F0-0D60-000000000070"
    assert (
        fnode.full_path
        == "\\home\\admin\\.cache\\mozilla\\firefox\\pe11scpa.default\\thumbnails\\31017840be38acf6baf0e8f850d5c94b.png"
    )
    assert fnode.file_name == "31017840be38acf6baf0e8f850d5c94b.png"
    assert (
        fnode.file_path == "\\home\\admin\\.cache\\mozilla\\firefox\\pe11scpa.default\\thumbnails"
    )


def test_make_file_no_properties(transformer):
    test_event = {
        "uuid": "0100D00F-1400-2E00-0000-00004FA79C38",
        "event_type": "fileobject",
        "baseObject": {
            "hostId": "0A00063C-5254-00F0-0D60-000000000070",
            "permission": None,
            "epoch": None,
            "properties": None,
        },
        "type": "FILE_OBJECT_BLOCK",
        "fileDescriptor": None,
        "localPrincipal": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "EC000000-0000-0000-0000-000000000060"
        },
        "size": None,
        "peInfo": None,
        "hashes": None,
    }
    nodes = transformer.transform(test_event)
    assert len(nodes) == 1

    fnode: TCFile = nodes[0]
    assert fnode.uuid == "0100D00F-1400-2E00-0000-00004FA79C38"
    assert fnode.host == "0A00063C-5254-00F0-0D60-000000000070"
    assert fnode.full_path == ""
    assert fnode.file_name is None
    assert fnode.file_path is None


def test_make_registry(transformer):
    test_event = {
        "event_type": "registrykeyobject",
        "uuid": "736F96AB-F043-4ED4-A456-D6F6DC3365FC",
        "baseObject": {
            "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
            "permission": None,
            "epoch": None,
            "properties": None,
        },
        "key": "\\REGISTRY\\USER\\S-1-5-21-231540947-922634896-4161786520-1001\\Software\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager\\Subscriptions\\280810",
        "value": {
            "com.bbn.tc.schema.avro.cdm18.Value": {
                "size": -1,
                "type": "VALUE_TYPE_SRC",
                "valueDataType": "VALUE_DATA_TYPE_LONG",
                "isNone": False,
                "name": {"string": "AccelerateCacheRefreshLastDetected"},
                "runtimeDataType": None,
                "valueBytes": {"bytes": "0000000000000000"},
                "provenance": None,
                "tag": None,
                "components": None,
            }
        },
        "size": None,
    }

    nodes = transformer.transform(test_event)
    assert len(nodes) == 1
    reg: TCRegistryKey = nodes[0]
    assert reg.uuid == "736F96AB-F043-4ED4-A456-D6F6DC3365FC"
    assert reg.key == "280810"
    assert reg.hive == "USER"


def test_make_addr(transformer):
    test_event = {
        "event_type": "netflowobject",
        "uuid": "80A1F002-2331-4910-982F-6C65930A49F2",
        "baseObject": {
            "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
            "permission": None,
            "epoch": None,
            "properties": None,
        },
        "localAddress": "ff02::1:3",
        "localPort": 5355,
        "remoteAddress": "fe80::2544:d52e:aa5e:4967",
        "remotePort": 56157,
        "ipProtocol": {"int": 17},
        "fileDescriptor": None,
    }

    nodes = transformer.transform(test_event)
    assert len(nodes) == 1
    addr: TCIPAddress = nodes[0]
    assert addr.uuid == "80A1F002-2331-4910-982F-6C65930A49F2"
    assert addr.ip_address == "fe80::2544:d52e:aa5e:4967"


@pytest.mark.parametrize(
    "eventtype, edgeattr",
    [
        ("EVENT_READ", "accessed"),
        ("EVENT_READ", "accessed"),
        ("EVENT_MODIFY_FILE_ATTRIBUTES", "accessed"),
        ("EVENT_OPEN", "accessed"),
        ("EVENT_WRITE", "wrote"),
        ("EVENT_WRITE_APPEND", "wrote"),
        ("EVENT_CREATE_OBJECT", "wrote"),
        ("EVENT_LOAD_LIBRARY", "loaded"),
    ],
)
def test_file_events(transformer, eventtype, edgeattr):
    test_event = {
        "event_type": "event",
        "uuid": "791D9014-6F4A-4F83-A9E2-FB6B5871D119",
        "sequence": {"long": 0},
        "type": eventtype,
        "threadId": {"int": 0},
        "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
        "subject": {"com.bbn.tc.schema.avro.cdm18.UUID": "DF3D9789-C388-440B-92B9-80D45E7E96D4"},
        "predicateObject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "0BCE7E88-FD42-4F41-9DFF-5C8D60DD2406"
        },
        "predicateObjectPath": None,
        "predicateObject2": None,
        "predicateObject2Path": None,
        "timestampNanos": 1523626653225000000,
        "name": {"string": "EVENT_READ"},
        "parameters": None,
        "location": {"long": 0},
        "size": {"long": 0},
        "programPoint": None,
        "properties": None,
    }
    nodes = transformer.transform(test_event)
    assert len(nodes) == 2
    proc: TCProcess = nodes[0]
    assert proc.uuid == "DF3D9789-C388-440B-92B9-80D45E7E96D4"
    f: TCFile = nodes[1]
    assert f.uuid == "0BCE7E88-FD42-4F41-9DFF-5C8D60DD2406"

    assert {"timestamp": 1523626653225000000} in getattr(proc, edgeattr)[f]


def test_launch(transformer):
    test_event = {
        "event_type": "event",
        "uuid": "7020C7EB-7BAC-42DD-B97B-D1BB383F1532",
        "sequence": {"long": 0},
        "type": "EVENT_EXECUTE",
        "threadId": {"int": 0},
        "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
        "subject": {"com.bbn.tc.schema.avro.cdm18.UUID": "BF86A6E5-B54A-4096-8E79-5F746A7EC400"},
        "predicateObject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "D0E7F30A-6F9D-452C-B296-A06350E97871"
        },
        "predicateObjectPath": {"string": "Idle"},
        "predicateObject2": None,
        "predicateObject2Path": None,
        "timestampNanos": 1523626952759000000,
        "name": {"string": "EVENT_EXECUTE"},
        "parameters": None,
        "location": {"long": 0},
        "size": {"long": 0},
        "programPoint": None,
        "properties": None,
    }

    nodes = transformer.transform(test_event)
    assert len(nodes) == 2
    assert nodes[0].uuid == "BF86A6E5-B54A-4096-8E79-5F746A7EC400"
    assert nodes[1].uuid == "D0E7F30A-6F9D-452C-B296-A06350E97871"

    assert {"timestamp": 1523626952759000000} in nodes[0].launched[nodes[1]]


def test_connect(transformer):
    test_event = {
        "event_type": "event",
        "uuid": "783B45BE-2208-4494-82CC-50005E4CA3E4",
        "sequence": {"long": 0},
        "type": "EVENT_CONNECT",
        "threadId": {"int": 0},
        "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
        "subject": {"com.bbn.tc.schema.avro.cdm18.UUID": "CA8B06B8-B4D4-4E64-90F4-FADF919C8556"},
        "predicateObject": {
            "com.bbn.tc.schema.avro.cdm18.UUID": "327970F4-B934-41F3-8146-19A02080F122"
        },
        "predicateObjectPath": None,
        "predicateObject2": None,
        "predicateObject2Path": None,
        "timestampNanos": 1523626654408000000,
        "name": {"string": "EVENT_CONNECT"},
        "parameters": None,
        "location": {"long": 0},
        "size": {"long": 0},
        "programPoint": None,
        "properties": None,
    }
    nodes = transformer.transform(test_event)
    assert len(nodes) == 2
    assert nodes[0].uuid == "CA8B06B8-B4D4-4E64-90F4-FADF919C8556"
    assert nodes[1].uuid == "327970F4-B934-41F3-8146-19A02080F122"

    assert {"timestamp": 1523626654408000000} in nodes[0].connected_to[nodes[1]]
