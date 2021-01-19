# https://devblogs.microsoft.com/scripting/use-powershell-to-integrate-with-the-lync-2013-sdk-for-skype-for-business-part-1/
# Microsoft Lync 2013 SDK: https://www.microsoft.com/en-us/download/details.aspx?id=36824
# Microsoft.Lync.Model namespace: https://docs.microsoft.com/en-us/previous-versions/office/lync-wpf/jj274810(v=office.15)

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";
$Url = "http://172.16.1.33:5000/api/presence"
$sleepInterval = 60

$lyncclient = [Microsoft.Lync.Model.LyncClient]::GetClient()

$myLastActivityId = ""

while($true){

    # ContactInformationType enumeration
    # https://docs.microsoft.com/en-us/previous-versions/office/lync-wpf/jj277212(v=office.15)

    # Invoke-RestMethod
    # https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/invoke-restmethod?view=powershell-7.1
    
    $myActivityId = $lyncclient.Self.Contact.GetContactInformation("ActivityId")

    if ($myActivityId -ne $myLastActivityId) {
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $myActivityId }
        $myLastActivityId = $myActivityId
    }

    start-sleep –Seconds $sleepInterval 
}

# Turn off the light when exiting
# https://stackoverflow.com/questions/33602561/how-do-i-run-a-powershell-function-upon-my-process-being-killed-via-stop-proc
# $a = [System.Management.Automation.PSEngineEvent]::Exiting
# Register-EngineEvent -SourceIdentifier $a -Action {[console]::Beep(500,500)}