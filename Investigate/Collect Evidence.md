## Collect Evidence

* Prioritize based on the investigative plan
* Collect live response data using {{LIVE_RESPONSE_TOOL}}.  `TODO: Customize live response tools and procedure.`
* Collect relevant logs from system(s) (if not part of live response), aggregator(s), SIEM(s), or device console(s).  `TODO: Customize log collection tools and procedure.`
* Collect memory image, if necessary and if not part of live response, using {{MEMORY_COLLECTION_TOOL}}.  `TODO: Customize memory collection tools and procedure.`
* Collect disk image, if necessary, using {{DISK_IMAGE_TOOL}}.  `TODO: Customize disk image collection tool and procedure.`
* Collect and store evidence in accordance with policy, and with proper chain of custody. `TODO: Customize evidence collection and chain of custody policy.`

Consider collecting the following artifacts as evidence, either in real time (_e.g., via EDR or a SIEM) or on demand:

###  Example Useful Artifacts

`TODO: Customize and prioritize useful artifacts.`

* Running Processes
* Running Services
* Executable Hashes
* Installed Applications
* Local and Domain Users
* Listening Ports and Associated Services
* Domain Name System (DNS) Resolution Settings and Static Routes
* Established and Recent Network Connections
* Run Key and other AutoRun Persistence
* Scheduled tasks and cron jobs
* Artifacts of past execution (e.g., Prefetch and Shimcache)
* Event logs
* Group policy and WMI artifacts
* Anti-virus detections
* Binaries in temporary storage locations
* Remote access credentials
* Network connection telemetry (e.g., netflow, firewall permits)
* DNS traffic and activity
* Remote access activity including Remote Desktop Protocol (RDP), virtual private network (VPN), SSH, virtual network computing (VNC), and other remote access tools
* Uniform Resource Identifier (URI) strings, user agent strings, and proxy enforcement actions
* Web traffic (HTTP/HTTPS)
