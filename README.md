# Home Assistant PiJuice Integration

Here is an integration to retrieve [PiJuice](https://github.com/PiSupply/PiJuice) values in [Home Assistant](https://home-assistant.io) sensors.


## Sensors supported
* Temperature in °C
* Charge in %


## Incoming features
* Handle other sensors :
  * Status (with event text and translations)
  * Fault events
  * Battery voltage
  * Battery current
* Support °C/°F for temperatures
* Add icons natively to sensors


## Credits
<a href="https://github.com/adamoutler/HassOSConfigurator" target="_blank">PI4 enable I2C configurator</a> : Home Assistant AddOn to easily activate I2C feature in HAOS<br>
<a href="https://pypi.org/project/smbus2/" target="_blank">smbus2</a> : PyPI library for I2C access
