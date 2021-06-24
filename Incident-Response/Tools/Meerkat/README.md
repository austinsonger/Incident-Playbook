# Meerkat
![Meerkat Logo](https://i.imgur.com/7gHUYBh.png)


Meerkat is collection of PowerShell modules designed for artifact gathering and reconnaisance of Windows-based endpoints without requiring a pre-deployed agent. Use cases include incident response triage, threat hunting, baseline monitoring, snapshot comparisons, and more.

# Artifacts and Wiki Articles
|       [Host Info](https://github.com/TonyPhipps/Meerkat/wiki/Computer)       | [Processes](https://github.com/TonyPhipps/Meerkat/wiki/Processes)* |      [Services](https://github.com/TonyPhipps/Meerkat/wiki/Services)      |   [Autoruns](https://github.com/TonyPhipps/Meerkat/wiki/Autoruns)    |      [Drivers](https://github.com/TonyPhipps/Meerkat/wiki/Drivers)      |
| :--------------------------------------------------------------------------: | :----------------------------------------------------------------: | :-----------------------------------------------------------------------: | :------------------------------------------------------------------: | :---------------------------------------------------------------------: |
|                                     ARP                                      |      [DLLs](https://github.com/TonyPhipps/Meerkat/wiki/DLLs)*      |                                  EnvVars                                  |                              Hosts File                              |                                   ADS                                   |
|            [DNS](https://github.com/TonyPhipps/Meerkat/wiki/DNS)             |                              Strings*                              | [Users & Groups](https://github.com/TonyPhipps/Meerkat/wiki/GroupMembers) |      [Ports](https://github.com/TonyPhipps/Meerkat/wiki/Ports)       | [Select Registry](https://github.com/TonyPhipps/Meerkat/wiki/Registry)  |
|                                   Hotfixes                                   |                              Handles*                              |                                  Software                                  |                               Hardware                               |   [Event Logs](https://github.com/TonyPhipps/Meerkat/wiki/EventLogs)    |
|                                 Net Adapters                                 |                             Net Routes                             |                                 Sessions                                  |                               [Shares]                               | [Certificates](https://github.com/TonyPhipps/Meerkat/wiki/Certificates) |
| [Scheduled Tasks](https://github.com/TonyPhipps/Meerkat/wiki/ScheduledTasks) |                                TPM                                 |                                 Bitlocker                                 | [Recycle Bin](https://github.com/TonyPhipps/Meerkat/wiki/RecycleBin) |        [Files](https://github.com/TonyPhipps/Meerkat/wiki/Files)        |

* Ingest using your SIEM of choice (_Check out the [SIEM](https://github.com/TonyPhipps/SIEM) Repository!_)
______________________________________________________

## Index

  * [Quick Start](#Quick-Start)
  * [Usage](#Usage)
  * [Analysis](#Analysis)
  * [Troubleshooting](#Troubleshooting)
  * [Screenshots](#Screenshots)
  * [Similar Projects](#Similar-Projects)
  
______________________________________________________

## Quick Start

### Requirements

* Requires Powershell 5.0 or above on the "scanning" device.
* Requires Powershell 3.0 or higher on target systems. You can make this further backward compatible to PowerShell 2.0 by replacing instances of "Get-CIMinstance" with "Get-WMIObject"
* Requires [WinRM access](https://github.com/TonyPhipps/Powershell/blob/master/Enable-WinRM.ps1).

### Install with [Git](https://gitforwindows.org/)

In a Command or PowerShell console, type the following...

```
git clone "https://github.com/TonyPhipps/Meerkat" "C:\Program Files\WindowsPowerShell\Modules\Meerkat"
```

To update...

```
cd C:\Program Files\WindowsPowerShell\Modules\Meerkat
git pull
```

### Install with PowerShell

Copy/paste this into a PowerShell console

```
$Modules = "C:\Program Files\WindowsPowerShell\Modules\"
New-Item -ItemType Directory $Modules\Meerkat\ -force
Invoke-WebRequest https://github.com/TonyPhipps/Meerkat/archive/master.zip -OutFile $Modules\master.zip
Expand-Archive $Modules\master.zip -DestinationPath $Modules
Copy-Item $Modules\Meerkat-master\* $Modules\Meerkat\ -Force -Recurse
Remove-Item  $Modules\Meerkat-master -Recurse -Force
```

To update, simply run the same block of commands again.

Functions can also be used by opening the .psm1 file and copy-pasting its entire contents into a PowerSell console.

## Run Meerkat

This command will output results to C:\Users\YourName\Meerkat\

```
Invoke-Meerkat
```

## Analysis

Analysis methodologies and techniques are provided in the [Wiki pages](https://github.com/TonyPhipps/Meerkat/wiki).

## Troubleshooting
[Installing a Powershell Module](https://msdn.microsoft.com/en-us/library/dd878350(v=vs.85).aspx)

If your system does not automatically load modules in your user [profile](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-6), you may need to [import the module manually](https://msdn.microsoft.com/en-us/library/dd878284(v=vs.85).aspx).

```
Import-Module C:\Program Files\WindowsPowerShell\Modules\Meerkat\Meerkat.psm1
```

## Screenshots

Output of Command "Invoke-Meerkat"

![Output of Command "Invoke-Meerkat"](https://i.imgur.com/C5eKInZ.png)

Output Files

![Output Files](https://i.imgur.com/dy3f1Id.png)


## Similar Projects

- https://github.com/travisfoley/dfirtriage
- https://github.com/Invoke-IR/PowerForensics
- https://github.com/PowerShellMafia/CimSweep
- https://www.crowdstrike.com/resources/community-tools/crowdresponse/
- https://github.com/gfoss/PSRecon/
- https://github.com/n3l5/irCRpull
- https://github.com/davehull/Kansa/
- https://github.com/WiredPulse/PoSh-R2
- https://github.com/google/grr
- https://github.com/diogo-fernan/ir-rescue
- https://github.com/SekoiaLab/Fastir_Collector
- https://github.com/AlmCo/Panorama
- https://github.com/certsocietegenerale/FIR
- https://github.com/securycore/Get-Baseline
- https://github.com/Infocyte/PSHunt
- https://github.com/giMini/NOAH
- https://github.com/A-mIn3/WINspect
- https://learn.duffandphelps.com/kape
- https://www.brimorlabs.com/tools/

What makes Meerkat stand out?
- Lightweight. Fits on a floppy disk!
- Very little footprint/impact on targets.
- Leverages Powershell & WMI/CIM.
- Coding style encourages proper code review, learning, and "borrowing."
- No DLLs or compiled components.
- Standardized output - defaults to .csv, and can easily support json, xml, etc.
