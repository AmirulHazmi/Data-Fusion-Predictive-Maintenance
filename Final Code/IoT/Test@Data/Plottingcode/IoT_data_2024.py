import os
import pandas as pd

# File paths for final merge
radiation_file = "C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@Radiation/result/RadiationAVG_raw.csv"
ctscan_file = "C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@CT_Scan/result/CTScanAVG_raw.csv"
output_directory = 'C:/Users/PC/Desktop/FYP/Final Code/Plotting'
output_file_path = os.path.join(output_directory, 'IoT_data_2024_raw.csv')

# Load CSV files with specifying encoding as 'latin-1' and date format
radiation_df = pd.read_csv(radiation_file, parse_dates=["Date Created"], encoding='latin-1', dayfirst=True)
ctscan_df = pd.read_csv(ctscan_file, parse_dates=["Date Created"], encoding='latin-1', dayfirst=True)

# Merge dataframes on 'Date Created'
merged_df = pd.merge(ctscan_df, radiation_df, on="Date Created", how="outer")

# Drop existing index columns
merged_df.drop(columns=['Index_x', 'Index_y'], inplace=True)

# Interpolation
merged_df['Date Created'] = pd.to_datetime(merged_df['Date Created'], dayfirst=True)
merged_df.set_index('Date Created', inplace=True)
merged_df.replace(0, pd.NA, inplace=True)
data_ffilled = merged_df.ffill()
data_bfilled = merged_df.bfill()
median_filled_data = (data_ffilled + data_bfilled) / 2
interpolated_data = median_filled_data.interpolate(method='linear', axis=0)
interpolated_data.reset_index(inplace=True)
interpolated_data.index += 1  # Start index from 1

# Drop the duplicate 'Index' column
if 'Index' in interpolated_data.columns:
    interpolated_data.drop(columns=['Index'], inplace=True)

# Save interpolated data to CSV with the index starting from 1
interpolated_data.to_csv(output_file_path, index_label="Index", date_format='%d/%m/%Y')

print("Final merged and interpolated data saved to:", output_file_path)
