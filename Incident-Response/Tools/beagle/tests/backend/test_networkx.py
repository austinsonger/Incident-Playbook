import json
from typing import Callable, List

import networkx
import pytest

from beagle.backends.networkx import NetworkX
from beagle.nodes import Process, File


from io import BytesIO

from scapy.all import Ether, PcapWriter, Packet, IP, UDP, TCP, DNS, DNSQR, DNSRR

from scapy.layers.http import HTTPRequest, HTTP

from beagle.datasources.pcap import PCAP


def packets_to_datasource_events(packets: List[Packet]) -> PCAP:
    f = BytesIO()
    PcapWriter(f).write(packets)
    f.seek(0)
    return PCAP(f)  # type: ignore


@pytest.fixture()
def nx() -> Callable[..., NetworkX]:
    def _backend(*args, **kwargs) -> networkx.Graph:
        return NetworkX(*args, consolidate_edges=True, **kwargs).graph()  # type: ignore

    return _backend


def test_one_node(nx):

    node = Process("1", "1", "1", "1", "1", "1")
    G = nx(nodes=[node])
    assert len(G.nodes()) == 1


def test_one_edge(nx):
    proc = Process(process_id=10, process_image="test.exe", command_line="test.exe /c foobar")
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    proc.launched[other_proc].append(timestamp=1)

    G = nx(nodes=[proc, other_proc])

    assert len(G.nodes()) == 2
    assert len(G.edges()) == 1

    u = hash(proc)
    v = hash(other_proc)

    assert networkx.has_path(G, u, v)
    assert "Launched" in G[u][v]
    assert {"timestamp": 1} == G[u][v]["Launched"]["data"][0]


def test_node_updated(nx):
    """After pushing in the first process, the second process which has the
    same hash should cause the command line attribute to update"""
    proc = Process(process_id=10, process_image="test.exe", command_line=None)
    next_proc = Process(process_id=10, process_image="test.exe", command_line="best.exe /c 123456")
    G = nx(nodes=[proc, next_proc])

    in_graph_proc = G.nodes(data=True)[hash(proc)]["data"]

    assert in_graph_proc.command_line == "best.exe /c 123456"
    assert in_graph_proc.process_id == 10
    assert in_graph_proc.process_image == "test.exe"

    # Should only have one node, since both nodes inserted are equal
    assert len(G.nodes()) == 1


def test_edge_has_no_name(nx):
    proc = Process(process_id=10, process_image="test.exe", command_line=None)
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    # append never called
    proc.launched[other_proc]

    # This shouldn't error.
    G = nx(nodes=[proc, other_proc])

    len(G.nodes()) == 2
    len(G.edges()) == 1


def test_empty_graph(nx):
    backend = NetworkX(nodes=[], consolidate_edges=True)
    backend.graph()
    assert backend.is_empty()


def test_from_json_object(nx):
    proc = Process(process_id=10, process_image="test.exe", command_line=None)
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    proc.launched[other_proc]

    G = nx(nodes=[proc, other_proc])

    _json_output = NetworkX.graph_to_json(G)

    assert isinstance(_json_output, dict)

    G2 = NetworkX.from_json(_json_output)

    # Graphs should be equal.
    assert networkx.is_isomorphic(G, G2)


def test_from_json_path(nx, tmpdir):
    proc = Process(process_id=10, process_image="test.exe", command_line=None)
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    proc.launched[other_proc]

    G = nx(nodes=[proc, other_proc])

    _json_output = NetworkX.graph_to_json(G)

    # Save to file
    p = tmpdir.mkdir("networkx").join("data.json")
    p.write(json.dumps(_json_output))

    G2 = NetworkX.from_json(p)

    # Graphs should be equal.
    assert networkx.is_isomorphic(G, G2)


def test_from_json_fails_on_invalid(nx, tmpdir):
    with pytest.raises(ValueError):

        NetworkX.from_json({})
    with pytest.raises(ValueError):

        NetworkX.from_json({"nodes": []})
    with pytest.raises(ValueError):

        NetworkX.from_json({"links": []})


def test_add_nodes_no_overlap(nx):
    proc = Process(process_id=10, process_image="test.exe", command_line="test.exe /c foobar")
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    proc.launched[other_proc].append(timestamp=1)

    backend = NetworkX(consolidate_edges=True, nodes=[proc, other_proc])
    G = backend.graph()

    assert len(G.nodes()) == 2
    assert len(G.edges()) == 1

    # Add in a new pair of nodes.
    proc2 = Process(process_id=4, process_image="malware.exe", command_line="malware.exe /c foobar")
    f = File(file_name="foo", file_path="bar")
    proc2.wrote[f]

    G = backend.add_nodes([proc2, f])

    # Graph grew
    assert len(G.nodes()) == 4
    assert len(G.edges()) == 2


def test_add_node_overlaps_existing(nx):
    proc = Process(process_id=10, process_image="test.exe", command_line="test.exe /c foobar")
    other_proc = Process(process_id=12, process_image="best.exe", command_line="best.exe /c 123456")

    proc.launched[other_proc].append(timestamp=1)

    backend = NetworkX(consolidate_edges=True, nodes=[proc, other_proc])
    G = backend.graph()

    assert len(G.nodes()) == 2
    assert len(G.edges()) == 1

    # Add a new node that *overlaps* an existing node (note - not the same node object.)
    proc2 = Process(process_id=10, process_image="test.exe", command_line="test.exe /c foobar")
    f = File(file_name="foo", file_path="bar")
    proc2.wrote[f]

    G = backend.add_nodes([proc2, f])

    # Graph grew, but only 3 nodes.
    assert len(G.nodes()) == 3
    assert len(G.edges()) == 2

    # Process should have both write and launched edges.

    u = hash(proc2)
    v = hash(other_proc)
    v2 = hash(f)

    assert networkx.has_path(G, u, v)
    assert networkx.has_path(G, u, v2)
    assert "Launched" in G[u][v]
    assert "Wrote" in G[u][v2]


def test_from_datasources():
    packets_1 = [
        Ether(src="ab:ab:ab:ab:ab:ab", dst="12:12:12:12:12:12")
        / IP(src="127.0.0.1", dst="192.168.1.1")
        / TCP(sport=12345, dport=80)
        / HTTP()
        / HTTPRequest(Method="GET", Path="/foo", Host="https://google.com")
    ]

    packets_2 = [
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

    nx = NetworkX.from_datasources(
        [packets_to_datasource_events(packets) for packets in [packets_1, packets_2]]
    )

    # Make the graph
    nx.graph()

    assert not nx.is_empty()
