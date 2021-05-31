## Playbook: Drive By Compromise

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Initial Access|T1189|Drive-by Compromise|                    |Linux, SaaS, Windows, macOS|User|


```
(P) Preparation
  
1.    Patch browsers and other software regularly
2.    Perform routine inspections of controls/weapons
3.    Ensure Antivirus/Endpoint Protection software is installed on workstations
4.    Ensure that workstations are logging to a central location
5.    Log network traffic
6.    Set up a proxy for web traffic
7.    Use Group Policy to manage security related browser settings
8.    Make use of Windows Defender Exploit Guard or other exploit mitigation tools"
```

Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

--------------

### Investigate

`TODO: Expand investigation steps, including key questions and strategies, for Drive By Compromise.`

  
1. Monitor for:
    - Unusual DNS activity
    - Antivirus/Endpoint alerts
    - IDS/IPS alerts
    - User reports of unexpected behavior
2.    Investigate and clear ALL alerts associated with the impacted assets

--------------

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for Drive By Compromise.`
  
`TODO: Specify tools and procedures for each step, below.`
  
`TODO: Consider automating containment measures using orchestration tools.`

1.    Inventory (enumerate & assess)
2.    Detect | Deny | Disrupt | Degrade | Deceive | Destroy
3.    Observe -> Orient -> Decide -> Act
4.    Issue perimeter enforcement for known threat actor locations
5.    Systems believed to have been compromised should be removed from the network
  
  
#### Eradicate
`TODO: Customize eradication steps, tactical and strategic, for Drive By Compromise.`
  
`TODO: Specify tools and procedures for each step, below.`

1.    Close the attack vector
2.    Patch asset vulnerabilities
3.    Perform an antivirus scan on the affected system
4.    Review logs and network traffic to identify any related malicious activity

#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`

--------------

### Communicate

`TODO: Customize communication steps for Drive By Compromise`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:

1. TODO

--------------

### Recover

`TODO: Customize recovery steps for Drive By Compromise.`

`TODO: Specify tools and procedures for each step, below.`

In addition to the general steps and guidance in the incident response plan:

1.    Restore to the RPO within the RTO
2.    Address collateral damage
3.    Reset the passwords of any accounts in use on the compromised system
4.    Resolve any related security incidents
5.    Perform routine cyber hygiene due diligence
6.    Engage external cybersecurity-as-a-service providers and response professionals

  
--------------

### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)
