
# Goal
The goal is the intended purpose of the alert. It is a simple, plaintext description of the type of behavior you're attempting to detect in your ADS.

# Categorization
The categorization is a mapping of the ADS to the relevant entry in the MITRE Adversarial Tactics, Techniques, and Common Knowledge (ATT&CK) Framework. ATT&CK provides a language for various post-exploitation techniques and strategies that adversaries might use. 

Mapping to the ATT&CK framework allows for further investigation into the technique, provides a reference to the areas of the killchain where the ADS will be used, and can further drive insight and metrics into alerting gaps. In our environment, we have a knowledge base which maps all of our ADS to individual components of the MITRE ATT&CK framework. When generating a hypothesis for a new alert, an engineer can simply review where we are strongest — or weakest — according to individual ATT&CK techniques.

When selecting a MITRE ATT&CK category, please select both the parent and child category (e.g. Credential Access / Brute Force). 

# Strategy Abstract
The strategy abstract is a high-level walkthrough of how the ADS functions. This describes what the alert is looking for, what technical data sources are used, any enrichment that occurs, and any false positive minimization steps.

# Technical Context
Technical Context provides detailed information and background needed for a responder to understand all components of the alert. This should appropriately link to any platform or tooling knowledge and should include information about the direct aspects of the alert. The goal of the Technical Context section is to provide a self-contained reference for a responder to make a judgement call on any potential alert, even if they do not have direct subject matter expertise on the ADS itself.

# Blind Spots and Assumptions
Blind Spots and Assumptions are the recognized issues, assumptions, and areas where an ADS may not fire. No ADS is perfect and identifying assumptions and blind spots can help other engineers understand how an ADS may fail to fire or be defeated by an adversary.

# False Positives
False Positives are the known instances of an ADS misfiring due to a misconfiguration, idiosyncrasy in the environment, or other non-malicious scenario. The False Positives section notes uniqueness to your own environment, and should include the defining characteristics of any activity that could generate a false positive alert. These false positive alerts should be suppressed within the SIEM to prevent alert generation when a known false positive event occurs.

Each alert / detection strategy needs to be tested and refined to remove as many false positives as possible before it is put into production.

False positive minimization relies on looking at several principles of the strategy and making adjustments, such as:

* Add an additional component to the rule to maximize true positives.
* Remove common false positives through patterns.
* Back-end filtering to store indices of expected false positives.

Ideally, you want your strategy to have the fewest false positives possible while maintaining the spirit of your rule. If a low false positive rate cannot be reached, the alert may need to be broken down, refactored, or entirely discarded.

# Validation
Validation are the steps required to generate a representative true positive event which triggers this alert. This is similar to a unit test and describes how an engineer can cause the ADS to fire. This can be a walkthrough of steps used to generate an alert, a script to trigger the ADS (such as Red Canary's Atomic Red Team Tests), or a scenario used in an alert testing and orchestration platform.

Each alert / detection strategy must have true positive validation. This is a testing process designed to prove the true positives are detected.

True positive validation relies on generating a scenario in which the detection strategy is testing, and then validating in the tool.

To perform positive validation:

* Generate a scenario where a true positive would be generated.
* Document the process of your testing scenario.
* From a testing device, generate a true positive alert.
* Validate the true positive alert was detected by the strategy.

If you are unable to generate a true positive alert, the alert may need to be broken down, refactored, or entirely discarded.

# Priority
Priority describes the various alerting levels that an ADS may be tagged with. While the alert itself should reflect the priority when it is fired through configuration in your SIEM (e.g. High, Medium, Low), this section details the criteria for the specific priorities.

# Response
These are the general response steps in the event that this alert fired. These steps instruct the next responder on the process of triaging and investigating an alert.

# Additional Resources
Additional Resources are any other internal, external, or technical references that may be useful for understanding the ADS.

The title for this alerting strategy should be informative but succinct, and should be targeting a singular event i.e "Non-SA Bastion Logon" rather than reference all events of this type ("Bastion Logons").

The strategy should be stored under the Draft Alerting and Detection Strategies page while you're working on it, peer-reviewed, and a Like attached to the page when approved by a peer to move into production. 
