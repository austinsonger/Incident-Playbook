## Playbook: Scheduled Task/Job 

### MITRE

| Tactic | Technique ID | Technique Name | Sub-Technique Name | Platforms | Permissions Required |
| ------ | ------------ | -------------- | ------------------ |---------- |--------------------- |
| Execution, Persistence, Privilege Escalation | T1053 | Scheduled Task/Job |  | Containers, Linux, Windows, macOS | Administrator, SYSTEM, User  |


**Investigate, remediate (contain, eradicate), and communicate in parallel!**

Assign steps to individuals or teams to work concurrently, when possible; this playbook is not purely sequential. Use your best judgment.

--------------

### Investigate

1. **Scope of the attack**
    * gather IOCs on the task and see, if there are multiple assets affected.
    * analyze log files to get a better understanding, how the task was created and clarify attack vector.
    * analyze if the user, which created the task, did other actions on assets
2. **Analyze task creation**
    * creation timestamp of the task
    * user that created the task
    * rights of the user
3. **Analyze the task**
    * called binaries
    * provided parameters
    * frequency in which the task is called
    * more IOCs for analyzing the scope of the attack
4. **Determine Severity**
    * number of affected assets
    * indicators of users compromised
    * data at risk
    * clear path of attack

--------------

### Remediate

* **Plan remediation events** where these steps are launched together (or in coordinated fashion), with appropriate teams ready to respond to any disruption.
* **Consider the timing and trade-offs** of remediation actions: your response has consequences.

#### Contain

1. **Originating account**
    * lock the account which created the task
    * change the password of the account and in all locations, where the same password was used
2. **Disable the task and prevent re-creation**
    * disable the task
    * block other ways of task creation identified by the investigation
3. **Automated blocking**
    * if in an highly controlled environment with good baseline-images, consider blocking unknown services on creation

#### Eradicate

1. **Remove task**
    * if it is clear how the task was created and what it did, you can remove it
2. **Reset asset to an clean state**
    * as an alternative, consider restoring an old image or re-imaging the asset


#### Reference: Remediation Resources

1. Resources need strongly depend on the complexity of the task and the overall attack.

--------------

### Communicate

In addition to the general steps and guidance in the incident response plan:
1. **Should be covered in default response plan**


--------------

### Recover

In addition to the general steps and guidance in the incident response plan:
1. **Monitoring**
    * monitor the environment more closely for the creation of tasks over the upcoming weeks.

--------------
  
### Lessons Learned

1. Follow default lessons learned procedures
 

--------------

### Resources

#### Additional Information

1. [MITRE T1053]("https://attack.mitre.org/techniques/T1053/")

