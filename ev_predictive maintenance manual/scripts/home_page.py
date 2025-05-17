
import streamlit as st
import streamlit as st
import pandas as pd
import joblib
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import random
from datetime import datetime

scaler = joblib.load('models/scaler.pkl')
model = joblib.load('models/battery_health_model.pkl')
def home_page():
    # Title and Image
    
   
    st.image('C:/Users/Hamelda Lourdus Mary/Downloads/image1.jpg', caption="Electric Vehicle - TATA Nexon")
        # Interactive Elements
        # Interactive Elements
    st.write("### Explore Your Vehicle")
    
    # Slider for Battery Status
    battery_status = st.slider(
        "Select Battery Status (%)", 
        min_value=0, 
        max_value=100, 
        value=85, 
        help="Adjust the slider to see different battery statuses."
    )
    
    # Dropdown for Vehicle Model
    vehicle_model = st.selectbox(
        "Choose Vehicle Model",
        options=["Tata-Nexon", "Tata-Harrier", "Tata-Tigor"],
        help="Select a vehicle model to see its specifications."
    )
    
    # Button for generating a report
    if st.button("Generate Report"):
        st.write(f"Generating report for {vehicle_model} with battery status at {battery_status}%...")
        # Add your report generation logic here
    
    st.write("---")    
    # Vehicle Specifications
    st.write("### Vehicle Specifications")
    
    st.markdown("""
        <style>
        .spec-box {
            background: linear-gradient(145deg, #1a1a2e, #16213e);
            padding: 20px;
            margin: 10px;
            border-radius: 8px;
            text-align: center;
            color: #ffffff;
        }
        .spec-icon {
            font-size: 30px;
        }
        </style>
        """, unsafe_allow_html=True)
    specific = [
        ("🚗", "Model", "Tata-Nexon"),
        ("📅", "Manufacture Year", "2022"),
        ("🔋", "Battery Status", "85%"),
        ("🖥", "CPU Load", "5%"),
        ("💾", "Memory Usage", "40%"),
        ("💽", "Hard Disk Space", "300/512 GB"),
        ("🌡", "Battery Temperature", "58°C"),
        ("🛡", "Warranty Expiration", "2026/11/15")
    ]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">🚗</div>
                <div>Model</div>
                <div>Tata-Nexon</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">📅</div>
                <div>Manufacture Year</div>
                <div>2022</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">🔋</div>
                <div>Battery Status</div>
                <div>85%</div>
            </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">🖥</div>
                <div>CPU Load</div>
                <div>5%</div>
            </div>
        """, unsafe_allow_html=True)

    col5, col6, col7, col8 = st.columns(4)

    with col5:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">💾</div>
                <div>Memory Usage</div>
                <div>40%</div>
            </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">💽</div>
                <div>Hard Disk Space</div>
                <div>300/512 GB</div>
            </div>
        """, unsafe_allow_html=True)

    with col7:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">🌡</div>
                <div>Battery Temperature</div>
                <div>58°C</div>
            </div>
        """, unsafe_allow_html=True)

    with col8:
        st.markdown("""
            <div class="spec-box">
                <div class="spec-icon">🛡</div>
                <div>Warranty Expiration</div>
                <div>2026/11/15</div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.write("---")

# Call the function to display the home page
