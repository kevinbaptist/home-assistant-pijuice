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
Home Assistant AddOn to easily activate I2C feature in HAOS : https://github.com/adamoutler/HassOSConfigurator<br>
PyPI library for I2C access : https://github.com/bivab/smbus-cffi
