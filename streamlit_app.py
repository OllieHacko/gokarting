import streamlit as st
import requests
from datetime import datetime

# Streamlit setup
st.set_page_config(page_title="GoKarting Weather 3.5", page_icon="🏎️", layout="centered")

# Load image as a placeholder
st.image("Untitled1.png", use_column_width=True)

# List of karting tracks
tracks = [
    {"Name": "Auckland", "lat": -36.8636448, "lon": 174.6622602},
    {"Name": "Hamilton", "lat": -37.8640908, "lon": 175.3403989},
    {"Name": "Tokoroa", "lat": -38.2395133, "lon": 175.892994},
    {"Name": "Wellington", "lat": -41.0860711, "lon": 175.1748693},
    {"Name": "Rotorua", "lat": -38.0650655, "lon": 176.0469196},
    {"Name": "Canterbury", "lat": -43.5681182, "lon": 172.5466141},
    {"Name": "Manawatu", "lat": -40.3877088, "lon": 175.5664372},
    {"Name": "Te Puke", "lat": -37.7852583, "lon": 176.2766372},
    {"Name": "Southland", "lat": -46.4417431, "lon": 168.2516316},
    {"Name": "Nelson", "lat": -41.3142389, "lon": 173.1070159},
    {"Name": "Hawkes Bay", "lat": -39.6001332, "lon": 176.7514339},
    {"Name": "Eastern Bay of Plenty", "lat": -41.5374283, "lon": 173.9368226},
    {"Name": "Whangarei", "lat": -41.5374283, "lon": 173.9368226},
    {"Name": "Taranaki", "lat": -41.5374283, "lon": 173.9368226},
    {"Name": "Dunedin", "lat": -45.8434795, "lon": 170.3912766},
    {"Name": "Marlborough", "lat": -41.5374283, "lon": 173.9368226},
]

# Helper to fetch weather from APIs
def get_weather(lat: float, lon: float) -> dict:
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url)
    data = response.json()
    temp = data['current_weather']['temperature']

    api_url = f"https://api.meteomatics.com/{now}/precip_1h:mm/{lat},{lon}/json"
    response = requests.get(api_url, auth=('school_moseby_oliver', '9Q0tc2ePJb'))
    data = response.json()
    precip = data['data'][0]['coordinates'][0]['dates'][0]['value']

    return {'temp': temp, 'precip': precip}

# Helper to determine PSI based on weather conditions
def get_psi(wet_tyre: bool, temp: float) -> int:
    if wet_tyre:
        if temp <= 5:
            return 13
        elif temp >= 15:
            return 12
    else:
        if temp <= 5:
            return 15
        elif temp <= 14:
            return 14
        elif temp <= 19:
            return 13
        else:
            return 12

# Track selection UI
st.header("GoKarting Weather 3.5")
track_names = [track['Name'] for track in tracks]
selected_track = st.selectbox("Select a Karting Track:", track_names)

if selected_track:
    # Find selected track details
    track = next((t for t in tracks if t["Name"] == selected_track), None)

    if st.button("Get Weather Information"):
        # Fetch weather data
        weather = get_weather(track['lat'], track['lon'])
        tyre_type = 'wet' if weather['precip'] > 0.25 else 'dry'
        psi = get_psi(tyre_type == 'wet', weather['temp'])

        # Display the results
        st.subheader(f"Weather for {track['Name']}")
        st.write(f"Temperature: {weather['temp']}°C")
        st.write(f"Precipitation: {weather['precip']}%")
        st.write(f"Recommended Tyres: {tyre_type}")
        st.write(f"Recommended PSI: {psi}")

        # Show track image
        image_path = f"images/{selected_track}.png"  # Ensure images are in the correct directory
        try:
            st.image(image_path, caption=f"Track: {selected_track}", use_column_width=True)
        except Exception:
            st.warning(f"No image found for {selected_track}")

# Footer/credits
st.write("---")
st.markdown("**Created by Ollie, Jamie with support from Open-Meteo API**")