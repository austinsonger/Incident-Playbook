function Invoke-Meerkat_PSExec {
    <#
    .SYNOPSIS 
        Deploys Invoke-Meerkat using psexec.

    .DESCRIPTION 
        Deploys Invoke-Meerkat using psexec. Some environments block ports 5985, 5986, or otherwise prohibit WinRM. 
        This uses psexec to bypass those restrictions.

        Invoke-Meerkat_PSExec is provided as a wrapper to simplify working with PSExec, since typical psexec use does not include deploying a module, importing it, running it, storing results, retrieving results, and removing the module and results from the target. 

        1. The basic syntax for Invoke-Meerkat_PSExec is `Invoke-Meerkat-PSExec -Computer WorkComputer`, which runs a default collection. Customization of the collection requires adjusting the -Command parameter: `Invoke-Meerkat_psexec -Computer "systemname" -Command 'Invoke-Meerkat -Mod Computer, MAC'`

        2. The syntax for a single function where you must specificy parameters (e.g. when you need to run MAC with -Path 'c:\') is 
        
        ```
        $ModulePath = "$ENV:USERPROFILE\Documents\WindowsPowerShell\Modules\Meerkat\Functions"
        $ModuleName = "Get-MAC.psm1"
        $Command = "Get-MAC -Path 'c:\' | export-csv 'c:\Windows\Toolkit\Results\mac.csv' -notypeinformation"

        Invoke-Meerkat_PSExec -Computer "systemname" -ModulePath $ModulePath -ModuleName $ModuleName -Command $Command
        ```

    .PARAMETER Computer  
        Computer can be a single hostname, FQDN, or IP address.

    .PARAMETER ModulePath
        Local folder of module to deploy. Default is "$ENV:USERPROFILE\Documents\WindowsPowerShell\Modules\Meerkat\"
    
    .PARAMETER Output
        Local folder save results to. Default is "C:\Temp\Results\"

    .PARAMETER ModuleName
        Name of module to deploy. Default is "Meerkat.psm1"

    .PARAMETER PSExec
        Local folder containing the psexec.exe file. Default is "C:\Program Files\Sysinternals"
        
    .PARAMETER RemoteModulePath
        Remote path to store deployed module. Default is "C:\Windows\Meerkat\"

    .PARAMETER RemoteOutputPath
        Remote path to store scan results. Default is "C:\Windows\Meerkat\Results\"

    .PARAMETER Command
        Command to execute on remote system. Default is "Invoke-Meerkat". 
        Special parameters to Invoke-Meerkat like "Invoke-Meerkat -Module MAC" can also be used.        

    .EXAMPLE
        Invoke-Meerkat-PSExec -Computer WorkComputer
        Invoke-Meerkat-PSExec -Computer WorkComputer -Command "Invoke-Meerkat -Module MAC"
        Invoke-Meerkat_psexec -Computer WorkComputer -Command 'Get-MAC -Hash | export-csv c:\windows\Meerkat\results\MAC.csv -notypeinformation'

    .NOTES 
        Updated: 2019-09-11

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
       https://docs.microsoft.com/en-us/sysinternals/downloads/
    #>

    [CmdletBinding()]
    param(
        #Remote Parameters
        [Parameter(ValueFromPipeline = $True, ValueFromPipelineByPropertyName = $True)]
        [string]$Computer = "127.0.0.1",
        [string]$RemoteModulePath = "c:\Windows\Meerkat\",
        [string]$RemoteOutputPath = "c:\Windows\Meerkat\Results\",
        [string]$Command = "Invoke-Meerkat",
        
        #Local Parameters
        [string]$ModulePath = "C:\Program Files\WindowsPowerShell\Modules\Meerkat\Modules",
        [string]$Output = "$ENV:USERPROFILE\Meerkat\",
        [string]$ModuleName = "Meerkat.psm1",
        [string]$PSExec = "C:\Program Files\Sysinternals"
    )

    begin{
        function Copy-WithProgress { # https://blogs.technet.microsoft.com/heyscriptingguy/2015/12/20/build-a-better-copy-item-cmdlet-2/

            param(
                $Source,
                $Destination
            )

            $Source = $Source.tolower()
            $Filelist = Get-Childitem $Source -Recurse
            $Total = $Filelist.count
            $Position = 0

            New-Item -ItemType Directory -Path $Destination -Force

            foreach ($File in $Filelist) {
                
                $Filename = $File.Fullname.tolower().replace($Source,"")
                $DestinationFile = ($Destination + $Filename)
                
                Copy-Item $File.FullName -Destination $DestinationFile -Recurse -Force
                
                $Position++
                Write-Progress -Activity "Copying data from $Source to $Destination" -Status "Copying File $Filename" -PercentComplete (($Position/$total)*100)
            }

            Write-Progress -Activity "Copying data from $Source to $Destination" -Completed
        }
    }

    process{

        # Prepare NTFS/Share path versions
         $ModuleShare = $RemoteModulePath.Replace(':', '$')
         $ModuleNTFS = $RemoteModulePath.Replace('$', ':')
         $OutputShare = $RemoteOutputPath.Replace(':', '$')

        if($Command -like "Invoke-Meerkat*"){
            
            if($Command -like "*output*"){
                Write-Error -Message "Specify remote output via -RemoteOutputPath parameter."
                exit
            }

            $Command = $Command + " -Output $RemoteOutputPath"
            
        } else {
            
            mkdir \\$Computer\$OutputShare -ErrorAction SilentlyContinue
        }

        # Stage files
        #Copy-Item $ModulePath -Recurse -Force -Destination \\$Computer\$ModuleShare -- has issues, hence the Copy-WithProgress function
        Copy-WithProgress -Source "$ModulePath" -Destination "\\$Computer\$ModuleShare"

        # Import modules and execute command as system. -s was added due to access denied errors on only some modules.
        & $PSExec\PsExec.exe \\$Computer -s -accepteula powershell -ExecutionPolicy ByPass -windowstyle hidden -nologo -noprofile -command "& {import-module $ModuleNTFS\$ModuleName; & $Command}"
    }

    end{
        # Retrieve Results
        Copy-WithProgress -Source \\$Computer\$OutputShare -Destination $Output

        # Cleanup
        Remove-Item \\$Computer\$OutputShare -Recurse -Force
        Remove-Item \\$Computer\$ModuleShare -Recurse -Force
    }
}