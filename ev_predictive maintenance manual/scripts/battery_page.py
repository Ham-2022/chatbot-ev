import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.distance import geodesic
import geocoder  # Library to get the live location

# Azure Maps API key
AZURE_MAPS_KEY = '9Mt72Mwi4JbWJaQ7sjtWVVfg8tndkdaKEYHiXDajSZBP7GhLFAUnJQQJ99AIACYeBjFF8uudAAAgAZMPfN4A'  # Replace with your Azure Maps key

# Sample data for battery locations (latitude, longitude)
battery_locations = [
    {"name": "Battery Station 1", "lat": 13.0827, "lon": 80.2707},
    {"name": "Battery Station 2", "lat": 16.0878, "lon": 80.2785},
    {"name": "Battery Station 3", "lat": 13.0900, "lon": 80.2900},
    {"name": "Battery Station 4", "lat": 13.0950, "lon": 80.2950},
]

# Create dataframe for Pydeck
battery_locations_df = pd.DataFrame(battery_locations)

def battery_page():
    # Function to get live location
    def get_live_location():
        g = geocoder.ip('me')
        return g.latlng  # Returns [latitude, longitude]

    # Function to calculate the route using Azure Maps Route API
    def calculate_route(start_lat, start_lon, end_lat, end_lon):
        route_url = f"https://atlas.microsoft.com/route/directions/json?api-version=1.0&query={start_lat},{start_lon}:{end_lat},{end_lon}&subscription-key={AZURE_MAPS_KEY}&traffic=true"
        route_data = requests.get(route_url).json()

        if 'routes' in route_data and route_data['routes']:
            route_geometry = route_data['routes'][0]['legs'][0]['points']
            traffic_summary = route_data['routes'][0]['legs'][0]['summary']
            return route_geometry, traffic_summary

        return None, None

    # Function to display map with route and markers
    def display_map(route_geometry, traffic_summary, live_location, nearest_station):
        # Create base map
        m = folium.Map(location=live_location, zoom_start=14)

        # Add marker for live location
        folium.Marker(
            location=live_location,
            popup="Your Live Location",
            icon=folium.Icon(color='blue', icon='info-sign', prefix='fa')
        ).add_to(m)

        # Add markers for battery stations
        for station in battery_locations:
            folium.Marker(
                location=[station['lat'], station['lon']],
                popup=f"Battery Station: {station['name']}",
                icon=folium.Icon(color='red', icon='bolt', prefix='fa')
            ).add_to(m)

        # Plot the route points on the map
        if route_geometry:
            route_coords = [(point['latitude'], point['longitude']) for point in route_geometry]

            # Highlight route with traffic conditions
            if traffic_summary:
                traffic_delay = traffic_summary.get('trafficDelayInSeconds', 0)
                distance = traffic_summary.get('lengthInMeters', 0) / 1000  # Convert to kilometers
                duration = traffic_summary.get('travelTimeInSeconds', 0) / 60  # Convert to minutes
                st.write(f"Traffic Summary: Distance = {distance:.2f} km, Duration = {duration:.2f} minutes, Traffic Delay = {traffic_delay} seconds")
                color = 'green' if traffic_delay == 0 else 'orange'
                folium.PolyLine(route_coords, color=color, weight=6, opacity=0.7, dash_array='5,5').add_to(m)
            else:
                folium.PolyLine(route_coords, color="blue", weight=6, opacity=0.7).add_to(m)

            # Add marker for nearest battery station
            folium.Marker(
                location=[nearest_station['lat'], nearest_station['lon']],
                popup=f"Nearest Battery Station: {nearest_station['name']}",
                icon=folium.Icon(color='red', icon='bolt', prefix='fa')
            ).add_to(m)

        # Render the map
        folium_static(m)

    # Function to calculate nearest battery station from live location
    def calculate_nearest_battery_station(live_location):
        min_distance = float("inf")
        nearest_station = None
        for station in battery_locations:
            distance = geodesic(live_location, (station["lat"], station["lon"])).km
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
        return nearest_station

    # Streamlit app
    st.title("Route and Location Mapping Application")

    # Get live location
    live_location = get_live_location()
    st.write(f"Your live location: {live_location}")

    if live_location:
        nearest_station = calculate_nearest_battery_station(live_location)

        if nearest_station:
            st.write(f"Nearest Battery Station: {nearest_station['name']} at ({nearest_station['lat']}, {nearest_station['lon']})")

            # Calculate route from live location to nearest battery station
            route_geometry, traffic_summary = calculate_route(live_location[0], live_location[1], nearest_station['lat'], nearest_station['lon'])

            if route_geometry:
                display_map(route_geometry, traffic_summary, live_location, nearest_station)

                # Notify if already at the nearest station
                if (live_location[0], live_location[1]) == (nearest_station['lat'], nearest_station['lon']):
                    st.success("You have reached the nearest battery station!")
            else:
                st.error("Could not calculate route. Please try again.")
        else:
            st.error("No nearest battery station found. Please try again.")
    else:
        st.error("Could not retrieve live location. Please try again.")
    if st.button("Return to Chatbot"):
        st.session_state.page = "Chatbot"
