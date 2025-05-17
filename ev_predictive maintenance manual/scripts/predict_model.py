import joblib
import pandas as pd

def predict_battery_health(voltage, current, temperature, state_of_charge):
    # Load model and scaler
    model = joblib.load('models/battery_health_model.pkl')
    scaler = joblib.load('models/scaler.pkl')

    # Prepare input data
    input_data = pd.DataFrame([[voltage, current, temperature, state_of_charge]],columns=['voltage', 'current', 'temperature', 'state_of_charge'])
    input_data_scaled = scaler.transform(input_data)
    
    # Predict
    prediction = model.predict(input_data_scaled)
    return prediction[0]
