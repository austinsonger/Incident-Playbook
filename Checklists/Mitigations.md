# Mitigations

##### **Restrict or Discontinue Use of FTP and Telnet Services**

The FTP and Telnet protocols transmit credentials in cleartext, which are susceptible to being intercepted. To mitigate this risk, discontinue FTP and Telnet services by moving to more secure file storage/file transfer and remote access services.

- Evaluate business needs and justifications to host files on alternative Secure File Transfer Protocol (SFTP) or HTTPS-based public sites.
- Use Secure Shell (SSH) for access to remote devices and servers.

##### **Restrict or Discontinue Use of Non-approved VPN Services**

- Investigate the business needs and justification for allowing traffic from non-approved VPN services.
- Identify such services across the enterprise and develop measures to add the application and browser plugins that enable non-approved VPN services to the denylist.
- Enhance endpoint monitoring to obtain visibility on devices with non-approved VPN services running. Enhanced endpoint monitoring and detection capabilities would enable an organization’s IT security personnel to manage approved software as well as identify and remove any instances of unapproved software.

##### **Shut down or Decommission Unused Services and Systems**

- Cyber actors regularly identify servers that are out of date or end of life (EOL) to gain access to a network and perform malicious activities. These present easy and safe locations to maintain persistence on a network.
- Often these services and servers are systems that have begun decommissioning, but the final stage has not been completed by shutting down the system. This means they are still running and vulnerable to compromise.
- Ensuring that decommissioning of systems has been completed or taking appropriate action to remove them from the network limits their susceptibility and reduces the investigative surface to be analyzed.

##### **Quarantine and Reimage Compromised Hosts**

**Note:** proceed with caution to avoid the adverse effects detailed in the Common Mistakes in Incident Handling section above.

- Reimage or remove any compromised systems found on the network.
- Monitor and educate users to be cautious of any downloads from third-party sites or vendors.
- Block the known bad domains and add a web content filtering capability to block malicious sites by category to prevent future compromise.
- Sanitize removable media and investigate network shares accessible by users.
- Improve existing network-based malware detection tools with sandboxing capabilities.

##### **Disable Unnecessary Ports, Protocols, and Services**

- Identify and disable ports, protocols, and services not needed for official business to prevent would-be attackers from moving laterally to exploit vulnerabilities. This includes external communications as well as communications between networks.
- Document allowed ports and protocols at the enterprise level.
- Restrict inbound and outbound access to ports and protocols not justified for business use.
- Restrict allowed access list to assets justified by business use.
- Enable a firewall log for inbound and outbound network traffic as well as allowed and denied traffic.

##### **Restrict or Disable Interactive Login for Service Accounts**

Service accounts are privileged accounts dedicated to certain services to perform activities related to the service or application without being tied to a single domain user. Given that services tend to be privileged accounts and thereby have administrative privileges, they are often a target for attackers aiming to obtain credentials. Interactive login to a service account not directly tied to an end-user account makes it difficult to identify accountability during cyber incidents.

- Audit the Active Directory (AD) to identify and document active service accounts.
- Restrict use of service accounts using AD group policy.
- Disallow interactive login by adding service account to a group of non-interactive login users.
- Continuously monitor service account activities by enhancing logging.
- Rotate service accounts and apply password best practices without service, degradation, or disruption.

##### **Disable Unnecessary Remote Network Administration Tools**

- If an attacker (or malware) gains access to a remote user’s computer, steals authentication data (login/password), hijacks an active remote administration session, or successfully attacks a vulnerability in the remote administration tool’s software, the attacker (or malware) will gain unrestricted control of the enterprise network environment. Attackers can use compromised hosts as a relay server for reverse connections, which could enable them to connect to these remote administration tools from anywhere.
- Remove all remote administration tools that are not required for day-to-day IT operations. Closely monitor and log events for each remote-control session required by department IT operations.

##### **Manage Unsecure Remote Desktop Services**

Allowing unrestricted RDP access can increase opportunities for malicious activity such as on path and Pass-the-Hash (PtH) attacks.

- Implement secure remote desktop gateway solutions.
- Restrict RDP service trust across multiple network zones.
- Implement privileged account monitoring and short time password lease for RDP service use.
- Implement enhanced and continuous monitoring of RDP services by enabling logging and ensure RDP logins are captured in the logs.

##### **Credential Reset and Access Policy Review**

Credential resets need to be done to strategically ensure that all the compromised accounts and devices are included and to reduce the likelihood that the attacker is able to adapt in response to this.

- Force password resets; revoke and issue new certificates for affected accounts/devices.

- If it is suspected that the attacker has gained access to the Domain Controller, then the passwords for all local accounts—such as Guest, HelpAssistant, DefaultAccount, System, Administrator, and

   

  ```
  kbrtgt
  ```

  —should be reset. It is essential that the password for the

   

  ```
  kbrtgt
  ```

   

  account is reset as this account is responsible for handling Kerberos ticket requests as well as encrypting and signing them. The account should be reset twice (as the account has a two-password history).

  - The first account reset for the `kbrtgt` needs to be allowed to replicate prior to the second reset to avoid any issues.

- If it is suspected that the `ntds.dit` file has been exfiltrated, then all domain user passwords will need to be reset.

- Review access policies to temporarily revoke privileges/access for affected accounts/devices. If it is necessary to not alert the attacker (e.g., for intelligence purposes), then privileges can be reduced for affected accounts/devices to “contain” them.

##### **Patch Vulnerabilities**

Attackers frequently exploit software or hardware vulnerabilities to gain access to a targeted system.

- Known vulnerabilities in external facing devices and servers should be patched immediately, starting with the point of compromise, if known.
  - Ensure external-facing devices have not been previously compromised while going through the patching process.
- If the point of compromise (i.e., the specific software, device, server) is known, but how the software, device, or server was exploited is unknown, notify the vendor so they can begin analysis and develop a new patch.
- Follow vendor remediation guidance including the installation of new patches as soon as they become available.