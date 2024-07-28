import os
import pandas as pd

# Load the combined CSV file
combined_file_path = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Prediction Result/result/PredictionCombined.csv'
data = pd.read_csv(combined_file_path)

# Convert 'date_created' column to datetime
data['date_created'] = pd.to_datetime(data['date_created'])

# Drop the 'Unnamed: 0' column
data.drop(columns=['Unnamed: 0'], inplace=True)

# Drop non-numeric columns and 'date_created' and 'prediction'
numeric_columns = data.select_dtypes(include=['float64', 'int64']).columns
numeric_columns = [col for col in numeric_columns if col not in ['date_created', 'prediction']]
numeric_data = data[numeric_columns]

# Group by date_created and aggregate to daily level
daily_data = data.groupby(data['date_created'].dt.date)[numeric_columns].mean()

# Reset index
daily_data.reset_index(inplace=True)

# Display the first few rows of the daily aggregated data
print(daily_data.head())

# Save the daily aggregated data to a new CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Prediction Result/result'
output_file_path = os.path.join(output_directory, 'PredictionTrain.csv')
daily_data.to_csv(output_file_path, index=False)
