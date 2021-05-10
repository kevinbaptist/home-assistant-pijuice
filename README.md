# Home Assistant PiJuice Integration

Here is an integration to retrieve [PiJuice](https://github.com/PiSupply/PiJuice) values in [Home Assistant](https://home-assistant.io) sensors.

## Sensors supported
* Battery status
* Power input status
* Power input I/O status
* Temperature in °C or °F
* Charge in %
* Battery voltage
* Battery current
* I/O voltage
* I/O current

## Manual installation

1. Using the tool of your choice (SSH, Samba, ...), open the directory of ther HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory, create it.
3. Inside the `custom_components` directory, create a new folder called `pijuice`.
4. Download _all_ the files from the `custom_components/pijuice/` repository to this directory `custom_components\pijuice`.

## Example configuration.yaml

```
sensor:
  - platform: pijuice
    monitored_conditions:
      - battery_status
      - power_input_status
      - power_input_io_status
      - charge
      - temperature
      - battery_voltage
      - battery_current
      - io_voltage
      - io_current
```

## Known issues
* ...


## Credits
[Home Assistant](https://github.com/home-assistant) : Home Assistant open-source powerful domotic plateform.<br>
[PI4 enable I2C configurator](https://github.com/adamoutler/HassOSConfigurator) : Home Assistant AddOn to easily activate I2C feature in HAOS.<br>
[smbus2 library](https://pypi.org/project/smbus2) : PyPI library for I2C access
