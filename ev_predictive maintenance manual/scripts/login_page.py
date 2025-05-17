import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase only if not already initialized
if not firebase_admin._apps:
    cred = credentials.Certificate("teamsparks-99b77-f8d6b9dfd5c3.json")  # Replace with your path
    firebase_admin.initialize_app(cred)

db = firestore.client()

# Function to register a user
def register_user(email, password):
    try:
        db.collection('users').document(email).set({
            'password': password
        })
        st.success("User registered successfully!")
    except Exception as e:
        st.error(f"Error registering user: {e}")

# Function to authenticate user
def login_user(email, password):
    user_doc = db.collection('users').document(email).get()
    if user_doc.exists and user_doc.to_dict().get('password') == password:
        st.session_state.logged_in = True
        st.session_state.email = email
        st.session_state.page = "chatbot"  # Set to chatbot after login
        st.success("Login successful!")
        return True
    else:
        st.error("Invalid email or password.")
        return False

# Function to fetch VIN data for a single VIN in flat format
def fetch_vin_data_flat(vin, model_year=None):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    if model_year:
        url += f"&modelyear={model_year}"

    response = requests.get(url)

    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("Results", [])
        except ValueError:
            st.error("Error decoding JSON response.")
            return []
    else:
        st.error(f"Failed to fetch data. Status Code: {response.status_code} - {response.text}")
        return []

# Function to save VIN to Firestore
def save_vin(vin):
    try:
        db.collection('vins').add({
            'vin': vin,
            'email': st.session_state.email
        })
        st.success("VIN saved successfully!")
    except Exception as e:
        st.error(f"Error saving VIN: {e}")

# Streamlit app
def login_page():
    st.title("EV Registration and Login")

    # Initialize session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Select Activity", menu)

        if choice == "Register":
            st.subheader("Register")
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')
            if st.button("Register"):
                register_user(email, password)

        elif choice == "Login":
            st.subheader("Login")
            email = st.text_input("Email")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                if login_user(email, password):
                    st.session_state.logged_in = True

    else:
        st.subheader(f"Welcome, {st.session_state.email}!")
        
        # VIN Registration
        st.subheader("VIN Registration")
        vin = st.text_input("Enter VIN")
        model_year = st.text_input("Model Year (optional)", "")
        if st.button("Submit VIN"):
            car_data = fetch_vin_data_flat(vin, model_year)
            if car_data:
                st.write("Manufacturer:", car_data[0].get("Make", "N/A"))
                st.write("Model:", car_data[0].get("Model", "N/A"))
                st.write("Year:", car_data[0].get("ModelYear", "N/A"))
                save_vin(vin)

                # Button to return to Chatbot
                if st.button("Return to Chatbot"):
                    st.session_state.page = "chatbot"

    # Chatbot navigation
    if st.session_state.page == "chatbot":
        st.write("Navigating to the Chatbot...")
        # Implement your chatbot code here

# Call login page on app start
