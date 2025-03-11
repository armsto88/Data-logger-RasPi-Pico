# Test 1: Battery Life

### Objective:
The goal of this test was to determine how long the data logger could operate on a fully charged battery under normal operating conditions, as well as to assess its overall power consumption profile.

### Method:

1. **Fully Charged the Battery**:
   - Verified that the battery was completely charged to 100% using the "LED charge status" indicator on the Waveshare power manager unit.
   - Measured the battery's voltage using a multimeter for an initial baseline.

2. **Ran the Data Logger Under Normal Load**:
   - Configured the data logger to record data at the standard sampling rate of 30-minute intervals.
   - Ensured that all sensors were running simultaneously to simulate real-world conditions:
     - 3 x DS18B20 temperature sensors
     - 3 x SHT30 humidity/temperature sensors
   - Used Wi-Fi to transmit data to the cloud during the test.

3. **Monitored Battery Status**:
   - Continuously monitored the battery level throughout the test using the system's battery tracking feature.
   - Logged the battery percentage at regular intervals and tracked its decrease over time.
   - Periodically validated the battery readings by using a multimeter to measure the system's voltage, ensuring accurate voltage measurements.

4. **Test Duration**:
   - Let the system run until the battery voltage reached 3.2V (the lowest safe voltage before potentially damaging the battery).
   - **Test Conditions**: Conducted tests in two different environments:
     - Indoor conditions with relatively stable temperature (~15°C)
     - Outdoor conditions under typical operating conditions in Germany (March 8th, 2025)

5. **Recorded Findings**:
   - **Documented Conditions**: Recorded temperature and humidity data from the sensors.
     - **Indoor or Outdoor**: Noted the treatment type (Indoor/Outdoor).
     - **Time**: Used datetime stamps of data logs to calculate battery runtime.
     - **Unit Voltage**: Recorded the voltage from the voltage divider on the unit.
     - **Actual Voltage**: Measured voltage periodically with a multimeter at the same time as it was being read by the unit.

6. **Post-Test Analysis**:
   - **Evaluated Performance**: Compared the battery life across both test conditions and noted any temperature variances.
   - **Identified Efficiency Improvements**: Analyzed components that may have consumed more power than anticipated (e.g., sensors, Wi-Fi module, or data storage).

### Expected Outcome:
The test was expected to provide a clear understanding of the **total operational time** before the battery was depleted. Key findings included:

- **Total battery runtime**: The number of hours or days the system could operate before requiring a recharge.
- **Performance vs expectations**: Whether the system lasted longer or shorter than expected based on the battery and component specifications.
- **Battery consumption trends**: Any noticeable patterns in battery usage, such as rapid depletion at certain intervals.

### Results


### 1. **Overview of Test Setup**
   - **Data Logger Configuration**: The data logger was set to record data at 30-minute intervals, using 3 x DS18B20 temperature sensors and 3 x SHT30 humidity/temperature sensors. Data was transmitted to the cloud via Wi-Fi.
   - **Test Conditions**: Two testing environments were used:
     - **Indoor**: Stable temperature (~15°C)
     - **Outdoor**: Normal operating conditions in Germany (March 8th, 2025)
   - **Battery Monitoring**: Battery voltage read from the voltage divider was monitored , with periodic validation using a multimeter.

### 2. **Battery Runtime**

#### **Indoor Test Duration**
- **Start Voltage**: 3.92 V (actual: 3.96 V)  
- **End Voltage**: 3.00 V (actual: 3.00 V)  
- **Total Runtime**: 71.2 hours  

#### **Key Observations**
- The internal voltage reading is approximately **0.02 V lower** than the multimeter reading at its maximum value.  
- Significant noise is present, likely due to the **ADC on the Raspberry Pi Pico**, causing fluctuations of around **±0.2 V**.  
- While the general trend of the internal voltage reading is accurate, it **is not reliable** for low-power shutoff decisions.  
- The **Waveshare power manager** automatically cuts power at **3.0 V**.

#### **Voltage Over Time**
![Battery Voltage Over Time](/Testing/test_1_(Voltage_Time).svg)

      

   - **Outdoor Test Duration**:
     - **Start Voltage**: [Insert start voltage]
     - **End Voltage**: [Insert end voltage]
     - **Total Runtime**: [Insert hours/days the battery lasted]
     - **Key Observations**: [Any relevant observations based on environmental factors like sunlight or weather]

### 3. **Battery Consumption Trends**
   - **Rate of Battery Depletion**: [Discuss how quickly the battery depleted over time. Did it remain constant, or were there periods of rapid depletion?]
   - **Power-Hungry Components**: [Identify which sensors or components appeared to draw more power than expected. E.g., were the Wi-Fi or sensors the primary contributors to power consumption?]
   - **Voltage Drops**: [Describe any significant drops in voltage or periods of instability, if any.]

### 4. **Comparison of Indoor vs. Outdoor Performance**
   - **Indoor vs. Outdoor Performance**: [Provide a comparative analysis of battery life under indoor and outdoor conditions. Discuss how environmental factors (e.g., temperature, sunlight) may have impacted the test.]
   - **Temperature Influence**: [Discuss the impact of temperature on battery life. Was there any significant difference between the two conditions?]

### 5. **Post-Test Analysis**
   - **Battery Life vs. Expectations**: [Was the battery life as expected? Compare the actual battery life to the anticipated performance based on the system specifications.]
   - **System Efficiency**: [Evaluate whether any specific components (sensors, Wi-Fi, etc.) could be optimized for better power consumption.]
   - **Recommendations for Improvement**: [Suggest any improvements or modifications to increase battery life. E.g., reducing the sampling rate, using lower-power sensors, etc.]

### 6. **Recharging Process**
   - **Recharging Time**: [How long did it take to recharge the system to 100%?]
   - **Recharging Efficiency**: [Was the recharging process efficient? Did it align with expected recharging times?]

### 7. **Conclusion**
   - **Summary of Findings**: [Summarize the overall battery performance and the key insights from the test.]
   - **Future Testing**: [Outline any follow-up tests or experiments that could further explore or optimize battery life.]



### Post-Test Considerations:
- **Data Optimization**: If the battery life was shorter than expected, adjustments could be made to the data logging frequency, power-saving modes, or the selection of more energy-efficient sensors.
- **Recharging Process**: After the battery was depleted, the time required to fully recharge the system was tested to assess recharging efficiency.
- **Real-World Use Case**: The test could be repeated under various environmental conditions to simulate real-world scenarios, such as different seasonal temperatures or varying sunlight exposure for solar charging.
