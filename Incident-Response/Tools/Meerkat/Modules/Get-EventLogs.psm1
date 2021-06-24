function Get-EventLogs {
    <#
    .SYNOPSIS
        Gets all event logs within the specified time frame. Defaults to now and the last 2 hours.

    .DESCRIPTION
        Gets all event logs within the specified time frame. Defaults to now and the last 2 hours.

    .PARAMETER StartTime
        Specify when to begin event log collection. Defaults to 2 hours ago based on system time.
        
    .PARAMETER EndTime
        Specify when to end event log collection. Defaults to current time on system time.

    .EXAMPLE 
        Get-EventLogs

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-EventLogs} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\EventLogs.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-EventLogs} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_EventLogs.csv")
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
       https://github.com/TonyPhipps/Meerkat/wiki/EventLogs
    #>

    [CmdletBinding()]
    param(
        [Parameter()]
        [datetime] $StartTime,

        [Parameter()]
        [datetime] $EndTime
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-EventLogs at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()

        if(!($StartTime)){
            $StartTime = (Get-Date) - (New-TimeSpan -Hours 2)
        }

        if(!($EndTime)){
            $EndTime = (Get-Date)
        }
    }

    process{

            $Logs = Get-WinEvent -ListLog * | Where-Object { ($_.RecordCount -gt 0) }

            $ResultsArray = Foreach ($Log in $Logs){

                Get-WinEvent -FilterHashTable @{ LogName=$Log.LogName; StartTime=$StartTime; EndTime=$EndTime } -ErrorAction SilentlyContinue
            }

            foreach ($Result in $ResultsArray) {
                $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
                $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
            }

            return $ResultsArray | Select-Object Host, DateScanned, TimeCreated, MachineName, UserId, 
            ProcessId, LogName, ProviderName, LevelDisplayName, Id, OpcodeDisplayName, TaskDisplayName, 
            Message, RecordId, RelatedActivityId, ThreadId, Version
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}