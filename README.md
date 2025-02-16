# Pico Data Logger

## Summary

The Pico Data Logger is a compact and efficient environmental data logging system designed to collect and store measurements from up to six sensors. Three of these sensors communicate via the 1-Wire protocol, while the remaining three utilize an I2C bus. This configuration provides flexibility for monitoring a variety of environmental parameters dependant on the use case.

This project is designed to be a part of a system that collects abiotic environmental data in a solar farm. The unit will be collecting temperature and humidity data at different strata, both below and above ground. The intention is to use this data to predict the likelihood of various groups of animals inhabiting the area, thus enabling better support for biodiversity enhancement efforts.&#x20;

## Data Storage and Connectivity

The logger stores collected data in CSV format across two SD cards, ensuring redundancy and reliable data retention. Additionally, when WiFi connectivity is available, the system uploads the data to a Google Sheets document, enabling remote access and real-time monitoring. This feature allows users to analyze data without needing to retrieve the physical device, making it ideal for field deployments and long-term studies.

## Power Management

To optimize power efficiency and extend operational lifespan, the logger employs a power management circuit. A DS3231 real-time clock (RTC) is used to control a P-channel transistor switch, enabling the system to power on and off at predefined intervals. This significantly reduces power consumption and allows the unit to function autonomously for extended periods without user intervention.

## Battery and Solar Charging

The logger is equipped with a battery management system that supports solar charging, making it suitable for remote, off-grid applications. The solar input allows for continuous operation by replenishing the battery during daylight hours, further extending runtime and minimizing the need for manual recharging. This sustainable energy solution ensures long-term deployment with minimal maintenance, making the Pico Data Logger an excellent choice for environmental monitoring in remote locations.

## Applications

- Climate and weather monitoring
- Wildlife and habitat research
- Remote environmental sensing
- Agricultural and soil monitoring
- Water quality assessment
- Biodiversity enhancement in solar farms

## Future Enhancements

Planned improvements for future versions include enhanced wireless communication options, increased sensor compatibility, and improved data visualization features to further streamline data accessibility and analysis.

## Installation and Usage

(Instructions on setting up, installing sensors, and configuring data storage and WiFi connectivity should be added here.)

## Contributions

(Instructions on how others can contribute, report issues, or suggest improvements.)

## License

(Include details about the project's license, if applicable.)

