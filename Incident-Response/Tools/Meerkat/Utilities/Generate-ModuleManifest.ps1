$FileList = @('Meerkat.psd1', 'Meerkat.psm1')
$FunctionsToExport = @()

Get-ChildItem "..\Modules" -Filter *.psm1 | Select-Object -ExpandProperty FullName | ForEach-Object {
    $File = Split-Path $_ -Leaf
    $Function = $File.Split(".")[0]
    $FileList += "Modules\" + $File
    $FunctionsToExport += $Function
}

$manifest = @{
    RootModule = 'Meerkat.psm1'
    Path = '..\Meerkat.psd1'
    CompatiblePSEditions = @('Desktop','Core')
    Author = 'Anthony Phipps, Jeremy Arnold'
    CompanyName = 'See Authors'
    Copyright = 
        'This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
        
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/'
    Description = 'Hunters Artifact, Metadata, and Events Recon'
    FileList = $FileList
    FunctionsToExport = $FunctionsToExport
}

New-ModuleManifest @manifest
