import os
import pandas as pd

# Specify the directory where your CSV files are located
directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Prediction Result'

# Create an empty list to store DataFrames
all_data_list = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        print("Processing file:", file_path)  # Add this line for debugging
        
        # Step 1: Load Data
        data = pd.read_csv(file_path)

        # Append data to the list
        all_data_list.append(data)

# Concatenate all DataFrames in the list
all_data = pd.concat(all_data_list, ignore_index=True)

# Convert 'Date Created' column to datetime
all_data['date_created'] = pd.to_datetime(all_data['date_created'], format="%d/%m/%Y %H:%M")

# Sort the DataFrame by 'Date Created'
all_data.sort_values(by='date_created', inplace=True)

# Reset index
all_data.reset_index(drop=True, inplace=True)

# Display the first few rows of the combined DataFrame
print(all_data.head())

# Save the combined data to a CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Prediction Result/result'
os.makedirs(output_directory, exist_ok=True)
output_file_path = os.path.join(output_directory, 'PredictionCombined.csv')
all_data.to_csv(output_file_path, index=True)
