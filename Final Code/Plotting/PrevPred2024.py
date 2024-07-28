import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
iot_data_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@IoT_data.csv'

# Load the IoT data with predictions
iot_data = pd.read_csv(iot_data_path, parse_dates=['Date Created'], dayfirst=True,encoding='latin1')

# Plotting the graphs
plt.figure(figsize=(14, 10))

# Plot 1: Actual Risk (renamed as Reference Risk) against date
plt.subplot(3, 1, 1)
plt.plot(iot_data['Date Created'], iot_data['Actual Risk'], label='Existing Prediction Model (Current Dashboard)', color='blue')
plt.xlabel('Date')
plt.ylabel('Existing Prediction Model (Current Dashboard)')
plt.title('Existing Prediction Model (Current Dashboard) vs Date')
plt.legend()


# Show the plot
plt.show()

