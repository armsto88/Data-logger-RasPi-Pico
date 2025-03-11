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
i2c_1 = SoftI2C(scl=Pin(18), sda=Pin(19))
rtc = DS3231(i2c_1) 
i2c = I2C(0, sda=Pin(4), scl=Pin(5))
sht = SHT30.SHT30(i2c)
led = machine.Pin("LED", machine.Pin.OUT)
mosfet_gate = Pin(16, Pin.OUT)
adc = ADC(2)
r1 = 1000  
r2 = 2200


# WiFi connection function with delay
def connect_to_wifi():
    import network   

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    ssid = 'gigacube-0F3C'
    password = '5dTQ7HA8242495T8'
    wlan.connect(ssid, password)

    retry_count = 0
    max_retries = 10
    delay_seconds = 2  

    while not wlan.isconnected() and retry_count < max_retries:
        print(f"Connecting to WiFi... Attempt {retry_count + 1}/{max_retries}")
        time.sleep(delay_seconds)  
        retry_count += 1

    if wlan.isconnected():
        print("Connected to WiFi:", wlan.ifconfig())
        del network  
        gc.collect()  
        return wlan
    else:
        print("Failed to connect to WiFi after retries.")
        del network  
        gc.collect()  
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

# SHT30 Function
def read_temperature_and_humidity(sensor):
    try:
        temperature, humidity = sensor.measure()
        return temperature, humidity
    except SHT30Error as e:
        print(f"SHT30 sensor error: {e.get_message()}")
        return None, None
    except Exception as e:
        print(f"Unexpected error reading SHT30 sensor: {e}")
        return None, None


def log_temperature_to_sd(data_to_log, sd_directory):
    log_path = f"{sd_directory}/log.csv"
    retries = 3

    for attempt in range(retries):
        try:
            if log_path not in uos.listdir(sd_directory):
                with open(log_path, 'w') as file:
                    file.write("Datetime,Temp1,Temp2,Temp3,Humidity1,Humidity2,Humidity3,Voltage\n")

            with open(log_path, 'a') as file:
                print("Logging data:", data_to_log)

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

                log_entry = ",".join(log_values) + "\n"
                file.write(log_entry)
                file.flush()

            print(f"Data logged successfully to {sd_directory}.")
            return  

        except OSError as e:
            print(f"Error writing to {sd_directory}: {e} (Attempt {attempt + 1}/{retries})")

    print(f"Failed to write to {sd_directory} after {retries} attempts.")


def send_data_to_webhook(data_to_send):
    try:
        headers = {'Content-Type': 'application/json'}
        response = urequests.post(WEBHOOK_URL, json=data_to_send, headers=headers, timeout=30)
        print("Response:", response.status_code, response.text)
    except Exception as e:
        print("Error sending data:", e)


def read_battery_voltage():
    raw_value = adc.read_u16()  
    voltage_out = (raw_value / 65535.0) * 3.3  
    vin = voltage_out * ((r1 + r2) / r2)  
    return vin


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
    connect_to_wifi()
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

        # Send the data to a webhook
        send_data_to_webhook(data)

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

