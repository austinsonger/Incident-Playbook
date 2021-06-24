$Module = "Get-ComputerDetails"
$InputList = "C:\Temp\Scope.csv"
$OutputPath = "C:\Temp\{0}_{1}.csv" -f $Module, (Get-Date -Format 'yyyy-MM-dd')

$JobArguments = @{
    Name = "$_"
    Throttle = 200
    InputObject = (Get-Content $InputList)
    FunctionsToLoad = $Module
    ScriptBlock = [scriptblock]::Create('& $Using:Module $_')
}

$stopwatch = New-Object System.Diagnostics.Stopwatch
$stopwatch.Start()

Start-RSJob @JobArguments

# Job management 
While (Get-RSJob) { # So long as there is a job remaining 
    $CompletedJobs = Get-RSJob -State Completed
    $RunningJobs = Get-RSJob -State Running
    $NotStartedJobs = Get-RSJob -State NotStarted
        
    Write-Host -Object ("{0} `t {1} completed jobs `t {2} active jobs `t {3} not started." -f (Get-Date -Format u), $CompletedJobs.Count, $RunningJobs.Count, $NotStartedJobs.Count)
        
    ForEach ($DoneJob in $CompletedJobs) {

        Receive-RSJob -Id $DoneJob.ID | Export-Csv $OutputPath -NoTypeInformation -Append
        Stop-RSJob -Id $DoneJob.ID
        Remove-RSJob -Id $DoneJob.ID
    }

    Start-Sleep -Seconds 10
}

$Elapsed = $stopwatch.Elapsed
Write-Host -Object ("Completed Jobs: {0} `t Total time elapsed: {1}" -f $CompletedJobs.Count, $Elapsed)
