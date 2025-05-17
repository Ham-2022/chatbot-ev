import streamlit as st
from datetime import datetime

def schedule_service_page():
    st.title('Schedule Service')

    # Updated data including India, its states, and Tamil Nadu cities
    countries = ['United States', 'Canada', 'United Kingdom', 'India']
    states = {
        'United States': ['New York', 'California', 'Texas'],
        'Canada': ['Ontario', 'Quebec', 'British Columbia'],
        'United Kingdom': ['England', 'Scotland', 'Wales'],
        'India': [
            'Tamil Nadu', 'Maharashtra', 'Karnataka', 'Delhi', 'Uttar Pradesh',
            'West Bengal', 'Gujarat', 'Rajasthan', 'Punjab', 'Haryana'
        ]
    }
    cities = {
        'New York': ['New York City', 'Buffalo', 'Rochester'],
        'California': ['Los Angeles', 'San Francisco', 'San Diego'],
        'Texas': ['Houston', 'Dallas', 'Austin'],
        'Ontario': ['Toronto', 'Ottawa', 'Hamilton'],
        'Quebec': ['Montreal', 'Quebec City', 'Laval'],
        'British Columbia': ['Vancouver', 'Victoria', 'Richmond'],
        'England': ['London', 'Manchester', 'Birmingham'],
        'Scotland': ['Edinburgh', 'Glasgow', 'Aberdeen'],
        'Wales': ['Cardiff', 'Swansea', 'Newport'],
        'Tamil Nadu': [
            'Chennai', 'Coimbatore', 'Madurai', 'Trichy', 'Salem',
            'Tirunelveli', 'Vellore', 'Erode', 'Nagercoil', 'Tirupur'
        ],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Aurangabad', 'Nashik'],
        'Karnataka': ['Bengaluru', 'Mysuru', 'Hubballi', 'Davanagere', 'Belagavi'],
        'Delhi': ['New Delhi', 'North Delhi', 'South Delhi', 'East Delhi', 'West Delhi'],
        'Uttar Pradesh': ['Lucknow', 'Kanpur', 'Agra', 'Varanasi', 'Ghaziabad'],
        'West Bengal': ['Kolkata', 'Siliguri', 'Howrah', 'Durgapur', 'Asansol'],
        'Gujarat': ['Ahmedabad', 'Surat', 'Vadodara', 'Rajkot', 'Gandhinagar'],
        'Rajasthan': ['Jaipur', 'Udaipur', 'Jodhpur', 'Kota', 'Bikaner'],
        'Punjab': ['Chandigarh', 'Amritsar', 'Ludhiana', 'Patiala', 'Jalandhar'],
        'Haryana': ['Gurugram', 'Faridabad', 'Ambala', 'Hisar', 'Karnal']
    }

    # Select country
    country = st.selectbox('Choose a country', countries)

    # Based on selected country, select state
    state = st.selectbox('Choose a state', states[country])

    # Based on selected state, select city
    city = st.selectbox('Choose a city', cities.get(state, []))

    # Enter pincode
    pincode = st.text_input('Enter pincode')

    # Choose a date to schedule
    schedule_date = st.date_input('Select date to schedule', min_value=datetime.today())

    # Button to confirm scheduling
    if st.button('Schedule'):
        if pincode:
            st.success('Scheduling completed!')
            st.write(f'Schedule Information:\nCountry: {country}\nState: {state}\nCity: {city}\nPincode: {pincode}\nDate: {schedule_date}')
        else:
            st.error('Please enter a valid pincode.')

    # Button to go back to the main page
    if st.button("return to chatbot"):
        st.session_state.page="chatbot"
    