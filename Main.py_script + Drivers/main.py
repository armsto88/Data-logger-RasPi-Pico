import network
import urequests
from machine import Pin, I2C, SoftI2C, ADC, SPI
import time
import sdcard
import uos
import onewire
import ds18x20
import json
from ds3231 import DS3231, EVERY_MINUTE, EVERY_HOUR
import gc
import SHT30
import sys

# Constants
WEBHOOK_URL = "https://hook.eu1.make.com/cxyhxctngdmc1ohme35cxln7fi9s7rjm"
TCA9548A_ADDRESS = 0x71  # TCA9548A I2C address for channel selection
AT_COMMAND_DELAY = 5
R1, R2 = 1000, 2200  # Voltage divider constants

# -------------------- Error Logging Functions --------------------

def get_timestamp():
    """Return a formatted timestamp using the RTC if available, else system time."""
    try:
        _time = rtc.get_time()  # using RTC
        year, month, day, hour, minute, second, _, _ = _time
        return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
    except Exception:
        return time.strftime("%Y-%m-%d %H:%M:%S")

def log_error_to_flash(error_message, log_file="/error.log"):
    """Append an error message with a timestamp to a log file on onboard flash."""
    timestamp = get_timestamp()
    try:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - {error_message}\n")
    except Exception as e:
        # If logging fails, print to the console as a last resort.
        print("Failed to write to onboard error log:", e)
        print(f"{timestamp} - {error_message}")

def log_exception_to_flash(e, context="", log_file="/error.log"):
    """Log an exception along with its context to the onboard error log."""
    timestamp = get_timestamp()
    try:
        with open(log_file, "a") as f:
            f.write(f"{timestamp} - Exception in {context}: {e}\n")
    except Exception as log_e:
        print("Failed to write exception to onboard error log:", log_e)
        print(f"{timestamp} - Exception in {context}: {e}")

# -------------------- Hardware Initialization --------------------

# Basic hardware: LED, MOSFET gate, and ADC.
try:
    led = Pin("LED", Pin.OUT)
    mosfet_gate = Pin(16, Pin.OUT)
    adc = ADC(2)
except Exception as e:
    print(f"Error initializing basic hardware components: {e}")
    log_exception_to_flash(e, "Basic hardware init")

hardware_initialized = True

# I2C, RTC, and SHT30 initialization.
try:
    i2c_1 = SoftI2C(scl=Pin(18), sda=Pin(19))
    rtc = DS3231(i2c_1)
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    sht = SHT30.SHT30(i2c)
except Exception as e:
    print(f"Error initializing I2C/RTC/SHT30: {e}")
    log_exception_to_flash(e, "I2C/RTC/SHT30 init")
    hardware_initialized = False

# DS18B20 sensor initialization.
try:
    ds_pin = Pin(22)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
except Exception as e:
    print(f"Error initializing DS18B20 sensor: {e}")
    log_exception_to_flash(e, "DS18B20 init")
    ds_sensor = None

gc.collect()

# -------------------- Utility Functions --------------------

def connect_to_wifi():
    """Attempt to connect to WiFi and return the WLAN interface."""
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        ssid, password = 'gigacube-0F3C', '5dTQ7HA8242495T8'
        
        if not wlan.isconnected():
            wlan.connect(ssid, password)
            start_time, timeout = time.time(), 20
            while not wlan.isconnected() and time.time() - start_time < timeout:
                print(f"Attempting WiFi... {int(time.time() - start_time)}s elapsed")
                time.sleep(2)
        
        if wlan.isconnected():
            print("Connected to WiFi:", wlan.ifconfig())
        else:
            print("Failed to connect to WiFi. Offline mode enabled.")
        gc.collect()
        return wlan
    except Exception as e:
        print(f"WiFi Connection Error: {e}")
        log_exception_to_flash(e, "WiFi Connection")
        return None



def initialize_sd_card(sd_mount="/sd1", cs_pin_num=13, spi_id=1, sck_pin_num=10, mosi_pin_num=11, miso_pin_num=12):
    """Attempt to initialize an SD card and mount it at the specified mount point."""
    cs = Pin(cs_pin_num, Pin.OUT)
    baudrate = 400_000 if sd_mount == "/sd2" else 1_000_000
    spi = SPI(spi_id, baudrate=baudrate, polarity=0, phase=0, bits=8,
              firstbit=SPI.MSB, sck=Pin(sck_pin_num),
              mosi=Pin(mosi_pin_num), miso=Pin(miso_pin_num))

    try:
        uos.umount(sd_mount)
        print(f"Unmounted previous SD card on {sd_mount} (if any).")
    except Exception as e:
        if hasattr(e, 'args') and e.args and e.args[0] == 22:
            print(f"Ignoring unmount error on {sd_mount}: {e}")
        else:
            print(f"Error unmounting SD card at {sd_mount}: {e}")
            log_exception_to_flash(e, f"Unmounting SD card at {sd_mount}")

    try:
        if sd_mount == "/sd2":
            print("Toggling CS pin for /sd2 to stabilise SD card...")
            cs.value(1)
            time.sleep(0.1)
            cs.value(0)
            time.sleep(0.1)
            cs.value(1)
            time.sleep(0.1)

        sd = sdcard.SDCard(spi, cs)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, sd_mount)
        print(f"SD card initialized and mounted at {sd_mount}.")
        gc.collect()
    except Exception as e:
        print(f"Error initializing SD card at {sd_mount}: {e}")
        log_exception_to_flash(e, f"Initializing SD card at {sd_mount}")
        return None
    return sd


def initialize_first_sd_card():
    """Initialize the first SD card with retry logic."""
    for attempt in range(3):
        print(f"Attempt {attempt + 1} to initialize /sd1...")
        card = initialize_sd_card(sd_mount="/sd1", cs_pin_num=13, spi_id=1,
                                  sck_pin_num=10, mosi_pin_num=11, miso_pin_num=12)
        if card:
            return card
        time.sleep(1)
    print("Failed to initialize /sd1 after 3 attempts.")
    return None


def initialize_second_sd_card():
    """Initialize the second SD card with retry logic."""
    for attempt in range(3):
        print(f"Attempt {attempt + 1} to initialize /sd2...")
        card = initialize_sd_card(sd_mount="/sd2", cs_pin_num=1, spi_id=0,
                                  sck_pin_num=6, mosi_pin_num=7, miso_pin_num=0)
        if card:
            return card
        time.sleep(1)
    print("Failed to initialize /sd2 after 3 attempts.")
    return None

def select_channel(i2c, channel):
    """Select a specific channel on the TCA9548A multiplexer."""
    if 0 <= channel <= 7:
        try:
            i2c.writeto(TCA9548A_ADDRESS, bytearray([1 << channel]))
            print(f"Selected channel {channel}")
        except Exception as e:
            print(f"Error selecting channel {channel}: {e}")
            log_exception_to_flash(e, f"select_channel {channel}")
    else:
        raise ValueError("Invalid channel. Must be between 0 and 7.")

def read_temperature_and_humidity(sensor):
    """Read temperature and humidity from the SHT30 sensor."""
    try:
        temperature, humidity = sensor.measure()
        if temperature is None or humidity is None:
            raise ValueError("Invalid sensor readings")
        return temperature, humidity
    except Exception as e:
        print(f"Error reading SHT30 sensor: {e}")
        log_exception_to_flash(e, "read_temperature_and_humidity")
        return None, None

def log_temperature_to_sd(data_to_log, sd_directory):
    """Append temperature and voltage data as CSV to a log file on the SD card."""
    log_path = f"{sd_directory}/log.csv"
    retries = 3

    try:
        files_in_directory = uos.listdir(sd_directory)
        print(f"Files in directory {sd_directory}: {files_in_directory}")
    except OSError as e:
        print(f"Error reading directory {sd_directory}: {e}")
        log_exception_to_flash(e, f"listdir {sd_directory}")
        return



    # Create the log file with a header if it does not exist.
    if 'log.csv' not in files_in_directory:
        print(f"{log_path} not found. Creating new file.")
        try:
            with open(log_path, 'w') as file:
                file.write(
                    'Datetime,DS18B20_1 Temp,DS18B20_2 Temp,DS18B20_3 Temp,'
                    'SHT30_Channel_1 Temp,SHT30_Channel_1 Hum,'
                    'SHT30_Channel_2 Temp,SHT30_Channel_2 Hum,'
                    'SHT30_Channel_3 Temp,SHT30_Channel_3 Hum,Voltage\n'
                )
        except OSError as e:
            print(f"Error creating file {log_path}: {e}")
            log_exception_to_flash(e, f"create file {log_path}")
            return

    # Try to append the log entry.
    for attempt in range(retries):
        try:
            print(f"Appending to {log_path} (Attempt {attempt + 1}/{retries})")
            with open(log_path, 'a') as file:
                log_values = [
                    data_to_log.get('datetime', 'N/A'),
                    f"{data_to_log.get('temperature_ds1', 0):.2f}",
                    f"{data_to_log.get('temperature_ds2', 0):.2f}",
                    f"{data_to_log.get('temperature_ds3', 0):.2f}",
                    f"{data_to_log.get('shtc3_temp_1', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_1', 0):.2f}",
                    f"{data_to_log.get('shtc3_temp_2', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_2', 0):.2f}",
                    f"{data_to_log.get('shtc3_temp_3', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_3', 0):.2f}",
                    f"{data_to_log.get('voltage', 0):.2f}"
                ]
                log_entry = ",".join(log_values) + "\n"
                file.write(log_entry)
                file.flush()
            print(f"Data logged successfully to {log_path}.")
            return
        except OSError as e:
            print(f"Error writing to {log_path}: {e} (Attempt {attempt + 1}/{retries})")
            log_exception_to_flash(e, f"writing to {log_path}")
            time.sleep(0.5)
    print(f"Failed to write to {log_path} after {retries} attempts.")

def send_data_to_webhook(data_to_send):
    """Send data to the webhook endpoint."""
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(WEBHOOK_URL, json=data_to_send, headers=headers, timeout=30)
        print("Webhook response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data to webhook:", e)
        log_exception_to_flash(e, "send_data_to_webhook")

def read_battery_voltage():
    """Read battery voltage using an ADC and the voltage divider."""
    try:
        raw_value = adc.read_u16()
        voltage_out = (raw_value / 65535.0) * 3.3
        vin = voltage_out * ((R1 + R2) / R2)
        return vin
    except Exception as e:
        print(f"Error reading battery voltage: {e}")
        log_exception_to_flash(e, "read_battery_voltage")
        return None

def disconnect_wifi():
    """Disconnect WiFi to conserve power after data upload."""
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        print("WiFi disconnected.")
    else:
        print("WiFi was not connected.")

# -------------------- Main Logging Routine --------------------

def main():
    gc.collect()

    # Connect to WiFi
    wlan = connect_to_wifi()
    time.sleep(2)

    # Initialize SD cards
    initialize_first_sd_card()
    time.sleep(1)
    initialize_second_sd_card()
    time.sleep(1)

    # Set RTC alarms once on boot (can stay here)
    try:
        print("Setting RTC alarms for every 30 minutes...")
        rtc.alarm1.set(EVERY_HOUR, min=0, sec=0)
        rtc.alarm2.set(EVERY_HOUR, min=30)
    except Exception as e:
        print(f"Error setting RTC alarms: {e}")
        log_exception_to_flash(e, "Setting RTC alarms")

    # Main data logging loop
    while True:
        try:
            time.sleep(1)
            led.value(1)
            print("Collecting data...")

            # Power sensors and measure voltage
            mosfet_gate.value(1)
            time.sleep(2)
            vin = read_battery_voltage()
            if vin is not None:
                print("Voltage: {:.2f} V".format(vin))
            else:
                print("Voltage reading failed.")
            time.sleep(1)
            mosfet_gate.value(0)
            print("MOSFET OFF")

            # RTC datetime
            try:
                _time = rtc.get_time()
                year, month, day, hour, minute, second, _, _ = _time
                datetime_str = f"{day:02d}-{month:02d}-{year:04d} {hour:02d}:{minute:02d}:{second:02d}"
                print("Current datetime:", datetime_str)
            except Exception as e:
                print(f"Error parsing RTC datetime: {e}")
                log_exception_to_flash(e, "RTC datetime parsing")
                datetime_str = "N/A"

            # DS18B20
            ds_temperatures = {}
            if ds_sensor:
                try:
                    ds_sensor.convert_temp()
                    time.sleep_ms(750)
                    sensor_roms = ds_sensor.scan()
                    if sensor_roms:
                        for idx, rom in enumerate(sensor_roms):
                            ds_temperatures[f'Sensor {idx + 1}'] = ds_sensor.read_temp(rom)
                    else:
                        print("No DS18B20 sensors found.")
                except Exception as e:
                    print(f"Error reading DS18B20 sensors: {e}")
                    log_exception_to_flash(e, "DS18B20 reading")
            else:
                print("DS18B20 sensor not initialized.")

            time.sleep(1)

            # SHT30 sensors
            shtc3_data = {}
            for channel in range(3):
                select_channel(i2c, channel)
                temperature, humidity = read_temperature_and_humidity(sht)
                shtc3_data[f'shtc3_temp_{channel + 1}'] = temperature if temperature is not None else 0.0
                shtc3_data[f'shtc3_hum_{channel + 1}'] = humidity if humidity is not None else 0.0

            # Prepare payload
            data = {
                "datetime": datetime_str,
                "temperature_ds1": ds_temperatures.get('Sensor 1', 0.0),
                "temperature_ds2": ds_temperatures.get('Sensor 2', 0.0),
                "temperature_ds3": ds_temperatures.get('Sensor 3', 0.0),
                "shtc3_temp_1": shtc3_data.get('shtc3_temp_1', 0.0),
                "shtc3_hum_1": shtc3_data.get('shtc3_hum_1', 0.0),
                "shtc3_temp_2": shtc3_data.get('shtc3_temp_2', 0.0),
                "shtc3_hum_2": shtc3_data.get('shtc3_hum_2', 0.0),
                "shtc3_temp_3": shtc3_data.get('shtc3_temp_3', 0.0),
                "shtc3_hum_3": shtc3_data.get('shtc3_hum_3', 0.0),
                "voltage": vin if vin is not None else 0.0
            }

            # Save and send data
            log_temperature_to_sd(data, "/sd1")
            time.sleep(1)
            log_temperature_to_sd(data, "/sd2")
            time.sleep(1)

            if wlan and wlan.isconnected():
                send_data_to_webhook(data)
            else:
                print("No WiFi connection, skipping data upload.")

            disconnect_wifi()
            time.sleep(1)
            

            # Clear the alarms (this powers off the system)
            print("Clearing alarms and powering off...")
            rtc.alarm1.clear()
            rtc.alarm2.clear()
            print("Both alarms cleared, system powering off...")

            break
        except Exception as e:
           print(f"Error during shutdown sequence: {e}")
           log_exception_to_flash(e, "Shutdown sequence")
           break

if __name__ == "__main__":
    main()
