function Get-DNS {
    <#
    .SYNOPSIS 
        Gets the DNS cache from all connected interfaces.

    .DESCRIPTION 
        Gets the DNS cache from all connected interfaces.

    .PARAMETER Computer  
        Computer can be a single hostname, FQDN, or IP address.

    .EXAMPLE 
        Get-DNS

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-DNS} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\DNS.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-DNS} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_DNS.csv")
        }

    .NOTES 
        Updated: 2019-04-18

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
        Write-Information -InformationAction Continue -MessageData ("Started Get-DNS at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()

        enum recordType {
            A = 1
            NS = 2
            CNAME = 5
            SOA = 6
            WKS = 11
            PTR = 12
            HINFO = 13
            MINFO = 14
            MX = 15
            TXT = 16
            AAAA = 28
            SRV = 33
            ALL = 255
        }

        enum recordStatus {
            Success = 0
            NotExist = 9003
            NoRecords = 9501
        }

        enum recordResponse {
            Question = 0
            Answer = 1
            Authority = 2
            Additional = 3
        }
    }

    process{

        $ResultsArray = Get-DnsClientCache

        foreach ($Result in $ResultsArray) {
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
            $Result | Add-Member -MemberType NoteProperty -Name "RecordType" -Value ([recordType]$Result.Type).ToString()
            $Result | Add-Member -MemberType NoteProperty -Name "RecordStatus" -Value ([recordStatus]$Result.Status).ToString()
            $Result | Add-Member -MemberType NoteProperty -Name "RecordResponse" -Value ([recordResponse]$Result.Section).ToString()
        }

        return $ResultsArray | Select-Object Host, DateScanned, Status, RecordStatus, DataLength, Section, RecordResponse, TimeToLive, Type, RecordType, Data, Entry, Name
    }

    end{
        
        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}