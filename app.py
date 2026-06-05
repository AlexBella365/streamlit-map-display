import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("Virgin Glamping Map")

df = pd.read_csv("data/glamping_options_geocoded.csv")
df = df.dropna(subset=["latitude", "longitude"]).copy()

def parse_nights(name):
    name = str(name).lower()
    if "one night" in name or name.startswith("overnight"):
        return 1
    if "two night" in name:
        return 2
    if "three night" in name:
        return 3
    return None

def nights_to_hex(n):
    if n == 1:
        return "#bf7980"
    if n == 2:
        return "#42A594"
    return "#b4b4b4"

df["nights"] = df["name"].apply(parse_nights)

m = folium.Map(
    location=[df["latitude"].mean(), df["longitude"].mean()],
    zoom_start=5,
    tiles="CartoDB positron",
)

for _, row in df.iterrows():
    color = nights_to_hex(row["nights"])
    nights_txt = f"{row['nights']} night{'s' if row['nights'] and row['nights'] > 1 else ''}" if row["nights"] else "Unknown"
    extra = row["extra_fee"] if not pd.isna(row["extra_fee"]) else "£0"
    html = (
        f"<b>{row['name']}</b><br>"
        f"Nights: {nights_txt}<br>"
        f"Extra Cost: {extra}<br>"
        f'<a href="{row["link"]}" target="_blank">see here</a>'
    )
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=8,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        color="#333",
        weight=1,
        popup=folium.Popup(html, max_width=350),
        tooltip=row["name"],
    ).add_to(m)

st_folium(m, width='stretch', height=600)
