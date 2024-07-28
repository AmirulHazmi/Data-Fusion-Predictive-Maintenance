import pandas as pd
import matplotlib.pyplot as plt

# Define file paths
data_fusion_2022_2023_path = 'C:/Users/PC/Desktop/FYP/Final Code/Fusion/Final_Prediction.csv'
data_fusion_2024_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/Final_Prediction2024.csv'

# Load the data fusion predictions for 2022 and 2023
data_fusion_2022_2023 = pd.read_csv(data_fusion_2022_2023_path, parse_dates=['Date Created'], dayfirst=True)

# Load the data fusion predictions for 2024
data_fusion_2024 = pd.read_csv(data_fusion_2024_path, parse_dates=['Date Created'], dayfirst=True)

# Plotting the graphs
plt.figure(figsize=(14, 8))

# Plot 1: Predicted Risk Level (Data Fusion) for 2022 and 2023 against date
plt.subplot(2, 1, 1)
plt.plot(data_fusion_2022_2023['Date Created'], data_fusion_2022_2023['Predicted Risk Level'], label='Predicted Risk Level (Data Fusion 2022 & 2023)', color='blue')
plt.xlabel('Date')
plt.ylabel('Predicted Risk Level')
plt.title('Predicted Risk Level (Data Fusion 2022 & 2023) vs Date')
plt.legend()

# Plot 2: Predicted Risk Level (Data Fusion) for 2024 against date
plt.subplot(2, 1, 2)
plt.plot(data_fusion_2024['Date Created'], data_fusion_2024['Predicted Risk Level'], label='Predicted Risk Level (Data Fusion 2024)', color='green')
plt.xlabel('Date')
plt.ylabel('Predicted Risk Level')
plt.title('Predicted Risk Level (Data Fusion 2024) vs Date')
plt.legend()

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the plot
plt.show()
