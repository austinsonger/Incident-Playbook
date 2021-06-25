| Name                    | Format              | Meaning                                             | Exception                                       |
| ----------------------- | ------------------- | --------------------------------------------------- | ----------------------------------------------- |
| a[0-3]                  | numeric             | the arguments to a syscall                          | syscall                                         |
| a[[:digit:]+]\[.*\]     | encoded             | the arguments to the execve syscall                 | execve                                          |
| acct                    | encoded             | a user's account name                               |                                                 |
| acl                     | alphabet            | access mode of resource assigned to vm              |                                                 |
| action                  | numeric             | netfilter packet disposition                        |                                                 |
| added                   | numeric             | number of new files detected                        |                                                 |
| addr                    | encoded             | the remote address that the user is connecting from |                                                 |
| apparmor                | encoded             | apparmor event information                          |                                                 |
| arch                    | numeric             | the elf architecture flags                          |                                                 |
| argc                    | numeric             | the number of arguments to an execve syscall        |                                                 |
| audit_backlog_limit     | numeric             | audit system's backlog queue size                   |                                                 |
| audit_backlog_wait_time | numeric             | audit system's backlog wait time                    |                                                 |
| audit_enabled           | numeric             | audit systems's enable/disable status               |                                                 |
| audit_failure           | numeric             | audit system's failure mode                         |                                                 |
| auid                    | numeric             | login user ID                                       |                                                 |
| banners                 | alphanumeric        | banners used on printed page                        |                                                 |
| bool                    | alphanumeric        | name of SELinux boolean                             |                                                 |
| bus                     | alphanumeric        | name of subsystem bus a vm resource belongs to      |                                                 |
| capability              | numeric             | posix capabilities                                  |                                                 |
| cap_fe                  | numeric             | file assigned effective capability map              |                                                 |
| cap_fi                  | numeric             | file inherited capability map                       |                                                 |
| cap_fp                  | numeric             | file permitted capability map                       |                                                 |
| cap_fver                | numeric             | file system capabilities version number             |                                                 |
| cap_pa                  | numeric             | process ambient capability map                      |                                                 |
| cap_pe                  | numeric             | process effective capability map                    |                                                 |
| cap_pi                  | numeric             | process inherited capability map                    |                                                 |
| cap_pp                  | numeric             | process permitted capability map                    |                                                 |
| category                | alphabet            | resource category assigned to vm                    |                                                 |
| cgroup                  | encoded             | path to cgroup in sysfs                             |                                                 |
| changed                 | numeric             | number of changed files                             |                                                 |
| cipher                  | alphanumeric        | name of crypto cipher selected                      |                                                 |
| class                   | alphabet            | resource class assigned to vm                       |                                                 |
| cmd                     | encoded             | command being executed                              |                                                 |
| code                    | numeric             | seccomp action code                                 |                                                 |
| comm                    | encoded             | command line program name                           |                                                 |
| compat                  | numeric             | is_compat_task result                               |                                                 |
| cwd                     | encoded             | the current working directory                       |                                                 |
| daddr                   | alphanumeric        | remote IP address                                   |                                                 |
| data                    | encoded             | TTY text                                            |                                                 |
| default-context         | alphanumeric        | default MAC context                                 |                                                 |
| dev                     | numeric             | in path records                                     | major and minor for device                      |
| dev                     | alphanumeric        | device name as found in /dev                        | avc                                             |
| device                  | encoded             | device name                                         |                                                 |
| dir                     | encoded             | directory name                                      |                                                 |
| direction               | alphanumeric        | direction of crypto operation                       |                                                 |
| dmac                    | numeric             | remote MAC address                                  |                                                 |
| dport                   | numeric             | remote port number                                  |                                                 |
| egid                    | numeric             | effective group ID                                  |                                                 |
| enforcing               | numeric             | new MAC enforcement status                          |                                                 |
| entries                 | numeric             | number of entries in the netfilter table            |                                                 |
| errno                   | numeric             | error code of the audited operation                 |                                                 |
| euid                    | numeric             | effective user ID                                   |                                                 |
| exe                     | encoded             | executable name                                     |                                                 |
| exit                    | numeric             | syscall exit code                                   |                                                 |
| fam                     | alphanumeric        | socket address family                               |                                                 |
| family                  | numeric             | netfilter protocol                                  |                                                 |
| fd                      | numeric             | file descriptor number                              |                                                 |
| file                    | encoded             | file name                                           |                                                 |
| flags                   | numeric             | mmap syscall flags                                  |                                                 |
| fe                      | numeric             | file assigned effective capability map              |                                                 |
| feature                 | alphanumeric        | kernel feature being changed                        |                                                 |
| fi                      | numeric             | file assigned inherited capability map              |                                                 |
| fp                      | numeric             | file assigned permitted capability map              |                                                 |
| fp                      | alphanumeric        | crypto key finger print                             | crypto_key                                      |
| format                  | alphanumeric        | audit log's format                                  |                                                 |
| fsgid                   | numeric             | file system group ID                                |                                                 |
| fsuid                   | numeric             | file system user ID                                 |                                                 |
| fver                    | numeric             | file system capabilities version number             |                                                 |
| gid                     | numeric             | group ID                                            |                                                 |
| grantors                | alphanumeric        | pam modules approving the action                    |                                                 |
| grp                     | encoded             | group name                                          |                                                 |
| hook                    | numeric             | netfilter hook that packet came from                |                                                 |
| hostname                | alphanumeric        | the hostname that the user is connecting from       |                                                 |
| icmp_type               | numeric             | type of icmp message                                |                                                 |
| id                      | numeric             | during account changes                              | the user ID of the account                      |
| igid                    | numeric             | ipc object's group ID                               |                                                 |
| img-ctx                 | alphanumeric        | the vm's disk image context string                  |                                                 |
| inif                    | numeric             | in interface number                                 |                                                 |
| ip                      | alphanumeric        | network address of a printer                        |                                                 |
| ipid                    | numeric             | IP datagram fragment identifier                     |                                                 |
| ino                     | numeric             | inode number                                        |                                                 |
| inode                   | numeric             | inode number                                        |                                                 |
| inode_gid               | numeric             | group ID of the inode's owner                       |                                                 |
| inode_uid               | numeric             | user ID of the inode's owner                        |                                                 |
| invalid_context         | encoded             | SELinux context                                     |                                                 |
| ioctlcmd                | numeric             | The request argument to the ioctl syscall           |                                                 |
| ipx-net                 | numeric             | IPX network number                                  |                                                 |
| item                    | numeric             | which item is being recorded                        |                                                 |
| items                   | numeric             | the number of path records in the event             |                                                 |
| iuid                    | numeric             | ipc object's user ID                                |                                                 |
| kernel                  | alphanumeric        | kernel's version number                             |                                                 |
| key                     | encoded             | key assigned from triggered audit rule              |                                                 |
| kind                    | alphabet            | server or client in crypto operation                |                                                 |
| ksize                   | numeric             | key size for crypto operation                       |                                                 |
| laddr                   | alphanumeric        | local network address                               |                                                 |
| len                     | numeric             | length                                              |                                                 |
| lport                   | alphanumeric        | local network port                                  |                                                 |
| list                    | numeric             | the audit system's filter list number               |                                                 |
| mac                     | alphanumeric        | crypto MAC algorithm selected                       |                                                 |
| macproto                | numeric             | ethernet packet type ID field                       |                                                 |
| maj                     | numeric             | device major number                                 |                                                 |
| major                   | numeric             | device major number                                 |                                                 |
| minor                   | numeric             | device minor number                                 |                                                 |
| mode                    | numeric             | mode flags on a file                                |                                                 |
| model                   | alphanumeric        | security model being used for virt                  |                                                 |
| msg                     | alphanumeric        | the payload of the audit record                     |                                                 |
| nargs                   | numeric             | the number of arguments to a socket call            |                                                 |
| name                    | encoded             | file name in avcs                                   |                                                 |
| nametype                | alphabet            | kind of file operation being referenced             |                                                 |
| net                     | alphanumeric        | network MAC address                                 |                                                 |
| new                     | numeric             | value being set in feature                          |                                                 |
| new-chardev             | encoded             | new character device being assigned to vm           |                                                 |
| new-disk                | encoded             | disk being added to vm                              |                                                 |
| new-enabled             | numeric             | new TTY audit enabled setting                       |                                                 |
| new-fs                  | encoded             | file system being added to vm                       |                                                 |
| new_gid                 | numeric             | new group ID being assigned                         |                                                 |
| new-level               | alphanumeric        | new run level                                       |                                                 |
| new_lock                | numeric             | new value of feature lock                           |                                                 |
| new-log_passwd          | numeric             | new value for TTY password logging                  |                                                 |
| new-mem                 | numeric             | new amount of memory in KB                          |                                                 |
| new-net                 | encoded             | MAC address being assigned to vm                    |                                                 |
| new_pe                  | numeric             | new process effective capability map(deprec)        |                                                 |
| new_pi                  | numeric             | new process inherited capability map(deprec)        |                                                 |
| new_pp                  | numeric             | new process permitted capability map(deprec)        |                                                 |
| new-range               | alphanumeric        | new SELinux range                                   |                                                 |
| new-rng                 | encoded             | device name of rng being added from a vm            |                                                 |
| new-role                | alphanumeric        | new SELinux role                                    |                                                 |
| new-seuser              | alphanumeric        | new SELinux user                                    |                                                 |
| new-vcpu                | numeric             | new number of CPU cores                             |                                                 |
| nlnk-fam                | numeric             | netlink protocol number                             |                                                 |
| nlnk-grp                | numeric             | netlink group number                                |                                                 |
| nlnk-pid                | numeric             | pid of netlink packet sender                        |                                                 |
| oauid                   | numeric             | object's login user ID                              |                                                 |
| obj                     | alphanumeric        | lspp object context string                          |                                                 |
| obj_gid                 | numeric             | group ID of object                                  |                                                 |
| obj_uid                 | numeric             | user ID of object                                   |                                                 |
| oflag                   | numeric             | open syscall flags                                  |                                                 |
| ogid                    | numeric             | file owner group ID                                 |                                                 |
| ocomm                   | encoded             | object's command line name                          |                                                 |
| old                     | numeric             | present value of kernel feature                     |                                                 |
| old                     | numeric             | old value                                           | audit_enabled audit_backlog audit_failure value |
| old-auid                | numeric             | previous auid value                                 |                                                 |
| old-chardev             | encoded             | present character device assigned to vm             |                                                 |
| old-disk                | encoded             | disk being removed from vm                          |                                                 |
| old-enabled             | numeric             | present TTY audit enabled setting                   |                                                 |
| old_enforcing           | numeric             | old MAC enforcement status                          |                                                 |
| old-fs                  | encoded             | file system being removed from vm                   |                                                 |
| old-level               | alphanumeric        | old run level                                       |                                                 |
| old_lock                | numeric             | present value of feature lock                       |                                                 |
| old-log_passwd          | numeric             | present value for TTY password logging              |                                                 |
| old-mem                 | numeric             | present amount of memory in KB                      |                                                 |
| old-net                 | encoded             | present MAC address assigned to vm                  |                                                 |
| old_pa                  | numeric             | old process ambient capability map                  |                                                 |
| old_pe                  | numeric             | old process effective capability map                |                                                 |
| old_pi                  | numeric             | old process inherited capability map                |                                                 |
| old_pp                  | numeric             | old process permitted capability map                |                                                 |
| old_prom                | numeric             | network promiscuity flag                            |                                                 |
| old-range               | alphanumeric        | present SELinux range                               |                                                 |
| old-rng                 | encoded             | device name of rng being removed from a vm          |                                                 |
| old-role                | alphanumeric        | present SELinux role                                |                                                 |
| old-ses                 | numeric             | previous ses value                                  |                                                 |
| old-seuser              | alphanumeric        | present SELinux user                                |                                                 |
| old_val                 | numeric             | current value of SELinux boolean                    |                                                 |
| old-vcpu                | numeric             | present number of CPU cores                         |                                                 |
| op                      | alphanumeric        | the operation being performed that is audited       |                                                 |
| opid                    | numeric             | object's process ID                                 |                                                 |
| oses                    | numeric             | object's session ID                                 |                                                 |
| ouid                    | numeric             | file owner user ID                                  |                                                 |
| outif                   | numeric             | out interface number                                |                                                 |
| pa                      | numeric             | process ambient capability map                      |                                                 |
| pe                      | numeric             | process effective capability map                    |                                                 |
| pi                      | numeric             | process inherited capability map                    |                                                 |
| pp                      | numeric             | process permitted capability map                    |                                                 |
| parent                  | numeric             | the inode number of the parent file                 |                                                 |
| path                    | encoded             | file system path name                               |                                                 |
| per                     | numeric hexadecimal | linux personality                                   |                                                 |
| perm                    | numeric             | the file permission being used                      |                                                 |
| perm_mask               | numeric             | file permission mask that triggered a watch event   |                                                 |
| permissive              | numeric             | SELinux is in permissive mode                       |                                                 |
| pfs                     | alphanumeric        | perfect forward secrecy method                      |                                                 |
| pid                     | numeric             | process ID                                          |                                                 |
| ppid                    | numeric             | parent process ID                                   |                                                 |
| printer                 | alphanumeric        | printer name                                        |                                                 |
| prom                    | numeric             | network promiscuity flag                            |                                                 |
| proctitle               | encoded             | process title and command line parameters           |                                                 |
| proto                   | numeric             | network protocol                                    |                                                 |
| qbytes                  | numeric             | ipc objects quantity of bytes                       |                                                 |
| range                   | alphanumeric        | user's SE Linux range                               |                                                 |
| rdev                    | numeric             | the device identifier (special files only)          |                                                 |
| reason                  | alphanumeric        | text string denoting a reason for the action        |                                                 |
| removed                 | numeric             | number of deleted files                             |                                                 |
| res                     | alphanumeric        | result of the audited operation(success/fail)       |                                                 |
| resrc                   | alphanumeric        | resource being assigned                             |                                                 |
| result                  | alphanumeric        | result of the audited operation(success/fail)       |                                                 |
| role                    | alphanumeric        | user's SELinux role                                 |                                                 |
| rport                   | numeric             | remote port number                                  |                                                 |
| saddr                   | encoded             | struct socket address structure                     |                                                 |
| sauid                   | numeric             | sent login user ID                                  |                                                 |
| scontext                | alphanumeric        | the subject's context string                        |                                                 |
| selected-context        | alphanumeric        | new MAC context assigned to session                 |                                                 |
| seperm                  | alphanumeric        | SELinux permission being decided on                 |                                                 |
| seqno                   | numeric             | sequence number                                     |                                                 |
| seperms                 | alphabet            | SELinux permissions being used                      |                                                 |
| seresult                | alphabet            | SELinux AVC decision granted/denied                 |                                                 |
| ses                     | numeric             | login session ID                                    |                                                 |
| seuser                  | alphanumeric        | user's SE Linux user acct                           |                                                 |
| sgid                    | numeric             | set group ID                                        |                                                 |
| sig                     | numeric             | signal number                                       |                                                 |
| sigev_signo             | numeric             | signal number                                       |                                                 |
| smac                    | numeric             | local MAC address                                   |                                                 |
| spid                    | numeric             | sent process ID                                     |                                                 |
| sport                   | numeric             | local port number                                   |                                                 |
| state                   | alphanumeric        | audit daemon configuration resulting state          |                                                 |
| subj                    | alphanumeric        | lspp subject's context string                       |                                                 |
| success                 | alphanumeric        | whether the syscall was successful or not           |                                                 |
| suid                    | numeric             | sent user ID                                        |                                                 |
| syscall                 | numeric             | syscall number in effect when the event occurred    |                                                 |
| table                   | alphanumeric        | netfilter table name                                |                                                 |
| tclass                  | alphanumeric        | target's object classification                      |                                                 |
| tcontext                | alphanumeric        | the target's or object's context string             |                                                 |
| terminal                | alphanumeric        | terminal name the user is running programs on       |                                                 |
| tty                     | alphanumeric        | tty udevice the user is running programs on         |                                                 |
| type                    | alphanumeric        | the audit record's type                             |                                                 |
| uid                     | numeric             | user ID                                             |                                                 |
| unit                    | alphanumeric        | systemd unit                                        |                                                 |
| uri                     | alphanumeric        | URI pointing to a printer                           |                                                 |
| user                    | alphanumeric        | account submitted for authentication                |                                                 |
| uuid                    | alphanumeric        | a UUID                                              |                                                 |
| val                     | alphanumeric        | generic value associated with the operation         |                                                 |
| ver                     | numeric             | audit daemon's version number                       |                                                 |
| virt                    | alphanumeric        | kind of virtualization being referenced             |                                                 |
| vm                      | encoded             | virtual machine name                                |                                                 |
| vm-ctx                  | alphanumeric        | the vm's context string                             |                                                 |
| vm-pid                  | numeric             | vm's process ID                                     |                                                 |
| watch                   | encoded             | file name in a watch record                         |                                                 |


