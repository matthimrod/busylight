$Url = "http://busylight.lan:5000/api/presence"
$StartTimeout = New-TimeSpan -Minutes 2
$InitTimeout = New-TimeSpan -Minutes 2
$LoopTimeout = New-TimeSpan -Minutes 5
$Delay = 15

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";

# Start Lync if it's not running (it won't spawn multiple).
Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"

# Loop until client object is returned. After 2 minutes, give up.
# Note: If we gave up waiting for Lync ot start, the call to get contact
# ActivityId below will fail and we'll turn the light off and exit.\
$Lync = $null
$Timer = [System.Diagnostics.Stopwatch]::StartNew()
while($Timer.Elapsed -lt $StartTimeout -and $null -eq $Lync) {
    try {
        $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
    } catch [System.Management.Automation.MethodInvocationException] {
        start-sleep –Seconds 1
        $Lync = $null
    }
} 

# Loop until we get the initial contact ActivityId. After 2 minutes, give up.
# Note: If we gave up waiting, the call to get contact ActivityId below will 
# fail and we'll turn the light off and exit. This just extends the initial 
# time.
$activity = ""
$Timer = [System.Diagnostics.Stopwatch]::StartNew()
while($Timer.Elapsed -lt $InitTimeout -and $activity -eq "") {
    try {
        $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
    } catch {
        $activity = ""
        start-sleep –Seconds 1
    }
} 

$LastActivity = ""
$Timer = [System.Diagnostics.Stopwatch]::StartNew()
while($true){
    # If the Lync client goes away, turn off the light and exit.
    try {
        $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
    } catch {
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = 'off' }
        Exit
    }
    
    # Loop if the activities (statuses) are different, change the light.
    # After 5 minutes, re-send the status in case something happened to the lights.
    if ($activity -ne $LastActivity -or $Timer.Elapsed -gt $LoopTimeout) {
        $Timer = [System.Diagnostics.Stopwatch]::StartNew()
        try {
            Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
            $LastActivity = $activity
        } catch [System.Object] {
            start-sleep 1
        }
    }
    start-sleep –Seconds $Delay 
}
