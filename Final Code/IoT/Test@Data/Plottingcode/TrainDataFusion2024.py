import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import pickle

#Define file paths
data_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@IoT_data.csv'
training_data_with_predictions_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/training2024.csv'
scaler_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/scaler.pkl'
model_path = 'C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Plottingcode/trained_model.keras'

#Load the training data with the appropriate date parsing format
training_data = pd.read_csv(data_path, parse_dates=['Date Created'], dayfirst=True, infer_datetime_format=True, encoding='latin1')

#Filter data for training period (1 January 2024 until 31 May 2024)
training_data = training_data[(training_data['Date Created'] >= '2024-01-01') & (training_data['Date Created'] <= '2024-05-31')]

#Exclude data points with missing values
training_data = training_data.dropna()

#Extract relevant parameters for training
X = training_data[['Radiation(uSv/h)', 'Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency']]

#Extract the actual risk column
y = training_data['Actual Risk']

#Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#Define the ANN model for regression
model = tf.keras.models.Sequential([
tf.keras.layers.Dense(64, activation='relu', input_shape=(X.shape[1],)),
tf.keras.layers.Dense(32, activation='relu'),
tf.keras.layers.Dense(1, activation='linear')
])

#Compile the model
model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])

#Train the model
history = model.fit(X_scaled, y, epochs=300, batch_size=32)

#Collect parameter statistics
parameter_means = X.mean()
parameter_std = X.std()
parameter_stats = {
'Parameter': X.columns,
'Mean': parameter_means,
'Standard Deviation': parameter_std
}

#Save training history to a DataFrame
history_df = pd.DataFrame(history.history)

#Save parameter statistics to a DataFrame
parameter_stats_df = pd.DataFrame(parameter_stats)

#Combine all the data into a single DataFrame
combined_df = pd.concat([history_df, parameter_stats_df], axis=1)

#Reset the index to start from 1 and add it as a column
combined_df.reset_index(drop=True, inplace=True)
combined_df.index = combined_df.index + 1


#Predict risk levels for the entire dataset
predicted_risk_levels = model.predict(X_scaled).flatten()

#Cap the predicted risk levels between 0 and 1
predicted_risk_levels = np.clip(predicted_risk_levels, 0, 1)

#Add predicted risk levels to the original data
training_data['Predicted Risk'] = predicted_risk_levels

# Define risk level categories based on discretization
def discretize_risk_level(risk_level):
    if risk_level < 0.3:
        return 0  # Low risk
    elif 0.3 <= risk_level <= 0.7:
        return 1  # Medium risk
    else:
        return 2  # High risk

#Apply discretization to predicted risk levels
predicted_categories = [discretize_risk_level(risk_level) for risk_level in predicted_risk_levels]

#Discretize actual risk levels
actual_categories = [discretize_risk_level(risk_level) for risk_level in y]

#Compute confusion matrix
confusion = tf.math.confusion_matrix(actual_categories, predicted_categories, num_classes=3)

#Compute accuracy
accuracy = np.trace(confusion) / np.sum(confusion)

print("Confusion Matrix:")
print(confusion.numpy())
print("Accuracy:", accuracy)

#Convert confusion matrix to DataFrame
confusion_df = pd.DataFrame(confusion.numpy(), index=['Low', 'Medium', 'High'], columns=['Low', 'Medium', 'High'])

#Create DataFrame for accuracy
accuracy_df = pd.DataFrame({'Accuracy': [accuracy]}, index=[''])

#Concatenate confusion matrix and accuracy DataFrames
result_df = pd.concat([confusion_df, accuracy_df], axis=0)

#Reset the index to start from 1 and add it as a column
result_df.reset_index(drop=True, inplace=True)
result_df.index = result_df.index + 1


#Save the updated data with predictions to a new CSV file without the default index
training_data.reset_index(drop=True, inplace=True)
training_data.index = training_data.index + 1
training_data.to_csv(training_data_with_predictions_path)

# Save the scaler after fitting
with open(scaler_path, 'wb') as f:
    pickle.dump(scaler, f)

#Save the model
model.save(model_path)