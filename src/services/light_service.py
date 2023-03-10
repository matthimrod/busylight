import re
from typing import Optional, Union

from unicornhatmini import UnicornHATMini


class LightService:
    """
    Service to control the Unicornhat Mini.
    """

    unicornhatmini: UnicornHATMini
    brightness: float
    color_map: dict
    status_map: dict
    state: Optional[str]
    override: Optional[str]
    _colorBlue: int
    _colorGreen: int
    _colorRed: int
    _test_mode: bool

    def __init__(self, **kwargs) -> None:
        self.brightness = float(kwargs.get('brightness',
                                kwargs.get('config', {}).get('brightness', 1.0)))
        self.color_map = kwargs.get('config', {}).get('colors', {})
        self.status_map = kwargs.get('config', {}).get('statuses', {})
        self._test_mode = kwargs.get('test_mode', False)

        if not self._test_mode:
            self.unicornhatmini = UnicornHATMini()
            self.unicornhatmini.clear()
            self.unicornhatmini.show()

        if 'status' in kwargs:
            self.set_status(str(kwargs.get('status')))

    def _update(self, red: int, green: int, blue: int) -> None:
        self._colorRed = red
        self._colorGreen = green
        self._colorBlue = blue

        if not self._test_mode:
            self.unicornhatmini.set_all(self._colorRed,
                                        self._colorGreen,
                                        self._colorBlue)
            self.unicornhatmini.show()

    def _set_rgb(self, rgb_value: str) -> None:
        result = re.match(r'#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', rgb_value)
        if result:
            self._update(int(result.group(1), 16),
                         int(result.group(2), 16),
                         int(result.group(3), 16))

    def _set_color_name(self, color_name_value: str) -> None:
        if color_name_value in self.color_map:
            if re.match(r'#[0-9a-fA-F]{6}', self.color_map.get(color_name_value, '')):
                self._set_rgb(self.color_map.get(color_name_value, ''))

            elif isinstance(self.color_map.get(color_name_value), dict):
                self._update(self.color_map[color_name_value][0],
                             self.color_map[color_name_value][1],
                             self.color_map[color_name_value][2])

    def _set_state_name(self, state_value: str) -> None:
        if state_value in self.status_map:
            if re.match(r'#[0-9a-fA-F]{6}', self.status_map.get(state_value, '')):
                self._set_rgb(self.status_map.get(state_value, ''))

            elif self.status_map.get(state_value, '') in self.color_map:
                self._set_color_name(self.status_map.get(state_value, ''))

            elif isinstance(self.status_map.get(state_value), dict):
                self._update(self.status_map[state_value][0],
                             self.status_map[state_value][1],
                             self.status_map[state_value][2])

    def set_status(self, value: str) -> None:
        if value in self.status_map:
            self.state = value
            if not self.override:
                self._set_state_name(str(self.state))

        elif value in self.color_map:
            self.state = value
            if not self.override:
                self._set_color_name(str(self.state))

        elif re.match(r'#[0-9a-fA-F]{6}', str(self.state)):
            self.state = value
            if not self.override:
                self._set_rgb(str(self.state))

    def set_override(self, value: str) -> None:
        if value in self.status_map:
            self.override = value
            self._set_state_name(str(self.override))

        elif value in self.color_map:
            self.override = value
            self._set_color_name(str(self.state))

        elif re.match(r'#[0-9a-fA-F]{6}', str(self.state)):
            self.override = value
            self._set_rgb(str(self.state))

    def clear_override(self) -> None:
        self.override = None
        if self.state:
            if self.state in self.status_map:
                self._set_state_name(self.state)

            elif self.state in self.color_map:
                self._set_color_name(self.state)

            elif re.match(r'#[0-9a-fA-F]{6}', str(self.state)):
                self._set_rgb(self.state)
