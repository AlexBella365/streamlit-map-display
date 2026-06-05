import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(layout="wide")
st.title("Virgin Experience Map")

df = pd.read_csv("data/virgin_sanitized_geodata.csv")
df = df.dropna(subset=["Latitude", "Longitude"]).copy()

# Build per-row color based on star rating
def rating_to_color(rating):
    if pd.isna(rating):
        return [180, 180, 180, 180]  # grey for N/A
    t = (rating - 1) / 4  # 0..1
    r = int(200 - t * 200)
    g = int(30 + t * 170)
    b = int(0 + t * 50)
    return [r, g, b, 180]

df["color"] = df["Star rating"].apply(rating_to_color)

df["Star rating display"] = df["Star rating"].apply(
    lambda x: f"{x:.1f}" if not pd.isna(x) else "N/A"
)
df["Extra fee display"] = df["Extra fee"].fillna(0).apply(lambda x: f"£{x:.0f}")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df,
    get_position="[Longitude, Latitude]",
    get_radius=15000,
    get_fill_color="color",
    pickable=True,
    auto_highlight=True,
)

tooltip = {
    "html": (
        "<b>{Experience}</b><br/>"
        "Star Rating: {Star rating display}<br/>"
        "Extra Cost: {Extra fee display}"
    ),
    "style": {"backgroundColor": "rgba(0,0,0,0.8)", "color": "white", "fontSize": "14px"},
}

view_state = pdk.ViewState(
    latitude=df["Latitude"].mean(),
    longitude=df["Longitude"].mean(),
    zoom=5,
    pitch=0,
)

st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="light",
    ),
    use_container_width=True,
)
