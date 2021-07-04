
|Event ID|Description| Scenario|
| ---------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
|1102|The audit log was cleared.|As attackers infiltrate your environment, they might want to clear their evidence, and cleaning the event log is an indication of that. Make sure to review who cleaned the log, if this operation was intentional and authorized, or if it was unintentional or unknown (due to a compromised account).|
|4624|An account successfully logged on|It is very common to log only the failures, but in many cases, knowing who successfully logged in is important for understanding who performed which action. Make sure to analyze this event on the local machine as well as on the domain controller.|  
|4625|An account failed to log on.|Multiple attempts to access an account can be a sign of a brute-force account attack. Reviewing this log can give you some indications of that.|  
|4657|A registry value was modified|Not everyone should be able to change the registry key, and even when you have high enough privileges to perform this operation, it is still an operation that needs further investigation to understand the veracity of the change.|  
|4663|   |   |  
|4688|   |   |  
|4700|   |   |  
|4702|   |   |  
|4719|   |   |  
|4720|   |   |  
|4722|   |   |  
|4724|   |   |  
|4727|   |   |  
|4732|   |   |  
|4739|   |   |  
|4740|   |   |  
|4825|   |   |  
|4946|   |   |  
|4948|   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  
|   |   |   |  