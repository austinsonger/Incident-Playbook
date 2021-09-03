| Macro Name                     | Value | Origin | Class                      | Description                                                                                               |
| ------------------------------ | ----- | ------ | -------------------------- | --------------------------------------------------------------------------------------------------------- |
| AUDIT_GET                      | 1000  | USER   | CTL                        | Get status                                                                                                |
| AUDIT_SET                      | 1001  | USER   | CTL                        | Set status (enable/disable/auditd)                                                                        |
| AUDIT_LIST                     | 1002  | USER   | DEP                        | List syscall rules -- deprecated                                                                          |
| AUDIT_ADD                      | 1003  | USER   | DEP                        | Add syscall rule -- deprecated                                                                            |
| AUDIT_DEL                      | 1004  | USER   | DEP                        | Delete syscall rule -- deprecated                                                                         |
| AUDIT_USER                     | 1005  | USER   | DEP                        | Message from userspace -- deprecated                                                                      |
| AUDIT_LOGIN                    | 1006  | KERN   | IND                        | Define the login ID and information                                                                       |
| AUDIT_WATCH_INS                | 1007  | USER   | DEP                        | Insert file/dir watch entry                                                                               |
| AUDIT_WATCH_REM                | 1008  | USER   | DEP                        | Remove file/dir watch entry                                                                               |
| AUDIT_WATCH_LIST               | 1009  | USER   | DEP                        | List all file/dir watches                                                                                 |
| AUDIT_SIGNAL_INFO              | 1010  | USER   | CTL                        | Get info about sender of signal to auditd                                                                 |
| AUDIT_ADD_RULE                 | 1011  | USER   | CTL                        | Add syscall filtering rule                                                                                |
| AUDIT_DEL_RULE                 | 1012  | USER   | CTL                        | Delete syscall filtering rule                                                                             |
| AUDIT_LIST_RULES               | 1013  | USER   | CTL                        | List syscall filtering rules                                                                              |
| AUDIT_TRIM                     | 1014  | USER   | CTL                        | Trim junk from watched tree                                                                               |
| AUDIT_MAKE_EQUIV               | 1015  | USER   | CTL                        | Append to watched tree                                                                                    |
| AUDIT_TTY_GET                  | 1016  | USER   | CTL                        | Get TTY auditing status                                                                                   |
| AUDIT_TTY_SET                  | 1017  | USER   | CTL                        | Set TTY auditing status                                                                                   |
| AUDIT_SET_FEATURE              | 1018  | USER   | CTL                        | Turn an audit feature on or off                                                                           |
| AUDIT_GET_FEATURE              | 1019  | USER   | CTL                        | Get which features are enabled                                                                            |
| AUDIT_USER_AUTH                | 1100  | USER   | IND                        | User system access authentication                                                                         |
| AUDIT_USER_ACCT                | 1101  | USER   | IND                        | User system access authorization                                                                          |
| AUDIT_USER_MGMT                | 1102  | USER   | IND                        | User account attribute change                                                                             |
| AUDIT_CRED_ACQ                 | 1103  | USER   | IND                        | User credential acquired                                                                                  |
| AUDIT_CRED_DISP                | 1104  | USER   | IND                        | User credential disposed                                                                                  |
| AUDIT_USER_START               | 1105  | USER   | IND                        | User session start                                                                                        |
| AUDIT_USER_END                 | 1106  | USER   | IND                        | User session end                                                                                          |
| AUDIT_USER_AVC                 | 1107  | USER   | IND                        | User space AVC (Access Vector Cache) message                                                              |
| AUDIT_USER_CHAUTHTOK           | 1108  | USER   | IND                        | User account password or PIN changed                                                                      |
| AUDIT_USER_ERR                 | 1109  | USER   | IND                        | User account state error                                                                                  |
| AUDIT_CRED_REFR                | 1110  | USER   | IND                        | User credential refreshed                                                                                 |
| AUDIT_USYS_CONFIG              | 1111  | USER   | IND                        | User space system config change                                                                           |
| AUDIT_USER_LOGIN               | 1112  | USER   | IND                        | User has logged in                                                                                        |
| AUDIT_USER_LOGOUT              | 1113  | USER   | IND                        | User has logged out                                                                                       |
| AUDIT_ADD_USER                 | 1114  | USER   | IND                        | User account added                                                                                        |
| AUDIT_DEL_USER                 | 1115  | USER   | IND                        | User account deleted                                                                                      |
| AUDIT_ADD_GROUP                | 1116  | USER   | IND                        | Group account added                                                                                       |
| AUDIT_DEL_GROUP                | 1117  | USER   | IND                        | Group account deleted                                                                                     |
| AUDIT_DAC_CHECK                | 1118  | USER   | IND                        | User space DAC check results                                                                              |
| AUDIT_CHGRP_ID                 | 1119  | USER   | IND                        | User space group ID changed                                                                               |
| AUDIT_TEST                     | 1120  | USER   | IND                        | Used for test success messages                                                                            |
| AUDIT_TRUSTED_APP              | 1121  | USER   | IND                        | Trusted app msg - freestyle text                                                                          |
| AUDIT_USER_SELINUX_ERR         | 1122  | USER   | IND                        | SELinux user space error                                                                                  |
| AUDIT_USER_CMD                 | 1123  | USER   | IND                        | User shell command and args                                                                               |
| AUDIT_USER_TTY                 | 1124  | USER   | IND                        | Non-ICANON TTY input meaning                                                                              |
| AUDIT_CHUSER_ID                | 1125  | USER   | IND                        | Changed user ID supplemental data                                                                         |
| AUDIT_GRP_AUTH                 | 1126  | USER   | IND                        | Authentication for group password                                                                         |
| AUDIT_SYSTEM_BOOT              | 1127  | USER   | IND                        | System boot                                                                                               |
| AUDIT_SYSTEM_SHUTDOWN          | 1128  | USER   | IND                        | System shutdown                                                                                           |
| AUDIT_SYSTEM_RUNLEVEL          | 1129  | USER   | IND                        | System runlevel change                                                                                    |
| AUDIT_SERVICE_START            | 1130  | USER   | IND                        | Service (daemon) start                                                                                    |
| AUDIT_SERVICE_STOP             | 1131  | USER   | IND                        | Service (daemon) stop                                                                                     |
| AUDIT_GRP_MGMT                 | 1132  | USER   | IND                        | Group account attribute was modified                                                                      |
| AUDIT_GRP_CHAUTHTOK            | 1133  | USER   | IND                        | Group account password or PIN changed                                                                     |
| AUDIT_MAC_CHECK                | 1134  | USER   | IND                        | User space MAC (Mandatory Access Control) decision results                                                |
| AUDIT_ACCT_LOCK                | 1135  | USER   | IND                        | User's account locked by admin                                                                            |
| AUDIT_ACCT_UNLOCK              | 1136  | USER   | IND                        | User's account unlocked by admin                                                                          |
| AUDIT_USER_DEVICE              | 1137  | USER   | IND                        | User space hotplug device changes                                                                         |
| AUDIT_SOFTWARE_UPDATE          | 1138  | USER   | IND                        | Software update event                                                                                     |
| AUDIT_DAEMON_START             | 1200  | USER   | IND                        | Daemon startup record                                                                                     |
| AUDIT_DAEMON_END               | 1201  | USER   | IND                        | Daemon normal stop record                                                                                 |
| AUDIT_DAEMON_ABORT             | 1202  | USER   | IND                        | Daemon error stop record                                                                                  |
| AUDIT_DAEMON_CONFIG            | 1203  | USER   | IND                        | Daemon config change                                                                                      |
| AUDIT_DAEMON_RECONFIG          | 1204  | USER   | IND                        | Auditd should reconfigure                                                                                 |
| AUDIT_DAEMON_ROTATE            | 1205  | USER   | IND                        | Auditd should rotate logs                                                                                 |
| AUDIT_DAEMON_RESUME            | 1206  | USER   | IND                        | Auditd should resume logging                                                                              |
| AUDIT_DAEMON_ACCEPT            | 1207  | USER   | IND                        | Auditd accepted remote connection                                                                         |
| AUDIT_DAEMON_CLOSE             | 1208  | USER   | IND                        | Auditd closed remote connection                                                                           |
| AUDIT_DAEMON_ERR               | 1209  | USER   | IND                        | Auditd internal error                                                                                     |
| AUDIT_SYSCALL                  | 1300  | KERN   | SC                         | System call event information                                                                             |
| AUDIT_FS_WATCH                 | 1301  | KERN   | DEP                        | Deprecated                                                                                                |
| AUDIT_PATH                     | 1302  | KERN   | SC                         | Filename path information                                                                                 |
| AUDIT_IPC                      | 1303  | KERN   | SC                         | System call IPC (Inter-Process Communication) object                                                      |
| AUDIT_SOCKETCALL               | 1304  | KERN   | SC                         | System call socketcall arguments                                                                          |
| AUDIT_CONFIG_CHANGE            | 1305  | KERN   | IND                        | Audit system configuration change                                                                         |
| AUDIT_SOCKADDR                 | 1306  | KERN   | SC                         | System call socket address argument information                                                           |
| AUDIT_CWD                      | 1307  | KERN   | SC                         | Current working directory                                                                                 |
| AUDIT_EXECVE                   | 1309  | KERN   | SC                         | Arguments supplied to the execve system call                                                              |
| AUDIT_IPC_SET_PERM             | 1311  | KERN   | SC                         | IPC new permissions record type                                                                           |
| AUDIT_MQ_OPEN                  | 1312  | KERN   | SC                         | POSIX MQ open record type                                                                                 |
| AUDIT_MQ_SENDRECV              | 1313  | KERN   | SC                         | POSIX MQ send/receive record type                                                                         |
| AUDIT_MQ_NOTIFY                | 1314  | KERN   | SC                         | POSIX MQ notify record type                                                                               |
| AUDIT_MQ_GETSETATTR            | 1315  | KERN   | SC                         | POSIX MQ get/set attribute record type                                                                    |
| AUDIT_KERNEL_OTHER             | 1316  | KERN   | IND                        | For use by 3rd party modules                                                                              |
| AUDIT_FD_PAIR                  | 1317  | KERN   | SC                         | Information for pipe and socketpair system calls                                                          |
| AUDIT_OBJ_PID                  | 1318  | KERN   | SC                         | ptrace target                                                                                             |
| AUDIT_TTY                      | 1319  | KERN   | IND                        | Input on an administrative TTY                                                                            |
| AUDIT_EOE                      | 1320  | KERN   | CTL                        | End of multi-record event                                                                                 |
| AUDIT_BPRM_FCAPS               | 1321  | KERN   | SC                         | Information about file system capabilities increasing permissions                                         |
| AUDIT_CAPSET                   | 1322  | KERN   | SC                         | Record showing argument to sys_capset setting process-based capabilities                                  |
| AUDIT_MMAP                     | 1323  | KERN   | SC                         | Mmap system call file descriptor and flags                                                                |
| AUDIT_NETFILTER_PKT            | 1324  | KERN   | IND                        | Packets traversing netfilter chains                                                                       |
| AUDIT_NETFILTER_CFG            | 1325  | KERN   | IND/SC                     | Netfilter chain modifications                                                                             |
| AUDIT_SECCOMP                  | 1326  | KERN   | IND                        | Secure Computing event                                                                                    |
| AUDIT_PROCTITLE                | 1327  | KERN   | SC                         | Process Title info                                                                                        |
| AUDIT_FEATURE_CHANGE           | 1328  | KERN   | IND                        | Audit feature changed value                                                                               |
| AUDIT_REPLACE                  | 1329  | KERN   | CTL                        | Replace auditd if this probe unanswerd                                                                    |
| AUDIT_KERN_MODULE              | 1330  | KERN   | SC                         | Kernel Module events                                                                                      |
| AUDIT_FANOTIFY                 | 1331  | KERN   | SC                         | Fanotify access decision                                                                                  |
| AUDIT_TIME_INJOFFSET           | 1332  | KERN   | SC                         | Timekeeping offset injected                                                                               |
| AUDIT_TIME_ADJNTPVAL           | 1333  | KERN   | SC                         | NTP value adjustment                                                                                      |
| AUDIT_BPF                      | 1334  | KERN   | SC                         | BPF load/unload                                                                                           |
| AUDIT_EVENT_LISTENER           | 1335  | SC     | audit mcast sock join/part |                                                                                                           |
| AUDIT_AVC                      | 1400  | KERN   | SC                         | SELinux AVC (Access Vector Cache) denial or grant                                                         |
| AUDIT_SELINUX_ERR              | 1401  | KERN   | SC                         | Internal SELinux errors                                                                                   |
| AUDIT_AVC_PATH                 | 1402  | KERN   | SC                         | dentry, vfsmount pair from AVC                                                                            |
| AUDIT_MAC_POLICY_LOAD          | 1403  | KERN   | SC                         | SELinux Policy file load                                                                                  |
| AUDIT_MAC_STATUS               | 1404  | KERN   | SC                         | SELinux mode (enforcing, permissive, off) changed                                                         |
| AUDIT_MAC_CONFIG_CHANGE        | 1405  | KERN   | SC                         | SELinux Boolean value modification                                                                        |
| AUDIT_MAC_UNLBL_ALLOW          | 1406  | KERN   | SC                         | NetLabel: allow unlabeled traffic                                                                         |
| AUDIT_MAC_CIPSOV4_ADD          | 1407  | KERN   | SC                         | NetLabel: add CIPSOv4 (Commercial Internet Protocol Security Option) DOI (Domain of Interpretation) entry |
| AUDIT_MAC_CIPSOV4_DEL          | 1408  | KERN   | SC                         | NetLabel: del CIPSOv4 (Commercial Internet Protocol Security Option) DOI (Domain of Interpretation) entry |
| AUDIT_MAC_MAP_ADD              | 1409  | KERN   | SC                         | NetLabel: add LSM (Linux Security Module) domain mapping                                                  |
| AUDIT_MAC_MAP_DEL              | 1410  | KERN   | SC                         | NetLabel: del LSM (Linux Security Module) domain mapping                                                  |
| AUDIT_MAC_IPSEC_ADDSA          | 1411  | KERN   | DEP                        | Not used                                                                                                  |
| AUDIT_MAC_IPSEC_DELSA          | 1412  | KERN   | DEP                        | Not used                                                                                                  |
| AUDIT_MAC_IPSEC_ADDSPD         | 1413  | KERN   | DEP                        | Not used                                                                                                  |
| AUDIT_MAC_IPSEC_DELSPD         | 1414  | KERN   | DEP                        | Not used                                                                                                  |
| AUDIT_MAC_IPSEC_EVENT          | 1415  | KERN   | SC                         | Audit an IPsec event                                                                                      |
| AUDIT_MAC_UNLBL_STCADD         | 1416  | KERN   | SC                         | NetLabel: add a static label                                                                              |
| AUDIT_MAC_UNLBL_STCDEL         | 1417  | KERN   | SC                         | NetLabel: del a static label                                                                              |
| AUDIT_MAC_CALIPSO_ADD          | 1418  | KERN   | SC                         | NetLabel: add CALIPSO DOI (Domain of Interpretation) entry                                                |
| AUDIT_MAC_CALIPSO_DEL          | 1419  | KERN   | SC                         | NetLabel: delete CALIPSO DOI (Domain of Interpretation) entry                                             |
| AUDIT_AA                       | 1500  | KERN   | ?                          |                                                                                                           |
| AUDIT_APPARMOR_AUDIT           | 1501  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_ALLOWED         | 1502  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_DENIED          | 1503  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_HINT            | 1504  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_STATUS          | 1505  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_ERROR           | 1506  | KERN   | SC                         |                                                                                                           |
| AUDIT_APPARMOR_KILL            | 1507  | KERN   | SC                         |                                                                                                           |
| AUDIT_ANOM_PROMISCUOUS         | 1700  | KERN   | SC/IND                     | Device changed promiscuous mode                                                                           |
| AUDIT_ANOM_ABEND               | 1701  | KERN   | IND                        | Process ended abnormally                                                                                  |
| AUDIT_ANOM_LINK                | 1702  | KERN   | SC?                        | Suspicious use of file links                                                                              |
| AUDIT_ANOM_CREAT               | 1703  | KERN   | SC?                        | Suspicious file creation                                                                                  |
| AUDIT_INTEGRITY_DATA           | 1800  | KERN   | SC                         | Data integrity verification                                                                               |
| AUDIT_INTEGRITY_METADATA       | 1801  | KERN   | SC                         | Metadata integrity verification                                                                           |
| AUDIT_INTEGRITY_STATUS         | 1802  | KERN   | SC                         | Integrity enable status                                                                                   |
| AUDIT_INTEGRITY_HASH           | 1803  | KERN   | SC                         | Integrity HASH type                                                                                       |
| AUDIT_INTEGRITY_PCR            | 1804  | KERN   | SC                         | PCR (Platform Configuration Register) invalidation messages                                               |
| AUDIT_INTEGRITY_RULE           | 1805  | KERN   | SC/IND                     | Integrity Policy action                                                                                   |
| AUDIT_INTEGRITY_EVM_XATTR      | 1806  | KERN   | SC                         | EVM XATTRS modifications                                                                                  |
| AUDIT_INTEGRITY_POLICY_RULE    | 1807  | KERN   | SC                         | Integrity Policy rule                                                                                     |
| AUDIT_KERNEL                   | 2000  | KERN   | IND                        | Kernel audit status                                                                                       |
| AUDIT_ANOM_LOGIN_FAILURES      | 2100  | USER   | IND                        | Failed login limit reached                                                                                |
| AUDIT_ANOM_LOGIN_TIME          | 2101  | USER   | IND                        | Login attempted at bad time                                                                               |
| AUDIT_ANOM_LOGIN_SESSIONS      | 2102  | USER   | IND                        | Maximum concurrent sessions reached                                                                       |
| AUDIT_ANOM_LOGIN_ACCT          | 2103  | USER   | IND                        | Login attempted to watched account                                                                        |
| AUDIT_ANOM_LOGIN_LOCATION      | 2104  | USER   | IND                        | Login from forbidden location                                                                             |
| AUDIT_ANOM_MAX_DAC             | 2105  | USER   | IND                        | Max DAC (Discretionary Access Control) failures reached                                                   |
| AUDIT_ANOM_MAX_MAC             | 2106  | USER   | IND                        | Max MAC (Mandatory Access Control) failures reached                                                       |
| AUDIT_ANOM_AMTU_FAIL           | 2107  | USER   | IND                        | AMTU (Abstract Machine Test Utility) failure                                                              |
| AUDIT_ANOM_RBAC_FAIL           | 2108  | USER   | IND                        | RBAC (Role-Based Access Control) self test failure                                                        |
| AUDIT_ANOM_RBAC_INTEGRITY_FAIL | 2109  | USER   | IND                        | RBAC (Role-Based Access Control) file integrity test failure                                              |
| AUDIT_ANOM_CRYPTO_FAIL         | 2110  | USER   | IND                        | Crypto system test failure                                                                                |
| AUDIT_ANOM_ACCESS_FS           | 2111  | USER   | IND                        | Access of file or directory ended abnormally                                                              |
| AUDIT_ANOM_EXEC                | 2112  | USER   | IND                        | Execution of file ended abnormally                                                                        |
| AUDIT_ANOM_MK_EXEC             | 2113  | USER   | IND                        | Make an executable                                                                                        |
| AUDIT_ANOM_ADD_ACCT            | 2114  | USER   | IND                        | Adding a user account ended abnormally                                                                    |
| AUDIT_ANOM_DEL_ACCT            | 2115  | USER   | IND                        | Deleting a user account ended abnormally                                                                  |
| AUDIT_ANOM_MOD_ACCT            | 2116  | USER   | IND                        | Changing an account ended abnormally                                                                      |
| AUDIT_ANOM_ROOT_TRANS          | 2117  | USER   | IND                        | User became root                                                                                          |
| AUDIT_ANOM_LOGIN_SERVICE       | 2118  | USER   | IND                        | Service acct attempted login                                                                              |
| AUDIT_RESP_ANOMALY             | 2200  | USER   | IND                        | Anomaly not reacted to                                                                                    |
| AUDIT_RESP_ALERT               | 2201  | USER   | IND                        | Alert email was sent                                                                                      |
| AUDIT_RESP_KILL_PROC           | 2202  | USER   | IND                        | Kill program                                                                                              |
| AUDIT_RESP_TERM_ACCESS         | 2203  | USER   | IND                        | Terminate session                                                                                         |
| AUDIT_RESP_ACCT_REMOTE         | 2204  | USER   | IND                        | User account locked from remote access                                                                    |
| AUDIT_RESP_ACCT_LOCK_TIMED     | 2205  | USER   | IND                        | User account locked for time                                                                              |
| AUDIT_RESP_ACCT_UNLOCK_TIMED   | 2206  | USER   | IND                        | User account unlocked from time                                                                           |
| AUDIT_RESP_ACCT_LOCK           | 2207  | USER   | IND                        | User account was locked                                                                                   |
| AUDIT_RESP_TERM_LOCK           | 2208  | USER   | IND                        | Terminal was locked                                                                                       |
| AUDIT_RESP_SEBOOL              | 2209  | USER   | IND                        | Set an SELinux boolean                                                                                    |
| AUDIT_RESP_EXEC                | 2210  | USER   | IND                        | Execute a script                                                                                          |
| AUDIT_RESP_SINGLE              | 2211  | USER   | IND                        | Go to single user mode                                                                                    |
| AUDIT_RESP_HALT                | 2212  | USER   | IND                        | Take the system down                                                                                      |
| AUDIT_RESP_ORIGIN_BLOCK        | 2213  | USER   | IND                        | Address blocked by iptables                                                                               |
| AUDIT_RESP_ORIGIN_BLOCK_TIMED  | 2214  | USER   | IND                        | Address blocked for time                                                                                  |
| AUDIT_USER_ROLE_CHANGE         | 2300  | USER   | IND                        | User changed to a new SELinux role                                                                        |
| AUDIT_ROLE_ASSIGN              | 2301  | USER   | IND                        | Administrator assigned user to SELinux role                                                               |
| AUDIT_ROLE_REMOVE              | 2302  | USER   | IND                        | Administrator removed user from SELinux role                                                              |
| AUDIT_LABEL_OVERRIDE           | 2303  | USER   | IND                        | Administrator is overriding a SELinux label                                                               |
| AUDIT_LABEL_LEVEL_CHANGE       | 2304  | USER   | IND                        | Object level SELinux label modified                                                                       |
| AUDIT_USER_LABELED_EXPORT      | 2305  | USER   | IND                        | Object exported with SELinux label                                                                        |
| AUDIT_USER_UNLABELED_EXPORT    | 2306  | USER   | IND                        | Object exported without SELinux label                                                                     |
| AUDIT_DEV_ALLOC                | 2307  | USER   | IND                        | Device was allocated                                                                                      |
| AUDIT_DEV_DEALLOC              | 2308  | USER   | IND                        | Device was deallocated                                                                                    |
| AUDIT_FS_RELABEL               | 2309  | USER   | IND                        | Filesystem relabeled                                                                                      |
| AUDIT_USER_MAC_POLICY_LOAD     | 2310  | USER   | IND                        | Userspace daemon loaded SELinux policy                                                                    |
| AUDIT_ROLE_MODIFY              | 2311  | USER   | IND                        | Administrator modified an SELinux role                                                                    |
| AUDIT_USER_MAC_CONFIG_CHANGE   | 2312  | USER   | IND                        | Change made to MAC (Mandatory Access Control) policy                                                      |
| AUDIT_USER_MAC_STATUS          | 2313  | USER   | IND                        | Userspc daemon enforcing change                                                                           |
| AUDIT_CRYPTO_TEST_USER         | 2400  | USER   | IND                        | Cryptographic test results                                                                                |
| AUDIT_CRYPTO_PARAM_CHANGE_USER | 2401  | USER   | IND                        | Cryptographic attribute change                                                                            |
| AUDIT_CRYPTO_LOGIN             | 2402  | USER   | IND                        | Cryptographic officer login                                                                               |
| AUDIT_CRYPTO_LOGOUT            | 2403  | USER   | IND                        | Cryptographic officer logout                                                                              |
| AUDIT_CRYPTO_KEY_USER          | 2404  | USER   | IND                        | Create, delete, negotiate cryptographic key identifier                                                    |
| AUDIT_CRYPTO_FAILURE_USER      | 2405  | USER   | IND                        | Fail decrypt, encrypt or randomize operation                                                              |
| AUDIT_CRYPTO_REPLAY_USER       | 2406  | USER   | IND                        | Cryptographic replay attack detected                                                                      |
| AUDIT_CRYPTO_SESSION           | 2407  | USER   | IND                        | Parameters set during TLS session establishment                                                           |
| AUDIT_CRYPTO_IKE_SA            | 2408  | USER   | IND                        | Parameters related to IKE SA                                                                              |
| AUDIT_CRYPTO_IPSEC_SA          | 2409  | USER   | IND                        | Parameters related to IPSEC SA                                                                            |
| AUDIT_VIRT_CONTROL             | 2500  | USER   | IND                        | Start, Pause, Stop VM                                                                                     |
| AUDIT_VIRT_RESOURCE            | 2501  | USER   | IND                        | Resource assignment                                                                                       |
| AUDIT_VIRT_MACHINE_ID          | 2502  | USER   | IND                        | Binding of label to VM                                                                                    |
| AUDIT_VIRT_INTEGRITY_CHECK     | 2503  | USER   | IND                        | Guest integrity results                                                                                   |
| AUDIT_VIRT_CREATE              | 2504  | USER   | IND                        | Creation of guest image                                                                                   |
| AUDIT_VIRT_DESTROY             | 2505  | USER   | IND                        | Destruction of guest image                                                                                |
| AUDIT_VIRT_MIGRATE_IN          | 2506  | USER   | IND                        | Inbound guest migration info                                                                              |
| AUDIT_VIRT_MIGRATE_OUT         | 2507  | USER   | IND                        | Outbound guest migration info                                                                             |
