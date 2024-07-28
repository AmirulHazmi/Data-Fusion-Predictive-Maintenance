import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
iot_data_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Training/training_data_with_predictions.csv'
data_fusion_path = 'C:/Users/PC/Desktop/FYP/Final Code/Fusion/Final_Prediction.csv'

# Load the IoT data with predictions
iot_data = pd.read_csv(iot_data_path, parse_dates=['Date Created'], dayfirst=True)

# Load the data fusion predictions
data_fusion_data = pd.read_csv(data_fusion_path, parse_dates=['Date Created'], dayfirst=True)

# Plotting the graphs
plt.figure(figsize=(14, 10))

# Plot 1: Actual Risk (renamed as Reference Risk) against date
plt.subplot(3, 1, 1)
plt.plot(iot_data['Date Created'], iot_data['Actual Risk'], label='Reference Risk (Current Dashboard)', color='blue')
plt.xlabel('Date')
plt.ylabel('Reference Risk (Current Dashboard)')
plt.title('Reference Risk (Current Dashboard) vs Date')
plt.legend()

# Plot 2: Predicted Risk (using IoT only) against date
plt.subplot(3, 1, 2)
plt.plot(iot_data['Date Created'], iot_data['Predicted Risk'], label='Predicted Risk (IoT only)', color='green')
plt.xlabel('Date')
plt.ylabel('Predicted Risk (IoT only)')
plt.title('Predicted Risk (IoT only) vs Date')
plt.legend()

# Plot 3: Predicted Risk Level (Data Fusion) against date
plt.subplot(3, 1, 3)
plt.plot(data_fusion_data['Date Created'], data_fusion_data['Predicted Risk Level'], label='Predicted Risk Level (Data Fusion)', color='red')
plt.xlabel('Date')
plt.ylabel('Predicted Risk Level (Data Fusion)')
plt.title('Predicted Risk Level (Data Fusion) vs Date')
plt.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
