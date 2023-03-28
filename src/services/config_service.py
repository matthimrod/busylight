import json
import re
from typing import Mapping, Tuple, TypedDict


class ConfigFileDict(TypedDict):
    default_brightness: float
    default_state: str
    colors: Mapping[str, str]
    statuses: Mapping[str, Mapping[str, str]]


# Sample
"""
{
    'default_brightness': 1.0,
    'default_state': 'off',
    'colors': {
        'red': '#ff0000',
        'orange': '#ff3000',
        'yellow': '#ffc000',
        'green': '#008000',
        'blue': '#0000ff',
        'purple': '#800080',
        'white': '#ffffff'
    },
    'hue_room': 'Webcam',
    'states': {
        'away': {'busylight': 'off', 
                 'hue': 'off'},
        'berightback': {'busylight': 'off', 
                        'hue': 'off'},
        'busy': {'busylight': 'orange', 
                 'hue': 'off'},
        'donotdisturb': {'busylight': 'red', 
                         'hue': 'off'},
        'free': {'busylight': 'green', 
                 'hue': 'off'},
        'in-a-meeting': {'busylight': 'red', 
                         'hue': 'Webcam'},
        'in-presentation': {'busylight': 'red', 
                            'hue': 'Webcam'},
        'on-the-phone': {'busylight': 'red', 
                         'hue': 'Webcam'}
    }
}
"""


class ConfigService:
    """
    Configuration management service.
    """

    config_file: str
    default_brightness: float
    default_state: str
    color_map: Mapping[str, str]
    status_map: Mapping[str, Mapping[str, str]]

    @staticmethod
    def rgb_hex_to_dec(rgb_hex: str) -> Tuple[int, int, int]:
        """
        Converts an RGB hex string in the format #RRGGBB to a tuple of RGB values in decimal.

        Args:
            rgb_hex (str): RGB Hex String #RRGGBB

        Returns:
            Tuple[int, int, int]: tuple contianing RGB values
        """
        result = re.match(
            r'#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$', rgb_hex)
        if result:
            return (int(result.group(1), 16), int(result.group(2), 16), int(result.group(3), 16))
        else:
            raise ValueError()

    def __init__(self, filename: str) -> None:
        """
        Constructor.
        """

        self.load(filename)

    def load(self, filename: str) -> None:
        """
        Loads the configuration from a JSON text file. 

        Args:
            filename (str): The filename containing the configuration.
        """
        try:
            with open(filename, 'r') as read_file:
                config: ConfigFileDict = json.load(read_file)
        except OSError as ex:
            # Unable to read file.
            raise ex
        except json.JSONDecodeError as ex:
            # Unable to decode file.
            raise ex

        self.default_brightness = config.get('default_brightness', 1.0)
        self.default_state = config.get('default_state', 'off')

        self.color_map = {}
        for color in config.get('colors', {}).keys():
            if re.match('^#[0-9a-fA-F]{6}$', config['colors'][color]):
                self.color_map[color] = config['colors'][color]


