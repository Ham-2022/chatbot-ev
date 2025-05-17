import streamlit as st

def maintenance_alerts_page():
    st.title("Maintenance Alerts 🔔")

    st.subheader("tyre Change 🛞")
    oil_change_miles = 5000
    if st.button(f"Enable Oil Change (Every {oil_change_miles} miles)"):
        st.success(f"Oil Change reminder enabled every {oil_change_miles} miles!")

    st.subheader("Battery Check 🔋")
    battery_check_miles = 10000
    if st.button(f"Enable Battery Check (Every {battery_check_miles} miles)"):
        st.success(f"Battery Check reminder enabled every {battery_check_miles} miles!")

    st.subheader("Brake Inspection 🚦🚩")
    brake_inspection_miles = 15000
    if st.button(f"Enable Brake Inspection (Every {brake_inspection_miles} miles)"):
        st.success(f"Brake Inspection reminder enabled every {brake_inspection_miles} miles!")

    # Option to schedule a service
    st.subheader("Schedule Service")
    if st.button("Book Service"):
        st.session_state.page = "/schedule_service"
def show_notifications():
    if st.session_state.get("show_notifications", False):
        st.sidebar.write("### Notifications")
        
        notifications = [
            {"title": "Tata-Nexon: Battery below 50%", "page": "/battery_report"},
            {"title": "Tata-Tigor: High Temperature Alert", "page": "/maintenance_alerts"},
            {"title": "Tata-Harrier: Service Overdue", "page": "/schedule_service"}
        ]
        
        for notification in notifications:
            if st.sidebar.button(notification["title"]):  # Each notification is a button
                st.session_state.page = notification["page"]  # Open maintenance alerts page on click
                st.session_state.show_notifications = False  # Hide notifications after clicking
