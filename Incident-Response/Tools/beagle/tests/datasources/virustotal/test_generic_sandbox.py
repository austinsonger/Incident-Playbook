import pytest

from beagle.constants import EventTypes, FieldNames, HashAlgos, Protocols
from beagle.datasources import GenericVTSandbox


def tencent1() -> GenericVTSandbox:
    r = GenericVTSandbox("tests/datasources/virustotal/test_files/example_tencent_habo1.json")
    next(r.events())
    return r


def tencent_nested() -> GenericVTSandbox:
    r = GenericVTSandbox(
        "tests/datasources/virustotal/test_files/example_tencent_habo_very_nested.json"
    )
    next(r.events())
    return r


def drweb_nested() -> GenericVTSandbox:
    r = GenericVTSandbox(
        "tests/datasources/virustotal/test_files/example_drweb_nested_children.json"
    )
    next(r.events())
    return r


def drweb_net() -> GenericVTSandbox:
    r = GenericVTSandbox("tests/datasources/virustotal/test_files/example_drweb_api_with_net.json")
    next(r.events())
    return r


def test_init():
    assert tencent1() is not None


@pytest.mark.parametrize(
    "proc_name, output",
    [
        # no path
        (
            "find.exe",
            {
                FieldNames.PROCESS_IMAGE: "find.exe",
                FieldNames.COMMAND_LINE: "",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
            },
        ),
        # no command line
        (
            "<SYSTEM32>\\find.exe",
            {
                FieldNames.PROCESS_IMAGE: "find.exe",
                FieldNames.PROCESS_IMAGE_PATH: "<SYSTEM32>",
                FieldNames.COMMAND_LINE: "",
            },
        ),
        (
            'tasklist.exe tasklist /nh /fi "imagename eq svhost.exe"',
            {
                FieldNames.PROCESS_IMAGE: "tasklist.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: 'tasklist /nh /fi "imagename eq svhost.exe"',
            },
        ),
        # Case with a command line
        (
            'C:\\Windows\\system32\\cmd.exe /c "C:\\Users\\USER\\AppData\\Local\\Temp\\qslrc.exe""',
            {
                FieldNames.PROCESS_IMAGE: "cmd.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\Windows\\system32",
                FieldNames.COMMAND_LINE: '/c "C:\\Users\\USER\\AppData\\Local\\Temp\\qslrc.exe""',
            },
        ),
        # Case with a space in dir name.
        (
            'C:\\foo bar\\cmd.exe /c "C:\\Users\\USER\\AppData\\Local\\Temp\\qslrc.exe""',
            {
                FieldNames.PROCESS_IMAGE: "cmd.exe",
                FieldNames.PROCESS_IMAGE_PATH: "C:\\foo bar",
                FieldNames.COMMAND_LINE: '/c "C:\\Users\\USER\\AppData\\Local\\Temp\\qslrc.exe""',
            },
        ),
        (
            "****.exe",
            {
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: "",
            },
        ),
    ],
)
def test_parse_process_name(proc_name, output):
    parser = tencent1()
    assert parser._parse_process_name(proc_name) == output


@pytest.mark.parametrize("source,count", [(tencent1, 48), (tencent_nested, 312)])
def test_proc_tree(source, count):
    # Make sure the process tree captures all nested processes.

    procs = list(source()._proc_tree())

    # 4 root procs, others are all nested.
    assert len(procs) == count


@pytest.mark.parametrize(
    "source,first_proc",
    [
        (
            tencent1,
            {
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1572",
                FieldNames.COMMAND_LINE: "",
            },
        ),
        (
            tencent_nested,
            {
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "716",
                FieldNames.COMMAND_LINE: "",
            },
        ),
        (
            drweb_nested,
            {
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "3852",
                FieldNames.COMMAND_LINE: "",
            },
        ),
        (
            drweb_net,
            {
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
            },
        ),
    ],
)
def test_get_root_proc(source, first_proc: dict):
    assert first_proc == source()._get_root_proc()


@pytest.mark.parametrize(
    "source,nested_proc",
    [
        (
            tencent1,
            {
                FieldNames.PARENT_PROCESS_IMAGE: "cmd.exe",
                FieldNames.PARENT_COMMAND_LINE: "",
                FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
                FieldNames.PARENT_PROCESS_ID: "244",
                FieldNames.PROCESS_ID: "636",
                FieldNames.PROCESS_IMAGE: "ping.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            },
        ),
        (
            tencent_nested,
            {
                FieldNames.PARENT_PROCESS_IMAGE: "cmd.exe",
                FieldNames.PARENT_PROCESS_IMAGE_PATH: "\\",
                FieldNames.PARENT_PROCESS_ID: "2568",
                FieldNames.PARENT_COMMAND_LINE: '/K name.exe"',
                FieldNames.PROCESS_IMAGE: "find.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.COMMAND_LINE: 'find /i "svhost.exe"',
                FieldNames.PROCESS_ID: "3144",
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            },
        ),
        (
            drweb_nested,
            {
                FieldNames.PARENT_PROCESS_IMAGE: "cmd.exe",
                FieldNames.PARENT_PROCESS_IMAGE_PATH: "<SYSTEM32>",
                FieldNames.PARENT_PROCESS_ID: "3868",
                FieldNames.PARENT_COMMAND_LINE: "",
                FieldNames.COMMAND_LINE: "",
                FieldNames.PROCESS_IMAGE_PATH: "<SYSTEM32>",
                FieldNames.PROCESS_IMAGE: "reg.exe",
                FieldNames.PROCESS_ID: "3876",
                FieldNames.TIMESTAMP: 5,
                FieldNames.EVENT_TYPE: EventTypes.PROCESS_LAUNCHED,
            },
        ),
    ],
)
def test_very_nested(source, nested_proc: dict):
    procs = list(source()._proc_tree())

    assert nested_proc in procs


@pytest.mark.parametrize(
    "source,file_entry",
    [
        (
            tencent_nested,
            {
                FieldNames.FILE_PATH: "C:\\Documents and Settings\\Administrator\\AppData\\Local\\Temp\\FolderN",
                FieldNames.FILE_NAME: "name.exe.lnk",
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "716",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.FILE_WRITTEN,
            },
        ),
        (
            tencent_nested,
            {
                FieldNames.FILE_NAME: "ADVAPI32.dll",
                FieldNames.FILE_PATH: "\\",
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "716",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.LOADED_MODULE,
            },
        ),
        (
            tencent_nested,
            {
                FieldNames.FILE_NAME: "desktop.ini",
                FieldNames.FILE_PATH: "C:\\Documents and Settings\\All Users\\「开始」菜单",
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "716",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.FILE_OPENED,
            },
        ),
        (
            drweb_nested,
            {
                FieldNames.FILE_NAME: "svhost.exe",
                FieldNames.FILE_PATH: "%TEMP%",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "3852",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.FILE_OPENED,
            },
        ),
    ],
)
def test_basic_file_operations(source, file_entry: dict):
    files = list(source()._basic_file_events())

    assert file_entry in files


@pytest.mark.parametrize(
    "source, file_entry",
    [
        (
            drweb_nested,
            {
                FieldNames.FILE_NAME: "name.exe.bat",
                FieldNames.FILE_PATH: "%HOMEPATH%\\appdata\\local\\temp\\foldern",
                FieldNames.HASHES: {
                    HashAlgos.SHA256: "4691d1592b74a2751ea8498ad898a6dec762a69f982dd78be321d29ba536600f"
                },
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "3852",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.FILE_WRITTEN,
            },
        ),
        (
            tencent_nested,
            {
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
            },
        ),
    ],
)
def test_complex_file_events(source, file_entry: dict):
    files = list(source()._complex_file_events())

    assert file_entry in files


@pytest.mark.parametrize(
    "source, network_event",
    [
        (
            tencent1,
            {
                FieldNames.HTTP_HOST: "imp.hmynewswire.co",
                FieldNames.PROCESS_IMAGE: "****.exe",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1572",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
            },
        ),
        (
            drweb_net,
            {
                FieldNames.HTTP_HOST: "crl.pki.goog",
                FieldNames.IP_ADDRESS: "216.58.212.238",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.DNS_LOOKUP,
            },
        ),
        (
            drweb_net,
            {
                FieldNames.HTTP_HOST: "107.10.49.252",
                FieldNames.URI: "/",
                FieldNames.HTTP_METHOD: "GET",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
            },
        ),
        (
            drweb_net,
            {
                FieldNames.HTTP_HOST: "107.10.49.252",
                FieldNames.URI: "/",
                FieldNames.HTTP_METHOD: "GET",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.HTTP_REQUEST,
            },
        ),
        (
            drweb_net,
            {
                FieldNames.IP_ADDRESS: "24.151.31.150",
                FieldNames.PROTOCOL: Protocols.TCP,
                FieldNames.PORT: 465,
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.CONNECTION,
            },
        ),
    ],
)
def test_network_events(source, network_event: dict):
    network_events = list(source()._network_events())

    assert network_event in network_events


@pytest.mark.parametrize(
    "source, reg_event",
    [
        (
            drweb_net,
            {
                FieldNames.HIVE: "",
                FieldNames.REG_KEY_PATH: "REGISTRY\\USER\\S-1-5-18\\Software\\Microsoft\\windows\\CurrentVersion\\Internet Settings",
                FieldNames.REG_KEY: "ProxyServer",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.REG_KEY_DELETED,
            },
        ),
        (
            drweb_net,
            {
                FieldNames.HIVE: "<HKLM>",
                FieldNames.REG_KEY_PATH: "System\\CurrentControlSet\\Control",
                FieldNames.REG_KEY: "Session Manager",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.REG_KEY_OPENED,
            },
        ),
    ],
)
def test_basic_registry(source, reg_event: dict):
    reg_events_basic = list(source()._basic_registry_events())

    assert reg_event in reg_events_basic


@pytest.mark.parametrize(
    "source, reg_event",
    [
        (
            drweb_net,
            {
                FieldNames.HIVE: "<HKLM>",
                FieldNames.REG_KEY_PATH: "System\\CurrentControlSet\\Services\\wordpadmouse",
                FieldNames.REG_KEY: "Type",
                FieldNames.REG_KEY_VALUE: "0x00000010",
                FieldNames.PROCESS_IMAGE: "<PATH_SAMPLE.EXE>",
                FieldNames.PROCESS_IMAGE_PATH: "\\",
                FieldNames.PROCESS_ID: "1748",
                FieldNames.COMMAND_LINE: "",
                FieldNames.EVENT_TYPE: EventTypes.REG_KEY_SET,
            },
        )
    ],
)
def test_complex_registry_events(source, reg_event: dict):
    reg_events_cmplx = list(source()._complex_registry_events())

    assert reg_event in reg_events_cmplx


def test_metadata():
    sandbox = GenericVTSandbox(
        "tests/datasources/virustotal/test_files/example_tencent_habo_very_nested.json",
        "tests/datasources/virustotal/test_files/example_vt3_api_results.json",
    )

    metadata = sandbox.metadata()

    assert metadata["name"] == "codexgigas_235f100673f34412b21f9f708be89384ae102db4"
    assert metadata["malicious"] == 57
