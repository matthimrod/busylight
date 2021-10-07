# Use a Garbage colection to reduce Memory RAM
# https://dmitrysotnikov.wordpress.com/2012/02/24/freeing-up-memory-in-powershell-using-garbage-collector/
# https://docs.microsoft.com/fr-fr/dotnet/api/system.gc.collect?view=netframework-4.7.2
[System.GC]::Collect()
 
# Add assemblies for WPF
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
# Add-Type -AssemblyName presentationframework
# Add-Type -AssemblyName System.Drawing WindowsFormsIntegration')

# Choose an icon to display in the systray
$icon = [System.Drawing.Icon]::ExtractAssociatedIcon("C:\Users\himrodma\GitHub\busylight\traffic_light.ico") 
 
# Add the systray icon
$Main_Tool_Icon = New-Object System.Windows.Forms.NotifyIcon
$Main_Tool_Icon.Text = "BusyLight Client"
$Main_Tool_Icon.Icon = $icon
$Main_Tool_Icon.Visible = $true

$Menu_Log = New-Object System.Windows.Forms.MenuItem
$Menu_Log.Text = "Show log"
$Menu_Log.Add_Click({
    Start-Process pwsh
})

$Menu_Status = New-Object System.Windows.Forms.MenuItem
$Menu_Status.Text = "Show status"

$Menu_Exit = New-Object System.Windows.Forms.MenuItem
$Menu_Exit.Text = "Exit"
$Menu_Exit.add_Click({
    $Main_Tool_Icon.Visible = $false
    Stop-Process $pid
})

# Add all menus as context menus
$contextmenu = New-Object System.Windows.Forms.ContextMenu
$Main_Tool_Icon.ContextMenu = $contextmenu
$Main_Tool_Icon.contextMenu.MenuItems.AddRange($Menu_Log)
$Main_Tool_Icon.contextMenu.MenuItems.AddRange($Menu_Status)
$Main_Tool_Icon.contextMenu.MenuItems.AddRange($Menu_Exit)

# Create an application context for it to all run within - Thanks Chrissy
# This helps with responsiveness, especially when clicking Exit - Thanks Chrissy
$appContext = New-Object System.Windows.Forms.ApplicationContext
[void][System.Windows.Forms.Application]::Run($appContext)


Write-Output "I'm still here"
Start-Sleep 5
Write-Output "Yup still here"
Start-Sleep 15
Write-Output "And still here"
