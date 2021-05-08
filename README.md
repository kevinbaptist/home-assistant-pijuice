# Home Assistant PiJuice Integration

Here is an integration to retrieve [PiJuice](https://github.com/PiSupply/PiJuice) values in [Home Assistant](https://home-assistant.io) sensors.


## Sensors supported
* Temperature in °C
* Charge in %


## Incoming features
* Handle other sensors :
  * Status (binary sensors with texts)
  * Battery voltage
  * Battery current
* Support °C/°F for temperatures
* Add icons natively to sensors


## Credits
[PI4 enable I2C configurator](https://github.com/adamoutler/HassOSConfigurator) : Home Assistant AddOn to easily activate I2C feature in HAOS<br>
[smbus2 library](https://pypi.org/project/smbus2) : PyPI library for I2C access
