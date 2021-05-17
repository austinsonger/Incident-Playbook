# Common Mistakes in Incident Handling

After determining that a system or multiple systems may be compromised, system administrators and/or system owners are often tempted to take immediate actions. Although well intentioned to limit the damage of the compromise, some of those actions have the adverse effect of:

1. Modifying volatile data that could give a sense of what has been done; and
2. Tipping the threat actor that the victim organization is aware of the compromise and forcing the actor to either hide their tracks or take more damaging actions (like detonating ransomware).

Below—and partially listed in figure 1—are actions to avoid taking and some of the consequence of taking such actions.

- Mitigating the affected systems before responders can protect and recover data
  - This can cause the loss of volatile data such as memory and other host-based artifacts.
  - The adversary may notice and change their tactics, techniques, and procedures.
- Touching adversary infrastructure (Pinging, NSlookup, Browsing, etc.)
  - These actions can tip off the adversary that they have been detected.
- Preemptively blocking adversary infrastructure
  - Network infrastructure is fairly inexpensive. An adversary can easily change to new command and control infrastructure, and you will lose visibility of their activity.
- Preemptive credential resets
  - Adversary likely has multiple credentials, or worse, has access to your entire Active Directory.
  - Adversary will use other credentials, create new credentials, or forge tickets.
- Failure to preserve or collect log data that could be critical to identifying access to the compromised systems
  - If critical log types are not collected, or are not retained for a sufficient length of time, key information about the incident may not be determinable. Retain log data for at least one year.
- **Communicating over the same network as the incident response is being conducted (ensure all communications are held out-of-band)**
- Only fixing the symptoms, not the root cause
  - Playing “whack-a-mole” by blocking an IP address—without taking steps to determine what the binary is and how it got there—leaves the adversary an opportunity to change tactics and retain access to the network.


