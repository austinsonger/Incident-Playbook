
<!--

Pre-Event (PE)
- Cyber Security User Awareness regarding phishing, ransomware, social engineering, and other attacks that involve user interaction
- Set Up Data Collection, data collection is managed by Log Management/Security Monitoring/Threat Detection teams. You need to provide them with a list of data that is critically important for IR process. Most of the time, data like DNS and DHCP logs are not being collected, as their value for detection is relatively low. You can refer to the existing Response Actions (Preparation stage) to develop the list
- Set up a centralized long-term log storage. This is one of the most critical problems companies have nowadays. Even if there is such a system, in most of the cases it stores irrelevant data or has too small retention period
- Develop a communication map for both internal (C-level, managers and technical specialists from the other departments, that could be involved in IR process) and external communications (law enforcement, national CERTs, subject matter experts that you have lack of, etc)
- Make sure there are both online and offline backups. In the case of a successful ransomware worm attack, that's the only thing that will help you to safe your critically important data
- Get network architecture map. It will help you to choose the containment strategy, such as isolating specific network segments
- Get Access Control Matrix. It will help you to identify adversary opportunities, such as laterally movement and so on
- Develop assets knowledge base. It will help you to compare observed activity with a normal activity profile for a specific host, user or network segment
- Make sure your toolset for analysis and management is updated and fully operational. Make sure that all the required permissions have been granted as well
- Access vulnerability management system logs. It will help to identify the vulnerabilities a specific host had at a specific time in the past
- Connect with trusted communities for information exchange
- Access to external Network Flow logs.md
- Access to internal Network Flow logs.md
- Access to internal HTTP logs.md
- Access to external HTTP logs.md
- Access to internal DNS logs.md
- Access to external DNS logs.md
- Access to VPN logs.md
- Access to DHCP logs.md
- Access to internal Packet Capture data.md
- Access to internal Packet Capture data.md
- Ability to block an external IP address from being accessed by corporate assets.md
- Ability to block an internal IP address from being accessed by corporate assets.md
- Ability to block an external domain name from being accessed by corporate assets.md
- Ability to block an internal domain name from being accessed by corporate assets.md
- Ability to block an external URL from being accessed by corporate assets.md
- Ability to block an internal URL from being accessed by corporate assets.md
- Ability to block a network port for external communications.md
- Ability to block a network port for internal communications.md
- Ability to block a user for external communications.md
- Ability to block a user for internal communications.md
- Ability to find data transferred at a particular time in the past by its content pattern (i.e. specific string, keyword, binary pattern etc)
- Ability to block data transferring by its content pattern (i.e. specific string, keyword, binary pattern etc)
- Ability to list the data that is being transferred at the moment or at a particular time in the past
- Ability to collect the data that is being transferred at the moment or at a particular time in the past
- Ability to identify the data that is being transferred at the moment or at a particular time in the past (i.e. its content, value)
- Ability to find the data that is being transferred at the moment or at a particular time in the past by its content pattern
- Ability to analyse an User-Agent request header
- Ability to list firewall rules
- Ability to list users who opened a particular email message
- Ability to list receivers of a particular email message
- Ability to block an email domain
- Ability to block an email sender
- Ability to delete an email message
- Ability to quarantine an email message
- Ability to collect an email message
- Ability to analyse an email address
- Ability to analyse an email address
- Ability to list files that have been modified at a particular time in the past
- Ability to list files that have been deleted at a particular time in the past
- Ability to list files that have been downloaded from the internet at a particular time in the past
- Ability to list files with a tampered timestamp
- Ability to find a file by its path (including its name)
- Ability to find file by its metadata (i.e. signature, permissions, MAC times)
- Ability to find a file by its hash
- Ability to find a file by its format
- Ability to find a file by its content pattern (i.e. specific string, keyword, binary pattern etc)
PE58 - Ability to quarantine file by path
PE59 - Ability to quarantine file by hash
PE60 - Ability to quarantine file by format
PE61 - Ability to quarantine file by content pattern
PE62 - Ability to remove file
PE63 - Ability to to analyse file hash
PE64 - Ability to analyse Windows PE
PE65 - Ability to analyse macOS Mach-O file
PE66 - Ability to analyse Unix Elf
PE67 - Ability to Analyse MS Office File
PE68 - Ability to Analyse PDF File
PE69 - Ability to Analyse Script
PE70 - Ability to Analyse Jar
PE71 - Ability to Analyse Filename
-->
