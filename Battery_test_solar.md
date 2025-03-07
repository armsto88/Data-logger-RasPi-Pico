# Test 1: Battery Life with Solar Input

### Objective:
The objective of this test was to determine how long the data logger could operate on a fully charged battery under normal operating conditions with solar input, and to assess its overall power consumption profile.

### Method:

1. **Fully Charge the Battery**:
   - Verified that the battery was fully charged to 100% using the "LED charge status" indicator on the Waveshare power manager unit.
   - Measured the battery’s voltage using a multimeter for an initial baseline.

2. **Ran the Data Logger Under Normal Load**:
   - Configured the data logger to record data at the standard sampling rate of 30-minute intervals.
   - Ensured that all sensors were running simultaneously to simulate real-world conditions:
     - 3 x DS18B20 temperature sensors
     - 3 x SHT30 humidity/temperature sensors
   - Used Wi-Fi to transmit data to the cloud during the test.

3. **Solar Input Setup**:
   - Positioned the solar panel outside under typical operating conditions to ensure it was exposed to sunlight.
   - Angled the panel to 40° facing south to optimize efficiency for the testing location in Germany.

4. **Monitored Battery Status**:
   - Continuously monitored the battery level throughout the test using the system's voltage monitoring feature.
   - Periodically validated the battery readings by using a multimeter to measure the system’s voltage, ensuring accurate voltage measurements.

5. **Test Duration**:
   - Let the system run until the battery voltage reached 3.2V (the lowest safe voltage before potentially damaging the battery).
   - **Test Conditions**: Conducted tests outdoors under typical operating conditions in Germany (March 8th, 2025).

6. **Recorded Findings**:
   - **Documented Conditions**: Recorded temperature and humidity data from the sensors.
     - **Outdoor Conditions**: Noted the outdoor conditions, including sunlight exposure.
     - **Time**: Used datetime stamps of data logs to calculate battery runtime.
     - **Unit Voltage**: Recorded the voltage from the voltage divider on the unit.
     - **Actual Voltage**: Measured voltage periodically with a multimeter at the same time as it was being read by the unit.

7. **Post-Test Analysis**:
   - **Evaluated Performance**: Compared the battery life achieved with solar input to a baseline (if previous tests were conducted without solar input) and noted any effects from temperature or sunlight.
   - **Identified Efficiency Improvements**: Analyzed components that may have consumed more power than anticipated (e.g., sensors, Wi-Fi module, or data storage).

### Expected Outcome:
The test was expected to provide a clear understanding of the **total operational time** before the battery was depleted, as well as the effectiveness of solar charging. Key findings included:

- **Total battery runtime**: How many hours or days the system could operate before requiring a recharge, with the added benefit of solar input.
- **Performance vs expectations**: Whether the system lasted longer or shorter than expected based on the battery, components, and solar panel efficiency.
- **Battery consumption trends**: Any noticeable patterns in battery usage, such as whether the solar panel contributed enough power to offset battery depletion or if solar input was minimal during cloudy days.

---

### Results

1. **Overview of Test Setup**:
   - **Data Logger Configuration**: The data logger was set to record data at 30-minute intervals, using 3 x DS18B20 temperature sensors and 3 x SHT30 humidity/temperature sensors. Data was transmitted to the cloud via Wi-Fi.
   - **Test Conditions**: Outdoor conditions in Germany (March 8th, 2025), with solar input provided through a solar panel.
   - **Battery Monitoring**: Battery voltage and percentage were monitored periodically, with periodic validation using a multimeter.

2. **Battery Runtime**:

   - **Outdoor Test Duration**:
     - **Start Voltage**: [Insert start voltage]
     - **End Voltage**: [Insert end voltage]
     - **Total Runtime**: [Insert hours/days the battery lasted]
     - **Key Observations**: [Any important notes on performance, e.g., temperature effects, battery consumption trends, or solar input behavior]

3. **Battery Consumption Trends**:
   - **Rate of Battery Depletion**: [Discuss how quickly the battery depleted over time. Did it remain constant, or were there periods of rapid depletion?]
   - **Power-Hungry Components**: [Identify which sensors or components appeared to draw more power than expected. E.g., were the Wi-Fi or sensors the primary contributors to power consumption?]
   - **Solar Input Contribution**: [Discuss how the solar input impacted battery consumption. Did it contribute enough to extend runtime, or was it insufficient due to weather/cloud cover?]

4. **Post-Test Analysis**:
   - **Battery Life vs. Expectations**: [Was the battery life as expected with the addition of solar input? Compare the actual battery life to the anticipated performance based on the system specifications.]
   - **System Efficiency**: [Evaluate whether any specific components (sensors, Wi-Fi, etc.) could be optimized for better power consumption.]
   - **Recommendations for Improvement**: [Suggest any improvements or modifications to increase battery life, such as optimizing solar panel positioning, reducing the data logging frequency, using low-power modes, or selecting more energy-efficient sensors.]

5. **Recharging Process**:
   - **Recharging Time**: [How long did it take to recharge the system to 100% using the solar panel after battery depletion?]
   - **Recharging Efficiency**: [Was the recharging process efficient? Did it align with expected recharging times under real-world sunlight conditions?]

6. **Conclusion**:
   - **Summary of Findings**: [Summarize the overall battery performance with solar input and the key insights from the test.]
   - **Future Testing**: [Outline any follow-up tests or experiments that could further explore or optimize battery life, particularly regarding solar charging efficiency.]

---

### Post-Test Considerations:
- **Data Optimization**: If the battery life was shorter than expected, adjustments could be made to the data logging frequency, low-power modes, or selection of more energy-efficient sensors.
- **Solar Panel Efficiency**: Evaluate the solar panel's ability to maintain an adequate power supply under varying weather conditions to ensure reliable operation during different times of the day or year.
