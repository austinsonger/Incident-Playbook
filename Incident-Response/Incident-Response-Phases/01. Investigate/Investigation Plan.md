## Playbook: Basic steps of an incident investigation

### Things to keep in mind

A central tenet of analysing data is maintaining a clear chain-of-custody to prevent accusations of manipulation or mis-handling of evidence by the analyst.

Consider that every action taken on a piece of data may leave a trace and should leave a chain-of-custody event.

Minimize the impact on original data and work on hashed copies which are created as soon as possible. Never work on original media!

### Investigation steps

#### Data Collection

1. Goal: _Identify and acquire data from potential sources_

2. Approach
  - Identify data sources and relevant media
    - enumerate physical sources with the intent of creating full images if possible
      - volatile memory
      - non-volatile disks / drives
      - USBs, network media
    - consider relevant logical sources if full images of physical sources is not possible
      - OS logs (Windows Event Logs, Linux logs)
      - auditd, syslog logs
      - console logs (Powershell, linux shells)
      - ...
  - Acquire data
      - Prioritize. Create a plan to acquire relevant data and consider:
          - value
          - order of volatility
          - amount of effort required
      - Acquire.
          - collect volatile data (by imaging as well as possible)
          - duplicate non-volatile data (use hardware write-blockers if possible)
          - secure original sources and store them safely
      - Verify integrity.
          - create digests (== hash/checksum) of every piece of original and copied data
          - if necessary or possible, take photos of process
      - Further considerations
          - consider business cost of data acqusition -> how much will it interfere with business? If office clients are confiscated, provide user with new hardware.

#### Data Examination
  
1. Goal: _extract relevant information from collected data_

2. Approach
      - reduce / filter amount of data in current scope
        - filter source to relevant areas and components
        - filter files by type, content or metadata
      - consider context and initial alerts to identify interesting areas, e.g. identify the initial infection vector
      - don't go through raw data line-by-line without knowing what to look for, instead focus on getting a bigger picture first of the system's behaviour and start small
      - don't be afraid to skip over a source when it seems exhausted and come back later
      - be aware of ways attackers might hide their traces, e.g. timestomping (faking timestamps to not seem suspicious)

#### Data Analysis

1. Goal: _draw conclusions from relevant information_

2. Approach
      - "The foundation of forensics is using a methodical approach to reach appropriate conclusions based on the available data or determine that no conclusion can yet be drawn." - NIST 800-86 3.3
      - cross-correlate data from different sources
      - translate hypothesis into a theory and try to prove or falsify it (convert "soft" hunches and indicators into hard evidence)

#### Reporting on Results

1. Goal: _make result of the analysis phase presentable_

2. Approach
      - Consider alternative explanations due to acknowledging insufficient information or incomplete artifacts by providing each plausible explanation for an event
      - Consider the report's audience in regards to level of (technical) detail, focus on process or result, using visuals and providing lessons learned
      - Consider how the results may be used:
        - take measures to prevent future incidents
        - change guidelines or their implementation
        - identify further actionable information

#### Lessons learned
    
1. Goal: _get better_

2. Approach
      - re-examine previous reports and investigations, their problems and address them
      - identify areas where knowledge is missing and acquire it
      - continuously train staff
    
--------------

### Resources

#### Additional Information

1. NIST Special Publication 800-86: Guide to Integrating Forensic Techniques into Incident Response, Recommendations of the National Institute of Standards and Technology, August 2006
