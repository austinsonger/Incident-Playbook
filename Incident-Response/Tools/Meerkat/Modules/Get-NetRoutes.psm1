function Get-NetRoutes {
    <#
    .SYNOPSIS 
        Gets a list of IPv4 Routes.

    .DESCRIPTION 
        Gets a list of IPv4 Routes.

    .EXAMPLE 
        Get-NetRoutes

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-NetRoutes} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\NetRoutes.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-MRU} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_NetRoute.csv")
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
        Write-Information -InformationAction Continue -MessageData ("Started Get-NetRoutes at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()

        Enum RouteType {
            AdminDefinedRoute = 2
            ComputedRoute = 3
            ActualRoute = 4        
        }
    }

    process{

        $InterfaceArray = $null
        $InterfaceArray = Get-NetAdapter | Where-Object {$_.MediaConnectionState -eq "Connected"}
        
        $ResultsArray = foreach ($Interface in $InterfaceArray) {
            Get-NetRoute -AddressFamily IPv4 -InterfaceIndex $Interface.ifIndex -IncludeAllCompartments -ErrorAction SilentlyContinue
        }

        foreach ($Result in $ResultsArray) {
            
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
            $Result | Add-Member -MemberType NoteProperty -Name "RouteType" -Value ([RouteType]$Result.TypeOfRoute).ToString()
        } 

        return $ResultsArray | Select-Object Host, DateScanned, ifIndex, InterfaceAlias, DestinationPrefix, 
        NextHop, RouteMetric, Protocol, Store, Publish, TypeOfRoute, RouteType
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}