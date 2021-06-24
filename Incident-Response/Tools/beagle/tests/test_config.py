import os
from beagle.config import BeagleConfig


def setup_function(function):
    """ setup any state tied to the execution of the given function.
    Invoked for every test function in the module.
    """
    os.environ["BEAGLE__TESTSECTION__TESTKEY"] = "testvalue"


def teardown_function(function):
    """ teardown any state that was previously setup with a setup_function
    call.
    """
    del os.environ["BEAGLE__TESTSECTION__TESTKEY"]


def test_get_env_var():

    conf = BeagleConfig()
    assert conf._get_env_var_option("TESTSECTION", "TESTKEY") == "testvalue"
    assert conf._get_env_var_option("testsection", "testkey") == "testvalue"
    assert conf._get_env_var_option("nothere", "foo") is None


def test_env_superseeds_file():

    conf = BeagleConfig()
    conf.read("tests/test.cfg")
    assert conf.get("default", "foo") == "bar"
    os.environ["BEAGLE__DEFAULT__FOO"] = "notintheconfig"
    assert conf.get("default", "foo") == "notintheconfig"
