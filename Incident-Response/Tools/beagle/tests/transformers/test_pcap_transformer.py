import pytest

from beagle.transformers import PCAPTransformer
from beagle.nodes import Domain, URI, IPAddress


@pytest.fixture
def transformer() -> PCAPTransformer:
    return PCAPTransformer(datasource=None)  # type: ignore


@pytest.mark.parametrize(
    "event",
    [
        {"event_type": "foobar"},
        {"event_type": "TCP"},
        {"event_type": "foobar", "src_ip": "123.0.0.1"},
        {"event_type": "foobar", "dst_ip": "123.0.0.1"},
        {"event_type": "foobar", "dst_ip": "123.0.0.1"},
        {"event_type": "Ether", "dst_ip": "123.0.0.1", "src_ip": "123.0.0.1"},
        {"event_type": "IP", "dst_ip": "123.0.0.1", "src_ip": "123.0.0.1"},
    ],
)
def test_expected_none(transformer, event):
    """Events should have atleast src_ip and dst_ip, and a protocol above IP only"""

    nodes = transformer.transform(event)

    assert nodes is None


def test_basic_connection(transformer):
    event = {
        "src_ip": "127.0.0.1",
        "dst_ip": "192.168.1.1",
        "src_mac": "ab:ab:ab:ab:ab:ab",
        "dst_mac": "12:12:12:12:12:12",
        "event_type": "TCP",
        "protocol": "tcp",
        "sport": "12345",
        "dport": "80",
        "payload": "1",
        "timestamp": 1,
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 2
    assert nodes[1] in nodes[0].connected_to
    src: IPAddress = nodes[0]
    dst: IPAddress = nodes[1]

    assert src.ip_address == "127.0.0.1"
    assert dst.ip_address == "192.168.1.1"
    assert src.mac == "ab:ab:ab:ab:ab:ab"
    assert dst.mac == "12:12:12:12:12:12"


def test_http_request(transformer):
    event = {
        "src_mac": "ab:ab:ab:ab:ab:ab",
        "dst_mac": "12:12:12:12:12:12",
        "src_ip": "127.0.0.1",
        "dst_ip": "192.168.1.1",
        "sport": 12345,
        "dport": 80,
        "http_method": "GET",
        "uri": "/foo",
        "http_dest": "https://google.com",
        "event_type": "HTTPRequest",
        "protocol": "tcp",
        "payload": "1",
        "timestamp": 1,
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 4
    assert nodes[1] in nodes[0].connected_to
    src: IPAddress = nodes[0]
    dst: IPAddress = nodes[1]
    dom: Domain = nodes[2]
    uri: URI = nodes[3]

    assert src.ip_address == "127.0.0.1"
    assert dst.ip_address == "192.168.1.1"
    assert src.mac == "ab:ab:ab:ab:ab:ab"
    assert dst.mac == "12:12:12:12:12:12"

    assert uri.uri == "/foo"
    assert dom.domain == "https://google.com"
    assert dom in uri.uri_of
    assert uri in src.http_request_to
    assert dst in dom.resolves_to


def test_dns_request_one_resp(transformer):
    event = {
        "src_mac": "ab:ab:ab:ab:ab:ab",
        "dst_mac": "12:12:12:12:12:12",
        "src_ip": "127.0.0.1",
        "dst_ip": "192.168.1.1",
        "sport": 80,
        "dport": 53,
        "qname": "google.com.",
        "qanswer": "123.0.0.1",
        "qtype": "A",
        "payload": "1",
        "event_type": "DNS",
        "timestamp": 1,
        "protocol": "udp",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 4
    src: IPAddress = nodes[0]
    dst: IPAddress = nodes[3]
    dom: Domain = nodes[1]
    ip: URI = nodes[2]
    assert dst in src.connected_to

    assert src.ip_address == "127.0.0.1"
    assert dst.ip_address == "192.168.1.1"
    assert src.mac == "ab:ab:ab:ab:ab:ab"
    assert dst.mac == "12:12:12:12:12:12"

    assert ip.ip_address == "123.0.0.1"
    assert dom.domain == "google.com"
    assert ip in dom.resolves_to
    assert dom in src.dns_query_for
    assert {"record_type": "A"} in src.dns_query_for[dom]


def test_dns_request_no_resp(transformer):
    event = {
        "src_mac": "ab:ab:ab:ab:ab:ab",
        "dst_mac": "12:12:12:12:12:12",
        "src_ip": "127.0.0.1",
        "dst_ip": "192.168.1.1",
        "sport": 80,
        "dport": 53,
        "qname": "google.com.",
        "qtype": "A",
        "timestamp": 1,
        "payload": "1",
        "event_type": "DNS",
        "protocol": "udp",
    }

    nodes = transformer.transform(event)
    assert len(nodes) == 3
    src: IPAddress = nodes[0]
    dst: IPAddress = nodes[2]
    dom: Domain = nodes[1]
    assert dst in src.connected_to

    assert src.ip_address == "127.0.0.1"
    assert dst.ip_address == "192.168.1.1"
    assert src.mac == "ab:ab:ab:ab:ab:ab"
    assert dst.mac == "12:12:12:12:12:12"

    assert dom.domain == "google.com"
    assert dom in src.dns_query_for
