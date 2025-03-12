import streamlit as st
import requests
from datetime import datetime
import pandas as pd

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
st.map(map_data)  # Render the map using the DataFrame

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
