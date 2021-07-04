## Playbook: Ransomware

> Containment is critical in ransomware incidents, prioritize accordingly.

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Impact|T1486|Data Encrypted for Impact|                    |IaaS, Linux, Windows, macOS|Administrator, SYSTEM, User, root|


```
(P) Preparation
  
1.    Patch asset vulnerabilities
2.    Perform routine inspections of controls/weapons
3.    Examine file shares for loose/open privileges
4.    Maintain Antivirus/EDR application updates
5.    Create network segmentation
6.    Log traffic between network segments
7.    Incorporate threat intelligence
8.    Incorporate deception technology
9.    Perform routine inspections of asset backups
10.   Validate proper functionality
11.   Confirm backups are free of malware
12.   Establish ability to pay ransoms w/cryptocurrency
13.   Obtain decryption keys for ransomware variants
14.   Confirm cybersecurity insurance coverages
15.   Conduct ransomware simulations
16.   Conduct phishing simulations
17.   Conduct user awareness training
18.   Conduct response training (this PBC)
```


### Investigate

1. **Determine the type** of ransomware (_i.e.,_ what is the family, variant, or flavor?)[<sup>[1]</sup>](#ransomware-playbook-ref-1)
    1. Find any related messages.  Check:
        * graphical user interfaces (GUIs) for the malware itself
        * text or html files, sometimes opened automatically after encryption
        * image files, often as wallpaper on infected systems
        * contact emails in encrypted file extensions
        * pop-ups after trying to open an encrypted file
        * voice messages
    1. Analyze the messages looking for clues to the ransomware type:
        * ransomware name
        * language, structure, phrases, artwork
        * contact email
        * format of the user id
        * ransom demand specifics (_e.g._, digital currency, gift cards)
        * payment address in case of digital currency
        * support chat or support page
    1. Analyze affected and/or new files.  Check:
        * file renaming scheme of encrypted files including extension (_e.g._, `.crypt`, `.cry`, `.locked`) and base name
        * file corruption vs encryption
        * targeted file types and locations
        * owning user/group of affected files
        * icon for encrypted files
        * file markers
        * existence of file listings, key files or other data files
    1. Analyze affected software or system types.  Some ransomware variants only affect certain tools (_e.g._, [databases](https://www.bleepingcomputer.com/news/security/mongodb-apocalypse-professional-ransomware-group-gets-involved-infections-reach-28k-servers/)) or platforms (_e.g._, [NAS products](https://forum.synology.com/enu/viewtopic.php?f=3&t=88716))
    1. Upload indicators to automated categorization services like [Crypto Sheriff](https://www.nomoreransom.org/crypto-sheriff.php), [ID Ransomware](https://id-ransomware.malwarehunterteam.com/), or similar.
1. **Determine the scope:**
    1. Which systems are affected? `TODO: Specify tool(s) and procedure`
        * Scan for concrete indicators of compromise (IOCs) such as files/hashes, processes, network connections, etc.  Use [endpoint protection/EDR](#TODO-link-to-actual-resource), [endpoint telemetry](#TODO-link-to-actual-resource), [system logs](#TODO-link-to-actual-resource), etc.
        * Check similar systems for infection (_e.g._, similar users, groups, data, tools, department,configuration, patch status): check [IAM tools](#TODO-link-to-actual-resource), [permissions management tools](#TODO-link-to-actual-resource), [directory services](#TODO-link-to-actual-resource), _etc._
        * Find external command and control (C2), if present, and find other systems connecting to it: check [firewall or IDS logs](#TODO-link-to-actual-resource), [system logs/EDR](#TODO-link-to-actual-resource), [DNS logs](#TODO-link-to-actual-resource), [netflow or router logs](#TODO-link-to-actual-resource), _etc._
    1. What data is affected? (_e.g._, file types, department or group, affected software) `TODO: Specify tool(s) and procedure`
        * Find anomalous changes to file metadata such as mass changes to creation or modification times.  Check [file metadata search tools](#TODO-link-to-actual-resource)
        * Find changes to normally-stable or critical data files.  Check [file integrity monitoring](#TODO-link-to-actual-resource) tools
1. **Assess the impact** to prioritize and motivate resources
    1. Assess functional impact: impact to business or mission.
        * How much money is lost or at risk?
        * How many (and which) missions are degraded or at risk?
    1. Assess information impact: impact to confidentiality, integrity, and availability of data.
        * How critical is the data to the business/mission?
        * How sensitive is the data? (_e.g._, trade secrets)
        * What is the regulatory status of data (_e.g._, PII, PHI)
1. **Find the infection vector.**  Check the tactics captured in the [Initial Access tactic](https://attack.mitre.org/tactics/TA0001/) of MITRE ATT&CK[<sup>[4]</sup>](#ransomware-playbook-ref-4).  Common specifics and data sources include:
    * email attachment: check [email logs](#TODO-link-to-actual-resource), [email security appliances and services](#TODO-link-to-actual-resource), [e-discovery tools](#TODO-link-to-actual-resource), _etc._
    * insecure remote desktop protocol (RDP): check [vulnerability scanning results](#TODO-link-to-actual-resource), [firewall configurations](#TODO-link-to-actual-resource), _etc._
    * self-propagation (worm or virus) (check [host telemetry/EDR](#TODO-link-to-actual-resource), [system logs](#TODO-link-to-actual-resource), [forensic analysis](#TODO-link-to-actual-resource), _etc._)
    * infection via removable drives (worm or virus)
    * delivered by other malware or attacker tool: expand investigation to include additional attacker tools or malware

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for ransomware.`

`TODO: Specify tools and procedures for each step, below.`

**In ransomware situations, containment is critical.  Inform containment measures with facts from the investigation.  Prioritize quarantines and other containment measures higher than during a typical response.**

Quarantines (logical, physical, or both) prevent spread _from_ infected systems and prevent spread _to_ critical systems and data. Quarantines should be comprehensive: include cloud/SaaS access, single-sign-on, system access such as to ERP or other business tools, _etc._

* Inventory (enumerate & assess)
* Detect | Deny | Disrupt | Degrade | Deceive | Destroy
* Observe -> Orient -> Decide -> Act
* Quarantine infected systems
* Quarantine affected users and groups.
* Quarantine file shares (not just known-infected shares; protect uninfected shares too)
* Quarantine shared databases (not just known-infected servers; protect uninfected databases too)
* Quarantine backups, if not already secured
* Block command and control domains and addresses
* Remove vector emails from inboxes
* Confirm endpoint protection (AV, NGAV, EDR, _etc._) is up-to-date and enabled on all systems.
* Confirm patches are deployed on all systems (prioritizing targeted systems, OSes, software, _etc._).
* Deploy custom signatures to endpoint protection and network security tools based on discovered IOCs

`TODO: Consider automating containment measures using orchestration tools.`

#### Eradicate

`TODO: Customize eradication steps, tactical and strategic, for ransomware.`

`TODO: Specify tools and procedures for each step, below.`

* Rebuild infected systems from known-good media
* Restore from known-clean backups
* Confirm endpoint protection (AV, NGAV, EDR, _etc._) is up-to-date and enabled on all systems.
* Confirm patches are deployed on all systems (prioritizing targeted systems, OSes, software, _etc._).
* Deploy custom signatures to endpoint protection and network security tools based on discovered IOCs
* **Watch for re-infection:** consider increased priority for alarms/alerts related to this incident.

#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`

### Communicate


1. Escalate incident and communicate with leadership per procedure
1. Document incident per procedure
1. Communicate with internal and external legal counsel per procedure, including discussions of compliance, risk exposure, liability, law enforcement contact, _etc._
1. Communicate with users (internal)
    1. Communicate incident response updates per procedure
    1. Communicate impact of incident **and** incident response actions (e.g., containment: "why is the file share down?"), which can be more intrusive/disruptive during ransomware incidents
    1. Communicate requirements: "what should users do and not do?"  See "Reference: User Actions for Suspected Ransomware," below
1. Communicate with customers
    1. Focus particularly on those whose data was affected
    1. Generate required notifications based on applicable regulations (particularly those that may consider ransomware a data breach or otherwise requires notifications (_e.g._, [HHS/HIPAA](https://www.hhs.gov/sites/default/files/RansomwareFactSheet.pdf))) `TODO: Expand notification requirements and procedures for applicable regulations`
1. Contact insurance provider(s)
    1. Discuss what resources they can make available, what tools and vendors they support and will pay for, _etc._
    1. Comply with reporting and claims requirements to protect eligibility
1. Communicate with regulators, including a discussion of what resources they can make available (not just boilerplate notification: many can actively assist)
1. Consider notifying and involving [law enforcement](https://www.nomoreransom.org/en/report-a-crime.html)
    1. [Local law enforcement](#TODO-link-to-actual-resource)
    1. [State or regional law enforcement](#TODO-link-to-actual-resource)
    1. [Federal or national law enforcement](#TODO-link-to-actual-resource)
1. Communicate with security and IT vendors
    1. Notify and collaborate with [managed providers](#TODO-link-to-actual-resource) per procedure
    1. Notify and collaborate with [incident response consultants](#TODO-link-to-actual-resource) per procedure

### Recover


1. Launch business continuity/disaster recovery plan(s): _e.g._, consider migration to alternate operating locations, fail-over sites, backup systems.
1. Recover data from known-clean backups to known-clean, patched, monitored systems (post-eradication), in accordance with our [well-tested backup strategy](#TODO-link-to-actual-resource).
    * Check backups for indicators of compromise
    * Consider partial recovery and backup integrity testing
1. Find and try known decryptors for the variant(s) discovered using resources like the No More Ransom! Project's [Decryption Tools page](https://www.nomoreransom.org/en/decryption-tools.html).
1. Consider paying the ransom for irrecoverable critical assets/data, in accordance with policy `TODO: Expand and socialize this decision matrix`
    * Consider ramifications with appropriate stakeholders
    * Understand finance implications and budget
    * Understand legal, regulatory, and insurance implications
    * Understand mechanisms (_e.g._, technologies, platforms, intermediate vendors/go-betweens)

### Lessons Learned

1.    Perform routine cyber hygiene due diligence
2.    Engage external cybersecurity-as-a-service providers and response professionals
3.    Avoid opening email and attachments from unfamiliar senders
4.    Avoid opening email attachments from senders that do not normally include attachments

### Resources

#### Reference: User Actions for Suspected Ransomware

1. Stay calm, take a deep breath.
1. Disconnect your system from the network `TODO: include detailed steps with screenshots, a pre-installed tool or script to make this easy ("break in case of emergency"), consider hardware network cut-off switches`
1. Take pictures of your screen using your smartphone showing the things you noticed: ransom messages, encrypted files, system error messages, _etc._
1. Take notes about the problem(s) using the voice memo app on your smartphone or pen-and-paper.  Every little bit helps!  Document the following:
    1. What did you notice?
    1. Why did you think it was a problem?
    1. What were you doing at the time you detected it?
    1. When did it first occur, and how often since?
    1. Where were you when it happened, and on what network? (office/home/shop, wired/wireless, with/without VPN, _etc._)
    1. What systems are you using? (operating system, hostname, _etc._)
    1. What account were you using?
    1. What data do you typically access?
    1. Who else have you contacted about this incident, and what did you tell them?
1. Contact the [help desk](#TODO-link-to-actual-resource) and be as helpful as possible
1. Be patient: the response may be disruptive, but you are protecting your team and the organization!  **Thank you.**

#### Reference: Help Desk Actions for Suspected Ransomware

1. Stay calm, take a deep breath.
1. Open a ticket to document the incident, per procedure `TODO: Customize template with key questions (see below) and follow-on workflow`
1. Ask the user to take pictures of their screen using their smartphone showing the things they noticed: ransom messages, encrypted files, system error messages, _etc._  If this is something you noticed directly, do the same yourself.
1. Take notes about the problem(s) using the voice memo app on your smartphone or pen-and-paper.  If this is a user report, ask detailed questions, including:
    1. What did you notice?
    1. Why did you think it was a problem?
    1. What were you doing at the time you detected it?
    1. When did it first occur, and how often since?
    1. What networks are involved? (office/home/shop, wired/wireless, with/without VPN, _etc._)
    1. What systems are involved? (operating system, hostname, _etc._)
    1. What data is involved? (paths, file types, file shares, databases, software, _etc._)
    1. What users and accounts are involved? (active directory, SaaS, SSO, service accounts, _etc._)
    1. What data do the involved users typically access?
    1. Who else have you contacted about this incident, and what did you tell them?
1. Ask follow-up questions as necessary.  **You are an incident responder, we are counting on you.**
1. Get detailed contact information from the user (home, office, mobile), if applicable
1. Record all information in the ticket, including hand-written and voice notes
1. Quarantine affected users and systems `TODO: Customize containment steps, automate as much as possible`
1. Contact the [security team](#TODO-link-to-actual-resource) and stand by to participate in the response as directed: investigation, remediation, communication, and recovery

#### Additional Information

1. <a name="ransomware-playbook-ref-1"></a>["Ransomware Identification for the Judicious Analyst"](https://www.gdatasoftware.com/blog/2019/06/31666-ransomware-identification-for-the-judicious-analyst), Hahn (12 Jun 2019)
1. <a name="ransomware-playbook-ref-2"></a>[No More Ransom!](https://www.nomoreransom.org) Project, including their [Crypto Sheriff](https://www.nomoreransom.org/crypto-sheriff.php?lang=en) service and their [Q&A](https://www.nomoreransom.org/en/ransomware-qa.html)
1. <a name="ransomware-playbook-ref-3"></a>[ID Ransomware](https://id-ransomware.malwarehunterteam.com/) service
1. <a name="ransomware-playbook-ref-4"></a>[MITRE ATT&CK Matrix](https://attack.mitre.org), including the [Initial Access](https://attack.mitre.org/tactics/TA0001/) and [Impact](https://attack.mitre.org/tactics/TA0040/) tactics

