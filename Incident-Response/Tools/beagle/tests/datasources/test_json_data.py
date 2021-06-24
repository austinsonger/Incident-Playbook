import json
from beagle.datasources.json_data import JSONFile


def test_init():
    d = JSONFile("data/tc3/ta1-cadets-e3-official.json")
    assert d.file_path == "data/tc3/ta1-cadets-e3-official.json"


def test_metadata():
    d = JSONFile("data/tc3/ta1-cadets-e3-official.json")
    assert d.metadata() == {"filename": "ta1-cadets-e3-official.json"}


def test_events_in_newline(tmpdir):
    p = tmpdir.mkdir("json_data").join("data.json")
    p.write("\n".join([json.dumps(x) for x in [{"foo": "bar"}, {"foo": "tar"}]]))
    events = list(JSONFile(p).events())

    assert all([x in events for x in [{"foo": "bar"}, {"foo": "tar"}]])


def test_event_in_array(tmpdir):
    p = tmpdir.mkdir("json_data").join("data.json")
    p.write(json.dumps([{"foo": "bar"}, {"foo": "tar"}]))

    assert list(JSONFile(p).events()) == [{"foo": "bar"}, {"foo": "tar"}]
