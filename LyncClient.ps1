$Url = "http://busylight.lan:5000/api/presence"
$Delay = 15

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";
$Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()

$LastActivity = ""

while($true){
    $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
    if ($activity -ne $LastActivity) {
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
        $LastActivity = $activity
    }
    start-sleep –Seconds $Delay 
}
