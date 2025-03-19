import requests
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static

# Verkrijg live data van een API (voorbeeld voor een fietsverhuurservice)
def get_live_data():
    url = "https://api.tfl.gov.uk/bikepoint"
    response = requests.get(url)
    data = response.json()
    return pd.json_normalize(data['bikePoints'])  # Zet de API response om naar een DataFrame

# Verkrijg de live data
df_cyclestations = get_live_data()

# Streamlit layout
st.title('London Cycle Stations')
st.markdown("Interaktive map met fietsverhuurstations in Londen")

# Voeg een slider toe om het aantal fietsen in te stellen
bike_slider = st.slider("Selecteer het aantal beschikbare fietsen", 0, 100, 0)

# Maak een basemap van Londen
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# MarkerCluster om stations te groeperen
marker_cluster = MarkerCluster().add_to(m)

# Voeg de stations toe aan de kaart
for index, row in df_cyclestations.iterrows():
    lat = row['lat']
    long = row['long']
    station_name = row['commonName']
    nb_bikes = row['availability.bikes']  # Aantal beschikbare fietsen van live data

    # Voeg een marker toe met info over het station
    if nb_bikes >= bike_slider:  # Controleer of het aantal fietsen groter of gelijk is aan de slider
        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(f"Station: {station_name}<br>Aantal fietsen: {nb_bikes}", max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

# Render de kaart in de Streamlit app
folium_static(m)
