from flask import Flask, render_template, request, jsonify
import pandas as pd
from prediction import predict_crime, prepare_features, send_alert
from utils import get_weather_data
from visualization import generate_interactive_charts_and_map, generate_interactive_new_charts

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualization')
def visualization():
    # Assume the data file is 'data/crime data 1106-1127 cleaned to visualize.csv'
    crime_data = pd.read_csv('data/crime data 1106-1127 cleaned to visualize.csv')
    merged_data = pd.read_csv('data/crime weather merge.csv')
    # Ensure 'CrimeDateTime' is in datetime format
    crime_data['CrimeDateTime'] = pd.to_datetime(crime_data['CrimeDateTime'])
    # Call function to generate charts and map
    chart_paths = generate_interactive_charts_and_map(crime_data).append(generate_interactive_new_charts(merged_data))
    return render_template('visualization.html', charts=chart_paths)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        latitude = float(request.form['latitude'])
        longitude = float(request.form['longitude'])

        # Get real-time weather data
        weather_data = get_weather_data(latitude, longitude)

        # Prepare input features
        input_data = {
            'temp': weather_data['temp'],
            'feels_like': weather_data['feels_like'],
            'humidity': weather_data['humidity'],
            'wind_speed': weather_data['wind_speed'],
            'clouds_all': weather_data['clouds_all'],
            'DayOfWeek': weather_data['DayOfWeek'],
            'Hour': weather_data['Hour'],
            'Latitude': latitude,
            'Longitude': longitude,
            'weather_description': weather_data['weather_description']  # Add weather_description
        }
        features = prepare_features(input_data)

        # Predict crime type and probability
        predicted_crime, probability = predict_crime(features)

        # Recommendation
        if probability <= 0.1:
            recommendation = "The area is very safe within the next hour. Feel free to go out."
        elif probability <= 0.5:
            recommendation = "There might be a crime incident nearby. Please stay cautious!"
        else:
            recommendation = "Be very careful going out. It's better to avoid going outside if possible."
        
        # Call send_alert to trigger the buzzer based on probability
        send_alert(probability)

        # Return JSON response
        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "weather_data": weather_data,
            "predicted_crime": predicted_crime,
            "probability": probability,
            "recommendation": recommendation
        })

    return render_template('prediction.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
