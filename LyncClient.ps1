$Url = "http://busylight.lan:5000/api/presence"
$Delay = 15

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";
try {
    $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
} catch [System.Management.Automation.MethodInvocationException] {
    Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"
    start-sleep –Seconds $Delay
    $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
}

$LastActivity = ""

while($true){
    try {
        $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
    } catch {
        Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"
        start-sleep –Seconds $Delay 
        $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
    }
    
    if ($activity -ne $LastActivity) {
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
        $LastActivity = $activity
    }
    start-sleep –Seconds $Delay 
}
