## Playbook: Cloud Email Compromise

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Collection|T1114|Email Collection|  |Google Workspace, Office 365, Windows|User|


```
(P) Preparation

1.    Ensure client software is fully patched
2.    Perform routine inspections of controls/weapons
3.    Verify that logging and alerting are enabled and configured
4.    Make use of risk based conditional access policies
5.    Perform routine phishing education and testing
6.    Familiarize yourself with the available security features of your service
7.    Generate and review reports of logins on a regular basis
8.    Ban the use of passwords that include your company’s name or product names, if possible
9.    Make use of a third party service to monitor for data breaches that include company email addresses
 
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

--------------

### Investigate

`TODO: Expand investigation steps, including key questions and strategies, for Cloud Email Compromise.`


1. Monitor for:
    * Unusual login activity
    * Changes to email forwarding rules
    * Security features being disabled
2. Investigate and clear ALL alerts associated with the impacted assets



--------------

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

`TODO: Customize containment steps, tactical and strategic, for Cloud Email Compromise.`

`TODO: Specify tools and procedures for each step, below.`

1. Inventory (enumerate & assess)
2. Detect | Deny | Disrupt | Degrade | Deceive | Destroy
3. Observe -> Orient -> Decide -> Act
4. Review logs to determine if the attacker successfully accessed any other accounts
5. Lock any compromised accounts
6. Issue perimeter enforcement for known threat actor locations

`TODO: Consider automating containment measures using orchestration tools.`

#### Eradicate

`TODO: Customize eradication steps, tactical and strategic, for Cloud Email Compromise.`

`TODO: Specify tools and procedures for each step, below.`



#### Reference: Remediation Resources

`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`

--------------

### Communicate

`TODO: Customize communication steps for <Type of Incident>`

`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`

In addition to the general steps and guidance in the incident response plan:

1.    Close the attack vector
2.    Reset the credentials of any compromised accounts
3.    Inspect the workstations of compromised users

--------------

### Recover

`TODO: Customize recovery steps for Cloud Email Compromise.`

`TODO: Specify tools and procedures for each step, below.`

In addition to the general steps and guidance in the incident response plan:

1.    Restore to the RPO within the RTO
2.    Resolve any related security incidents
3.    Address collateral damage
4.    Perform routine cyber hygiene due diligence
5.    Engage external cybersecurity-as-a-service providers and response professionals


--------------

### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)
