from beagle.nodes import Domain, URI


def test_create_dom():
    dom = Domain("foobar.com")
    assert dom.domain == "foobar.com"
    assert dom._display == "foobar.com"


def test_create_uri():
    uri = URI("/foobar")
    assert uri.uri == "/foobar"


def test_uri_of():
    dom = Domain("foobar.com")
    uri = URI("/foobar")

    uri.uri_of[dom].append(timestamp=1234)

    assert dom in uri.uri_of
    assert {"timestamp": 1234} in uri.uri_of[dom]
