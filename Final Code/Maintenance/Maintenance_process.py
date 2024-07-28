import pandas as pd

# Path to the existing CSV file
file_path = r"C:\Users\PC\Desktop\FYP\Final Code\Maintenance\maintenanceReport_processed.csv"

# Read the CSV file
df = pd.read_csv(file_path)

# Define the new rows for specific dates
new_rows = {
    '10/4/2021': {
        'File': '2017507', 'Issue': 'Gantry', 'Details': """1) Removed the existing x-ray tube - OK 
2) Installed the new x-ray tube - OK 
3) Secure all cables and connection - OK 
4) Test scan done. All ok, performed full warm up - OK 
5) Performed If adjustment - OK 
6) Performed X-ray tube alignment - OK 
7) Performed NRA calibration - OK 
8) Image quality checked  - All OK 
9) QC test done - All pass OK 
10) EST done: i)Enclosure leakage: 7uA ii) Patient leakage: 0ua. } pass. 
11) System is in good working condition - OK"""
    },
    '8/12/2023': {
        'File': '2018444', 'Issue': 'Software', 'Details': """1) Checks found the symptoms above 
2) Check log found Rotsory Communication error occur 
3) Check the error code on GCIFA found previous error occur on Channel 4 
4) Perform MUDAT Test no error occur on DCA 
5) Check raw data E3 for mudat error , no error found due to error didn't occur during scanning 
6) Reset cable at OPCONTA GCIFA OK 
7) KIV the symptom 1 week"""
    },
    '7/2/2024': {
        'File': '2025423', 'Issue': 'None', 'Details': """1) Checked all the scan images on 7/2/2024 - most of the scan have multiple line artifact 
2) Checked the output and offset data - OK 
3) Compare reference output graph with good image data and bad image data 
4) Found reference graph output for bad image data abnormal 
5) Confirmed CT value with phantom scan - OK 
6) Replaced the new Reference Detector for troubleshooting purpose 
7) Found no more multiple line artifact at scan image 
8) Checked reference output graph - OK 
9) Confirmed the symptom due to faulty reference detector 
10) Faulty part replaced under leasing project 
11) Performed electrical safety test - OK"""
    }
}

# Define the date ranges for which new rows need to be added
date_ranges = {
    '10/4/2021': pd.date_range(start='2023-07-07', end='2023-11-07', freq='D'),
    '8/12/2023': pd.date_range(start='2023-12-08', end='2024-02-03', freq='D'),
    '7/2/2024': pd.date_range(start='2024-02-07', end='2024-05-31', freq='D')
}

# Initialize a list to collect all rows
all_rows = []

# Populate the list with existing rows
for _, row in df.iterrows():
    all_rows.append(row.to_dict())

# Append the new rows for the specified date ranges
for key, date_range in date_ranges.items():
    for date in date_range:
        new_row = new_rows[key].copy()
        new_row['Date'] = date.strftime('%d/%m/%Y')
        all_rows.append(new_row)

# Convert the list of rows back into a DataFrame
new_df = pd.DataFrame(all_rows)

# Sort by date to ensure chronological order
new_df['Date'] = pd.to_datetime(new_df['Date'], format='%d/%m/%Y')
new_df = new_df.sort_values(by='Date')

# Fill in the remaining dates with a default message
date_range_full = pd.date_range(start=new_df['Date'].min(), end=new_df['Date'].max(), freq='D')
date_range_str = date_range_full.strftime('%d/%m/%Y')

# Add default message for dates not covered
default_rows = []
for date in date_range_str:
    if date not in new_df['Date'].dt.strftime('%d/%m/%Y').values:
        default_rows.append({'Date': date, 'Details': 'No maintenance has been done, Please do soon'})

# Concatenate the default rows to the existing DataFrame
if default_rows:
    default_df = pd.DataFrame(default_rows)
    default_df['Date'] = pd.to_datetime(default_df['Date'], format='%d/%m/%Y')
    new_df = pd.concat([new_df, default_df], ignore_index=True)

# Sort again to ensure correct order after adding default rows
new_df = new_df.sort_values(by='Date')

# Save the modified DataFrame to a new CSV file
new_df.to_csv(r"C:\Users\PC\Desktop\FYP\Final Code\Maintenance\modified_maintenanceReport.csv", index=False)
