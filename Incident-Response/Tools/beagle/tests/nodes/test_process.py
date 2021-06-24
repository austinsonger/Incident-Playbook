from beagle.nodes import Process


def testCreate():
    proc = Process(process_id=10, process_image="test.exe")
    assert type(proc) == Process


def testEquals():
    proc = Process(process_id=10, process_image="test.exe")
    other_proc = Process(process_id=10, process_image="test.exe")
    assert proc == other_proc
    assert hash(proc) == hash(other_proc)


def testEqualsMoreFields():
    proc = Process(process_id=10, process_image="test.exe", command_line="test.exe /c foobar")
    other_proc = Process(process_id=10, process_image="test.exe", command_line="test.exe /c 123456")
    assert proc == other_proc
    assert hash(proc) == hash(other_proc)


def testNotEquals():
    proc = Process(process_id=10, process_image="test.exe")
    other_proc = Process(process_id=12, process_image="test.exe")
    assert proc != other_proc
    assert hash(proc) != hash(other_proc)


def testLaunchedAdd():
    parent = Process(process_id=1, process_image="parent.exe")
    child = Process(process_id=2, process_image="child.exe")

    parent.launched[child] += {"timestamp": 12456}
    assert {"timestamp": 12456} in parent.launched[child]


def testLaunchedKeyValues():
    parent = Process(process_id=1, process_image="parent.exe")
    child = Process(process_id=2, process_image="child.exe")

    parent.launched[child].append(timestamp=12456)
    assert {"timestamp": 12456} in parent.launched[child]


def testLaunchedMultipleProces():
    parent = Process(process_id=1, process_image="parent.exe")
    child = Process(process_id=2, process_image="child.exe")

    parent2 = Process(process_id=4, process_image="parent.exe")
    child2 = Process(process_id=3, process_image="child.exe")

    parent.launched[child].append(timestamp=12456)

    parent2.launched[child2].append(timestamp=2)

    assert {"timestamp": 12456} in parent.launched[child]
    assert {"timestamp": 2} not in parent.launched[child]
    assert {"timestamp": 2} in parent2.launched[child2]
    assert {"timestamp": 12456} not in parent2.launched[child2]
