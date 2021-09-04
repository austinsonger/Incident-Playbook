

| error         | severity | loglevel     | description                                                  |
| :------------ | :------- | :----------- | ------------------------------------------------------------ |
| ASA-1-101001  | 1        | Alert        | (Primary) Failover cable OK.                                 |
| ASA-1-101002  | 1        | Alert        | (Primary) Bad failover cable.                                |
| ASA-1-101003  | 1        | Alert        | (Primary) Failover cable not connected (this unit).          |
| ASA-1-101004  | 1        | Alert        | (Primary) Failover cable not connected (other unit).         |
| ASA-1-101005  | 1        | Alert        | (Primary) Error reading failover cable status.               |
| ASA-1-103001  | 1        | Alert        | (Primary) No response from other firewall (reason code = code). |
| ASA-1-103002  | 1        | Alert        | (Primary) Other firewall network interface interface_number OK. |
| ASA-1-103003  | 1        | Alert        | (Primary) Other firewall network interface interface_number failed. |
| ASA-1-103004  | 1        | Alert        | (Primary) Other firewall reports this firewall failed. Reason: reason-string. |
| ASA-1-103005  | 1        | Alert        | (Primary) Other firewall reporting failure. Reason: SSM card failure. |
| ASA-1-103006  | 1        | Alert        | (Primary\|Secondary) Mate version ver_num is not compatible with ours ver_num. |
| ASA-1-103007  | 1        | Alert        | (Primary\|Secondary) Mate version ver_num is not identical with ours ver_num%ASA-1-104001: (Primary) Switching to ACTIVE (cause: string). |
| ASA-1-103008  | 1        | Alert        | Mate hwdib index is not compatible.                          |
| ASA-1-104002  | 1        | Alert        | (Primary) Switching to STANDBY (cause: string).              |
| ASA-1-104003  | 1        | Alert        | (Primary) Switching to FAILED.                               |
| ASA-1-104004  | 1        | Alert        | (Primary) Switching to OK.                                   |
| ASA-1-104501  | 1        | Alert        | (Primary\|Secondary) Switching to ACTIVE OR Switching to BACKUP (cause: reason) |
| ASA-1-104502  | 1        | Alert        | (Primary\|Secondary) Becoming Backup unit failed             |
| ASA-1-105001  | 1        | Alert        | (Primary) Disabling failover.                                |
| ASA-1-105002  | 1        | Alert        | (Primary) Enabling failover.                                 |
| ASA-1-105003  | 1        | Alert        | (Primary) Monitoring on interface interface_name waiting     |
| ASA-1-105004  | 1        | Alert        | (Primary) Monitoring on interface interface_name normal      |
| ASA-1-105005  | 1        | Alert        | (Primary) Lost Failover communications with mate on interface interface_name. |
| ASA-1-105006  | 1        | Alert        | (Primary) Link status Up on interface interface_name.        |
| ASA-1-105007  | 1        | Alert        | (Primary) Link status Down on interface interface_name.      |
| ASA-1-105008  | 1        | Alert        | (Primary) Testing interface interface_name.                  |
| ASA-1-105009  | 1        | Alert        | (Primary) Testing on interface interface_name {Passed\|Failed}. |
| ASA-1-105011  | 1        | Alert        | (Primary) Failover cable communication failure               |
| ASA-1-105020  | 1        | Alert        | (Primary) Incomplete/slow config replication                 |
| ASA-1-105021  | 1        | Alert        | (failover_unit) Standby unit failed to sync due to a locked context_name config. Lock held by lock_owner_name. |
| ASA-1-105031  | 1        | Alert        | Failover LAN interface is up.                                |
| ASA-1-105032  | 1        | Alert        | LAN Failover interface is down.                              |
| ASA-1-105033  | 1        | Alert        | LAN FO cmd Iface down and up again.                          |
| ASA-1-105034  | 1        | Alert        | Receive a LAN_FAILOVER_UP message from peer.                 |
| ASA-1-105035  | 1        | Alert        | Receive a LAN failover interface down msg from peer.         |
| ASA-1-105036  | 1        | Alert        | dropped a LAN Failover command message.                      |
| ASA-1-105037  | 1        | Alert        | The primary and standby units are switching back and forth as the active unit. |
| ASA-1-105038  | 1        | Alert        | (Primary) Interface count mismatch.                          |
| ASA-1-105039  | 1        | Alert        | (Primary) Unable to verify the Interface count with mate. Failover may be disabled in mate. |
| ASA-1-105040  | 1        | Alert        | (Primary) Mate failover version is not compatible.           |
| ASA-1-105041  | 1        | Alert        | cmd failed during sync.                                      |
| ASA-1-105042  | 1        | Alert        | (Primary) Failover interface OK.                             |
| ASA-1-105043  | 1        | Alert        | (Primary) Failover interface failed.                         |
| ASA-1-105044  | 1        | Alert        | (Primary) Mate operational mode mode is not compatible with my mode mode. |
| ASA-1-105045  | 1        | Alert        | (Primary) Mate license (number contexts) is not compatible with my license (number contexts). |
| ASA-1-105046  | 1        | Alert        | (Primary\|Secondary) Mate has a different chassis.           |
| ASA-1-105047  | 1        | Alert        | Mate has a io_card_name1 card in slot slot_number which is different from my io_card_name2 |
| ASA-1-105048  | 1        | Alert        | (unit) Mate’s service module (application) is different from mine (application). |
| ASA-1-105502  | 1        | Alert        | (Primary\|Secondary) Restarting Cloud HA on this unit        |
| ASA-1-106021  | 1        | Alert        | Deny protocol reverse path check from source_address to dest_address on interface interface_name. |
| ASA-1-106022  | 1        | Alert        | Deny protocol connection spoof from source_address to dest_address on interface interface_name. |
| ASA-1-106101  | 1        | Alert        | Number of cached deny-flows for ACL log has reached limit (number). |
| ASA-1-107001  | 1        | Alert        | RIP auth failed from IP_address: version=number              |
| ASA-1-107002  | 1        | Alert        | RIP pkt failed from IP_address: version=number on interface interface_name. |
| ASA-1-111111  | 1        | Alert        | error_message                                                |
| ASA-1-114001  | 1        | Alert        | Failed to initialize 4GE SSM I/O card (error error_string).  |
| ASA-1-114002  | 1        | Alert        | Failed to initialize SFP in 4GE SSM I/O card (error error_string). |
| ASA-1-114003  | 1        | Alert        | Failed to run cached commands in 4GE SSM I/O card (error error_string). |
| ASA-1-1199012 | 1        | Alert        | Stack smash during new_stack_call in process/fiber process/fiber |
| ASA-1-199010  | 1        | Alert        | Signal 11 caught in process/fiber(rtcli async executor process)/(rtcli async executor) at address 0xf132e03b |
| ASA-1-199021  | 1        | Alert        | System memory utilization has reached the configured watchdog trigger level of Y%. System will now reload. |
| ASA-1-211004  | 1        | Alert        | WARNING: Minimum Memory Requirement for ASA version ver not met for ASA image. min MB required |
| ASA-1-216005  | 1        | Alert        | ERROR: Duplex-mismatch on interface_name resulted in transmitter lockup. A soft reset of the switch was performed. |
| ASA-1-323006  | 1        | Alert        | Module ips experienced a data channel communication failure  |
| ASA-1-332004  | 1        | Alert        | Web Cache IP_address/service_ID lost.                        |
| ASA-1-413007  | 1        | Alert        | An unsupported ASA and IPS configuration is installed. mpc_description with ips_description is not supported. |
| ASA-1-413008  | 1        | Alert        | There was a backplane PCI communications failure with module module_description_string in slot slot_num. |
| ASA-1-505011  | 1        | Alert        | Module ips data channel communication is UP.                 |
| ASA-1-505014  | 1        | Alert        | Module module_id                                             |
| ASA-1-505015  | 1        | Alert        | Module module_id                                             |
| ASA-1-709003  | 1        | Alert        | (Primary) Beginning configuration replication: Sending to mate. |
| ASA-1-709004  | 1        | Alert        | (Primary) End Configuration Replication (ACT).               |
| ASA-1-709005  | 1        | Alert        | (Primary) Beginning configuration replication: Receiving from mate. |
| ASA-1-709006  | 1        | Alert        | (Primary) End Configuration Replication (STB).               |
| ASA-1-713900  | 1        | Alert        | Descriptive_event_string.                                    |
| ASA-1-716507  | 1        | Alert        | Fiber scheduler has reached unreachable code. Cannot continue |
| ASA-1-716508  | 1        | Alert        | internal error in: function: Fiber scheduler is scheduling rotten fiber. Cannot continuing terminating. |
| ASA-1-716509  | 1        | Alert        | internal error in: function: Fiber scheduler is scheduling alien fiber. Cannot continue terminating. |
| ASA-1-716510  | 1        | Alert        | internal error in: function: Fiber scheduler is scheduling finished fiber. Cannot continue terminating. |
| ASA-1-716516  | 1        | Alert        | internal error in: function: OCCAM has corrupted ROL array. Cannot continue terminating. |
| ASA-1-716519  | 1        | Alert        | internal error in: function: OCCAM has corrupted pool list. Cannot continue terminating. |
| ASA-1-716528  | 1        | Alert        | Unexpected fiber scheduler error; possible out-of-memory condition. |
| ASA-1-717049  | 1        | Alert        | Local CA Server certificate is due to expire in number days and a replacement certificate is available for export. |
| ASA-1-717054  | 1        | Alert        | The type certificate in the trustpoint tp name is due to expire in number days. Expiration date and time Subject Name subject name Issuer Name issuer name Serial Number serial number. |
| ASA-1-717055  | 1        | Alert        | The type certificate in the trustpoint tp name has expired. Expiration date and time Subject Name subject name Issuer Name issuer name Serial Number serial number. |
| ASA-1-735001  | 1        | Alert        | Cooling Fan var1: OK.                                        |
| ASA-1-735002  | 1        | Alert        | Cooling Fan var1: Failure Detected.                          |
| ASA-1-735003  | 1        | Alert        | Power Supply var1: OK.                                       |
| ASA-1-735004  | 1        | Alert        | Power Supply var1: Failure Detected.                         |
| ASA-1-735005  | 1        | Alert        | Power Supply Unit Redundancy OK.                             |
| ASA-1-735006  | 1        | Alert        | Power Supply Unit Redundancy Lost.                           |
| ASA-1-735007  | 1        | Alert        | Temp: var2 var3                                              |
| ASA-1-735008  | 1        | Alert        | Chassis Ambient var1: Temp: var2 var3                        |
| ASA-1-735011  | 1        | Alert        | Power Supply var1: Fan OK.                                   |
| ASA-1-735012  | 1        | Alert        | Power Supply var1: Fan Failure Detected.                     |
| ASA-1-735013  | 1        | Alert        | Voltage Channel var1: Voltage OK.                            |
| ASA-1-735014  | 1        | Alert        | Voltage Channel var1: Voltage Critical.                      |
| ASA-1-735017  | 1        | Alert        | Power Supply var1: Temp: var2 var3                           |
| ASA-1-735020  | 1        | Alert        | CPU var1: Temp: var2 var3 OK.                                |
| ASA-1-735021  | 1        | Alert        | Chassis var1: Temp: var2 var3 OK.                            |
| ASA-1-735022  | 1        | Alert        | CPU# is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the CPU. |
| ASA-1-735024  | 1        | Alert        | IO Hub var1: Temp: var2 var3                                 |
| ASA-1-735025  | 1        | Alert        | IO Hub var1: Temp: var2 var3                                 |
| ASA-1-735027  | 1        | Alert        | CPU cpu_num Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues. |
| ASA-1-735029  | 1        | Alert        | IO Hub is running beyond the max thermal operating temperature and the device will be shutting down immediately to prevent permanent damage to the circuit. |
| ASA-1-743000  | 1        | Alert        | The PCI device with vendor ID: vendor_id device ID: device_id located at bus:device.function bus_num:dev_num |
| ASA-1-743001  | 1        | Alert        | Backplane health monitoring detected link failure.           |
| ASA-1-743002  | 1        | Alert        | Backplane health monitoring detected link OK.                |
| ASA-1-743004  | 1        | Alert        | System is not fully operational - PCI device with vendor ID vendor_id (vendor_name) |
| ASA-1-770002  | 1        | Alert        | Resource resource allocation is more than the permitted limit for this platform. ASA will be rebooted. |
| ASA-2-105506  | 2        | Critical     | (Primary\|Secondary) Unable to create socket on port port for (failover connection \| load balancer probes) |
| ASA-2-105507  | 2        | Critical     | (Primary\|Secondary) Unable to bind socket on port port for (failover connection \| load balancer probes) |
| ASA-2-105508  | 2        | Critical     | (Primary\|Secondary) Error creating failover connection socket on port port |
| ASA-2-105525  | 2        | Critical     | (Primary\|Secondary) Incomplete configuration to initiate access token change request |
| ASA-2-105526  | 2        | Critical     | (Primary\|Secondary) Unexpected status in response to access token request: status_string |
| ASA-2-105527  | 2        | Critical     | (Primary\|Secondary) Failure reading response to access token request |
| ASA-2-105528  | 2        | Critical     | (Primary\|Secondary) No access token in response to access token request |
| ASA-2-105529  | 2        | Critical     | (Primary\|Secondary) Error creating authentication header from access token |
| ASA-2-105530  | 2        | Critical     | (Primary\|Secondary) No response to access token request url |
| ASA-2-105531  | 2        | Critical     | (Primary\|Secondary) Failed to obtain route-table information needed for change request for route-table route_table_name |
| ASA-2-105532  | 2        | Critical     | (Primary\|Secondary) Unexpected status in response to route-table change request for route-table route_table_name: status_string |
| ASA-2-105533  | 2        | Critical     | (Primary\|Secondary) Failure reading response to route-table change request for route-table route_table_name |
| ASA-2-105534  | 2        | Critical     | (Primary\|Secondary) No provisioning state in response to route-table change request route-table route_table_name |
| ASA-2-105535  | 2        | Critical     | (Primary\|Secondary) No response to route-table change request for route-table route_table_name from url |
| ASA-2-105536  | 2        | Critical     | (Primary\|Secondary) Failed to obtain Azure authentication header for route status request for route route_name |
| ASA-2-105537  | 2        | Critical     | (Primary\|Secondary) Unexpected status in response to route state request for route route_name: status_string |
| ASA-2-105538  | 2        | Critical     | (Primary\|Secondary) Failure reading response to route state request for route route_name |
| ASA-2-105539  | 2        | Critical     | (Primary\|Secondary) No response to route state request for route route_name from url |
| ASA-2-105540  | 2        | Critical     | (Primary\|Secondary) No route-tables configured              |
| ASA-2-105541  | 2        | Critical     | (Primary\|Secondary) Failed to update route-table route_table_name |
| ASA-2-105544  | 2        | Critical     | (Primary\|Secondary) Error creating load balancer probe socket on port port |
| ASA-2-106001  | 2        | Critical     | Inbound TCP connection denied from IP_address/port to IP_address/port flags tcp_flags on interface interface_name |
| ASA-2-106002  | 2        | Critical     | protocol Connection denied by outbound list acl_ID src inside_address dest outside_address |
| ASA-2-106006  | 2        | Critical     | Deny inbound UDP from outside_address/outside_port to inside_address/inside_port on interface interface_name. |
| ASA-2-106007  | 2        | Critical     | Deny inbound UDP from outside_address/outside_port to inside_address/inside_port due to DNS {Response\|Query}. |
| ASA-2-106013  | 2        | Critical     | Dropping echo request from IP_address to PAT address IP_address |
| ASA-2-106016  | 2        | Critical     | Deny IP spoof from (IP_address) to IP_address on interface interface_name. |
| ASA-2-106017  | 2        | Critical     | Deny IP due to Land Attack from IP_address to IP_address     |
| ASA-2-106018  | 2        | Critical     | ICMP packet type ICMP_type denied by outbound list acl_ID src inside_address dest outside_address |
| ASA-2-106020  | 2        | Critical     | Deny IP teardrop fragment (size = number                     |
| ASA-2-106024  | 2        | Critical     | Access rules memory exhausted                                |
| ASA-2-108002  | 2        | Critical     | SMTP replaced string: out source_address in inside_address data: string |
| ASA-2-108003  | 2        | Critical     | Terminating ESMTP/SMTP connection; malicious pattern detected in the mail address from source_interface:source_address/source_port to dest_interface:dest_address/dset_port. Data:string |
| ASA-2-109011  | 2        | Critical     | Authen Session Start: user 'user'                            |
| ASA-2-112001  | 2        | Critical     | (string:dec) Clear complete.                                 |
| ASA-2-113022  | 2        | Critical     | AAA Marking RADIUS server servername in aaa-server group AAA-Using-DNS as FAILED |
| ASA-2-113023  | 2        | Critical     | AAA Marking protocol server ip-addr in server group tag as ACTIVE |
| ASA-2-113027  | 2        | Critical     | Username could not be found in certificate                   |
| ASA-2-115000  | 2        | Critical     | Critical assertion in process: process name fiber: fiber name |
| ASA-2-199011  | 2        | Critical     | Close on bad channel in process/fiber process/fiber          |
| ASA-2-199014  | 2        | Critical     | syslog                                                       |
| ASA-2-199020  | 2        | Critical     | System memory utilization has reached X%. System will reload if memory usage reaches the configured trigger level of Y%. |
| ASA-2-201003  | 2        | Critical     | Embryonic limit exceeded nconns/elimit for outside_address/outside_port (global_address) inside_address/inside_port on interface interface_name |
| ASA-2-214001  | 2        | Critical     | Terminating manager session from IP_address on interface interface_name. Reason: incoming encrypted data (number bytes) longer than number bytes |
| ASA-2-215001  | 2        | Critical     | Bad route_compress() call                                    |
| ASA-2-217001  | 2        | Critical     | No memory for string in string                               |
| ASA-2-218001  | 2        | Critical     | Failed Identification Test in slot# [fail#/res].             |
| ASA-2-218002  | 2        | Critical     | Module (slot#) is a registered proto-type for Cisco Lab use only |
| ASA-2-218003  | 2        | Critical     | Module Version in slot# is obsolete. The module in slot = slot# is obsolete and must be returned via RMA to Cisco Manufacturing. If it is a lab unit |
| ASA-2-218004  | 2        | Critical     | Failed Identification Test in slot# [fail#/res]              |
| ASA-2-218005  | 2        | Critical     | Inconsistency detected in the system information programmed in non-volatile memory |
| ASA-2-304007  | 2        | Critical     | URL Server IP_address not responding                         |
| ASA-2-304008  | 2        | Critical     | LEAVING ALLOW mode                                           |
| ASA-2-321005  | 2        | Critical     | System CPU utilization reached utilization %                 |
| ASA-2-321006  | 2        | Critical     | System memory usage reached utilization %                    |
| ASA-2-410002  | 2        | Critical     | Dropped num DNS responses with mis-matched id in the past sec second(s): from src_ifc:sip/sport to dest_ifc:dip/dport |
| ASA-2-444004  | 2        | Critical     | Temporary license key key has expired. Applying permanent license key permkey |
| ASA-2-444007  | 2        | Critical     | Timebased activation key activation-key has expired. Reverting to [permanent \| timebased] license key. The following features will be affected: feature |
| ASA-2-444009  | 2        | Critical     | %s license has expired 30 days ago. The system will now reload. |
| ASA-2-444102  | 2        | Critical     | Shared license service inactive. License server is not responding |
| ASA-2-444105  | 2        | Critical     | Released value shared licensetype license(s). License server has been unreachable for 24 hours |
| ASA-2-444111  | 2        | Critical     | Shared license backup service has been terminated due to the primary license server address being unavailable for more than days days. The license server needs to be brought back online to continue using shared licensing. |
| ASA-2-709007  | 2        | Critical     | Configuration replication failed for command command         |
| ASA-2-713078  | 2        | Critical     | Temp buffer for building mode config attributes exceeded: bufsize available_size |
| ASA-2-713176  | 2        | Critical     | Device_type memory resources are critical                    |
| ASA-2-713901  | 2        | Critical     | Descriptive_text_string.                                     |
| ASA-2-716500  | 2        | Critical     | internal error in: function: Fiber library cannot locate AK47 instance |
| ASA-2-716501  | 2        | Critical     | internal error in: function: Fiber library cannot attach AK47 instance |
| ASA-2-716502  | 2        | Critical     | internal error in: function: Fiber library cannot allocate default arena |
| ASA-2-716503  | 2        | Critical     | internal error in: function: Fiber library cannot allocate fiber descriptors pool |
| ASA-2-716504  | 2        | Critical     | internal error in: function: Fiber library cannot allocate fiber stacks pool |
| ASA-2-716505  | 2        | Critical     | internal error in: function: Fiber has joined fiber in unfinished state |
| ASA-2-716506  | 2        | Critical     | UNICORN_SYSLOGID_JOINED_UNEXPECTED_FIBER                     |
| ASA-2-716512  | 2        | Critical     | internal error in: function: Fiber has joined fiber waited upon by someone else |
| ASA-2-716513  | 2        | Critical     | internal error in: function: Fiber in callback blocked on other channel |
| ASA-2-716515  | 2        | Critical     | internal error in: function: OCCAM failed to allocate memory for AK47 instance |
| ASA-2-716517  | 2        | Critical     | internal error in: function: OCCAM cached block has no associated arena |
| ASA-2-716520  | 2        | Critical     | internal error in: function: OCCAM pool has no block list    |
| ASA-2-716521  | 2        | Critical     | internal error in: function: OCCAM no realloc allowed in named pool |
| ASA-2-716522  | 2        | Critical     | internal error in: function: OCCAM corrupted standalone block |
| ASA-2-716525  | 2        | Critical     | UNICORN_SYSLOGID_SAL_CLOSE_PRIVDATA_CHANGED                  |
| ASA-2-716526  | 2        | Critical     | UNICORN_SYSLOGID_PERM_STORAGE_SERVER_LOAD_FAIL               |
| ASA-2-716527  | 2        | Critical     | UNICORN_SYSLOGID_PERM_STORAGE_SERVER_STORE_FAI               |
| ASA-2-717008  | 2        | Critical     | Insufficient memory to process_requiring_memory.             |
| ASA-2-717011  | 2        | Critical     | Unexpected event event event_ID                              |
| ASA-2-717040  | 2        | Critical     | Local CA Server has failed and is being disabled. Reason: reason. |
| ASA-2-735009  | 2        | Critical     | IPMI: Environment Monitoring has failed initialization and configuration. Environment Monitoring is not running. |
| ASA-2-735023  | 2        | Critical     | ASA was previously shutdown due to the CPU complex running beyond the maximum thermal operating temperature. The chassis needs to be inspected immediately for ventilation issues. |
| ASA-2-735028  | 2        | Critical     | ASA was previously shutdown due to a CPU Voltage Regulator running beyond the max thermal operating temperature. The chassis and CPU need to be inspected immediately for ventilation issues. |
| ASA-2-736001  | 2        | Critical     | Unable to allocate enough memory at boot for jumbo-frame reservation. Jumbo-frame support has been disabled. |
| ASA-2-747009  | 2        | Critical     | Clustering: Fatal error due to failure to create RPC server for module module name. |
| ASA-2-747011  | 2        | Critical     | Clustering: Memory allocation error.%ASA-2-752001: Tunnel Manager received invalid parameter to remove record. |
| ASA-2-748007  | 2        | Critical     | Failed to de-bundle the ports for module slot_number in chassis chassis_number; traffic may be black holed |
| ASA-2-752001  | 2        | Critical     | Tunnel Manager received invalid parameter to remove record.  |
| ASA-2-752005  | 2        | Critical     | Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Memory may be low. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-2-772003  | 2        | Critical     | PASSWORD: session login failed                               |
| ASA-2-772006  | 2        | Critical     | REAUTH: user username failed authentication                  |
| ASA-2-774001  | 2        | Critical     | POST: unspecified error                                      |
| ASA-2-774002  | 2        | Critical     | POST: error err                                              |
| ASA-2-775007  | 2        | Critical     | Scansafe: Primary server_interface_name:server_ip_address and backup server_interface_name:server_ip_address servers are not reachable. |
| ASA-3-105010  | 3        | Error        | (Primary) Failover message block alloc failed                |
| ASA-3-105050  | 3        | Error        | ASAv ethernet interface mismatch                             |
| ASA-3-105509  | 3        | Error        | (Primary\|Secondary) Error sending message_name message to peer unit peer-ip |
| ASA-3-105510  | 3        | Error        | (Primary\|Secondary) Error receiving message from peer unit peer-ip |
| ASA-3-105511  | 3        | Error        | (Primary\|Secondary) Incomplete read of message header of message from peer unit peer-ip: bytes bytes read of expected header_length header bytes |
| ASA-3-105512  | 3        | Error        | (Primary\|Secondary) Error receiving message body of message from peer unit peer-ip |
| ASA-3-105513  | 3        | Error        | (Primary\|Secondary) Incomplete read of message body of message from peer unit peer-ip: bytes bytes read of expected message_length message body bytes |
| ASA-3-105514  | 3        | Error        | (Primary\|Secondary) Error occurred when responding to message_name message received from peer unit peer-ip |
| ASA-3-105515  | 3        | Error        | (Primary\|Secondary) Error receiving message_name message from peer unit peer-ip |
| ASA-3-105516  | 3        | Error        | (Primary\|Secondary) Incomplete read of message header of message_name message from peer unit peer-ip: bytes bytes read of expected header_length header bytes |
| ASA-3-105517  | 3        | Error        | (Primary\|Secondary) Error receiving message body of message_name message from peer unit peer-ip |
| ASA-3-105518  | 3        | Error        | (Primary\|Secondary) Incomplete read of message body of message_name message from peer unit peer-ip: bytes bytes read of expected message_length message body bytes |
| ASA-3-105519  | 3        | Error        | (Primary\|Secondary) Invalid response to message_name message received from peer unit peer-ip: type message_type |
| ASA-3-105545  | 3        | Error        | (Primary\|Secondary) Error starting load balancer probe socket on port port |
| ASA-3-105546  | 3        | Error        | (Primary\|Secondary) Error starting load balancer probe handler |
| ASA-3-105547  | 3        | Error        | (Primary\|Secondary) Error generating encryption key for Azure secret key |
| ASA-3-105548  | 3        | Error        | (Primary\|Secondary) Error storing encryption key for Azure secret key |
| ASA-3-105549  | 3        | Error        | (Primary\|Secondary) Error retrieving encryption key for Azure secret key |
| ASA-3-105550  | 3        | Error        | (Primary\|Secondary) Error encrypting Azure secret key       |
| ASA-3-105551  | 3        | Error        | (Primary\|Secondary) Error encrypting Azure secret key       |
| ASA-3-106010  | 3        | Error        | Deny inbound protocol src [interface_name: source_address/source_port] [([idfw_user \| FQDN_string] |
| ASA-3-106011  | 3        | Error        | Deny inbound (No xlate) string                               |
| ASA-3-106014  | 3        | Error        | Deny inbound icmp src interface_name: IP_address [([idfw_user \| FQDN_string] |
| ASA-3-109010  | 3        | Error        | Auth from inside_address/inside_port to outside_address/outside_port failed (too many pending auths) on interface interface_name. |
| ASA-3-109013  | 3        | Error        | User must authenticate before using this service             |
| ASA-3-109016  | 3        | Error        | Can't find authorization ACL acl_ID for user 'user'          |
| ASA-3-109018  | 3        | Error        | Downloaded ACL acl_ID is empty                               |
| ASA-3-109019  | 3        | Error        | Downloaded ACL acl_ID has parsing error; ACE string          |
| ASA-3-109020  | 3        | Error        | Downloaded ACL has config error; ACE                         |
| ASA-3-109023  | 3        | Error        | User from source_address/source_port to dest_address/dest_port on interface outside_interface must authenticate before using this service. |
| ASA-3-109026  | 3        | Error        | [aaa protocol] Invalid reply digest received; shared server key may be mismatched. |
| ASA-3-109032  | 3        | Error        | Unable to install ACL access_list                            |
| ASA-3-109035  | 3        | Error        | Exceeded maximum number (<max_num>) of DAP attribute instances for user <user> |
| ASA-3-109037  | 3        | Error        | Exceeded 5000 attribute values for the attribute name attribute for user username |
| ASA-3-109038  | 3        | Error        | Attribute internal-attribute-name value string-from-server from AAA server could not be parsed as a type internal-attribute-name string representation of the attribute name |
| ASA-3-109103  | 3        | Error        | CoA action-type from coa-source-ip failed for user username  |
| ASA-3-109104  | 3        | Error        | CoA action-type from coa-source-ip failed for user username  |
| ASA-3-109105  | 3        | Error        | Failed to determine the egress interface for locally generated traffic destined to <protocol> <IP>:<port> |
| ASA-3-113001  | 3        | Error        | Unable to open AAA session. Session limit [limit] reached.   |
| ASA-3-113018  | 3        | Error        | User: user                                                   |
| ASA-3-113020  | 3        | Error        | Kerberos error: Clock skew with server ip_address greater than 300 seconds |
| ASA-3-113021  | 3        | Error        | Attempted console login failed. User username did NOT have appropriate Admin Rights. |
| ASA-3-114006  | 3        | Error        | Failed to get port statistics in 4GE SSM I/O card (error error_string). |
| ASA-3-114007  | 3        | Error        | Failed to get current msr in 4GE SSM I/O card (error error_string). |
| ASA-3-114008  | 3        | Error        | Failed to enable port after link is up in 4GE SSM I/O card due to either I2C serial bus access error or switch access error. |
| ASA-3-114009  | 3        | Error        | Failed to set multicast address in 4GE SSM I/O card (error error_string). |
| ASA-3-114010  | 3        | Error        | Failed to set multicast hardware address in 4GE SSM I/O card (error error_string). |
| ASA-3-114011  | 3        | Error        | Failed to delete multicast address in 4GE SSM I/O card (error error_string). |
| ASA-3-114012  | 3        | Error        | Failed to delete multicast hardware address in 4GE SSM I/O card (error error_string). |
| ASA-3-114013  | 3        | Error        | Failed to set mac address table in 4GE SSM I/O card (error error_string). |
| ASA-3-114014  | 3        | Error        | Failed to set mac address in 4GE SSM I/O card (error error_string). |
| ASA-3-114015  | 3        | Error        | Failed to set mode in 4GE SSM I/O card (error error_string). |
| ASA-3-114016  | 3        | Error        | Failed to set multicast mode in 4GE SSM I/O card (error error_string). |
| ASA-3-114017  | 3        | Error        | Failed to get link status in 4GE SSM I/O card (error error_string). |
| ASA-3-114018  | 3        | Error        | Failed to set port speed in 4GE SSM I/O card (error error_string). |
| ASA-3-114019  | 3        | Error        | Failed to set media type in 4GE SSM I/O card (error error_string). |
| ASA-3-114020  | 3        | Error        | Port link speed is unknown in 4GE SSM I/O card.              |
| ASA-3-114021  | 3        | Error        | Failed to set multicast address table in 4GE SSM I/O card due to error. |
| ASA-3-114022  | 3        | Error        | Failed to pass broadcast traffic in 4GE SSM I/O card due to error_string |
| ASA-3-114023  | 3        | Error        | Failed to cache/flush mac table in 4GE SSM I/O card due to error_string. |
| ASA-3-115001  | 3        | Error        | Error in process: process name fiber: fiber name             |
| ASA-3-120010  | 3        | Error        | Notify command command to SCH client client failed. Reason reason. |
| ASA-3-199015  | 3        | Error        | syslog                                                       |
| ASA-3-201002  | 3        | Error        | Too many TCP connections on {static\|xlate} global_address! econns nconns |
| ASA-3-201004  | 3        | Error        | Too many UDP connections on {static\|xlate} global_address! udp connections limit |
| ASA-3-201005  | 3        | Error        | FTP data connection failed for IP_address IP_address         |
| ASA-3-201006  | 3        | Error        | RCMD backconnection failed for IP_address/port.              |
| ASA-3-201008  | 3        | Error        | Disallowing new connections.                                 |
| ASA-3-201009  | 3        | Error        | TCP connection limit of number for host IP_address on interface_name exceeded |
| ASA-3-201011  | 3        | Error        | Connection limit exceeded cnt/limit for dir packet from sip/sport to dip/dport on interface if_name. |
| ASA-3-201013  | 3        | Error        | Per-client connection limit exceeded curr num/limit for [input\|output] packet from ip/port to ip/port on interface interface_name |
| ASA-3-202001  | 3        | Error        | Out of address translation slots!                            |
| ASA-3-202005  | 3        | Error        | Non-embryonic in embryonic list outside_address/outside_port inside_address/inside_port |
| ASA-3-202010  | 3        | Error        | [NAT \| PAT] pool exhausted for pool-name                    |
| ASA-3-202016  | 3        | Error        | %d: Unable to pre-allocate SIP %s secondary channel for message \ from %s:%A/%d to %s:%A/%d with PAT and missing port information. |
| ASA-3-208005  | 3        | Error        | (function:line_num) clear command return code                |
| ASA-3-210001  | 3        | Error        | LU sw_module_name error = number                             |
| ASA-3-210002  | 3        | Error        | LU allocate block (bytes) failed.                            |
| ASA-3-210003  | 3        | Error        | Unknown LU Object number                                     |
| ASA-3-210005  | 3        | Error        | LU allocate secondary(optional) connection failed for protocol[TCP\|UDP] connection from ingress interface name:Real IP Address/Real Port to egress interface name:Real IP Address/Real Port |
| ASA-3-210006  | 3        | Error        | LU look NAT for IP_address failed                            |
| ASA-3-210007  | 3        | Error        | LU allocate xlate failed for type[static \| dynamic]-[NAT \| PAT] secondary(optional) protocol translation from ingress interface name:Real IP Address/real port (Mapped IP Address/Mapped Port) to egress interface name:Real IP Address/Real Port (Mapped IP Address/Mapped Port) |
| ASA-3-210008  | 3        | Error        | LU no xlate for inside_address/inside_port outside_address/outside_port |
| ASA-3-210010  | 3        | Error        | LU make UDP connection for outside_address:outside_port inside_address:inside_port failed |
| ASA-3-210020  | 3        | Error        | LU PAT port port reserve failed                              |
| ASA-3-210021  | 3        | Error        | LU create static xlate global_address ifc interface_name failed |
| ASA-3-211001  | 3        | Error        | Memory allocation Error                                      |
| ASA-3-211003  | 3        | Error        | Error in computed percentage CPU usage value                 |
| ASA-3-212001  | 3        | Error        | Unable to open SNMP channel (UDP port port) on interface interface_number |
| ASA-3-212002  | 3        | Error        | Unable to open SNMP trap channel (UDP port port) on interface interface_number |
| ASA-3-212003  | 3        | Error        | Unable to receive an SNMP request on interface interface_number |
| ASA-3-212004  | 3        | Error        | Unable to send an SNMP response to IP Address IP_address Port port interface interface_number |
| ASA-3-212005  | 3        | Error        | incoming SNMP request (number bytes) on interface interface_name exceeds data buffer size |
| ASA-3-212006  | 3        | Error        | Dropping SNMP request from src_addr/src_port to ifc:dst_addr/dst_port because: reason username. |
| ASA-3-212010  | 3        | Error        | Configuration request for SNMP user %s failed. Host %s reason. |
| ASA-3-212011  | 3        | Error        | SNMP engineBoots is set to maximum value. Reason: %s User intervention necessary. |
| ASA-3-212012  | 3        | Error        | Unable to write SNMP engine data to persistent storage.      |
| ASA-3-213001  | 3        | Error        | PPTP control daemon socket io string                         |
| ASA-3-213002  | 3        | Error        | PPTP tunnel hashtable insert failed                          |
| ASA-3-213003  | 3        | Error        | PPP virtual interface interface_number isn't opened.         |
| ASA-3-213004  | 3        | Error        | PPP virtual interface interface_number client ip allocation failed. |
| ASA-3-213005  | 3        | Error        | Dynamic-Access-Policy action (DAP) action aborted            |
| ASA-3-213006  | 3        | Error        | Unable to read dynamic access policy record.                 |
| ASA-3-216002  | 3        | Error        | Unexpected event (major: major_id                            |
| ASA-3-216003  | 3        | Error        | Unrecognized timer timer_ptr                                 |
| ASA-3-219002  | 3        | Error        | I2C_API_name error                                           |
| ASA-3-302019  | 3        | Error        | H.323 library_name ASN Library failed to initialize          |
| ASA-3-302302  | 3        | Error        | ACL = deny; no sa created                                    |
| ASA-3-304003  | 3        | Error        | URL Server IP_address timed out URL url                      |
| ASA-3-304006  | 3        | Error        | URL Server IP_address not responding                         |
| ASA-3-305005  | 3        | Error        | No translation group found for protocol src interface_name: source_address/source_port [(idfw_user)] dst interface_nam: dest_address/dest_port [(idfw_user)] |
| ASA-3-305006  | 3        | Error        | {outbound static\|identity\|portmap\|regular) translation creation failed for protocol src interface_name:source_address/source_port [(idfw_user)] dst interface_name:dest_address/dest_port [(idfw_user)] |
| ASA-3-305008  | 3        | Error        | Free unallocated global IP address.                          |
| ASA-3-305016  | 3        | Error        | Unable to create protocol connection from real_interface:real_host_ip/real_source_port to real_dest_interface:real_dest_ip/real_dest_port due to reason. |
| ASA-3-313001  | 3        | Error        | Denied ICMP type=number                                      |
| ASA-3-313008  | 3        | Error        | Denied ICMPv6 type=number                                    |
| ASA-3-315004  | 3        | Error        | Fail to establish SSH session because RSA host key retrieval failed. |
| ASA-3-315012  | 3        | Error        | Weak SSH type (alg) provided from client ‘IP’ on interface int. Connection failed. Not FIPS 140-2 compliant |
| ASA-3-316001  | 3        | Error        | Denied new tunnel to IP_address. VPN peer limit (platform_vpn_peer_limit) exceeded |
| ASA-3-316002  | 3        | Error        | VPN Handle error: protocol=protocol                          |
| ASA-3-317001  | 3        | Error        | No memory available for limit_slow                           |
| ASA-3-317002  | 3        | Error        | Bad path index of number for IP_address                      |
| ASA-3-317003  | 3        | Error        | IP routing table creation failure - reason                   |
| ASA-3-317004  | 3        | Error        | IP routing table limit warning                               |
| ASA-3-317005  | 3        | Error        | IP routing table limit exceeded - reason                     |
| ASA-3-317006  | 3        | Error        | Pdb index error pdb                                          |
| ASA-3-317012  | 3        | Error        | Interface IP route counter negative - nameif-string-value    |
| ASA-3-318001  | 3        | Error        | Internal error: reason                                       |
| ASA-3-318002  | 3        | Error        | Flagged as being an ABR without a backbone area              |
| ASA-3-318003  | 3        | Error        | Reached unknown state in neighbor state machine              |
| ASA-3-318004  | 3        | Error        | area string lsid IP_address mask netmask adv IP_address type number |
| ASA-3-318005  | 3        | Error        | lsid ip_address adv IP_address type number gateway gateway_address metric number network IP_address mask netmask protocol hex attr hex net-metric number |
| ASA-3-318006  | 3        | Error        | if interface_name if_state number                            |
| ASA-3-318007  | 3        | Error        | OSPF is enabled on interface_name during idb initialization  |
| ASA-3-318008  | 3        | Error        | OSPF process number is changing router-id. Reconfigure virtual link neighbors with our new router-id |
| ASA-3-318009  | 3        | Error        | OSPF: Attempted reference of stale data encountered in function |
| ASA-3-318101  | 3        | Error        | Internal error: %REASON                                      |
| ASA-3-318102  | 3        | Error        | Flagged as being an ABR without a backbone area T            |
| ASA-3-318103  | 3        | Error        | Reached unknown state in neighbor state machine              |
| ASA-3-318104  | 3        | Error        | DB already exist : area %AREA_ID_STR lsid %i adv %i type 0x%x |
| ASA-3-318105  | 3        | Error        | lsid %i adv %i type 0x%x gateway %i metric %d network %i mask %i protocol %#x attr %#x net-metric %d |
| ASA-3-318106  | 3        | Error        | if %IF_NAME if_state %d                                      |
| ASA-3-318107  | 3        | Error        | OSPF is enabled on %IF_NAME during idb initialization        |
| ASA-3-318108  | 3        | Error        | OSPF process %d is changing router-id. Reconfigure virtual link neighbors with our new router-id |
| ASA-3-318109  | 3        | Error        | OSPFv3 has received an unexpected message: %0x/%0x           |
| ASA-3-318110  | 3        | Error        | Invalid encrypted key %s.                                    |
| ASA-3-318111  | 3        | Error        | SPI %u is already in use with ospf process %d                |
| ASA-3-318112  | 3        | Error        | SPI %u is already in use by a process other than ospf process %d. |
| ASA-3-318113  | 3        | Error        | %s %s is already configured with SPI %u.                     |
| ASA-3-318114  | 3        | Error        | The key length used with SPI %u is not valid                 |
| ASA-3-318115  | 3        | Error        | %s error occurred when attempting to create an IPsec policy for SPI %u |
| ASA-3-318116  | 3        | Error        | SPI %u is not being used by ospf process %d.                 |
| ASA-3-318117  | 3        | Error        | The policy for SPI %u could not be removed because it is in use. |
| ASA-3-318118  | 3        | Error        | %s error occurred when attempting to remove the IPsec policy with SPI %u |
| ASA-3-318119  | 3        | Error        | Unable to close secure socket with SPI %u on interface %s    |
| ASA-3-318120  | 3        | Error        | OSPFv3 was unable to register with IPsec                     |
| ASA-3-318121  | 3        | Error        | IPsec reported a GENERAL ERROR: message %s                   |
| ASA-3-318122  | 3        | Error        | IPsec sent a %s message %s to OSPFv3 for interface %s. Recovery attempt %d . |
| ASA-3-318123  | 3        | Error        | IPsec sent a %s message %s to OSPFv3 for interface %IF_NAME. Recovery aborted |
| ASA-3-318125  | 3        | Error        | Init failed for interface %IF_NAME                           |
| ASA-3-318126  | 3        | Error        | Interface %IF_NAME is attached to more than one area         |
| ASA-3-318127  | 3        | Error        | Could not allocate or find the neighbor                      |
| ASA-3-319001  | 3        | Error        | Acknowledge for arp update for IP address dest_address not received (number). |
| ASA-3-319002  | 3        | Error        | Acknowledge for route update for IP address dest_address not received (number). |
| ASA-3-319003  | 3        | Error        | Arp update for IP address address to NPn failed.             |
| ASA-3-319004  | 3        | Error        | Route update for IP address dest_address failed (number).    |
| ASA-3-320001  | 3        | Error        | The subject name of the peer cert is not allowed for connection |
| ASA-3-321007  | 3        | Error        | System is low on free memory blocks of size block_size (free_blocks CNT out of max_blocks MAX) |
| ASA-3-322001  | 3        | Error        | Deny MAC address MAC_address                                 |
| ASA-3-322002  | 3        | Error        | ARP inspection check failed for arp {request\|response} received from host MAC_address on interface interface. This host is advertising MAC Address MAC_address_1 for IP Address IP_address |
| ASA-3-322003  | 3        | Error        | ARP inspection check failed for arp {request\|response} received from host MAC_address on interface interface. This host is advertising MAC Address MAC_address_1 for IP Address IP_address |
| ASA-3-323001  | 3        | Error        | Module module_id experienced a control channel communications failure. |
| ASA-3-323002  | 3        | Error        | Module module_id is not able to shut down                    |
| ASA-3-323003  | 3        | Error        | Module module_id is not able to reload                       |
| ASA-3-323004  | 3        | Error        | Module module_id failed to write software vnewver (currently vver) |
| ASA-3-323005  | 3        | Error        | Module module_id can not be started completely               |
| ASA-3-323007  | 3        | Error        | Module in slot slot experienced a firmware failure and the recovery is in progress. |
| ASA-3-324000  | 3        | Error        | Drop GTPv version message msg_type from source_interface:source_address/source_port to dest_interface:dest_address/dest_port Reason: reason |
| ASA-3-324001  | 3        | Error        | GTPv0 packet parsing error from source_interface:source_address/source_port to dest_interface:dest_address/dest_port |
| ASA-3-324002  | 3        | Error        | No PDP[MCB] exists to process GTPv0 msg_type from source_interface:source_address/source_port to dest_interface:dest_address/dest_port |
| ASA-3-324003  | 3        | Error        | No matching request to process GTPv version msg_type from source_interface:source_address/source_port to source_interface:dest_address/dest_port |
| ASA-3-324004  | 3        | Error        | GTP packet with version%d from source_interface:source_address/source_port to dest_interface:dest_address/dest_port is not supported |
| ASA-3-324005  | 3        | Error        | Unable to create tunnel from source_interface:source_address/source_port to dest_interface:dest_address/dest_port |
| ASA-3-324006  | 3        | Error        | GSN IP_address tunnel limit tunnel_limit exceeded            |
| ASA-3-324007  | 3        | Error        | Unable to create GTP connection for response from: source_address/0 to dest_address/dest_port |
| ASA-3-324008  | 3        | Error        | No PDP exists to update the data sgsn [ggsn] PDPMCB Info REID: teid_value |
| ASA-3-324300  | 3        | Error        | Radius Accounting Request from from_addr has an incorrect request authenticator |
| ASA-3-324301  | 3        | Error        | Radius Accounting Request has a bad header length hdr_len    |
| ASA-3-325001  | 3        | Error        | Router ipv6_address on interface has conflicting ND (Neighbor Discovery) settings |
| ASA-3-326001  | 3        | Error        | Unexpected error in the timer library: error_message         |
| ASA-3-326002  | 3        | Error        | Error in error_message: error_message                        |
| ASA-3-326004  | 3        | Error        | An internal error occurred while processing a packet queue   |
| ASA-3-326005  | 3        | Error        | Mrib notification failed for (IP_address                     |
| ASA-3-326006  | 3        | Error        | Entry-creation failed for (IP_address                        |
| ASA-3-326007  | 3        | Error        | Entry-update failed for (IP_address                          |
| ASA-3-326008  | 3        | Error        | MRIB registration failed                                     |
| ASA-3-326009  | 3        | Error        | MRIB connection-open failed                                  |
| ASA-3-326010  | 3        | Error        | MRIB unbind failed                                           |
| ASA-3-326011  | 3        | Error        | MRIB table deletion failed                                   |
| ASA-3-326012  | 3        | Error        | Initialization of string functionality failed                |
| ASA-3-326013  | 3        | Error        | Internal error: string in string line %d (%s)                |
| ASA-3-326014  | 3        | Error        | Initialization failed: error_message error_message           |
| ASA-3-326015  | 3        | Error        | Communication error: error_message error_message             |
| ASA-3-326016  | 3        | Error        | Failed to set un-numbered interface for interface_name (string) |
| ASA-3-326017  | 3        | Error        | Interface Manager error - string in string: string           |
| ASA-3-326019  | 3        | Error        | string in string: string                                     |
| ASA-3-326020  | 3        | Error        | List error in string: string                                 |
| ASA-3-326021  | 3        | Error        | Error in string: string                                      |
| ASA-3-326022  | 3        | Error        | Error in string: string                                      |
| ASA-3-326023  | 3        | Error        | string - IP_address: string                                  |
| ASA-3-326024  | 3        | Error        | An internal error occurred while processing a packet queue.  |
| ASA-3-326025  | 3        | Error        | string                                                       |
| ASA-3-326026  | 3        | Error        | Server unexpected error: error_message                       |
| ASA-3-326027  | 3        | Error        | Corrupted update: error_message                              |
| ASA-3-326028  | 3        | Error        | Asynchronous error: error_message                            |
| ASA-3-327001  | 3        | Error        | IP SLA Monitor: Cannot create a new process                  |
| ASA-3-327002  | 3        | Error        | IP SLA Monitor: Failed to initialize                         |
| ASA-3-327003  | 3        | Error        | IP SLA Monitor: Generic Timer wheel timer functionality failed to initialize |
| ASA-3-328001  | 3        | Error        | Attempt made to overwrite a set stub function in string.     |
| ASA-3-329001  | 3        | Error        | The string0 subblock named string1 was not removed           |
| ASA-3-331001  | 3        | Error        | Dynamic DNS Update for 'fqdn_name' = ip_address failed       |
| ASA-3-332001  | 3        | Error        | Unable to open cache discovery socket                        |
| ASA-3-332002  | 3        | Error        | Unable to allocate message buffer                            |
| ASA-3-336001  | 3        | Error        | Route desination_network stuck-in-active state in EIGRP-ddb_name as_num. Cleaning up |
| ASA-3-336002  | 3        | Error        | Handle handle_id is not allocated in pool.                   |
| ASA-3-336003  | 3        | Error        | No buffers available for bytes byte packet                   |
| ASA-3-336004  | 3        | Error        | Negative refcount in pakdesc pakdesc.                        |
| ASA-3-336005  | 3        | Error        | Flow control error                                           |
| ASA-3-336006  | 3        | Error        | num peers exist on IIDB interface_name.                      |
| ASA-3-336007  | 3        | Error        | Anchor count negative                                        |
| ASA-3-336008  | 3        | Error        | Lingering DRDB deleting IIDB                                 |
| ASA-3-336009  | 3        | Error        | Internal Error                                               |
| ASA-3-336012  | 3        | Error        | Interface interface_names going down and neighbor_links links exist |
| ASA-3-336013  | 3        | Error        | Route iproute                                                |
| ASA-3-336014  | 3        | Error        | EIGRP_PDM_Process_name                                       |
| ASA-3-336015  | 3        | Error        | Unable to open socket for AS as_number                       |
| ASA-3-336016  | 3        | Error        | Unknown timer type timer_type expiration                     |
| ASA-3-336018  | 3        | Error        | process_name as_number: prefix_source threshold prefix level (prefix_threshold) reached |
| ASA-3-336019  | 3        | Error        | process_name as_number: prefix_source prefix limit reached (prefix_threshold). |
| ASA-3-338305  | 3        | Error        | Failed to download dynamic filter data file from updater server url |
| ASA-3-338306  | 3        | Error        | Failed to authenticate with dynamic filter updater server url |
| ASA-3-338307  | 3        | Error        | Failed to decrypt downloaded dynamic filter database file    |
| ASA-3-338309  | 3        | Error        | The license on this ASA does not support dynamic filter updater feature. |
| ASA-3-338310  | 3        | Error        | Failed to update from dynamic filter updater server url      |
| ASA-3-339001  | 3        | Error        | DNSCRYPT certificate update failed for <num_tries> tries     |
| ASA-3-339002  | 3        | Error        | Umbrella device registration failed with error code <err_code> |
| ASA-3-339003  | 3        | Error        | Umbrella device registration was successful                  |
| ASA-3-339004  | 3        | Error        | Umbrella device registration failed due to missing token     |
| ASA-3-339005  | 3        | Error        | Umbrella device registration failed after <num_tries> retries |
| ASA-3-340001  | 3        | Error        | Loopback-proxy info: error_string context id context_id      |
| ASA-3-341003  | 3        | Error        | Policy Agent failed to start for VNMC vnmc_ip_addr           |
| ASA-3-341004  | 3        | Error        | Storage device not available: Attempt to shutdown module %s failed. |
| ASA-3-341005  | 3        | Error        | Storage device not available. Shutdown issued for module %s. |
| ASA-3-341006  | 3        | Error        | Storage device not available. Failed to stop recovery of module %s . |
| ASA-3-341007  | 3        | Error        | Storage device not available. Further recovery of module %s was stopped. This may take several minutes to complete. |
| ASA-3-341008  | 3        | Error        | Storage device not found. Auto-boot of module %s cancelled. Install drive and reload to try again. |
| ASA-3-341011  | 3        | Error        | Storage device with serial number ser_no in bay bay_no faulty. |
| ASA-3-342002  | 3        | Error        | REST API Agent failed                                        |
| ASA-3-342003  | 3        | Error        | REST API Agent failure notification received. Agent will be restarted automatically. |
| ASA-3-342004  | 3        | Error        | Failed to automatically restart the REST API Agent after 5 unsuccessful attempts. Use the 'no rest-api agent' and 'rest-api agent' commands to manually restart the Agent. |
| ASA-3-342006  | 3        | Error        | Filed to install REST API image                              |
| ASA-3-342008  | 3        | Error        | <reason>                                                     |
| ASA-3-402140  | 3        | Error        | CRYPTO: RSA key generation error: modulus len len            |
| ASA-3-402141  | 3        | Error        | CRYPTO: Key zeroization error: key set type                  |
| ASA-3-402142  | 3        | Error        | CRYPTO: Bulk data op error: algorithm alg                    |
| ASA-3-402143  | 3        | Error        | CRYPTO: alg type key op                                      |
| ASA-3-402144  | 3        | Error        | CRYPTO: Digital signature error: signature algorithm sig     |
| ASA-3-402145  | 3        | Error        | CRYPTO: Hash generation error: algorithm hash                |
| ASA-3-402146  | 3        | Error        | CRYPTO: Keyed hash generation error: algorithm hash          |
| ASA-3-402147  | 3        | Error        | CRYPTO: HMAC generation error: algorithm alg                 |
| ASA-3-402148  | 3        | Error        | CRYPTO: Random Number Generator error                        |
| ASA-3-402149  | 3        | Error        | CRYPTO: weak encryption type (length). Operation disallowed. Not FIPS 140-2 compliant |
| ASA-3-402150  | 3        | Error        | CRYPTO: Deprecated hash algorithm used for RSA operation (hash alg). Operation disallowed. Not FIPS 140-2 compliant |
| ASA-3-403501  | 3        | Error        | PPPoE - Bad host-unique in PADO - packet dropped. Intf:interface_name AC:ac_name |
| ASA-3-403502  | 3        | Error        | PPPoE - Bad host-unique in PADS - dropping packet. Intf:interface_name AC:ac_name |
| ASA-3-403503  | 3        | Error        | PPPoE:PPP link down:reason                                   |
| ASA-3-403504  | 3        | Error        | PPPoE:No vpdn group group_name for PPPoE is created          |
| ASA-3-403507  | 3        | Error        | PPPoE:PPPoE client on interface interface failed to locate PPPoE vpdn group group_name |
| ASA-3-414001  | 3        | Error        | Failed to save logging buffer using file name filename to FTP server ftp_server_address on interface interface_name: [fail_reason] |
| ASA-3-414002  | 3        | Error        | Failed to save logging buffer to flash:/syslog directory using file name: filename: [fail_reason] |
| ASA-3-414003  | 3        | Error        | TCP Syslog Server intf: IP_Address/port not responding. New connections are [permitted\|denied] based on logging permit-hostdown policy. |
| ASA-3-414005  | 3        | Error        | TCP Syslog Server intf: IP_Address/port connected            |
| ASA-3-414006  | 3        | Error        | TCP Syslog Server configured and logging queue is full. New connections denied based on logging permit-hostdown policy. |
| ASA-3-418018  | 3        | Error        | neighbor IP_Address Down User reset OR neighbor IP_Address IPv4 Unicast topology base removed from session User reset OR neighbor IP_Address Up OR neighbor IP_Address IPv4 Unicast topology base removed from session BGP Notification sent |
| ASA-3-418019  | 3        | Error        | sent to neighbor IP_Address                                  |
| ASA-3-418040  | 3        | Error        | unsupported or mal-formatted message received from IP_Address |
| ASA-3-420001  | 3        | Error        | IPS card not up and fail-close mode used                     |
| ASA-3-420006  | 3        | Error        | Virtual Sensor not present and fail-close mode used          |
| ASA-3-420008  | 3        | Error        | IPS module license disabled and fail-close mode used         |
| ASA-3-421001  | 3        | Error        | TCP\|UDP flow from interface_name:ip/port to interface_name:ip/port is dropped because application has failed. |
| ASA-3-421003  | 3        | Error        | Invalid data plane encapsulation.                            |
| ASA-3-421007  | 3        | Error        | TCP\|UDP flow from interface_name:IP_address/port to interface_name:IP_address/port is skipped because application has failed. |
| ASA-3-425006  | 3        | Error        | Redundant interface redundant_interface_name switch active member to interface_name failed. |
| ASA-3-429001  | 3        | Error        | CXSC card not up and fail-close mode used. Dropping protocol packet from interface_name:ip_address/port to interface_name:ip_address/port |
| ASA-3-429004  | 3        | Error        | Unable to set up authentication-proxy rule for the cx action on interface interface_name for policy_type service-policy. |
| ASA-3-500005  | 3        | Error        | connection terminated from in_ifc_name:src_adddress/src_port to out_ifc_name:dest_address/dest_port due to invalid combination of inspections on same flow. Inspect inspect_name is not compatible with inspect inspect_name_2 |
| ASA-3-505016  | 3        | Error        | Module module_id application changed from: name version version state state to: name version state state. |
| ASA-3-507003  | 3        | Error        | The flow of type protocol from the originating interface: src_ip/src_port to dest_if:dest_ip/dest_port terminated by inspection engine |
| ASA-3-520001  | 3        | Error        | error_string                                                 |
| ASA-3-520002  | 3        | Error        | bad new ID table size                                        |
| ASA-3-520003  | 3        | Error        | bad id in error_string (id: 0xid_num)                        |
| ASA-3-520004  | 3        | Error        | error_string                                                 |
| ASA-3-520005  | 3        | Error        | error_string                                                 |
| ASA-3-520010  | 3        | Error        | Bad queue elem – qelem_ptr: flink flink_ptr                  |
| ASA-3-520011  | 3        | Error        | Null queue elem                                              |
| ASA-3-520013  | 3        | Error        | Regular expression access check with bad list acl_ID         |
| ASA-3-520020  | 3        | Error        | No memory available                                          |
| ASA-3-520021  | 3        | Error        | Error deleting trie entry                                    |
| ASA-3-520022  | 3        | Error        | Error adding mask entry                                      |
| ASA-3-520023  | 3        | Error        | Invalid pointer to head of tree                              |
| ASA-3-520024  | 3        | Error        | Orphaned mask #radix_mask_ptr                                |
| ASA-3-520025  | 3        | Error        | No memory for radix initialization: error_msg%ASA-3-602305: IPSEC: SA creation error |
| ASA-3-602306  | 3        | Error        | IPSEC: SA change peer IP error                               |
| ASA-3-610001  | 3        | Error        | NTP daemon interface interface_name: Packet denied from IP_address |
| ASA-3-610002  | 3        | Error        | NTP daemon interface interface_name: Authentication failed for packet from IP_address |
| ASA-3-611313  | 3        | Error        | VPN Client: Backup Server List Error: reason                 |
| ASA-3-613004  | 3        | Error        | Internal error: memory allocation failure                    |
| ASA-3-613005  | 3        | Error        | Flagged as being an ABR without a backbone area              |
| ASA-3-613006  | 3        | Error        | Reached unknown state in neighbor state machine              |
| ASA-3-613007  | 3        | Error        | area string lsid IP_address mask netmask type number         |
| ASA-3-613008  | 3        | Error        | if inside if_state number                                    |
| ASA-3-613011  | 3        | Error        | OSPF process number is changing router-id. Reconfigure virtual link neighbors with our new router-id |
| ASA-3-613013  | 3        | Error        | OSPF LSID IP_address adv IP_address type number gateway IP_address metric number forwarding addr route IP_address /mask type number has no corresponding LSA |
| ASA-3-613029  | 3        | Error        | Router-ID IP_address is in use by ospf process number%ASA-3-613016: Area string router-LSA of length number bytes plus update overhead bytes is too large to flood. |
| ASA-3-613032  | 3        | Error        | Init failed for interface inside                             |
| ASA-3-613034  | 3        | Error        | Neighbor IP_address not configured                           |
| ASA-3-613035  | 3        | Error        | Could not allocate or find neighbor IP_address%ASA-4-613015: Process 1 flushes LSA ID IP_address type-number adv-rtr IP_address in area mask%ASA-3-702305: IPSEC: An direction tunnel_type SA (SPI=spi) between local_IP and remote_IP (username) is rekeying due to sequence number rollover. |
| ASA-3-710003  | 3        | Error        | {TCP\|UDP} access denied by ACL from source_IP/source_port to interface_name:dest_IP/service |
| ASA-3-713004  | 3        | Error        | device scheduled for reboot or shutdown                      |
| ASA-3-713008  | 3        | Error        | Key ID in ID payload too big for pre-shared IKE tunnel       |
| ASA-3-713009  | 3        | Error        | OU in DN in ID payload too big for Certs IKE tunnel          |
| ASA-3-713012  | 3        | Error        | Unknown protocol (protocol). Not adding SA w/spi=SPI value   |
| ASA-3-713014  | 3        | Error        | Unknown Domain of Interpretation (DOI): DOI value            |
| ASA-3-713016  | 3        | Error        | Unknown identification type                                  |
| ASA-3-713017  | 3        | Error        | Identification type not supported                            |
| ASA-3-713018  | 3        | Error        | Unknown ID type during find of group name for certs          |
| ASA-3-713020  | 3        | Error        | No Group found by matching OU(s) from ID payload: OU_value   |
| ASA-3-713022  | 3        | Error        | No Group found matching peer_ID or IP_address for Pre-shared key peer IP_address |
| ASA-3-713032  | 3        | Error        | Received invalid local Proxy Range IP_address - IP_address   |
| ASA-3-713033  | 3        | Error        | Received invalid remote Proxy Range IP_address - IP_address  |
| ASA-3-713042  | 3        | Error        | IKE Initiator unable to find policy: Intf interface_number   |
| ASA-3-713043  | 3        | Error        | Cookie/peer address IP_address session already in progress   |
| ASA-3-713047  | 3        | Error        | Unsupported Oakley group: Group <Diffie-Hellman group>       |
| ASA-3-713048  | 3        | Error        | Error processing payload: Payload ID: id                     |
| ASA-3-713056  | 3        | Error        | Tunnel rejected: SA (SA_name) not found for group (group_name)! |
| ASA-3-713060  | 3        | Error        | Tunnel Rejected: User (user) not member of group (group_name) |
| ASA-3-713061  | 3        | Error        | Tunnel rejected: Crypto Map Policy not found for Src:source_address |
| ASA-3-713062  | 3        | Error        | IKE Peer address same as our interface address IP_address    |
| ASA-3-713063  | 3        | Error        | IKE Peer address not configured for destination IP_address   |
| ASA-3-713065  | 3        | Error        | IKE Remote Peer did not negotiate the following: proposal attribute |
| ASA-3-713072  | 3        | Error        | Password for user (user) too long                            |
| ASA-3-713081  | 3        | Error        | Unsupported certificate encoding type encoding_type          |
| ASA-3-713082  | 3        | Error        | Failed to retrieve identity certificate                      |
| ASA-3-713083  | 3        | Error        | Invalid certificate handle                                   |
| ASA-3-713084  | 3        | Error        | Received invalid phase 1 port value (port) in ID payload     |
| ASA-3-713085  | 3        | Error        | Received invalid phase 1 protocol (protocol) in ID payload   |
| ASA-3-713086  | 3        | Error        | Received unexpected Certificate payload Possible invalid Auth Method (Auth method (auth numerical value)) |
| ASA-3-713088  | 3        | Error        | Set Cert file handle failure: no IPSec SA in group group_name |
| ASA-3-713098  | 3        | Error        | Aborting: No identity cert specified in IPSec SA (SA_name)!  |
| ASA-3-713102  | 3        | Error        | Phase 1 ID Data length number too long - reject tunnel!      |
| ASA-3-713105  | 3        | Error        | Zero length data in ID payload received during phase 1 or 2 processing |
| ASA-3-713107  | 3        | Error        | IP_Address request attempt failed!                           |
| ASA-3-713109  | 3        | Error        | Unable to process the received peer certificate              |
| ASA-3-713112  | 3        | Error        | Failed to process CONNECTED notify (SPI SPI_value)!          |
| ASA-3-713118  | 3        | Error        | Detected invalid Diffie-Helmann group_descriptor group_number |
| ASA-3-713122  | 3        | Error        | Keep-alives configured keepalive_type but peer IP_address support keep-alives (type = keepalive_type) |
| ASA-3-713123  | 3        | Error        | IKE lost contact with remote peer                            |
| ASA-3-713124  | 3        | Error        | Received DPD sequence number rcv_sequence_# in DPD Action    |
| ASA-3-713127  | 3        | Error        | Xauth required but selected Proposal does not support xauth  |
| ASA-3-713129  | 3        | Error        | Received unexpected Transaction Exchange payload type: payload_id |
| ASA-3-713132  | 3        | Error        | Cannot obtain an IP_address for remote peer                  |
| ASA-3-713133  | 3        | Error        | Mismatch: Overriding phase 2 DH Group(DH group DH group_id) with phase 1 group(DH group DH group_number |
| ASA-3-713134  | 3        | Error        | Mismatch: P1 Authentication algorithm in the crypto map entry different from negotiated algorithm for the L2L connection |
| ASA-3-713138  | 3        | Error        | Group group_name not found and BASE GROUP default preshared key not configured |
| ASA-3-713140  | 3        | Error        | Split Tunneling Policy requires network list but none configured |
| ASA-3-713141  | 3        | Error        | Client-reported firewall does not match configured firewall: action tunnel. Received -- Vendor: vendor(id) |
| ASA-3-713142  | 3        | Error        | Client did not report firewall in use                        |
| ASA-3-713146  | 3        | Error        | Could not add route for Hardware Client in network extension mode |
| ASA-3-713149  | 3        | Error        | Hardware client security attribute attribute_name was enabled but not requested. |
| ASA-3-713152  | 3        | Error        | Unable to obtain any rules from filter ACL_tag to send to client for CPP |
| ASA-3-713159  | 3        | Error        | TCP Connection to Firewall Server has been lost              |
| ASA-3-713161  | 3        | Error        | Remote user (session Id - id) network access has been restricted by the Firewall Server |
| ASA-3-713162  | 3        | Error        | Remote user (session Id - id) has been rejected by the Firewall Server |
| ASA-3-713163  | 3        | Error        | Remote user (session Id - id) has been terminated by the Firewall Server |
| ASA-3-713165  | 3        | Error        | Client IKE Auth mode differs from the group's configured Auth mode |
| ASA-3-713166  | 3        | Error        | Headend security gateway has failed our user authentication attempt - check configured username and password |
| ASA-3-713167  | 3        | Error        | Remote peer has failed user authentication - check configured username and password |
| ASA-3-713168  | 3        | Error        | Re-auth enabled                                              |
| ASA-3-713174  | 3        | Error        | Hardware Client connection rejected! Network Extension Mode is not allowed for this group! |
| ASA-3-713182  | 3        | Error        | IKE could not recognize the version of the client! IPSec Fragmentation Policy will be ignored for this connection! |
| ASA-3-713185  | 3        | Error        | Error: Username too long - connection aborted                |
| ASA-3-713186  | 3        | Error        | Invalid secondary domain name list received from the authentication server. List Received: list_text Character index (value) is illegal |
| ASA-3-713189  | 3        | Error        | Attempted to assign network or broadcast IP_address          |
| ASA-3-713191  | 3        | Error        | Maximum concurrent IKE negotiations exceeded!                |
| ASA-3-713193  | 3        | Error        | Received packet with missing payload                         |
| ASA-3-713194  | 3        | Error        | Sending IKE\|IPSec Delete With Reason message: termination_reason |
| ASA-3-713195  | 3        | Error        | Tunnel rejected: Originate-Only: Cannot accept incoming tunnel yet! |
| ASA-3-713198  | 3        | Error        | User Authorization failed: user User authorization failed.   |
| ASA-3-713203  | 3        | Error        | IKE Receiver: Error reading from socket.                     |
| ASA-3-713205  | 3        | Error        | Could not add static route for client address: IP_address    |
| ASA-3-713206  | 3        | Error        | Tunnel Rejected: Conflicting protocols specified by tunnel-group and group-policy |
| ASA-3-713208  | 3        | Error        | Cannot create dynamic rule for Backup L2L entry rule rule_id |
| ASA-3-713209  | 3        | Error        | Cannot delete dynamic rule for Backup L2L entry rule id      |
| ASA-3-713210  | 3        | Error        | Cannot create dynamic map for Backup L2L entry rule_id       |
| ASA-3-713212  | 3        | Error        | Could not add route for L2L peer coming in on a dynamic map. address: IP_address |
| ASA-3-713214  | 3        | Error        | Could not delete route for L2L peer that came in on a dynamic map. address: IP_address |
| ASA-3-713217  | 3        | Error        | Skipping unrecognized rule: action: action client type: client_type client version: client_version |
| ASA-3-713218  | 3        | Error        | Tunnel Rejected: Client Type or Version not allowed.         |
| ASA-3-713226  | 3        | Error        | Connection failed with peer IP_address                       |
| ASA-3-713227  | 3        | Error        | Rejecting new IPSec SA negotiation for peer Peer_address. A negotiation was already in progress for local Proxy Local_address/Local_netmask |
| ASA-3-713230  | 3        | Error        | Internal Error                                               |
| ASA-3-713231  | 3        | Error        | Internal Error                                               |
| ASA-3-713232  | 3        | Error        | SA lock refCnt = value                                       |
| ASA-3-713238  | 3        | Error        | Invalid source proxy address: 0.0.0.0! Check private address on remote client |
| ASA-3-713254  | 3        | Error        | Group = groupname                                            |
| ASA-3-713258  | 3        | Error        | IP = var1                                                    |
| ASA-3-713260  | 3        | Error        | Output interface %d to peer was not found                    |
| ASA-3-713261  | 3        | Error        | IPV6 address on output interface %d was not found            |
| ASA-3-713262  | 3        | Error        | Rejecting new IPSec SA negotiation for peer Peer_address. A negotiation was already in progress for local Proxy Local_address/Local_prefix_len |
| ASA-3-713266  | 3        | Error        | Could not add route for L2L peer coming in on a dynamic map. address: IP_address |
| ASA-3-713268  | 3        | Error        | Could not delete route for L2L peer that came in on a dynamic map. address: IP_address |
| ASA-3-713270  | 3        | Error        | Could not add route for Hardware Client in network extension mode |
| ASA-3-713272  | 3        | Error        | Terminating tunnel to Hardware Client in network extension mode |
| ASA-3-713274  | 3        | Error        | Could not delete static route for client address: IP_Address IP_Address address of client whose route is being removed |
| ASA-3-713275  | 3        | Error        | IKEv1 Unsupported certificate keytype %s found at trustpoint %s |
| ASA-3-713276  | 3        | Error        | Dropping new negotiation - IKEv1 in-negotiation context limit of %u reached |
| ASA-3-713902  | 3        | Error        | Descriptive_event_string.                                    |
| ASA-3-716056  | 3        | Error        | Group group-name User user-name IP IP_address Authentication to SSO server name: name type type failed reason: reason |
| ASA-3-716057  | 3        | Error        | Group group User user IP ip Session terminated               |
| ASA-3-716061  | 3        | Error        | Group DfltGrpPolicy User user IP ip addr IPv6 User Filter tempipv6 configured for AnyConnect. This setting has been deprecated |
| ASA-3-716600  | 3        | Error        | Rejected size-recv KB Hostscan data from IP src-ip. Hostscan results exceed default \| configured limit of size-conf KB. |
| ASA-3-716601  | 3        | Error        | Rejected size-recv KB Hostscan data from IP src-ip. System-wide limit on the amount of Hostscan data stored on ASA exceeds the limit of data-max KB. |
| ASA-3-716602  | 3        | Error        | Memory allocation error. Rejected size-recv KB Hostscan data from IP src-ip. |
| ASA-3-717001  | 3        | Error        | Querying keypair failed.                                     |
| ASA-3-717002  | 3        | Error        | Certificate enrollment failed for trustpoint trustpoint_name. Reason: reason_string. |
| ASA-3-717009  | 3        | Error        | Certificate validation failed. Reason: reason_string.        |
| ASA-3-717010  | 3        | Error        | CRL polling failed for trustpoint trustpoint_name.           |
| ASA-3-717012  | 3        | Error        | Failed to refresh CRL cache entry from the server for trustpoint trustpoint_name at time_of_failure |
| ASA-3-717015  | 3        | Error        | CRL received from issuer is too large to process (CRL size = crl_size |
| ASA-3-717017  | 3        | Error        | Failed to query CA certificate for trustpoint trustpoint_name from enrollment_url |
| ASA-3-717018  | 3        | Error        | CRL received from issuer has too many entries to process (number of entries = number_of_entries |
| ASA-3-717019  | 3        | Error        | Failed to insert CRL for trustpoint trustpoint_name. Reason: failure_reason. |
| ASA-3-717020  | 3        | Error        | Failed to install device certificate for trustpoint label. Reason: reason string. |
| ASA-3-717021  | 3        | Error        | Certificate data could not be verified. Locate Reason: reason_string serial number: serial number |
| ASA-3-717023  | 3        | Error        | SSL failed to set device certificate for trustpoint trustpoint name. Reason: reason_string. |
| ASA-3-717027  | 3        | Error        | Certificate chain failed validation. reason_string.          |
| ASA-3-717039  | 3        | Error        | Local CA Server internal error detected: error.              |
| ASA-3-717042  | 3        | Error        | Failed to enable Local CA Server. Reason: reason.            |
| ASA-3-717044  | 3        | Error        | Local CA server certificate enrollment related error for user: user. Error: error. |
| ASA-3-717046  | 3        | Error        | Local CA Server CRL error: error.                            |
| ASA-3-717051  | 3        | Error        | SCEP Proxy: Denied processing the request type type received from IP client ip address |
| ASA-3-717057  | 3        | Error        | Automatic import of trustpool certificate bundle has failed. < Maximum retry attempts reached. Failed to reach CA server> \| <Cisco root bundle signature validation failed> \| <Failed to update trustpool bundle in flash> \| <Failed to install trustpool bundle in memory> |
| ASA-3-717060  | 3        | Error        | Peer certificate with serial number: <serial>                |
| ASA-3-717063  | 3        | Error        | protocol Certificate enrollment failed for the trustpoint tpname with the CA ca |
| ASA-3-719002  | 3        | Error        | Email Proxy session pointer from source_address has been terminated due to reason error. |
| ASA-3-719008  | 3        | Error        | Email Proxy service is shutting down.                        |
| ASA-3-722007  | 3        | Error        | Group group User user-name IP IP_address SVC Message: type-num/ERROR: message |
| ASA-3-722008  | 3        | Error        | Group group User user-name IP IP_address SVC Message: type-num/ERROR: message |
| ASA-3-722009  | 3        | Error        | Group group User user-name IP IP_address SVC Message: type-num/ERROR: message |
| ASA-3-722020  | 3        | Error        | TunnelGroup tunnel_group GroupPolicy group_policy User user-name IP IP_address No address available for SVC connection |
| ASA-3-722021  | 3        | Error        | Group group User user-name IP IP_address Unable to start compression due to lack of memory resources |
| ASA-3-722035  | 3        | Error        | Group group User user-name IP IP_address Received large packet length threshold num). |
| ASA-3-722036  | 3        | Error        | Group group User user-name IP IP_address Transmitting large packet length (threshold num). |
| ASA-3-722045  | 3        | Error        | Connection terminated: no SSL tunnel initialization data.    |
| ASA-3-722046  | 3        | Error        | Group group User user IP ip Session terminated: unable to establish tunnel. |
| ASA-3-725015  | 3        | Error        | Error verifying client certificate. Public key size in client certificate exceeds the maximum supported key size. |
| ASA-3-734004  | 3        | Error        | DAP: Processing error: internal error code                   |
| ASA-3-735010  | 3        | Error        | IPMI: Environment Monitoring has failed to update one or more of its records. |
| ASA-3-737002  | 3        | Error        | IPAA: Received unknown message 'num'                         |
| ASA-3-737027  | 3        | Error        | IPAA: No data for address request                            |
| ASA-3-742001  | 3        | Error        | failed to read master key for password encryption from persistent store |
| ASA-3-742002  | 3        | Error        | failed to set master key for password encryption             |
| ASA-3-742003  | 3        | Error        | failed to save master key for password encryption            |
| ASA-3-742004  | 3        | Error        | failed to sync master key for password encryption            |
| ASA-3-742005  | 3        | Error        | cipher text enc_pass is not compatible with the configured master key or the cipher text has been tampered with |
| ASA-3-742006  | 3        | Error        | password decryption failed due to unavailable memory         |
| ASA-3-742007  | 3        | Error        | password encryption failed due to unavailable memory         |
| ASA-3-742008  | 3        | Error        | password enc_pass decryption failed due to decoding error    |
| ASA-3-742009  | 3        | Error        | password encryption failed due to decoding error             |
| ASA-3-742010  | 3        | Error        | encrypted password enc_pass is not well formed               |
| ASA-3-743010  | 3        | Error        | EOBC RPC server failed to start for client module client name. |
| ASA-3-743011  | 3        | Error        | EOBC RPC call failed                                         |
| ASA-3-746003  | 3        | Error        | user-identity: activated import user groups \| activated host names \| user-to-IP address databases download failed - reason |
| ASA-3-746005  | 3        | Error        | user-identity: The AD Agent AD agent IP address cannot be reached - reason [action] |
| ASA-3-746010  | 3        | Error        | user-identity: update import-user domain_name\\group_name - Import Failed [reason] |
| ASA-3-746016  | 3        | Error        | user-identity: DNS lookup failed                             |
| ASA-3-746019  | 3        | Error        | user-identity: Update \| Remove AD Agent AD agent IP Address IP-user mapping user_IP - domain_name\user_name failed |
| ASA-3-747001  | 3        | Error        | Clustering: Recovered from state machine event queue depleted. Event (event-id |
| ASA-3-747010  | 3        | Error        | Clustering: RPC call failed                                  |
| ASA-3-747012  | 3        | Error        | Clustering: Failed to replicate global object id hex-id-value in domain domain-name to peer unit-name |
| ASA-3-747013  | 3        | Error        | Clustering: Failed to remove global object id hex-id-value in domain domain-name from peer unit-name |
| ASA-3-747014  | 3        | Error        | Clustering: Failed to install global object id hex-id-value in domain domain-name |
| ASA-3-747018  | 3        | Error        | Clustering: State progression failed due to timeout in module module-name. |
| ASA-3-747021  | 3        | Error        | Clustering: Master unit unit-name is quitting due to interface health check failure on failed-interface. |
| ASA-3-747022  | 3        | Error        | Clustering: Asking slave unit unit-name to quit because it failed interface health check x times |
| ASA-3-747023  | 3        | Error        | Clustering: Master unit unit-name is quitting due to card name card health check failure |
| ASA-3-747024  | 3        | Error        | Clustering: Asking slave unit unit-name to quit due to card name card health check failure |
| ASA-3-747030  | 3        | Error        | Clustering: Asking slave unit unit-name to quit because it failed interface health check x times (last failure on interface-name) |
| ASA-3-747031  | 3        | Error        | Clustering: Platform mismatch between cluster master (platform-type) and joining unit unit-name (platform-type). unit-name aborting cluster join. |
| ASA-3-747032  | 3        | Error        | Clustering: Service module mismatch between cluster master (module-name) and joining unit unit-name (module-name) in slot slot-number. unit-name aborting cluster join. |
| ASA-3-747033  | 3        | Error        | Clustering: Interface mismatch between cluster master and joining unit unit-name. unit-name aborting cluster join. |
| ASA-3-747036  | 3        | Error        | Application software mismatch between cluster master %s[Master unit name] (%s[Master application software name]) and joining unit (%s[Joining unit application software name]). %s[Joining member name] aborting cluster join. |
| ASA-3-747037  | 3        | Error        | Asking slave unit %s to quit due to its Security Service Module health check failure %d times |
| ASA-3-747038  | 3        | Error        | Asking slave unit %s to quit due to Security Service Module health check failure %d times |
| ASA-3-747039  | 3        | Error        | Unit %s is quitting due to system failure for %d time(s) (last failure is %s[cluster system failure reason]). Rejoin will be attempted after %d minutes. |
| ASA-3-747040  | 3        | Error        | Unit %s is quitting due to system failure for %d time(s) (last failure is %s[cluster system failure reason]). Clustering must be manually enabled on the unit to rejoin. |
| ASA-3-747041  | 3        | Error        | Unit %s is quitting due to system failure for %d time(s) (last failure is %s[cluster system failure reason]). Clustering must be manually enabled on the unit to rejoin.Master unit %s is quitting due to interface health check failure on %s[interface name], %d times. Clustering must be manually enabled on the unit to rejoin. |
| ASA-3-748005  | 3        | Error        | Failed to bundle the ports for module slot_number in chassis chassis_number; clustering is disabled |
| ASA-3-748006  | 3        | Error        | Asking module slot_number in chassis chassis_number to leave the cluster due to a port bundling failure |
| ASA-3-748100  | 3        | Error        | <application_name> application status is changed from <status> to <status>. |
| ASA-3-748101  | 3        | Error        | Peer unit <unit_id> reported its <application_name> application status is <status>. |
| ASA-3-748102  | 3        | Error        | Master unit <unit_id> is quitting due to <application_name> Application health check failure |
| ASA-3-748103  | 3        | Error        | Asking slave unit <unit_id> to quit due to <application_name> Application health check failure |
| ASA-3-748202  | 3        | Error        | Module <module_id> in chassis <chassis id> is leaving the cluster due to <aplpication name> application failure. |
| ASA-3-750011  | 3        | Error        | Tunnel Rejected: Selected IKEv2 encryption algorithm (IKEV2 encry algo) is not strong enough to secure proposed IPSEC encryption algorithm (IPSEC encry algo). |
| ASA-3-751001  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Failed to complete Diffie-Hellman operation. Error: error |
| ASA-3-751002  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group No preshared key or trustpoint configured for self in tunnel group group |
| ASA-3-751004  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group No remote authentication method configured for peer in tunnel group group |
| ASA-3-751005  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group AnyConnect client reconnect authentication failed. Session ID: sessionID |
| ASA-3-751006  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Certificate authentication failed. Error: error |
| ASA-3-751008  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Group=group |
| ASA-3-751009  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Unable to find tunnel group for peer. |
| ASA-3-751010  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Unable to determine self-authentication method. No crypto map setting or tunnel group found. |
| ASA-3-751011  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Failed user authentication. Error: error |
| ASA-3-751012  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Failure occurred during Configuration Mode processing. Error: error |
| ASA-3-751013  | 3        | Error        | Local: localIP:port Remote:remoteIP:port Username: username/group Failed to process Configuration Payload request for attribute attribute ID. Error: error |
| ASA-3-751017  | 3        | Error        | Local: localIP:port Remote remoteIP:port Username: username/group Configuration Error error description |
| ASA-3-751018  | 3        | Error        | Terminating the VPN connection attempt from landing group. Reason: This connection is group locked to locked group. |
| ASA-3-751020  | 3        | Error        | Local:%A:%u Remote:%A:%u Username:%s An %s remote access connection failed. Attempting to use an NSA Suite B crypto algorithm (%s) without an AnyConnect Premium license. |
| ASA-3-751022  | 3        | Error        | Local: local-ip Remote: remote-ip Username:username Tunnel rejected: Crypto Map Policy not found for remote traffic selector rem-ts-start/rem-ts-end/rem-ts.startport/rem-ts.endport/rem-ts.protocol local traffic selector local-ts-start/local-ts-end/local-ts.startport/local-ts.endport/local-ts.protocol! |
| ASA-3-751024  | 3        | Error        | Local:ip addr Remote:ip addr Username:username IKEv2 IPv6 User Filter tempipv6 configured. This setting has been deprecated |
| ASA-3-752006  | 3        | Error        | Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Probable mis-configuration of the crypto map or tunnel-group. Map Tag = Tag. Map Sequence Number = num |
| ASA-3-752007  | 3        | Error        | Tunnel Manager failed to dispatch a KEY_ACQUIRE message. Entry already in Tunnel Manager. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-3-752015  | 3        | Error        | Tunnel Manager has failed to establish an L2L SA. All configured IKE versions failed to establish the tunnel. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-3-768001  | 3        | Error        | QUOTA: resource utilization is high: requested req           |
| ASA-3-768002  | 3        | Error        | QUOTA: resource quota exceeded: requested req                |
| ASA-3-769006  | 3        | Error        | UPDATE: ASA boot system image image_name was not found on disk |
| ASA-3-772002  | 3        | Error        | PASSWORD: console login warning                              |
| ASA-3-772004  | 3        | Error        | PASSWORD: session login failed                               |
| ASA-3-776001  | 3        | Error        | CTS SXP: Configured source IP source ip error                |
| ASA-3-776002  | 3        | Error        | CTS SXP: Invalid message from peer peer IP: error            |
| ASA-3-776003  | 3        | Error        | CTS SXP: Connection with peer peer IP failed: error          |
| ASA-3-776004  | 3        | Error        | CTS SXP: Fail to start listening socket after TCP process restart. |
| ASA-3-776005  | 3        | Error        | CTS SXP: Binding Binding IP - SGname(SGT) from peer IP instance connection instance num error. |
| ASA-3-776006  | 3        | Error        | CTS SXP: Internal error: error                               |
| ASA-3-776007  | 3        | Error        | CTS SXP: Connection with peer peer IP (instance connection instance num) state changed from original state to Off. |
| ASA-3-776020  | 3        | Error        | CTS SXP: Unable to locate egress interface to peer peer IP.  |
| ASA-3-776202  | 3        | Error        | CTS PAC for Server IP_address                                |
| ASA-3-776203  | 3        | Error        | Unable to retrieve CTS Environment data due to: reason       |
| ASA-3-776204  | 3        | Error        | CTS Environment data has expired                             |
| ASA-3-776254  | 3        | Error        | CTS SGT-MAP: Binding manager unable to action binding binding IP - SGname (SGT) from source name. |
| ASA-3-776313  | 3        | Error        | CTS Policy: Failure to update policies for security-group sgname -sgt |
| ASA-3-779003  | 3        | Error        | STS: Failed to read tag-switching table - reason             |
| ASA-3-779004  | 3        | Error        | STS: Failed to write tag-switching table - reason            |
| ASA-3-779005  | 3        | Error        | STS: Failed to parse tag-switching request from http - reason |
| ASA-3-779006  | 3        | Error        | STS: Failed to save tag-switching table to flash - reason    |
| ASA-3-779007  | 3        | Error        | STS: Failed to replicate tag-switching table to peer - reason |
| ASA-3-8300003 | 3        | Error        | Failed to send session redistribution message to <variable 1> |
| ASA-3-8300005 | 3        | Error        | Failed to receive session move response from <variable 1>    |
| ASA-3-840001  | 3        | Error        | Failed to create the backup for an IKEv2 session <Local IP>  |
| ASA-4-105505  | 4        | Warning      | (Primary\|Secondary) Failed to connect to peer unit peer-ip:port |
| ASA-4-105524  | 4        | Warning      | (Primary\|Secondary) Transitioning to Negotiating state due to the presence of another Active HA unit |
| ASA-4-105553  | 4        | Warning      | (Primary\|Secondary) Detected another Active HA unit         |
| ASA-4-106023  | 4        | Warning      | Deny protocol src [interface_name:source_address/source_port] [([idfw_user\|FQDN_string] |
| ASA-4-106027  | 4        | Warning      | Deny src [source address] dst [destination address] by access-group “access-list name”. |
| ASA-4-106103  | 4        | Warning      | access-list acl_ID denied protocol for user username interface_name/source_address source_port interface_name/dest_address dest_port hit-cnt number first hit hash codes |
| ASA-4-108004  | 4        | Warning      | action_class: action ESMTP req_resp from src_ifc:sip\|sport to dest_ifc:dip\|dport;further_info |
| ASA-4-109017  | 4        | Warning      | User at IP_address exceeded auth proxy connection limit (max) |
| ASA-4-109022  | 4        | Warning      | exceeded HTTPS proxy process limit                           |
| ASA-4-109027  | 4        | Warning      | [aaa protocol] Unable to decipher response message Server = server_IP_address |
| ASA-4-109028  | 4        | Warning      | aaa bypassed for same-security traffic from ingress_ interface:source_address/source_port to egress_interface:dest_address/dest_port |
| ASA-4-109030  | 4        | Warning      | Autodetect ACL convert wildcard did not convert ACL access_list source \| dest netmask netmask. |
| ASA-4-109031  | 4        | Warning      | NT Domain Authentication Failed: rejecting guest login for username. |
| ASA-4-109033  | 4        | Warning      | Authentication failed for admin user user from src_IP. Interactive challenge processing is not supported for protocol connections |
| ASA-4-109034  | 4        | Warning      | Authentication failed for network user user from src_IP/port to dst_IP/port. Interactive challenge processing is not supported for protocol connections |
| ASA-4-109040  | 4        | Warning      | User at IP exceeded auth proxy rate limit of 10 connections/sec |
| ASA-4-109102  | 4        | Warning      | Received CoA action-type from coa-source-ip                  |
| ASA-4-113019  | 4        | Warning      | Group = group                                                |
| ASA-4-113026  | 4        | Warning      | Error error while executing Lua script for group tunnel group |
| ASA-4-113029  | 4        | Warning      | Group group User user IP ipaddr Session could not be established: session limit of num reached |
| ASA-4-113030  | 4        | Warning      | Group group User user IP ipaddr User ACL acl from AAA doesn't exist on the device |
| ASA-4-113031  | 4        | Warning      | Group group User user IP ipaddr AnyConnect vpn-filter filter is an IPv6 ACL; ACL not applied. |
| ASA-4-113032  | 4        | Warning      | Group group User user IP ipaddr AnyConnect ipv6-vpn-filter filter is an IPv4 ACL; ACL not applied. |
| ASA-4-113034  | 4        | Warning      | Group group User user IP ipaddr User ACL acl from AAA ignored |
| ASA-4-113035  | 4        | Warning      | Group group User user IP ipaddr Session terminated: AnyConnect not enabled or invalid AnyConnect image on the ASA. |
| ASA-4-113036  | 4        | Warning      | Group group User user IP ipaddr AAA parameter name value invalid. |
| ASA-4-113038  | 4        | Warning      | Group group User user IP ipaddr Unable to create AnyConnect p0arent session. |
| ASA-4-113040  | 4        | Warning      | Terminating the VPN connection attempt from attempted group. Reason: This connection is group locked to locked group. |
| ASA-4-113041  | 4        | Warning      | Redirect ACL configured for assigned IP does not exist on the device. |
| ASA-4-113042  | 4        | Warning      | CoA: Non-HTTP connection from src_if:src_ip/src_port to dest_if:dest_ip/dest_port for user username at client_IP denied by redirect filter; only HTTP connections are supported for redirection. |
| ASA-4-115002  | 4        | Warning      | Warning in process: process name fiber: fiber name           |
| ASA-4-120004  | 4        | Warning      | Event group title is dropped. Reason reason                  |
| ASA-4-120005  | 4        | Warning      | Message group to destination is dropped. Reason reason       |
| ASA-4-120006  | 4        | Warning      | Delivering message group to destination failed. Reason reason |
| ASA-4-199016  | 4        | Warning      | syslog                                                       |
| ASA-4-209003  | 4        | Warning      | Fragment database limit of number exceeded: src = source_address |
| ASA-4-209004  | 4        | Warning      | Invalid IP fragment                                          |
| ASA-4-209005  | 4        | Warning      | Discard IP fragment set with more than number elements: src = Too many elements are in a fragment set. |
| ASA-4-213007  | 4        | Warning      | L2TP: Failed to install Redirect URL: redirect URL Redirect ACL: non_exist for assigned IP. |
| ASA-4-216004  | 4        | Warning      | prevented: error in function at file(line) - stack trace     |
| ASA-4-302034  | 4        | Warning      | Unable to pre-allocate H323 GUP Connection for faddr interface: foreign address/foreign-port to laddr interface:local-address/local-port |
| ASA-4-308002  | 4        | Warning      | static global_address inside_address netmask netmask overlapped with global_address inside_address |
| ASA-4-313004  | 4        | Warning      | Denied ICMP type=icmp_type                                   |
| ASA-4-313005  | 4        | Warning      | No matching connection for ICMP error message: icmp_msg_info on interface_name interface. Original IP payload: embedded_frame_info icmp_msg_info = icmp src src_interface_name:src_address [([idfw_user \| FQDN_string] |
| ASA-4-313009  | 4        | Warning      | Denied invalid ICMP code icmp-code                           |
| ASA-4-325002  | 4        | Warning      | Duplicate address ipv6_address/MAC_address on interface      |
| ASA-4-325004  | 4        | Warning      | IPv6 Extension Header hdr_type action configuration. protocol from src_int:src_ipv6_addr/src_port to dst_interface: dst_ipv6_addr/dst_port. |
| ASA-4-325005  | 4        | Warning      | Invalid IPv6 Extension Header Content: string. detail regarding protocol |
| ASA-4-325006  | 4        | Warning      | IPv6 Extension Header not in order: Type hdr_type occurs after Type hdr_type. TCP prot from inside src_int: src_ipv6_addr/src_port to dst_interface:dst_ipv6_addr/dst_port |
| ASA-4-335005  | 4        | Warning      | NAC Downloaded ACL parse failure - host-address              |
| ASA-4-337005  | 4        | Warning      | Phone Proxy SRTP: Media session not found for media_term_ip/media_term_port for packet from in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-338001  | 4        | Warning      | Dynamic filter monitored blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port |
| ASA-4-338002  | 4        | Warning      | Dynamic filter monitored blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338003  | 4        | Warning      | Dynamic filter monitored blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port |
| ASA-4-338004  | 4        | Warning      | Dynamic filter monitored blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338005  | 4        | Warning      | Dynamic filter dropped blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338006  | 4        | Warning      | Dynamic filter dropped blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338007  | 4        | Warning      | Dynamic filter dropped blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338008  | 4        | Warning      | Dynamic filter dropped blacklisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338101  | 4        | Warning      | Dynamic filter action whitelisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port |
| ASA-4-338102  | 4        | Warning      | Dynamic filter action whitelisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338103  | 4        | Warning      | Dynamic filter action whitelisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port |
| ASA-4-338104  | 4        | Warning      | Dynamic filter action whitelisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338201  | 4        | Warning      | Dynamic filter monitored greylisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port |
| ASA-4-338202  | 4        | Warning      | Dynamic filter monitored greylisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338203  | 4        | Warning      | Dynamic filter dropped greylisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338204  | 4        | Warning      | Dynamic filter dropped greylisted protocol traffic from in_interface:src_ip_addr/src_port (mapped-ip/mapped-port) to out_interface:dest_ip_addr/dest_port (mapped-ip/mapped-port) |
| ASA-4-338301  | 4        | Warning      | Intercepted DNS reply for domain name from in_interface:src_ip_addr/src_port to out_interface:dest_ip_addr/dest_port |
| ASA-4-4000nn  | 4        | Warning      | IPS:number string from IP_address to IP_address on interface interface_name |
| ASA-4-400037  | 4        | Warning      | IDS:6053 DNS all records request from local_IP to remote_IP interface_name |
| ASA-4-401001  | 4        | Warning      | Shuns cleared                                                |
| ASA-4-401002  | 4        | Warning      | Shun added: IP_address IP_address port port                  |
| ASA-4-401003  | 4        | Warning      | Shun deleted: IP_address                                     |
| ASA-4-401004  | 4        | Warning      | Shunned packet: IP_address = IP_address on interface interface_name |
| ASA-4-401005  | 4        | Warning      | Shun add failed: unable to allocate resources for IP_address IP_address port port |
| ASA-4-402114  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402115  | 4        | Warning      | IPSEC: Received a packet from remote_IP to local_IP containing act_prot data instead of exp_prot data. |
| ASA-4-402116  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402117  | 4        | Warning      | IPSEC: Received a non-IPSec (protocol) packet from remote_IP to local_IP. |
| ASA-4-402118  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402119  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402120  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402121  | 4        | Warning      | IPSEC: Received an protocol packet (SPI=spi                  |
| ASA-4-402122  | 4        | Warning      | Received a cleartext packet from src_addr to dest_addr that was to be encapsulated in IPSec that was dropped by IPSec (drop_reason). |
| ASA-4-402123  | 4        | Warning      | CRYPTO: The accel_type hardware accelerator encountered an error (code= error_string) while executing crypto command command. |
| ASA-4-402124  | 4        | Warning      | CRYPTO: The ASA hardware accelerator encountered an error (Hardware error address |
| ASA-4-402125  | 4        | Warning      | The ASA hardware accelerator ring timed out (parameters).    |
| ASA-4-402126  | 4        | Warning      | CRYPTO: The ASA created Crypto Archive File Archive Filename as a Soft Reset was necessary. Please forward this archived information to Cisco. |
| ASA-4-402127  | 4        | Warning      | CRYPTO: The ASA is skipping the writing of latest Crypto Archive File as the maximum # of files |
| ASA-4-402131  | 4        | Warning      | CRYPTO: status changing the accel_instance hardware accelerator's configuration bias from old_config_bias to new_config_bias. |
| ASA-4-403101  | 4        | Warning      | PPTP session state not established                           |
| ASA-4-403102  | 4        | Warning      | PPP virtual interface interface_name rcvd pkt with invalid protocol: protocol |
| ASA-4-403103  | 4        | Warning      | PPP virtual interface max connections reached.               |
| ASA-4-403104  | 4        | Warning      | PPP virtual interface interface_name requires mschap for MPPE. |
| ASA-4-403106  | 4        | Warning      | PPP virtual interface interface_name requires RADIUS for MPPE. |
| ASA-4-403107  | 4        | Warning      | PPP virtual interface interface_name missing aaa server group info |
| ASA-4-403108  | 4        | Warning      | PPP virtual interface interface_name missing client ip address option |
| ASA-4-403109  | 4        | Warning      | Rec'd packet not an PPTP packet. (ip) dest_address= dest_address |
| ASA-4-403110  | 4        | Warning      | PPP virtual interface interface_name                         |
| ASA-4-403505  | 4        | Warning      | PPPoE:PPP - Unable to set default route to IP_address at interface_name |
| ASA-4-403506  | 4        | Warning      | PPPoE:failed to assign PPP IP_address netmask netmask at interface_name |
| ASA-4-405001  | 4        | Warning      | Received ARP {request \| response} collision from IP_address/MAC_address on interface interface_name to IP_address/MAC_address on interface interface_name |
| ASA-4-405002  | 4        | Warning      | Received mac mismatch collision from IP_address/MAC_address for authenticated host |
| ASA-4-405003  | 4        | Warning      | IP address collision detected between host IP_address at MAC_address and interface interface_name |
| ASA-4-405101  | 4        | Warning      | Unable to Pre-allocate H225 Call Signalling Connection for foreign_address outside_address[/outside_port] to local_address inside_address[/inside_port] |
| ASA-4-405102  | 4        | Warning      | Unable to Pre-allocate H245 Connection for foreign_address outside_address[/outside_port] to local_address inside_address[/inside_port] |
| ASA-4-405103  | 4        | Warning      | H225 message from source_address/source_port to dest_address/dest_port contains bad protocol discriminator hex |
| ASA-4-405104  | 4        | Warning      | H225 message received from outside_address/outside_port to inside_address/inside_port before SETUP |
| ASA-4-405105  | 4        | Warning      | H323 RAS message AdmissionConfirm received from source_address/source_port to dest_address/dest_port without an AdmissionRequest |
| ASA-4-405106  | 4        | Warning      | H323 num channel is not created from %I/%d to %I/%d %s       |
| ASA-4-405107  | 4        | Warning      | H245 Tunnel is detected and connection dropped from %I/%d to %I/%d %s |
| ASA-4-405201  | 4        | Warning      | ILS ILS_message_type from inside_interface:source_IP_address to outside_interface:/destination_IP_address has wrong embedded address embedded_IP_address |
| ASA-4-405300  | 4        | Warning      | Radius Accounting Request received from from_addr is not allowed |
| ASA-4-405301  | 4        | Warning      | Attribute attribute_number does not match for user user_ip   |
| ASA-4-406001  | 4        | Warning      | FTP port command low port: IP_address/port to IP_address on interface interface_name |
| ASA-4-406002  | 4        | Warning      | FTP port command different address: IP_address(IP_address) to IP_address on interface interface_name |
| ASA-4-407001  | 4        | Warning      | Deny traffic for local-host interface_name:inside_address    |
| ASA-4-407002  | 4        | Warning      | Embryonic limit nconns/elimit for through connections exceeded.outside_address/outside_port to global_address (inside_address)/inside_port on interface interface_name |
| ASA-4-407003  | 4        | Warning      | Established limit for RPC services exceeded number           |
| ASA-4-408001  | 4        | Warning      | IP route counter negative - reason                           |
| ASA-4-408002  | 4        | Warning      | ospf process id route type update address1 netmask1 [distance1/metric1] via source IP:interface1 address2 netmask2 [distance2/metric2] interface2 |
| ASA-4-408003  | 4        | Warning      | can't track this type of object hex                          |
| ASA-4-409001  | 4        | Warning      | Database scanner: external LSA IP_address netmask is lost    |
| ASA-4-409002  | 4        | Warning      | db_free: external LSA IP_address netmask                     |
| ASA-4-409003  | 4        | Warning      | Received invalid packet: reason from IP_address              |
| ASA-4-409004  | 4        | Warning      | Received reason from unknown neighbor IP_address             |
| ASA-4-409005  | 4        | Warning      | Invalid length number in OSPF packet from IP_address (ID IP_address) |
| ASA-4-409006  | 4        | Warning      | Invalid lsa: reason Type number                              |
| ASA-4-409007  | 4        | Warning      | Found LSA with the same host bit set but using different mask LSA ID IP_address netmask New: Destination IP_address netmask |
| ASA-4-409008  | 4        | Warning      | Found generating default LSA with non-zero mask LSA type : number Mask: netmask metric: number area: string |
| ASA-4-409009  | 4        | Warning      | OSPF process number cannot start. There must be at least one up IP interface |
| ASA-4-409010  | 4        | Warning      | Virtual link information found in non-backbone area: string  |
| ASA-4-409011  | 4        | Warning      | OSPF detected duplicate router-id IP_address from IP_address on interface interface_name |
| ASA-4-409012  | 4        | Warning      | Detected router with duplicate router ID IP_address in area string |
| ASA-4-409013  | 4        | Warning      | Detected router with duplicate router ID IP_address in Type-4 LSA advertised by IP_address |
| ASA-4-409023  | 4        | Warning      | Attempting AAA Fallback method method_name for request_type request for user user:Auth-server group server_tag unreachable |
| ASA-4-409101  | 4        | Warning      | Received invalid packet: %s from %P                          |
| ASA-4-409102  | 4        | Warning      | Received packet with incorrect area from %P                  |
| ASA-4-409103  | 4        | Warning      | Received %s from unknown neighbor %i                         |
| ASA-4-409104  | 4        | Warning      | Invalid length %d in OSPF packet type %d from %P (ID %i)     |
| ASA-4-409105  | 4        | Warning      | Invalid lsa: %s: Type 0x%x                                   |
| ASA-4-409106  | 4        | Warning      | Found generating default LSA with non-zero mask LSA type: 0x%x Mask: %i metric: %lu area: %AREA_ID_STR |
| ASA-4-409107  | 4        | Warning      | OSPFv3 process %d could not pick a router-id                 |
| ASA-4-409108  | 4        | Warning      | Virtual link information found in non-backbone area: %AREA_ID_STR |
| ASA-4-409109  | 4        | Warning      | OSPF detected duplicate router-id %i from %P on interface %IF_NAME |
| ASA-4-409110  | 4        | Warning      | Detected router with duplicate router ID %i in area %AREA_ID_STR |
| ASA-4-409111  | 4        | Warning      | Multiple interfaces (%IF_NAME /%IF_NAME) on a single link detected. |
| ASA-4-409112  | 4        | Warning      | Packet not written to the output queue                       |
| ASA-4-409113  | 4        | Warning      | Doubly linked list linkage is NULL                           |
| ASA-4-409114  | 4        | Warning      | Doubly linked list prev linkage is NULL %x                   |
| ASA-4-409115  | 4        | Warning      | Unrecognized timer %d in OSPF %s                             |
| ASA-4-409116  | 4        | Warning      | Error for timer %d in OSPF process %s                        |
| ASA-4-409117  | 4        | Warning      | Can't find LSA database type %x                              |
| ASA-4-409118  | 4        | Warning      | Could not allocate DBD packet                                |
| ASA-4-409119  | 4        | Warning      | Invalid build flag %x for LSA %i                             |
| ASA-4-409120  | 4        | Warning      | Router-ID %i is in use by ospf process %d                    |
| ASA-4-409121  | 4        | Warning      | Router is currently an ASBR while having only one area which is a stub area |
| ASA-4-409122  | 4        | Warning      | Could not select a global IPv6 address. Virtual links require at least one global IPv6 address. |
| ASA-4-409123  | 4        | Warning      | Neighbor command allowed only on NBMA networks               |
| ASA-4-409125  | 4        | Warning      | Can not use configured neighbor: poll and priority options are allowed only for a NBMA network |
| ASA-4-409128  | 4        | Warning      | OSPFv3-%d Area %AREA_ID_STR: Router %i originating invalid type 0x%x LSA |
| ASA-4-410001  | 4        | Warning      | UDP DNS request from source_interface:source_address/source_port to dest_interface:dest_address/dest_port; (label length \| domain-name length) 52 bytes exceeds remaining packet length of 44 bytes. |
| ASA-4-410003  | 4        | Warning      | action_class: action DNS query_response from src_ifc:sip/sport to dest_ifc:dip/dport; further_info |
| ASA-4-411001  | 4        | Warning      | Line protocol on interface interface_name changed state to up |
| ASA-4-411002  | 4        | Warning      | Line protocol on interface interface_name changed state to down |
| ASA-4-411003  | 4        | Warning      | Configuration status on interface interface_name changed state to downup |
| ASA-4-411004  | 4        | Warning      | Configuration status on interface interface_name changed state to up |
| ASA-4-411005  | 4        | Warning      | Interface variable 1 experienced a hardware transmit hang. The interface has been reset. |
| ASA-4-412001  | 4        | Warning      | MAC MAC_address moved from interface_1 to interface_2        |
| ASA-4-412002  | 4        | Warning      | Detected bridge table full while inserting MAC MAC_address on interface interface. Number of entries = num |
| ASA-4-413001  | 4        | Warning      | Module module_id is not able to shut down. Module Error: errnum message |
| ASA-4-413002  | 4        | Warning      | Module module_id is not able to reload. Module Error: errnum message |
| ASA-4-413003  | 4        | Warning      | Module module_id is not a recognized type                    |
| ASA-4-413004  | 4        | Warning      | Module module_id failed to write software vnewver (currently vver) |
| ASA-4-413005  | 4        | Warning      | Module module_id                                             |
| ASA-4-413006  | 4        | Warning      | prod-id Module software version mismatch; slot slot is prod-id version running-vers. Slot slot prod-id requires required-vers. |
| ASA-4-415016  | 4        | Warning      | policy-map map_name:Maximum number of unanswered HTTP requests exceeded connection_action from int_type:IP_address/port_num to int_type:IP_address/port_num |
| ASA-4-416001  | 4        | Warning      | Dropped UDP SNMP packet from source_interface:source_IP/source_port to dest_interface:dest_address/dest_port; version (prot_version) is not allowed through the firewall |
| ASA-4-417001  | 4        | Warning      | Unexpected event received: number                            |
| ASA-4-417004  | 4        | Warning      | Filter violation error: conn number (string:string) in string |
| ASA-4-417006  | 4        | Warning      | No memory for string) in string. Handling: string            |
| ASA-4-418001  | 4        | Warning      | Through-the-device packet to/from management-only network is denied: protocol_string from interface_name IP_address (port) [([idfw_user\|FQDN_string] |
| ASA-4-419001  | 4        | Warning      | Dropping TCP packet from src_ifc:src_IP/src_port to dest_ifc:dest_IP/dest_port |
| ASA-4-419002  | 4        | Warning      | Received duplicate TCP SYN from in_interface:src_address/src_port to out_interface:dest_address/dest_port with different initial sequence number. |
| ASA-4-419003  | 4        | Warning      | Cleared TCP urgent flag from out_ifc:src_ip/src_port to in_ifc:dest_ip/dest_port. |
| ASA-4-420002  | 4        | Warning      | IPS requested to drop ICMP packets ifc_in:SIP to ifc_out:DIP (typeICMP_TYPE |
| ASA-4-420003  | 4        | Warning      | IPS requested to reset TCP connection from ifc_in:SIP/SPORT to ifc_out:DIP/DPORT |
| ASA-4-420007  | 4        | Warning      | application-string cannot be enabled for the module in slot slot_id. The module’s current software version does not support this feature. Please upgrade the software on the module in slot slot_id to support this feature. Received backplane header version version_number, required backplane header version version_number or higher. |
| ASA-4-422004  | 4        | Warning      | IP SLA Monitor number0: Duplicate event received. Event number number1 |
| ASA-4-422005  | 4        | Warning      | IP SLA Monitor Probe(s) could not be scheduled because clock is not set. |
| ASA-4-422006  | 4        | Warning      | IP SLA Monitor Probe number: string                          |
| ASA-4-423001  | 4        | Warning      | {Allowed \| Dropped} invalid NBNS pkt_type_name with error_reason_str from ifc_name:ip_address/port to ifc_name:ip_address/port. |
| ASA-4-423002  | 4        | Warning      | {Allowed \| Dropped} mismatched NBNS pkt_type_name with error_reason_str from ifc_name:ip_address/port to ifc_name:ip_address/port. |
| ASA-4-423003  | 4        | Warning      | {Allowed \| Dropped} invalid NBDGM pkt_type_name with error_reason_str from ifc_name:ip_address/port to ifc_name:ip_address/port. |
| ASA-4-423004  | 4        | Warning      | {Allowed \| Dropped} mismatched NBDGM pkt_type_name with error_reason_str from ifc_name:ip_address/port to ifc_name:ip_address/port. |
| ASA-4-423005  | 4        | Warning      | {Allowed \| Dropped} NBDGM pkt_type_name fragment with error_reason_str from ifc_name:ip_address/port to ifc_name:ip_address/port. |
| ASA-4-424001  | 4        | Warning      | Packet denied protocol_string intf_in:src_ip/src_port [([idfw_user \| FQDN_string] |
| ASA-4-424002  | 4        | Warning      | Connection to the backup interface is denied: protocol_string intf:src_ip/src_port intf:dst_ip/dst_port |
| ASA-4-426004  | 4        | Warning      | PORT-CHANNEL: Interface ifc_name1 is not compatible with ifc_name and will be suspended (speed of ifc_name1 is X Mbps |
| ASA-4-429002  | 4        | Warning      | CXSC service card requested to drop protocol packet from interface_name:ip_address/port to interface_name:ip_address/port |
| ASA-4-429003  | 4        | Warning      | CXSC service card requested to reset TCP connection from interface_name:ip_addr/port to interface_name:ip_addr/port |
| ASA-4-429007  | 4        | Warning      | CXSC redirect will override Scansafe redirect for flow from interface_name:ip_address/port to interface_name:ip_address/port with username |
| ASA-4-429008  | 4        | Warning      | Unable to respond to VPN query from CX for session 0x%x. Reason %s |
| ASA-4-431001  | 4        | Warning      | RTP conformance: Dropping RTP packet from in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-431002  | 4        | Warning      | RTCP conformance: Dropping RTCP packet from in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-434001  | 4        | Warning      | SFR card not up and fail-close mode used                     |
| ASA-4-434002  | 4        | Warning      | SFR requested to drop protocol packet from ingress interface:source IP address/source port to egress interface:destination IP address/destination port |
| ASA-4-434003  | 4        | Warning      | SFR requested to reset TCP connection from ingress interface:source IP address/source port to egress interface:destination IP address/destination port |
| ASA-4-434007  | 4        | Warning      | SFR redirect will override Scansafe redirect for flow from ingress interface:source IP address/source port to egress interface:destination IP address/destination port (user) |
| ASA-4-444005  | 4        | Warning      | Timebased activation key activation-key will expire in num days. |
| ASA-4-444106  | 4        | Warning      | Shared license backup server address is not available        |
| ASA-4-444109  | 4        | Warning      | Shared license backup server role changed to state           |
| ASA-4-444110  | 4        | Warning      | Shared license server backup has days remaining as active license server |
| ASA-4-446001  | 4        | Warning      | Maximum TLS Proxy session limit of max_sess reached.         |
| ASA-4-446003  | 4        | Warning      | Denied TLS Proxy session from src_int:src_ip/src_port to dst_int:dst_ip/dst_port |
| ASA-4-447001  | 4        | Warning      | ASP DP to CP queue_name was full. Queue length length        |
| ASA-4-448001  | 4        | Warning      | Denied SRTP crypto session setup on flow from src_int:src_ip/src_port to dst_int:dst_ip/dst_port |
| ASA-4-450001  | 4        | Warning      | Deny traffic for protocol protocol_id src interface_name:IP_address/port dst interface_name:IP_address/port |
| ASA-4-500004  | 4        | Warning      | Invalid transport field for protocol=protocol                |
| ASA-4-507002  | 4        | Warning      | Data copy in proxy-mode exceeded the buffer limit            |
| ASA-4-603110  | 4        | Warning      | Failed to establish L2TP session                             |
| ASA-4-604105  | 4        | Warning      | DHCPD: Unable to send DHCP reply to client hardware_address on interface interface_name. Reply exceeds options field size (options_field_size) by number_of_octets octets. |
| ASA-4-607002  | 4        | Warning      | action_class: action SIP req_resp req_resp_info from src_ifc:sip/sport to dest_ifc:dip/dport; further_info |
| ASA-4-607004  | 4        | Warning      | Phone Proxy: Dropping SIP message from src_if:src_ip/src_port to dest_if:dest_ip/dest_port with source MAC mac_address due to secure phone database mismatch. |
| ASA-4-608002  | 4        | Warning      | Dropping Skinny message for in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-608003  | 4        | Warning      | Dropping Skinny message for in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-608004  | 4        | Warning      | Dropping Skinny message for in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-608005  | 4        | Warning      | Dropping Skinny message for in_ifc:src_ip/src_port to out_ifc:dest_ip/dest_port |
| ASA-4-612002  | 4        | Warning      | Auto Update failed:filename                                  |
| ASA-4-612003  | 4        | Warning      | Auto Update failed to contact:url                            |
| ASA-4-613017  | 4        | Warning      | Bad LSA mask: Type number                                    |
| ASA-4-613018  | 4        | Warning      | Maximum number of non self-generated LSA has been exceeded “OSPF number” - number LSAs |
| ASA-4-613019  | 4        | Warning      | Threshold for maximum number of non self-generated LSA has been reached OSPF number - number LSAs |
| ASA-4-613021  | 4        | Warning      | Packet not written to the output queue                       |
| ASA-4-613022  | 4        | Warning      | Doubly linked list linkage is NULL                           |
| ASA-4-613023  | 4        | Warning      | Doubly linked list prev linkage is NULL number               |
| ASA-4-613024  | 4        | Warning      | Unrecognized timer number in OSPF string                     |
| ASA-4-613025  | 4        | Warning      | Invalid build flag number for LSA IP_address                 |
| ASA-4-613026  | 4        | Warning      | Can not allocate memory for area structure                   |
| ASA-4-613030  | 4        | Warning      | Router is currently an ASBR while having only one area which is a stub area |
| ASA-4-613031  | 4        | Warning      | No IP address for interface inside                           |
| ASA-4-613036  | 4        | Warning      | Can not use configured neighbor: cost and database-filter options are allowed only for a point-to-multipoint network |
| ASA-4-613037  | 4        | Warning      | Can not use configured neighbor: poll and priority options are allowed only for a NBMA network |
| ASA-4-613038  | 4        | Warning      | Can not use configured neighbor: cost or database-filter option is required for point-to-multipoint broadcast network |
| ASA-4-613039  | 4        | Warning      | Can not use configured neighbor: neighbor command is allowed only on NBMA and point-to-multipoint networks |
| ASA-4-613040  | 4        | Warning      | OSPF-1 Area string: Router IP_address originating invalid type number LSA |
| ASA-4-613042  | 4        | Warning      | OSPF process number lacks forwarding address for type 7 LSA IP_address in NSSA string - P-bit cleared |
| ASA-4-620002  | 4        | Warning      | Unsupported CTIQBE version: hex: from interface_name:IP_address/port to interface_name:IP_address/port |
| ASA-4-709008  | 4        | Warning      | (Primary \| Secondary) Configuration sync in progress. Command: ‘command’ executed from (terminal/http) will not be replicated to or executed by the standby unit. |
| ASA-4-711002  | 4        | Warning      | Task ran for elapsed_time msecs                              |
| ASA-4-711004  | 4        | Warning      | Task ran for msec msec                                       |
| ASA-4-713154  | 4        | Warning      | DNS lookup for peer_description Server [server_name] failed! |
| ASA-4-713157  | 4        | Warning      | Timed out on initial contact to server [server_name or IP_address] Tunnel could not be established. |
| ASA-4-713207  | 4        | Warning      | Terminating connection: IKE Initiator and tunnel group specifies L2TP Over IPSec |
| ASA-4-713239  | 4        | Warning      | IP_Address: Tunnel Rejected: The maximum tunnel count allowed has been reached |
| ASA-4-713240  | 4        | Warning      | Received DH key with bad length: received length=rlength expected length=elength |
| ASA-4-713241  | 4        | Warning      | IE Browser Proxy Method setting_number is Invalid            |
| ASA-4-713242  | 4        | Warning      | Remote user is authenticated using Hybrid Authentication. Not starting IKE rekey. |
| ASA-4-713243  | 4        | Warning      | META-DATA Unable to find the requested certificate           |
| ASA-4-713244  | 4        | Warning      | META-DATA Received Legacy Authentication Method(LAM) type type is different from the last type received type. |
| ASA-4-713245  | 4        | Warning      | META-DATA Unknown Legacy Authentication Method(LAM) type type received. |
| ASA-4-713246  | 4        | Warning      | META-DATA Unknown Legacy Authentication Method(LAM) attribute type type received. |
| ASA-4-713247  | 4        | Warning      | META-DATA Unexpected error: in Next Card Code mode while not doing SDI. |
| ASA-4-713249  | 4        | Warning      | META-DATA Received unsupported authentication results: result |
| ASA-4-713251  | 4        | Warning      | META-DATA Received authentication failure message            |
| ASA-4-713255  | 4        | Warning      | IP = peer-IP                                                 |
| ASA-4-713903  | 4        | Warning      | Group = group policy                                         |
| ASA-4-716007  | 4        | Warning      | Group group User user WebVPN Unable to create session.       |
| ASA-4-716022  | 4        | Warning      | Unable to connect to proxy server reason.                    |
| ASA-4-716023  | 4        | Warning      | Group name User user Session could not be established: session limit of maximum_sessions reached. |
| ASA-4-716044  | 4        | Warning      | Group group-name User user-name IP IP_address AAA parameter param-name value param-value out of range. |
| ASA-4-716045  | 4        | Warning      | Group group-name User user-name IP IP_address AAA parameter param-name value invalid. |
| ASA-4-716046  | 4        | Warning      | Group group-name-name User user-name IP IP_address User ACL access-list-name from AAA doesn't exist on the device |
| ASA-4-716047  | 4        | Warning      | Group group-name User user-name IP IP_address User ACL access-list from AAA ignored |
| ASA-4-716048  | 4        | Warning      | Group group-name User user-name IP IP_address No memory to parse ACL. |
| ASA-4-716052  | 4        | Warning      | Group group-name User user-name IP IP_address Pending session terminated. |
| ASA-4-717026  | 4        | Warning      | Name lookup failed for hostname hostname during PKI operation. |
| ASA-4-717031  | 4        | Warning      | Failed to find a suitable trustpoint for the issuer: issuer Reason: reason_string |
| ASA-4-717035  | 4        | Warning      | OCSP status is being checked for certificate. certificate_identifier. |
| ASA-4-717037  | 4        | Warning      | Tunnel group search using certificate maps failed for peer certificate: certificate_identifier. |
| ASA-4-717052  | 4        | Warning      | Group group name User user name IP IP Address Session disconnected due to periodic certificate authentication failure. Subject Name id subject name Issuer Name id issuer name Serial Number id serial number |
| ASA-4-720001  | 4        | Warning      | (VPN-unit) Failed to initialize with Chunk Manager.          |
| ASA-4-720007  | 4        | Warning      | (VPN-unit) Failed to allocate chunk from Chunk Manager.      |
| ASA-4-720008  | 4        | Warning      | (VPN-unit) Failed to register to High Availability Framework. |
| ASA-4-720009  | 4        | Warning      | (VPN-unit) Failed to create version control block.           |
| ASA-4-720011  | 4        | Warning      | (VPN-unit) Failed to allocate memory                         |
| ASA-4-720013  | 4        | Warning      | (VPN-unit) Failed to insert certificate in trust point trustpoint_name |
| ASA-4-720022  | 4        | Warning      | (VPN-unit) Cannot find trust point trustpoint                |
| ASA-4-720033  | 4        | Warning      | (VPN-unit) Failed to queue add to message queue.             |
| ASA-4-720038  | 4        | Warning      | (VPN-unit) Corrupted message from active unit.               |
| ASA-4-720043  | 4        | Warning      | (VPN-unit) Failed to send type message id to standby unit    |
| ASA-4-720044  | 4        | Warning      | (VPN-unit) Failed to receive message from active unit        |
| ASA-4-720047  | 4        | Warning      | (VPN-unit) Failed to sync SDI node secret file for server IP_address on the standby unit. |
| ASA-4-720051  | 4        | Warning      | (VPN-unit) Failed to add new SDI node secret file for server id on the standby unit. |
| ASA-4-720052  | 4        | Warning      | (VPN-unit) Failed to delete SDI node secret file for server id on the standby unit. |
| ASA-4-720053  | 4        | Warning      | (VPN-unit) Failed to add cTCP IKE rule during bulk sync      |
| ASA-4-720054  | 4        | Warning      | (VPN-unit) Failed to add new cTCP record                     |
| ASA-4-720055  | 4        | Warning      | (VPN-unit) VPN Stateful failover can only be run in single/non-transparent mode. |
| ASA-4-720064  | 4        | Warning      | (VPN-unit) Failed to update cTCP database record for peer=IP_address |
| ASA-4-720065  | 4        | Warning      | (VPN-unit) Failed to add new cTCP IKE rule                   |
| ASA-4-720066  | 4        | Warning      | (VPN-unit) Failed to activate IKE database.                  |
| ASA-4-720067  | 4        | Warning      | (VPN-unit) Failed to deactivate IKE database.                |
| ASA-4-720068  | 4        | Warning      | (VPN-unit) Failed to parse peer message.                     |
| ASA-4-720069  | 4        | Warning      | (VPN-unit) Failed to activate cTCP database.                 |
| ASA-4-720070  | 4        | Warning      | (VPN-unit) Failed to deactivate cTCP database.               |
| ASA-4-720073  | 4        | Warning      | VPN Session failed to replicate - ACL acl_name not found     |
| ASA-4-721007  | 4        | Warning      | (device) Fail to update access list list_name on standby unit. |
| ASA-4-721011  | 4        | Warning      | (device) Fail to add access list rule list_name              |
| ASA-4-721013  | 4        | Warning      | (device) Fail to enable APCF XML file file_name on the standby unit. |
| ASA-4-721015  | 4        | Warning      | (device) Fail to disable APCF XML file file_name on the standby unit. |
| ASA-4-721017  | 4        | Warning      | (device) Fail to create WebVPN session for user user_name    |
| ASA-4-721019  | 4        | Warning      | (device) Fail to delete WebVPN session for client user user_name |
| ASA-4-722001  | 4        | Warning      | IP IP_address Error parsing SVC connect request.             |
| ASA-4-722002  | 4        | Warning      | IP IP_address Error consolidating SVC connect request.       |
| ASA-4-722003  | 4        | Warning      | IP IP_address Error authenticating SVC connect request.      |
| ASA-4-722004  | 4        | Warning      | Group group User user-name IP IP_address Error responding to SVC connect request. |
| ASA-4-722015  | 4        | Warning      | Group group User user-name IP IP_address Unknown SVC frame type: type-num |
| ASA-4-722016  | 4        | Warning      | Group group User user-name IP IP_address Bad SVC frame length: length expected: expected-length |
| ASA-4-722017  | 4        | Warning      | Group group User user-name IP IP_address Bad SVC framing: 525446 |
| ASA-4-722018  | 4        | Warning      | Group group User user-name IP IP_address Bad SVC protocol version: version |
| ASA-4-722019  | 4        | Warning      | Group group User user-name IP IP_address Not enough data for an SVC header: length |
| ASA-4-722039  | 4        | Warning      | Group group                                                  |
| ASA-4-722040  | 4        | Warning      | Group group                                                  |
| ASA-4-722041  | 4        | Warning      | TunnelGroup tunnel_group GroupPolicy group_policy User username IP peer_address No IPv6 address available for SVC connection |
| ASA-4-722042  | 4        | Warning      | Group group User user IP ip Invalid Cisco SSL Tunneling Protocol version. |
| ASA-4-722047  | 4        | Warning      | Group group User user IP ip Tunnel terminated: SVC not enabled or invalid SVC image on the ASA. |
| ASA-4-722048  | 4        | Warning      | Group group User user IP ip Tunnel terminated: SVC not enabled for the user. |
| ASA-4-722049  | 4        | Warning      | Group group User user IP ip Session terminated: SVC not enabled or invalid image on the ASA. |
| ASA-4-722050  | 4        | Warning      | Group group User user IP ip Session terminated: SVC not enabled for the user. |
| ASA-4-722054  | 4        | Warning      | Group group policy User user name IP remote IP SVC terminating connection: Failed to install Redirect URL: redirect URL Redirect ACL: non_exist for assigned IP |
| ASA-4-724001  | 4        | Warning      | Group group-name User user-name IP IP_address WebVPN session not allowed. Unable to determine if Cisco Secure Desktop was running on the client's workstation. |
| ASA-4-724002  | 4        | Warning      | Group group-name User user-name IP IP_address WebVPN session not terminated. Cisco Secure Desktop was not running on the client's workstation. |
| ASA-4-733100  | 4        | Warning      | Object drop rate rate_ID exceeded. Current burst rate is rate_val per second |
| ASA-4-733101  | 4        | Warning      | Object objectIP (is targeted\|is attacking). Current burst rate is rate_val per second |
| ASA-4-733102  | 4        | Warning      | Threat-detection adds host %I to shun list                   |
| ASA-4-733103  | 4        | Warning      | Threat-detection removes host %I from shun list              |
| ASA-4-733104  | 4        | Warning      | TD_SYSLOG_TCP_INTERCEPT_AVERAGE_RATE_EXCEED                  |
| ASA-4-733105  | 4        | Warning      | TD_SYSLOG_TCP_INTERCEPT_BURST_RATE_EXCEED                    |
| ASA-4-735015  | 4        | Warning      | CPU var1: Temp: var2 var3                                    |
| ASA-4-735016  | 4        | Warning      | Chassis Ambient var1: Temp: var2 var3                        |
| ASA-4-735018  | 4        | Warning      | Power Supply var1: Temp: var2 var3                           |
| ASA-4-735019  | 4        | Warning      | Power Supply var1: Temp: var2 var3                           |
| ASA-4-735026  | 4        | Warning      | CPU cpu_num Voltage Regulator is running beyond the max thermal operating temperature and the device will be shutting down immediately. The chassis and CPU need to be inspected immediately for ventilation issues. |
| ASA-4-737012  | 4        | Warning      | IPAA: Address assignment failed                              |
| ASA-4-737013  | 4        | Warning      | IPAA: Error freeing address ip-address                       |
| ASA-4-737019  | 4        | Warning      | IPAA: Unable to get address from group-policy or tunnel-group local pools |
| ASA-4-737028  | 4        | Warning      | IPAA: Adding ip-address to standby: failed                   |
| ASA-4-737030  | 4        | Warning      | IPAA: Adding %m to standby: address already in use           |
| ASA-4-737032  | 4        | Warning      | IPAA: Removing ip-address from standby: not found            |
| ASA-4-737033  | 4        | Warning      | IPAA: Unable to assign addr_allocator provided IP address ip_addr to client. This IP address has already been assigned by previous_addr_allocator |
| ASA-4-741005  | 4        | Warning      | Coredump operation variable 1 failed with error variable 2 variable 3 |
| ASA-4-741006  | 4        | Warning      | Unable to write Coredump Helper configuration                |
| ASA-4-746004  | 4        | Warning      | user identity: Total number of activated user groups exceeds the maximum number of max_groups groups for this platform. |
| ASA-4-746006  | 4        | Warning      | user-identity: Out of sync with AD Agent                     |
| ASA-4-746011  | 4        | Warning      | Total number of users created exceeds the maximum number of max_users for this platform. |
| ASA-4-747008  | 4        | Warning      | Clustering: New cluster member name with serial number serial-number-A rejected due to name conflict with existing unit with serial number serial-number-B. |
| ASA-4-747015  | 4        | Warning      | Clustering: Forcing stray member unit-name to leave the cluster. |
| ASA-4-747016  | 4        | Warning      | Clustering: Found a split cluster with both unit-name-A and unit-name-B as master units. Master role retained by unit-name-A |
| ASA-4-747017  | 4        | Warning      | Clustering: Failed to enroll unit unit-name due to maximum member limit limit-value reached. |
| ASA-4-747019  | 4        | Warning      | Clustering: New cluster member name rejected due to Cluster Control Link IP subnet mismatch (ip-address/ip-mask on new unit |
| ASA-4-747020  | 4        | Warning      | Clustering: New cluster member unit-name rejected due to encryption license mismatch. |
| ASA-4-747025  | 4        | Warning      | Clustering: New cluster member unit-name rejected due to firewall mode mismatch. |
| ASA-4-747026  | 4        | Warning      | Clustering: New cluster member unit-name rejected due to cluster interface name mismatch (ifc-name on new unit |
| ASA-4-747027  | 4        | Warning      | Clustering: Failed to enroll unit unit-name due to insufficient size of cluster pool pool-name in context-name. |
| ASA-4-747028  | 4        | Warning      | Clustering: New cluster member unit-name rejected due to interface mode mismatch (mode-name on new unit |
| ASA-4-747029  | 4        | Warning      | Clustering: Unit unit-name is quitting due to Cluster Control Link down. |
| ASA-4-747034  | 4        | Warning      | Unit %s is quitting due to Cluster Control Link down (%d times after last rejoin). Rejoin will be attempted after %d minutes. |
| ASA-4-747035  | 4        | Warning      | Unit %s is quitting due to Cluster Control Link down. Clustering must be manually enabled on the unit to rejoin. |
| ASA-4-748002  | 4        | Warning      | Clustering configuration on the chassis is missing or incomplete; clustering is disabled. |
| ASA-4-748003  | 4        | Warning      | Module slot_number in chassis chassis_number is leaving the cluster due to a chassis health check failure |
| ASA-4-748201  | 4        | Warning      | <Application name> application on module <module id> in chassis <chassis id> is <status>. |
| ASA-4-750003  | 4        | Warning      | Local: local IP:local port Remote: remote IP:remote port Username: username Negotiation aborted due to ERROR: error |
| ASA-4-750012  | 4        | Warning      | Selected IKEv2 encryption algorithm (IKEV2 encry algo) is not strong enough to secure proposed IPSEC encryption algorithm (IPSEC encry algo). |
| ASA-4-750014  | 4        | Warning      | Local:<self ip>:<self port> Remote:<peer ip>:<peer port> Username:<TG or Username> IKEv2 Session aborted. Reason: Initial Contact received for Local ID: <self ID> |
| ASA-4-750015  | 4        | Warning      | Local:<self ip>:<self port> Remote:<peer ip>:<peer port> Username:<TG or Username> IKEv2 deleting IPSec SA. Reason: invalid SPI notification received for SPI 0x<SPI>; local traffic selector = Address Range: <start address>-<end address> Protocol: <protocol number> Port Range: <start port>-<end port> ; remote traffic selector = Address Range: <start address>-<end address> Protocol: <protocol number> Port Range: <start port>-<end port> |
| ASA-4-751014  | 4        | Warning      | Local: localIP:port Remote remoteIP:port Username: username/group Warning Configuration Payload request for attribute attribute ID could not be processed. Error: error |
| ASA-4-751015  | 4        | Warning      | Local: localIP:port Remote remoteIP:port Username: username/group SA request rejected by CAC. Reason: reason |
| ASA-4-751016  | 4        | Warning      | Local: localIP:port Remote remoteIP:port Username: username/group L2L peer initiated a tunnel with the same outer and inner addresses. Peer could be Originate only - Possible misconfiguration! |
| ASA-4-751019  | 4        | Warning      | Local:LocalAddr Remote:RemoteAddr Username:username Failed to obtain an licenseType license. Maximum license limit limit exceeded. |
| ASA-4-751021  | 4        | Warning      | Local:variable 1:variable 2 Remote:variable 3:variable 4 Username:variable 5 variable 6 with variable 7 encryption is not supported with this version of the AnyConnect Client. Please upgrade to the latest Anyconnect Client. |
| ASA-4-751027  | 4        | Warning      | Local:local IP:local port Remote:peer IP:peer port Username:username IKEv2 Received INVALID_SELECTORS Notification from peer. Peer received a packet (SPI=spi). The decapsulated inner packet didn’t match the negotiated policy in the SA. Packet destination pkt_daddr, port pkt_dest_port, source pkt_saddr, port pkt_src_port, protocol pkt_prot. |
| ASA-4-752009  | 4        | Warning      | IKEv2 Doesn't support Multiple Peers                         |
| ASA-4-752010  | 4        | Warning      | IKEv2 Doesn't have a proposal specified                      |
| ASA-4-752011  | 4        | Warning      | IKEv1 Doesn't have a transform set specified                 |
| ASA-4-752012  | 4        | Warning      | IKEv protocol was unsuccessful at setting up a tunnel. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-4-752013  | 4        | Warning      | Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv2 after a failed attempt. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-4-752014  | 4        | Warning      | Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv1 after a failed attempt. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-4-752017  | 4        | Warning      | IKEv2 Backup L2L tunnel initiation denied on interface interface matching crypto map name |
| ASA-4-753001  | 4        | Warning      | Unexpected IKEv2 packet received from <IP>:<port>. Error: <reason> |
| ASA-4-768003  | 4        | Warning      | SSH: connection timed out: username username                 |
| ASA-4-770001  | 4        | Warning      | Resource resource allocation is more than the permitted list of limit for this platform. If this condition persists |
| ASA-4-770003  | 4        | Warning      | Resource resource allocation is less than the minimum requirement of value for this platform. If this condition persists |
| ASA-4-775002  | 4        | Warning      | Reason - protocol connection conn_id from interface_name:real_address/real_port [(idfw_user)] to interface_name:real_address/real_port is action locally |
| ASA-4-775004  | 4        | Warning      | Scansafe: Primary server ip_address is not reachable         |
| ASA-4-776201  | 4        | Warning      | CTS PAC: CTS PAC for Server IP_address                       |
| ASA-4-776304  | 4        | Warning      | CTS Policy: Unresolved security-group name sgname referenced |
| ASA-4-776305  | 4        | Warning      | CTS Policy: Security-group table cleared                     |
| ASA-4-776312  | 4        | Warning      | CTS Policy: Previously resolved security-group name sgname is now unresolved |
| ASA-5-105500  | 5        | Notification | (Primary\|Secondary) Started HA                              |
| ASA-5-105501  | 5        | Notification | (Primary\|Secondary) Stopping HA                             |
| ASA-5-105503  | 5        | Notification | (Primary\|Secondary) Internal state change from previous_state to new_state |
| ASA-5-105504  | 5        | Notification | (Primary\|Secondary) Connected to peer peer-ip:port          |
| ASA-5-105520  | 5        | Notification | (Primary\|Secondary) Responding to Azure Load Balancer probes |
| ASA-5-105521  | 5        | Notification | (Primary\|Secondary) No longer responding to Azure Load Balancer probes |
| ASA-5-105522  | 5        | Notification | (Primary\|Secondary) Updating route route_table_name         |
| ASA-5-105523  | 5        | Notification | (Primary\|Secondary) Updated route route_table_name          |
| ASA-5-105542  | 5        | Notification | (Primary\|Secondary) Enabling load balancer probe responses  |
| ASA-5-105543  | 5        | Notification | (Primary\|Secondary) Disabling load balancer probe responses |
| ASA-5-105552  | 5        | Notification | (Primary\|Secondary) Stopped HA                              |
| ASA-5-109012  | 5        | Notification | Authen Session End: user 'user'                              |
| ASA-5-109029  | 5        | Notification | Parsing downloaded ACL: string                               |
| ASA-5-109039  | 5        | Notification | AAA Authentication:Dropping an unsupported IPv6/IP46/IP64 packet from lifc:laddr to fifc:faddr |
| ASA-5-111001  | 5        | Notification | Begin configuration: IP_address writing to device            |
| ASA-5-111002  | 5        | Notification | Begin configuration: IP_address reading from device          |
| ASA-5-111003  | 5        | Notification | IP_address Erase configuration                               |
| ASA-5-111004  | 5        | Notification | IP_address end configuration: {FAILED\|OK}                   |
| ASA-5-111005  | 5        | Notification | IP_address end configuration: OK                             |
| ASA-5-111007  | 5        | Notification | Begin configuration: IP_address reading from device.         |
| ASA-5-111008  | 5        | Notification | User user executed the command string                        |
| ASA-5-111010  | 5        | Notification | User username                                                |
| ASA-5-113024  | 5        | Notification | Group tg: Authenticating type connection from ip with username |
| ASA-5-113025  | 5        | Notification | Group tg: FAILED to extract username from certificate while authenticating type connection from ip |
| ASA-5-120001  | 5        | Notification | Smart Call-Home Module is started.                           |
| ASA-5-120002  | 5        | Notification | Smart Call-Home Module is terminated.                        |
| ASA-5-120008  | 5        | Notification | SCH client client is activated.                              |
| ASA-5-120009  | 5        | Notification | SCH client client is deactivated.                            |
| ASA-5-120012  | 5        | Notification | User username chose to choice call-home anonymous reporting at the prompt. |
| ASA-5-199001  | 5        | Notification | Reload command executed from Telnet (remote IP_address).     |
| ASA-5-199017  | 5        | Notification | syslog                                                       |
| ASA-5-199027  | 5        | Notification | Restore operation was aborted at <HH:MM:SS> UTC <DD:MM:YY>   |
| ASA-5-212009  | 5        | Notification | Configuration request for SNMP group groupname failed. User username |
| ASA-5-303004  | 5        | Notification | FTP cmd_string command unsupported - failed strict inspection |
| ASA-5-303005  | 5        | Notification | Strict FTP inspection matched match_string in policy-map policy-name |
| ASA-5-304001  | 5        | Notification | user source_address [(idfw_user)] Accessed URL dest_address: url. |
| ASA-5-304002  | 5        | Notification | Access denied URL chars SRC IP_address [(idfw_user)] DEST IP_address: chars |
| ASA-5-305013  | 5        | Notification | Asymmetric NAT rules matched for forward and reverse flows; Connection protocol src interface_name:source_address/source_port [(idfw_user)] dst interface_name:dest_address/dst_port [(idfw_user)] denied due to NAT reverse path failure. |
| ASA-5-321001  | 5        | Notification | Resource var1 limit of var2 reached.                         |
| ASA-5-321002  | 5        | Notification | Resource var1 rate limit of var2 reached.                    |
| ASA-5-332003  | 5        | Notification | Web Cache IP_address/service_ID acquired                     |
| ASA-5-333002  | 5        | Notification | Timeout waiting for EAP response - context:EAP-context       |
| ASA-5-333010  | 5        | Notification | EAP-SQ response Validation Flags TLV indicates PV request - context:EAP-context |
| ASA-5-334002  | 5        | Notification | EAPoUDP association successfully established - host-address  |
| ASA-5-334003  | 5        | Notification | EAPoUDP association failed to establish - host-address       |
| ASA-5-334005  | 5        | Notification | Host put into NAC Hold state - host-address                  |
| ASA-5-334006  | 5        | Notification | EAPoUDP failed to get a response from host - host-address    |
| ASA-5-335002  | 5        | Notification | Host is on the NAC Exception List - host-address             |
| ASA-5-335003  | 5        | Notification | NAC Default ACL applied                                      |
| ASA-5-335008  | 5        | Notification | NAC IPSec terminate from dynamic ACL:ACL-name - host-address |
| ASA-5-336010  | 5        | Notification | Neighbor address (%interface) is event_msg: msg              |
| ASA-5-338302  | 5        | Notification | Address ipaddr discovered for domain name from list          |
| ASA-5-338303  | 5        | Notification | Address ipaddr (name) timed out                              |
| ASA-5-338308  | 5        | Notification | Dynamic filter updater server dynamically changed from old_server_host: old_server_port to new_server_host: new_server_port |
| ASA-5-402128  | 5        | Notification | CRYPTO: An attempt to allocate a large memory block failed   |
| ASA-5-415004  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415005  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415006  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415007  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415008  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415009  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415010  | 5        | Notification | matched matched_string in policy-map map_name                |
| ASA-5-415011  | 5        | Notification | HTTP - policy-map map_name:Protocol violation connection_action from int_type:IP_address/port_num to int_type:IP_address/port_num |
| ASA-5-415012  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415013  | 5        | Notification | HTTP - policy-map map-name:Malformed chunked encoding connection_action from int_type:IP_address/port_num to int_type:IP_address/port_num |
| ASA-5-415014  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415015  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415018  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415019  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-415020  | 5        | Notification | HTTP - matched matched_string in policy-map map_name         |
| ASA-5-425005  | 5        | Notification | Interface interface_name become active in redundant interface redundant_interface_name |
| ASA-5-4302310 | 5        | Notification | SCTP packet received from src_ifc:src_ip/src_port to dst_ifc:dst_ip/dst_port contains unsupported Hostname Parameter. |
| ASA-5-434004  | 5        | Notification | SFR requested ASA to bypass further packet redirection and process flow from %s:%A/%d to %s:%A/%d locally |
| ASA-5-444100  | 5        | Notification | Shared request request failed. Reason: reason                |
| ASA-5-444101  | 5        | Notification | Shared license service is active. License server address: address |
| ASA-5-500001  | 5        | Notification | ActiveX content in java script is modified: src src ip dest dest ip on interface interface name |
| ASA-5-500002  | 5        | Notification | Java content in java script is modified: src src ip dest dest ip on interface interface name |
| ASA-5-500003  | 5        | Notification | Bad TCP hdr length (hdrlen=bytes                             |
| ASA-5-501101  | 5        | Notification | User transitioning priv level                                |
| ASA-5-502101  | 5        | Notification | New user added to local dbase: Uname: user Priv: privilege_level Encpass: string |
| ASA-5-502102  | 5        | Notification | User deleted from local dbase: Uname: user Priv: privilege_level Encpass: string |
| ASA-5-502103  | 5        | Notification | User priv level changed: Uname: user From: privilege_level To: privilege_level |
| ASA-5-502111  | 5        | Notification | New group policy added: name: policy_name Type: policy_type  |
| ASA-5-502112  | 5        | Notification | Group policy deleted: name: policy_name Type: policy_type    |
| ASA-5-503001  | 5        | Notification | Process number                                               |
| ASA-5-503101  | 5        | Notification | Process %d                                                   |
| ASA-5-504001  | 5        | Notification | Security context context_name was added to the system        |
| ASA-5-504002  | 5        | Notification | Security context context_name was removed from the system    |
| ASA-5-505001  | 5        | Notification | Module module_id is shutting down. Please wait...            |
| ASA-5-505002  | 5        | Notification | Module ips is reloading. Please wait...                      |
| ASA-5-505003  | 5        | Notification | Module module_id is resetting. Please wait...                |
| ASA-5-505004  | 5        | Notification | Module module_id shutdown is complete.                       |
| ASA-5-505005  | 5        | Notification | Module module_name is initializing control communication. Please wait... |
| ASA-5-505006  | 5        | Notification | Module module_id is Up.                                      |
| ASA-5-505007  | 5        | Notification | Module module_id is recovering. Please wait...               |
| ASA-5-505008  | 5        | Notification | Module module_id software is being updated to vnewver (currently vver) |
| ASA-5-505009  | 5        | Notification | Module module_id software was updated to vnewver (previously vver) |
| ASA-5-505010  | 5        | Notification | Module in slot slot removed.                                 |
| ASA-5-505012  | 5        | Notification | Module module_id                                             |
| ASA-5-505013  | 5        | Notification | Module module_id application changed from: application version version to: newapplication version newversion. |
| ASA-5-506001  | 5        | Notification | event_source_string event_string                             |
| ASA-5-507001  | 5        | Notification | Terminating TCP-Proxy connection from interface_inside:source_address/source_port to interface_outside:dest_address/dest_port - reassembly limit of limit bytes exceeded |
| ASA-5-508001  | 5        | Notification | DCERPC message_type non-standard version_type version version_number from src_if:src_ip/src_port to dest_if:dest_ip/dest_port |
| ASA-5-508002  | 5        | Notification | DCERPC response has low endpoint port port_number from src_if:src_ip/src_port to dest_if:dest_ip/dest_port |
| ASA-5-509001  | 5        | Notification | Connection attempt from src_intf:src_ip/src_port [([idfw_user \| FQDN_string] |
| ASA-5-611103  | 5        | Notification | User logged out: Uname: user                                 |
| ASA-5-611104  | 5        | Notification | Serial console idle timeout exceeded                         |
| ASA-5-612001  | 5        | Notification | Auto Update succeeded:filename                               |
| ASA-5-711005  | 5        | Notification | Traceback: call_stack                                        |
| ASA-5-713006  | 5        | Notification | Failed to obtain state for message Id message_number         |
| ASA-5-713010  | 5        | Notification | IKE area: failed to find centry for message Id message_number |
| ASA-5-713041  | 5        | Notification | IKE Initiator: new or rekey Phase 1 or 2                     |
| ASA-5-713049  | 5        | Notification | Security negotiation complete for tunnel_type type (group_name) Initiator/Responder |
| ASA-5-713050  | 5        | Notification | Connection terminated for peer IP_address. Reason: termination reason Remote Proxy IP_address |
| ASA-5-713068  | 5        | Notification | Received non-routine Notify message: notify_type (notify_value) |
| ASA-5-713073  | 5        | Notification | Responder forcing change of Phase 1/Phase 2 rekeying duration from larger_value to smaller_value seconds |
| ASA-5-713074  | 5        | Notification | Responder forcing change of IPSec rekeying duration from larger_value to smaller_value Kbs |
| ASA-5-713075  | 5        | Notification | Overriding Initiator's IPSec rekeying duration from larger_value to smaller_value seconds |
| ASA-5-713076  | 5        | Notification | Overriding Initiator's IPSec rekeying duration from larger_value to smaller_value Kbs |
| ASA-5-713092  | 5        | Notification | Failure during phase 1 rekeying attempt due to collision     |
| ASA-5-713115  | 5        | Notification | Client rejected NAT enabled IPSec request                    |
| ASA-5-713119  | 5        | Notification | Group group IP ip PHASE 1 COMPLETED                          |
| ASA-5-713120  | 5        | Notification | PHASE 2 COMPLETED (msgid=msg_id)                             |
| ASA-5-713130  | 5        | Notification | Received unsupported transaction mode attribute: attribute id |
| ASA-5-713131  | 5        | Notification | Received unknown transaction mode attribute: attribute_id    |
| ASA-5-713135  | 5        | Notification | message received                                             |
| ASA-5-713136  | 5        | Notification | IKE session establishment timed out [IKE_state_name]         |
| ASA-5-713137  | 5        | Notification | Reaper overriding refCnt [ref_count] and tunnelCnt [tunnel_count] -- deleting SA! |
| ASA-5-713139  | 5        | Notification | group_name not found                                         |
| ASA-5-713144  | 5        | Notification | Ignoring received malformed firewall record; reason - error_reason TLV type attribute_value correction |
| ASA-5-713148  | 5        | Notification | Terminating tunnel to Hardware Client in network extension mode |
| ASA-5-713155  | 5        | Notification | DNS lookup for Primary VPN Server [server_name] successfully resolved after a previous failure. Resetting any Backup Server init. |
| ASA-5-713156  | 5        | Notification | Initializing Backup Server [server_name or IP_address]       |
| ASA-5-713158  | 5        | Notification | Client rejected NAT enabled IPSec Over UDP request           |
| ASA-5-713178  | 5        | Notification | IKE Initiator received a packet from its peer without a Responder cookie |
| ASA-5-713179  | 5        | Notification | IKE AM Initiator received a packet from its peer without a payload_type payload |
| ASA-5-713196  | 5        | Notification | Remote L2L Peer IP_address initiated a tunnel with same outer and inner addresses. Peer could be Originate Only - Possible misconfiguration! |
| ASA-5-713197  | 5        | Notification | The configured Confidence Interval of number seconds is invalid for this tunnel_type connection. Enforcing the second default. |
| ASA-5-713199  | 5        | Notification | Reaper corrected an SA that has not decremented the concurrent IKE negotiations counter (counter_value)! |
| ASA-5-713201  | 5        | Notification | Duplicate Phase Phase packet detected. Action                |
| ASA-5-713216  | 5        | Notification | Rule: action [Client type]: version Client: type version allowed/ not allowed |
| ASA-5-713229  | 5        | Notification | Auto Update - Notification to client client_ip of update string: message_string. |
| ASA-5-713237  | 5        | Notification | ACL update (access_list) received during re-key re-authentication will not be applied to the tunnel. |
| ASA-5-713248  | 5        | Notification | META-DATA Rekey initiation is being disabled during CRACK authentication. |
| ASA-5-713250  | 5        | Notification | META-DATA Received unknown Internal Address attribute: attribute |
| ASA-5-713252  | 5        | Notification | Group = group                                                |
| ASA-5-713253  | 5        | Notification | Group = group                                                |
| ASA-5-713257  | 5        | Notification | Phase var1 failure: Mismatched attribute types for class var2 : Rcv'd: var3 Cfg'd: var4 |
| ASA-5-713259  | 5        | Notification | Group = groupname                                            |
| ASA-5-713904  | 5        | Notification | Descriptive_event_string.                                    |
| ASA-5-716053  | 5        | Notification | SSO Server added: name: name Type: type                      |
| ASA-5-716054  | 5        | Notification | SSO Server deleted: name: name Type: type                    |
| ASA-5-717013  | 5        | Notification | Removing a cached CRL to accommodate an incoming CRL. Issuer: issuer |
| ASA-5-717014  | 5        | Notification | Unable to cache a CRL received from CDP due to size limitations (CRL size = size |
| ASA-5-717050  | 5        | Notification | SCEP Proxy: Processed request type type from IP client ip address |
| ASA-5-717053  | 5        | Notification | Group group name User user name IP IP Address Periodic certificate authentication succeeded. Subject Name id subject name Issuer Name id issuer name Serial Number id serial number |
| ASA-5-717061  | 5        | Notification | Starting protocol certificate enrollment for the trustpoint tpname with the CA ca_name. Request Type type Mode mode |
| ASA-5-717062  | 5        | Notification | protocol Certificate enrollment succeeded for the trustpoint tpname with the CA ca. Received a new certificate with Subject Name subject Issuer Name issuer Serial Number serial |
| ASA-5-717064  | 5        | Notification | Keypair keyname in the trustpoint tpname is regenerated for mode protocol certificate renewal |
| ASA-5-718002  | 5        | Notification | Create peer IP_address failure                               |
| ASA-5-718005  | 5        | Notification | Fail to send to IP_address                                   |
| ASA-5-718006  | 5        | Notification | Invalid load balancing state transition [cur=state_number][event=event_number] |
| ASA-5-718007  | 5        | Notification | Socket open failure failure_code                             |
| ASA-5-718008  | 5        | Notification | Socket bind failure failure_code                             |
| ASA-5-718009  | 5        | Notification | Send HELLO response failure to IP_address                    |
| ASA-5-718010  | 5        | Notification | Sent HELLO response to IP_address                            |
| ASA-5-718011  | 5        | Notification | Send HELLO request failure to IP_address                     |
| ASA-5-718012  | 5        | Notification | Sent HELLO request to IP_address                             |
| ASA-5-718014  | 5        | Notification | Master peer IP_address is not answering HELLO                |
| ASA-5-718015  | 5        | Notification | Received HELLO request from IP_address                       |
| ASA-5-718016  | 5        | Notification | Received HELLO response from IP_address                      |
| ASA-5-718024  | 5        | Notification | Send CFG UPDATE failure to IP_address                        |
| ASA-5-718028  | 5        | Notification | Send OOS indicator failure to IP_address                     |
| ASA-5-718031  | 5        | Notification | Received OOS obituary for IP_address                         |
| ASA-5-718032  | 5        | Notification | Received OOS indicator from IP_address                       |
| ASA-5-718033  | 5        | Notification | Send TOPOLOGY indicator failure to IP_address                |
| ASA-5-718042  | 5        | Notification | Unable to ARP for IP_address                                 |
| ASA-5-718043  | 5        | Notification | Updating/removing duplicate peer entry IP_address            |
| ASA-5-718044  | 5        | Notification | Deleted peer IP_address                                      |
| ASA-5-718045  | 5        | Notification | Created peer IP_address                                      |
| ASA-5-718048  | 5        | Notification | Create of secure tunnel failure for peer IP_address          |
| ASA-5-718050  | 5        | Notification | Delete of secure tunnel failure for peer IP_address          |
| ASA-5-718052  | 5        | Notification | Received GRAT-ARP from duplicate master MAC_address          |
| ASA-5-718053  | 5        | Notification | Detected duplicate master                                    |
| ASA-5-718054  | 5        | Notification | Detected duplicate master MAC_address and going to SLAVE     |
| ASA-5-718055  | 5        | Notification | Detected duplicate master MAC_address and staying MASTER     |
| ASA-5-718057  | 5        | Notification | Queue send failure from ISR                                  |
| ASA-5-718060  | 5        | Notification | Inbound socket select fail: context=context_ID.              |
| ASA-5-718061  | 5        | Notification | Inbound socket read fail: context=context_ID.                |
| ASA-5-718062  | 5        | Notification | Inbound thread is awake (context=context_ID).                |
| ASA-5-718063  | 5        | Notification | Interface interface_name is down.                            |
| ASA-5-718064  | 5        | Notification | Admin. interface interface_name is down.                     |
| ASA-5-718065  | 5        | Notification | Cannot continue to run (public=up/down                       |
| ASA-5-718066  | 5        | Notification | Cannot add secondary address to interface interface_name     |
| ASA-5-718067  | 5        | Notification | Cannot delete secondary address to interface interface_name  |
| ASA-5-718068  | 5        | Notification | Start VPN Load Balancing in context context_ID.              |
| ASA-5-718069  | 5        | Notification | Stop VPN Load Balancing in context context_ID.               |
| ASA-5-718070  | 5        | Notification | Reset VPN Load Balancing in context context_ID.              |
| ASA-5-718071  | 5        | Notification | Terminate VPN Load Balancing in context context_ID.          |
| ASA-5-718072  | 5        | Notification | Becoming master of Load Balancing in context context_ID.     |
| ASA-5-718073  | 5        | Notification | Becoming slave of Load Balancing in context context_ID.      |
| ASA-5-718074  | 5        | Notification | Fail to create access list for peer context_ID.              |
| ASA-5-718075  | 5        | Notification | Peer IP_address access list not set.                         |
| ASA-5-718076  | 5        | Notification | Fail to create tunnel group for peer IP_address.             |
| ASA-5-718077  | 5        | Notification | Fail to delete tunnel group for peer IP_address.             |
| ASA-5-718078  | 5        | Notification | Fail to create crypto map for peer IP_address.               |
| ASA-5-718079  | 5        | Notification | Fail to delete crypto map for peer IP_address.               |
| ASA-5-718080  | 5        | Notification | Fail to create crypto policy for peer IP_address.            |
| ASA-5-718081  | 5        | Notification | Fail to delete crypto policy for peer IP_address.            |
| ASA-5-718082  | 5        | Notification | Fail to create crypto ipsec for peer IP_address.             |
| ASA-5-718083  | 5        | Notification | Fail to delete crypto ipsec for peer IP_address.             |
| ASA-5-718084  | 5        | Notification | Public/cluster IP not on the same subnet: public IP_address  |
| ASA-5-718085  | 5        | Notification | Interface interface_name has no IP address defined.          |
| ASA-5-718086  | 5        | Notification | Fail to install LB NP rules: type rule_type                  |
| ASA-5-718087  | 5        | Notification | Fail to delete LB NP rules: type rule_type                   |
| ASA-5-719014  | 5        | Notification | Email Proxy is changing listen port from old_port to new_port for mail protocol protocol. |
| ASA-5-720016  | 5        | Notification | (VPN-unit) Failed to initialize default timer #index.        |
| ASA-5-720017  | 5        | Notification | (VPN-unit) Failed to update LB runtime data                  |
| ASA-5-720018  | 5        | Notification | (VPN-unit) Failed to get a buffer from the underlying core high availability subsystem. Error code code. |
| ASA-5-720019  | 5        | Notification | (VPN-unit) Failed to update cTCP statistics.                 |
| ASA-5-720020  | 5        | Notification | (VPN-unit) Failed to send type timer message.                |
| ASA-5-720021  | 5        | Notification | (VPN-unit) HA non-block send failed for peer msg message_number. HA error code. |
| ASA-5-720035  | 5        | Notification | (VPN-unit) Fail to look up CTCP flow handle                  |
| ASA-5-720036  | 5        | Notification | (VPN-unit) Failed to process state update message from the active peer. |
| ASA-5-720071  | 5        | Notification | (VPN-unit) Failed to update cTCP dynamic data.               |
| ASA-5-720072  | 5        | Notification | Timeout waiting for Integrity Firewall Server [interface     |
| ASA-5-722005  | 5        | Notification | Group group User user-name IP IP_address Unable to update session information for SVC connection. |
| ASA-5-722006  | 5        | Notification | Group group User user-name IP IP_address Invalid address IP_address assigned to SVC connection. |
| ASA-5-722010  | 5        | Notification | Group group User user-name IP IP_address SVC Message: type-num/NOTICE: message |
| ASA-5-722011  | 5        | Notification | Group group User user-name IP IP_address SVC Message: type-num/NOTICE: message |
| ASA-5-722012  | 5        | Notification | Group group User user-name IP IP_address SVC Message: type-num/INFO: message |
| ASA-5-722028  | 5        | Notification | Group group User user-name IP IP_address Stale SVC connection closed. |
| ASA-5-722032  | 5        | Notification | Group group User user-name IP IP_address New SVC connection replacing old connection. |
| ASA-5-722033  | 5        | Notification | Group group User user-name IP IP_address First SVC connection established for SVC session. |
| ASA-5-722034  | 5        | Notification | Group group User user-name IP IP_address New SVC connection  |
| ASA-5-722037  | 5        | Notification | Group group User user-name IP IP_address SVC closing connection: reason. |
| ASA-5-722038  | 5        | Notification | Group group-name User user-name IP IP_address SVC terminating session: reason. |
| ASA-5-722043  | 5        | Notification | Group group User user IP ip DTLS disabled: unable to negotiate cipher. |
| ASA-5-722044  | 5        | Notification | Group group User user IP ip Unable to request ver address for SSL tunnel. |
| ASA-5-730009  | 5        | Notification | Group groupname                                              |
| ASA-5-734002  | 5        | Notification | DAP: User user                                               |
| ASA-5-737003  | 5        | Notification | IPAA: DHCP configured                                        |
| ASA-5-737004  | 5        | Notification | IPAA: DHCP configured                                        |
| ASA-5-737007  | 5        | Notification | IPAA: Local pool request failed for tunnel-group 'tunnel-group' |
| ASA-5-737008  | 5        | Notification | IPAA: 'tunnel-group' not found                               |
| ASA-5-737011  | 5        | Notification | IPAA: AAA assigned address ip-address                        |
| ASA-5-737018  | 5        | Notification | IPAA: DHCP request attempt num failed                        |
| ASA-5-737021  | 5        | Notification | IPAA: Address from local pool (ip-address) duplicates address from DHCP |
| ASA-5-737022  | 5        | Notification | IPAA: Address from local pool (ip-address) duplicates address from AAA |
| ASA-5-737023  | 5        | Notification | IPAA: Unable to allocate memory to store local pool address ip-address |
| ASA-5-737024  | 5        | Notification | IPAA: Local pool assignment failed for suggested IP ip-address |
| ASA-5-737025  | 5        | Notification | IPAA: Not releasing local pool ip-address                    |
| ASA-5-737034  | 5        | Notification | IPAA: Session=<session>                                      |
| ASA-5-746007  | 5        | Notification | user-identity: NetBIOS response failed from User user_name at user_ip |
| ASA-5-746012  | 5        | Notification | user-identity: Add IP-User mapping IP Address - domain_name\user_name result - reason |
| ASA-5-746013  | 5        | Notification | user-identity: Delete IP-User mapping IP Address - domain_name\user_name result - reason |
| ASA-5-746014  | 5        | Notification | user-identity: [FQDN] fqdn address IP Address obsolete       |
| ASA-5-746015  | 5        | Notification | user-identity: [FQDN] fqdn resolved IP address               |
| ASA-5-747002  | 5        | Notification | Clustering: Recovered from state machine dropped event (event-id |
| ASA-5-747003  | 5        | Notification | Clustering: Recovered from state machine failure to process event (event-id |
| ASA-5-747007  | 5        | Notification | Clustering: Recovered from finding stray config sync thread  |
| ASA-5-748001  | 5        | Notification | Module slot_number in chassis chassis_number is leaving the cluster due to a chassis configuration change |
| ASA-5-748004  | 5        | Notification | Module slot_number in chassis chassis_number is re-joining the cluster due to a chassis health check recovery |
| ASA-5-748203  | 5        | Notification | Module <module_id> in chassis <chassis id> is re-joining the cluster due to a service chain application recovery. |
| ASA-5-750001  | 5        | Notification | Local:local IP:local port Remote:remote IP: remote port Username: username Received request to request an IPsec tunnel; local traffic selector = local selectors: range |
| ASA-5-750002  | 5        | Notification | Local:local IP:local port Remote: remote IP: remote port Username: username Received a IKE_INIT_SA request |
| ASA-5-750004  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username Sending COOKIE challenge to throttle possible DoS |
| ASA-5-750005  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username IPsec rekey collision detected. I am lowest nonce initiator |
| ASA-5-750006  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username SA UP. Reason: reason |
| ASA-5-750007  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username SA DOWN. Reason: reason |
| ASA-5-750008  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username SA rejected due to system resource low |
| ASA-5-750009  | 5        | Notification | Local: local IP: local port Remote: remote IP: remote port Username: username SA request rejected due to CAC limit reached: Rejection reason: reason |
| ASA-5-750010  | 5        | Notification | Local: local-ip Remote: remote-ip Username:username IKEv2 local throttle-request queue depth threshold of threshold reached; increase the window size on peer peer for better performance |
| ASA-5-750013  | 5        | Notification | IKEv2 SA (iSPI <ISPI> rRSP <rSPI>) Peer Moved: Previous <prev_remote_ip>:<prev_remote_port>/<prev_local_ip>:<prev_local_port>. Updated <new_remote_ip>:<new_remote_port>/<new_local_ip>:<new_local_port> |
| ASA-5-751007  | 5        | Notification | Local: localIP:port Remote:remoteIP:port Username: username/group Configured attribute not supported for IKEv2. Attribute: attribute |
| ASA-5-751025  | 5        | Notification | Local: local IP:local port Remote: remote IP:remote port Username:username Group:group-policy IPv4 Address=assigned_IPv4_addr IPv6 address=assigned_IPv6_addr assigned to session. |
| ASA-5-751028  | 5        | Notification | Local:<localIP:port> Remote:<remoteIP:port> Username:<username/group> IKEv2 Overriding configured keepalive values of threshold:<config_threshold>/retry:<config_retry> to threshold:<applied_threshold>/retry:<applied_retry>. |
| ASA-5-752003  | 5        | Notification | Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv2. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-5-752004  | 5        | Notification | Tunnel Manager dispatching a KEY_ACQUIRE message to IKEv1. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-5-752016  | 5        | Notification | IKEv protocol was successful at setting up a tunnel. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-5-769001  | 5        | Notification | UPDATE: ASA image src was added to system boot list          |
| ASA-5-769002  | 5        | Notification | UPDATE: ASA image src was copied to dest                     |
| ASA-5-769003  | 5        | Notification | UPDATE: ASA image src was renamed to dest                    |
| ASA-5-769004  | 5        | Notification | UPDATE: ASA image src_file failed verification               |
| ASA-5-769005  | 5        | Notification | UPDATE: ASA image image_name passed image verification       |
| ASA-5-771001  | 5        | Notification | CLOCK: System clock set                                      |
| ASA-5-771002  | 5        | Notification | CLOCK: System clock set                                      |
| ASA-5-776009  | 5        | Notification | CTS SXP: password changed.                                   |
| ASA-5-776010  | 5        | Notification | CTS SXP: SXP default source IP is changed original source IP final source IP. |
| ASA-5-776011  | 5        | Notification | CTS SXP: operational state.                                  |
| ASA-5-776252  | 5        | Notification | CTS SGT-MAP: CTS SGT-MAP: Binding binding IP - SGname(SGT) from source name deleted from binding manager. |
| ASA-5-776309  | 5        | Notification | CTS Policy: Previously known security-group tag sgt is now unknown |
| ASA-5-776310  | 5        | Notification | CTS Policy: Security-group name sgname remapped from security-group tag old_sgt to new_sgt |
| ASA-5-8300006 | 5        | Notification | Cluster topology change detected. VPN session redistribution aborted. |
| ASA-6-106012  | 6        | Info         | Deny IP from IP_address to IP_address                        |
| ASA-6-106015  | 6        | Info         | Deny TCP (no connection) from IP_address/port to IP_address/port flags tcp_flags on interface interface_name. |
| ASA-6-106025  | 6        | Info         | Failed to determine the security context for the packet:sourceVlan:source_address dest_address source_port dest_port protocol |
| ASA-6-106026  | 6        | Info         | Failed to determine the security context for the packet:sourceVlan:source_address dest_address source_port dest_port protocol |
| ASA-6-106100  | 6        | Info         | access-list acl_ID {permitted \| denied \| est-allowed} protocol interface_name/source_address(source_port)(idfw_user |
| ASA-6-106102  | 6        | Info         | access-list acl_ID {permitted \| denied} protocol for user username interface_name/source_address source_port interface_name/dest_address dest_port hit-cnt number {first hit \| number-second interval} hash codes |
| ASA-6-108005  | 6        | Info         | action_class: Received ESMTP req_resp from src_ifc:sip\|sport to dest_ifc:dip\|dport;further_info |
| ASA-6-108007  | 6        | Info         | TLS started on ESMTP session between client client-side interface-name: clientIP address/client port and server server-side interface-name: server IP address/server port |
| ASA-6-109001  | 6        | Info         | Auth start for user user from inside_address/inside_port to outside_address/outside_port |
| ASA-6-109002  | 6        | Info         | Auth from inside_address/inside_port to outside_address/outside_port failed (server IP_address failed) on interface interface_name. |
| ASA-6-109003  | 6        | Info         | Auth from inside_address to outside_address/outside_port failed (all servers failed) on interface interface_name |
| ASA-6-109005  | 6        | Info         | Authentication succeeded for user user from inside_address/inside_port to outside_address/outside_port on interface interface_name. |
| ASA-6-109006  | 6        | Info         | Authentication failed for user user from inside_address/inside_port to outside_address/outside_port on interface interface_name. |
| ASA-6-109007  | 6        | Info         | Authorization permitted for user user from inside_address/inside_port to outside_address/outside_port on interface interface_name. |
| ASA-6-109008  | 6        | Info         | Authorization denied for user user from outside_address/outside_port to inside_address/ inside_port on interface interface_name. |
| ASA-6-109024  | 6        | Info         | Authorization denied from source_address/source_port to dest_address/dest_port (not authenticated) on interface interface_name using protocol |
| ASA-6-109025  | 6        | Info         | Authorization denied (acl=acl_ID) for user 'user' from source_address/source_port to dest_address/dest_port on interface interface_name using protocol |
| ASA-6-109036  | 6        | Info         | Exceeded 1000 attribute values for the attribute name attribute for user username. |
| ASA-6-109100  | 6        | Info         | Received CoA update from coa-source-ip for user username     |
| ASA-6-109101  | 6        | Info         | Received CoA disconnect request from coa-source-ip for user username |
| ASA-6-110002  | 6        | Info         | Failed to locate egress interface for protocol from src interface:src IP/src port to dest IP/dest port |
| ASA-6-110003  | 6        | Info         | Routing failed to locate next-hop for protocol from src interface:src IP/src port to dest interface:dest IP/dest port |
| ASA-6-110004  | 6        | Info         | Egress interface changed from old_active_ifc to new_active_ifc on ip_protocol connection conn_id for outside_zone/parent_outside_ifc:outside_addr/outside_port (mapped_addr/mapped_port) to inside_zone/parent_inside_ifc:inside_addr/inside_port (mapped_addr/mapped_port) |
| ASA-6-113003  | 6        | Info         | AAA group policy for user user is being set to policy_name.  |
| ASA-6-113004  | 6        | Info         | AAA user aaa_type Successful: server = server_IP_address     |
| ASA-6-113005  | 6        | Info         | AAA user authentication Rejected: reason = string: server = server_IP_address |
| ASA-6-113006  | 6        | Info         | User user locked out on exceeding number successive failed authentication attempts |
| ASA-6-113007  | 6        | Info         | User user unlocked by administrator                          |
| ASA-6-113008  | 6        | Info         | AAA transaction status ACCEPT: user = user                   |
| ASA-6-113009  | 6        | Info         | AAA retrieved default group policy policy for user user      |
| ASA-6-113010  | 6        | Info         | AAA challenge received for user user from server server_IP_address |
| ASA-6-113011  | 6        | Info         | AAA retrieved user specific group policy policy for user user |
| ASA-6-113012  | 6        | Info         | AAA user authentication Successful: local database: user = user |
| ASA-6-113013  | 6        | Info         | AAA unable to complete the request Error: reason = reason: user = user |
| ASA-6-113014  | 6        | Info         | AAA authentication server not accessible: server = server_IP_address: user = user |
| ASA-6-113015  | 6        | Info         | AAA user authentication Rejected: reason = reason: local database: user = user: user IP =xxx.xxx.xxx.xxx |
| ASA-6-113016  | 6        | Info         | AAA credentials rejected: reason = reason: server = server_IP_address: user = user: user IP = xxx.xxx.xxx.xxx |
| ASA-6-113017  | 6        | Info         | AAA credentials rejected: reason = reason: local database: user = user: user IP = user_ip=xxx.xxx.xxx.xxx |
| ASA-6-113033  | 6        | Info         | Group group User user IP ipaddr AnyConnect session not allowed. ACL parse error. |
| ASA-6-113037  | 6        | Info         | Reboot pending                                               |
| ASA-6-113039  | 6        | Info         | Group group User user IP ipaddr AnyConnect parent session started. |
| ASA-6-114004  | 6        | Info         | 4GE SSM I/O Initialization start.                            |
| ASA-6-114005  | 6        | Info         | 4GE SSM I/O Initialization end.                              |
| ASA-6-120003  | 6        | Info         | Process event group title                                    |
| ASA-6-120007  | 6        | Info         | Message group to destination delivered.                      |
| ASA-6-199002  | 6        | Info         | startup completed. Beginning operation.                      |
| ASA-6-199003  | 6        | Info         | Reducing link MTU dec.                                       |
| ASA-6-199005  | 6        | Info         | Startup begin                                                |
| ASA-6-199018  | 6        | Info         | syslog                                                       |
| ASA-6-201010  | 6        | Info         | Embryonic connection limit exceeded econns/limit for dir packet from source_address/source_port to dest_address/dest_port on interface interface_name |
| ASA-6-201012  | 6        | Info         | Per-client embryonic connection limit exceeded curr num/limit for [input\|output] packet from IP_address/ port to ip/port on interface interface_name |
| ASA-6-210022  | 6        | Info         | LU missed number updates                                     |
| ASA-6-302003  | 6        | Info         | Built H245 connection for foreign_address outside_address/outside_port local_address inside_address/inside_port |
| ASA-6-302004  | 6        | Info         | Pre-allocate H323 UDP backconnection for foreign_address outside_address/outside_port to local_address inside_address/inside_port |
| ASA-6-302010  | 6        | Info         | connections in use                                           |
| ASA-6-302012  | 6        | Info         | Pre-allocate H225 Call Signalling Connection for faddr IP_address/port to laddr IP_address |
| ASA-6-302013  | 6        | Info         | Built {inbound\|outbound} TCP connection_id for interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] to interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] [(user)] |
| ASA-6-302014  | 6        | Info         | Teardown TCP connection id for interface :real-address /real-port [(idfw_user )] to interface :real-address /real-port [(idfw_user )] duration hh:mm:ss bytes bytes [reason [from teardown-initiator]] [(user )] |
| ASA-6-302015  | 6        | Info         | Built {inbound\|outbound} UDP connection number for interface_name:real_address/real_port (mapped_address/mapped_port) [(idfw_user)] to interface_name:real_address/real_port (mapped_address/mapped_port) [(idfw_user)] [(user)] |
| ASA-6-302016  | 6        | Info         | Teardown UDP connection number for interface:real-address/real-port [(idfw_user)] to interface:real-address/real-port [(idfw_user)] duration hh:mm:ss bytes bytes [(user)] |
| ASA-6-302017  | 6        | Info         | Built {inbound\|outbound} GRE connection id from interface:real_address (translated_address) [(idfw_user)] to interface:real_address/real_cid (translated_address/translated_cid) [(idfw_user)] [(user) |
| ASA-6-302018  | 6        | Info         | Teardown GRE connection id from interface:real_address (translated_address) [(idfw_user)] to interface:real_address/real_cid (translated_address/translated_cid) [(idfw_user)] duration hh:mm:ss bytes bytes [(user)] |
| ASA-6-302020  | 6        | Info         | Built ICMP connection connection_id from interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] to interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] [(user)] |
| ASA-6-302021  | 6        | Info         | Teardown ICMP connection connection_id from interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] to interface:real-address/real-port (mapped-address/mapped-port) [(idfw_user)] [(user)] |
| ASA-6-302022  | 6        | Info         | Built role stub TCP connection for interface:real-address/real-port (mapped-address/mapped-port) to interface:real-address/real-port (mapped-address/mapped-port) |
| ASA-6-302023  | 6        | Info         | Teardown stub TCP connection for interface:real-address/real-port to interface:real-address/real-port duration hh:mm:ss forwarded bytes bytes reason |
| ASA-6-302024  | 6        | Info         | Built role stub UDP connection for interface:real-address/real-port (mapped-address/mapped-port) to interface:real-address/real-port (mapped-address/mapped-port) |
| ASA-6-302025  | 6        | Info         | Teardown stub UDP connection for interface:real-address/real-port to interface:real-address/real-port duration hh:mm:ss forwarded bytes bytes reason |
| ASA-6-302026  | 6        | Info         | Built role stub ICMP connection for interface:real-address/real-port (mapped-address) to interface:real-address/real-port (mapped-address) |
| ASA-6-302027  | 6        | Info         | Teardown stub ICMP connection for interface:real-address/real-port to interface:real-address/real-port duration hh:mm:ss forwarded bytes bytes reason |
| ASA-6-302033  | 6        | Info         | Pre-allocated H323 GUP Connection for faddr interface:foreign address/foreign-port to laddr interface:local-address/local-port |
| ASA-6-302035  | 6        | Info         | Built {inbound\|outbound} SCTP connection conn_id for outside_interface:outside_ip/outside_port (mapped_outside_ip/mapped_outside_port)[([outside_idfw_user] |
| ASA-6-302036  | 6        | Info         | Teardown SCTP connection conn_id for outside_interface:outside_ip/outside_port[([outside_idfw_user] |
| ASA-6-302303  | 6        | Info         | Built TCP state-bypass connection conn_id from initiator_interface:real_ip/real_port(mapped_ip/mapped_port) to responder_interface:real_ip/real_port (mapped_ip/mapped_port) |
| ASA-6-302304  | 6        | Info         | Teardown TCP state-bypass connection conn_id from initiator_interface:ip/port to responder_interface:ip/port duration |
| ASA-6-302305  | 6        | Info         | Built SCTP state-bypass connection conn_id for outside_interface:outside_ip/outside_port (mapped_outside_ip/mapped_outside_port)[([outside_idfw_user] |
| ASA-6-302306  | 6        | Info         | Teardown SCTP state-bypass connection conn_id for outside_interface:outside_ip/outside_port[([outside_idfw_user] |
| ASA-6-303002  | 6        | Info         | FTP connection from src_ifc:src_ip/src_port to dst_ifc:dst_ip/dst_port |
| ASA-6-304004  | 6        | Info         | URL Server IP_address request failed URL url HTTP/1.0        |
| ASA-6-305007  | 6        | Info         | addrpool_free(): Orphan IP IP_address on interface interface_number |
| ASA-6-305009  | 6        | Info         | Built {dynamic\|static} translation from interface_name [(acl-name)]:real_address [(idfw_user)] to interface_name:mapped_address |
| ASA-6-305010  | 6        | Info         | Teardown {dynamic\|static} translation from interface_name:real_address [(idfw_user)] to interface_name:mapped_address duration time |
| ASA-6-305011  | 6        | Info         | Built {dynamic\|static} {TCP\|UDP\|ICMP} translation from interface_name:real_address/real_port [(idfw_user)] to interface_name:mapped_address/mapped_port |
| ASA-6-305012  | 6        | Info         | Teardown {dynamic\|static} {TCP\|UDP\|ICMP} translation from interface_name [(acl-name)]:real_address/{real_port\|real_ICMP_ID} [(idfw_user)] to interface_name:mapped_address/{mapped_port\|mapped_ICMP_ID} duration time |
| ASA-6-305014  | 6        | Info         | %d: Allocated %s block of ports for translation from %s:%B to %s:%B/%d-%d |
| ASA-6-308001  | 6        | Info         | console enable password incorrect for number tries (from IP_address) |
| ASA-6-311001  | 6        | Info         | LU loading standby start                                     |
| ASA-6-311002  | 6        | Info         | LU loading standby end                                       |
| ASA-6-311003  | 6        | Info         | LU recv thread up                                            |
| ASA-6-311004  | 6        | Info         | LU xmit thread up                                            |
| ASA-6-312001  | 6        | Info         | RIP hdr failed from IP_address: cmd=string                   |
| ASA-6-314001  | 6        | Info         | Pre-allocated RTSP UDP backconnection for src_intf:src_IP to dst_intf:dst_IP/dst_port. |
| ASA-6-314002  | 6        | Info         | RTSP failed to allocate UDP media connection from src_intf:src_IP to dst_intf:dst_IP/dst_port: reason_string. |
| ASA-6-314003  | 6        | Info         | Dropped RTSP traffic from src_intf:src_ip due to: reason.    |
| ASA-6-314004  | 6        | Info         | RTSP client src_intf:src_IP accessed RTSP URL RTSP URL       |
| ASA-6-314005  | 6        | Info         | RTSP client src_intf:src_IP denied access to URL RTSP_URL.   |
| ASA-6-314006  | 6        | Info         | RTSP client src_intf:src_IP exceeds configured rate limit of rate for request_method messages. |
| ASA-6-315011  | 6        | Info         | SSH session from IP_address on interface interface_name for user user disconnected by SSH server |
| ASA-6-315013  | 6        | Info         | SSH session from SSH client address on interface interface_name for user user_name rekeyed successfully. |
| ASA-6-317007  | 6        | Info         | Added route_type route dest_address netmask via gateway_address [distance/metric] on interface_name route_type |
| ASA-6-317008  | 6        | Info         | Deleted route_type route dest_address netmask via gateway_address [distance/metric] on interface_name route_type |
| ASA-6-321003  | 6        | Info         | Resource var1 log level of var2 reached.                     |
| ASA-6-321004  | 6        | Info         | Resource var1 rate log level of var2 reached                 |
| ASA-6-322004  | 6        | Info         | No management IP address configured for transparent firewall. Dropping protocol protocol packet from interface_in:source_address/source_port to interface_out:dest_address/dest_port |
| ASA-6-333001  | 6        | Info         | EAP association initiated - context:EAP-context              |
| ASA-6-333003  | 6        | Info         | EAP association terminated - context:EAP-context             |
| ASA-6-333009  | 6        | Info         | EAP-SQ response MAC TLV is invalid - context:EAP-context     |
| ASA-6-334001  | 6        | Info         | EAPoUDP association initiated - host-address                 |
| ASA-6-334004  | 6        | Info         | Authentication request for NAC Clientless host - host-address |
| ASA-6-334007  | 6        | Info         | EAPoUDP association terminated - host-address                |
| ASA-6-334008  | 6        | Info         | NAC EAP association initiated - host-address                 |
| ASA-6-334009  | 6        | Info         | Audit request for NAC Clientless host - Assigned_IP.         |
| ASA-6-335001  | 6        | Info         | NAC session initialized - host-address                       |
| ASA-6-335004  | 6        | Info         | NAC is disabled for host - host-address                      |
| ASA-6-335006  | 6        | Info         | NAC Applying ACL:ACL-name - host-address                     |
| ASA-6-335009  | 6        | Info         | NAC 'Revalidate' request by administrative action - host-address |
| ASA-6-335010  | 6        | Info         | NAC 'Revalidate All' request by administrative action - num sessions |
| ASA-6-335011  | 6        | Info         | NAC 'Revalidate Group' request by administrative action for group-name group - num sessions |
| ASA-6-335012  | 6        | Info         | NAC 'Initialize' request by administrative action - host-address |
| ASA-6-335013  | 6        | Info         | NAC 'Initialize All' request by administrative action - num sessions |
| ASA-6-335014  | 6        | Info         | NAC 'Initialize Group' request by administrative action for group-name group - num sessions |
| ASA-6-336011  | 6        | Info         | event event                                                  |
| ASA-6-337000  | 6        | Info         | Created BFD session with local discriminator id on real_interface with neighbor real_host_ip. |
| ASA-6-337001  | 6        | Info         | Terminated BFD session with local discriminator id on real_interface with neighbor real_host_ip due to failure_reason. |
| ASA-6-338304  | 6        | Info         | Successfully downloaded dynamic filter data file from updater server url |
| ASA-6-340002  | 6        | Info         | Loopback-proxy info: error_string context id context_id      |
| ASA-6-341001  | 6        | Info         | Policy Agent started successfully for VNMC vnmc_ip_addr      |
| ASA-6-341002  | 6        | Info         | Policy Agent stopped successfully for VNMC vnmc_ip_add       |
| ASA-6-341010  | 6        | Info         | Storage device with serial number ser_no [inserted into \| removed from] bay bay_no |
| ASA-6-402129  | 6        | Info         | CRYPTO: An attempt to release a DMA memory block failed      |
| ASA-6-402130  | 6        | Info         | CRYPTO: Received an ESP packet (SPI = 0x54A5C634             |
| ASA-6-403500  | 6        | Info         | PPPoE - Service name 'any' not received in PADO. Intf:interface_name AC:ac_name. |
| ASA-6-410004  | 6        | Info         | action_class: action DNS query_response from src_ifc:sip/sport to dest_ifc:dip/dport; further_info |
| ASA-6-414004  | 6        | Info         | TCP Syslog Server intf: IP_Address/port - Connection restored |
| ASA-6-414007  | 6        | Info         | TCP Syslog Server connection restored. New connections are allowed. |
| ASA-6-414008  | 6        | Info         | New connections are now allowed due to change of logging permit-hostdown policy. |
| ASA-6-415001  | 6        | Info         | HTTP - matched matched_string in policy-map map_name         |
| ASA-6-415002  | 6        | Info         | HTTP - matched matched_string in policy-map map_name         |
| ASA-6-415003  | 6        | Info         | HTTP - matched matched_string in policy-map map_name         |
| ASA-6-415017  | 6        | Info         | HTTP - matched_string in policy-map map_name                 |
| ASA-6-420004  | 6        | Info         | Virtual Sensor sensor_name was added on the AIP SSM          |
| ASA-6-420005  | 6        | Info         | Virtual Sensor sensor_name was deleted from the AIP SSM      |
| ASA-6-421002  | 6        | Info         | TCP\|UDP flow from interface_name:IP_address/port to interface_nam:IP_address/port bypassed application checking because the protocol is not supported. |
| ASA-6-421005  | 6        | Info         | interface_name:IP_address is counted as a user of application |
| ASA-6-421006  | 6        | Info         | There are number users of application accounted during the past 24 hours. |
| ASA-6-425001  | 6        | Info         | Redundant interface redundant_interface_name created.        |
| ASA-6-425002  | 6        | Info         | Redundant interface redundant_interface_name created.        |
| ASA-6-425003  | 6        | Info         | Interface interface_name added into redundant interface redundant_interface_name.#VALUE! |
| ASA-6-425004  | 6        | Info         | Interface interface_name removed from redundant interface redundant_interface_name. |
| ASA-6-426001  | 6        | Info         | PORT-CHANNEL:Interface ifc_name bundled into EtherChannel interface Port-channel num |
| ASA-6-426002  | 6        | Info         | PORT-CHANNEL:Interface ifc_name unbundled from EtherChannel interface Port-channel num |
| ASA-6-426003  | 6        | Info         | PORT-CHANNEL:Interface ifc_name1 has become standby in EtherChannel interface Port-channel num |
| ASA-6-426101  | 6        | Info         | PORT-CHANNEL:Interface ifc_name is allowed to bundle into EtherChannel interface port-channel id by CLACP |
| ASA-6-426102  | 6        | Info         | PORT-CHANNEL:Interface ifc_name is moved to standby in EtherChannel interface port-channel id by CLACP |
| ASA-6-426103  | 6        | Info         | PORT-CHANNEL:Interface ifc_name is selected to move from standby to bundle in EtherChannel interface port-channel id by CLACP |
| ASA-6-426104  | 6        | Info         | PORT-CHANNEL:Interface ifc_name is unselected in EtherChannel interface port-channel id by CLACP |
| ASA-6-428001  | 6        | Info         | WAAS confirmed from in_interface:src_ip_addr/src_port to out_interface:dest_ip_addr/dest_port |
| ASA-6-429005  | 6        | Info         | Set up authentication-proxy protocol_type rule for the CXSC action on interface interface_name for traffic destined to ip_address/port for policy_type service-policy. |
| ASA-6-429006  | 6        | Info         | Cleaned up authentication-proxy rule for the CXSC action on interface interface_name for traffic destined to ip_address for policy_type service-policy. |
| ASA-6-444103  | 6        | Info         | Shared licensetype license usage is over 90% capacity        |
| ASA-6-444104  | 6        | Info         | Shared licensetype license availability: value.              |
| ASA-6-444107  | 6        | Info         | Shared license service status on interface ifname            |
| ASA-6-444108  | 6        | Info         | Shared license state client id id                            |
| ASA-6-602101  | 6        | Info         | PMTU-D packet number bytes greater than effective mtu number dest_addr=dest_address |
| ASA-6-602103  | 6        | Info         | IPSEC: Received an ICMP Destination Unreachable from src_addr with suggested PMTU of rcvd_mtu; PMTU updated for SA with peer peer_addr |
| ASA-6-602104  | 6        | Info         | IPSEC: Received an ICMP Destination Unreachable from src_addr |
| ASA-6-602303  | 6        | Info         | IPSEC: An direction tunnel_type SA (SPI=spi) between local_IP and remote_IP (username) has been created. |
| ASA-6-602304  | 6        | Info         | IPSEC: An direction tunnel_type SA (SPI=spi) between local_IP and remote_IP (username) has been deleted. |
| ASA-6-603101  | 6        | Info         | PPTP received out of seq or duplicate pkt                    |
| ASA-6-603102  | 6        | Info         | PPP virtual interface interface_name - user: user aaa authentication started. |
| ASA-6-603103  | 6        | Info         | PPP virtual interface interface_name - user: user aaa authentication status |
| ASA-6-603104  | 6        | Info         | PPTP Tunnel created                                          |
| ASA-6-603105  | 6        | Info         | PPTP Tunnel deleted                                          |
| ASA-6-603106  | 6        | Info         | L2TP Tunnel created                                          |
| ASA-6-603107  | 6        | Info         | L2TP Tunnel deleted                                          |
| ASA-6-603108  | 6        | Info         | Built PPTP Tunnel at interface_name                          |
| ASA-6-603109  | 6        | Info         | Teardown PPPOE Tunnel at interface_name                      |
| ASA-6-604101  | 6        | Info         | DHCP client interface interface_name: Allocated ip = IP_address |
| ASA-6-604102  | 6        | Info         | DHCP client interface interface_name: address released       |
| ASA-6-604103  | 6        | Info         | DHCP daemon interface interface_name: address granted MAC_address (IP_address) |
| ASA-6-604104  | 6        | Info         | DHCP daemon interface interface_name: address released build_name (IP_address) |
| ASA-6-604201  | 6        | Info         | DHCPv6 PD client on interface <pd-client-iface> received delegated prefix <prefix> from DHCPv6 PD server <server-address> with preferred lifetime <in-seconds> seconds and valid lifetime <in-seconds> seconds |
| ASA-6-604202  | 6        | Info         | DHCPv6 PD client on interface <pd-client-iface> releasing delegated prefix <prefix> received from DHCPv6 PD server <server-address> |
| ASA-6-604203  | 6        | Info         | DHCPv6 PD client on interface <pd-client-iface> renewed delegated prefix <prefix> from DHCPv6 PD server <server-address> with preferred lifetime <in-seconds> seconds and valid lifetime <in-seconds> seconds |
| ASA-6-604204  | 6        | Info         | DHCPv6 delegated prefix <delegated prefix> got expired on interface <pd-client-iface> |
| ASA-6-604205  | 6        | Info         | DHCPv6 client on interface <client-iface> allocated address <ipv6-address> from DHCPv6 server <server-address> with preferred lifetime <in-seconds> seconds and valid lifetime <in-seconds> seconds |
| ASA-6-604206  | 6        | Info         | DHCPv6 client on interface <client-iface> releasing address <ipv6-address> received from DHCPv6 server <server-address> |
| ASA-6-604207  | 6        | Info         | DHCPv6 client on interface <client-iface> renewed address <ipv6-address> from DHCPv6 server <server-address> with preferred lifetime <in-seconds> seconds and valid lifetime <in-seconds> seconds |
| ASA-6-604208  | 6        | Info         | DHCPv6 client address <ipv6-address > got expired on interface <client-iface> |
| ASA-6-605004  | 6        | Info         | Login denied from source-address/source-port to interface:destination/service for user “username” |
| ASA-6-605005  | 6        | Info         | Login permitted from source-address/source-port to interface:destination/service for user “username” |
| ASA-6-606001  | 6        | Info         | ASDM session number number from IP_address started           |
| ASA-6-606002  | 6        | Info         | ASDM session number number from IP_address ended             |
| ASA-6-606003  | 6        | Info         | ASDM logging session number id from IP_address started id session ID assigned |
| ASA-6-606004  | 6        | Info         | ASDM logging session number id from IP_address ended         |
| ASA-6-607001  | 6        | Info         | Pre-allocate SIP connection_type secondary channel for interface_name:IP_address/port to interface_name:IP_address from string message |
| ASA-6-607003  | 6        | Info         | action_class: Received SIP req_resp req_resp_info from src_ifc:sip/sport to dest_ifc:dip/dport; further_info |
| ASA-6-608001  | 6        | Info         | Pre-allocate Skinny connection_type secondary channel for interface_name:IP_address to interface_name:IP_address from string message |
| ASA-6-610101  | 6        | Info         | Authorization failed: Cmd: command Cmdtype: command_modifier |
| ASA-6-611101  | 6        | Info         | User authentication succeeded: IP                            |
| ASA-6-611102  | 6        | Info         | User authentication failed: IP = IP address                  |
| ASA-6-611301  | 6        | Info         | VPN Client: NAT configured for Client Mode with no split tunneling: NAT address: mapped_address |
| ASA-6-611302  | 6        | Info         | VPN Client: NAT exemption configured for Network Extension Mode with no split tunneling |
| ASA-6-611303  | 6        | Info         | VPN Client: NAT configured for Client Mode with split tunneling: NAT address: mapped_address Split Tunnel Networks: IP_address/netmask IP_address/netmask |
| ASA-6-611304  | 6        | Info         | VPN Client: NAT exemption configured for Network Extension Mode with split tunneling: Split Tunnel Networks: IP_address/netmask IP_address/netmask |
| ASA-6-611305  | 6        | Info         | VPN Client: DHCP Policy installed: Primary DNS: IP_address Secondary DNS: IP_address Primary WINS: IP_address Secondary WINS: IP_address |
| ASA-6-611306  | 6        | Info         | VPN Client: Perfect Forward Secrecy Policy installed         |
| ASA-6-611307  | 6        | Info         | VPN Client: Head end: IP_address                             |
| ASA-6-611308  | 6        | Info         | VPN Client: Split DNS Policy installed: List of domains: string string |
| ASA-6-611309  | 6        | Info         | VPN Client: Disconnecting from head end and uninstalling previously downloaded policy: Head End: IP_address |
| ASA-6-611310  | 6        | Info         | VNP Client: XAUTH Succeeded: Peer: IP_address                |
| ASA-6-611311  | 6        | Info         | VNP Client: XAUTH Failed: Peer: IP_address                   |
| ASA-6-611312  | 6        | Info         | VPN Client: Backup Server List: reason                       |
| ASA-6-611314  | 6        | Info         | VPN Client: Load Balancing Cluster with Virtual IP: IP_address has redirected the to server IP_address |
| ASA-6-611315  | 6        | Info         | VPN Client: Disconnecting from Load Balancing Cluster member IP_address |
| ASA-6-611316  | 6        | Info         | VPN Client: Secure Unit Authentication Enabled               |
| ASA-6-611317  | 6        | Info         | VPN Client: Secure Unit Authentication Disabled              |
| ASA-6-611318  | 6        | Info         | VPN Client: User Authentication Enabled: Auth Server IP: IP_address Auth Server Port: port Idle Timeout: time |
| ASA-6-611319  | 6        | Info         | VPN Client: User Authentication Disabled                     |
| ASA-6-611320  | 6        | Info         | VPN Client: Device Pass Thru Enabled                         |
| ASA-6-611321  | 6        | Info         | VPN Client: Device Pass Thru Disabled                        |
| ASA-6-611322  | 6        | Info         | VPN Client: Extended XAUTH conversation initiated when SUA disabled |
| ASA-6-611323  | 6        | Info         | VPN Client: Duplicate split nw entry                         |
| ASA-6-613001  | 6        | Info         | Checksum Failure in database in area string Link State Id IP_address Old Checksum number New Checksum number |
| ASA-6-613002  | 6        | Info         | interface interface_name has zero bandwidth                  |
| ASA-6-613003  | 6        | Info         | IP_address netmask changed from area string to area string   |
| ASA-6-613014  | 6        | Info         | Base topology enabled on interface string attached to MTR compatible mode area string%ASA-6-613027: OSPF process number removed from interface interface_name |
| ASA-6-613028  | 6        | Info         | Unrecognized virtual interface intetface_name. Treat it as loopback stub route |
| ASA-6-613041  | 6        | Info         | OSPF-100 Areav string: LSA ID IP_address                     |
| ASA-6-613043  | 6        | Info         | N/A                                                          |
| ASA-6-613101  | 6        | Info         | Checksum Failure in database in area %s Link State Id %i Old Checksum %#x New Checksum %#x |
| ASA-6-613102  | 6        | Info         | interface %s has zero bandwidth                              |
| ASA-6-613103  | 6        | Info         | %i%m changed from area %AREA_ID_STR to area %AREA_ID_STR     |
| ASA-6-613104  | 6        | Info         | Unrecognized virtual interface %IF_NAME.                     |
| ASA-6-614001  | 6        | Info         | Split DNS: request patched from server: IP_address to server: IP_address |
| ASA-6-614002  | 6        | Info         | Split DNS: reply from server: IP_address reverse patched back to original server: IP_address |
| ASA-6-615001  | 6        | Info         | vlan number not available for firewall interface             |
| ASA-6-615002  | 6        | Info         | vlan number available for firewall interface                 |
| ASA-6-616001  | 6        | Info         | Pre-allocate MGCP data_channel connection for inside_interface:inside_address to outside_interface:outside_address/port from message_type message |
| ASA-6-617001  | 6        | Info         | GTPv version msg_type from source_interface:source_address/source_port not accepted by source_interface:dest_address/dest_port |
| ASA-6-617002  | 6        | Info         | Removing v1 PDP Context with TID tid from GGSN IP_address and SGSN IP_address |
| ASA-6-617003  | 6        | Info         | GTP Tunnel created from source_interface:source_address/source_port to source_interface:dest_address/dest_port |
| ASA-6-617004  | 6        | Info         | GTP connection created for response from source_interface:source_address/0 to source_interface:dest_address/dest_port |
| ASA-6-617100  | 6        | Info         | Teardown num_conns connection(s) for user user_ip            |
| ASA-6-618001  | 6        | Info         | Denied STUN packet <msg_type> from <ingress_ifc>:<source_addr>/<source_port> to <egress_ifc>:<destination_addr>/<destination_port> for connection <conn_id> |
| ASA-6-620001  | 6        | Info         | Pre-allocate CTIQBE {RTP \| RTCP} secondary channel for interface_name:outside_address[/outside_port] to interface_name:inside_address[/inside_port] from CTIQBE_message_name message |
| ASA-6-621001  | 6        | Info         | Interface interface_name does not support multicast          |
| ASA-6-621002  | 6        | Info         | Interface interface_name does not support multicast          |
| ASA-6-621003  | 6        | Info         | The event queue size has exceeded number                     |
| ASA-6-621006  | 6        | Info         | Mrib disconnected                                            |
| ASA-6-621007  | 6        | Info         | Bad register from interface_name:IP_address to IP_address for (IP_address |
| ASA-6-622001  | 6        | Info         | string tracked route network mask address                    |
| ASA-6-622101  | 6        | Info         | Starting regex table compilation for match_command; table entries = regex_num entries |
| ASA-6-622102  | 6        | Info         | Completed regex table compilation for match_command; table size = num bytes |
| ASA-6-634001  | 6        | Info         | DAP: User user                                               |
| ASA-6-713128  | 6        | Info         | Connection attempt to VCPIP redirected to VCA peer IP_address via load balancing |
| ASA-6-713145  | 6        | Info         | Detected Hardware Client in network extension mode           |
| ASA-6-713147  | 6        | Info         | Terminating tunnel to Hardware Client in network extension mode |
| ASA-6-713172  | 6        | Info         | Automatic NAT Detection Status: Remote end is\|is not behind a NAT device This end is\|is_not behind a NAT device |
| ASA-6-713177  | 6        | Info         | Received remote Proxy Host FQDN in ID Payload: Host Name: host_name Address IP_address |
| ASA-6-713184  | 6        | Info         | Client Type: Client_type Client Application Version: Application_version_string |
| ASA-6-713202  | 6        | Info         | Duplicate IP_addr packet detected.                           |
| ASA-6-713211  | 6        | Info         | Adding static route for L2L peer coming in on a dynamic map. address: IP_address |
| ASA-6-713213  | 6        | Info         | Deleting static route for L2L peer that came in on a dynamic map. address: IP_address |
| ASA-6-713215  | 6        | Info         | No match against Client Type and Version rules. Client: type version is/is not allowed by default |
| ASA-6-713219  | 6        | Info         | Queuing KEY-ACQUIRE messages to be processed when P1 SA is complete. |
| ASA-6-713220  | 6        | Info         | De-queuing KEY-ACQUIRE messages that were left pending.      |
| ASA-6-713228  | 6        | Info         | Assigned private IP address assigned_private_IP              |
| ASA-6-713235  | 6        | Info         | Attempt to send an IKE packet from standby unit. Dropping the packet! |
| ASA-6-713256  | 6        | Info         | IP = peer-IP                                                 |
| ASA-6-713265  | 6        | Info         | Adding static route for L2L peer coming in on a dynamic map. address: IP_address |
| ASA-6-713267  | 6        | Info         | Deleting static route for L2L peer that came in on a dynamic map. address: IP_address |
| ASA-6-713269  | 6        | Info         | Detected Hardware Client in network extension mode           |
| ASA-6-713271  | 6        | Info         | Terminating tunnel to Hardware Client in network extension mode |
| ASA-6-713905  | 6        | Info         | Descriptive_event_string.                                    |
| ASA-6-716001  | 6        | Info         | Group group User user WebVPN session started.                |
| ASA-6-716002  | 6        | Info         | Group group User user WebVPN session terminated: reason.     |
| ASA-6-716003  | 6        | Info         | Group group User user WebVPN access GRANTED: url             |
| ASA-6-716004  | 6        | Info         | Group group User user WebVPN access DENIED to specified location: url |
| ASA-6-716005  | 6        | Info         | Group group User user WebVPN ACL Parse Error: reason         |
| ASA-6-716006  | 6        | Info         | Group name User user WebVPN session terminated. Idle timeout. |
| ASA-6-716009  | 6        | Info         | Group group User user WebVPN session not allowed. WebVPN ACL parse error. |
| ASA-6-716038  | 6        | Info         | Authentication: successful                                   |
| ASA-6-716039  | 6        | Info         | Authentication: rejected                                     |
| ASA-6-716040  | 6        | Info         | Reboot pending                                               |
| ASA-6-716041  | 6        | Info         | access-list acl_ID action url url hit_cnt count              |
| ASA-6-716042  | 6        | Info         | access-list acl_ID action tcp source_interface/source_address (source_port) - dest_interface/dest_address(dest_port) hit-cnt count |
| ASA-6-716043  | 6        | Info         | Group group-name                                             |
| ASA-6-716049  | 6        | Info         | Group group-name User user-name IP IP_address Empty SVC ACL. |
| ASA-6-716050  | 6        | Info         | Error adding to ACL: ace_command_line                        |
| ASA-6-716051  | 6        | Info         | Group group-name User user-name IP IP_address Error adding dynamic ACL for user. |
| ASA-6-716055  | 6        | Info         | Group group-name User user-name IP IP_address Authentication to SSO server name: name type type succeeded |
| ASA-6-716058  | 6        | Info         | Group group User user IP ip AnyConnect session lost connection. Waiting to resume. |
| ASA-6-716059  | 6        | Info         | Group group User user IP ip AnyConnect session resumed. Connection from ip2 |
| ASA-6-716060  | 6        | Info         | Group group User user IP ip Terminated AnyConnect session in inactive state to accept a new connection. License limit reached. |
| ASA-6-717003  | 6        | Info         | Certificate received from Certificate Authority for trustpoint trustpoint_name. |
| ASA-6-717004  | 6        | Info         | PKCS #12 export failed for trustpoint trustpoint_name.       |
| ASA-6-717005  | 6        | Info         | PKCS #12 export succeeded for trustpoint trustpoint_name.    |
| ASA-6-717006  | 6        | Info         | PKCS #12 import failed for trustpoint trustpoint_name.       |
| ASA-6-717007  | 6        | Info         | PKCS #12 import succeeded for trustpoint trustpoint_name.    |
| ASA-6-717016  | 6        | Info         | Removing expired CRL from the CRL cache. Issuer: issuer      |
| ASA-6-717022  | 6        | Info         | Certificate was successfully validated. certificate_identifiers |
| ASA-6-717028  | 6        | Info         | Certificate chain was successfully validated additional info. |
| ASA-6-717033  | 6        | Info         | OCSP response status - Successful.                           |
| ASA-6-717043  | 6        | Info         | Local CA Server certificate enrollment related info for user: user. Info: info. |
| ASA-6-717047  | 6        | Info         | Revoked certificate issued to user: username                 |
| ASA-6-717048  | 6        | Info         | Unrevoked certificate issued to user: username               |
| ASA-6-717056  | 6        | Info         | Attempting type revocation check from Src Interface:Src IP/Src Port to Dst IP/Dst Port using protocol |
| ASA-6-717058  | 6        | Info         | Automatic import of trustpool certificate bundle is successful: <No change in trustpool bundle> \| <Trustpool updated in flash> |
| ASA-6-717059  | 6        | Info         | Peer certificate with serial number: <serial>                |
| ASA-6-718003  | 6        | Info         | Got unknown peer message message_number from IP_address      |
| ASA-6-718004  | 6        | Info         | Got unknown internal message message_number                  |
| ASA-6-718013  | 6        | Info         | Peer IP_address is not answering HELLO                       |
| ASA-6-718027  | 6        | Info         | Received unexpected KEEPALIVE request from IP_address        |
| ASA-6-718030  | 6        | Info         | Received planned OOS from IP_address                         |
| ASA-6-718037  | 6        | Info         | Master processed number_of_timeouts timeouts                 |
| ASA-6-718038  | 6        | Info         | Slave processed number_of_timeouts timeouts                  |
| ASA-6-718039  | 6        | Info         | Process dead peer IP_address                                 |
| ASA-6-718040  | 6        | Info         | Timed-out exchange ID exchange_ID not found                  |
| ASA-6-718051  | 6        | Info         | Deleted secure tunnel to peer IP_address                     |
| ASA-6-719001  | 6        | Info         | Email Proxy session could not be established: session limit of maximum_sessions has been reached. |
| ASA-6-719003  | 6        | Info         | Email Proxy session pointer resources have been freed for source_address. |
| ASA-6-719004  | 6        | Info         | Email Proxy session pointer has been successfully established for source_address. |
| ASA-6-719010  | 6        | Info         | protocol Email Proxy feature is disabled on interface interface_name. |
| ASA-6-719011  | 6        | Info         | Protocol Email Proxy feature is enabled on interface interface_name. |
| ASA-6-719012  | 6        | Info         | Email Proxy server listening on port port for mail protocol protocol. |
| ASA-6-719013  | 6        | Info         | Email Proxy server closing port port for mail protocol protocol. |
| ASA-6-719017  | 6        | Info         | WebVPN user: vpnuser invalid dynamic ACL.                    |
| ASA-6-719018  | 6        | Info         | WebVPN user: vpnuser ACL ID acl_ID not found                 |
| ASA-6-719019  | 6        | Info         | WebVPN user: vpnuser authorization failed.                   |
| ASA-6-719020  | 6        | Info         | WebVPN user vpnuser authorization completed successfully.    |
| ASA-6-719021  | 6        | Info         | WebVPN user: vpnuser is not checked against ACL.             |
| ASA-6-719022  | 6        | Info         | WebVPN user vpnuser has been authenticated.                  |
| ASA-6-719023  | 6        | Info         | WebVPN user vpnuser has not been successfully authenticated. Access denied. |
| ASA-6-719024  | 6        | Info         | Email Proxy piggyback auth fail: session = pointer user=vpnuser addr=source_address |
| ASA-6-719025  | 6        | Info         | Email Proxy DNS name resolution failed for hostname.         |
| ASA-6-719026  | 6        | Info         | Email Proxy DNS name hostname resolved to IP_address.        |
| ASA-6-720002  | 6        | Info         | (VPN-unit) Starting VPN Stateful Failover Subsystem...       |
| ASA-6-720003  | 6        | Info         | (VPN-unit) Initialization of VPN Stateful Failover Component completed successfully |
| ASA-6-720004  | 6        | Info         | (VPN-unit) VPN failover main thread started.                 |
| ASA-6-720005  | 6        | Info         | (VPN-unit) VPN failover timer thread started.                |
| ASA-6-720006  | 6        | Info         | (VPN-unit) VPN failover sync thread started.                 |
| ASA-6-720010  | 6        | Info         | (VPN-unit) VPN failover client is being disabled             |
| ASA-6-720012  | 6        | Info         | (VPN-unit) Failed to update IPSec failover runtime data on the standby unit. |
| ASA-6-720014  | 6        | Info         | (VPN-unit) Phase 2 connection entry (msg_id=message_number   |
| ASA-6-720015  | 6        | Info         | (VPN-unit) Cannot found Phase 1 SA for Phase 2 connection entry (msg_id=message_number |
| ASA-6-720023  | 6        | Info         | (VPN-unit) HA status callback: Peer is not present.          |
| ASA-6-720024  | 6        | Info         | (VPN-unit) HA status callback: Control channel is status.    |
| ASA-6-720025  | 6        | Info         | (VPN-unit) HA status callback: Data channel is status.       |
| ASA-6-720026  | 6        | Info         | (VPN-unit) HA status callback: Current progression is being aborted. |
| ASA-6-720027  | 6        | Info         | (VPN-unit) HA status callback: My state state.               |
| ASA-6-720028  | 6        | Info         | (VPN-unit) HA status callback: Peer state state.             |
| ASA-6-720029  | 6        | Info         | (VPN-unit) HA status callback: Start VPN bulk sync state.    |
| ASA-6-720030  | 6        | Info         | (VPN-unit) HA status callback: Stop bulk sync state.         |
| ASA-6-720032  | 6        | Info         | (VPN-unit) HA status callback: id=ID                         |
| ASA-6-720037  | 6        | Info         | (VPN-unit) HA progression callback: id=id                    |
| ASA-6-720039  | 6        | Info         | (VPN-unit) VPN failover client is transitioning to active state |
| ASA-6-720040  | 6        | Info         | (VPN-unit) VPN failover client is transitioning to standby state. |
| ASA-6-720045  | 6        | Info         | (VPN-unit) Start bulk syncing of state information on standby unit. |
| ASA-6-720046  | 6        | Info         | (VPN-unit) End bulk syncing of state information on standby unit |
| ASA-6-720056  | 6        | Info         | (VPN-unit) VPN Stateful failover Message Thread is being disabled. |
| ASA-6-720057  | 6        | Info         | (VPN-unit) VPN Stateful failover Message Thread is enabled.  |
| ASA-6-720058  | 6        | Info         | (VPN-unit) VPN Stateful failover Timer Thread is disabled.   |
| ASA-6-720059  | 6        | Info         | (VPN-unit) VPN Stateful failover Timer Thread is enabled.    |
| ASA-6-720060  | 6        | Info         | (VPN-unit) VPN Stateful failover Sync Thread is disabled.    |
| ASA-6-720061  | 6        | Info         | (VPN-unit) VPN Stateful failover Sync Thread is enabled.     |
| ASA-6-720062  | 6        | Info         | (VPN-unit) Active unit started bulk sync of state information to standby unit. |
| ASA-6-720063  | 6        | Info         | (VPN-unit) Active unit completed bulk sync of state information to standby. |
| ASA-6-721001  | 6        | Info         | (device) WebVPN Failover SubSystem started successfully.(device) either WebVPN-primary or WebVPN-secondary. |
| ASA-6-721002  | 6        | Info         | (device) HA status change: event event                       |
| ASA-6-721003  | 6        | Info         | (device) HA progression change: event event                  |
| ASA-6-721004  | 6        | Info         | (device) Create access list list_name on standby unit.       |
| ASA-6-721005  | 6        | Info         | (device) Fail to create access list list_name on standby unit. |
| ASA-6-721006  | 6        | Info         | (device) Update access list list_name on standby unit.       |
| ASA-6-721008  | 6        | Info         | (device) Delete access list list_name on standby unit.       |
| ASA-6-721009  | 6        | Info         | (device) Fail to delete access list list_name on standby unit. |
| ASA-6-721010  | 6        | Info         | (device) Add access list rule list_name                      |
| ASA-6-721012  | 6        | Info         | (device) Enable APCF XML file file_name on the standby unit. |
| ASA-6-721014  | 6        | Info         | (device) Disable APCF XML file file_name on the standby unit. |
| ASA-6-721016  | 6        | Info         | (device) WebVPN session for client user user_name            |
| ASA-6-721018  | 6        | Info         | (device) WebVPN session for client user user_name            |
| ASA-6-722013  | 6        | Info         | Group group User user-name IP IP_address SVC Message: type-num/INFO: message |
| ASA-6-722014  | 6        | Info         | Group group User user-name IP IP_address SVC Message: type-num/INFO: message |
| ASA-6-722022  | 6        | Info         | Group group-name User user-name IP addr (TCP \| UDP) connection established (with \| without) compression |
| ASA-6-722023  | 6        | Info         | Group group User user-name IP IP_address SVC connection terminated {with\|without} compression |
| ASA-6-722024  | 6        | Info         | SVC Global Compression Enabled                               |
| ASA-6-722025  | 6        | Info         | SVC Global Compression Disabled                              |
| ASA-6-722026  | 6        | Info         | Group group User user-name IP IP_address SVC compression history reset |
| ASA-6-722027  | 6        | Info         | Group group User user-name IP IP_address SVC decompression history reset |
| ASA-6-722051  | 6        | Info         | Group group-policy User username IP public-ip Address assigned-ip assigned to session |
| ASA-6-722053  | 6        | Info         | Group g User u IP ip Unknown client user-agent connection.   |
| ASA-6-722055  | 6        | Info         | Group group-policy User username IP public-ip Client Type: user-agent |
| ASA-6-723001  | 6        | Info         | Group group-name                                             |
| ASA-6-723002  | 6        | Info         | Group group-name                                             |
| ASA-6-725001  | 6        | Info         | Starting SSL handshake with peer-type interface:src-ip/src-port to dst-ip/dst-port for protocol session. |
| ASA-6-725002  | 6        | Info         | Device completed SSL handshake with peer-type interface:src-ip/src-port to dst-ip/dst-port for protocol-version session |
| ASA-6-725003  | 6        | Info         | SSL peer-type interface:src-ip/src-port to dst-ip/dst-port request to resume previous session. |
| ASA-6-725004  | 6        | Info         | Device requesting certificate from SSL peer-type interface:src-ip/src-port to dst-ip/dst-port for authentication. |
| ASA-6-725005  | 6        | Info         | SSL peer-type interface:src-ip/src-port to dst-ip/dst-port requesting our device certificate for authentication. |
| ASA-6-725006  | 6        | Info         | Device failed SSL handshake with peer-type interface:src-ip/src-port to dst-ip/dst-port |
| ASA-6-725007  | 6        | Info         | SSL session with peer-type interface:src-ip/src-port to dst-ip/dst-port terminated. |
| ASA-6-725016  | 6        | Info         | Device selects trust-point <trustpoint> for peer-type interface:src-ip/src-port to dst-ip/dst-port |
| ASA-6-726001  | 6        | Info         | Inspected im_protocol im_service Session between Client im_client_1 and im_client_2 Packet flow from src_ifc:/sip/sport to dest_ifc:/dip/dport Action: action Matched Class class_map_id class_map_name |
| ASA-6-730004  | 6        | Info         | Group groupname User username IP ipaddr VLAN ID vlanid from AAA ignored. |
| ASA-6-730005  | 6        | Info         | Group groupname User username IP ipaddr VLAN ID vlanid from AAA is invalid. |
| ASA-6-730008  | 6        | Info         | Group groupname                                              |
| ASA-6-731001  | 6        | Info         | NAC policy added: name: policyname Type: policytype.         |
| ASA-6-731002  | 6        | Info         | NAC policy deleted: name: policyname Type: policytype.       |
| ASA-6-731003  | 6        | Info         | nac-policy unused: name: policyname Type: policytype.        |
| ASA-6-732001  | 6        | Info         | Group groupname                                              |
| ASA-6-732002  | 6        | Info         | Group groupname                                              |
| ASA-6-732003  | 6        | Info         | Group groupname                                              |
| ASA-6-734001  | 6        | Info         | DAP: User user                                               |
| ASA-6-737005  | 6        | Info         | IPAA: DHCP configured                                        |
| ASA-6-737006  | 6        | Info         | IPAA: Local pool request succeeded for tunnel-group 'tunnel-group' |
| ASA-6-737009  | 6        | Info         | IPAA: AAA assigned address ip-address                        |
| ASA-6-737010  | 6        | Info         | IPAA: AAA assigned address ip-address                        |
| ASA-6-737014  | 6        | Info         | IPAA: Freeing AAA address ip-address                         |
| ASA-6-737015  | 6        | Info         | IPAA: Freeing DHCP address ip-address                        |
| ASA-6-737016  | 6        | Info         | IPAA: Freeing local pool address ip-address                  |
| ASA-6-737017  | 6        | Info         | IPAA: DHCP request attempt num succeeded                     |
| ASA-6-737026  | 6        | Info         | IPAA: Client assigned ip-address from local pool             |
| ASA-6-737029  | 6        | Info         | IPAA: Adding ip-address to standby: succeeded                |
| ASA-6-737031  | 6        | Info         | IPAA: Removing %m from standby: succeeded                    |
| ASA-6-737036  | 6        | Info         | IPAA: Session=<session>                                      |
| ASA-6-741000  | 6        | Info         | Coredump filesystem image created on variable 1 -size variable 2 MB |
| ASA-6-741001  | 6        | Info         | Coredump filesystem image on variable 1 - resized from variable 2 MB to variable 3 MB |
| ASA-6-741002  | 6        | Info         | Coredump log and filesystem contents cleared on variable 1   |
| ASA-6-741003  | 6        | Info         | Coredump filesystem and its contents removed on variable 1   |
| ASA-6-741004  | 6        | Info         | Coredump configuration reset to default values               |
| ASA-6-746001  | 6        | Info         | user-identity: activated import user groups \| activated host names \| user-to-IP address databases download started |
| ASA-6-746002  | 6        | Info         | user-identity: activated import user groups \| activated host names \| user-to-IP address databases download complete |
| ASA-6-746008  | 6        | Info         | user-identity: NetBIOS Probe Process started                 |
| ASA-6-746009  | 6        | Info         | user-identity: NetBIOS Probe Process stopped                 |
| ASA-6-746017  | 6        | Info         | user-identity: Update import-user domain_name\\group_name    |
| ASA-6-746018  | 6        | Info         | user-identity: Update import-user domain_name\\group_name done |
| ASA-6-747004  | 6        | Info         | Clustering: state machine changed from state state-name to state-name. |
| ASA-6-748008  | 6        | Info         | [CPU load percentage \| memory load percentage ] of module slot_number in chassis chassis_number (member-name ) exceeds overflow protection threshold [CPU percentage \| memory percentage ]. System may be oversubscribed on member failure. |
| ASA-6-748009  | 6        | Info         | [CPU load percentage \| memory load percentage] of chassis chassis_number exceeds overflow protection threshold [CPU percentage \| memory percentage}. System may be oversubscribed on chassis failure. |
| ASA-6-751023  | 6        | Info         | Local a:p Remote: a:p Username:n Unknown client connection   |
| ASA-6-751026  | 6        | Info         | Local: localIP:port Remote: remoteIP:port Username: username/group IKEv2 Client OS: client-os Client: client-name client-version |
| ASA-6-767001  | 6        | Info         | Inspect-name: Dropping an unsupported IPv6/IP46/IP64 packet from interface:IP Addr to interface:IP Addr (fail-close) |
| ASA-6-772005  | 6        | Info         | REAUTH: user username passed authentication                  |
| ASA-6-775001  | 6        | Info         | Scansafe: protocol connection conn_id from interface_name:real_address/real_port [(idfw_user)] to interface_name:real_address/real_port redirected to server_interface_name:server_ip_address |
| ASA-6-775003  | 6        | Info         | Scansafe:protocol connection conn_id from interface_name:real_address/real_port [(idfw_user)] to interface_name:real_address/real_port is whitelisted. |
| ASA-6-775005  | 6        | Info         | Scansafe: Primary server ip_address is reachable now         |
| ASA-6-775006  | 6        | Info         | Primary server interface:ip_address is not reachable and backup server interface:ip_address is now active |
| ASA-6-776008  | 6        | Info         | CTS SXP: Connection with peer IP (instance connection instance num) state changed from original state to final state. |
| ASA-6-776251  | 6        | Info         | CTS SGT-MAP: Binding binding IP - SGname(SGT) from source name added to binding manager. |
| ASA-6-776253  | 6        | Info         | CTS SGT-MAP: Binding binding IP - new SGname(SGT) from new source name changed from old sgt: old SGname(SGT) from old source old source name. |
| ASA-6-776303  | 6        | Info         | CTS Policy: Security-group name sgname is resolved to security-group tag sgt |
| ASA-6-776311  | 6        | Info         | CTS Policy: Previously unresolved security-group name sgname is now resolved to security-group tag sgt |
| ASA-6-778001  | 6        | Info         | VXLAN: Invalid VXLAN segment-id segment-id for protocol from ifc-name:(IP-address/port) to ifc-name:(IP-address/port). |
| ASA-6-778002  | 6        | Info         | VXLAN: There is no VNI interface for segment-id segment-id.  |
| ASA-6-778003  | 6        | Info         | VXLAN: Invalid VXLAN segment-id segment-id for protocol from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP. |
| ASA-6-778004  | 6        | Info         | VXLAN: Invalid VXLAN header for protocol from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP. |
| ASA-6-778005  | 6        | Info         | VXLAN: Packet with VXLAN segment-id segment-id from ifc-name is denied by FP L2 check. |
| ASA-6-778006  | 6        | Info         | VXLAN: Invalid VXLAN UDP checksum from ifc-name:(IP-address/port) to ifc-name:(IP-address/port) in FP. |
| ASA-6-778007  | 6        | Info         | VXLAN: Packet from ifc-name:IP-address/port to IP-address/port was discarded due to invalid NVE peer. |
| ASA-6-779001  | 6        | Info         | STS: Out-tag lookup failed for in-tag segment-id of protocol from ifc-name:IP-address/port to IP-address/port. |
| ASA-6-779002  | 6        | Info         | STS: STS and NAT locate different egress interface for segment-id segment-id |
| ASA-6-780001  | 6        | Info         | RULE ENGINE: Started compilation for access-group transaction - description of the transaction. |
| ASA-6-780002  | 6        | Info         | RULE ENGINE: Finished compilation for access-group transaction - description of the transaction. |
| ASA-6-780003  | 6        | Info         | RULE ENGINE: Started compilation for nat transaction - description of the transaction. |
| ASA-6-780004  | 6        | Info         | RULE ENGINE: Finished compilation for nat transaction - description of the transaction. |
| ASA-6-803001  | 6        | Info         | Flow offloaded: connection conn_id outside_ifc:outside_addr/outside_port (mapped_addr/mapped_port) inside_ifc:inside_addr/inside_port (mapped_addr/mapped_port) Protocol OR Bypass is continuing after power up |
| ASA-6-803002  | 6        | Info         | Flow is no longer offloaded: connection conn_id outside_ifc:outside_addr/outside_port (mapped_addr/mapped_port) inside_ifc:inside_addr/inside_port (mapped_addr/mapped_port) Protocol |
| ASA-6-803003  | 6        | Info         | User disabled bypass manually on GigabitEthernet 1/1-1/2     |
| ASA-6-804001  | 6        | Info         | Interface GigabitEthernet1/3 1000BaseSX SFP has been inserted |
| ASA-6-804002  | 6        | Info         | Interface GigabitEthernet1/3 SFP has been removed            |
| ASA-6-805001  | 6        | Info         | Flow offloaded: connection conn_id outside_ifc:outside_addr/outside_port (mapped_addr/mapped_port) inside_ifc:inside_addr/inside_port (mapped_addr/mapped_port) Protocol |
| ASA-6-805002  | 6        | Info         | Flow is no longer offloaded: connection conn_id outside_ifc:outside_addr/outside_port (mapped_addr/mapped_port) inside_ifc:inside_addr/inside_port (mapped_addr/mapped_port) Protocol |
| ASA-6-805003  | 6        | Info         | Flow could not be offloaded: connection <conn_id> <outside_ifc>:<outside_addr>/<outside_port> (<mapped_addr>/<mapped_port>) < inside_ifc>:<inside_addr>/<inside_port> (<mapped_addr>/<mapped_port>) <Protocol> |
| ASA-6-806001  | 6        | Info         | Primary alarm CPU temperature is High temperature            |
| ASA-6-806002  | 6        | Info         | Primary alarm for CPU high temperature is cleared            |
| ASA-6-806003  | 6        | Info         | Primary alarm CPU temperature is Low temperature             |
| ASA-6-806004  | 6        | Info         | Primary alarm for CPU Low temperature is cleared             |
| ASA-6-806005  | 6        | Info         | Secondary alarm CPU temperature is High temperature          |
| ASA-6-806006  | 6        | Info         | Secondary alarm for CPU high temperature is cleared          |
| ASA-6-806007  | 6        | Info         | Secondary alarm CPU temperature is Low temperature           |
| ASA-6-806008  | 6        | Info         | Secondary alarm for CPU Low temperature is cleared           |
| ASA-6-806009  | 6        | Info         | Alarm asserted for ALARM_IN_1 description                    |
| ASA-6-806010  | 6        | Info         | Alarm cleared for ALARM_IN_1 alarm_1_description             |
| ASA-6-806011  | 6        | Info         | Alarm asserted for ALARM_IN_2 description                    |
| ASA-6-806012  | 6        | Info         | Alarm cleared for ALARM_IN_2 alarm_2_description             |
| ASA-6-8300001 | 6        | Info         | VPN session redistribution <variable 1>                      |
| ASA-6-8300002 | 6        | Info         | Moved <variable 1> sessions to <variable 2>                  |
| ASA-6-8300004 | 6        | Info         | <variable 1> request to move <variable 2> sessions from <variable 3> to <variable 4> |
| ASA-7-108006  | 7        | Debug        | Detected ESMTP size violation from src_ifc:sip\|sport to dest_ifc:dip\|dport;declared size is: decl_size |
| ASA-7-109014  | 7        | Debug        | A non-Telnet connection was denied to the configured virtual Telnet IP address. |
| ASA-7-109021  | 7        | Debug        | Uauth null proxy error                                       |
| ASA-7-111009  | 7        | Debug        | User user executed cmd:string                                |
| ASA-7-113028  | 7        | Debug        | Extraction of username from VPN client certificate has string. [Request num] |
| ASA-7-199019  | 7        | Debug        | syslog                                                       |
| ASA-7-304005  | 7        | Debug        | URL Server IP_address request pending URL url                |
| ASA-7-304009  | 7        | Debug        | Ran out of buffer blocks specified by url-block command      |
| ASA-7-333004  | 7        | Debug        | EAP-SQ response invalid - context:EAP-context                |
| ASA-7-333005  | 7        | Debug        | EAP-SQ response contains invalid TLV(s) - context:EAP-context |
| ASA-7-333006  | 7        | Debug        | EAP-SQ response with missing TLV(s) - context:EAP-context    |
| ASA-7-333007  | 7        | Debug        | EAP-SQ response TLV has invalid length - context:EAP-context |
| ASA-7-333008  | 7        | Debug        | EAP-SQ response has invalid nonce TLV - context:EAP-context  |
| ASA-7-335007  | 7        | Debug        | NAC Default ACL not configured - host-address                |
| ASA-7-342001  | 7        | Debug        | REST API Agent started successfully.                         |
| ASA-7-342005  | 7        | Debug        | REST API image has been installed successfully.              |
| ASA-7-342007  | 7        | Debug        | REST API image has been uninstalled successfully.            |
| ASA-7-419003  | 7        | Debug        | Cleared TCP urgent flag                                      |
| ASA-7-421004  | 7        | Debug        | Failed to inject {TCP\|UDP} packet from IP_address/port to IP_address/port |
| ASA-7-609001  | 7        | Debug        | Built local-host zone_name/*: ip_address                     |
| ASA-7-609002  | 7        | Debug        | Teardown local-host zone_name/*: ip_address duration time    |
| ASA-7-701001  | 7        | Debug        | alloc_user() out of Tcp_user objects                         |
| ASA-7-701002  | 7        | Debug        | alloc_user() out of Tcp_proxy objects                        |
| ASA-7-702307  | 7        | Debug        | IPSEC: An direction tunnel_type SA (SPI=spi) between local_IP and remote_IP (username) is rekeying due to data rollover. |
| ASA-7-703001  | 7        | Debug        | H.225 message received from interface_name:IP_address/port to interface_name:IP_address/port is using an unsupported version number |
| ASA-7-703002  | 7        | Debug        | Received H.225 Release Complete with newConnectionNeeded for interface_name:IP_address to interface_name:IP_address/port |
| ASA-7-703008  | 7        | Debug        | Allowing early-message: %s before SETUP from %s:%Q/%d to %s:%Q/%d |
| ASA-7-709001  | 7        | Debug        | FO replication failed: cmd=command returned=code             |
| ASA-7-709002  | 7        | Debug        | FO unreplicable: cmd=command                                 |
| ASA-7-710001  | 7        | Debug        | TCP access requested from source_address/source_port to interface_name:dest_address/service |
| ASA-7-710002  | 7        | Debug        | {TCP\|UDP} access permitted from source_address/source_port to interface_name:dest_address/service |
| ASA-7-710004  | 7        | Debug        | TCP connection limit exceeded from Src_ip/Src_port to In_name:Dest_ip/Dest_port (current connections/connection limit = Curr_conn/Conn_lmt) |
| ASA-7-710005  | 7        | Debug        | {TCP\|UDP} request discarded from source_address/source_port to interface_name:dest_address/service |
| ASA-7-710006  | 7        | Debug        | protocol request discarded from source_address to interface_name:dest_address |
| ASA-7-710007  | 7        | Debug        | NAT-T keepalive received from 86.1.161.1/1028 to outside:86:1.129.1/4500 |
| ASA-7-711001  | 7        | Debug        | debug_trace_msg                                              |
| ASA-7-711003  | 7        | Debug        | Unknown/Invalid interface identifier(vpifnum) detected.      |
| ASA-7-711006  | 7        | Debug        | CPU profiling has started for n-samples samples. Reason: reason-string. |
| ASA-7-713024  | 7        | Debug        | Group group IP ip Received local Proxy Host data in ID Payload: Address IP_address |
| ASA-7-713025  | 7        | Debug        | Received remote Proxy Host data in ID Payload: Address IP_address |
| ASA-7-713028  | 7        | Debug        | Received local Proxy Range data in ID Payload: Addresses IP_address - IP_address |
| ASA-7-713029  | 7        | Debug        | Received remote Proxy Range data in ID Payload: Addresses IP_address - IP_address |
| ASA-7-713034  | 7        | Debug        | Received local IP Proxy Subnet data in ID Payload: Address IP_address |
| ASA-7-713035  | 7        | Debug        | Group group IP ip Received remote IP Proxy Subnet data in ID Payload: Address IP_address |
| ASA-7-713039  | 7        | Debug        | Send failure: Bytes (number)                                 |
| ASA-7-713040  | 7        | Debug        | Could not find connection entry and can not encrypt: msgid message_number |
| ASA-7-713052  | 7        | Debug        | User (user) authenticated.                                   |
| ASA-7-713066  | 7        | Debug        | IKE Remote Peer configured for SA: SA_name                   |
| ASA-7-713094  | 7        | Debug        | Cert validation failure: handle invalid for Main/Aggressive Mode Initiator/Responder! |
| ASA-7-713099  | 7        | Debug        | Tunnel Rejected: Received NONCE length number is out of range! |
| ASA-7-713103  | 7        | Debug        | Invalid (NULL) secret key detected while computing hash      |
| ASA-7-713104  | 7        | Debug        | Attempt to get Phase 1 ID data failed while hash computation |
| ASA-7-713113  | 7        | Debug        | Deleting IKE SA with associated IPSec connection entries. IKE peer: IP_address |
| ASA-7-713114  | 7        | Debug        | Connection entry (conn entry internal address) points to IKE SA (SA_internal_address) for peer IP_address |
| ASA-7-713117  | 7        | Debug        | Received Invalid SPI notify (SPI SPI_Value)!                 |
| ASA-7-713121  | 7        | Debug        | Keep-alive type for this connection: keepalive_type          |
| ASA-7-713143  | 7        | Debug        | Processing firewall record. Vendor: vendor(id)               |
| ASA-7-713160  | 7        | Debug        | Remote user (session Id - id) has been granted access by the Firewall Server |
| ASA-7-713164  | 7        | Debug        | The Firewall Server has requested a list of active user sessions |
| ASA-7-713169  | 7        | Debug        | IKE Received delete for rekeyed SA IKE peer: IP_address      |
| ASA-7-713170  | 7        | Debug        | Group group IP ip IKE Received delete for rekeyed centry IKE peer: IP_address |
| ASA-7-713171  | 7        | Debug        | NAT-Traversal sending NAT-Original-Address payload           |
| ASA-7-713187  | 7        | Debug        | Tunnel Rejected: IKE peer does not match remote peer as defined in L2L policy IKE peer address: IP_address |
| ASA-7-713190  | 7        | Debug        | Got bad refCnt (ref_count_value) assigning IP_address (IP_address) |
| ASA-7-713204  | 7        | Debug        | Adding static route for client address: IP_address           |
| ASA-7-713221  | 7        | Debug        | Static Crypto Map check                                      |
| ASA-7-713222  | 7        | Debug        | Group group Username username IP ip Static Crypto Map check  |
| ASA-7-713223  | 7        | Debug        | Static Crypto Map check                                      |
| ASA-7-713224  | 7        | Debug        | Static Crypto Map Check by-passed: Crypto map entry incomplete! |
| ASA-7-713225  | 7        | Debug        | [IKEv1]                                                      |
| ASA-7-713233  | 7        | Debug        | (VPN-unit) Remote network (remote network) validated for network extension mode. |
| ASA-7-713234  | 7        | Debug        | (VPN-unit) Remote network (remote network) from network extension mode client mismatches AAA configuration (aaa network). |
| ASA-7-713236  | 7        | Debug        | IKE_DECODE tx/rx Message (msgid=msgid) with payloads:payload1 (payload1_len) + payload2 (payload2_len)...total length: tlen |
| ASA-7-713263  | 7        | Debug        | Received local IP Proxy Subnet data in ID Payload: Address IP_address |
| ASA-7-713264  | 7        | Debug        | Received local IP Proxy Subnet data in ID Payload: Address IP_address |
| ASA-7-713273  | 7        | Debug        | Deleting static route for client address: IP_Address IP_Address address of client whose route is being removed |
| ASA-7-713906  | 7        | Debug        | Descriptive_event_string.                                    |
| ASA-7-714001  | 7        | Debug        | description_of_event_or_packet                               |
| ASA-7-714002  | 7        | Debug        | IKE Initiator starting QM: msg id = message_number           |
| ASA-7-714003  | 7        | Debug        | IKE Responder starting QM: msg id = message_number           |
| ASA-7-714004  | 7        | Debug        | IKE Initiator sending 1st QM pkt: msg id = message_number    |
| ASA-7-714005  | 7        | Debug        | IKE Responder sending 2nd QM pkt: msg id = message_number    |
| ASA-7-714006  | 7        | Debug        | IKE Initiator sending 3rd QM pkt: msg id = message_number    |
| ASA-7-714007  | 7        | Debug        | IKE Initiator sending Initial Contact                        |
| ASA-7-714011  | 7        | Debug        | Description of received ID values                            |
| ASA-7-715001  | 7        | Debug        | Descriptive statement                                        |
| ASA-7-715004  | 7        | Debug        | subroutine name() Q Send failure: RetCode (return_code)      |
| ASA-7-715005  | 7        | Debug        | subroutine name() Bad message code: Code (message_code)      |
| ASA-7-715006  | 7        | Debug        | IKE got SPI from key engine: SPI = SPI_value                 |
| ASA-7-715007  | 7        | Debug        | IKE got a KEY_ADD msg for SA: SPI = SPI_value                |
| ASA-7-715008  | 7        | Debug        | Could not delete SA SA_address                               |
| ASA-7-715009  | 7        | Debug        | IKE Deleting SA: Remote Proxy IP_address                     |
| ASA-7-715013  | 7        | Debug        | Tunnel negotiation in progress for destination IP_address    |
| ASA-7-715018  | 7        | Debug        | IP Range type id was loaded: Direction %s                    |
| ASA-7-715019  | 7        | Debug        | Group group Username username IP ip IKEGetUserAttributes: Attribute name = name |
| ASA-7-715020  | 7        | Debug        | construct_cfg_set: Attribute name = name                     |
| ASA-7-715021  | 7        | Debug        | Delay Quick Mode processing                                  |
| ASA-7-715022  | 7        | Debug        | Resume Quick Mode processing                                 |
| ASA-7-715027  | 7        | Debug        | IPSec SA Proposal # chosen_proposal                          |
| ASA-7-715028  | 7        | Debug        | IKE SA Proposal # 1                                          |
| ASA-7-715031  | 7        | Debug        | Obtained IP addr (%s) prior to initiating Mode Cfg (XAuth %s) |
| ASA-7-715032  | 7        | Debug        | Sending subnet mask (%s) to remote client                    |
| ASA-7-715033  | 7        | Debug        | Processing CONNECTED notify (MsgId message_number)           |
| ASA-7-715034  | 7        | Debug        | action IOS keep alive payload: proposal=time 1/time 2 sec.   |
| ASA-7-715035  | 7        | Debug        | Starting IOS keepalive monitor: seconds sec.                 |
| ASA-7-715036  | 7        | Debug        | Sending keep-alive of type notify_type (seq number number)   |
| ASA-7-715037  | 7        | Debug        | Unknown IOS Vendor ID version: major.minor.variance          |
| ASA-7-715038  | 7        | Debug        | action Spoofing_information Vendor ID payload (version: major.minor.variance |
| ASA-7-715039  | 7        | Debug        | Unexpected cleanup of tunnel table entry during SA delete.   |
| ASA-7-715040  | 7        | Debug        | Deleting active auth handle during SA deletion: handle = internal_authentication_handle |
| ASA-7-715041  | 7        | Debug        | Received keep-alive of type keepalive_type                   |
| ASA-7-715042  | 7        | Debug        | IKE received response of type failure_type to a request from the IP_address utility |
| ASA-7-715044  | 7        | Debug        | Ignoring Keepalive payload from vendor not support KeepAlive capability |
| ASA-7-715045  | 7        | Debug        | ERROR: malformed Keepalive payload                           |
| ASA-7-715046  | 7        | Debug        | Group = groupname                                            |
| ASA-7-715047  | 7        | Debug        | processing payload_description payload                       |
| ASA-7-715048  | 7        | Debug        | Send VID_type VID                                            |
| ASA-7-715049  | 7        | Debug        | Received VID_type VID                                        |
| ASA-7-715050  | 7        | Debug        | Claims to be IOS but failed authentication                   |
| ASA-7-715051  | 7        | Debug        | Received unexpected TLV type TLV_type while processing FWTYPE ModeCfg Reply |
| ASA-7-715052  | 7        | Debug        | Old P1 SA is being deleted but new SA is DEAD                |
| ASA-7-715053  | 7        | Debug        | MODE_CFG: Received request for attribute_info!               |
| ASA-7-715054  | 7        | Debug        | MODE_CFG: Received attribute_name reply: value               |
| ASA-7-715055  | 7        | Debug        | Send attribute_name                                          |
| ASA-7-715056  | 7        | Debug        | Client is configured for TCP_transparency                    |
| ASA-7-715057  | 7        | Debug        | Auto-detected a NAT device with NAT-Traversal. Ignoring IPSec-over-UDP configuration. |
| ASA-7-715058  | 7        | Debug        | NAT-Discovery payloads missing. Aborting NAT-Traversal.      |
| ASA-7-715059  | 7        | Debug        | Proposing/Selecting only UDP-Encapsulated-Tunnel and UDP-Encapsulated-Transport modes defined by NAT-Traversal |
| ASA-7-715060  | 7        | Debug        | Dropped received IKE fragment. Reason: reason                |
| ASA-7-715061  | 7        | Debug        | Rcv'd fragment from a new fragmentation set. Deleting any old fragments. |
| ASA-7-715062  | 7        | Debug        | Error assembling fragments! Fragment numbers are non-continuous. |
| ASA-7-715063  | 7        | Debug        | Successfully assembled an encrypted pkt from rcv'd fragments! |
| ASA-7-715064  | 7        | Debug        | IKE Peer included IKE fragmentation capability flags: Main Mode: true/false Aggressive Mode: true/false |
| ASA-7-715065  | 7        | Debug        | IKE state_machine subtype FSM error history (struct data_structure_address) state |
| ASA-7-715066  | 7        | Debug        | Can't load an IPSec SA! The corresponding IKE SA contains an invalid logical ID. |
| ASA-7-715067  | 7        | Debug        | QM IsRekeyed: existing sa from different peer                |
| ASA-7-715068  | 7        | Debug        | QM IsRekeyed: duplicate sa found by address                  |
| ASA-7-715069  | 7        | Debug        | Invalid ESP SPI size of SPI_size                             |
| ASA-7-715070  | 7        | Debug        | Invalid IPComp SPI size of SPI_size                          |
| ASA-7-715071  | 7        | Debug        | AH proposal not supported                                    |
| ASA-7-715072  | 7        | Debug        | Received proposal with unknown protocol ID protocol_ID       |
| ASA-7-715074  | 7        | Debug        | Could not retrieve authentication attributes for peer IP_address |
| ASA-7-715075  | 7        | Debug        | Group = group_name                                           |
| ASA-7-715076  | 7        | Debug        | Computing hash for ISAKMP                                    |
| ASA-7-715077  | 7        | Debug        | Pitcher: msg string                                          |
| ASA-7-715078  | 7        | Debug        | Received %s LAM attribute                                    |
| ASA-7-715079  | 7        | Debug        | INTERNAL_ADDRESS: Received request for %s                    |
| ASA-7-715080  | 7        | Debug        | VPN: Starting P2 rekey timer: 28800 seconds.                 |
| ASA-7-716008  | 7        | Debug        | WebVPN ACL: action                                           |
| ASA-7-716010  | 7        | Debug        | Group group User user Browse network.                        |
| ASA-7-716011  | 7        | Debug        | Group group User user Browse domain domain.                  |
| ASA-7-716012  | 7        | Debug        | Group group User user Browse directory directory.            |
| ASA-7-716013  | 7        | Debug        | Group group User user Close file filename.                   |
| ASA-7-716014  | 7        | Debug        | Group group User user View file filename.                    |
| ASA-7-716015  | 7        | Debug        | Group group User user Remove file filename.                  |
| ASA-7-716016  | 7        | Debug        | Group group User user Rename file old_filename to new_filename. |
| ASA-7-716017  | 7        | Debug        | Group group User user Modify file filename.                  |
| ASA-7-716018  | 7        | Debug        | Group group User user Create file filename.                  |
| ASA-7-716019  | 7        | Debug        | Group group User user Create directory directory.            |
| ASA-7-716020  | 7        | Debug        | Group group User user Remove directory directory.            |
| ASA-7-716021  | 7        | Debug        | File access DENIED                                           |
| ASA-7-716024  | 7        | Debug        | Group name User user Unable to browse the network.Error: description |
| ASA-7-716025  | 7        | Debug        | Group name User user Unable to browse domain domain. Error: description |
| ASA-7-716026  | 7        | Debug        | Group name User user Unable to browse directory directory. Error: description |
| ASA-7-716027  | 7        | Debug        | Group name User user Unable to view file filename. Error: description |
| ASA-7-716028  | 7        | Debug        | Group name User user Unable to remove file filename. Error: description |
| ASA-7-716029  | 7        | Debug        | Group name User user Unable to rename file filename. Error: description |
| ASA-7-716030  | 7        | Debug        | Group name User user Unable to modify file filename. Error: description |
| ASA-7-716031  | 7        | Debug        | Group name User user Unable to create file filename. Error: description |
| ASA-7-716032  | 7        | Debug        | Group name User user Unable to create folder folder. Error: description |
| ASA-7-716033  | 7        | Debug        | Group name User user Unable to remove folder folder. Error: description |
| ASA-7-716034  | 7        | Debug        | Group name User user Unable to write to file filename.       |
| ASA-7-716035  | 7        | Debug        | Group name User user Unable to read file filename.           |
| ASA-7-716036  | 7        | Debug        | Group name User user File Access: User user logged into the server server. |
| ASA-7-716037  | 7        | Debug        | Group name User user File Access: User user failed to login into the server server. |
| ASA-7-716603  | 7        | Debug        | Received size-recv KB Hostscan data from IP src-ip.          |
| ASA-7-717024  | 7        | Debug        | Checking CRL from trustpoint: trustpoint name for purpose    |
| ASA-7-717025  | 7        | Debug        | Validating certificate chain containing number of certs certificate(s). |
| ASA-7-717029  | 7        | Debug        | Identified client certificate within certificate chain. serial number: serial_number |
| ASA-7-717030  | 7        | Debug        | Found a suitable trustpoint trustpoint name to validate certificate. |
| ASA-7-717034  | 7        | Debug        | No-check extension found in certificate. OCSP check bypassed. |
| ASA-7-717038  | 7        | Debug        | Tunnel group match found. Tunnel Group: tunnel_group_name    |
| ASA-7-717041  | 7        | Debug        | Local CA Server event: event info.                           |
| ASA-7-717045  | 7        | Debug        | Local CA Server CRL info: info                               |
| ASA-7-718001  | 7        | Debug        | Internal interprocess communication queue send failure: code error_code |
| ASA-7-718017  | 7        | Debug        | Got timeout for unknown peer IP_address msg type message_type |
| ASA-7-718018  | 7        | Debug        | Send KEEPALIVE request failure to IP_address                 |
| ASA-7-718019  | 7        | Debug        | Sent KEEPALIVE request to IP_address                         |
| ASA-7-718020  | 7        | Debug        | Send KEEPALIVE response failure to IP_address                |
| ASA-7-718021  | 7        | Debug        | Sent KEEPALIVE response to IP_address                        |
| ASA-7-718022  | 7        | Debug        | Received KEEPALIVE request from IP_address                   |
| ASA-7-718023  | 7        | Debug        | Received KEEPALIVE response from IP_address                  |
| ASA-7-718025  | 7        | Debug        | Sent CFG UPDATE to IP_address                                |
| ASA-7-718026  | 7        | Debug        | Received CFG UPDATE from IP_address                          |
| ASA-7-718029  | 7        | Debug        | Sent OOS indicator to IP_address                             |
| ASA-7-718034  | 7        | Debug        | Sent TOPOLOGY indicator to IP_address                        |
| ASA-7-718035  | 7        | Debug        | Received TOPOLOGY indicator from IP_address                  |
| ASA-7-718036  | 7        | Debug        | Process timeout for req-type type_value                      |
| ASA-7-718041  | 7        | Debug        | Timeout [msgType=type] processed with no callback            |
| ASA-7-718046  | 7        | Debug        | Create group policy policy_name                              |
| ASA-7-718047  | 7        | Debug        | Fail to create group policy policy_name                      |
| ASA-7-718049  | 7        | Debug        | Created secure tunnel to peer IP_address                     |
| ASA-7-718056  | 7        | Debug        | Deleted Master peer                                          |
| ASA-7-718058  | 7        | Debug        | State machine return code: action_routine                    |
| ASA-7-718059  | 7        | Debug        | State machine function trace: state=state_name               |
| ASA-7-718088  | 7        | Debug        | Possible VPN LB misconfiguration. Offending device MAC MAC_address. |
| ASA-7-719005  | 7        | Debug        | FSM NAME has been created using protocol for session pointer from source_address. |
| ASA-7-719006  | 7        | Debug        | Email Proxy session pointer has timed out for source_address because of network congestion. |
| ASA-7-719007  | 7        | Debug        | Email Proxy session pointer cannot be found for source_address. |
| ASA-7-719009  | 7        | Debug        | Email Proxy service is starting.                             |
| ASA-7-719015  | 7        | Debug        | Parsed emailproxy session pointer from source_address username: mailuser = mail_user |
| ASA-7-719016  | 7        | Debug        | Parsed emailproxy session pointer from source_address password: mailpass = ****** |
| ASA-7-720031  | 7        | Debug        | (VPN-unit) HA status callback: Invalid event received. event=event_ID. |
| ASA-7-720034  | 7        | Debug        | (VPN-unit) Invalid type (type) for message handler.          |
| ASA-7-720041  | 7        | Debug        | (VPN-unit) Sending type message id to standby unit           |
| ASA-7-720042  | 7        | Debug        | (VPN-unit) Receiving type message id from active unit        |
| ASA-7-720048  | 7        | Debug        | (VPN-unit) FSM action trace begin: state=state               |
| ASA-7-720049  | 7        | Debug        | (VPN-unit) FSM action trace end: state=state                 |
| ASA-7-720050  | 7        | Debug        | (VPN-unit) Failed to remove timer. ID = id.                  |
| ASA-7-722029  | 7        | Debug        | Group group User user-name IP IP_address SVC Session Termination: Conns: connections |
| ASA-7-722030  | 7        | Debug        | Group group User user-name IP IP_address SVC Session Termination: In: data_bytes (+ctrl_bytes) bytes |
| ASA-7-722031  | 7        | Debug        | Group group User user-name IP IP_address SVC Session Termination: Out: data_bytes (+ctrl_bytes) bytes |
| ASA-7-723003  | 7        | Debug        | No memory for WebVPN Citrix ICA connection connection.       |
| ASA-7-723004  | 7        | Debug        | WebVPN Citrix encountered bad flow control flow.             |
| ASA-7-723005  | 7        | Debug        | No channel to set up WebVPN Citrix ICA connection.           |
| ASA-7-723006  | 7        | Debug        | WebVPN Citrix SOCKS errors.                                  |
| ASA-7-723007  | 7        | Debug        | WebVPN Citrix ICA connection connection list is broken.      |
| ASA-7-723008  | 7        | Debug        | WebVPN Citrix ICA SOCKS Server server is invalid.            |
| ASA-7-723009  | 7        | Debug        | Group group-name                                             |
| ASA-7-723010  | 7        | Debug        | Group group-name                                             |
| ASA-7-723011  | 7        | Debug        | Group group-name                                             |
| ASA-7-723012  | 7        | Debug        | Group group-name                                             |
| ASA-7-723013  | 7        | Debug        | WebVPN Citrix encountered invalid connection connection during periodic timeout. |
| ASA-7-723014  | 7        | Debug        | Group group-name                                             |
| ASA-7-725008  | 7        | Debug        | SSL peer-type interface:src-ip/src-port to dst-ip/dst-port proposes the following n cipher(s). |
| ASA-7-725009  | 7        | Debug        | Device proposes the following n cipher(s) peer-type interface:src-ip/src-port to dst-ip/dst-port. |
| ASA-7-725010  | 7        | Debug        | Device supports the following n cipher(s).                   |
| ASA-7-725011  | 7        | Debug        | Cipher[order]: cipher_name                                   |
| ASA-7-725012  | 7        | Debug        | Device chooses cipher cipher for the SSL session with peer-type interface:src-ip/src-port to dst-ip/dst-port. |
| ASA-7-725013  | 7        | Debug        | SSL peer-type interface:src-ip/src-port to dst-ip/dst-port chooses cipher cipher |
| ASA-7-725014  | 7        | Debug        | SSL lib error. Function: function Reason: reason             |
| ASA-7-725017  | 7        | Debug        | No certificates received during the handshake with %s %s:%B/%d to %B/%d for %s session |
| ASA-7-730001  | 7        | Debug        | Group groupname                                              |
| ASA-7-730002  | 7        | Debug        | Group groupname                                              |
| ASA-7-730003  | 7        | Debug        | NACApp sets IP ipaddr VLAN to vlanid                         |
| ASA-7-730006  | 7        | Debug        | Group groupname                                              |
| ASA-7-730010  | 7        | Debug        | Group groupname                                              |
| ASA-7-73007   | 7        | Debug        | Group groupname                                              |
| ASA-7-734003  | 7        | Debug        | DAP: User name                                               |
| ASA-7-737001  | 7        | Debug        | IPAA: Received message ‘message-type’                        |
| ASA-7-737035  | 7        | Debug        | IPAA: Session=<session>                                      |
| ASA-7-747005  | 7        | Debug        | Clustering: State machine notify event event-name (event-id  |
| ASA-7-747006  | 7        | Debug        | Clustering: State machine is at state state-name             |
| ASA-7-751003  | 7        | Debug        | Local: localIP:port Remote:remoteIP:port Username: username/group Need to send a DPD message to peer |
| ASA-7-752002  | 7        | Debug        | Tunnel Manager Removed entry. Map Tag = mapTag. Map Sequence Number = mapSeq. |
| ASA-7-752008  | 7        | Debug        | Duplicate entry already in Tunnel Manager.                   |
| ASA-7-776012  | 7        | Debug        | CTS SXP: timer name timer started for connection with peer peer IP. |
| ASA-7-776013  | 7        | Debug        | CTS SXP: timer name timer stopped for connection with peer peer IP. |
| ASA-7-776014  | 7        | Debug        | CTS SXP: SXP received binding forwarding request (action) binding binding IP - SGname(SGT). |
| ASA-7-776015  | 7        | Debug        | CTS SXP: Binding binding IP - SGname(SGT) is forwarded to peer peer IP (instance connection instance num). |
| ASA-7-776016  | 7        | Debug        | CTS SXP: Binding binding IP - SGName(SGT) from peer peer IP (instance binding's connection instance num) changed from old instance: old instance num |
| ASA-7-776017  | 7        | Debug        | CTS SXP: Binding binding IP - SGname(SGT) from peer peer IP (instance connection instance num) deleted in SXP database. |
| ASA-7-776018  | 7        | Debug        | CTS SXP: Binding binding IP - SGname(SGT) from peer peer IP (instance connection instance num) added in SXP database. |
| ASA-7-776019  | 7        | Debug        | CTS SXP: Binding binding IP - SGname(SGT) action taken. Update binding manager. |
| ASA-7-776301  | 7        | Debug        | CTS Policy: Security-group tag sgt is mapped to security-group name sgname |
| ASA-7-776302  | 7        | Debug        | CTS Policy: Unknown security-group tag sgt referenced in policies |
| ASA-7-776307  | 7        | Debug        | CTS Policy: Security-group name for security-group tag sgt renamed from old_sgname to new_sgname |
| ASA-7-776308  | 7        | Debug        | CTS Policy: Previously unknown security-group tag sgt is now mapped to security-group name sgname |
| ASA-7-785001  | 7        | Debug        | Clustering: Ownership for existing flow from <in_interface>:<src_ip_addr>/<src_port> to <out_interface>:<dest_ip_addr>/<dest_port> moved from unit <old-owner-unit-id> at site <old-site-id> to <new-owner-unit-id> at site <old-site-id> due to <reason>. |