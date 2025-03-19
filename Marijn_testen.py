import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static  # Importeer folium_static

# Laad de bestanden
df_cyclestations = pd.read_csv('cycle_stations.csv')

# Bestanden voor elk kwartaal
bestanden = {
    '2021_Q2': '2021_Q2_Central.csv',
    '2021_Q3': '2021_Q3_Central.csv',
    '2021_Q4': '2021_Q4_Central.csv'
}

# Voeg een dropdown toe waarmee de gebruiker het kwartaal kan kiezen
selected_quarter = st.selectbox("Selecteer kwartaal", options=['2021_Q2', '2021_Q3', '2021_Q4'])

# Laad de juiste data op basis van het gekozen kwartaal
df_fiets_data = pd.read_csv(bestanden[selected_quarter])

# Streamlit layout
st.title('London Cycle Stations')
st.markdown(f"Interaktive map voor fietsverhuurstations in Londen - {selected_quarter}")

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

    # Voeg een marker toe met info over het station
    if nb_bikes >= bike_slider:  # Controleer of het aantal fietsen groter of gelijk is aan de slider
        folium.Marker(
            location=[lat, long],
            popup=folium.Popup(f"Station: {station_name}<br>Aantal fietsen: {nb_bikes}<br>Standaard: {nb_standard_bikes}<br>EBikes: {nb_ebikes}", max_width=300),
            icon=folium.Icon(color='blue', icon='info-sign')
        ).add_to(marker_cluster)

# Render de kaart in de Streamlit app
folium_static(m)

