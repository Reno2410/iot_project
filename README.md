# IoT Project - Final Project

## Overview
This project is an IoT-based final project focused on predicting crimes in real-time. The project uses crime data and weather data collected between **November 6, 2024** and **November 27, 2024**. The objective is to train a machine learning model to predict the likelihood of crime happening in a specific area based on real-time weather conditions and trigger a vibration alert for different levels of crime risk.

## Data Collected
- **Crime Data**: Contains crime types, locations, and timestamps for incidents recorded between **November 6, 2024**, and **November 27, 2024**.
- **Weather Data**: Includes weather conditions like temperature, humidity, wind speed, and weather descriptions for the same period.

## Objective
The goal of this project is to develop a machine learning model that predicts crime likelihood based on the historical crime and weather data. The system will then trigger a vibration alert based on the predicted level of risk:

- **Low Risk**: No alert triggered.
- **Moderate Risk**: A light vibration alert is triggered.
- **High Risk**: A stronger vibration alert is triggered.

This project serves as a **prototype**, demonstrating the potential of using IoT and machine learning to predict and respond to crime risk in real time.

## Features
- **Real-Time Crime Prediction**: Uses real-time weather data to predict the likelihood of a crime.
- **Vibration Alert System**: Triggers vibration alerts based on the predicted crime risk levels.
- **Machine Learning Model**: Trained using historical crime and weather data to make predictions.

## Installation and Setup
To get started with the project:

1. Clone this repository to your local machine.
2. Install necessary dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. Collect real-time weather data or use historical data to train the machine learning model.
4. Run the application to predict crime based on real-time weather and trigger vibration alerts.
