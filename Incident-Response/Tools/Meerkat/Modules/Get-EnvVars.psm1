Function Get-EnvVars {
    <#
    .SYNOPSIS 
        Retreives the values of all environment variables from the system.
    
    .DESCRIPTION
        Retreives the values of all environment variables from the system.
    
    .EXAMPLE 
        Get-EnvVars

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-EnvVars} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\EnvVars.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-EnvVars} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_EnvVars.csv")
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
    #>


    [cmdletbinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-EnvVars at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()          
    }

    process{

        $Win32_Environment = Get-CimInstance -Class Win32_Environment 
        
        if ($Win32_Environment) {

            $ResultsArray = ForEach ($Variable in $Win32_Environment) {

                $VariableValues = $Variable.VariableValue.Split(";") | Where-Object {$_ -ne ""}
            
                Foreach ($VariableValue in $VariableValues) {
                    $VariableValueSplit = $Variable
                    $VariableValueSplit.VariableValue = $VariableValue
                
                    $output = $null
                    $output = [PSCustomObject]@{
                        UserName = $VariableValueSplit.UserName
                        VariableName = $VariableValueSplit.Name
                        VariableValue = $VariableValueSplit.VariableValue  
                    }

                    $output
                }
            }
        }

        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }

        return $ResultsArray | Select-Object Host, DateScanned, UserName, VariableName, VariableValue
    }

    end{
        
        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}