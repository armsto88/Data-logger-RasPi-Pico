#Build Overview

This Pico-based Data Logger is a low-power, autonomous environmental monitoring system. It incorporates a Raspberry Pi Pico WH, multiple sensors, power management circuits, and data storage components to ensure efficient and reliable data collection. Below is a comprehensive breakdown of the hardware components, along with step-by-step assembly instructions.


## Hardware Components

### 1. Core Processing Unit
- **Raspberry Pi Pico WH** – Microcontroller handling data acquisition, processing, and storage.

### 2. Sensors
- **Temperature Sensors:**
  - 3 × [DS18B20](https://www.adafruit.com/product/381) (1-Wire protocol) for temperature measurements.
- **Temperature & Humidity Sensors:**
  - 3 × [SHT30](https://www.adafruit.com/product/2857) (I2C protocol) for dual temperature and humidity readings.

### 3. Data Storage
- 2 × [SD Card Breakout Boards](https://www.az-delivery.de/products/copy-of-spi-reader-micro-speicherkartenmodul-fur-arduino) – Connected via SPI for redundant data logging.

### 4. Power Management
- **[Waveshare Solar Power Manager Module](https://www.waveshare.com/solar-power-manager.htm)** – Manages solar charging and battery output.
- **14500 LiPo Battery** – Provides backup power for continuous operation.
- **[DS3231 Real-Time Clock (RTC)](https://www.amazon.de/AZDelivery-RTC-Batterie-inklusive-Arduino/dp/B01M2B7HQB)** – Controls power cycles to optimize energy consumption.

### 5. Transistors and Resistors
- **MOSFETs:**
  - P-Channel: 2 × IRF4905
  - N-Channel: 1 × IRFZ44N
- **Resistors:**
  - 2 × 4.7KΩ
  - 1 × 220KΩ
  - 1 × 1KΩ
  - 1 × 2.2KΩ
  - 1 × 100KΩ
 
  ##Step-by-Step Assesbly

  ### **Step-by-Step Assembly**  

#### **1. Setting Up the Raspberry Pi Pico WH**  

The Raspberry Pi Pico WH comes pre-soldered with headers, making it easier to connect components. However, if you are using a standard **Raspberry Pi Pico** (without pre-soldered headers), you will need to solder them manually before proceeding.  

---

### **Soldering the Headers (If Necessary)**  
If you are using a **Raspberry Pi Pico (non-WH version)** without pre-soldered headers, follow these steps:  

#### **Required Materials:**  
- **40-pin male headers** (included with most Pico kits)  
- **Soldering iron** (set to ~350°C)  
- **Solder**  
- **Breadboard** (optional but recommended)  

#### **Steps:**  
1. Insert the **male headers** into a breadboard to hold them steady.  
2. Place the **Pico board** onto the headers with the component side facing up.  
3. Heat one **corner pin** with the soldering iron and apply **a small amount of solder** to hold the header in place.  
4. Repeat for the opposite corner to keep the board level.  
5. Solder the remaining pins, ensuring a clean, shiny connection without excess solder.  
6. Inspect the joints and remove any solder bridges if necessary.  

### **Flashing MicroPython onto the Pico WH using Thonny**  

Before the Pico WH can run your data logging program, you must install **MicroPython**—a lightweight Python implementation designed for microcontrollers. Follow these steps to flash MicroPython onto your Pico WH using **Thonny IDE**:  

#### **Step 1: Download and Install Thonny**  
1. Visit [Thonny’s official website](https://thonny.org/) and download the version suitable for your operating system.  
2. Install Thonny by following the on-screen instructions.  

#### **Step 2: Connect the Pico WH in Bootloader Mode**  
1. **Hold down the BOOTSEL button** on the Pico WH.  
2. While holding the button, **connect the Pico WH to your computer** using a micro-USB cable.  
3. Release the **BOOTSEL button** once the device appears as a new storage drive named **RPI-RP2** on your computer.  

#### **Step 3: Download and Install MicroPython**  
1. Open **Thonny IDE**.  
2. Click on **"Run" → "Select Interpreter"** from the menu.  
3. In the dialog box, choose:  
   - **Interpreter**: MicroPython (Raspberry Pi Pico)  
   - **Port**: Select the COM port where the Pico is connected  
4. If MicroPython is not already installed, Thonny will prompt you to **install MicroPython firmware**.  
5. Click **"Install"** and wait for the process to complete.  

#### **Step 4: Verify MicroPython Installation**  
1. After installation, a **Python shell (REPL)** will appear at the bottom of Thonny.  
2. Type:  
   ```python
   print("Hello, Pico!")
   ```  
   and press **Enter**. If the message prints successfully, MicroPython is installed correctly.  

---





  
