import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Define data paths
iot_data_path = "C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/training2024.csv"
sound_data_path = "C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/Sound_Data.csv"
maintenance_data_path = "C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/Maintenance_data.csv"

# Load data
iot_data = pd.read_csv(iot_data_path)
sound_data = pd.read_csv(sound_data_path)
maintenance_data = pd.read_csv(maintenance_data_path)

# Merge dataframes on "Date Created"
merged_data = pd.merge(maintenance_data, iot_data, on="Date Created")
merged_data = pd.merge(merged_data, sound_data, on="Date Created")

# Preprocess maintenance data
merged_data["Maintenance_Risk"] = merged_data["Data"] * 5

# Preprocess IoT data
merged_data["IoT_Risk"] = merged_data["Predicted Risk"] * 3

# Preprocess sound data
merged_data["Sound_Risk"] = merged_data["Risk level"] * 0.2

# Create DEIDEO features
features = merged_data["Maintenance_Risk"] + merged_data["IoT_Risk"] + merged_data["Sound_Risk"]

# Define the prediction function
def predict_risk_level(weighted_sum):
    if weighted_sum <= 4:
        return "Low Risk"
    elif weighted_sum <= 8:
        return "Medium Risk"
    else:
        return "High Risk"

# Apply the prediction function to each weighted sum
predictions = features.apply(predict_risk_level)

# Define function to convert maintenance value to string
def convert_maintenance_value(maintenance_value):
    return "Maintenance have been done" if maintenance_value == 0 else "No Maintenance"

# Apply the conversion function to "Maintenance" column
merged_data["Maintenance"] = merged_data["Data"].apply(convert_maintenance_value)

# Save the predictions to a CSV file
final_predictions = pd.DataFrame({
    "Index": np.arange(1, len(predictions) + 1),
    "Date Created": merged_data["Date Created"],
    "Maintenance": merged_data["Maintenance"],
    "IoT Risk level": merged_data["Predicted Risk"],
    "Sound Risk level": merged_data["Risk level"],
    "Predicted Risk Level": features,
    "Prediction": predictions
})

final_predictions.to_csv("C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/Final_Prediction2024.csv", index=False)
print("Final prediction saved to Final_Prediction.csv")
