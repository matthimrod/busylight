$Delay = 15
$LogFile = Join-Path -Path (Split-Path $MyInvocation.MyCommand.Path) -ChildPath 'LyncClient.log'
$Url = "http://busylight.lan:5000/api/presence"

Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";

function Get-LyncClient {
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
        [System.Object[]]$Lync
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
        [String]$Text
    )
    $Timestamp = "[{0:MM/dd/yy} {0:HH:mm:ss}]" -f (Get-Date)
    Write-Output "$Timestamp $Text"
    Write-Output "$Timestamp $Text" | Out-File -Append $LogFile
}

function Set-Light {
    param (
        [String]$activity = 'off'
    )
    Write-Log "Sending activity: $($activity) to $($Url)"
    try {
        $result = Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
        Write-Log (ConvertTo-Json -Compress $result)
        return $true
    } catch [System.Net.Http.HttpRequestException], 
            [Microsoft.PowerShell.Commands.HttpResponseException] {
        Write-Log $_.Exception.Message
        return $false
    }
}

function Done {
    param (
        [String]$Text
    )
    if ($Text) { Write-Log $Text }
    Set-Light
    Exit
}


# Make PowerShell Disappear
$windowcode = '[DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);'
$asyncwindow = Add-Type -MemberDefinition $windowcode -name Win32ShowWindowAsync -namespace Win32Functions -PassThru
$null = $asyncwindow::ShowWindowAsync((Get-Process -PID $pid).MainWindowHandle, 0)


Write-Log "Getting Lync Client object."
$Lync = Get-LyncClient
if ($null -eq $Lync) {
    Done "Unable to create Lync Client object."
} else {
    Write-Log "Got Lync Client object."
}

$LastActivity = ""

while($true){

    $activity = Get-LyncActivity $Lync
    if ($null -eq $activity) {
        Done "Unable to get Lync Activity."
    }

    $try = 0
    while ($activity -ne $LastActivity) {
        if (Set-Light $activity) {
            $LastActivity = $activity
        } elseif ($tries -eq 10) {
            Done "Unable to update BusyLight."
        } else {
            Start-Sleep –Seconds $Delay 
            $try++
        }
    }
    Start-Sleep –Seconds $Delay     
}
