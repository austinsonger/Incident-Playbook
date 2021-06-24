function Get-TPMDetails{
    <#
    .SYNOPSIS 
        Gets TPM info.

    .DESCRIPTION 
        Gets TPM info. Converts ManufacturerId if the ID is in the list of built-in names.

    .EXAMPLE 
        Get-TPMDetails

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-TPMDetails} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\TPM.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-TPMDetails} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_TPM.csv")
        }

    .NOTES 
        Updated: 2019-04-07

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
        https://trustedcomputinggroup.org/vendor-id-registry/
        https://portal.msrc.microsoft.com/en-US/security-guidance/advisory/ADV170012
    #>

    [CmdletBinding()]
    param(
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-TPMDetails at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()

        $Manufacturers = @{
            0x414D4400 = "AMD"
            0x41544D4C = "Atmel"
            0x4252434D = "Broadcom"
            0x474F4F47 = "Google"
            0x48504500 = "HPE"
            0x49424d00 = "IBM"
            0x49465800 = "Infineon"
            0x494E5443 = "Intel"
            0x4C454E00 = "Lenovo"
            0x4D534654 = "Microsoft"
            0x4E534D20 = "National Semiconductor"
            0x4E544300 = "Nuvoton Technology"
            0x4E545A00 = "Nationz"
            0x51434F4D = "Qualcomm"
            0x524F4343 = "Fuzhou Rockchip"
            0x534D5343  = "SMSC"
            0x534D534E = "Samsung"
            0x534E5300 = "Sinosun"
            0x53544D20 = "ST Microelectronics"
            0x54584E00 = "Texas Instruments"
            0x57454300 = "Winbond"
        }
    }

    process{

        $ResultsArray =  Get-Tpm -ErrorAction SilentlyContinue
        
        foreach ($Result in $ResultsArray) {
           
            $Result | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME            
            $Result | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned

            $Result | Add-Member -MemberType NoteProperty -Name "FirmwareVersionAtLastProvision" -Value (Get-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\TPM\WMI" -Name "FirmwareVersionAtLastProvision" -ErrorAction SilentlyContinue).FirmwareVersionAtLastProvision
            $Result | Add-Member -MemberType NoteProperty -Name "ManufacturerName" -Value ""

            foreach ($Key in $Manufacturers.Keys) {

                if ($Key -eq $Result.ManufacturerId) {
                    
                    $Result.ManufacturerName = $Manufacturers[$Key]
                }
            }
        }

        return $ResultsArray | Select-Object Host, DateScanned, TpmPresent, TpmReady, ManufacturerId, ManufacturerName, ManufacturerVersion,
        ManagedAuthLevel, OwnerAuth, OwnerClearDisabled, AutoProvisioning, LockedOut, LockoutCount, LockoutMax, SelfTest, FirmwareVersionAtLastProvision
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}
