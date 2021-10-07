$Logfile = "C:\Users\himrodma\GitHub\busylight\busylight.log"
$Url = "http://busylight.lan:5000/api/presence"
$Delay = 15

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";

function Get-LyncClient {
    param (
        [Int32]$Delay
    )

    $Lync = $null

    for ($i = 0; $i -lt 5 -and $null -eq $Lync; $i++) {
        try {
            $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
        } catch [System.Management.Automation.MethodInvocationException] {
            Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"
            Start-Sleep –Seconds $Delay
        }
    }

    return $Lync
}

function Get-LyncActivity {
    param (
        [System.Object[]]$Lync,
        [Int32]$Delay
    )

    $activity = $null

    for ($i = 0; $i -lt 5 -and $null -eq $activity; $i++) {
        try {
            $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
        } catch {
            $activity = $null
            Start-Sleep –Seconds $Delay
        }
    }

    return $activity
}

function Write-Log {
    param (
        [String]$Log,
        [String]$Text
    )

    $Timestamp = "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    Write-Output "$Timestamp $Text"
    Write-Output "$Timestamp $Text" | Out-File -Append $Log 
}

Write-Log $Logfile "Getting Lync Client object."
$Lync = Get-LyncClient($Delay)
if ($null -eq $Lync) { 
    Write-Log $Logfile "Unable to create Lync Client object."
    Exit 
} else {
    Write-Log $Logfile "Got Lync Client object."
}

$LastActivity = ""

while($true){
    $activity = Get-LyncActivity($Lync, $Delay)
    if ($null -eq $activity) {
        Write-Log $Logfile "Unable to get Lync Activity."
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = 'off' }
        Exit
    }

    if ($activity -ne $LastActivity) {
        try {
            Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
            $LastActivity = $activity
        } catch [System.Object] {
            start-sleep 1
        }
                
    }
    start-sleep –Seconds $Delay 
}
