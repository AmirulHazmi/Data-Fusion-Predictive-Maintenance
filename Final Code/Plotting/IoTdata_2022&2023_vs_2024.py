import matplotlib.pyplot as plt
import pandas as pd

# Load data from CSV files with latin1 encoding
data_2022_2023 = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/Plotting/IoT_data_2022&2023_raw.csv', parse_dates=["Date Created"], encoding='latin1')
data_2024 = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/Plotting/IoT_data_2024_raw.csv', parse_dates=["Date Created"], encoding='latin1')

# Parameters to plot
parameters = ['Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency', 'Radiation(uSv/h)']

# Plotting each parameter
plt.figure(figsize=(16, 8))

for i, param in enumerate(parameters, start=1):
    plt.subplot(2, 4, i)
    plt.hist(data_2022_2023[param], bins=30, alpha=0.5, color='green', label='2022&2023')
    plt.hist(data_2024[param], bins=30, alpha=0.5, color='blue', label='2024')
    plt.xlabel(param)
    plt.ylabel('Frequency')
    plt.legend()

plt.suptitle('Parameter Distributions: 2022&2023 vs 2024', fontsize=16)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
