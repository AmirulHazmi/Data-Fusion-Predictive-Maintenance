import os
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Specify the directory where your CSV files are located
directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation'

# Create an empty list to store processed DataFrames
all_data_list = []

# Initialize StandardScaler
scaler = StandardScaler()

# Loop through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(directory, filename)
        print("Processing file:", file_path)  # Add this line for debugging
        
        # Step 1: Load Data
        data = pd.read_csv(file_path)
        
        # Step 2: Data Preprocessing
        data['Date Created'] = pd.to_datetime(data['Date Created'], format="%d/%m/%Y %H:%M", errors='coerce')  # Handle any parsing errors
        
        # Drop rows with NaN in 'Radiation(uSv/h)' or 'Date Created' columns
        data = data.dropna(subset=['Radiation(uSv/h)', 'Date Created'])
        
        # Fill remaining missing values in 'Radiation(uSv/h)' column with 0
        data['Radiation(uSv/h)'] = data['Radiation(uSv/h)'].fillna(0)
        
        # Step 3: Feature Selection
        selected_columns = ['Date Created', 'Radiation(uSv/h)']
        features = data[selected_columns]
        
        # Ensure there are no missing values in 'Date Created' after the operations
        if features['Date Created'].isnull().any():
            print("Warning: Missing dates found after preprocessing.")
        
        # Step 4: Scaling
        features_scaled = scaler.fit_transform(features[['Radiation(uSv/h)']])
        
        # Combine Features, Date Created
        processed_data = pd.concat([features[['Date Created']].reset_index(drop=True), 
                                    pd.DataFrame(features_scaled, columns=['Radiation(uSv/h)'])], axis=1)
        
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

# Ensure there are no missing values in 'Date Created' before saving
if all_data['Date Created'].isnull().any():
    print("Warning: Missing dates found in the final combined data.")

# Save the combined data to a CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation/result'
os.makedirs(output_directory, exist_ok=True)
output_file_path = os.path.join(output_directory, 'Radiation_combined.csv')
all_data.to_csv(output_file_path, index=True)
