import streamlit as st
from battery_report_page import battery_report_page
from home_page import home_page
from schedule_service_page import schedule_service_page
from battery_page import battery_page
from maintenance_alerts_page import maintenance_alerts_page
from fleet_manager_page import fleet_manager_pager
from pdf_generator import generate_pdf
from maintenance_alerts_page import show_notifications

import requests
import pyttsx3
import threading
import speech_recognition as sr
import firebase_admin
from firebase_admin import credentials, firestore
import plotly.express as px

# Firebase Initialization
if not firebase_admin._apps:
    cred = credentials.Certificate("teamsparks-99b77-f8d6b9dfd5c3.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# Gemini API Configuration
API_KEY = "AIzaSyC2AKBIqOuBF53K4PG7hTv24dp_5Rc2byg"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"

# Text-to-Speech Setup
engine = pyttsx3.init()
recognizer = sr.Recognizer()

def speak_text(text):
    def run_speak():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run_speak).start()

def capture_voice_input():
    with sr.Microphone() as source:
        st.info("Listening...")
        audio = recognizer.listen(source)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Speech recognition error: {e}")
    return None

# Correct Gemini request function
def send_gpt4_request(user_query):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": user_query}
                ]
            }
        ]
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except requests.RequestException as e:
        st.error(f"Request error: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
    return None

# Firebase User Auth
def register_user(email, password):
    try:
        db.collection('users').document(email).set({'password': password})
        st.success("User registered!")
    except Exception as e:
        st.error(f"Registration error: {e}")

def login_user(email, password):
    doc = db.collection('users').document(email).get()
    if doc.exists and doc.to_dict().get('password') == password:
        st.session_state.logged_in = True
        st.session_state.email = email
        st.session_state.page = "vin_registration"
        st.success("Login successful!")
        return True
    st.error("Invalid email or password.")
    return False

# Fetch VIN
def fetch_vin_data_flat(vin, model_year=None):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinValues/{vin}?format=json"
    if model_year:
        url += f"&modelyear={model_year}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json().get("Results", [])
        except ValueError:
            st.error("Error decoding JSON.")
    else:
        st.error("Failed to fetch VIN data.")
    return []

def save_vin(vin):
    try:
        db.collection('vins').add({'vin': vin, 'email': st.session_state.email})
        st.success("VIN saved.")
    except Exception as e:
        st.error(f"Error saving VIN: {e}")

# Pages
def vin_registration_page():
    st.title("VIN Registration")
    vin = st.text_input("Enter VIN")
    model_year = st.text_input("Model Year (optional)", "")
    if st.button("Submit VIN"):
        car_data = fetch_vin_data_flat(vin, model_year)
        if car_data:
            st.write("Manufacturer:", car_data[0].get("Make", "N/A"))
            st.write("Model:", car_data[0].get("Model", "N/A"))
            st.write("Year:", car_data[0].get("ModelYear", "N/A"))
            save_vin(vin)
    if st.button("Return to Chatbot"):
        st.session_state.page = "chatbot"

def login_page():
    st.title("EV Login / Registration")
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "page" not in st.session_state:
        st.session_state.page = "login"

    if not st.session_state.logged_in:
        option = st.sidebar.selectbox("Choose", ["Login", "Register"])
        email = st.text_input("Email")
        password = st.text_input("Password", type='password')

        if option == "Register" and st.button("Register"):
            register_user(email, password)

        if option == "Login" and st.button("Login"):
            if login_user(email, password):
                st.session_state.logged_in = True
    else:
        vin_registration_page()

# Chatbot
def chatbot():
    st.title("🤖 EV Gemini Chatbot")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = None
    method = st.radio("Choose Input Method", ["Text", "Voice"])

    if method == "Voice":
        if st.button("Speak"):
            user_input = capture_voice_input()
            if user_input:
                st.success(f"You said: {user_input}")
    else:
        user_input = st.chat_input("Ask something about EVs...")

    if user_input and user_input.strip():
        st.chat_message("user").markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        gpt_response = send_gpt4_request(user_input)

        if gpt_response:
            st.chat_message("assistant").markdown(gpt_response)
            st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
            speak_text(gpt_response)
        else:
            st.error("No response from Gemini.")

# Navigation
def navigation_switch(page):
    pages = {
        "/home": home_page,
        "/battery_report": battery_report_page,
        "/schedule_service": schedule_service_page,
        "/battery_station": battery_page,
        "/maintenance_alerts": maintenance_alerts_page,
        "/fleet_manager": fleet_manager_pager
    }
    return pages.get(page.lower(), chatbot)

def add_header():
    col1, col2, col3, col4 = st.columns([1, 6, 1, 1])
    with col1:
        st.image("logo.jpg", width=50)
    with col3:
        st.image("profile_icon.png", width=40)
    with col4:
        if st.button("🔔"):
            st.session_state.show_notifications = not st.session_state.get("show_notifications", False)

# Main
def main():
    add_header()
    show_notifications()

    if "page" not in st.session_state:
        st.session_state.page = "login"

    page = st.session_state.page
    if page == "login":
        login_page()
    elif page == "vin_registration":
        vin_registration_page()
    elif page == "chatbot":
        chatbot()
    else:
        navigation_page = navigation_switch(page)
        navigation_page()

if __name__ == "__main__":
    main()
