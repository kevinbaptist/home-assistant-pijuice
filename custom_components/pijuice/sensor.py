""" The PiJuice component."""
import logging
import voluptuous as vol
from datetime import timedelta

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.util.temperature import celsius_to_fahrenheit
from homeassistant.const import (
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    PERCENTAGE,
    VOLT,
    ELECTRICAL_CURRENT_AMPERE)

from smbus2 import SMBus


_LOGGER = logging.getLogger(__name__)

CONF_I2C_ADDRESS = 'i2c_address'
CONF_I2C_BUS = 'i2c_bus'

DEFAULT_NAME = 'PiJuice'
DEFAULT_I2C_ADDRESS = 0x14
DEFAULT_I2C_BUS = 1

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_STATUS = "status"
SENSOR_CHARGE = "charge"
SENSOR_TEMP = "temperature"
SENSOR_BATTERY_VOLTAGE = "battery_voltage"
SENSOR_BATTERY_CURRENT = "battery_current"
SENSOR_IO_VOLTAGE = "io_voltage"
SENSOR_IO_CURRENT = "io_current"

SENSOR_LIST = {
    # [name, unit, index]
    SENSOR_STATUS: ['Status', '', 0x40, 1],
    SENSOR_CHARGE: ['Charge', PERCENTAGE, 0x41, 1],
    SENSOR_TEMP: ['Temperature', TEMP_CELSIUS, 0x47, 2],
    SENSOR_BATTERY_VOLTAGE: ['Battery voltage', VOLT, 0x49, 2],
    SENSOR_BATTERY_CURRENT: ['Battery current', ELECTRICAL_CURRENT_AMPERE, 0x4b, 2],
    SENSOR_IO_VOLTAGE: ['IO voltage', VOLT, 0x4d, 2],
    SENSOR_IO_CURRENT: ['IO current', ELECTRICAL_CURRENT_AMPERE, 0x4f, 2],
}

POSSIBLE_MONITORED = [
    SENSOR_CHARGE,
    SENSOR_STATUS,
    SENSOR_TEMP,
    SENSOR_BATTERY_VOLTAGE,
    SENSOR_BATTERY_CURRENT,
    SENSOR_IO_VOLTAGE,
    SENSOR_IO_CURRENT]
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
    SENSOR_LIST[SENSOR_TEMP][1] = hass.config.units.temperature_unit
    
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
        # Reading data from I2C bus
        i2c_address = int(self._config.get(CONF_I2C_ADDRESS))
        i2c_bus = int(self._config.get(CONF_I2C_BUS))
        bus = SMBus(i2c_bus)
        data = bus.read_i2c_block_data(i2c_address, self._index, self._size)
        
        # Scale values
        if self._sensor == SENSOR_STATUS:
            #To be separated in binary sensors
            self._state = data[0]
        elif self._sensor == SENSOR_CHARGE:
            self._state = data[0]
        elif self._sensor == SENSOR_TEMP:
            value = data[0]                     #get unsigned value
            if (data[0] & (1 << 7)):            #unsigned to signed
                value = value - (1 << 8)
            if self._unit_of_measurement == TEMP_FAHRENHEIT:
                value = round(celsius_to_fahrenheit(value), 2)
            self._state = value
        elif self._sensor == SENSOR_BATTERY_VOLTAGE or self._sensor == SENSOR_IO_VOLTAGE:
            self._state = ((data[1] << 8) | data[0]) / 1000.0
        elif self._sensor == SENSOR_BATTERY_CURRENT or self._sensor == SENSOR_BATTERY_CURRENT:
            value = (data[1] << 8) | data[0]    #assembly unsigned value
            if (value & (1 << 15)):             #unsigned to signed
                value = value - (1 << 16)
            self._state = value /1000.0
        else: #should never occurs
            self._state = 0
        
        _LOGGER.info(f"PiJuice: Updated sensor '{self._name}' - new value '{self._state}'")
