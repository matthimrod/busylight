# busylight

Raspberry Pi busy indicator light

## PowerShell Client

The PowerShell-based client has been moved to its own repository [here](https://github.com/matthimrod/busylight_client).

## Server

* Raspberry Pi / Raspberry Pi Zero with SPI enabled (see below)
* Pimoroni Unicorn HAT Mini for Raspberry Pi - PIM498 (https://www.adafruit.com/product/4637)

```bash
$ sudo raspi-config nonint do_spi 0
$ pip3 install -r requirements.txt
```

### Configuration

```json
{
    "default_brightness": 0.1,
    "default_state": "off",
    "colors": {
        "red":    [255,   0,   0],
        "orange": [255,  48,   0],
        "yellow": [255, 192,   0],
        "green":  [  0, 128,   0],
        "blue":   [  0,   0, 255],
        "purple": [128,   0, 128],
        "white":  [255, 255, 255]
    },
    "statuses": {
        "away":            "off",
        "berightback":     "off",
        "busy":         "orange",
        "donotdisturb":    "red",
        "free":          "green",
        "in-a-meeting":    "red",
        "in-presentation": "red", 
        "on-the-phone":    "red"
    }
}
```

brightness: Default brightness percentage (0.00 to 1.00)

default_state: Default state of the light when the server initializes

colors: map of names to RGB values

statuses: map of status names (from Lync API) to colors
