import requests
import pandas as pd
import streamlit as st
from folium.features import CustomIcon
from streamlit_folium import st_folium  # Import this for Folium integration
import folium
import matplotlib.pyplot as plt  # For graphing
from datetime import datetime

# API Configuration
api_key = 'd5184c3b4e'
cities = [
    'Assen', 'Lelystad', 'Leeuwarden', 'Arnhem', 'Groningen', 'Maastricht', 
    'Eindhoven', 'Den Helder', 'Enschede', 'Amersfoort', 'Middelburg', 'Rotterdam'
]

# Fetch and transform weather data
@st.cache_data
def fetch_weather_data():
    liveweer, wk_verw, uur_verw, api_data = [], [], [], []
    
    for city in cities:
        api_url = f'https://weerlive.nl/api/weerlive_api_v2.php?key={api_key}&locatie={city}'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if 'liveweer' in data:
                liveweer.extend(data['liveweer'])
            if 'wk_verw' in data:
                for entry in data['wk_verw']:
                    entry['plaats'] = city
                wk_verw.extend(data['wk_verw'])
            if 'uur_verw' in data:
                for entry in data['uur_verw']:
                    entry['plaats'] = city
                uur_verw.extend(data['uur_verw'])
            if 'api_data' in data:
                api_data.extend(data['api'])
        else:
            print(f"Error fetching data for {city}: {response.status_code}")
    
    return liveweer, wk_verw, uur_verw, api_data

# Caching the weather data processing
@st.cache_data
def process_hourly_data(df):
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['datum'] = df['datetime'].dt.strftime('%d-%m-%Y')
    df['tijd'] = df['datetime'].dt.strftime('%H:%M')
    df['tijd'] = pd.to_datetime(df['tijd'], format='%H:%M', errors='coerce')
    return df

# Streamlit UI components
st.title("Weerkaart Nederland")

# City coordinates
city_coords = {
    "Assen": [52.9929, 6.5642],
    "Lelystad": [52.5185, 5.4714],
    "Leeuwarden": [53.2012, 5.7999],
    "Arnhem": [51.9851, 5.8987],
    "Groningen": [53.2194, 6.5665],
    "Maastricht": [50.8514, 5.6910],
    "Eindhoven": [51.4416, 5.4697],
    "Den Helder": [52.9563, 4.7601],
    "Enschede": [52.2215, 6.8937],
    "Amersfoort": [52.1561, 5.3878],
    "Middelburg": [51.4988, 3.6136],
    "Rotterdam": [51.9225, 4.4792],
}

# Initial cache fetch and process
liveweer, wk_verw, uur_verw, api_data = fetch_weather_data()
df_uur_verw = pd.DataFrame(uur_verw)
df_uur_verw = process_hourly_data(df_uur_verw)

# Map Creation
@st.cache_data
def create_map(df, visualisatie_optie, geselecteerde_uur, selected_cities):
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    df_filtered = df[(df["tijd"] == geselecteerde_uur) & (df["plaats"].isin(selected_cities))]

    for index, row in df_filtered.iterrows():
        if visualisatie_optie == "Weather":
            icon_file = f"iconen-weerlive/{row['image'].lower()}.png"  # Icon based on weather condition
            popup_text = f"{row['plaats']}: {row['temp']}°C, {row['image']}"
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=CustomIcon(icon_file, icon_size=(30, 30))
            ).add_to(nl_map)
        
        elif visualisatie_optie == "Temperature":
            folium.Marker(
                location=[row["lat"], row["lon"]],
                tooltip=row["plaats"],
                icon=folium.DivIcon(html=f'<div style="color:red; font-weight:bold; font-size:18px;">{row["temp"]}°C</div>')
            ).add_to(nl_map)
        
        elif visualisatie_optie == "Precipitation":
            folium.Marker(
                location=[row["lat"], row["lon"]],
                tooltip=row["plaats"],
                icon=folium.DivIcon(html=f'<div style="color:blue; font-weight:bold; font-size:18px;">{row["neersl"]} mm</div>')
            ).add_to(nl_map)
    
    return nl_map

# Streamlit: Select/Deselect All cities
select_all = st.button("Select/Deselect All Cities")

if select_all:
    if 'all_selected' not in st.session_state:
        st.session_state['all_selected'] = True
    else:
        st.session_state['all_selected'] = not st.session_state['all_selected']

# Default all cities selected or deselected based on button press
selected_cities = cities if st.session_state.get('all_selected', False) else []

# Checkbox interface for cities
for city in cities:
    if city not in selected_cities:
        selected_cities.append(city) if st.checkbox(city, value=False) else selected_cities

# If no cities are selected for the graph, show a warning
if not selected_cities:
    st.warning("Select at least one city to view the weather graph.")

# Slider for time selection
visualization_option = st.selectbox("Select visualization", ["Temperature", "Weather", "Precipitation"])

# Time selection
unieke_tijden = df_uur_verw["tijd"].dropna().unique()
huidig_uur = datetime.now().replace(minute=0, second=0, microsecond=0)
if huidig_uur not in unieke_tijden:
    huidig_uur = unieke_tijden[0]
selected_hour = st.select_slider("Select hour", options=sorted(unieke_tijden), value=huidig_uur, format_func=lambda t: t.strftime('%H:%M'))

# Create the map with all cities always displayed
nl_map = create_map(df_uur_verw, visualization_option, selected_hour, selected_cities)

# Display the map in Streamlit
st_folium(nl_map, width=700)

# Plot temperature and precipitation graphs
if selected_cities:
    # Create subplots for comparison
    fig, ax1 = plt.subplots(figsize=(10, 5))

    # Loop through selected cities to plot the data for each city
    for city in selected_cities:
        city_data = df_uur_verw[df_uur_verw['plaats'] == city]

        if visualization_option == "Temperature":
            # Plot only the temperature for each city
            ax1.plot(city_data['tijd'], city_data['temp'], label=f'Temperature ({city})', linestyle='-', marker='o')

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature (°C)', color='tab:red')
    ax1.tick_params(axis='y', labelcolor='tab:red')

    # Plot precipitation for each city on the same graph (only for valid precipitation values)
    if visualization_option == "Precipitation":
        ax2 = ax1.twinx()
        for city in selected_cities:
            city_data = df_uur_verw[df_uur_verw['plaats'] == city]

            # Filter out rows where precipitation is NaN or zero
            city_data = city_data[city_data['neersl'].notna() & (city_data['neersl'] > 0)]

            if not city_data.empty:
                ax2.set_ylabel('Precipitation (mm)', color='tab:blue')
                ax2.plot(city_data['tijd'], city_data['neersl'], label=f'Precipitation ({city})', linestyle='--', marker='x')

        ax2.tick_params(axis='y', labelcolor='tab:blue')

    # Add title and show plot
    plt.title(f"{visualization_option} Comparison")
    fig.legend(loc='upper right', bbox_to_anchor=(1.1, 1), bbox_transform=ax1.transAxes)
    plt.tight_layout()
    st.pyplot(fig)
