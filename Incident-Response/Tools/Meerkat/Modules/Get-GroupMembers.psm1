function Get-GroupMembers {
    <#
    .SYNOPSIS 
        Gets a list of the members of each local group.

    .DESCRIPTION 
        Gets a list of the members of each local group.

        Alternative: net.exe user
        Alternative: net.exe localgroup
        Alternative: net.exe localgroup administrators

    .EXAMPLE 
        Get-GroupMembers

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-GroupMembers} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\GroupMembers.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-GroupMembers} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_GroupMembers.csv")
        }

    .NOTES 
        Updated: 2019-03-28

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
       https://github.com/TonyPhipps/Meerkat/wiki/GroupMembers
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-GroupMembers at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{

        $GroupArray = Get-LocalGroup
            
        $ResultsArray = Foreach ($Group in $GroupArray) { # get members of each group
            
            $MemberArray = Get-LocalGroupMember -Group $Group.Name
            
            Foreach ($Member in $MemberArray) { # add group properties to each member
        
                $Member | Add-Member -MemberType NoteProperty -Name "UserDomain" -Value $Member.Name.Split("\")[0]
                $Member | Add-Member -MemberType NoteProperty -Name "UserName" -Value $Member.Name.Split("\")[1]
                $Member | Add-Member -MemberType NoteProperty -Name "GroupDescription" -Value $Group.DESCRIPTION
                $Member | Add-Member -MemberType NoteProperty -Name "GroupName" -Value $Group.Name
                $Member | Add-Member -MemberType NoteProperty -Name "GroupSID" -Value $Group.SID
                $Member | Add-Member -MemberType NoteProperty -Name "GroupPrincipalSource" -Value $Group.PrincipalSource
                $Member | Add-Member -MemberType NoteProperty -Name "GroupObjectClass" -Value $Group.ObjectClass
                
                $Member
            }
        }

        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }

        return $ResultsArray | Select-Object Host, DateScanned, UserDomain, UserName, SID, PrincipalSource, 
        ObjectClass, GroupName, GroupDescription, GroupSID, GroupPrincipalSource, GroupObjectClass

    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}