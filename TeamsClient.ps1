$TeamsLogFile = (Join-Path -Path $Env:APPDATA -ChildPath 'Microsoft\Teams\logs.txt')
$Url = "http://busylight.lan:5000/api/presence"
$MaxRetry = 5
$RetryWait = 5
$Delay = 60
$Host.UI.RawUI.WindowTitle = "BusyLight Client"

function Get-TimeStamp {
    return "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
}

$LastActivity = ""

while($true){

    $LogContent = Get-Content $TeamsLogFile -tail 1000 | Select-String -Pattern 'StatusIndicatorStateService\: Added (\w+) [^|]*'
    $activity = $LogContent.Matches[$LogContent.Matches.Length - 1].Groups[1].Value

    if ($null -ne $activity -and $activity -ne $LastActivity) {
        $retries = $MaxRetry
        do {
            Write-Output "$(Get-TimeStamp) Setting status to $activity"
            try {
                $result = Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
                $LastActivity = $activity
                $retries = 0
            } catch [System.Object] {
                $retries--
                Start-Sleep -Seconds $RetryWait
            }
        } until ($retries -eq 0) 
    }
    Start-Sleep –Seconds $Delay 
}
