
# Data Logger (Raspberry Pi - Pico)

# Overview

This Data Logger is an environmental data logging system designed to collect and store measurements from up to six sensors. Three of these sensors communicate via the 1-Wire protocol, while the remaining three utilize an I2C bus. This configuration provides flexibility for monitoring a variety of environmental parameters depending on the use case.

This project is designed to be part of a monitoring system that collects abiotic environmental data within a solar farm. The unit will collect temperature and humidity data at different strata, both below and above ground. The goal is to use this data to predict the likelihood of various animal groups inhabiting the area, thereby supporting biodiversity enhancement efforts.

## Data Storage and Connectivity

The logger stores collected data in CSV format across two SD cards, ensuring redundancy and reliable data retention. Additionally, when WiFi connectivity is available, the system uploads the data to a Google Sheets document, enabling remote access and real-time monitoring. This feature allows users to analyze data without needing to retrieve the physical device, making it ideal for field deployments and long-term studies.

## Power Management

To optimize power efficiency and extend operational lifespan, the logger employs an automatic power-off circuit. A DS3231 real-time clock (RTC) controls a P-channel transistor switch, enabling the system to power on and off at predefined intervals. This significantly reduces power consumption and allows the unit to function autonomously for extended periods without user intervention.

## Battery and Solar Charging

The logger is equipped with a battery management system that supports solar charging, making it suitable for remote, off-grid applications. The solar input allows for continuous operation by replenishing the battery during daylight hours, further extending runtime and minimizing the need for manual recharging. This sustainable energy solution ensures long-term deployment with minimal maintenance.

## Future Enhancements

Planned improvements for future versions include enhanced wireless communication options, increased sensor compatibility, and improved data visualization features to further streamline data accessibility and analysis.

# Build Overview

(Instructions on setting up, installing sensors, and configuring data storage and WiFi connectivity should be added here.)

## Contributions

(Instructions on how others can contribute, report issues, or suggest improvements.)

## License

(Include details about the project's license, if applicable.)

---

This version improves grammar, structure, and clarity while keeping your original meaning intact. Let me know if you'd like any additional refinements!
