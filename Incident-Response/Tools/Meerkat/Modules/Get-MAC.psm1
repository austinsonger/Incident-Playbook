function Get-MAC {
    <#
    .SYNOPSIS 
        Records Modified, Accessed, and Created (MAC) times on files.

    .DESCRIPTION 
        Records Modified, Accessed, and Created (MAC) times on files. Use the -Path command to 
        provide a directory to recursively record MAC times.

    .PARAMETER Path  
        Specify a path to begin recursive recording of MAC times (Defaults to "$ENV:SystemDrive\Users")

    .PARAMETER Hash
        Include file hashes. Will increase scan time significantly.

    .EXAMPLE 
        Get-MAC

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-MAC} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\MAC.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-MAC} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_MAC.csv")
        }

    .NOTES 
        Updated: 2019-04-02

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
        [Parameter(ValueFromPipeline = $True, ValueFromPipelineByPropertyName = $True)]
        $Path, # Will default to "$ENV:SystemDrive\Users"

        [Parameter()]
        [switch] $Hash
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-MAC at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
        
        if (!$Path) {

            $Path = "$ENV:SystemDrive\Users"

        } else {

            $Path = $Path
        }

        $ResultsArray = Get-ChildItem -Path $Path -File -Recurse | 
            Select-Object FullName, Mode, Length, Hash, LastWriteTimeUtc, LastAccessTimeUtc, CreationTimeUtc

        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned

            if ($Hash){

                Write-Verbose ("Hashing: {0}" -f $Result.FullName)
                $Result.Hash = (Get-FileHash -Path $Result.FullName -ErrorAction SilentlyContinue).Hash
            }
        }

        return $ResultsArray | Select-Object Host, DateScanned, FullName, Mode, Length, Hash, LastWriteTimeUTC, LastAccessTimeUTC, creationTimeUtc
        
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}