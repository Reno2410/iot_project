import pickle
import pandas as pd
import numpy as np
import serial
import time

# Load the pre-trained model
model = pickle.load(open('models/crime_prediction_model.pkl', 'rb'))

# Load the label encoder for crime type decoding
label_encoder = pickle.load(open('models/label_encoder.pkl', 'rb'))

# Load feature columns
with open('models/feature_columns.pkl', 'rb') as fc_file:
    feature_columns = pickle.load(fc_file)

# Load OneHotEncoder (if applicable)
with open('models/onehot_encoder.pkl', 'rb') as ohe_file:
    onehot_encoder = pickle.load(ohe_file)

# New values that are not in historical data
WEATHER_SYNONYMS = {
    'clear sky': 'sky is clear'
}

def prepare_features(input_data):
    """
    Prepare input features to match the model's training set format.
    """
    # Handle one-hot encoding for weather_description
    if 'weather_description' in input_data:
        input_data['weather_description'] = WEATHER_SYNONYMS.get(
            input_data['weather_description'], 
            input_data['weather_description']
        )
        weather_encoded = onehot_encoder.transform([[input_data['weather_description']]]).toarray()
        weather_columns = [f"weather_{cat}" for cat in onehot_encoder.categories_[0]]
        weather_df = pd.DataFrame(weather_encoded, columns=weather_columns)
        input_data.update(weather_df.to_dict(orient='records')[0])

    # Convert input data to DataFrame and align with feature columns
    input_sample = pd.DataFrame([input_data])
    input_sample = input_sample.reindex(columns=feature_columns, fill_value=0)
    return input_sample

def predict_crime(features):
    """
    Predict the crime type and probabilities.
    """
    probabilities = model.predict_proba(features)[0]
    predicted_crime_index = np.argmax(probabilities)
    predicted_crime = label_encoder.inverse_transform([predicted_crime_index])[0]
    return predicted_crime, probabilities[predicted_crime_index]

# Initialize serial port
time.sleep(2)  
ser = serial.Serial('COM7', 9600)  # Replace '/dev/ttyUSB0' with the actual serial port address

if not ser.is_open:
    ser.open()  

def send_alert(probability):
    if probability > 0.5:
        ser.write(b'2')  # Fast buzzer signal
    elif probability > 0.1:
        ser.write(b'1')  # Slow buzzer signal
    else:
        ser.write(b'0')  # No buzzer signal
