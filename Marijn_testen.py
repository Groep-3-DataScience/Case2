import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st

# Load the dataset for cycle stations
df_cyclestations = pd.read_csv('/Users/marijn/Downloads/cycle_stations.csv')

# Initialize a map centered around London (You can adjust the latitude and longitude accordingly)
m = folium.Map(location=[51.5074, -0.1278], zoom_start=12, tiles='CartoDB.Positron')

# Add markers for each cycle station on the map
for index, row in df_cyclestations.iterrows():
    folium.Marker(
        location=[row['lat'], row['long']],
        popup=f"Station: {row['name']}<br> Bikes Available: {row['nbBikes']}<br> EBikes: {row['nbEBikes']}",
        tooltip=row['name']
    ).add_to(m)

# Display the map in Streamlit
folium_static(m)
