from io import BytesIO
from scapy.all import Ether, PcapWriter, Packet, IP, UDP, TCP, DNS, DNSQR, DNSRR
from scapy.layers.http import HTTPRequest, HTTP
from typing import List
from beagle.datasources.pcap import PCAP


def packets_to_datasource_events(packets: List[Packet]) -> PCAP:
    f = BytesIO()
    PcapWriter(f).write(packets)
    f.seek(0)
    return PCAP(f)  # type: ignore


def test_single_ether_packet():

    packets = [Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["event_type"] == "Ether"


def test_single_ip_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["event_type"] == "IP"


def test_single_udp_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / UDP(sport=80, dport=5355)
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["sport"] == 80
    assert events[0]["dport"] == 5355
    assert events[0]["event_type"] == "UDP"


def test_single_tcp_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / TCP(sport=80, dport=5355)
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["sport"] == 80
    assert events[0]["dport"] == 5355
    assert events[0]["event_type"] == "TCP"


def test_single_dns_resp_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / UDP(sport=80, dport=53)
        / DNS(rd=1, qd=DNSQR(qtype="A", qname="google.com"), an=DNSRR(rdata="123.0.0.1"))
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["sport"] == 80
    assert events[0]["dport"] == 53
    assert events[0]["qname"] == "google.com."
    assert events[0]["qanswer"] == "123.0.0.1"
    assert events[0]["qtype"] == "A"
    assert events[0]["event_type"] == "DNS"


def test_single_dns_query_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / UDP(sport=80, dport=53)
        / DNS(rd=1, qd=DNSQR(qtype="A", qname="google.com"))
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["sport"] == 80
    assert events[0]["dport"] == 53
    assert events[0]["qname"] == "google.com."
    assert events[0]["qtype"] == "A"

    assert events[0]["event_type"] == "DNS"


def test_single_http_packet():

    packets = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / TCP(sport=12345, dport=80)
        / HTTP()
        / HTTPRequest(Method="GET", Path="/foo", Host="https://google.com")
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 1

    assert events[0]["src_mac"] == "ab:ab:ab:ab:ab:ab"
    assert events[0]["dst_mac"] == "12:12:12:12:12:12"
    assert events[0]["src_ip"] == "127.0.0.1"
    assert events[0]["dst_ip"] == "192.168.1.1"
    assert events[0]["sport"] == 12345
    assert events[0]["dport"] == 80
    assert events[0]["http_method"] == "GET"
    assert events[0]["uri"] == "/foo"
    assert events[0]["http_dest"] == "https://google.com"

    assert events[0]["event_type"] == "HTTPRequest"


def test_multiple_packets():
    packets = [
        # HTTP Packet
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / TCP(sport=12345, dport=80)
        / HTTP()
        / HTTPRequest(Method="GET", Path="/foo", Host="https://google.com"),
        # DNS Packet
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / UDP(sport=80, dport=53)
        / DNS(rd=1, qd=DNSQR(qtype="A", qname="google.com"), an=DNSRR(rdata="123.0.0.1")),
        # TCP Packet
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / TCP(sport=80, dport=5355),
    ]

    events = list(packets_to_datasource_events(packets).events())
    assert len(events) == 3

    assert [e["event_type"] for e in events] == ["HTTPRequest", "DNS", "TCP"]
