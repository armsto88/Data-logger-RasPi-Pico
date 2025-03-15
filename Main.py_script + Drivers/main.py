import network
import urequests
from machine import Pin, I2C, SoftI2C, ADC
import time
import sdcard
import uos
import onewire
import ds18x20
import json
from ds3231 import DS3231, EVERY_MINUTE, EVERY_HOUR
import gc
import SHT30

# Constants
WEBHOOK_URL = "https://hook.eu1.make.com/cxyhxctngdmc1ohme35cxln7fi9s7rjm"
TCA9548A_ADDRESS = 0x71
AT_COMMAND_DELAY = 5
led = Pin("LED", Pin.OUT)
mosfet_gate = Pin(16, Pin.OUT)
adc = ADC(2)
r1, r2 = 1000, 2200

try:
    i2c_1 = SoftI2C(scl=Pin(18), sda=Pin(19))
    rtc = DS3231(i2c_1)
    i2c = I2C(0, sda=Pin(4), scl=Pin(5))
    sht = SHT30.SHT30(i2c)
    led = Pin("LED", Pin.OUT)
    mosfet_gate = Pin(16, Pin.OUT)
    adc = ADC(2)
    r1, r2 = 1000, 2200
except Exception as e:
    print(f"Error initializing hardware components: {e}")

#Connect to WIFI
    
def connect_to_wifi():
    try:
        import network
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
        
        del network
        gc.collect()
        return wlan
    except Exception as e:
        print(f"WiFi Connection Error: {e}")
        return None



    
def initialize_sd_card():
    cs = machine.Pin(13, machine.Pin.OUT)  
    spi = machine.SPI(1, baudrate=1000000, polarity=0, phase=0, bits=8,
                      firstbit=machine.SPI.MSB, sck=machine.Pin(10),
                      mosi=machine.Pin(11), miso=machine.Pin(12))

    try:
        uos.umount("/sd1")
        print("Unmounted previous SD card (if any).")
    except Exception as e:
        print(f"Error unmounting SD card: {e}")

    try:
        sd = sdcard.SDCard(spi, cs)
        vfs = uos.VfsFat(sd)
        uos.mount(vfs, "/sd1")
        print("First SD card initialized and mounted.")
        gc.collect()
    except Exception as e:
        print(f"Error initializing SD card: {e}")
        return None  

    return sd

def initialize_second_sd_card():
    cs2 = machine.Pin(1, machine.Pin.OUT)  
    spi2 = machine.SPI(0, baudrate=1000000, polarity=0, phase=0, bits=8,
                       firstbit=machine.SPI.MSB, sck=machine.Pin(6),
                       mosi=machine.Pin(7), miso=machine.Pin(0))

    try:
        uos.umount("/sd2")
        print("Unmounted previous second SD card (if any).")
    except Exception as e:
        print(f"Error unmounting second SD card: {e}")

    try:
        sd2 = sdcard.SDCard(spi2, cs2)
        vfs2 = uos.VfsFat(sd2)
        uos.mount(vfs2, "/sd2")
        print("Second SD card initialized and mounted.")
        gc.collect()
    except Exception as e:
        print(f"Error initializing second SD card: {e}")
        return None  

    return sd2


# Initialize DS18B20
ds_pin = machine.Pin(22)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))


def select_channel(i2c, channel):
    if 0 <= channel <= 7:
        i2c.writeto(0x71, bytearray([1 << channel]))  
        print(f"Selected channel {channel}")
    else:
        raise ValueError("Invalid channel. Must be between 0 and 7.")

#Read SHT30
    
def read_temperature_and_humidity(sensor):
    try:
        temperature, humidity = sensor.measure()
        if temperature is None or humidity is None:
            raise ValueError("Invalid sensor readings")
        return temperature, humidity
    except Exception as e:
        print(f"Error reading SHT30 sensor: {e}")
        return None, None



#Log to SD cards

def log_temperature_to_sd(data_to_log, sd_directory):
    log_path = f"{sd_directory}/log.csv"
    retries = 3

    try:
        files_in_directory = uos.listdir(sd_directory)
        print(f"Files in directory: {files_in_directory}")
    except OSError as e:
        print(f"Error reading directory {sd_directory}: {e}")
        return

    # Check if log.csv exists in the directory
    if 'log.csv' not in files_in_directory:
        print(f"{log_path} not found in directory, creating new file.")
        try:
            with open(log_path, 'w') as file:
                # Write the header only if the file is being created
                file.write("Datetime,Temp1,Temp2,Temp3,Humidity1,Humidity2,Humidity3,Voltage\n")
        except OSError as e:
            print(f"Error creating file: {e}")
            return

    # Now attempt to append data to the file
    for attempt in range(retries):
        try:
            print(f"Attempting to append to {log_path} (Attempt {attempt + 1}/{retries})")

            with open(log_path, 'a') as file:
                print("Logging data:", data_to_log)

                # Prepare the log entry data
                log_values = [
                    data_to_log.get('datetime', 'N/A'),
                    f"{data_to_log.get('temperature_ds1', 0):.2f}",
                    f"{data_to_log.get('temperature_ds2', 0):.2f}",
                    f"{data_to_log.get('temperature_ds3', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_1', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_2', 0):.2f}",
                    f"{data_to_log.get('shtc3_hum_3', 0):.2f}",
                    f"{data_to_log.get('voltage', 0):.2f}"
                ]

                # Format the log entry and append it to the file
                log_entry = ",".join(log_values) + "\n"
                file.write(log_entry)
                file.flush()  # Ensure the data is written immediately

            print(f"Data logged successfully to {log_path}.")
            return  # Exit after successful log entry

        except OSError as e:
            print(f"Error writing to {log_path}: {e} (Attempt {attempt + 1}/{retries})")

    # If retries are exhausted, notify the user
    print(f"Failed to write to {log_path} after {retries} attempts.")






def send_data_to_webhook(data_to_send):
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(WEBHOOK_URL, json=data_to_send, headers=headers, timeout=30)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)


def read_battery_voltage():
    try:
        raw_value = adc.read_u16()
        voltage_out = (raw_value / 65535.0) * 3.3
        vin = voltage_out * ((r1 + r2) / r2)
        return vin
    except Exception as e:
        print(f"Error reading battery voltage: {e}")
        return None


def disconnect_wifi():
    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        wlan.disconnect()
        print("WiFi disconnected.")
    else:
        print("WiFi was not connected.")


def main():
    gc.collect()

    # Connect to WiFi
    wlan = connect_to_wifi() 
    time.sleep(2)

    # Initialize SD cards
    initialize_sd_card()
    time.sleep(1)
    initialize_second_sd_card()
    time.sleep(1)

    # Set the alarm
    print("Setting alarm for every 30 minutes...")
    rtc.alarm1.set(EVERY_HOUR, min=0, sec=0)
    rtc.alarm2.set(EVERY_HOUR, min=30)

    while True:
        time.sleep(1)
        led.value(1)

        # Collect data and publish
        print("Collecting data...")

        # Read voltage with MOSFET ON
        mosfet_gate.value(1)  
        time.sleep(2)  
        vin = read_battery_voltage()
        print("voltage: {:.2f} V".format(vin))

        time.sleep(1)

        # Turn MOSFET OFF
        mosfet_gate.value(0)  
        print("MOSFET OFF")

        try:
            _time = rtc.get_time()
            year, month, day, hour, minute, second, _, _ = _time
            datetime_str = f"{day:02d}-{month:02d}-{year:04d} {hour:02d}:{minute:02d}:{second:02d}"
            print("Current datetime:", datetime_str)
        except Exception as e:
            print(f"Error parsing RTC datetime: {e}")
            datetime_str = "N/A"

        # DS18B20 Temperature Reading
        ds_temperatures = {}
        ds_sensor.convert_temp()
        time.sleep_ms(750)
        for idx, rom in enumerate(ds_sensor.scan()):
            ds_temperatures[f'Sensor {idx + 1}'] = ds_sensor.read_temp(rom)

        time.sleep(1)

        # SHT30 Temperature and Humidity
        shtc3_data = {}
        for channel in range(3):  
            select_channel(i2c, channel)  
            temperature, humidity = read_temperature_and_humidity(sht)
            if temperature is not None and humidity is not None:
                shtc3_data[f'shtc3_temp_{channel + 1}'] = temperature
                shtc3_data[f'shtc3_hum_{channel + 1}'] = humidity
            else:
                print(f"Failed to read data from Channel {channel + 1}")
                shtc3_data[f'shtc3_temp_{channel + 1}'] = 0.0
                shtc3_data[f'shtc3_hum_{channel + 1}'] = 0.0

        # Prepare data for logging and sending
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
            "voltage": vin
        }

        # Log the temperature data to SD cards
        log_temperature_to_sd(data, "/sd1")
        time.sleep(1)
        log_temperature_to_sd(data, "/sd2")
        time.sleep(1)

        
        # If WiFi is connected, send data to the webhook
        
        if wlan and wlan.isconnected():
            send_data_to_webhook(data)
        else:
            print("No WiFi connection, skipping data upload.")

        # Disconnect WiFi after publish
        disconnect_wifi()
        time.sleep(1)
        led.value(0)

        # Clear the alarms (this powers off the system)
        print("Clearing alarms and powering off...")
        rtc.alarm1.clear()
        rtc.alarm2.clear()
        print("Both alarms cleared, system powering off...")

        # Optionally, add deep sleep or shutdown code here
        # machine.deepsleep()
        break  # Exit the loop and end the program


if __name__ == "__main__":
    main()

