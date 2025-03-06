import requests
import pandas as pd
import streamlit as st
import folium
from folium.features import CustomIcon
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from datetime import datetime

# Configure Streamlit
st.set_page_config(page_title="Weerkaart Nederland", layout="wide")

api_key = 'd5184c3b4e'
cities = [
    'Assen', 'Lelystad', 'Leeuwarden', 'Arnhem', 'Groningen', 'Maastricht', 
    'Eindhoven', 'Den Helder', 'Enschede', 'Amersfoort', 'Middelburg', 'Rotterdam'
]

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

liveweer, wk_verw, uur_verw, api_data = fetch_weather_data()

df_liveweer = pd.DataFrame(liveweer)
df_wk_verw = pd.DataFrame(wk_verw)
df_uur_verw = pd.DataFrame(uur_verw)
df_api_data = pd.DataFrame(api_data)

@st.cache_data
def process_hourly_data(df):
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='s')
    df['datum'] = df['datetime'].dt.strftime('%d-%m-%Y')
    df['tijd'] = df['datetime'].dt.strftime('%H:%M')
    df['tijd'] = pd.to_datetime(df['tijd'], format='%H:%M', errors='coerce')
    return df

df_uur_verw = process_hourly_data(df_uur_verw)

st.title("Weerkaart Nederland")

# Base URL for GitHub-hosted images
BASE_ICON_URL = "https://raw.githubusercontent.com/Groep-3-Datascience/Case2/main/iconen-weerlive/"

weather_icons = {
    "zonnig": "zonnig.png",
    "bewolkt": "bewolkt.png",
    "half bewolkt": "halfbewolkt.png",
    "licht bewolkt": "halfbewolkt.png",
    "regen": "regen.png",
    "buien": "buien.png",
    "mist": "mist.png",
    "sneeuw": "sneeuw.png",
    "onweer": "bliksem.png",
    "hagel": "hagel.png",
    "heldere nacht": "helderenacht.png",
    "nachtmist": "nachtmist.png",
    "wolkennacht": "wolkennacht.png",
    "zwaar bewolkt": "zwaarbewolkt.png"
}

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

df_uur_verw["lat"] = df_uur_verw["plaats"].map(lambda city: city_coords.get(city, [None, None])[0])
df_uur_verw["lon"] = df_uur_verw["plaats"].map(lambda city: city_coords.get(city, [None, None])[1])

# Function to create weather map
def create_map(df, title, selected_hour):
    map_center = [52.3676, 4.9041]  # Centered on the Netherlands
    m = folium.Map(location=map_center, zoom_start=7)

    df_filtered = df[df["tijd"] == selected_hour]

    for _, row in df_filtered.iterrows():
        city = row["plaats"]
        lat, lon = row["lat"], row["lon"]
        weather = row["samenv"]  # Weather description

        if city in city_coords and lat and lon:
            icon_url = BASE_ICON_URL + weather_icons.get(weather, "zonnig.png")
            icon = CustomIcon(icon_url, icon_size=(50, 50))
            folium.Marker(
                location=[lat, lon],
                popup=f"{city}: {weather}",
                icon=icon
            ).add_to(m)

    return m

# Layout for map and graph
col1, col2 = st.columns([1, 1])

# Weather map
with col1:
    st.subheader("Weerkaart Nederland")

    selected_hour = st.select_slider(
        "Selecteer het uur",
        options=sorted(df_uur_verw["tijd"].dropna().unique()),
        format_func=lambda t: t.strftime('%H:%M')
    )

    nl_map = create_map(df_uur_verw, "Weer", selected_hour)
    st_folium(nl_map, width=700)

# Weather graph
with col2:
    st.subheader("Weersverloop per uur")

    selected_city = st.selectbox("Selecteer een stad", cities)
    show_temp = st.checkbox("Temperatuur (°C)", value=True)
    show_wind = st.checkbox("Windkracht (Bft)")
    show_precip = st.checkbox("Neerslag (mm)")

    df_city = df_uur_verw[df_uur_verw["plaats"] == selected_city].copy()

    if not df_city.empty:
        df_city["tijd"] = df_city["tijd"].dt.strftime('%H:%M')

        fig, ax1 = plt.subplots(figsize=(12, 6))

        if show_temp:
            ax1.plot(df_city["tijd"], df_city["temp"], marker="o", label="Temperatuur (°C)", color="red")

        ax1.set_xlabel("Tijd")
        ax1.set_ylabel("Temperatuur (°C)")
        ax1.tick_params(axis="y", labelcolor="black")
        ax1.set_xticklabels(df_city["tijd"], rotation=45, ha="right")

        ax2 = ax1.twinx()

        if show_wind:
            ax2.plot(df_city["tijd"], df_city["windbft"], marker="s", label="Windkracht (Bft)", color="green", linestyle="dashed")
        if show_precip:
            ax2.plot(df_city["tijd"], df_city["neersl"], marker="^", label="Neerslag (mm)", color="blue")

        ax1.set_title(f"Weer van {selected_city} per uur")
        ax2.set_ylabel("Windkracht (Bft) / Neerslag (mm)")
        ax2.tick_params(axis="y", labelcolor="black")

        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines + lines2, labels + labels2, loc="upper left")

        st.pyplot(fig)
    else:
        st.write("Geen gegevens beschikbaar voor deze stad.")
