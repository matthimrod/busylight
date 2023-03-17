from assertpy import assert_that

from src.services.light_service import LightService

CONFIG = {
    "brightness": 0.1,
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
    service = LightService(test_mode=True)

    assert_that(service).is_not_none()
    assert_that(service.brightness).is_equal_to(1.0)
    assert_that(service.state).is_none()
    assert_that(service._colorRed).is_equal_to(0)
    assert_that(service._colorGreen).is_equal_to(0)
    assert_that(service._colorBlue).is_equal_to(0)


def test_constructor_with_parameters():
    service = LightService(brightness=0.5, config=CONFIG, init_status='busy', test_mode=True)

    assert_that(service).is_not_none()
    assert_that(service.brightness).is_equal_to(0.5)
    assert_that(service._colorRed).is_equal_to(255)
    assert_that(service._colorGreen).is_equal_to(48)
    assert_that(service._colorBlue).is_equal_to(0)
    assert_that(service.state).is_equal_to('busy')


def test__update():
    service = LightService(test_mode=True)

    service._update(1, 2, 3)

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(1)
    assert_that(service._colorGreen).is_equal_to(2)
    assert_that(service._colorBlue).is_equal_to(3)

def test__update_out_of_range():
    service = LightService(test_mode=True)

    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(-1, 1, 1)

    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(1, -1, 1)

    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(1, 1, -1)
    
    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(300, 1, 1)

    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(1, 260, 1)

    assert_that(service._update) \
        .raises(ValueError) \
        .when_called_with(1, 1, 9876)


def test__set_rgb():
    service = LightService(test_mode=True)

    service._set_rgb('#010203')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(1)
    assert_that(service._colorGreen).is_equal_to(2)
    assert_that(service._colorBlue).is_equal_to(3)


def test__set_rgb_string():
    service = LightService(test_mode=True)

    assert_that(service._set_rgb) \
        .raises(ValueError) \
        .when_called_with("Chicken")

    assert_that(service._set_rgb) \
        .raises(ValueError) \
        .when_called_with("#badc0ffee")

    assert_that(service._set_rgb) \
        .raises(ValueError) \
        .when_called_with("#zzzzzz")


def test__set_color_name_list():
    service = LightService(config={"colors": {"red": [255, 0, 0]}}, test_mode=True)
    service._set_color_name('red')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(255)
    assert_that(service._colorGreen).is_equal_to(0)
    assert_that(service._colorBlue).is_equal_to(0)


def test__set_color_name_rgb():
    service = LightService(config={"colors": {"red": "#ff0000"}}, test_mode=True)
    service._set_color_name('red')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(255)
    assert_that(service._colorGreen).is_equal_to(0)
    assert_that(service._colorBlue).is_equal_to(0)


def test__set_state_name_list():
    service = LightService(config={"statuses": {"busy": [0, 255, 0]}}, test_mode=True)
    service._set_state_name('busy')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(0)
    assert_that(service._colorGreen).is_equal_to(255)
    assert_that(service._colorBlue).is_equal_to(0)


def test__set_state_name_rgb():
    service = LightService(config={"statuses": {"busy": "#00ff00"}}, test_mode=True)
    service._set_state_name('busy')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(0)
    assert_that(service._colorGreen).is_equal_to(255)
    assert_that(service._colorBlue).is_equal_to(0)


def test__set_state_name_colorname():
    service = LightService(config={"colors": {"blue": "#0000ff"},"statuses": {"busy": "blue"}}, test_mode=True)
    service._set_state_name('busy')

    assert_that(service).is_not_none()
    assert_that(service._colorRed).is_equal_to(0)
    assert_that(service._colorGreen).is_equal_to(0)
    assert_that(service._colorBlue).is_equal_to(255)


