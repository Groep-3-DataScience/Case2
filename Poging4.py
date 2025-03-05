# %% [markdown]
# #Verwerken van API en downloaden van 

# %%
import requests
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# %%
import requests
import pandas as pd

api_key = 'd5184c3b4e'
cities = [
    'Assen', 'Lelystad', 'Leeuwarden', 'Arnhem', 'Groningen', 'Maastricht', 
    'Eindhoven', 'Den Helder', 'Enschede', 'Amersfoort', 'Middelburg', 'Rotterdam'
]
liveweer = []
wk_verw = []
uur_verw = []
api_data = []

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

df_liveweer = pd.DataFrame(liveweer)
df_wk_verw = pd.DataFrame(wk_verw)
df_uur_verw = pd.DataFrame(uur_verw)
df_api_data = pd.DataFrame(api_data)
print(df_liveweer)


# %% [markdown]
# pd.DataFrame.from_dict(data)

# %%
# Save to CSV file
df_liveweer.to_csv('WL_LiveWeer.csv')
df_wk_verw.to_csv('WL_week_werwachting.csv')
df_uur_verw.to_csv('WL_uur_werwachting.csv')
df_api_data.to_csv('WL_API.csv')

# %% [markdown]
# Moet het volgende weten voordat ik verder kan:
# 1. Hoe kan ik locatie zetten bij uur- en weekverwachting? Kan ik 'plaats' van LiveWeer mergen met de andere twee DFs? (Done)

# %% [markdown]
# # Visualisaties #

# %%
import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.features import CustomIcon

# City coordinations for icon placements
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

# Weather condition to icon mapping
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

# Voeg lat/lon toe aan df_liveweer
df_liveweer["lat"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[0])
df_liveweer["lon"] = df_liveweer["plaats"].map(lambda city: city_coords.get(city, [None, None])[1])

# Streamlit titel
st.title("Weerkaart van Nederland")

# Creëer een folium kaart
nl_map = folium.Map(location=[52.3, 5.3], zoom_start=8)

for _, row in df_liveweer.iterrows():
    weather_desc = row['samenv'].lower()
    icon_file = weather_icons.get(weather_desc, "bewolkt.png")  # Default naar "bewolkt.png"
    icon_path = f"iconen-weerlive/{icon_file}"  # Zorg ervoor dat het pad correct is
    
    popup_text = f"{row['plaats']}: {row['temp']}°C, {row['samenv']}"

    # Voeg marker toe met weericoon
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=popup_text,
        tooltip=row["plaats"],
        icon=CustomIcon(icon_path, icon_size=(30, 30))
    ).add_to(nl_map)

# Toon de kaart in Streamlit
st_folium(nl_map, width=700, height=500)


# %%



