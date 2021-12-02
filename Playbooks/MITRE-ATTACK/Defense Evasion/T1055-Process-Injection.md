## Playbook: Process Injection

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
|Defense Evasion|T1055|Process Injection|                     |Linux, Windows, macOS|                      |


```
(P) Preparation
  
1.    Patch asset vulnerabilities
2.    Perform routine inspections of controls/weapons
3.    Ensure antivirus/endpoint protection software is installed on workstations and laptops
4.    Secure local administrator accounts
5.    Ensure that servers and workstations are logging to a central location
6.    Configure endpoint security solutions to detect and block process injection behaviors
7.    On Unix-based operating systems, restrict the use of ptrace to privileged users
8.    Utilize Yama or other Linux security modules to configure advanced access control and process restrictions
```
  
Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

--------------

### Investigate



1. Monitor for the following Windows API calls:
    * `CreateRemoteThread`
    * `SuspendThread`
    * `SetThreadContext`
    * `ResumeThread`
    * `QueueUserAPC`
    * `NtQueueApcThread`
    * `VirtualAllocEx`
    * `WriteProcessMemory`
2. On Linux systems, monitor the ptrace system call
3. Detect named pipe creation and connection events
4. Collect DLL/PE file events
5. Analyze process behavior and compare to expected activity
6. Investigate and clear ALL alerts associated with impacted assets


--------------

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and tradeoffs** of remediation actions: your response has consequences.

#### Contain

<!--
`TODO: Customize containment steps, tactical and strategic, for Process Injection.`
`TODO: Specify tools and procedures for each step, below.`
-->

1.    Inventory (enumerate & assess)
2.    Detect | Deny | Disrupt | Degrade | Deceive | Destroy
3.    Observe -> Orient -> Decide -> Act
4.    Utilize EDR hunter/killer agents to terminate offending processes
5.    Remove the affected system from the network
6.    Determine the source and pathway of the attack
7.    Issue a perimeter enforcement for known threat actor locations

<!--
`TODO: Consider automating containment measures using orchestration tools.`
-->


#### Eradicate

<!--
`TODO: Customize eradication steps, tactical and strategic, for Process Injection.`
`TODO: Specify tools and procedures for each step, below.`
-->

1.    Close the attack vector
2.    Create forensic backups of affected systems
3.    Perform endpoint/AV scans on affected systems
4.    Reset any compromised passwords
5.    Review the logs of all impacted assets
6.    Patch asset vulnerabilities

#### Reference: Remediation Resources

<!--
`TODO: Specify financial, personnel, and logistical resources to accomplish remediation.`
-->


--------------

### Communicate

<!--
`TODO: Customize communication steps for Process Injection`
`TODO: Specify tools and procedures (including who must be involved) for each step, below, or refer to overall plan.`
-->

In addition to the general steps and guidance in the incident response plan:


 
--------------

### Recover

<!--
`TODO: Customize recovery steps for Process Injection.`
`TODO: Specify tools and procedures for each step, below.`
-->

In addition to the general steps and guidance in the incident response plan:

1.    Restore to the RPO within the RTO
2.    Assess and address collateral damage
3.    Determine the root cause of the incident
4.    Resolve any related security incidents
5.    Restore affected systems to their last clean backup
6.    Perform routine cyber hygiene due diligence
7.    Engage external cybersecurity-as-a-service providers and response professionals
8.    Implement policy changes to reduce future risk
9.    Conduct employee security awareness training

--------------

### Resources

#### Additional Information

1. <a name="identity-and-access-playbook-ref-1"></a>["Title"](#TODO-url), Author Last Name (Date)
