## Playbook: Unauthorized VPN and VDI Access

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Initial Access|T1133|External Remote Services|               |Containers, Linux, Windows|User|



```
(P) Preparation

1.    Patch asset vulnerabilities
2.    Perform routine inspections of controls/weapons
3.    Ensure Antivirus/Endpoint Protection software is installed on workstations and laptops
4.    Prohibit non-employees from accessing company devices
5.    Ensure that all remotely accessible services are logging to a central location
6.    Provide security awareness training to employees
7.    Use multifactor authentication where possible
8.    Ensure proper network segmentation/firewall rules are in place for remote users
9.    Routinely audit remote system access
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

--------------

### Investigate

<!--
`TODO: Expand investigation steps, including key questions and strategies, for Unauthorized VPN and VDI Access.`
-->

1. Monitor for:
    * Remote access during unusual hours/days
    * Remote access from unusual sources (i.e. geographic locations, IPs, etc.)
    * Excessive failed login attempts
    * IPS/IDS alerts
    * Antivirus/Endpoint alerts
2.    Investigate and clear ALL alerts associated with the impacted assets
3.    Contact the user out of band to determine the legitimacy of the detected activity

--------------

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

<!--
`TODO: Customize containment steps, tactical and strategic, for Unauthorized VPN and VDI Access.`

`TODO: Specify tools and procedures for each step, below.`

-->

1.    Inventory (enumerate & assess)
2.    Detect | Deny | Disrupt | Degrade | Deceive | Destroy
3.    Observe -> Orient -> Decide -> Act
4.    Issue perimeter enforcement for known threat actor locations
5.    Block access from the compromised user
6.    Lock accounts associated with the compromised user
7.    Inspect all potentially compromised systems for IOCs


<!--
`TODO: Consider automating containment measures using orchestration tools.`
-->

#### Eradicate


<!--
`TODO: Customize eradication steps, tactical and strategic, for Unauthorized VPN and VDI Access.`

`TODO: Specify tools and procedures for each step, below.`
-->


1.    Close the attack vector
2.    Patch asset vulnerabilities
3.    Perform Endpoint/AV scans on affected systems
4.    Review logs to determine the extent of the unauthorized activity

#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`

--------------

### Communicate

`TODO: Customize communication steps for <Type of Incident>`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:



--------------

### Recover

<!--
`TODO: Customize recovery steps for Unauthorized VPN and VDI Access.`

`TODO: Specify tools and procedures for each step, below.`
-->


In addition to the general steps and guidance in the incident response plan:


1.    Restore to the RPO within the RTO
2.    Address collateral damage
3.    Resolve any related security incidents
4.    Perform routine cyber hygiene due diligence
5.    Engage external cybersecurity-as-a-service providers and response professionals

--------------

### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)
