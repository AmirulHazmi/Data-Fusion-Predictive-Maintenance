import os
import pandas as pd

# Specify the directory where your CSV files are located
directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation'

# Create an empty list to store DataFrames
all_data_list = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        print("Processing file:", file_path)  # Debugging line to see which file is being processed
        
        # Load Data
        data = pd.read_csv(file_path)
        
        # Append the data to the list
        all_data_list.append(data)

# Concatenate all DataFrames in the list
all_data = pd.concat(all_data_list, ignore_index=True)

# Sort the DataFrame by 'Date Created' if the column exists
if 'Date Created' in all_data.columns:
    all_data['Date Created'] = pd.to_datetime(all_data['Date Created'], format="%d/%m/%Y %H:%M", errors='coerce')
    all_data = all_data.sort_values(by='Date Created')

# Add an index column with a name
all_data.reset_index(inplace=True, drop=True)
all_data.index = all_data.index + 1
all_data = all_data.rename_axis('Index')

# Display the first few rows of the combined DataFrame
print(all_data.head())

# Save the combined data to a CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation/result'
os.makedirs(output_directory, exist_ok=True)
output_file_path = os.path.join(output_directory, 'Radiation_combined_raw.csv')
all_data.to_csv(output_file_path, index=True)
