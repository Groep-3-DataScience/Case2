import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static  # Importeer folium_static

# Laad de bestanden
df_cyclestations = pd.read_csv('cycle_stations.csv')

# Converteer de installatiedatum van Unix timestamp (epoch) naar een leesbare datum (dd-mm-yyyy)
df_cyclestations['installDate'] = pd.to_datetime(df_cyclestations['installDate'], unit='ms')

# Streamlit layout
st.title('London Cycle Stations')
st.markdown("Interaktive map voor fietsverhuurstations in Londen")

# Voeg een slider toe om het aantal beschikbare fietsen in te stellen
bike_slider = st.slider("Selecteer het aantal beschikbare fietsen", 0, 100, 0)

# Maak een basemap van Londen
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# MarkerCluster om stations te groeperen
marker_cluster = MarkerCluster().add_to(m)

# Voeg de stations toe aan de kaart
for index, row in df_cyclestations.iterrows():
    lat = row['lat']
    long = row['long']
    station_name = row['name']
    nb_bikes = row['nbBikes']  # Aantal fietsen
    nb_standard_bikes = row['nbStandardBikes']  # Aantal standaardfietsen
    nb_ebikes = row['nbEBikes']  # Aantal ebikes
    install_date = row['installDate'].strftime('%d-%m-%Y')  # Zet de installatiedatum om naar 'dd-mm-yyyy'

    # Voeg een marker toe met info over het station
    if nb_bikes >= bike_slider:  # Controleer of het aantal fietsen groter of gelijk is aan de slider
        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(f"Station: {station_name}<br>Aantal fietsen: {nb_bikes}<br>Standaard: {nb_standard_bikes}<br>EBikes: {nb_ebikes}<br>Installatiedatum: {install_date}", max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

# Render de kaart in de Streamlit app
folium_static(m)
