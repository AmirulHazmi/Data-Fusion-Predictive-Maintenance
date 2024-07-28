import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pickle

# Load testing data
testing_data = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@IoT_data.csv', encoding='latin1')

# Extract relevant parameters for testing
X_test = testing_data[['Radiation(uSv/h)', 'Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency']]
y = testing_data['Actual Risk']

# Load training data to compare
training_data = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/Data/IoT_data/IoT_data.csv', parse_dates=['Date Created'], dayfirst=True, infer_datetime_format=True, encoding='latin1')
training_data = training_data[(training_data['Date Created'] >= '2022-10-01') & (training_data['Date Created'] <= '2023-12-31')]
training_data = training_data.dropna()

# Compare feature distributions
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(16, 8))
for i, col in enumerate(X_test.columns):  # Use X_test.columns instead of X.columns
    ax = axes[i//4, i%4]
    ax.hist(training_data[col], bins=30, alpha=0.5, color='blue', label='Training')
    ax.hist(X_test[col], bins=30, alpha=0.5, color='green', label='Testing')
    ax.set_title(col)
    ax.legend()

plt.tight_layout()
plt.show()

# Compare target distributions
plt.figure(figsize=(6, 4))
plt.hist(y, bins=30, alpha=0.5, color='blue', label='Training')
plt.hist(testing_data['Actual Risk'], bins=30, alpha=0.5, color='green', label='Testing')
plt.title('Target Distribution')
plt.legend()
plt.show()

# Compare data size
print("Training Data Size:", len(training_data))
print("Testing Data Size:", len(testing_data))
