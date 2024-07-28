import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler

# Load the testing data
testing_data = pd.read_csv('C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@IoT_data.csv', encoding='latin1')

# Extract relevant parameters for testing
X_test = testing_data[['Radiation(uSv/h)', 'Temperature(°C)', 'Humidity(%)', 'CO2(ppm)', 'Battery', 'RSSI', 'loRaSNR', 'Frequency']]

y = testing_data['Actual Risk']

# Standardize features using the same scaler used in training
scaler = StandardScaler()
X_test_scaled = scaler.fit_transform(X_test)

# Load the trained model
model = tf.keras.models.load_model('C:/Users/PC/Desktop/FYP/Final Code/IoT/Training/trained_model.keras')

# Predict risk levels for the entire dataset
predicted_risk_levels = model.predict(X_test_scaled).flatten()

# Cap the predicted risk levels between 0 and 1
predicted_risk_levels = np.clip(predicted_risk_levels, 0, 1)

# Add predicted risk levels to the original data
testing_data['Predicted Risk'] = predicted_risk_levels

# Define risk level categories based on discretization
def discretize_risk_level(risk_level):
    if risk_level < 0.3:
        return 0  # Low risk
    elif 0.3 <= risk_level <= 0.7:
        return 1  # Medium risk
    else:
        return 2  # High risk

# Apply discretization to predicted risk levels
predicted_categories = [discretize_risk_level(risk_level) for risk_level in predicted_risk_levels]

# Discretize actual risk levels
actual_categories = [discretize_risk_level(risk_level) for risk_level in y]

# Compute confusion matrix
confusion = tf.math.confusion_matrix(actual_categories, predicted_categories, num_classes=3)

# Compute accuracy
accuracy = np.trace(confusion) / np.sum(confusion)

print("Confusion Matrix:")
print(confusion.numpy())
print("Accuracy:", accuracy)

# Convert confusion matrix to DataFrame
confusion_df = pd.DataFrame(confusion.numpy(), index=['Low', 'Medium', 'High'], columns=['Low', 'Medium', 'High'])

# Create DataFrame for accuracy
accuracy_df = pd.DataFrame({'Accuracy': [accuracy]}, index=[''])

# Concatenate confusion matrix and accuracy DataFrames
result_df = pd.concat([confusion_df, accuracy_df], axis=0)

# Reset the index to start from 1 and add it as a column
result_df.reset_index(drop=True, inplace=True)
result_df.index = result_df.index + 1

# Save combined DataFrame to CSV file without the default index
result_df.to_csv('C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Testing_confusion_matrix_and_accuracy.csv', index_label='Index')

# Save the updated data with predictions to a new CSV file without the default index
testing_data.reset_index(drop=True, inplace=True)
testing_data.index = testing_data.index + 1
testing_data.to_csv('C:/Users/PC/Desktop/FYP/Final Code/IoT/Test@Data/Test@IoT_data_with_predictions.csv')
