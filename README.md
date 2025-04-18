# 🌱 Enviro Logger – Prototype 1

## Overview

The **Enviro Logger** is an environmental data logging system designed to collect and store abiotic data using up to six sensors.  
- **Three** sensors communicate via the **1-Wire** protocol  
- **Three** sensors communicate via the **I2C** bus  

This versatile configuration supports a wide range of environmental monitoring needs.

The system is part of a broader project aimed at **monitoring microclimates within solar farms**. By capturing temperature and humidity data across different strata—**above and below ground**—the project aims to predict the likelihood of various animal groups inhabiting the site, thereby contributing to **biodiversity enhancement** efforts.

---

## 💾 Data Storage & Connectivity

- Data is saved in **CSV format** across **two SD cards** for redundancy and reliability.  
- When **WiFi** is available, the logger uploads data to a **Google Sheets document** for real-time remote monitoring and analysis.  

This remote access minimizes the need to retrieve physical devices—ideal for **long-term field deployments**.

---

## 🔋 Power Management

An **automatic power-off circuit** ensures energy efficiency:

- A **DS3231 Real-Time Clock (RTC)** controls a **P-channel MOSFET switch**  
- The system powers on and off at **predefined intervals**  
- Greatly reduces power consumption for **autonomous operation**

---

## ☀️ Battery & Solar Charging

- Features a **battery management system with solar charging support**
- Ensures **continuous operation** by recharging during daylight hours
- Ideal for **remote and off-grid environments**

This renewable energy setup allows for **long-term deployment with minimal maintenance**.

---

## 🚀 Future Enhancements

Planned improvements for upcoming versions:

- Enhanced wireless communication (e.g. LoRa, LTE)
- Expanded sensor compatibility


---

## 🔧 Build Overview

📄 [Build Overview](Build_Overview.md)

---

## 💰 Cost Breakdown

| Component                                | Qty | Unit Price (€) | Total (€) |
|------------------------------------------|-----|----------------|-----------|
| **Raspberry Pi Pico WH**                 | 1   | 7.20           | 7.20      |
| **Waveshare Solar Management Module**    | 1   | 15.95          | 15.95     |
| **14500 LiPo Battery**                   | 1   | 6.00           | 6.00      |
| **SD Card Breakout Board**               | 2   | 3.00           | 6.00      |
| **DS18B20 Temperature Sensors**          | 3   | 2.95           | 8.85      |
| **SHT30 Sensors**                        | 3   | 6.00           | 18.00     |
| **IRF4905 P-Channel MOSFETs**            | 2   | 1.50           | 3.00      |
| **IRFZ44N N-Channel MOSFET**             | 1   | 1.50           | 1.50      |
| **Resistors**                            |     |                |           |
| - 4.7KΩ                                  | 2   | 0.05           | 0.10      |
| - 220KΩ                                  | 1   | 0.05           | 0.05      |
| - 1KΩ                                    | 1   | 0.05           | 0.05      |
| - 2.2KΩ                                  | 1   | 0.05           | 0.05      |
| - 100KΩ                                  | 1   | 0.05           | 0.05      |
| **PCA9546A I2C Multiplexer**             | 1   | 11.00          | 11.00     |
| **Adafruit Proto Underplate**            | 1   | 6.00           | 6.00      |
| **Waterproof Housing**                   | 1   | 15.00          | 15.00     |
| **RJ45 Couplers**                        | 6   | 4.33           | 26.00     |
| **RJ45 Patch Cables**                    | 6   | 1.50           | 9.00      |
| **USB Couplers**                         | 1   | 6.00           | 6.00      |
| **🧮 Total Estimated Cost**              |     |                | **141.90** |

---

## 🧪 Testing

🔋 [Battery Test #1 – "Voltage Profile"](Testing/Test_1/Battery_test.md)

---

# 🌿 Enviro Logger – Prototype 2

## 🔌 PCB Schematic & Design

📘 [PCB Overview](PCB/PCB.md)

---

## 🤝 Contributions

_Interested in contributing?_  
Please open an issue or submit a pull request to suggest improvements, report bugs, or share ideas for future development.

---

## 📄 License

(Include your license type here, e.g. MIT, GPLv3, etc.)

---

