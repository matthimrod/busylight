Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";
$Url = "http://172.16.1.33:5000/api/presence"
$Delay = 60
$lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
$lastActivity = ""

while($true){
    $activity = $lync.Self.Contact.GetContactInformation("ActivityId")
    if ($activity -ne $lastActivity) {
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
        $lastActivity = $activity
    }
    start-sleep –Seconds $Delay 
}