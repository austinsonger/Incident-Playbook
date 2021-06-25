| Event                      | Category                               | Event Description                                      |
| -------------------------- | -------------------------------------- | ------------------------------------------------------ |
| AUDIT_SYSTEM_BOOT          | System Lifecycle                       | System boot                                            |
| AUDIT_SYSTEM_RUNLEVEL      | System Lifecycle                       | System runlevel change                                 |
| AUDIT_DAEMON_START         | System Lifecycle                       | Audit daemon startup record                            |
| AUDIT_DAEMON_ABORT         | System Lifecycle                       | Audit daemon error stop record                         |
| AUDIT_SERVICE_START        | System Lifecycle                       | Service (daemon) start                                 |
| AUDIT_SERVICE_STOP         | System Lifecycle                       | Service (daemon) stop                                  |
| AUDIT_SYSTEM_SHUTDOWN      | System Lifecycle                       | System shutdown                                        |
| AUDIT_DAEMON_END           | System Lifecycle                       | Audit daemon normal stop record                        |
| AUDIT_ADD_USER             | User Account Lifecycle                 | user mapping created                                   |
| AUDIT_USER_MGMT            | User Account Lifecycle                 | user account attribute changed                         |
| AUDIT_USER_CHAUTHTOK       | User Account Lifecycle                 | user authentication token (e.g. password) changed      |
| AUDIT_ROLE_ASSIGN          | User Account Lifecycle                 | a role was assigned to user account                    |
| AUDIT_ROLE_REMOVE          | User Account Lifecycle                 | a role was removed from user account                   |
| AUDIT_DEL_USER             | User Account Lifecycle                 | a user mapping was deleted                             |
| AUDIT_ADD_GROUP            | User Account Lifecycle                 | a group mapping was created                            |
| AUDIT_GRP_MGMT             | User Account Lifecycle                 | an attribute of the group was changed                  |
| AUDIT_GRP_CHAUTHTOK        | User Account Lifecycle                 | group authentication token (e.g. password) changed     |
| AUDIT_DEL_GROUP            | User Account Lifecycle                 | a group mapping was deleted                            |
| AUDIT_CRYPTO_KEY_USER      | User Login Lifecycle                   | Create, delete, negotiate crypto keys                  |
| AUDIT_CRYPTO_SESSION       | User Login Lifecycle                   | Record parameters set during TLS session establishment |
| AUDIT_USER_AUTH            | User Login Lifecycle                   | User system access authentication                      |
| AUDIT_LOGIN                | User Login Lifecycle                   | Define the login id and information                    |
| AUDIT_USER_ACCT            | User Login Lifecycle                   | User system access authorization                       |
| AUDIT_USER_CHAUTHTOK       | User Login Lifecycle                   | User acct password or pin changed                      |
| AUDIT_USER_ERR             | User Login Lifecycle                   | User acct state error                                  |
| AUDIT_CRED_ACQ             | User Login Lifecycle                   | User credential acquired                               |
| AUDIT_USER_ROLE_CHANGE     | User Login Lifecycle                   | User changed to a new role                             |
| AUDIT_USER_START           | User Login Lifecycle                   | User session start                                     |
| AUDIT_USER_LOGIN           | User Login Lifecycle                   | User has logged in                                     |
| AUDIT_CRED_REFR            | User Login Lifecycle                   | User credential refreshed                              |
| AUDIT_GRP_AUTH             | User Login Lifecycle                   | Authentication for group password                      |
| AUDIT_CHUSER_ID            | User Login Lifecycle                   | Changed user ID supplemental data                      |
| AUDIT_CHGRP_ID             | User Login Lifecycle                   | User space group ID changed                            |
| AUDIT_USER_LOGOUT          | User Login Lifecycle                   | User has logged out                                    |
| AUDIT_USER_END             | User Login Lifecycle                   | User session end                                       |
| AUDIT_CRED_DISP            | User Login Lifecycle                   | User credential disposed                               |
| AUDIT_ANOM_LOGIN_FAILURES  | User Login Lifecycle                   | Failed login limit reached                             |
| AUDIT_ANOM_LOGIN_TIME      | User Login Lifecycle                   | Login attempted at bad time                            |
| AUDIT_ANOM_LOGIN_SESSIONS  | User Login Lifecycle                   | Max concurrent sessions reached                        |
| AUDIT_ANOM_LOGIN_ACCT      | User Login Lifecycle                   | Login attempted to watched acct                        |
| AUDIT_ANOM_LOGIN_LOCATION  | User Login Lifecycle                   | Login from forbidden location                          |
| AUDIT_VIRT_MACHINE_ID      | Virtualization Manager Guest Lifecycle | Records guest name to be associated with events        |
| AUDIT_VIRT_INTEGRITY_CHECK | Virtualization Manager Guest Lifecycle | Records results of guest integrity test                |
| AUDIT_VIRT_RESOURCE        | Virtualization Manager Guest Lifecycle | Records assignment of all resources to guest           |
| AUDIT_VIRT_CONTROL         | Virtualization Manager Guest Lifecycle | Records start/pause/stop of guest                      |
| AUDIT_VIRT_CREATE          | Virtualization Manager Guest Lifecycle | Records the creation of the guest image                |
| AUDIT_VIRT_DESTROY         | Virtualization Manager Guest Lifecycle | Records the destruction of the guest image             |
| AUDIT_VIRT_MIGRATE_IN      | Virtualization Manager Guest Lifecycle | Records information about the arrival of a guest       |
| AUDIT_VIRT_MIGRATE_OUT     | Virtualization Manager Guest Lifecycle | Records information about the departure of a guest     |


