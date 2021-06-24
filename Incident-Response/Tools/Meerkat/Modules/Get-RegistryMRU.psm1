function Get-RegistryMRU {
    <#
    .SYNOPSIS 
        Gets a Most Recently Used information from various locations.

    .DESCRIPTION 
        Gets a Most Recently Used information from various locations.

    .EXAMPLE 
        Get-RegistryMRU

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-RegistryMRU} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\RegistryMRU.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-RegistryMRU} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_RegistryMRU.csv")
        }

    .NOTES 
        Updated: 2019-04-03

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
       https://andreafortuna.org/cybersecurity/windows-registry-in-forensic-analysis/
       https://gbhackers.com/windows-registry-analysis-tracking-everything-you-do-on-the-system/

    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-RegistryMRU at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
            
        $UserKeys =
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaveMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\LastVisitedPidlMRULegacy",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\CIDSizeMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs",
            "\Software\Microsoft\Currentversion\Search\RecentApps",
            "\Software\Microsoft\Internet Explorer\TypedURLs",
            "\Software\Microsoft\Microsoft Management Console\Recent File List",
            "\Software\Microsoft\Office\*\Access\User MRU\*\File MRU",
            "\Software\Microsoft\Office\*\Excel\User MRU\*\File MRU",
            "\Software\Microsoft\Office\*\OneNote\User MRU\*\File MRU",
            "\Software\Microsoft\Office\*\Powerpoint\User MRU\*\File MRU",
            "\Software\Microsoft\Office\*\Visio\User MRU\*\File MRU",
            "\Software\Microsoft\Office\*\Word\User MRU\*\File MRU",
            "\Software\Microsoft\Search Assistant\ACMru",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\FindComputerMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\Map Network Drive MRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\PrnPortsMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths",
            "\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist",
            "\Software\Microsoft\Windows\CurrentVersion\Applets\Wordpad\Recent File List"

        # Regex pattern for SIDs
        $PatternSID = 'S-1-5-21-\d+-\d+\-\d+\-\d+$'
        
        # Get all users' Username, SID, and location of ntuser.dat
        $UserArray = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList\*' | 
            Where-Object {$_.PSChildName -match $PatternSID} | 
            Select-Object  @{name="SID";expression={$_.PSChildName}}, 
                @{name="UserHive"; expression={"$($_.ProfileImagePath)\ntuser.dat"}}, 
                @{name="Username"; expression={$_.ProfileImagePath -replace '^(.*[\\\/])', ''}}
        
        $LoadedHives = Get-ChildItem Registry::HKEY_USERS | 
            Where-Object {$_.PSChildname -match $PatternSID} | 
            Select-Object @{name="SID"; expression={$_.PSChildName}}
        
        $UnloadedHives = Compare-Object $UserArray.SID $LoadedHives.SID | 
            Select-Object @{name="SID"; expression={$_.InputObject}}, UserHive, Username

        $UserKeysArray = foreach ($User in $UserArray) {
            
            If ($User.SID -in $UnloadedHives.SID) {

                reg load HKU\$($User.SID) $($User.UserHive) | Out-Null
            }

            foreach ($Key in $UserKeys){

                $Key = "Registry::HKEY_USERS\$($User.SID)" + $Key

                if (Test-Path $Key){

                    $KeyObject = Get-Item $Key   
                    $Properties = $KeyObject.Property
                            
                    if ($Properties) { 
                            
                        foreach ($Property in $Properties){
                            
                            $ThisKey = $Key.Split(":")[2]
                            $ThisValue = $Property
                            
                            try{
                                
                                $ThisData = $KeyObject.GetValue($Property)
                                $ThisDataType = $ThisData.GetType()
                            }
                            catch{ # Necessary due to how some registry keys are structured differently
                                
                                $ThisData = (Get-ItemProperty $Key)."$Property"
                                $ThisDataType = $ThisData.GetType()
                            }

                            # If Shellbag, convert to ASCII
                            if ($ThisDataType.Name -eq "byte[]" -and $ThisValue -match "[0-9]+") {
                                
                                # Read in the data as decimals
                                $decimal = $KeyObject.GetValue($Property)

                                $hexArray = @()
    
                                # To determine file name only, read each byte until null is hit
                                for($j = 0; $j -lt $decimal.length; $j+=2) {
        
                                    # Break at the first null character
                                    if($decimal[$j + 1] -eq 0 -and $decimal[$j] -eq 0) { break }
                                    # Retrieve a byte and add it to the hex array
                                    $tempstring = "{0:x2}" -f $decimal[$j + 1]
                                    $tempstring += "{0:x2}" -f $decimal[$j]
                                    $hexArray += $tempstring
                                } 
    
                                $asciiArray = $hexArray | ForEach-Object { [CHAR][BYTE]([CONVERT]::toint32($_,16)) }
                                $ThisData = $asciiArray -join ""     
                            }
                            
                            $output = [pscustomobject] @{
                                Key = $ThisKey
                                Value = $ThisValue
                                Data = $ThisData
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
        
        $ResultsArray = $MachineKeysArray + $MachineValuesArray + $UserKeysArray

        foreach ($Result in $ResultsArray) {
            
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }        

        return $ResultsArray | Where-Object {$_.Data -ne ""} | Select-Object Host, DateScanned, Key, Value, Data
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}