from assertpy import assert_that

from src.services.light_service import LightService

CONFIG = {
    "brightness": 0.1,
    "default_state": "off",
    "colors": {
        "red": [255, 0, 0],
        "orange": [255, 48, 0],
        "yellow": [255, 192, 0],
        "green": [0, 128, 0],
        "blue": [0, 0, 255],
        "purple": [128, 0, 128],
        "white": [255, 255, 255]
    },
    "statuses": {
        "away": "off",
        "berightback": "off",
        "busy": "orange",
        "donotdisturb": "red",
        "free": "green",
        "in-a-meeting": "red",
        "in-presentation": "red",
        "on-the-phone": "red"
    }
}


def test_constructor():
    service = LightService(brightness=0.5, config=CONFIG, test_mode=True)

    assert_that(service).is_not_none()
    assert_that(service.brightness).is_equal_to(0.50)
