Function Get-ComputerDetails {
    <#
    .SYNOPSIS
        Gets general system information.

    .DESCRIPTION
        Gets general system information. Includes data from 
        Win32_ComputerSystem, Win32_OperatingSystem, and win32_BIOS.

    .EXAMPLE 
        Get-ComputerDetails

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-Computer} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\Computer.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-ComputerDetails} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_Computer.csv")
        }

    .NOTES
        Updated: 2019-03-27

        Contributing Authors:
            Anthony Phipps
            
        LEGAL: Copyright (C) 2019
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
    
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.

    .LINK
       https://github.com/TonyPhipps/Meerkat
       https://github.com/TonyPhipps/Meerkat/wiki/Computer
       
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-ComputerDetails at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{

            $Win32_OperatingSystem = Get-CIMinstance -class Win32_OperatingSystem
            $Win32_ComputerSystem = Get-CimInstance -class Win32_ComputerSystem
            $Win32_BIOS = Get-CIMinstance -class Win32_BIOS
            $Win32_Processor = Get-CIMinstance -class Win32_Processor

            $Computer = New-Object -TypeName PSObject

            foreach ($Property in $Win32_OperatingSystem.PSObject.Properties) {
                $Computer | Add-Member -MemberType NoteProperty -Name $Property.Name -Value $Property.value -ErrorAction SilentlyContinue
            }            

            foreach ($Property in $Win32_ComputerSystem.PSObject.Properties) {
                $Computer | Add-Member -MemberType NoteProperty -Name $Property.Name -Value $Property.value -ErrorAction SilentlyContinue
            }
                
            foreach ($Property in $Win32_Processor.PSObject.Properties) {
                $Computer | Add-Member -MemberType NoteProperty -Name $Property.Name -Value $Property.value -ErrorAction SilentlyContinue
            }

            foreach ($Property in $Win32_BIOS.PSObject.Properties) {
                $Computer | Add-Member -MemberType NoteProperty -Name $Property.Name -Value $Property.value -ErrorAction SilentlyContinue
            }

            $Computer | Add-Member -MemberType NoteProperty -Name BIOSInstallDate -Value $Win32_BIOS.InstallDate -ErrorAction SilentlyContinue # Resolves InstallDate conflict with Win32_OperatingSystem

            $Computer | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Computer | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned

            return $Computer | Select-Object Host, DateScanned, BootDevice, BuildNumber, Caption,
            CurrentTimeZone, DataExecutionPrevention_32BitApplications, DataExecutionPrevention_Available,
            DataExecutionPrevention_Drivers, DataExecutionPrevention_SupportPolicy, Debug, Description, Distributed,
            EncryptionLevel, InstallDate, LastBootUpTime, LocalDateTime, MUILanguages, OSArchitecture, OSProductSuite, 
            OSType, OperatingSystemSKU, Organization, OtherTypeDescription, PortableOperatingSystem, ProductType, 
            RegisteredUser, ServicePackMajorVersion, ServicePackMinorVersion, Status, SuiteMask, SystemDevice, 
            SystemDirectory, SystemDrive, Version, WindowsDirectory, AdminPasswordStatus, BootROMSupported, BootupState, 
            ChassisBootupState, DNSHostName, DaylightInEffect, Domain, DomainRole, EnableDaylightSavingsTime, 
            HypervisorPresent, Manufacturer, Model, NetworkServerModeEnabled, PrimaryOwnerContact, PrimaryOwnerName, 
            SupportContactDescription, SystemSKUNumber, ThermalState, UserName, BIOSVersion, BIOSInstallDate, 
            BIOSManufacturer, PrimaryBIOS, BIOSReleaseDate, SMBIOSBIOSVersion, SMBIOSMajorVersion, SMBIOSMinorVersion, 
            SMBIOSPresent, SerialNumber, SystemBiosMajorVersion, SystemBiosMinorVersion, VirtualizationFirmwareEnabled
    }

    end{
        
        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}