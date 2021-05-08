"""
Support for Unifi Security Gateway Units.

For more details about this platform, please refer to the documentation at
https://github.com/custom-components/sensor.unifigateway

"""
import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    TEMP_CELSIUS,
    PERCENTAGE)

from smbus import SMBus


_LOGGER = logging.getLogger(__name__)

CONF_I2C_ADDRESS = 'i2c_address'
CONF_I2C_BUS = 'i2c_bus'

DEFAULT_NAME = 'PiJuice'
DEFAULT_I2C_ADDRESS = 0x14
DEFAULT_I2C_BUS = 1

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_TEMP = "temperature"
SENSOR_CHARGE = "charge"

SENSOR_LIST = {
    # [name, unit, index, size]
    SENSOR_CHARGE: ['Charge', PERCENTAGE, 0x41, 1],
    SENSOR_TEMP: ['Temperature', TEMP_CELSIUS, 0x47, 2]
}

POSSIBLE_MONITORED = [ SENSOR_TEMP, SENSOR_CHARGE ]
DEFAULT_MONITORED = POSSIBLE_MONITORED

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_I2C_ADDRESS, default=DEFAULT_I2C_ADDRESS): vol.Coerce(int),
    vol.Optional(CONF_I2C_BUS, default=DEFAULT_I2C_BUS): vol.Coerce(int),
    vol.Optional(CONF_MONITORED_CONDITIONS, default=DEFAULT_MONITORED):
        vol.All(cv.ensure_list, [vol.In(POSSIBLE_MONITORED)])
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the PiJuice sensor."""
    name = config.get(CONF_NAME)
    
    sensors = []
    for sensor in config.get(CONF_MONITORED_CONDITIONS):
        sensors.append(PiJuiceSensor(hass, config, name, sensor))
#        add_entities([PiJuiceSensor(hass, config, name, sensor)], True)
    
    async_add_entities(sensors, True)
    _LOGGER.info("PiJuice: Everything is setup.")


class PiJuiceSensor(Entity):
    """Implementation of PiJuice sensor."""

    def __init__(self, hass, config, name, sensor):
        """Initialize the sensor."""
        self._hass = hass
        self._client_name = name
        self._name = SENSOR_LIST[sensor][0]
        self._unit_of_measurement = SENSOR_LIST[sensor][1]
        self._index = SENSOR_LIST[sensor][2]
        self._size = SENSOR_LIST[sensor][3]
        self._sensor = sensor
        self._state = None
        self._config = config

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._client_name} {self._name}"

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement

#    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self):
        """Set up the sensor."""
        i2c_address = int(self._config.get(CONF_I2C_ADDRESS))
        i2c_bus = int(self._config.get(CONF_I2C_BUS))
        # Reading data from I2C bus
        bus = SMBus(i2c_bus)
        self._state = bus.read_byte_data(i2c_address, self._index)
        _LOGGER.info(f"PiJuice: Updated sensor '{self._name}' - new value '{self._state}'")
