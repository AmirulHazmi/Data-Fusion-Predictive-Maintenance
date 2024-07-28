import pandas as pd

# Load the combined dataset
file_path = 'C:/Users/PC/Desktop/FYP/Final Code/Data/Radiation/result/Radiation_combined.csv'
data = pd.read_csv(file_path, parse_dates=['Date Created'])

# Normalize 'Date Created' to only include the date part
data['Date'] = data['Date Created'].dt.date

# Drop duplicate dates, keeping the first occurrence
data = data.drop_duplicates(subset='Date', keep='first')

# Set the date column as the index
data.set_index('Date', inplace=True)

# Create a complete date range from the start date to the end date
complete_date_range = pd.date_range(start=data.index.min(), end=data.index.max(), freq='D')

# Reindex the dataframe to this complete date range
reindexed_data = data.reindex(complete_date_range)

# Find missing dates
missing_dates = reindexed_data[reindexed_data['Radiation(uSv/h)'].isna()].index

# Output missing dates if any
if not missing_dates.empty:
    print("Missing dates found:")
    print(missing_dates.date)
else:
    print("No missing dates found. All dates are present.")
