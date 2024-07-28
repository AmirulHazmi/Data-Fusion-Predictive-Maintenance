import pandas as pd

def combine_to_daily(input_file, output_file, value_columns):
    # Load the data with specified encoding
    data = pd.read_csv(input_file, encoding='latin1')
    
    # Convert 'Date Created' column to datetime with specified format
    data['Date Created'] = pd.to_datetime(data['Date Created'], format='%d/%m/%Y')
    
    # Group by daily date and take average of specified value columns
    data = data.groupby(data['Date Created'].dt.date)[value_columns].mean().reset_index()
    
    # Ensure every date from start to end exists and fill missing values with zeros
    date_range = pd.date_range(start=data['Date Created'].min(), end=data['Date Created'].max(), freq='D')
    full_dates = pd.DataFrame({'Date Created': date_range})
    
    # Convert 'Date Created' column to datetime for the second DataFrame
    data['Date Created'] = pd.to_datetime(data['Date Created'])
    
    # Merge on datetime column
    data = full_dates.merge(data, on='Date Created', how='left').fillna(0)
    
    # Add an index column starting from 1
    data.insert(0, 'Index', range(1, len(data) + 1))
    
    # Save the combined data
    data.to_csv(output_file, index=False)

# Paths for input and output files
radiation_input_file = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@Radiation/result/Test@Radiation_combined.csv'
radiation_output_file = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@Radiation/result/Test@RadiationAVG.csv'

ct_scan_input_file = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@CT_Scan/result/Test@CTScan_combined.csv'
ct_scan_output_file = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@CT_Scan/result/Test@CTScanAVG.csv'

# Columns to include for CT scan data
ct_scan_columns = ['Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency']

# Combine radiation data to daily format and save
combine_to_daily(radiation_input_file, radiation_output_file, ['Radiation(uSv/h)'])

# Combine CT scan data to daily format and save with all columns
combine_to_daily(ct_scan_input_file, ct_scan_output_file, ct_scan_columns)

print("Data combined and saved successfully!")
