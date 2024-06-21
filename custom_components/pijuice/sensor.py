""" The PiJuice component."""
import logging
import os
import voluptuous as vol
from datetime import timedelta

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

from homeassistant.const import (
    CONF_NAME,
    CONF_MONITORED_CONDITIONS,
    PERCENTAGE,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfTemperature,
)

from smbus2 import SMBus


_LOGGER = logging.getLogger(__name__)

DOMAIN = "pijuice"

CONF_I2C_ADDRESS = 'i2c_address'
CONF_I2C_BUS = 'i2c_bus'

DEFAULT_NAME = 'PiJuice'
DEFAULT_I2C_ADDRESS = 0x14
DEFAULT_I2C_BUS = 1

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=10)

SENSOR_BATTERY_STATUS = "battery_status"
SENSOR_POWER_STATUS = "power_input_status"
SENSOR_POWER_IO_STATUS = "power_input_io_status"
SENSOR_CHARGE = "charge"
SENSOR_TEMP = "temperature"
SENSOR_BATTERY_VOLTAGE = "battery_voltage"
SENSOR_BATTERY_CURRENT = "battery_current"
SENSOR_IO_VOLTAGE = "io_voltage"
SENSOR_IO_CURRENT = "io_current"

SENSOR_LIST = {
    # [name, device class, state class, unit, icon, index, size]
    SENSOR_BATTERY_STATUS:
        ['Battery status',        SensorDeviceClass.ENUM,        "",                           None,                         "mdi:flash",       0x40, 1],
    SENSOR_POWER_STATUS:
        ['Power input status',    SensorDeviceClass.ENUM,        "",                           None,                         "mdi:power-plug",  0x40, 1],
    SENSOR_POWER_IO_STATUS:
        ['Power input IO status', SensorDeviceClass.ENUM,        "",                           None,                         "mdi:power-plug",  0x40, 1],
    SENSOR_CHARGE:
        ['Charge',                SensorDeviceClass.BATTERY,     SensorStateClass.MEASUREMENT, PERCENTAGE,                   "mdi:battery",     0x41, 1],
    SENSOR_TEMP:
        ['Temperature',           SensorDeviceClass.TEMPERATURE, SensorStateClass.MEASUREMENT, UnitOfTemperature.CELSIUS,    "mdi:thermometer", 0x47, 2],
    SENSOR_BATTERY_VOLTAGE:
        ['Battery voltage',       SensorDeviceClass.VOLTAGE,     SensorStateClass.MEASUREMENT, UnitOfElectricPotential.VOLT, "mdi:flash",       0x49, 2],
    SENSOR_BATTERY_CURRENT:
        ['Battery current',       SensorDeviceClass.CURRENT,     SensorStateClass.MEASUREMENT, UnitOfElectricCurrent.AMPERE, "mdi:current-dc",  0x4b, 2],
    SENSOR_IO_VOLTAGE:
        ['IO voltage',            SensorDeviceClass.VOLTAGE,     SensorStateClass.MEASUREMENT, UnitOfElectricPotential.VOLT, "mdi:flash",       0x4d, 2],
    SENSOR_IO_CURRENT:
        ['IO current',            SensorDeviceClass.CURRENT,     SensorStateClass.MEASUREMENT, UnitOfElectricCurrent.AMPERE, "mdi:current-dc",  0x4f, 2],
}

BAT_STATUS_NORMAL = 'normal'
BAT_STATUS_CHARGING_FROM_IN = 'charging_from_in'
BAT_STATUS_CHARGING_FROM_5V_IO = 'charging_from_5v_io'
BAT_STATUS_NOT_PRESENT = 'not_present'

BATTERY_STATUS_LIST = [
    BAT_STATUS_NORMAL,
    BAT_STATUS_CHARGING_FROM_IN,
    BAT_STATUS_CHARGING_FROM_5V_IO,
    BAT_STATUS_NOT_PRESENT,
]

POWER_INPUT_NOT_PRESENT = 'not_present'
POWER_INPUT_BAD = 'bad'
POWER_INPUT_WEAK = 'weak'
POWER_INPUT_PRESENT = 'present'

POWER_INPUT_LIST = [
    POWER_INPUT_NOT_PRESENT,
    POWER_INPUT_BAD,
    POWER_INPUT_WEAK,
    POWER_INPUT_PRESENT,
]

POSSIBLE_MONITORED = [
    SENSOR_BATTERY_STATUS,
    SENSOR_POWER_STATUS,
    SENSOR_POWER_IO_STATUS,
    SENSOR_CHARGE,
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

    if ((os.path.exists('/dev/i2c-0') == False) and (os.path.exists('/dev/i2c-1') == False)) :
        _LOGGER.error("I2C does not exist! No sensor will be served. Please activate I2C bus in your OS.")
        return

    _LOGGER.info("PiJuice: I2C is present. Start serving sensors...")
    sensors = []
    for sensor in config.get(CONF_MONITORED_CONDITIONS):
        sensors.append(PiJuiceSensor(hass, config, name, sensor))

    async_add_entities(sensors, True)
    _LOGGER.info("PiJuice: Everything is setup.")


class PiJuiceSensor(SensorEntity):
    """Implementation of PiJuice sensor."""

    def __init__(self, hass, config, name, sensor):
        """Initialize the sensor."""
        self._hass = hass
        self._sensor = sensor
        self._config = config
        self._client_name = name
        self._attr_name = SENSOR_LIST[sensor][0]
        self._attr_device_class = SENSOR_LIST[sensor][1]
        self._attr_state_class = SENSOR_LIST[sensor][2]
        self._attr_native_unit_of_measurement = SENSOR_LIST[sensor][3]
        self._attr_icon = SENSOR_LIST[sensor][4]
        self._index = SENSOR_LIST[sensor][5]
        self._size = SENSOR_LIST[sensor][6]
        self._attr_native_value  = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._client_name} {self._attr_name}"

    @property
    def native_value(self):
        """Return the state of the device."""
        return self._attr_native_value

    @property
    def device_class(self):
        """Return the device class of the entity."""
        if self._attr_device_class != "":
            return self._attr_device_class
        else:
            return "pijuice__input"

    @property
    def native_unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._attr_native_unit_of_measurement

    @property
    def icon(self):
        """Return the icon of the sensor."""
        if self._sensor == SENSOR_BATTERY_STATUS:
            if self._attr_native_value == BAT_STATUS_NORMAL:
                return "mdi:battery"
            elif self._attr_native_value == BAT_STATUS_CHARGING_FROM_IN or self._attr_native_value == BAT_STATUS_CHARGING_FROM_5V_IO:
                return "mdi:battery-charging"
            elif self._attr_native_value == BAT_STATUS_NOT_PRESENT:
                return "mdi:battery-off"
        elif self._sensor == SENSOR_POWER_STATUS or self._sensor == SENSOR_POWER_IO_STATUS:
            if self._attr_native_value == POWER_INPUT_NOT_PRESENT:
                return "mdi:power-plug-off-outline"
            elif self._attr_native_value == POWER_INPUT_BAD or self._attr_native_value == POWER_INPUT_WEAK:
                return "mdi:power-plug-outline"
            elif self._attr_native_value == POWER_INPUT_PRESENT:
                return "mdi:power-plug"
        elif self._sensor == SENSOR_CHARGE:
            if self._attr_native_value > 90:
                return "mdi:battery"
            elif self._attr_native_value > 70:
                return "mdi:battery-80"
            elif self._attr_native_value > 50:
                return "mdi:battery-60"
            elif self._attr_native_value > 30:
                return "mdi:battery-40"
            else:
                return "mdi:battery-20"
        return self._attr_icon

    async def async_update(self):
        """Set up the sensor."""
        # Reading data from I2C bus
        i2c_address = int(self._config.get(CONF_I2C_ADDRESS))
        i2c_bus = int(self._config.get(CONF_I2C_BUS))

        try:
            with SMBus(i2c_bus) as bus:
                data = bus.read_i2c_block_data(i2c_address, self._index, self._size)

            # Scale red values
            if self._sensor == SENSOR_BATTERY_STATUS:
                self._attr_native_value = BATTERY_STATUS_LIST[(data[0] >> 2) & 0x03]
            elif self._sensor == SENSOR_POWER_STATUS:
                self._attr_native_value = POWER_INPUT_LIST[(data[0] >> 4) & 0x03]
            elif self._sensor == SENSOR_POWER_IO_STATUS:
                self._attr_native_value = POWER_INPUT_LIST[(data[0] >> 6) & 0x03]
            elif self._sensor == SENSOR_CHARGE:
                self._attr_native_value = data[0]
            elif self._sensor == SENSOR_TEMP:
                value = data[0]                     #get unsigned value
                if (data[0] & (1 << 7)):            #unsigned to signed
                    value = value - (1 << 8)
                self._attr_native_value = value
            elif self._sensor == SENSOR_BATTERY_VOLTAGE or self._sensor == SENSOR_IO_VOLTAGE:
                self._attr_native_value = ((data[1] << 8) | data[0]) / 1000.0
            elif self._sensor == SENSOR_BATTERY_CURRENT or self._sensor == SENSOR_IO_CURRENT:
                value = (data[1] << 8) | data[0]    #assembly unsigned value
                if (value & (1 << 15)):             #unsigned to signed
                    value = value - (1 << 16)
                self._attr_native_value = value /1000.0
            else: #should never occurs
                self._attr_native_value = data[0]

            _LOGGER.debug(f"PiJuice: Updated sensor '{self._attr_name}' - new value '{self._attr_native_value}'")
        # Error while reading on I2C bus
        except Exception as error:
            _LOGGER.warn(f"PiJuice: Error while retrieving data for sensor '{self._attr_name}' (Error code: '{error}')")
            pass


