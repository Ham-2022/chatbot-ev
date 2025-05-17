import streamlit as st
import pandas as pd

# Function for fetching EV car details from CSV based on VIN
def get_ev_car_details_from_csv(vin):
    # Load CSV data
    data = pd.read_csv("C:/Users/Hamelda Lourdus Mary/Downloads/ev_predictive maintenance manual/data/ev_car_data.csv")

    
    # Search for the VIN in the data
    car_data = data[data["VIN"] == vin]
    
    # If VIN found, return details as dictionary
    if not car_data.empty:
        car_details = car_data.iloc[0].to_dict()  # Convert the row to dictionary
        return car_details
    else:
        return None

def user_profile():
    st.markdown("""
        <h1 style='text-align: center;'>User Profile</h1>
    """, unsafe_allow_html=True)

    # VIN registration section
    st.subheader("Register Vehicle Identification Number (VIN)")
    vin = st.text_input("Enter VIN number")

    if vin:
        # Fetch and display car details from CSV
        car_details = get_ev_car_details_from_csv(vin)
        
        if car_details:
            st.subheader(f"Car Details for VIN: {vin}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"🔋 Battery: {car_details['Battery Status']}")
                st.write(f"🖥 CPU Load: {car_details['CPU Load']}")

            with col2:
                st.write(f"💾 Memory Usage: {car_details['Memory Usage']}")
                st.write(f"🌡 Battery Temp: {car_details['Battery Temperature']}")

            with col3:
                st.write(f"💽 Hard Disk Space: {car_details['Hard Disk Space']}")

            st.write("---")
            st.write(f"🚗 Model: {car_details['Model']}")
            st.write(f"📅 Year of Manufacture: {car_details['Manufacture Year']}")
            st.write(f"🛡 Warranty Expiration: {car_details['Warranty Expiration']}")
        else:
            st.error(f"No car details found for VIN: {vin}")
    else:
        st.info("Please enter your VIN number to see vehicle details.")
    
    st.write("---")

    # Profile management
    st.subheader("Manage Account")
    email = st.text_input("Email")
    old_password = st.text_input("Old Password", type="password")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    # Submit button
    if st.button("Update Profile"):
        st.success("Profile updated successfully.")
    
    # Battery status progress
    st.subheader("Battery Status")
    st.progress(75)  # Example progress bar set at 75%

    # Help & Support Section
    st.subheader("Help & Support")
    issue_description = st.text_area("Describe your issue")

    if st.button("Submit Issue"):
        st.success("Your issue has been submitted successfully.")

# Run the Streamlit app
if __name__ == '__main__':
    user_profile()
