import json
from beagle.datasources import DARPATCJson
from typing import List


def make_tmp_file(data: List[dict], tmpdir):
    p = tmpdir.mkdir("darpa").join("data.json")
    for event in data:
        p.write(json.dumps(event))
    return p


def test_init():
    d = DARPATCJson("data/tc3/ta1-cadets-e3-official.json")
    assert d.file_path == "data/tc3/ta1-cadets-e3-official.json"


def test_metadata():
    d = DARPATCJson("data/tc3/ta1-cadets-e3-official.json")
    assert d.metadata() == {"filename": "ta1-cadets-e3-official.json"}


def test_event_adjusted(tmpdir):
    event = {
        "datum": {
            "CDMVersion": "18",
            "source": "SOURCE_WINDOWS_FIVEDIRECTIONS",
            "com.bbn.tc.schema.avro.cdm18.Event": {
                "uuid": "783B45BE-2208-4494-82CC-50005E4CA3E4",
                "sequence": {"long": 0},
                "type": "EVENT_CONNECT",
                "threadId": {"int": 0},
                "hostId": "47923ED7-29D4-4E65-ABA2-F70A4E74DCCD",
                "subject": {
                    "com.bbn.tc.schema.avro.cdm18.UUID": "CA8B06B8-B4D4-4E64-90F4-FADF919C8556"
                },
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
            },
        }
    }

    f = make_tmp_file(data=[event], tmpdir=tmpdir)

    events = DARPATCJson(f).events()

    assert next(events) == {
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
