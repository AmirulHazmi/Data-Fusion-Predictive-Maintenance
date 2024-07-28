import os
import pandas as pd

# File paths
radiation_file = "C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation/result/RadiationAVG.csv"
ctscan_file = "C:/Users/PC/Desktop/FYP/Final Code/Data/CT-Scan/result/CTScanAVG.csv"
additional_file = "C:/Users/PC/Desktop/FYP/Final Code/Data/Prediction Result/result/PredictionTrain.csv"  # Path to the additional CSV file
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Data/IoT_data'
output_file_path = os.path.join(output_directory, 'IoT_data_raw.csv')

# Create output directory if not exists
os.makedirs(output_directory, exist_ok=True)

# Load CSV files with specifying encoding as 'latin-1' and date format
radiation_df = pd.read_csv(radiation_file, parse_dates=["Date Created"], encoding='latin-1', dayfirst=True)
ctscan_df = pd.read_csv(ctscan_file, parse_dates=["Date Created"], encoding='latin-1', dayfirst=True)

# Merge dataframes on 'Date Created'
merged_df = pd.merge(ctscan_df, radiation_df, on="Date Created", how="outer")

# Drop existing index columns
merged_df.drop(columns=['Index_x', 'Index_y'], inplace=True)

# Reset index starting from 1
merged_df.reset_index(drop=True, inplace=True)
merged_df.index += 1  # Start index from 1

# Load additional CSV file with only necessary columns
additional_df = pd.read_csv(additional_file, usecols=["date_created", "result"], dayfirst=True)

# Convert 'date_created' column to datetime64 with dayfirst format
additional_df['date_created'] = pd.to_datetime(additional_df['date_created'], dayfirst=True)

# Merge additional dataframe with merged_df based on 'date_created'
final_merged_df = pd.merge(merged_df, additional_df, left_on="Date Created", right_on="date_created", how="left")

# Drop the 'date_created' column from additional_df as it's already included in merged_df
final_merged_df.drop(columns=['date_created'], inplace=True)

# Rename the 'result' column to 'Actual Risk'
final_merged_df.rename(columns={'result': 'Actual Risk'}, inplace=True)

# Save the final merged dataframe to a new CSV file with date format 'dd/mm/yyyy'
final_merged_df.to_csv(output_file_path, index_label="Index", date_format='%d/%m/%Y')

print("Final merged data saved to:", output_file_path)
