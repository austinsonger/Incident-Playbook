## Create and Deploy Indicators of Compromise (IOCs)

> Emphasize **dynamic and behavioral** indicators alongside static fingerprints.

* Create IOCs based on [initial leads](#collect-initial-leads) and [analysis](#analyze-evidence).
* Create IOCs using an open format supported by your tools (_e.g._, [STIX 2.0](https://oasis-open.github.io/cti-documentation/stix/intro)), if possible. `TODO: Customize IOC format as necessary.`
* Use automation, if possible. `TODO: Add IOC deployment/revocation procedure.`
* **Do not** deploy unrelated, un-curated "feeds" of IOCs; these can cause confusion and fatigue.
* Consider all IOC types:
  * Network-based IOCs such as IP or MAC addresses, ports, email addresses, email content or metadata, URLs, domains, or PCAP patterns.
  * Host-based IOCs such as paths, file hashes, file content or metadata, registry keys, MUTEXes, autoruns, or user artifacts and permissions.
  * Cloud-based IOCs such as log patterns for [SaaS](https://en.wikipedia.org/wiki/Software_as_a_service) or [IaaS](https://en.wikipedia.org/wiki/Infrastructure_as_a_service) deployments
  * Behavioral IOCs (a.k.a., patterns, TTPs) such as process tree patterns, heuristics, deviation from baseline, and login patterns.
* Correlate various IOC types, such as network and host-based indicators on the same systems(s).
