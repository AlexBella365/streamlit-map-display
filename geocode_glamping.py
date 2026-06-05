import re
import pandas as pd

glamping = pd.read_csv("data/glamping_options.csv")

# All known coordinates (no geocoding API needed)
coord_map = {
    "wall eden farm": (51.227, -2.962),
    "culdees castle estate": (56.362, -3.866),
    "stanley villa farm": (53.764, -2.705),
    "baxby manor": (54.151, -1.499),
    "the quiet site": (54.460, -3.089),
    "penhein glamping": (51.745, -2.782),
    "secret garden": (51.210, 0.905),
    "moddershall oaks": (52.966, -2.151),
    "port lympne": (51.075, 1.001),
    "northcombe farm and lakes": (50.936, -3.826),
    "new lodge farm, rockingham forest": (52.436, -0.678),
    "new lodge farm": (52.436, -0.678),
    "back of beyond": (50.938, -1.915),
    "oastbrook estate": (50.953, 0.686),
    "jerusalem farm": (55.958, -2.882),
    "catanger farm": (52.134, -1.146),
    "dartmoor, langstone manor": (50.603, -3.875),
    "south lytchett manor": (50.745, -2.057),
    "the apple farm": (52.196, -1.729),
    "stratford-upon-avon": (52.191, -1.707),
    "cornwall": (50.500, -4.500),
    "devon": (50.700, -3.500),
    "lake district": (54.500, -3.000),
    "cairngorms national park": (57.100, -3.700),
}


def extract_place(location):
    if pd.isna(location):
        return None
    loc = str(location).strip()
    m = re.search(r"\((.+?)\)", loc)
    if m:
        return m.group(1).strip()
    if loc and loc != "(Location in detailed product page)":
        return loc
    return None


lats, lngs = [], []

for _, row in glamping.iterrows():
    loc = str(row["location"]).strip() if not pd.isna(row["location"]) else ""
    place = extract_place(loc)
    key = place.strip().lower() if place else None

    if key and key in coord_map:
        lat, lng = coord_map[key]
        lats.append(lat)
        lngs.append(lng)
    else:
        lats.append(None)
        lngs.append(None)
        label = loc if loc else "(empty)"
        print(f"  MISSING: {label}")

glamping["latitude"] = lats
glamping["longitude"] = lngs

glamping.to_csv("data/glamping_options_geocoded.csv", index=False)

print(f"Written: {len(glamping)} rows, {glamping['latitude'].notna().sum()} with coordinates")
