import pandas as pd

# Load the data
data = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/Data/IoT_data/IoT_data_raw.csv')

# Convert date column to datetime
data['Date Created'] = pd.to_datetime(data['Date Created'], dayfirst=True)

# Set Date column as index
data.set_index('Date Created', inplace=True)

# Replace zeros with NaN to represent missing values
data.replace(0, pd.NA, inplace=True)

# Forward fill missing values
data_ffilled = data.ffill()

# Backward fill missing values
data_bfilled = data.bfill()

# Fill missing values with the median of forward fill and backward fill
median_filled_data = (data_ffilled + data_bfilled) / 2

# Interpolate remaining missing values
interpolated_data = median_filled_data.interpolate(method='linear', axis=0)

# Reset index and start it from 1
interpolated_data.reset_index(inplace=True)
interpolated_data.index += 1  # Start index from 1

# Drop the duplicate 'Index' column
if 'Index' in interpolated_data.columns:
    interpolated_data.drop(columns=['Index'], inplace=True)

# Save interpolated data to CSV with the index starting from 1
interpolated_data.to_csv('C:/Users/PC/Desktop/FYP/Final Code/Data/IoT_data/IoT_data.csv', index_label="Index")

print("Interpolated data saved successfully.")
