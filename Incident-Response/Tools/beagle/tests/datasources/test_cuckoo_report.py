import json

import pytest

from beagle.constants import EventTypes, FieldNames, Protocols
from beagle.datasources.cuckoo_report import CuckooReport


def make_tmp_file(data: dict, tmpdir):
    p = tmpdir.mkdir("cuckoo").join("data.json")
    p.write(json.dumps(data))
    return p


def test_metadata(tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {},
            "info": {
                "added": 1553807600.200415,
                "started": 1553810186.098672,
                "duration": 325,
                "ended": 1553810511.668111,
                "owner": "",
                "score": 10.4,
                "id": 1003314,
                "category": "file",
                "git": {
                    "head": "03731c4c136532389e93239ac6c3ad38441f81a7",
                    "fetch_head": "03731c4c136532389e93239ac6c3ad38441f81a7",
                },
                "monitor": "22c39cbb35f4d916477b47453673bc50bcd0df09",
                "package": "exe",
                "route": "internet",
                "custom": "",
                "machine": {
                    "status": "stopped",
                    "name": "win7x6415",
                    "label": "win7x6415",
                    "manager": "VirtualBox",
                    "started_on": "2019-03-28 21:56:26",
                    "shutdown_on": "2019-03-28 22:01:47",
                },
                "platform": "windows",
                "version": "2.0.6",
                "options": "procmemdump=yes",
            },
            "target": {
                "category": "file",
                "file": {
                    "sha1": "8338f79279b7126791e0937d1c3933f259e5d658",
                    "name": "It6QworVAgY.exe",
                    "type": "PE32 executable (GUI) Intel 80386, for MS Windows",
                    "sha256": "c1db4b2578729a1faede84d2735eb8463bfd2c6b15d2fdf2de7a89f1954d0dfb",
                    "urls": ["http://ocsp.usertrust.com0"],
                    "crc32": "660E35BC",
                    "path": "/srv/cuckoo/cwd/storage/binaries/c1db4b2578729a1faede84d2735eb8463bfd2c6b15d2fdf2de7a89f1954d0dfb",
                    "ssdeep": "3072:RNkhoRdoQbxSTcbrh82bQZfR3pKHJL1cx0W5yOpIX:RNgo3oInbQZp5MJL1cs7",
                    "size": 206088,
                    "sha512": "8f705313d7c240e72967ac3dfc0d9e3d72090e39e51dd05e803a439a78430946945f87aa596112461aedee68a472a7880a25bb6d5e019615162fa6c35a8108b2",
                    "md5": "44b696079356579d250f716a37ca9b17",
                },
            },
        },
        tmpdir=tmpdir,
    )
    assert CuckooReport(f).metadata() == {
        "machine": "win7x6415",
        "package": "exe",
        "score": 10.4,
        "report_id": 1003314,
        "category": "file",
        "name": "It6QworVAgY.exe",
        "type": "PE32 executable (GUI) Intel 80386, for MS Windows",
    }


def test_identify_processes(tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Windows\\System32\\lsass.exe",
                        "process_name": "lsass.exe",
                        "pid": 488,
                        "first_seen": 1553811201.859375,
                        "ppid": 380,
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                    },
                    {
                        "process_path": "C:\\Windows\\explorer.exe",
                        "process_name": "explorer.exe",
                        "pid": 1260,
                        "first_seen": 1553811213.8125,
                        "ppid": 1184,
                    },
                ]
            }
        },
        tmpdir=tmpdir,
    )

    report = CuckooReport(f)
    report.processes = report.identify_processes()

    # Proc dicts are values.
    json_procs = [json.dumps(proc, sort_keys=True) for proc in report.processes.values()]

    for entry in [
        {
            FieldNames.PROCESS_ID: 488,
            FieldNames.PROCESS_IMAGE: "lsass.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Windows\\System32",
        },
        {
            FieldNames.PROCESS_ID: 2548,
            FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
        },
        {
            FieldNames.PROCESS_ID: 2460,
            FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
        },
        {
            FieldNames.PROCESS_ID: 1260,
            FieldNames.PROCESS_IMAGE: "explorer.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Windows",
        },
    ]:
        assert json.dumps(entry, sort_keys=True) in json_procs


def test_process_tree(tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Windows\\System32\\lsass.exe",
                        "process_name": "lsass.exe",
                        "pid": 488,
                        "first_seen": 1553811201.859375,
                        "ppid": 380,
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                    },
                    {
                        "process_path": "C:\\Windows\\explorer.exe",
                        "process_name": "explorer.exe",
                        "pid": 1260,
                        "first_seen": 1553811213.8125,
                        "ppid": 1184,
                    },
                ],
                "processtree": [
                    {
                        "track": False,
                        "pid": 488,
                        "process_name": "lsass.exe",
                        "command_line": "C:\\Windows\\system32\\lsass.exe",
                        "first_seen": 1553811201.859375,
                        "ppid": 380,
                        "children": [],
                    },
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    },
                    {
                        "track": True,
                        "pid": 1260,
                        "process_name": "explorer.exe",
                        "command_line": "C:\\Windows\\Explorer.EXE",
                        "first_seen": 1553811213.8125,
                        "ppid": 1184,
                        "children": [],
                    },
                ],
            }
        },
        tmpdir=tmpdir,
    )

    report = CuckooReport(f)
    report.processes = report.identify_processes()

    process_events = [json.dumps(proc, sort_keys=True) for proc in report.process_tree()]

    for entry in [
        # This is the only one that has a real parent, all other ones we only know hte PID
        {
            FieldNames.PARENT_PROCESS_ID: 2460,
            FieldNames.PARENT_PROCESS_IMAGE: "It6QworVAgY.exe",
            FieldNames.PARENT_PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
            FieldNames.PARENT_COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
            FieldNames.PROCESS_ID: 2548,
            FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
            FieldNames.COMMAND_LINE: "--39dd5ff7",
            FieldNames.TIMESTAMP: 1553811204.703125,
            FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
        },
        {
            FieldNames.PROCESS_ID: 488,
            FieldNames.PROCESS_IMAGE: "lsass.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Windows\\System32",
            FieldNames.COMMAND_LINE: "C:\\Windows\\system32\\lsass.exe",
            FieldNames.TIMESTAMP: 1553811201.859375,
            FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            FieldNames.PARENT_PROCESS_ID: 380,
            FieldNames.PARENT_PROCESS_IMAGE: "Unknown",
            FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
            FieldNames.PARENT_COMMAND_LINE: "",
        },
        {
            FieldNames.PROCESS_ID: 2460,
            FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
            FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
            FieldNames.TIMESTAMP: 1553811202.765625,
            FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            FieldNames.PARENT_PROCESS_ID: 1272,
            FieldNames.PARENT_PROCESS_IMAGE: "Unknown",
            FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
            FieldNames.PARENT_COMMAND_LINE: "",
        },
        {
            FieldNames.PROCESS_ID: 1260,
            FieldNames.PROCESS_IMAGE: "explorer.exe",
            FieldNames.PROCESS_IMAGE_PATH: "C:\\Windows",
            FieldNames.COMMAND_LINE: "C:\\Windows\\Explorer.EXE",
            FieldNames.TIMESTAMP: 1553811213.8125,
            FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            FieldNames.PARENT_PROCESS_ID: 1184,
            FieldNames.PARENT_PROCESS_IMAGE: "Unknown",
            FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
            FieldNames.PARENT_COMMAND_LINE: "",
        },
    ]:
        assert json.dumps(entry, sort_keys=True) in process_events


@pytest.mark.parametrize(
    "dictkey,eventtype",
    [
        ("file_deleted", EventTypes.FILE_DELETED),
        ("file_opened", EventTypes.FILE_OPENED),
        ("file_failed", EventTypes.FILE_OPENED),
        ("file_read", EventTypes.FILE_OPENED),
        ("file_written", EventTypes.FILE_WRITTEN),
        ("dll_loaded", EventTypes.LOADED_MODULE),
        ("file_attribute_changed", EventTypes.FILE_OPENED),
        ("file_exists", EventTypes.FILE_OPENED),
    ],
)
def test_basic_file_events(dictkey, eventtype, tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {dictkey: ["C:\\Users\\desktop.ini"]},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: eventtype,
                FieldNames.FILE_NAME: "desktop.ini",
                FieldNames.FILE_PATH: "C:\\Users",
            },
            sort_keys=True,
        )
        in events
    )


def test_basicfile_skips_folders(tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {"file_opened": ["C:\\Users\\"]},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    # Should have no events, only two for the processes.
    assert len(events) == 2


@pytest.mark.parametrize("connects_type", ["connects_host", "connects_ip"])
def test_connections(connects_type, tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {connects_type: ["domain.com"]},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    # Should have no events, only two for the processes.
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.IP_ADDRESS: "domain.com",
            },
            sort_keys=True,
        )
        in events
    )


def test_dnslookup(tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {"resolves_host": ["domain.com"]},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    # Should have no events, only two for the processes.
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                FieldNames.HTTP_HOST: "domain.com",
            },
            sort_keys=True,
        )
        in events
    )


@pytest.mark.parametrize("url_type", ["fetches_url", "downloads_file"])
def test_url_events(url_type, tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {url_type: ["http://domain.com/foobar"]},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    # Should have no events, only two for the processes.
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
                FieldNames.HTTP_METHOD: "GET",
                FieldNames.HTTP_HOST: "domain.com",
                FieldNames.URI: "/foobar",
            },
            sort_keys=True,
        )
        in events
    )


@pytest.mark.parametrize(
    "event_type,edge_type",
    [
        ("regkey_written", EventTypes.REG_KEY_SET),
        ("regkey_deleted", EventTypes.REG_KEY_DELETED),
        ("regkey_opened", EventTypes.REG_KEY_OPENED),
        ("regkey_read", EventTypes.REG_KEY_OPENED),
    ],
)
def test_regevents(event_type, edge_type, tmpdir):
    f = make_tmp_file(
        data={
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {
                            event_type: [
                                "HKEY_USERS\\S-1\\Software\\Microsoft\\Internet Explorer\\Toolbar\\Locked"
                            ]
                        },
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            }
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]
    # Should have no events, only two for the processes.
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: edge_type,
                FieldNames.HIVE: "HKEY_USERS",
                FieldNames.REG_KEY_PATH: "S-1\\Software\\Microsoft\\Internet Explorer\\Toolbar",
                FieldNames.REG_KEY: "Locked",
            },
            sort_keys=True,
        )
        in events
    )


@pytest.mark.parametrize("key,conn_type", [("udp", Protocols.UDP), ("tcp", Protocols.TCP)])
def test_global_connection(key, conn_type, tmpdir):
    f = make_tmp_file(
        data={
            "target": {"file": {"name": "It6QworVAgY.exe"}},
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            "network": {
                key: [
                    {
                        "src": "192.168.168.201",
                        "dst": "192.168.168.205",
                        "offset": 24,
                        "time": 0.0,
                        "dport": 52884,
                        "sport": 5355,
                    }
                ]
            },
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]

    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.IP_ADDRESS: "192.168.168.205",
                FieldNames.PROTOCOL: conn_type,
                FieldNames.PORT: 52884,
            },
            sort_keys=True,
        )
        in events
    )


def test_icmp_connection(tmpdir):
    f = make_tmp_file(
        data={
            "target": {"file": {"name": "It6QworVAgY.exe"}},
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            "network": {"icmp": [{"src": "192.168.168.201", "dst": "192.168.168.205", "type": 3}]},
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]

    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
                FieldNames.IP_ADDRESS: "192.168.168.205",
                FieldNames.PROTOCOL: Protocols.ICMP,
            },
            sort_keys=True,
        )
        in events
    )


def test_dnslookup_no_answer_connection(tmpdir):
    f = make_tmp_file(
        data={
            "target": {"file": {"name": "It6QworVAgY.exe"}},
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            "network": {"dns": [{"request": "pastebin.com", "type": "A", "answers": []}]},
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]

    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                FieldNames.HTTP_HOST: "pastebin.com",
            },
            sort_keys=True,
        )
        in events
    )


def test_dnslookup_answers_connection(tmpdir):
    f = make_tmp_file(
        data={
            "target": {"file": {"name": "It6QworVAgY.exe"}},
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            "network": {
                "dns": [
                    {
                        "request": "pastebin.com",
                        "type": "A",
                        "answers": [
                            {"data": "1.1.1.1", "type": "A"},
                            {"data": "2.2.2.2", "type": "A"},
                        ],
                    }
                ]
            },
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]

    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                FieldNames.HTTP_HOST: "pastebin.com",
                FieldNames.IP_ADDRESS: "1.1.1.1",
            },
            sort_keys=True,
        )
        in events
    )

    # Both answers need to be in there.
    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
                FieldNames.HTTP_HOST: "pastebin.com",
                FieldNames.IP_ADDRESS: "2.2.2.2",
            },
            sort_keys=True,
        )
        in events
    )


def test_http_ex_requests(tmpdir):
    f = make_tmp_file(
        data={
            "target": {"file": {"name": "It6QworVAgY.exe"}},
            "behavior": {
                "generic": [
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2460,
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "summary": {},
                    },
                    {
                        "process_path": "C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe",
                        "process_name": "It6QworVAgY.exe",
                        "pid": 2548,
                        "first_seen": 1553811204.703125,
                        "ppid": 2460,
                        "summary": {},
                    },
                ],
                "processtree": [
                    {
                        "track": True,
                        "pid": 2460,
                        "process_name": "It6QworVAgY.exe",
                        "command_line": '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                        "first_seen": 1553811202.765625,
                        "ppid": 1272,
                        "children": [
                            {
                                "track": True,
                                "pid": 2548,
                                "process_name": "It6QworVAgY.exe",
                                "command_line": "--39dd5ff7",
                                "first_seen": 1553811204.703125,
                                "ppid": 2460,
                                "children": [],
                            }
                        ],
                    }
                ],
            },
            "network": {
                "http_ex": [
                    {
                        "status": 200,
                        "src": "192.168.168.205",
                        "resp": {
                            "path": "/srv/cuckoo/cwd/storage/analyses/944094/network/33bf88d5b82df3723d5863c7d23445e345828904",
                            "sha1": "33bf88d5b82df3723d5863c7d23445e345828904",
                            "md5": "cd5a4d3fdd5bffc16bf959ef75cf37bc",
                        },
                        "sha1": "33bf88d5b82df3723d5863c7d23445e345828904",
                        "protocol": "http",
                        "dst": "92.122.190.16",
                        "req": {
                            "path": "/srv/cuckoo/cwd/storage/analyses/944094/network/da39a3ee5e6b4b0d3255bfef95601890afd80709",
                            "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
                            "md5": "d41d8cd98f00b204e9800998ecf8427e",
                        },
                        "request": "GET /ncsi.txt HTTP/1.1\r\nConnection: Close\r\nUser-Agent: Microsoft NCSI\r\nHost: www.msftncsi.com",
                        "uri": "/ncsi.txt",
                        "response": "HTTP/1.1 200 OK\r\nContent-Length: 14\r\nDate: Mon, 25 Feb 2019 17:31:25 GMT\r\nConnection: close\r\nContent-Type: text/plain\r\nCache-Control: max-age=30, must-revalidate",
                        "host": "www.msftncsi.com",
                        "dport": 80,
                        "path": "/srv/cuckoo/cwd/storage/analyses/944094/network/33bf88d5b82df3723d5863c7d23445e345828904",
                        "sport": 49159,
                        "method": "GET",
                        "md5": "cd5a4d3fdd5bffc16bf959ef75cf37bc",
                    }
                ]
            },
        },
        tmpdir=tmpdir,
    )
    report = CuckooReport(f)
    report.processes = report.identify_processes()

    events = [json.dumps(e, sort_keys=True) for e in report.events()]

    assert (
        json.dumps(
            {
                FieldNames.PROCESS_ID: 2460,
                FieldNames.PROCESS_IMAGE: "It6QworVAgY.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Users\\Administrator\\AppData\\Local\\Temp",
                FieldNames.COMMAND_LINE: '"C:\\Users\\Administrator\\AppData\\Local\\Temp\\It6QworVAgY.exe" ',
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
                FieldNames.HTTP_HOST: "www.msftncsi.com",
                FieldNames.IP_ADDRESS: "92.122.190.16",
                FieldNames.HTTP_METHOD: "GET",
                FieldNames.URI: "/ncsi.txt",
            },
            sort_keys=True,
        )
        in events
    )

