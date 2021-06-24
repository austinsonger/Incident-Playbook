import json

import pytest

from beagle.datasources.fireeye_ax_report import FireEyeAXReport


@pytest.fixture
def datasource(tmpdir) -> FireEyeAXReport:
    return FireEyeAXReport(make_default_file(tmpdir))


def make_tmp_file(data: dict, tmpdir):
    p = tmpdir.mkdir("ax").join("data.json")
    p.write(json.dumps(data))
    return p


def make_default_file(tmpdir):
    p = tmpdir.mkdir("ax").join("data.json")
    p.write(json.dumps({"version": "8.1.0", "alert": [{"explanation": {"osChanges": [{}]}}]}))
    return p


def test_no_data(tmpdir):

    f = make_tmp_file(data={"test": "fest"}, tmpdir=tmpdir)
    FireEyeAXReport(f)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"version": "8.1.0", "alert": []},
        {"version": "8.1.0", "alert": [{"occurred": "2018-03-31 13:40:01 +0000", "foo": []}]},
        {
            "version": "8.1.0",
            "alert": [{"occurred": "2018-03-31 13:40:01 +0000", "explanation": {}}],
        },
        {
            "version": "8.1.0",
            "alert": [
                {"occurred": "2018-03-31 13:40:01 +0000", "explanation": {"osChanges": [{}]}}
            ],
        },
    ],
)
def test_no_events(data, tmpdir):
    f = make_tmp_file(data=data, tmpdir=tmpdir)
    assert len(list(FireEyeAXReport(f).events())) == 0


def test_get_metadata(tmpdir):
    f = make_tmp_file(
        data={
            "version": "8.1.0",
            "alert": [
                {
                    "explanation": {"malwareDetected": {"malware": [{"name": "Stuxnet"}]}},
                    "src": {},
                    "alertUrl": "https://foo",
                    "action": "notified",
                    "occurred": "2018-03-31 13:40:01 +0000",
                    "dst": {},
                    "id": 1234,
                    "name": "MALWARE_OBJECT",
                    "severity": "MAJR",
                    "product": "MAS",
                }
            ],
            "appliance": "my_appliance",
        },
        tmpdir=tmpdir,
    )

    assert FireEyeAXReport(f).metadata() == {
        "hostname": "my_appliance",
        "analyzed_on": "2018-03-31 13:40:01 +0000",
        "severity": "MAJR",
        "alert": "Stuxnet",
        "alert_url": "https://foo",
    }


@pytest.mark.parametrize(
    "data",
    [
        {"version": "8.1.0", "alert": [{"occurred": "2018-03-31 13:40:01 +0000", "foo": []}]},
        {"version": "8.1.0", "alert": [{"occurred": "2018-03-31T13:40:01Z +0000", "foo": []}]},
        {"version": "8.1.0", "alert": [{"occurred": "2018-03-31T13:40:01Z", "foo": []}]},
    ],
)
def test_multiple_time_formats(data, tmpdir):
    f = make_tmp_file(data=data, tmpdir=tmpdir)
    assert isinstance(FireEyeAXReport(f).base_timestamp, int)


def test_invalid_time_format(tmpdir):

    # invalid raises value error.
    data = {"version": "8.1.0", "alert": [{"occurred": "2018/03/31 13:40:01 +0000", "foo": []}]}
    f = make_tmp_file(data=data, tmpdir=tmpdir)
    with pytest.raises(ValueError):
        assert 1522503601 == FireEyeAXReport(f).base_timestamp
