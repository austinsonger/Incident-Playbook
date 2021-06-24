function Get-RegistryPersistence {
    <#
    .SYNOPSIS 
        Gets a list of registry keys that may be used to achieve persistence or clear tracks.

    .DESCRIPTION 
        Gets a list of registry keys that may be used to achieve persistence or clear tracks.

    .EXAMPLE 
        Get-RegistryPersistence

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-RegistryPersistence} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\RegistryPersistence.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-RegistryPersistence} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_RegistryPersistence.csv")
        }

    .NOTES 
        Updated: 2019-04-08

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
       https://github.com/TonyPhipps/Meerkat/wiki/RegistryPersistence
       https://blog.cylance.com/windows-registry-persistence-part-2-the-run-keys-and-search-order
       http://resources.infosecinstitute.com/common-malware-persistence-mechanisms
       https://andreafortuna.org/cybersecurity/windows-registry-in-forensic-analysis
       https://github.com/redcanaryco/atomic-red-team
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-RegistryPersistence at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
    
        $KeysValues = 
            "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\BootExecute",
            "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\KnownDLLs",
            "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\SafeDllSearchMode",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunServices",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServices",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnce",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnceEx",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\RunOnceEx",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Run",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SharedTaskScheduler",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run32",            
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\StartupFolder",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Browser Helper Objects",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\ShellServiceObjectDelayLoad",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor",
            "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Winlogon",
            "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\Windows\AppInit_DLLs",
            "HKEY_LOCAL_MACHINE\Software\Microsoft\Windows NT\CurrentVersion\IniFileMapping\system.ini\boot\Shell",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\osk.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\sethc.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\utilman.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\magnify.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\narrator.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\DisplaySwitch.exe",
            "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Image File Execution Options\AtBroker.exe"

        $UserKeysValues =
            "\Software\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            "\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\RunServicesOnce",
            "\Software\Microsoft\Windows\CurrentVersion\RunServices",
            "\Software\Microsoft\Windows\CurrentVersion\Run",
            "\Software\Microsoft\Windows\CurrentVersion\RunOnce",
            "\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\Run32",            
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\StartupApproved\StartupFolder",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders",
            "\Software\Microsoft\Windows NT\CurrentVersion\Windows",
            "\Software\Microsoft\Command Processor",
            "\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Control Panel\CPLs",
            "\Software\Microsoft\Windows\CurrentVersion\Control Panel\CPLs"

        $DataArray = foreach ($KeyValue in $KeysValues){
            
            $Key = "Registry::" + $KeyValue
        
            if (Test-Path $Key){ # A Key was given
                $keyObject = Get-Item $Key               
                $Properties = $keyObject.Property

                foreach ($Property in $Properties){
    
                    $output = [pscustomobject] @{
                        Key = $Key.Split(":")[2]
                        Value = $Property 
                        Data = $keyObject.GetValue($Property)
                    }

                    if ($output.data -is [array]){
                        if ($output.data[0] -is [byte]){
                            $output.Data = (($output.Data | ForEach-Object{[char]$_}) -join "")
                        }
                        else{
                            $output.Data = [string]$output.Data
                        }
                    }

                    $output
                }
            }

            else{ # A key and value was given
                $Key = Split-Path -Path $Key
                $hasData = (Get-Item $Key -ErrorAction SilentlyContinue)
                    
                    if ($hasData) {

                    $output = [pscustomobject] @{
                        Key = $Key.Split(":")[2]
                        Value = $value 
                        Data = (Get-Item $Key).GetValue($value)
                    }

                    if ($output.data -is [array]){
                        if ($output.data[0] -is [byte]){
                            $output.Data = (($output.Data | ForEach-Object{[char]$_}) -join "")
                        }
                        else{
                            $output.Data = [string]$output.Data
                        }
                    }
                    
                    $output
                }
            }
        }


        # Regex pattern for SIDs
        $PatternSID = 'S-1-5-21-\d+-\d+\-\d+\-\d+$'
        
        # Get all users' Username, SID, and location of ntuser.dat
        $UserArray = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\*' | 
            Where-Object {$_.PSChildName -match $PatternSID} | 
            Select-Object  @{name="SID";expression={$_.PSChildName}}, 
                @{name="UserHive";expression={"$($_.ProfileImagePath)\ntuser.dat"}}, 
                @{name="Username";expression={$_.ProfileImagePath -replace '^(.*[\\\/])', ''}}
        
        $LoadedHives = Get-ChildItem Registry::HKEY_USERS | 
            Where-Object {$_.PSChildname -match $PatternSID} | 
            Select-Object @{name="SID";expression={$_.PSChildName}}
        
        $UnloadedHives = Compare-Object $UserArray.SID $LoadedHives.SID | 
            Select-Object @{name="SID";expression={$_.InputObject}}, UserHive, Username

        $UserDataArray = foreach ($User in $UserArray) {
            
            If ($User.SID -in $UnloadedHives.SID) {

                reg load HKU\$($User.SID) $($User.UserHive) | Out-Null
            }

            foreach ($Key in $UserKeysValues){

                $Key = "Registry::HKEY_USERS\$($User.SID)" + $Key

                if (Test-Path $Key){

                    $KeyObject = Get-Item $Key
                            
                    $Properties = $KeyObject.Property
                            
                    if ($Properties) { 
                            
                        foreach ($Property in $Properties){
                            
                            $output = [pscustomobject] @{
                                Key = $Key.Split(":")[2]
                                Value = $Property 
                                Data = $KeyObject.GetValue($Property)
                            }

                            if ($output.data -is [array]){
                                if ($output.data[0] -is [byte]){
                                    $output.Data = (($output.Data | ForEach-Object{[char]$_}) -join "")
                                }
                                else{
                                    $output.Data = [string]$output.Data
                                }
                            }

                            $output
                        }  
                    }
                }
            }
            
            If ($User.SID -in $UnloadedHives.SID) {
                ### Garbage collection and closing of ntuser.dat ###

                [gc]::Collect()
                reg unload HKU\$($User.SID) | Out-Null
            }
        }
        
        
        $ResultsArray = $DataArray + $UserDataArray

        foreach ($Result in $ResultsArray) {
        
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }  

        return $ResultsArray | Select-Object Host, DateScanned, Key, Value, Data
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}