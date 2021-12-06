## Playbook: Phishing

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Initial Access|T1566|Phishing|                    |Google Workspace, Linux, Office 365, SaaS, Windows, macOS||


**Investigate, remediate (contain, eradicate), and communicate in parallel!**

Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

### Investigate

1. **Scope the attack** Usually you will be notified that a potential phishing attack is underway, either by a user, customer, or partner.
    * Determine **total number of impacted users**
    * Understand **user actions** in response to the phishing email (_e.g._, did they download the attachment, visit the spoofed site, or give out any personal or business information such as credentials)
    * Find the potentially related activity. Check:
        * social media
        * any possibly suspicious emails
        * emails with links to external and unknown URLs
        * non-returnable or non-deliverable emails
        * any kind of notification of suspicious activity
1. **Analyze the message** using a safe device (i.e., **do not** open messages on a device with access to sensitive data or credentials as the message may contain malware), determine: `TODO: Specify tools and procedure`
    * who received the message
    * who was targeted by the message (may be different than "successful" recipients)
    * email address of the sender
    * subject line
    * message body
    * attachments (**do not open attachments** except according to established procedures)
    * links, domains, and hostnames (**do not follow links** except according to established procedures)
    * email metadata including message headers (see below)
        * sender information from the 'from' field and the X-authenticated user header
        * all client and mail server IP addresses
    * note "quirks" or suspicious features
1. **Analyze links and attachments** `TODO: Specify tools and procedure`
    * use passive collection such as nslookup and whois to find IP addresses and registration information
    * find related domains using OSINT (_e.g._, [reverse whois](https://www.whoxy.com/reverse-whois/)) on email addresses and other registration data
    * submit links, attachments, and/or hashes to [VirusTotal](https://www.virustotal.com/gui/)
    * submit links, attachments, and/or hashes to a malware sandbox such as [Cuckoo](https://cuckoosandbox.org/), [Hybrid Analysis](https://www.hybrid-analysis.com/), [Joe Sandbox](https://www.joesecurity.org/), or [VMray](https://www.vmray.com/).
1. Categorize the type of attack. `TODO: Customize categories and create additional playbooks for common or high-impact phishing types`
1. **Determine the severity.** Consider:
    * whether public or personal safety is at risk
    * whether personal data (or other sensitive data) is at risk
    * any evidence of who is behind the attack
    * number of affected assets
    * preliminary business impact
    * whether services are affected
    * whether you are able to control/record critical systems


### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain


* Contain affected accounts
    * change login credentials
    * reduce access to critical services, systems, or data until investigation is complete
    * reenforce multi-factor authentication (MFA)
* Block activity based on discovered indicators of compromise, _e.g._:
    * block malicious domains using DNS, firewalls, or proxies
    * block messages with similar senders, message bodies, subjects, links, attachments, _etc._, using email gateway or service.
* Implement forensic hold or retain forensic copies of messages
* Purge related messages from other user inboxes, or otherwise make inaccessible
* Contain broader compromise in accordance with general IR plan
* Consider mobile device containment measures such as wiping via mobile device management (MDM).  Balance against investigative/forensic impact.
* Increase detection "alert level," with enhanced monitoring, particularly from related accounts, domains, or IP addresses.
* Consider outside security assistance to support investigation and remediation
* Confirm relevant software upgrades and anti-malware updates on assets.

#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation`

### Communicate


1. Escalate incident and communicate with leadership per procedure
1. Document incident per procedure (and [report](https://us-cert.cisa.gov/report-phishing))
1. Communicate with internal and external legal counsel per procedure, including discussions of compliance, risk exposure, liability, law enforcement contact, _etc._
1. Communicate with users (internal)
    1. Communicate incident response updates per procedure
    1. Communicate impact of incident **and** incident response actions (e.g., containment: "why is the file share down?")
    1. Communicate requirements: "what should users do and not do?"  
1. Communicate with customers
    1. Focus particularly on those whose data was affected
    1. Generate required notifications based on applicable regulations (particularly those that may consider phishing a data breach or otherwise requires notifications) `TODO: Expand notification requirements and procedures for applicable regulations`
1. Contact insurance provider(s)
    1. Discuss what resources they can make available, what tools and vendors they support and will pay for, _etc._
    1. Comply with reporting and claims requirements to protect eligibility
1. Consider notifying and involving [law enforcement](https://www.usa.gov/stop-scams-frauds) TODO: Link the following bullets to actual resources for your organization
    1. [Local law enforcement](#TODO-link-to-actual-resource)
    1. [State or regional law enforcement](#TODO-link-to-actual-resource)
    1. [Federal or national law enforcement](#TODO-link-to-actual-resource)
1. Communicate with security and IT vendors TODO: Link the following bullets to actual resources for your organization
    1. Notify and collaborate with [managed providers](#TODO-link-to-actual-resource) per procedure
    1. Notify and collaborate with [incident response consultants](#TODO-link-to-actual-resource) per procedure

### Recover


1. Launch business continuity/disaster recovery plan(s) if compromise involved business outages: _e.g._, consider migration to alternate operating locations, fail-over sites, backup systems.
1. Reinforce training programs regarding suspected phishing attacks. Key suspicious indicators may include: 
    * misspellings in the message or subject
    * phony-seeming sender names, including mismatches between display name and email address
    * personal email addresses for official business (e.g., gmail or yahoo emails from business colleagues)
    * subject lines marked "[EXTERNAL]" on emails that look internal
    * [malicious or suspicious links](https://www.pcworld.com/article/248963/how-to-tell-if-a-link-is-safe-without-clicking-on-it.html)
    * receiving an email or attachment they were not expecting but from someone they know (contact sender before opening it)
    * reporting suspicious activity to IT or security
1. Ensure that IT and security staff is up to date on recent phishing techniques.
1. Determine if any controls have failed when falling victim to an attack and rectify them. Here is a [good source](https://www.proofpoint.com/us/security-awareness/post/14-things-do-after-phishing-attack) to consider following a phishing attack.

### Resources

#### Reference: User Actions for Suspected Phishing Attack

1. Stay calm, take a deep breath.
1. Take pictures of your screen using your smartphone showing the things you noticed: the phishing message, the link if you opened it, the sender information.
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
1. Contact the [help desk](#TODO-link-to-actual-resource) using the [phishing hotline](#TODO-link-to-actual-resource) or the [phishing report toolbar](#TODO-link-to-actual-resource) and be as helpful as possible.
1. Be patient: the response may be disruptive, but you are protecting your team and the organization!  **Thank you.**

#### Reference: Help Desk Actions for Suspected Phishing Attack


1. Stay calm, take a deep breath.
1. Open a ticket to document the incident, per procedure. `TODO: Customize template with key questions (see below) and follow-on workflow`
1. Ask the user to take pictures of their screen using their smartphone showing the things they noticed: the phishing message, the link if you opened it, the sender information, _etc._  If this is something you noticed directly, do the same yourself.
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
1. Get detailed contact information from the user (home, office, mobile), if applicable.
1. Record all information in the ticket, including hand-written and voice notes.
1. Quarantine affected users and systems. `TODO: Customize containment steps, automate as much as possible`
1. Contact the [security team](#TODO-link-to-actual-resource) and stand by to participate in the response as directed: investigation, remediation, communication, and recovery.

#### Additional Information

1. <a name="phishing-playbook-ref-1"></a>[Anti-Phishing Attack resources](https://resources.infosecinstitute.com/category/enterprise/phishing/phishing-countermeasures/top-16-anti-phishing-resources/#gref)
1. <a name="phisphing-playbook-ref-2"></a>[Methods of Identifying a Phishing attack](https://www.securitymetrics.com/blog/7-ways-recognize-phishing-email) 
1. <a name="phishing-playbook-ref-3"></a>[Phishing Email Examples](https://www.phishing.org/phishing-examples) 
1. <a name="phishing-playbook-ref-4"></a>[Anti-Phishing best practices](https://resources.infosecinstitute.com/category/enterprise/phishing/phishing-countermeasures/anti-phishing-best-practices/#gref)

------------------------
------------------------
------------------------


## Sub-technique Playbook: T1566.001 - Spearphishing Attachment

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|        |              |                |                    |           |                      |


```
(P) Preparation
  
 
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.



### Investigate

`TODO: Expand investigation steps, including key questions and strategies, for <Type of Incident>.`





### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



`TODO: Consider automating containment measures using orchestration tools.`

#### Eradicate

`TODO: Customize eradication steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`



### Communicate

`TODO: Customize communication steps for <Type of Incident>`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:


  
  



### Recover

`TODO: Customize recovery steps for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`

In addition to the general steps and guidance in the incident response plan:



  
### Lessons Learned

`TODO: Add items that will occur post recover.`
  
1.    Perform routine cyber hygiene due diligence
2.    Engage external cybersecurity-as-a-service providers and response professionals
 



### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)


------------------------
------------------------
------------------------

## Sub-technique Playbook: T1566.002 - Spearphishing Link

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|        |              |                |                    |           |                      |


```
(P) Preparation
  
 
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.



### Investigate

`TODO: Expand investigation steps, including key questions and strategies, for <Type of Incident>.`






### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



`TODO: Consider automating containment measures using orchestration tools.`

#### Eradicate

`TODO: Customize eradication steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`



### Communicate

`TODO: Customize communication steps for <Type of Incident>`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:


  
 

### Recover

`TODO: Customize recovery steps for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`

In addition to the general steps and guidance in the incident response plan:



  
### Lessons Learned

`TODO: Add items that will occur post recover.`
  
1.    Perform routine cyber hygiene due diligence
2.    Engage external cybersecurity-as-a-service providers and response professionals
 



### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)


------------------------
------------------------
------------------------

## Playbook: Sub-technique T1566.003 - Spearphishing via Service

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|        |              |                |                    |           |                      |


```
(P) Preparation
  
 
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.



### Investigate

`TODO: Expand investigation steps, including key questions and strategies, for <Type of Incident>.`





### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



`TODO: Consider automating containment measures using orchestration tools.`

#### Eradicate

`TODO: Customize eradication steps, tactical and strategic, for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`



#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`

--------------

### Communicate

`TODO: Customize communication steps for <Type of Incident>`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:


  
  

--------------

### Recover

`TODO: Customize recovery steps for <Type of Incident>.`

`TODO: Specify tools and procedures for each step, below.`

In addition to the general steps and guidance in the incident response plan:


--------------
  
### Lessons Learned

`TODO: Add items that will occur post recover.`
  
1.    Perform routine cyber hygiene due diligence
2.    Engage external cybersecurity-as-a-service providers and response professionals
 

--------------

### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)



