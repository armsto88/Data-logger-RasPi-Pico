library(tidyverse)
library(lubridate)
library(ggplot2)
library(zoo)


###Test_1
write.csv(df,"Pico_solar_abiotic - test_1.csv")
df<-read.csv("raw_test_data/Pico_solar_abiotic - test_1.csv")
df <- df %>%
  slice(10:n())
df <- df %>%
  mutate(acc.V = replace(acc.V,1,4.02))


str(df)

df <- df %>%
  mutate(datetime = dmy_hms(datetime),
         cumulative_hours = as.numeric(difftime(datetime, first(datetime), units = "hours")))

df <- df %>%
  slice(2:n())

df<- df%>%
  rename(Batt_voltage = Voltage,`Acc..V`=acc.V)


# Interpolate missing values
df <- df %>%
  mutate(
    Batt_voltage = na.approx(Batt_voltage, cumulative_hours, na.rm = FALSE),
    `Acc..V` = na.approx(`Acc..V`, cumulative_hours, na.rm = FALSE)
  )

Inside <-ggplot(df, aes(x = cumulative_hours)) +
  geom_line(aes(y = Batt_voltage, color = "Batt Voltage"), size = 1.2) +
  geom_line(aes(y = `Acc..V`, color = "Acc. Voltage"), size = 1.2) +
  scale_color_manual(values = c("Batt Voltage" = "#1B9E77", "Acc. Voltage" = "#D95F02")) +
  scale_x_continuous(
    limits = c(0, max(df$cumulative_hours,na.rm = T)),  # Adjust x-axis limits based on your data
    breaks = seq(0, max(df$cumulative_hours,na.rm = T), by = 5))+
  labs(
    title = paste0("Average temp.", " = ", round(mean(df$temperature_ds1, na.rm = TRUE), digits = 3), "°C"),
    x = "Cumulative Hours",
    y = "Voltage (V)",
    color = "Legend"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    legend.title = element_blank(),
    axis.title.y  = element_text(vjust = 5,face = "bold"),
    axis.title.x  = element_text(vjust = -3,face = "bold"),
    plot.margin = margin(20, 20, 20, 20) # Adjust margins (top, right, bottom, left)
  )

Inside
#Sensor comparisons 

#Temperature
temp_ds<-df%>%
  select(c(cumulative_hours,temperature_ds1,temperature_ds2,temperature_ds3))

under<-temp_ds %>%
  ggplot(aes(x = cumulative_hours)) +
  geom_line(aes(y = temperature_ds1, color = "Temperature DS1"), size = 1.2) +
  geom_line(aes(y = temperature_ds2, color = "Temperature DS2"), size = 1.2) +
  geom_line(aes(y = temperature_ds3, color = "Temperature DS3"), size = 1.2) +
  scale_color_manual(values = c("Temperature DS1" = "#1B9E77", "Temperature DS2" = "#D95F02", "Temperature DS3" = "#7570B3")) +
  scale_x_continuous(
    limits = c(0, max(temp_ds$cumulative_hours, na.rm = TRUE)),  # Ignore NA values in max calculation
    breaks = seq(0, max(temp_ds$cumulative_hours, na.rm = TRUE), by = 5)  # Set breaks at 5-hour intervals
  ) +
  labs(
    x = "Cumulative Hours",
    y = "Temperature (°C)",
    color = "Legend"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    legend.title = element_blank(),
    axis.title.x = element_text(vjust = -2,face="bold"),
    axis.title.y = element_text(vjust = 3,face="bold"),
    plot.margin = margin(20, 20, 20, 20)
  )


# Select relevant columns from the df data
temperature_data <- df %>%
  select(c(cumulative_hours, shtc3_temp_1, shtc3_temp_2, shtc3_temp_3))

# Plot temperature data
over<-ggplot(temperature_data, aes(x = cumulative_hours)) +
  geom_line(aes(y = shtc3_temp_1, color = "SHT30_temp_1"), size = 1.2) +
  geom_line(aes(y = shtc3_temp_2, color = "SHT30_temp_2"), size = 1.2) +
  geom_line(aes(y = shtc3_temp_3, color = "SHT30_temp_3"), size = 1.2) +
  scale_color_manual(values = c("SHT30_temp_1" = "#1B9E77", 
                                "SHT30_temp_2" = "#D95F02", 
                                "SHT30_temp_3" = "#7570B3")) +
  scale_x_continuous(
    limits = c(0, max(temperature_data$cumulative_hours, na.rm = TRUE)),  # Ignore NA values in max calculation
    breaks = seq(0, max(temperature_data$cumulative_hours, na.rm = TRUE), by = 5)  # Set breaks at 5-hour intervals
  ) +
  labs(
    x = "Cumulative Hours",
    y = "Temperature (°C)",
    color = "Sensors"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    legend.title = element_blank(),
    axis.title.x = element_text(vjust = -2, face = "bold"),
    axis.title.y = element_text(vjust = 3, face = "bold"),
    plot.margin = margin(20, 20, 20, 20)
  )

library(gridExtra)


grid.arrange(under, over, ncol = 2)

# Correct data labeling and use proper variables for humidity
humidity_data <- df %>%
  select(c(cumulative_hours, shtc3_hum_1, shtc3_hum_2, shtc3_hum_3))

hum <- ggplot(humidity_data, aes(x = cumulative_hours)) +
  geom_line(aes(y = shtc3_hum_1, color = "SHT30_Humidity_1"), size = 1.2) +
  geom_line(aes(y = shtc3_hum_2, color = "SHT30_Humidity_2"), size = 1.2) +
  geom_line(aes(y = shtc3_hum_3, color = "SHT30_Humidity_3"), size = 1.2) +
  scale_color_manual(values = c("SHT30_Humidity_1" = "#1B9E77", 
                                "SHT30_Humidity_2" = "#D95F02", 
                                "SHT30_Humidity_3" = "#7570B3")) +
  scale_x_continuous(
    limits = c(0, max(humidity_data$cumulative_hours, na.rm = TRUE)),  # Ignore NA values in max calculation
    breaks = seq(0, max(humidity_data$cumulative_hours, na.rm = TRUE), by = 5)  # Set breaks at 5-hour intervals
  ) +
  labs(
    x = "Cumulative Hours",
    y = "Humidity (%)",
    color = "Sensors"
  ) +
  theme_minimal() +
  theme(
    legend.position = "top",
    legend.title = element_blank(),
    axis.title.x = element_text(vjust = -2, face = "bold"),
    axis.title.y = element_text(vjust = 3, face = "bold"),
    plot.margin = margin(20, 20, 20, 20)
  )

hum

out
Inside
grid.arrange(out, Inside, ncol = 2)

