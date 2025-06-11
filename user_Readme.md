# 🌿  Data Logger – Quick Start Guide

Welcome to your custom-built solar-powered data logger! This guide will walk you through setting up and testing the device.

---

## 🛠 Step 1 – Install Thonny IDE

Download and install **Thonny**, a beginner-friendly Python editor:

- **Windows**: [Download Installer](https://thonny.org)
- **macOS**: [Download Installer](https://thonny.org)

> Thonny includes Python and is perfect for working with MicroPython on Raspberry Pi Pico.

---

## 🔌 Step 2 – Connect the Logger to Your Computer

1. Plug the **micro-USB** end into the **Raspberry Pi Pico** on the logger.
2. Plug the **USB-A** end into your **computer**.
3. Open **Thonny IDE**.

### Setup Thonny to Recognise the Pico:

- Go to `Tools` → `Options…` → **Interpreter**
- Set **Interpreter** to `MicroPython (Raspberry Pi Pico)`
- Set **Port** to:
  - `COMx` (Windows)
  - `/dev/tty.usbmodem...` (macOS)

Click **OK**. You should see a `>>>` prompt in the Shell.

---

## ⏱️ Step 3 – Power On & Set the Logger’s Real-Time Clock (RTC)

### Power On the Device

- The **power switch** is on the **battery module underneath** the unit (not on the PCB).
- You **can’t see** the switch—feel for it near the **bottom-left edge**.
- Slide it to the **right** to turn on.

> 💡 It’s a snug fit—use your pinky finger. (It’s a design flaw 😅)

- A **green LED** on the PCB will light up to confirm it’s powered on.

### Set the Time

1. In Thonny, open `setting_time_ds3231.py` from the file pane.
2. Click the **Run** button (green triangle, top-left).
3. The logger’s clock will sync to your PC's system time.

---

## 🌱 Step 4 – Connect Sensors & Open Main Script

### Connect the Sensors

- Match each **sensor label** to the correct **port label** on the box.
- Plug in all sensors **before running the script**.

> Plugging sensors in later or in the wrong order will mislabel data.

### Open the Main Script

1. In Thonny, open `main.py` from the left-hand file pane.

---
## 🌐 Step 5 – Update WiFi Credentials (Optional Testing)

Scroll to **line 95** in `main.py`. You’ll see:

```python
ssid, password = 'gigacube-0F3C', '5dTQ7HA8242495T8'
```

Replace this with your own WiFi details. For example:

```python
ssid, password = 'YourWiFiName', 'YourWiFiPassword'
```

> 🔒 **Note**: WiFi is only used to send test data to Google Sheets. The logger still saves data to SD cards even if no WiFi is configured.

Be sure to **save the file** before continuing.

---

## 📊 Step 6 – Run the Logger and View Live Test Data

Open the live data sheet in your browser:  
[📄 Google Sheet – Live Data](https://docs.google.com/spreadsheets/d/1Fp3gE0CN5dDJawXwoVpkiC7PFwAjhU7pCCHq3XwCfAo/edit?usp=sharing)

### ▶️ To Run the Logger:

1. With `main.py` open in Thonny, click the **green Run button** (top-left).
2. The logger will:
   - Connect to WiFi 
   - Take a set of sensor readings
   - Upload to the Google Sheet

> ⏱ It will repeat this process **every 30 minutes** until powered off or the battery is depleted.

---

## 📴 Step 7 – Powering Off the Logger

To turn off the device:

- Use the **same switch** on the **battery module** (feel underneath the unit).
- Slide it to the **left** to completely power down the logger.

> ⚠️ **Important:** This cuts **all power**, including **solar charging**.  
> To allow the solar panel to continue charging the battery, leave the device **switched on**, even when not actively logging.

---

## 💡 Tips & Important Notes

### 🔌 Sensor Setup

- Plug all sensors into the **correct ports** **before running `main.py`**.
- The script assumes a specific order—incorrect or delayed connections will result in **mislabelled data** in both the SD card and Google Sheet.

---

### 💾 SD Cards

- The logger includes **two SD cards** for redundancy.
- The SD slots are **a little awkward to access** due to their design.
- With a bit of familiarity, inserting and removing the cards becomes easier.

---

### ☀️ Solar Charging

- The logger is designed for **continuous operation** using solar power.
- It doesn’t require full sun—**cloudy days usually provide a net-positive charge**.
- However, **unobstructed sky access** gives best performance (as tested).
- The solar panel cable can be **easily extended** with standard 2-wire joins if needed.

---

✅ You're all set!

For questions or troubleshooting, feel free to reach out any time.
thomasgarmstrong88@gmail.com

