import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go
import plotly.express as px
from pdf_generator import generate_pdf
import numpy as np

# Load model and scaler
scaler = joblib.load('models/scaler.pkl')
model = joblib.load('models/battery_health_model.pkl')

def predict_battery_health(voltage, current, temperature, state_of_charge):
    input_data = pd.DataFrame({
        'voltage': [voltage],
        'current': [current],
        'temperature': [temperature],
        'state_of_charge': [state_of_charge]
    })
    
    input_data_scaled = scaler.transform(input_data)
    prediction = model.predict(input_data_scaled)
    
    return prediction[0]

def battery_report_page():
    st.header("Battery Health Report")

    # Initialize session state variables if not already set
    if 'voltage' not in st.session_state:
        st.session_state.voltage = 3.7
        st.session_state.current = 1.2
        st.session_state.temperature = 25
        st.session_state.state_of_charge = 80

    # Input fields
    st.session_state.voltage = st.number_input('Voltage (V)', min_value=0.0, value=st.session_state.voltage)
    st.session_state.current = st.number_input('Current (A)', min_value=0.0, value=st.session_state.current)
    st.session_state.temperature = st.number_input('Temperature (°C)', min_value=-50, value=st.session_state.temperature)
    st.session_state.state_of_charge = st.number_input('State of Charge (%)', min_value=0, max_value=100, value=st.session_state.state_of_charge)

    # Automatically predict battery health when inputs change
    try:
        # Predict battery health
        health_prediction = predict_battery_health(
            st.session_state.voltage, 
            st.session_state.current, 
            st.session_state.temperature, 
            st.session_state.state_of_charge
        )
        health_prediction = max(0, min(1, health_prediction))
        st.write(f'Predicted Battery Health: {health_prediction * 100:.2f}%')

        # Plotting the Pie Chart
        st.write("Battery Health Overview")
        fig = go.Figure(data=[go.Pie(
            labels=['Health', 'Remaining'],
            values=[health_prediction, 1 - health_prediction],
            hole=0.4,
            marker=dict(colors=['#00cc96', '#e3e3e3']),
            textinfo='label+percent',
            textfont_size=20,
            showlegend=False
        )])
        fig.update_layout(
            title_text='Battery Health Overview',
            annotations=[dict(
                text=f'{health_prediction * 100:.2f}%', 
                x=0.5, 
                y=0.5, 
                font_size=24, 
                showarrow=False
            )]
        )
        st.plotly_chart(fig)

        # Warning based on health prediction
        if health_prediction < 0.3:
            st.warning("⚠️ Critical: Battery health is poor. Immediate replacement is recommended.")
        elif health_prediction < 0.6:
            st.warning("⚠️ Caution: Battery health is moderate. Consider monitoring or replacing soon.")
        else:
            st.success("✅ Good: Battery health is acceptable. No immediate action needed.")

        # Historical Battery Health Trends
        st.write("Historical Battery Health Trends")
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        values = [health_prediction + (np.random.uniform(-0.1, 0.1)) for _ in dates]
        historical_df = pd.DataFrame({'Date': dates, 'Health Score': values})

        fig = px.line(historical_df, x='Date', y='Health Score', title='Battery Health Over Time', labels={'Health Score': 'Health Score'})
        st.plotly_chart(fig)

        # Generate and download PDF report
        pdf_buffer = generate_pdf(st.session_state.voltage, st.session_state.current, st.session_state.temperature, st.session_state.state_of_charge, health_prediction)
        st.download_button(
            label="Download Battery Report",
            data=pdf_buffer,
            file_name="battery_health_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.write(f'Error: {e}')
    if st.button("Return to Chatbot"):
        st.session_state.page = "Chatbot"
