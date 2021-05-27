# Home Assistant PiJuice Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs) [![version](https://img.shields.io/github/v/release/Racailloux/home-assistant-pijuice)](https://github.com/Racailloux/home-assistant-pijuice/releases)


Here is an integration to retrieve [PiJuice](https://github.com/PiSupply/PiJuice) values in [Home Assistant](https://home-assistant.io) sensors.

## Sensors supported
* Battery status
* Power input status
* Power input I/O status
* Charge in %
* Temperature in °C or °F
* Battery voltage
* Battery current
* I/O voltage
* I/O current

## Prerequisite
To make the Pi Juice working, this is required that I2C is activated in the system. Follow the [official guide](https://www.home-assistant.io/common-tasks/os/#enable-i2c) or use an addon to do this : 
[PI4 enable I2C configurator](https://github.com/adamoutler/HassOSConfigurator).

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
If no "monitored_conditions" is setup, all sensors will be added to Home Assistant as Entities.

## Credits
[Home Assistant](https://github.com/home-assistant) : Home Assistant open-source powerful domotic plateform.<br>
[PI4 enable I2C configurator](https://github.com/adamoutler/HassOSConfigurator) : Home Assistant AddOn to easily activate I2C feature in HAOS.<br>
[smbus2 library](https://pypi.org/project/smbus2) : PyPI library for I2C access
