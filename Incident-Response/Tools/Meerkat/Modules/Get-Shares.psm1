function Get-Shares {
    <#
    .SYNOPSIS 
        Gets all shares.

    .DESCRIPTION 
        Gets all shares.

    .EXAMPLE 
        Get-Shares

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-Shares} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\Shares.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-Shares} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_Shares.csv")
        }

    .NOTES 
        Updated: 2019-04-05

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
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-Shares at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{

        $PermissionFlags = @{
            0x1     =     "Read-List"
            0x2     =     "Write-Create"
            0x4     =     "Append-Create Subdirectory"                      
            0x20    =     "Execute file-Traverse directory"
            0x40    =     "Delete child"
            0x10000 =     "Delete"                     
            0x40000 =     "Write access to DACL"
            0x80000 =     "Write Owner"
        }

        $SharesArray = Get-WmiObject -class Win32_share -Filter "type=0"

        if ($SharesArray) {
            
            $ResultsArray = foreach ($Share in $SharesArray) {

                $ShareName = $Share.Name

                $ShareSettings = Get-WmiObject -class Win32_LogicalShareSecuritySetting  -Filter "Name='$ShareName'"

                $DACLArray = $ShareSettings.GetSecurityDescriptor().Descriptor.DACL

                foreach ($DACL in $DACLArray) {

                    $TrusteeName = $DACL.Trustee.Name
                    $TrusteeDomain = $DACL.Trustee.Domain
                    $TrusteeSID = $DACL.Trustee.SIDString

                    # 1 Deny 0 Allow
                    if ($DACL.AceType) 
                        { $Type = "Deny" }
                    else 
                        { $Type = "Allow" }
        
                    $SharePermission = foreach ($Key in $PermissionFlags.Keys) { # Convert AccessMask to human-readable format

                        if ($Key -band $DACL.AccessMask) {
                                        
                            $PermissionFlags[$Key] + ";"
                        }
                    }

                    $output = New-Object -TypeName PSObject
                    
                    $output | Add-Member -MemberType NoteProperty -Name Computer -Value $Share.PSComputerName
                    $output | Add-Member -MemberType NoteProperty -Name Name -Value $Share.Name
                    $output | Add-Member -MemberType NoteProperty -Name Path -Value $Share.Path
                    $output | Add-Member -MemberType NoteProperty -Name DESCRIPTION -Value $Share.DESCRIPTION
                    $output | Add-Member -MemberType NoteProperty -Name TrusteeName -Value $TrusteeName
                    $output | Add-Member -MemberType NoteProperty -Name TrusteeDomain -Value $TrusteeDomain
                    $output | Add-Member -MemberType NoteProperty -Name TrusteeSID -Value $TrusteeSID
                    $output | Add-Member -MemberType NoteProperty -Name AccessType -Value $Type
                    $output | Add-Member -MemberType NoteProperty -Name AccessMask -Value $DACL.AccessMask
                    $output | Add-Member -MemberType NoteProperty -Name SharePermissions -Value $SharePermission

                    $output
                }
            } 

            foreach ($Result in $ResultsArray) {

                $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
                $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
            }

            return $ResultsArray | Select-Object Host, DateScanned, Name, Path, Description, TrusteeName, 
            TrusteeDomain, TrusteeSID, Type, AccessMask, SharePermission
        }
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}