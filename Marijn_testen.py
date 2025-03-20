import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit as st
from streamlit_folium import folium_static  # Importeer folium_static

# Gebruik caching om de data sneller te laden
@st.cache
def load_data():
    # Laad de CSV-bestanden en geef de dataframe terug
    df_cyclestations = pd.read_csv('cycle_stations.csv')
    bestanden = ['2021_Q2_Central.csv', '2021_Q3_Central.csv', '2021_Q4_Central.csv']
    fiets_data_jaar = pd.concat([pd.read_csv(file) for file in bestanden], ignore_index=True)
    return df_cyclestations, fiets_data_jaar

# Laad de gegevens met caching
df_cyclestations, fiets_data_jaar = load_data()

# Streamlit app layout
st.title('London Cycle Stations')
st.markdown("Interaktive map met fietsverhuurstations in Londen")

# Voeg een slider toe om het aantal fietsen in te stellen
bike_slider = st.slider("Selecteer het aantal beschikbare fietsen", 0, 100, 0)

# Maak een basemap van Londen
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12)

# MarkerCluster om stations te groeperen
marker_cluster = MarkerCluster().add_to(m)

# Filter de fietsstations op basis van het aantal beschikbare fietsen
filtered_df = df_cyclestations[df_cyclestations['nbBikes'] >= bike_slider]

# Beperk het aantal markers voor snellere rendering
top_stations = filtered_df.head(100)  # Je kunt dit aantal aanpassen

# Voeg de stations toe aan de kaart
for index, row in top_stations.iterrows():
    lat = row['lat']
    long = row['long']
    station_name = row['name']
    nb_bikes = row['nbBikes']  # Aantal fietsen
    nb_standard_bikes = row['nbStandardBikes']  # Aantal standaardfietsen
    nb_ebikes = row['nbEBikes']  # Aantal ebikes

    # Voeg een marker toe met info over het station
    folium.Marker(
        location=[lat, long],
        popup=folium.Popup(f"Station: {station_name}<br>Aantal fietsen: {nb_bikes}<br>Standaard: {nb_standard_bikes}<br>EBikes: {nb_ebikes}", max_width=300),
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(marker_cluster)

# Render de kaart in de Streamlit app
folium_static(m)
