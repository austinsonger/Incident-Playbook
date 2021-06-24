function Get-Certificates {
    <#
    .SYNOPSIS 
        Gets a list of trusted certificates at the system level.

    .DESCRIPTION 
        Gets a list of trusted certificates at the system level.

    .EXAMPLE 
        Get-Certificates

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-Certificates} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\Certificates.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-Certificates} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_Certificates.csv")
        }

    .NOTES
        Updated: 2019-03-23

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
        Write-Information -InformationAction Continue -MessageData ("Started Get-Certificates at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{
        
        $ResultsArray = Get-ChildItem Cert:\LocalMachine\ -Recurse | 
            Select-Object @{Name="Path"; Expression = {$_.PSParentPath.Split("::")[2]}}, DnsNameList, SendAsTrustedIssuer, FriendlyName, Issuer, Subject, NotAfter, NotBefore, Thumbprint, @{Name="Algorithm"; Expression = {$_.SignatureAlgorithm.FriendlyName}} | 
            Where-Object {$_.PSIsContainer -ne $True}
        
        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
        }

        return $ResultsArray | Select-Object Host, DateScanned, Path, DnsNameList, SendAsTrustedIssuer, FriendlyName, Issuer, Subject, NotAfter, NotBefore, Thumbprint, Algorithm
    }

    end{
        
        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}