import streamlit as st

# Sample fleet manager profiles (can be extended)
fleet_managers = [
    {
        'name': 'John Doe',
        'rating': 4.5,
        'services': ['Battery Health Monitoring', 'Predictive Maintenance'],
        'contact': 'john.doe@example.com'
    },
    {
        'name': 'Jane Smith',
        'rating': 4.8,
        'services': ['Route Optimization', 'Service Scheduling'],
        'contact': 'jane.smith@example.com'
    },
    {
        'name': 'Michael Brown',
        'rating': 4.2,
        'services': ['Fleet Maintenance', 'EV Charging Assistance'],
        'contact': 'michael.brown@example.com'
    },
    {
        'name': 'Emily Davis',
        'rating': 4.9,
        'services': ['Battery Health Monitoring', 'EV Charging Assistance'],
        'contact': 'emily.davis@example.com'
    }
]

def fleet_manager_pager():
    """
    Display a list of fleet managers, allow the user to select one,
    and send a message to the selected manager.
    """
    

    # User input to select a fleet manager by name
    selected_manager_name = st.selectbox(
        "Select a Fleet Manager by Name",
        [manager['name'] for manager in fleet_managers]
    )

    # Get selected fleet manager details
    selected_manager = next((manager for manager in fleet_managers if manager['name'] == selected_manager_name), None)

    if selected_manager:
        st.write(f"**Selected Manager**: {selected_manager['name']}")
        st.write(f"**Rating**: {selected_manager['rating']} ⭐")
        st.write(f"**Services**: {', '.join(selected_manager['services'])}")
        st.write(f"**Contact**: {selected_manager['contact']}")

        # Allow user to send a message to the fleet manager
        message = st.text_area(f"Send a message to {selected_manager['name']}:")
        
        if st.button("Send Message"):
            if message:
                st.success(f"Message sent to {selected_manager['name']} at {selected_manager['contact']}")
            else:
                st.warning("Please write a message before sending.")
    if st.button("Return to Chatbot"):
        st.session_state.page = "Chatbot"

