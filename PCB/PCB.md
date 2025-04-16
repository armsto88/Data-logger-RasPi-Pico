# PCB Overview

As part of the development of Enviro Logger (Prototype 2), this document outlines the intention to design and build a custom printed circuit board (PCB) that replaces the various breakout board components used in Prototype 1.

Prototype 1 utilised a modular hardware approach using multiple breakout boards to manage power, data storage, sensor input, and communication. While ideal for prototyping and functional testing, this method introduced unnecessary complexity in wiring, increased the size of the unit, and presented durability challenges for long-term, field-based environmental monitoring.

The aim of the PCB design is to consolidate these components into a single, compact, and robust board optimised for real-world deployment. This will improve reliability, simplify assembly, and reduce the chances of connection failure due to vibration, moisture, or prolonged use in outdoor environments.

###Schematic of the PCB design
![Schematic of the PCB design](PCB_images/schematic.svg)

The new PCB will integrate:
- A microcontroller (Raspberry Pi Pico)
- Data storage via 2 × SD card interface
- 1-Wire and I2C sensor support
- RTC-based power scheduling
- Modular ports for external sensor connectivity

This document will be updated as the schematic is finalised, the board is laid out, and testing begins. Fabrication files and assembly instructions will also be provided to support replication and contribution.

---

