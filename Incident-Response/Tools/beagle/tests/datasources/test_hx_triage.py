import mock
import pytest
from beagle.datasources.hx_triage import HXTriage


class MockHXTriage(HXTriage):
    name = "HXTriage"
    transformers = []  # type: ignore
    category = "foo"

    def __init__(self):
        pass


@pytest.mark.parametrize(
    "event,expected",
    [
        (
            {"pid": "4"},
            {
                "pid": "4",
                "processPath": "\\",
                "process": "SYSTEM",
                "username": "NT AUTHORITY\\SYSTEM",
            },
        ),
        (
            {"pid": "0"},
            {
                "pid": "0",
                "processPath": "\\",
                "process": "System Idle Process",
                "username": "Unknown",
            },
        ),
        (
            {"pid": "10"},
            {
                "pid": "10",
                "processPath": "\\",
                "process": "System Idle Process",
                "username": "Unknown",
            },
        ),
        ({"pid": "10", "processPath": "foo"}, {"pid": "10", "processPath": "foo"}),
    ],
)
def test_fix_missing_fields(event, expected):
    triage = MockHXTriage()

    assert triage._fix_missing_fields(event) == expected


def test_agent_events_file(tmpdir):
    triage = MockHXTriage()
    triage._hx_time_to_epoch = mock.MagicMock()
    triage._hx_time_to_epoch.return_value = 1234

    agent_events = """<?xml version="1.0" encoding="UTF-8"?>
<itemList generator="stateagentinspector" generatorVersion="24.9.0" itemSchemaLocation="http://schemas.mandiant.com/2013/11/stateagentinspectoritem.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://schemas.mandiant.com/2013/11/stateagentinspectoritem.xsd">
 <eventItem uid="39265403">
  <timestamp>2018-06-27T21:15:32.678Z</timestamp>
  <eventType>dnsLookupEvent</eventType>
  <details>
   <detail>
    <name>hostname</name>
    <value>github.com</value>
   </detail>
   <detail>
    <name>pid</name>
    <value>25048</value>
   </detail>
   <detail>
    <name>process</name>
    <value>git-remote-https.exe</value>
   </detail>
   <detail>
    <name>processPath</name>
    <value>\\Device\\HarddiskVolume3\\Program Files\\Git\\mingw64\\libexec\\git-core</value>
   </detail>
   <detail>
    <name>username</name>
    <value>test</value>
   </detail>
  </details>
 </eventItem>
</itemList>"""
    p = tmpdir.mkdir("hxtriage").join("agentevents.xml")
    p.write(agent_events)
    # returns a generator
    events = list(triage.parse_agent_events(p))
    assert len(events) == 1

    assert events[0] == {
        "event_type": "dnsLookupEvent",
        "hostname": "github.com",
        "pid": "25048",
        "process": "git-remote-https.exe",
        "processPath": "\\Device\\HarddiskVolume3\\Program Files\\Git\\mingw64\\libexec\\git-core",
        "username": "test",
        "event_time": 1234,
    }
