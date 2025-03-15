import machine
from machine import Pin, SoftI2C
import time
from ds3231 import DS3231, EVERY_MINUTE

# Initialize onboard LED
led = machine.Pin("LED", machine.Pin.OUT)

# Initialize I2C for DS3231
i2c = SoftI2C(scl=Pin(21), sda=Pin(20))

# Initialize DS3231
try:
    rtc = DS3231(i2c)
    print("DS3231 successfully initialized!")
except Exception as e:
    print("Error: DS3231 not found! Check wiring. Exception:", e)
    while True:
        pass  # Stop execution if RTC is not found

# Set DS3231 alarm to trigger at second 0 of every minute
rtc.alarm1.set(EVERY_MINUTE, sec=0)
print("Alarm set to trigger at second 0 of each minute.")

# Add a startup delay to give Pico more time to initialize
print("Starting up... Giving Pico more time to initialize.")
time.sleep(5)  # Adjust this delay to the desired startup time

while True:
    rtc.alarm1.clear()  # Clear any old alarms

    print("Waiting for DS3231 alarm trigger...")
    while not rtc.alarm1():  # Wait for alarm
        time.sleep(0.5)

    print("⏰ Alarm Triggered! Turning ON LED...")
    led.value(1)

    # Keep LED on for 1 second
    time.sleep(20)
    
    rtc.alarm1.clear()  # Reset alarm

    print("Waiting another 30 seconds for manual trigger...")
    time.sleep(10)  # Manually add a second trigger at 30s


