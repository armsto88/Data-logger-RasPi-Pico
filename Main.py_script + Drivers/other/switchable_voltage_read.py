from machine import ADC, Pin
from time import sleep

# MOSFET control on GPIO16
mosfet_gate = Pin(16, Pin.OUT)

# ADC setup (measuring from GP28 / ADC2)
adc = ADC(2)

# Resistor values for voltage divider
r1 = 1000  # 100kΩ
r2 = 2200  # 100kΩ

def read_battery_voltage():
    raw_value = adc.read_u16()  # Read ADC (0-65535)
    voltage_out = (raw_value / 65535.0) * 3.3  # Convert ADC to voltage
    vin = voltage_out * ((r1 + r2) / r2)  # Calculate input voltage
    return vin

while True:
    # Read voltage with MOSFET OFF
    mosfet_gate.value(0)  # Turn MOSFET OFF
    sleep(2)  # Allow time for stabilization
    vin_off = read_battery_voltage()
    print("Voltage with MOSFET OFF: {:.2f} V".format(vin_off))

    # Read voltage with MOSFET ON
    mosfet_gate.value(1)  # Turn MOSFET ON
    sleep(2 )  # Allow time for stabilization
    vin_on = read_battery_voltage()
    print("Voltage with MOSFET ON: {:.2f} V".format(vin_on))

    # Wait before next measurement
    sleep(5)

