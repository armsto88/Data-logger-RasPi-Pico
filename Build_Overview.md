# 🛠️ Build Overview

---

This Pico-based Data Logger is a low-power, autonomous environmental monitoring system. It features a Raspberry Pi Pico WH alongside multiple sensors, power management circuits, and data storage components to ensure efficient and reliable data collection. Below is a comprehensive breakdown of the hardware components, followed by step-by-step assembly instructions.

---

## Hardware Components

### 1. Core Processing Unit
- **Raspberry Pi Pico WH** – Handles data acquisition, processing, and storage.

### 2. Sensors
- **Temperature Sensors:**
  - 3 × DS18B20 (1-Wire protocol) for temperature measurements.
- **Temperature & Humidity Sensors:**
  - 3 × SHT30 (I2C protocol) for dual temperature and humidity readings.

### 3. Data Storage
- 2 × SD Card Breakout Boards – Connected via SPI for data storage.

### 4. Power Management
- **Waveshare Solar Power Manager Module** – Manages solar charging and battery output.
- **14500 LiPo Battery** – Provides backup power for continuous operation.
- **DS3231 Real-Time Clock (RTC)** – Controls power cycles to optimize energy consumption.

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

### 6. Additional Components
- **PCA9546A I2C Multiplexer** – Expands the I2C bus for multiple sensors.
- **Adafruit Proto Underplate** – A prototyping board for mounting and connecting components.
- **Jumper Wires** – For flexible connections.
- **Perf-board** – 6 × 4 cm prototyping board.
- **Waterproof Housing** – [Amazon Link](https://www.amazon.de/-/en/dp/B0D4V6SBXM?ref=ppx_yo2ov_dt_b_fed_asin_title)
- **RJ45 Patch Cables** – [Amazon Link](https://www.amazon.de/-/en/dp/B0797SCT55?ref=ppx_yo2ov_dt_b_fed_asin_title)
- **RJ45 Waterproof Couplings** – [Amazon Link](https://www.amazon.de/-/en/dp/B0CRZ3MTG8?ref=ppx_yo2ov_dt_b_fed_asin_title)

---

## Step-by-Step Assembly

### 1. Setting Up the Raspberry Pi Pico WH

The Raspberry Pi Pico WH comes pre-soldered with headers, making it easier to connect components. However, if you are using a standard **Raspberry Pi Pico** (without pre-soldered headers), you will need to solder them manually before proceeding.

#### Soldering the Headers (If Necessary)

**Required Materials:**
- 40-pin male headers (included with most Pico kits)
- Soldering iron (set to ~350°C or a fixed-temperature iron over 40W)
- Solder
- Breadboard (optional but recommended)

**Steps:**
1. Insert the male headers into a breadboard to hold them steady.
2. Place the Pico board onto the headers with the component side facing up.
3. Heat one corner pin and apply a small amount of solder to hold the header in place.
4. Repeat for the opposite corner to level the board.
5. Solder the remaining pins.
6. Inspect the joints and remove any solder bridges if necessary.

---

### Flashing MicroPython onto the Pico WH using Thonny

Before the Pico WH can run your data logging program, install **MicroPython**.

#### Step 1: Download and Install Thonny
- Visit [Thonny’s official website](https://thonny.org/) and download the appropriate version.
- Install Thonny by following the on-screen instructions.

#### Step 2: Connect the Pico WH in Bootloader Mode
1. Hold down the **BOOTSEL button**.
2. While holding the button, connect the Pico WH to your computer via USB.
3. Release the BOOTSEL button once a drive named **RPI-RP2** appears.

#### Step 3: Install MicroPython
1. Open Thonny.
2. Go to **Run → Select Interpreter**.
3. Select:
   - Interpreter: **MicroPython (Raspberry Pi Pico)**
   - Port: The one where the Pico is connected.
4. If prompted, click **Install** to install MicroPython firmware.

#### Step 4: Test the Installation
In the Python shell (REPL) at the bottom of Thonny, type:


#### **Step 4: Verify MicroPython Installation**
1. After installation, a **Python shell (REPL)** will appear at the bottom of Thonny.
2. Type:
   ```python
   print("Hello, Pico!")
   ```  
   and press **Enter**. If the message prints successfully, MicroPython is installed correctly.

---

### **2. Modifications to the DS3231**

Articles I have read, including this [blog](https://thecavepearlproject.org/2014/05/21/using-a-cheap-3-ds3231-rtc-at24c32-eeprom-from-ebay/), highlight the need for modifications to the DS3231 to ensure proper functionality when using its alarm as a trigger for the P-channel MOSFET.

The DS3231 includes pull-up resistors on the SQW (alarm) line, which must be removed. However, these resistors are part of a resistor block that also contains the necessary I2C lines (SCL, SDA). To compensate for their removal, external 4.7KΩ pull-up resistors must be reintroduced into the circuit to maintain proper operation. This modification provides greater control over the pull-up resistance for the SQW (alarm) line, ensuring reliable triggering.

The other necessary modification is the removal of the charging circuit for the coin battery. The same [blog](https://thecavepearlproject.org/2014/05/21/using-a-cheap-3-ds3231-rtc-at24c32-eeprom-from-ebay/) mentioned earlier, along with other sources, recommends disabling this feature for safety reasons.

To achieve this, the charging resistor can be removed.

The image below highlights both resistors that should be removed. Applying heat and gentle pressure will quickly dislodge them. However, be careful not to apply excessive force, as this could damage the DS3231 or cause injury.

![DS3231 Modifications](Build_images/ds3231_RTC.jpg)

---

### **3. Making the Auto-Power Off and Voltage Indicator Circuits**

The auto power-off and voltage measurement circuit was built on a 6 × 4 cm section of double-sided perfboard. Before transitioning to the more permanent perfboard, the circuit was first assembled and tested on a breadboard.

All soldering was done on the underside at a temperature of 350 °C. The resistors used in the voltage divider were 1 kΩ and 2.2 kΩ. External pull-ups for the RTC were 4.7 kΩ, while the pull-ups for the transistor in the voltage divider were 100 kΩ, and for the auto power-off, 220 kΩ.

The voltage divider was powered directly from the battery, with leads soldered to the positive and negative terminals. This approach was necessary because the main output of the Waveshare power unit is boosted to 5V.

Below are some images to assist in its reconstruction. I plan to make this into a PCB hat for the Pico in the future.

![Auto-off Circuit 1](Build_images/auto_off_1.jpg)  
![Auto-off Circuit 2](Build_images/auto_off_2.jpg)  
![Auto-off Circuit 3](Build_images/auto_off_3.jpg)

---

### **4. Preparing the Waterproof Housing**

I decided to use **RJ45 couplers** ([link](https://www.amazon.de/dp/B0CRZ3MTG8?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1)) to connect the sensors through the waterproof case. This choice was mainly driven by cost. While there are likely more robust and better-form-factor waterproof through couplers available, these were much more affordable at the time.

I drilled **23mm holes** using a **Forstner drill bit** ([link](https://www.amazon.de/-/en/dp/B0BQ7CHXVP?ref=ppx_yo2ov_dt_b_fed_asin_title)) through the bottom of the case. Care must be taken when measuring the holes, as there is little tolerance. I ensured that the long side of the coupler was oriented on the outside of the box to provide more space for cabling later on.

A waterproof gland also needs to be added to the right side of the case for the solar input. I installed this after mounting the hardware and positioning it inside the case to ensure proper placement. I used a [PG7 Waterproof Gland](https://www.amazon.de/-/en/PUWOWYE-PG13-5-Connection-Waterproof-Feed-Through/dp/B0D838PL5S) for this purpose.

---

### **5. Preparing the Sensors**

Using RJ45 couplers required modifying the ends of each sensor to allow them to connect properly. To achieve this, I purchased some short [Cat7 patch cables](https://www.amazon.de/dp/B0797SCT55?ref=ppx_yo2ov_dt_b_fed_asin_title&th=1). I cut a 10 cm length, removed the shielding to expose the four wire pairs, then stripped and twisted the pairs together.

For the temperature sensors, which have three wires, one pair could be discarded. The connector and the sensor wire were then soldered together and insulated. The humidity/temperature sensors, however, use a digital protocol that requires four wires, meaning all pairs from the Cat7 cable are needed.

**Be sure to note where each wire is connected to the RJ45 plug, as you'll need to replicate this inside the box and route each wire correctly to the Pico.**

I chose to merge the three wires from each temperature sensor inside the case before routing them to the Pico. Since they use the digital "1-wire" protocol, this connection needed to be made somewhere, and doing it inside the case kept the wiring clean.

This involved soldering all power wires together, all ground wires together, and all signal wires together using three pairs from another set of RJ45 connectors. Three wires (Power, Ground, and Signal) then emerged from the connectors and were routed to the Pico.

The humidity/temperature sensors, which use the I2C protocol, needed to pass through a multiplexer since they all shared the same digital address. The multiplexer I used had four STEMMA QT connectors as inputs, so I soldered these to the ends of each RJ45 connector inside the box.

The output of the multiplexer (another STEMMA QT) was then routed into the provided input on the proto underplate, reducing cable clutter and avoiding the need for an additional four wires running directly into the Pico's GPIOs.

![Connectors](Build_images/RJ45_connectors.jpg)

---

### **6. Connecting the Hardware**

My plan was to design a plate that sits atop the Waveshare power manager, providing a mounting surface for both SD card readers and the proto underplate with the Pico on top. The auto power-off circuit is mounted directly onto a backing plate that spans the width of the case.

Files for printing both mounting plates can be found in the repository:

- **[Base plate](3D_prints/base_plate-Body.stl)**
- **[Small mounting plate](3D_prints/top_plate_v21-Body.stl)**

*Note: The prints may require some re-drilling and adjustments to align the holes properly.*

![Hardware Mounting](Build_images/hardware_3.jpg)

---

### **7. Bringing It All Together**

![Breadboard View](Build_images/data_logger_P1_1.png)  
![Schematic View](Build_images/data_logger_P1_schem.png)

---

![Final Build](Build_images/complete_2.jpg)






  
