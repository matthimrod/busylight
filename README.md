# busylight
Raspberry Pi busy indicator light

## Requirements

### PowerShell Client

* Microsoft Lync 2013 SDK: https://www.microsoft.com/en-us/download/details.aspx?id=36824
* Microsoft Skype for Business 
* Microsoft PowerShell 7.x

Start the client in the background by running the following in PowerShell:

```PowerShell
Start-Job -FileName queryLyncStatus.ps1
```

Stop the client using the following:
```PowerShell
Get-Job                  # Gets the list of Job IDs
Stop-Job -Id {Job ID}    # Stops the Job
Remove-Job -Id {Job ID}  # Removes the Job from the Job List
```

<sub>Note: Microsoft Teams Presence is available throught the Graph API (https://docs.microsoft.com/en-us/graph/api/presence-get). However, this requires the Presence.Read permission, and my organization has this permission restricted. As a workaround, a users' status is reflected in Skype for Business even though my organization uses Teams exclusively. The Lync API allows reading Availability, which reflects the same value as the Teams presence.</sub>

### Server

* Raspberry Pi / Raspberry Pi Zero with SPI enabled (see below)
* Pimoroni Unicorn HAT Mini for Raspberry Pi - PIM498 (https://www.adafruit.com/product/4637)

```bash
$ sudo raspi-config nonint do_spi 0
$ pip3 install -r requirements.txt
```

