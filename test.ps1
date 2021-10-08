$Url = "http://busylight.lan:5000/api/presence"
$Delay = 15
$scriptPath = split-path -parent $MyInvocation.MyCommand.Definition
$Logfile = Join-Path -Path $scriptPath -ChildPath "busylight.log"

# Add-Type –Path "C:\Program Files (x86)\Microsoft Office 2013\LyncSDK\Assemblies\Desktop\Microsoft.Lync.Model.dll";

function Get-LyncClient {
    param (
        [Int32]$Delay
    )

    $Lync = $null

    # for ($i = 0; $i -lt 5 -and $null -eq $Lync; $i++) {
    #     try {
    #         $Lync = [Microsoft.Lync.Model.LyncClient]::GetClient()
    #     } catch [System.Management.Automation.MethodInvocationException] {
    #         Start-Process "C:\Program Files (x86)\Microsoft Office\root\Office16\lync.exe"
    #         Start-Sleep –Seconds $Delay
    #     }
    # }
    $Lync = "Not null!!"

    return $Lync
}

function Get-LyncActivity {
    param (
        [System.Object[]]$Lync,
        [Int32]$Delay
    )

    $activity = $null

    # for ($i = 0; $i -lt 5 -and $null -eq $activity; $i++) {
    #     try {
    #         $activity = $Lync.Self.Contact.GetContactInformation("ActivityId")
    #     } catch {
    #         $activity = $null
    #         Start-Sleep –Seconds $Delay
    #     }
    # }
    $activity = 'busy'

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


function Set-Light {
    param (
        [String]$activity = 'off'
    )

    Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }

}

function CleanupAndExit {
    Set-Light
    $Main_Tool_Icon.Visible = $false
    Stop-Process $pid
}





# Make PowerShell Disappear - Thanks Chrissy
$windowcode = '[DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hWnd, int nCmdShow);'
$asyncwindow = Add-Type -MemberDefinition $windowcode -name Win32ShowWindowAsync -namespace Win32Functions -PassThru
$null = $asyncwindow::ShowWindowAsync((Get-Process -PID $pid).MainWindowHandle, 0)
 
# Use a Garbage colection to reduce Memory RAM
# https://dmitrysotnikov.wordpress.com/2012/02/24/freeing-up-memory-in-powershell-using-garbage-collector/
# https://docs.microsoft.com/fr-fr/dotnet/api/system.gc.collect?view=netframework-4.7.2
[System.GC]::Collect()
 
# Add assemblies for WPF
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
# Add-Type -AssemblyName presentationframework
# Add-Type -AssemblyName System.Drawing WindowsFormsIntegration')

# Add the systray icon
$Main_Tool_Icon = New-Object System.Windows.Forms.NotifyIcon
$Main_Tool_Icon.Text = "BusyLight Client"
$Main_Tool_Icon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon((Join-Path -Path $scriptPath -ChildPath "traffic_light.ico")) 
$Main_Tool_Icon.Visible = $true

$Menu_Log = New-Object System.Windows.Forms.MenuItem
$Menu_Log.Text = "Show log"
$Menu_Log.Add_Click({
    Start-Process notepad.exe $Logfile 
})

$Menu_Exit = New-Object System.Windows.Forms.MenuItem
$Menu_Exit.Text = "Exit"
$Menu_Exit.add_Click({
    CleanupAndExit
})

# Add all menus as context menus
$contextmenu = New-Object System.Windows.Forms.ContextMenu
$Main_Tool_Icon.ContextMenu = $contextmenu
$Main_Tool_Icon.contextMenu.MenuItems.AddRange($Menu_Log)
$Main_Tool_Icon.contextMenu.MenuItems.AddRange($Menu_Exit)







Write-Log $Logfile "Getting Lync Client object."
$Lync = Get-LyncClient($Delay)
if ($null -eq $Lync) { 
    Write-Log $Logfile "Unable to create Lync Client object."
    CleanupAndExit 
} else {
    Write-Log $Logfile "Got Lync Client object."
}

$LastActivity = ""

while($true) {
    $activity = Get-LyncActivity($Lync, $Delay)
    if ($null -eq $activity) {
        Write-Log $Logfile "Unable to get Lync Activity."
        Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = 'off' }
        CleanupAndExit
    }

    if ($activity -ne $LastActivity) {
        try {
            Invoke-RestMethod -Uri $Url -Method 'Post' -Body @{ state = $activity }
            $LastActivity = $activity
        } catch [System.Object] {
            Start-Sleep -Milliseconds 1
        }
                
    }
    
    for($i = 0; $i -lt (1000 * $Delay); $i =+ 100) {
        Start-Sleep -Milliseconds 100
    }
}


# Create an application context for it to all run within - Thanks Chrissy
# This helps with responsiveness, especially when clicking Exit - Thanks Chrissy
$appContext = New-Object System.Windows.Forms.ApplicationContext
[void][System.Windows.Forms.Application]::Run($appContext)
