# Virgin Glamping Map

Interactive map of Virgin Experience glamping deals, colour-coded by number of nights.

- **Grey** — unknown nights
- **Red** — 1 night
- **Green** — 2 nights
- **Yellow** — 3+ nights

Click a pin to see details and a link to the offer.

## Usage

```bash
make install   # or: pip install -r requirements.txt
make run       # or: streamlit run app.py
```

Opens at `http://localhost:8501`.

## Data

`data/glamping_options_geocoded.csv` — glamping deals with lat/lng, price, and link.
