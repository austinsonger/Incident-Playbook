## Update Remediation Plan

1. Review the incident file at {{INCIDENT_FILE_LOCATION}} using the [incident name](#name-the-incident)
1. Review applicable [playbooks](#playbooks).
1. Review the [Response Resource List](#reference-response-resource-list)).
1. Consider which attacker tactics are in play in this incident.  Use the MITRE [ATT&CK](https://attack.mitre.org/wiki/Main_Page) list (_i.e._, Persistence, Privilege Escalation, Defense Evasion, Credential Access, Discovery, Lateral Movement, Execution, Collection, Exfiltration, and Command and Control), or similar framework.
1. Develop remediations for each tactic in play, as feasible given existing tools and resources.  Consider remediations to [Protect](#protect), [Detect](#detect), [Contain](#contain), and [Eradicate](#eradicate) each attacker behavior.
1. Prioritize based on [timing strategy](#choose-remediation-timing), impact, and urgency.
1. Document in incident file.

Use [information security (infosec) frameworks](https://www.nist.gov/cyberframework) as inspiration, but **do not use incident remediation as a substitute for an infosec program with an appropriate framework.**  Use them to supplement one another.

### Protect

> "How can we stop tactic X from happening again, or reduce risk?  How can we improve future protection?"

Use the following as a starting point for protective remediation:

* Patch applications.
* Patch operating systems.
* Update network and host IPS signatures.
* Update endpoint protection/EDR/anti-virus signatures.
* Reduce locations with critical data.
* Reduce administrative or privileged accounts.
* Enable multi-factor authentication.
* Strengthen password requirements.
* Block unused ports and protocols at segment and network boundaries, both inbound and outbound.
* Whitelist network connections for critical servers and services.

### Detect

> "How can we detect this on new systems or in the future?  How can we improve future detection and investigation?"

Use the following as a starting point for detective remediation:

* Enhance logging and retention for system logs, particularly critical systems.
* Enhance logging for applications, including SaaS applications.
* Enhance log aggregation.
* Update network and host IDS signatures using IOCs.

### Contain

> "How can we stop this from spreading, or getting more severe? How can we improve future containment?"

Use the following as a starting point for containment remediation:

* Implement access lists (ACLs) at network segment boundaries
* Implement blocks at the enterprise boundary, at multiple layers of the [OSI model](https://en.wikipedia.org/wiki/OSI_model).
* Disable or remove compromised account access.
* Block malicious IP addresses or networks.
* Black hole or sinkhole malicious domains.
* Update network and host IPS and anti-malware signatures using IOCs.
* Remove critical or compromised systems from the network.
* Contact providers for assistance (_e.g._, internet service providers, SaaS vendors)
* Whitelist network connections for critical servers and services.
* Kill or disable processes or services.
* Block or remove access for external vendors and partners, especially privileged access.

### Eradicate

> "How can we eliminate this from our assets?  How can we improve future eradication?"

Use the following as a starting point for eradication remediation:

* Rebuild or restore compromised systems and data from known-good state.
* Reset account passwords.
* Remove hostile accounts or credentials.
* Delete or remove specific malware (difficult!).
* Implement alternative vendors.
* Activate and migrate to alternate locations, services, or servers.

## Choose Remediation Timing

Determine the timing strategy---when remediation actions will be taken---by engaging the Incident Commander, the system SMEs and owners, business unit SMEs and owners, and the executive team.  Each strategy is appropriate under different circumstances:

* Choose **immediate** remediation when it is more important to immediately stop attacker activities than to continue investigating.  For example, ongoing financial loss, or ongoing mission failure, active data loss, or prevention of an imminent significant threat.
* Choose **delayed** remediation when it is important to complete the investigation, or important not to alert the attacker.  For example, long-term compromise by an advanced attacker, corporate espionage, or large-scale compromise of an an unknown number of systems.
* Choose **combined** remediation when both immediate and delayed circumstances apply in the same incident.  For example, immediate segmentation of a sensitive server or network to meet regulatory requirements while still investigating a long-term compromise.

## Execute Remediation

* Assess and explain risks of remediation actions to stakeholders.  `TODO: Customize remediation risk approval procedure, if necessary.`
* Immediately implement those remediation actions with little or no affect on the attacker (sometimes called "posturing actions").  For example, many of the [protection](#protect) and [detection](#detect) actions above are good candidates.
* Schedule and task remediation actions according to the timing strategy.
* Execute remediation actions in batches, as events, for maximum effectiveness and minimum risk.
* Document execution status and time in the incident file, especially for temporary measures.

## Iterate Remediation

[Update the remediation plan](#update-remediation-plan) and repeat until closure.
