import machine
import time
from ds3231 import DS3231

# Define I2C interface
sda_pin = machine.Pin(20)
scl_pin = machine.Pin(21)
i2c = machine.SoftI2C(sda=sda_pin, scl=scl_pin)

# Initialize DS3231 RTC
ds3231 = DS3231(i2c)

# Get current local time from Pico
current_time = time.localtime()

# Set time on DS3231 (Year, Month, Day, Hour, Minute, Second, Weekday, Yearday)
ds3231.set_time((current_time[0], current_time[1], current_time[2],
                 current_time[3], current_time[4], current_time[5],
                 current_time[6], 0))

print("RTC time set successfully!")

# Verify time set
time_set = ds3231.get_time()

# Format the time nicely
formatted_time = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
    time_set[0], time_set[1], time_set[2],  # YYYY-MM-DD
    time_set[3], time_set[4], time_set[5]   # HH:MM:SS
)

print("DS3231 Current Time:", formatted_time)

