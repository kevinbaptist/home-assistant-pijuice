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
To make the Pi Juice Hat accessible and the integration working, this is required that I2C is enabled in th host system.<br>
- If you use Home Assistant Operating System, follow the official documentation : https://www.home-assistant.io/common-tasks/os/#enable-i2c<br>
- If you use Docker or Core version of Home Assistant, activate I2C depending on your host OS.

## HACS installation (Easy mode)
Use [HACS](https://hacs.xyz/). This will also inform you when there are new releases and you can update easily. If installed this way, you can proceed to configuration either using the Integrations Page or Configuration.yaml (legacy).<br>
If you are not familiar with HACS, please check the [usage](https://hacs.xyz/docs/basic/getting_started).

## Manual installation 
1. Using the tool of your choice (SSH, Samba, ...), open the directory of ther HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory, create it.
3. Inside the `custom_components` directory, create a new folder called `pijuice`.
4. Download _all_ the files from the `custom_components/pijuice/` repository to this directory `custom_components\pijuice`.

## Example configuration.yaml
Whatever the installation of this integration used, you need to activate the integration to your configuration file (using share folder or addon to access to it).<br>
Here is a complete configuration with all entities activated :
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
[PiJuice](https://pi-supply.com/) : PiJuice Pi supply hardware/software platform to support Raspberry Pi, Arduino, ...<br>
[Home Assistant](https://github.com/home-assistant) : Home Assistant open-source powerful domotic plateform.<br>
[HACS](https://hacs.xyz/) : Home Assistant Community Store gives you a powerful UI to handle downloads of all your custom needs.<br>
[smbus2 library](https://pypi.org/project/smbus2) : PyPI library for I2C access
