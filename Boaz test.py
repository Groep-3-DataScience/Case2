import requests
import pandas as pd
import streamlit as st
from folium.features import CustomIcon
from streamlit_folium import st_folium
import folium
from datetime import datetime

# Enable static serving for Streamlit
st.set_page_config(page_title="Weerkaart Nederland", layout="wide")
st.enableStaticServing = True

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

visualization_option = st.selectbox("Selecteer de visualisatie", ["Temperatuur", "Weer"])

unieke_tijden = df_uur_verw["tijd"].dropna().unique()
huidig_uur = datetime.now().replace(minute=0, second=0, microsecond=0)
if huidig_uur not in unieke_tijden:
    huidig_uur = unieke_tijden[0]
selected_hour = st.select_slider("Selecteer het uur", options=sorted(unieke_tijden), value=huidig_uur, format_func=lambda t: t.strftime('%H:%M'))

@st.cache_data
def create_map(df, visualisatie_optie, geselecteerde_uur):
    nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)
    df_filtered = df[df["tijd"] == geselecteerde_uur]

    for index, row in df_filtered.iterrows():
        if visualisatie_optie == "Weer":
            icon_file = weather_icons.get(row['image'].lower(), "bewolkt.png")
            icon_path = f"Case2/iconen-weerlive/{icon_file}"
            popup_text = f"{row['plaats']}: {row['temp']}°C, {row['image']}"
            
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=popup_text,
                tooltip=row["plaats"],
                icon=CustomIcon(icon_path, icon_size=(30, 30))
            ).add_to(nl_map)
        
        elif visualisatie_optie == "Temperatuur":
            folium.map.Marker(
                location=[row["lat"], row["lon"]],
                tooltip=row["plaats"],
                icon=folium.DivIcon(html=f'<div style="color:red; font-weight:bold; font-size:18px;">{row["temp"]}°C</div>')
            ).add_to(nl_map)
    
    return nl_map

nl_map = create_map(df_uur_verw, visualization_option, selected_hour)
st_folium(nl_map, width=700)
