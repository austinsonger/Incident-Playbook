- Anomalous DNS traffic and activity, unexpected DNS resolution servers, unauthorized DNS zone transfers, data exfiltration through DNS, and changes to host files
- Remote Desktop Protocol (RDP), virtual private network (VPN) sessions, SSH terminal connections, and other remote abilities to evaluate for inbound connections, unapproved third-party tools, cleartext information, and unauthorized lateral movement
- Uniform Resource Identifier (URI) strings, user agent strings, and proxy enforcement actions for abusive, suspicious, or malicious website access
- Hypertext Transfer Protocol Secure/Secure Sockets Layer (HTTPS/SSL)
- Unauthorized connections to known threat indicators
- Telnet
- Internet Relay Chat (IRC)
- File Transfer Protocol (FTP)

#### **Information to Review for Network Analysis**

- Look for new connections on previously unused ports.
- Look for traffic patterns related to time, frequency, and byte count of the connections.
- Preserve proxy logs. Add in the URI parameters to the event log if possible.
- Disable LLMNR on the corporate network; if unable to disable, collect LLMNR (UDP port 5355) and NetBIOS-NS (UDP port 137).
- Review changes to routing tables, such as weighting, static entries, gateways, and peer relationships.