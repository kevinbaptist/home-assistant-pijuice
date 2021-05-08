# Home-assistant PiJuice Integration

Here is an integration to retrive [PiJuice](https://github.com/PiSupply/PiJuice) values in [Home Assistant](https://home-assistant.io) through sensors.


## Sensors supported
* Temperature in °C
* Charge in %


## Incoming features
* Use threads to avoid latencies during update
* Handle other sensors :
  * Status (with event text and translations)
  * Fault events
  * Battery voltage
  * Battery current
* Support °C/°F for temperatures
* Add icons natively to sensors


## Credits
https://github.com/bivab/smbus-cffi
