function Get-Autoruns {
    <#
    .SYNOPSIS 
        Gets a list of programs that auto start.

    .DESCRIPTION 
        Gets a list of programs that auto start.

        Alternative: Sysinternals autoruns.exe
        Alternative: wmic.exe startup list full

    .EXAMPLE 
        Get-Autoruns

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-Autoruns} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\Autoruns.csv")

    .EXAMPLE 
        Get-Autoruns SomeHostName.domain.com
        Get-Content C:\hosts.csv | Get-Autoruns
        Get-Autoruns -Computer $env:computername
        Get-ADComputer -filter * | Select -ExpandProperty Name | Get-Autoruns

    .NOTES
        Updated: 2019-03-27

        Contributing Authors:
            Jeremy Arnold
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
        Write-Information -InformationAction Continue -MessageData ("Started Get-Autoruns at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
        
        $ResultsArray = Get-CimInstance Win32_StartupCommand -ErrorAction SilentlyContinue

        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }

        return $ResultsArray | Select-Object Host, DateScanned, Name, Caption, Command, Location, User, UserSID
    }

    end{
        
        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}