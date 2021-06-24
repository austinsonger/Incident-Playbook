function Get-Strings {
    <#
    .SYNOPSIS 
        Gets a list of strings from the executables tied to each process.

    .DESCRIPTION 
        Gets a list of strings from the executables tied to each process.

    .PARAMETER PathContains
        If specified, limits the strings collection via -like.

    .PARAMETER MinimumLength
        7 by default. Specifies the minimum string length to return. 

    .EXAMPLE 
        Get-Strings

    .EXAMPLE 
        Invoke-Command -ComputerName remoteHost -ScriptBlock ${Function:Get-Strings} | 
        Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
        Export-Csv -NoTypeInformation ("c:\temp\Strings.csv")

    .EXAMPLE 
        $Targets = Get-ADComputer -filter * | Select -ExpandProperty Name
        ForEach ($Target in $Targets) {
            Invoke-Command -ComputerName $Target -ScriptBlock ${Function:Get-Strings} | 
            Select-Object -Property * -ExcludeProperty PSComputerName,RunspaceID | 
            Export-Csv -NoTypeInformation ("c:\temp\" + $Target + "_Strings.csv")
        }

    .NOTES 
        Updated: 2019-04-05

        Contributing Authors:
            Anthony Phipps    
            Jeremy Arnold
            
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
       https://www.zerrouki.com/powershell-cheatsheet-regular-expressions/
    #>

    [CmdletBinding()]
    param(
        [Parameter()]
        $PathContains,

        [Parameter()]
        $MinimumLength = 7
    )

    begin{

        $DateScanned = Get-Date -Format u
        Write-Information -InformationAction Continue -MessageData ("Started Get-Strings at {0}" -f $DateScanned)

        $stopwatch = New-Object System.Diagnostics.Stopwatch
        $stopwatch.Start()
    }

    process{

        $ProcessArray = Get-Process | Where-Object {$null -ne $_.Path} | Select-Object -Unique path

        if ($PathContains){
            $ProcessArray = $ProcessArray | Where-Object {$_.Path -like $PathContains} | Select-Object -Unique path    
        }

        $ProcessStringsArray = foreach ($ProcessFile in $ProcessArray) {
            
            $ProcessLocation = $ProcessFile.Path

            $UnicodeFileContents = Get-Content -Encoding "Unicode" -Path $ProcessLocation
            $UnicodeRegex = [Regex] "[\u0020-\u007E]{$MinimumLength,}"
            $StringArray = $UnicodeRegex.Matches($UnicodeFileContents).Value
            
            $Process = [pscustomobject] @{

                ProcessLocation = $ProcessLocation 
                StringArray = $StringArray
            }
                
            $AsciiFileContents = Get-Content -Encoding "UTF7" -Path $ProcessLocation
            $AsciiRegex = [Regex] "[\x20-\x7E]{$MinimumLength,}"
            $StringArray = $AsciiRegex.Matches($AsciiFileContents).Value
            
            $Process = [pscustomobject] @{
                ProcessLocation = $ProcessLocation 
                StringArray = $StringArray
            }

            $Process
        }

        if ($ProcessStringsArray) {

            [regex]$regexEmail = '^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$'
            [regex]$regexIP = '^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])$'
            [regex]$regexURL = '^https?:\/\/'
            
            $ResultsArray = foreach ($Process in $ProcessStringsArray) {
                
                foreach ($StringItem in $Process.StringArray){

                    if (($StringItem -match $regexEmail) -or ($StringItem -match $regexIP) -or ($StringItem -match $regexURL)){
                                        
                        $output = $null
                        $output = New-Object -TypeName PSObject

                        $output | Add-Member -MemberType NoteProperty -Name "Host" -Value $env:COMPUTERNAME
                        $output | Add-Member -MemberType NoteProperty -Name "DateScanned" -Value $DateScanned
                        
                        $output | Add-Member -MemberType NoteProperty -Name ProcessLocation -Value $Process.ProcessLocation -ErrorAction SilentlyContinue
                        $output | Add-Member -MemberType NoteProperty -Name String -Value $StringItem -ErrorAction SilentlyContinue
                                        
                        $output
                    }
                }
            }
            
            return $ResultsArray | Select-Object Host, DateScanned, ProcessLocation, String
        }
    }

    end{

        $elapsed = $stopwatch.Elapsed

        Write-Verbose ("Total time elapsed: {0}" -f $elapsed)
        Write-Verbose ("Ended at {0}" -f (Get-Date -Format u))
    }
}