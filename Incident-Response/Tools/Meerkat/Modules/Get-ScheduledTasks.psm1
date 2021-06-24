function Get-ScheduledTasks {
    <#
    .SYNOPSIS 
        Gets scheduled tasks.

    .DESCRIPTION 
        Gets scheduled tasks.

        Alternative: schtasks.exe

    .EXAMPLE 
        Get-ScheduledTasks

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-ScheduledTasks} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\ScheduledTasks.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-ScheduledTasks} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_ScheduledTasks.csv")
        }

    .NOTES 
        Updated: 2019-04-04

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
       https://github.com/TonyPhipps/Meerkat/wiki/ScheduledTasks
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-ScheduledTasks at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
        
        $ScheduledTaskArray = Get-ScheduledTask
       
        $ResultsArray = foreach($ScheduledTask in $ScheduledTaskArray) {

            $output = $null
            $output = [PSCustomObject]@{
                
                Host = $env:COMPUTERNAME
                DateScanned = $DateScanned
                
                Author = $ScheduledTask.Author
                Description = $ScheduledTask.Description
                SecurityDescriptor = $ScheduledTask.SecurityDescriptor
                Source = $ScheduledTask.Source
                State = $ScheduledTask.State
                TaskName = $ScheduledTask.TaskName
                TaskPath = $ScheduledTask.TaskPath
                URI = $ScheduledTask.URI

                ActionsArguments = ($ScheduledTask.Actions.Arguments -join " ")
                ActionsExecute = ($ScheduledTask.Actions.Execute -join " ")
                ActionsId = ($ScheduledTask.Actions.Id -join " ")
                ActionsWorkingDirectory = ($ScheduledTask.Actions.WorkingDirectory -join " ")
                
                TriggersId = ($ScheduledTask.Triggers.Id -join " ")
                TriggersDelay = ($ScheduledTask.Triggers.Delay -join " ")
                TriggersEnabled = ($ScheduledTask.Triggers.Enabled -join " ")
                TriggersEndBoundary = ($ScheduledTask.Triggers.EndBoundary -join " ")
                TriggersExecutionTimeLimit = ($ScheduledTask.Triggers.ExecutionTimeLimit -join " ")
                TriggersRepetitionDuration = ($ScheduledTask.Triggers.Repetition.Duration -join " ")
                TriggersRepetitionInterval = ($ScheduledTask.Triggers.Repetition.Interval -join " ")
                TriggersStartBoundary = ($ScheduledTask.Triggers.StartBoundary -join " ")
            }

            $output
        }
        
        return $ResultsArray | Select-Object Host, DateScanned, Author, Description, SecurityDescriptor, Source, State, TaskName, TaskPath, URI, 
        ActionsArguments, ActionsExecute, ActionsId, ActionsWorkingDirectory, 
        TriggersId, TriggersDelay, TriggersEnabled, TriggersEndBoundary, TriggersExecutionTimeLimit, TriggersRepetitionDuration, 
        TriggersRepetitionInterval, TriggersStartBoundary
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}