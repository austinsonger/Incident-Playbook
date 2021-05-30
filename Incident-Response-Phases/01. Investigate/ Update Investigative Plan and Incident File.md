## Update Investigative Plan and Incident File

1. Review and refine incident impact.
1. Review and refine incident vector.
1. Review and refine incident summary.
1. Review and refine incident timeline with facts and inferences.
1. Create hypotheses: what may have happened, and with what confidence.
1. **Identify and prioritize key questions** (information gaps) to support or discredit hypotheses.
    * Use the MITRE ATT&CK matrix or similar framework to [develop questions](#reference-attacker-tactics-to-key-questions-matrix).
        * [ATT&CK for Enterprise](https://attack.mitre.org/wiki/Main_Page), including links to Windows, Mac, and Linux specifics.
        * [ATT&CK Mobile Profile](https://attack.mitre.org/mobile/index.php/Main_Page) for mobile devices.
    * Use interrogative words as inspiration:
        * **When?**: first compromise, first data loss, access to x data, access to y system, _etc._
        * **What?**: impact, vector, root cause, motivation, tools/exploits used, accounts/systems compromised, data targeted/lost, infrastructure, IOCs, _etc._
        * **Where?**: attacker location, affected business units, infrastructure, _etc._
        * **How?**: compromise (exploit), persistence, access, exfiltration, lateral movement, _etc._
        * **Why?**: targeted, timing, access x data, access y system, _etc._
        * **Who?**: attacker, affected users, affected customers, _etc._
1. **Identify and prioritize witness devices and strategies** to answer key questions.
    * Consult network diagrams, asset management systems, and SME expertise
    * Check the [Response Resource List](#reference-response-resource-list))
1. Refer to [incident playbooks](#playbooks) for key questions, witness devices, and strategies for investigating common or highly damaging threats.

**The investigative plan is critical to an effective response; it drives all investigative actions.  Use critical thinking, creativity, and sound judgment.**

### Reference: Attacker Tactics to Key Questions Matrix

Attacker Tactic      | The way attackers ...         | Possible Key Questions
-------------------- | ----------------------------- | -----------------------------------------
Reconnaissance       | ... learn about targets       | How? Since when? Where? Which systems?
Resource Development | ... build infrastructure      | Where? Which systems?
Initial Access       | ... get in                    | How? Since when? Where? Which systems?
Execution            | ... run hostile code          | What malware? What tools? Where? When?
Persistence          | ... stick around              | How? Since when? Where? Which systems?
Privilege Escalation | ... get higher level access   | How? Where? What tools?
Defense Evasion      | ... dodge security            | How? Where? Since when?
Credential Access    | ... get/create accounts       | Which accounts? Since when? Why?
Discovery            | ... learn our network         | How? Where? What do they know?
Lateral Movement     | ... move around               | How? When? Which accounts?
Collection           | ... find and gather data      | What data? Why? When? Where?
Command and Control  | ... control tools and systems | How? Where? Who? Why?
Exfiltration         | ... take data                 | What data? How? When? Where?
Impact               | ... break things              | What systems or data? How? When? Where? How bad?
