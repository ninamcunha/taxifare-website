import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import folium
from streamlit_folium import folium_static

# Custom CSS for gay flag header and pink button
st.markdown(
    """
    <style>
    /* Add a horizontal gay flag as a header */
    .header {
        width: 100%;
        height: 50px;
        background: linear-gradient(
            to right,
            #FF0018, #FFA52C, #FFFF41, #008018, #0000F9, #86007D
        );
        margin-bottom: 20px;
    }

    /* Style the button */
    .stButton button {
        font-size: 20px !important;
        background-color: #FF69B4 !important; /* Pink background */
        color: white !important; /* White text */
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    </style>
    <div class="header"></div>
    """,
    unsafe_allow_html=True
)

st.title("Taxi Fare Predictor")

st.markdown('''
### Enter ride details to get a fare prediction:
''')

# Ensure the date_time persists across reruns
if "date_time" not in st.session_state:
    st.session_state.date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

date_time = st.text_input("Date & Time (YYYY-MM-DD HH:MM:SS)", st.session_state.date_time)

pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=8, value=1, step=1)

# Prepare data for the map
map_data = pd.DataFrame({
    "lat": [pickup_latitude, dropoff_latitude],  # Latitude values
    "lon": [pickup_longitude, dropoff_longitude]  # Longitude values
})

# Display the map
st.markdown("### Ride Locations on Map")
#st.map(map_data)  # Render the map using the DataFrame
m = folium.Map(location=[pickup_latitude, pickup_longitude], zoom_start=13)

# Add markers for pickup and dropoff locations
folium.Marker(
    location=[pickup_latitude, pickup_longitude],
    popup="Pickup Location",
    icon=folium.Icon(color="green", icon="info-sign")
).add_to(m)

folium.Marker(
    location=[dropoff_latitude, dropoff_longitude],
    popup="Dropoff Location",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Display the folium map
folium_static(m)

# API URL
url = 'https://taxifare.lewagon.ai/predict'

# Prepare API request
params = {
    "pickup_datetime": date_time,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

# Call API
if st.button("Predict Fare"):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        prediction = response.json().get("fare", "Error retrieving prediction")
        st.success(f"Estimated Fare: ${prediction:.2f}")
    else:
        st.error("Error calling the API. Please try again.")
