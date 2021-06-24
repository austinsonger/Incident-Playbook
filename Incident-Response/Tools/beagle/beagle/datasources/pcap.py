import unicodedata
from typing import Generator, cast

from beagle.common import logger
from beagle.datasources.base_datasource import DataSource
from beagle.transformers.pcap_transformer import PCAPTransformer


class PCAP(DataSource):
    """Yields events from a PCAP file.

    Parameters
    ----------
    pcap_file : str
        path to a PCAP file.
    """

    name = "PCAP File"
    transformers = [PCAPTransformer]
    category = "PCAP"

    def __init__(self, pcap_file: str) -> None:

        self.pcap_file = pcap_file
        self._imported_scapy = False

    def metadata(self) -> dict:  # pragma: no cover
        return {"filename": self.pcap_file}

    def _get_rdpcap(self):

        if not self._imported_scapy:
            logger.info("Loading Scapy")
            from scapy.all import rdpcap

            logger.info("Scapy Loaded")

            self._imported_scapy = True

        return rdpcap

    def events(self) -> Generator[dict, None, None]:
        reader = self._get_rdpcap()

        from scapy.all import Ether, IP, TCP, DNS, UDP, Packet
        from scapy.layers.http import HTTPRequest

        logger.info("Reading PCAP File")

        pcap = reader(self.pcap_file)

        layers_data = {
            Ether: {
                "src_mac": lambda layer: layer.fields["src"],
                "dst_mac": lambda layer: layer.fields["dst"],
            },
            IP: {
                "src_ip": lambda layer: layer.fields["src"],
                "dst_ip": lambda layer: layer.fields["dst"],
                # returns protocol as a human readable string.
                "protocol": lambda layer: layer.get_field("proto")
                .i2s[layer.fields["proto"]]
                .upper(),
            },
            UDP: {
                "dport": lambda layer: layer.fields["dport"],
                "sport": lambda layer: layer.fields["sport"],
            },
            TCP: {
                "sport": lambda layer: layer.fields["sport"],
                "dport": lambda layer: layer.fields["dport"],
            },
            DNS: {"dns": self._parse_dns_request},
            HTTPRequest: {
                "http_method": lambda layer: layer.fields["Method"].decode(),
                "uri": lambda layer: layer.fields["Path"].decode(),
                "http_dest": lambda layer: layer.fields.get("Host", b"").decode(),
            },
        }

        packet_type = "Ether"
        for packet in pcap:

            packet = cast(Packet, packet)

            payload = packet.build()
            if packet.haslayer(IP):
                payload = packet[IP].build()

            packet_data = {
                "payload": "".join(
                    c
                    for c in payload.decode(encoding="ascii", errors="ignore").replace(
                        "\x00", "."
                    )  # replace null bytes
                    # Remove unicode control characters
                    if unicodedata.category(c) not in {"Cc", "Cf", "Cs", "Co", "Cn"}
                ),
                "timestamp": int(packet.time),
            }

            for layer_name, config in layers_data.items():

                if not packet.haslayer(layer_name):
                    continue

                packet_type = layer_name.__name__

                layer = packet[layer_name]

                for name, processor in config.items():

                    output = processor(layer)

                    # Allows the processor to output multiple values.
                    if isinstance(output, dict):
                        packet_data.update(output)
                    else:
                        packet_data[name] = output

            packet_data["event_type"] = packet_type

            yield packet_data

    def _parse_dns_request(self, dns_layer) -> dict:
        from scapy.layers.dns import DNS, DNSRR

        dns_layer = cast(DNS, dns_layer)

        # Each DNS request has the basic qname/qtype
        dns_data = {
            "qname": dns_layer.qd.qname.decode(),
            # Get 'A/MX/NS' as string rather than number.
            "qtype": dns_layer.qd.get_field("qtype").i2repr(dns_layer.qd, dns_layer.qd.qtype),
        }

        if dns_layer.ancount > 0 and isinstance(dns_layer.an, DNSRR):
            resp = dns_layer.an.rdata
            if isinstance(resp, bytes):
                resp = resp.decode()
            dns_data["qanswer"] = resp
        return dns_data
