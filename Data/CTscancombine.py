# combine data of the excel file

import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Specify the directory where your CSV files are located
directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/CT-Scan'

# Create an empty list to store processed DataFrames
all_data_list = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        print("Processing file:", file_path)  # Add this line for debugging
        
        # Step 1: Load Data
        data = pd.read_csv(file_path)

        # Step 2: Data Preprocessing
        data = data.dropna()
        data['Date Created'] = pd.to_datetime(data['Date Created'], format="%d/%m/%Y %H:%M")

        # Step 3: Feature Selection
        selected_columns = ['Date Created', 'Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency']
        features = data[selected_columns]

        # Step 4: Target Variable
        # Assuming you have a target variable named 'DR'
        target = data['DR']

        # Step 5: Scaling
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features.drop('Date Created', axis=1))

        # Combine Features, Date Created, and Target
        processed_data = pd.concat([features[['Date Created']], pd.DataFrame(features_scaled, columns=selected_columns[1:]), target], axis=1)

        # Append processed data to the list
        all_data_list.append(processed_data)

# Concatenate all DataFrames in the list
all_data = pd.concat(all_data_list, ignore_index=True)

# Sort the DataFrame by 'Date Created'
all_data = all_data.sort_values(by='Date Created')

# Add an index column with a name
all_data.reset_index(inplace=True, drop=True)
all_data.index = all_data.index + 1
all_data = all_data.rename_axis('Index')

# Display the first few rows of the combined DataFrame
print(all_data.head())

# Save the combined data to a CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/CT-Scan/result'
os.makedirs(output_directory, exist_ok=True)
output_file_path = os.path.join(output_directory, 'CTScan_combined.csv')
all_data.to_csv(output_file_path, index=True)
