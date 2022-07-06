$TeamsLogFile = (Join-Path -Path $Env:APPDATA -ChildPath 'Microsoft\Teams\logs.txt')
$Url = "http://busylight.lan:5000/api/presence"
$MaxRetry = 5
$RetryWait = 5
$Delay = 60

while($true){

    $LogContent = Get-Content $TeamsLogFile -tail 1000
    $Selected = ($LogContent | Select-String -Pattern 'StatusIndicatorStateService\: Added (\w+) [^|]*')
    $activity = $Selected.Matches[$Selected.Matches.Length - 1].Groups[1].Value
    Write-Output "Found $activity"

    if ($null -ne $activity) {
        $retries = $MaxRetry
        do {
            Write-Log "Setting status to $activity"
            try {
                Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
                $retries = 0
            } catch [System.Object] {
                $retries--
                Start-Sleep -Seconds $RetryWait
            }
        } until ($retries -eq 0) 
    }
    Start-Sleep –Seconds $Delay 
}
