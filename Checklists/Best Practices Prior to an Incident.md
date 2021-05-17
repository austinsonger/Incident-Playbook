# Best Practices Prior to an Incident

##### **User Education**

End users are the frontline security of the organizations. Educating them in security principles as well as actions to take and not take during an incident will increase the organization’s resilience and might prevent easily avoidable compromises.

- Educate users to be cautious of any downloads from third-party sites or vendors.
- Train users on recognizing phishing emails. There are several systems and services (free and otherwise) that can be deployed or leveraged.
- Train users on identifying which groups/individuals to contact when they suspect an incident.
- Train users on the actions they can and cannot take if they suspect an incident and why (some users will attempt to remediate and might make things worst).

##### **Allowlisting**

- Enable application directory allowlisting through Microsoft Software Restriction Policy or AppLocker.
- Use directory allowlisting rather than attempting to list every possible permutation of applications in a network environment. Safe defaults allow applications to run from `PROGRAMFILES`, `PROGRAMFILES(X86)`, and `SYSTEM32`. Disallow all other locations unless an exception is granted.
- Prevent the execution of unauthorized software by using application allowlisting as part of the OS installation and security hardening process.

##### **Account Control**

- Decrease a threat actor’s ability to access key network resources by implementing the principle of least privilege.
- Limit the ability of a local administrator account to log in from a local interactive session (e.g., Deny access to this computer from the network) and prevent access via an RDP session.
- Remove unnecessary accounts and groups; restrict root access.
- Control and limit local administration; e.g. implementing Just Enough Administration (JEA), just-in-time (JIT) administration, or enforcing PowerShell Constrained Language mode via a User Mode Code Integrity (UMCI) policy.
- Make use of the Protected Users Active Directory group in Windows domains to further secure privileged user accounts against pass-the-hash attacks.

##### **Backups**

- Identify what data is essential to keeping operations running; make regular backup copies.
- Test that backups are working to ensure they can restore the data in the event of an incident.
- Create offline backups to help recover from a ransomware attack or from disasters (fire, flooding, etc.).
- Securely store offline backups at an offsite location. If feasible, choose an offsite location that is at a distance from the primary location that would be unaffected in the event of a regional natural disaster.

##### **Workstation Management**

- Create and deploy a secure system baseline image to all workstations.
- Mitigate potential exploitation by threat actors by following a normal patching cycle for all OSs, applications, and software, with exceptions for emergency patches.
- Apply asset and patch management processes.
- Reduce the number of cached credentials to one (if a laptop) or zero (if a desktop or fixed asset).

##### **Host-Based Intrusion Detection / Endpoint Detection and Response**

- Configure and monitor workstation system logs through a host-based endpoint detection and response platform and firewall.
- Deploy an anti-malware solution on workstations to prevent spyware, adware, and malware as part of the OS security baseline.
  - Ensure that your anti-malware solution remains up to date.
- Monitor antivirus scan results on a regular basis.

##### **Server Management**

- Create a secure system baseline image and deploy it to all servers.
- Upgrade or decommission end-of-life non-Windows servers.
- Upgrade or decommission servers running Windows Server 2003 or older versions.
- Implement asset and patch management processes.
- Audit for and disable unnecessary services.

##### **Server Configuration and Logging**

- Establish remote server logging and retention.
- Reduce the number of cached credentials to zero.
- Configure and monitor system logs via a centralized security information and event management (SIEM) appliance.
- Add an explicit `DENY` for `%USERPROFILE%`.
- Restrict egress web traffic from servers.
- In Windows environments, use Restricted Admin mode or remote credential guard to further secure remote desktop sessions against pass-the-hash attacks.
- Restrict anonymous shares.
- Limit remote access by only using jump servers for such access.
- On Linux, use SELINUX or AppArmor in enforcing mode and/or turn on audit logging.
- Turn on bash shell logging; ship this and all logs to a remote server.
- Do not allow users to use `su`. Use `Sudo -l` instead.
- Configure automatic updates in yum or apt.
- Mount `/var/tmp` and `/tmp` as `noexec`.

##### **Change Control**

- Create a change control process for all implemented changes.

##### **Network Security**

- Implement an intrusion detection system (IDS).
  - Apply continuous monitoring.
  - Send alerts to a SIEM tool.
  - Monitor internal activity (this tool may use the same tap points as the netflow generation tools).
- Employ netflow capture.
  - Set a minimum retention period of 180 days.
  - Capture netflow on all ingress and egress points of network segments, not just at the Managed Trusted Internet Protocol Services or Trusted Internet Connections locations.
- Capture all network traffic
  - Retain captured traffic for a minimum of 24 hours.
  - Capture traffic on all ingress and egress points of the network.
- Use VPN
  - Maintain site-to-site VPN with customers and vendors.
  - Authenticate users utilizing site-to-site VPNs.
  - Use authentication, authorization, and accounting for controlling network access.
  - Require smartcard authentication to an HTTPS page in order to control access. Authentication should also require explicit rostering of permitted smartcard distinguished names to enhance the security posture on both networks participating in the site-to-site VPN.
- Establish appropriate secure tunneling protocol and encryption.
- Strengthen router configuration (e.g., avoid enabling remote management over the internet and using default IP ranges, automatically log out after configuring routers, and use encryption.).
- Turn off Wi-Fi protected setup, enforce the use of strong passwords, and keep router firmware up-to-date.
- Improve firewall security (e.g., enable automatic updates, revise firewall rules as appropriate, implement allowlists, establish packet filtering, enforce the use of strong passwords, encrypt networks).
  - Whenever possible, ensure access to network devices via external or untrusted networks (specifically the internet) is disabled.
- Manage access to the internet (e.g., providing internet access from only devices/accounts that need it, proxying all connections, disabling internet access for privileged/administrator accounts, enabling policies that restrict internet access using a blocklist, a resource allowlist, content type, etc.)
  - Conduct regular vulnerability scans of the internal and external networks and hosted content to identify and mitigate vulnerabilities.
  - Define areas within the network that should be segmented to increase the visibility of lateral movement by a threat and increase the defense-in-depth posture.
  - Develop a process to block traffic to IP addresses and domain names that have been identified as being used to aid previous attacks.
- Evaluate and consider the security configurations of Microsoft Office 365 (O365) and other cloud collaboration service platforms prior to deployment.
  - Use multi-factor authentication. This is the best mitigation technique to protect against credential theft for O365 administrators and users.
  - Protect Global Admins from compromise and use the principle of “Least Privilege.”
  - Enable unified audit logging in the Security and Compliance Center.
  - Enable alerting capabilities.
  - Integrate with organizational SIEM solutions.
  - Disable legacy email protocols, if not required, or limit their use to specific users.

##### **Network Infrastructure Recommendations**

- Create a secure system baseline image and deploy it to all networking equipment (e.g., switches, routers, firewalls).
- Remove unnecessary OS files from the internetwork operating system (IOS). This will limit the possible targets of persistence (i.e., files to embed malicious code) if the device is compromised and will align with National Security Agency Network Device Integrity best practices.
- Remove vulnerable IOS OS files (i.e., older iterations) from the device’s boot variable (i.e., show boot or show bootvar).
- Update to the latest available operating system for IOS devices.
- On devices with a Secure Sockets Layer VPN enabled, routinely verify customized web objects against the organization’s known good files for such VPNs, to ensure the devices remain free of unauthorized modification.
- Ensure that any incident response tools that point to external domains are either removed or updated to point to internal security tools. If this is not done and an external domain to which a tool points expires, a malicious threat actor may register it and start collecting telemetry from the infrastructure.

##### **Host Recommendations**

- Implement policies to block workstation-to-workstation RDP connections through a Group Policy Object on Windows, or by a similar mechanism.
- Store system logs of mission critical systems for at least one year within a SIEM tool.
- Review the configuration of application logs to verify that recorded fields will contribute to an incident response investigation.

##### **User Management**

- Reduce the number of domain and enterprise administrator accounts.
- Create non-privileged accounts for privileged users and ensure they use the non- privileged accounts for all non-privileged access (e.g., web browsing, email access).
- If possible, use technical methods to detect or prevent browsing by privileged accounts (authentication to web proxies would enable blocking of Domain Administrators).
- Use two-factor authentication (e.g., security tokens for remote access and access to any sensitive data repositories).
- If soft tokens are used, they should not exist on the same device that is requesting remote access (e.g., a laptop) and instead should be on a smartphone, token, or other out-of-band device.
- Create privileged role tracking.
- Create a change control process for all privilege escalations and role changes on user accounts.
- Enable alerts on privilege escalations and role changes.
- Log privileged user changes in the network environment and create an alert for unusual events.
- Establish least privilege controls.
- Implement a security-awareness training program.

##### **Segregate Networks and Functions**

Proper network segmentation is a very effective security mechanism to prevent an intruder from propagating exploits or laterally moving around an internal network. On a poorly segmented network, intruders are able to extend their impact to control critical devices or gain access to sensitive data and intellectual property. Security architects must consider the overall infrastructure layout, segmentation, and segregation. Segregation separates network segments based on role and functionality. A securely segregated network can contain malicious occurrences, reducing the impact from intruders, in the event that they have gained a foothold somewhere inside the network.

###### **Physical Separation of Sensitive Information**

Local Area Network (LAN) segments are separated by traditional network devices such as routers. Routers are placed between networks to create boundaries, increase the number of broadcast domains, and effectively filter users’ broadcast traffic. These boundaries can be used to contain security breaches by restricting traffic to separate segments and can even shut down segments of the network during an intrusion, restricting adversary access.

Recommendations:

- Implement Principles of Least Privilege and need-to-know when designing network segments.
- Separate sensitive information and security requirements into network segments.
- Apply security recommendations and secure configurations to all network segments and network layers.

###### **Virtual Separation of Sensitive Information**

As technologies change, new strategies are developed to improve IT efficiencies and network security controls. Virtual separation is the logical isolation of networks on the same physical network. The same physical segmentation design principles apply to virtual segmentation but no additional hardware is required. Existing technologies can be used to prevent an intruder from breaching other internal network segments.

Recommendations:

- Use Private Virtual LANs to isolate a user from the rest of the broadcast domains.
- Use Virtual Routing and Forwarding (VRF) technology to segment network traffic over multiple routing tables simultaneously on a single router.
- Use VPNs to securely extend a host/network by tunneling through public or private networks.

