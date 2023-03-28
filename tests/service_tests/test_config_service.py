from assertpy import assert_that

from src.services.config_service import ConfigService

CONFIG_FILE = 'test/config.json'

def test_rgb_hex_to_dec():
    """
    Tests rgb_hex_to_dex() with some valid values.
    """
    assert_that(ConfigService.rgb_hex_to_dec('#000000')) \
        .is_equal_to((0, 0, 0))
    
    assert_that(ConfigService.rgb_hex_to_dec('#ff0000')) \
        .is_equal_to((255, 0, 0))
    
    assert_that(ConfigService.rgb_hex_to_dec('#00ff00')) \
        .is_equal_to((0, 255, 0))
    
    assert_that(ConfigService.rgb_hex_to_dec('#0000ff')) \
        .is_equal_to((0, 0, 255))
    
    assert_that(ConfigService.rgb_hex_to_dec('#123456')) \
        .is_equal_to((18, 52, 86))

    assert_that(ConfigService.rgb_hex_to_dec('#B4D123')) \
        .is_equal_to((180, 209, 35))

def test_rgb_hex_to_dec_bad_values():
    """
    Tests rgb_hex_to_dex() with some bad values. Each should raise the appropriate exception.
    """
    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(ValueError) \
        .when_called_with('Chicken')
    
    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(ValueError) \
        .when_called_with('#1234567890')

    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(ValueError) \
        .when_called_with('#NOTHEX')
    
    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(ValueError) \
        .when_called_with('B4D123')

    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(ValueError) \
        .when_called_with('123456')

    assert_that(ConfigService.rgb_hex_to_dec) \
        .raises(TypeError) \
        .when_called_with(123456)

def test_config_service():
    """
    Tests the ConfigService() constructior.
    """

    service = ConfigService(CONFIG_FILE)

    assert_that(service.default_state) \
        .is_equal_to('busy')
    
    assert_that(service.color_map['orange']) \
        .is_equal_to('#ff3000')
