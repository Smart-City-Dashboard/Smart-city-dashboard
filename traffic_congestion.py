import streamlit as st
import pandas as pd
import requests
from sklearn.cluster import DBSCAN
import pydeck as pdk
from datetime import datetime
import numpy as np

API_KEY = 'yHiibeu1NXs9q1JpgTft9kxOZvgXjOdu'

@st.cache_data(ttl=3600)
def get_city_bbox(city_name):
    url = f"https://api.tomtom.com/search/2/geocode/{city_name}.json?key={API_KEY}&typeahead=true&limit=1"
    res = requests.get(url)
    data = res.json()

    if 'results' not in data or len(data['results']) == 0:
        st.error(f"No results found for '{city_name}'")
        return None

    result = data['results'][0]

    if 'viewport' in result and 'minPoint' in result['viewport'] and 'maxPoint' in result['viewport']:
        bb = result['viewport']
        min_lat = bb['minPoint']['lat']
        min_lon = bb['minPoint']['lon']
        max_lat = bb['maxPoint']['lat']
        max_lon = bb['maxPoint']['lon']
    elif 'position' in result:
        lat = result['position']['lat']
        lon = result['position']['lon']
        buffer = 0.05
        min_lat = lat - buffer
        max_lat = lat + buffer
        min_lon = lon - buffer
        max_lon = lon + buffer
    else:
        st.error("No bounding box or position found.")
        return None

    return min_lat, max_lat, min_lon, max_lon

def generate_grid_points(min_lat, max_lat, min_lon, max_lon, step=0.01):
    lat_points = np.arange(min_lat, max_lat, step)
    lon_points = np.arange(min_lon, max_lon, step)
    return [(lat, lon) for lat in lat_points for lon in lon_points]

def fetch_tomtom_data(min_lat, max_lat, min_lon, max_lon):
    points = generate_grid_points(min_lat, max_lat, min_lon, max_lon)
    records = []
    total_points = len(points)
    progress_bar = st.progress(0)

    for i, (lat, lon) in enumerate(points):
        url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={lat},{lon}&unit=KMPH&key={API_KEY}'
        try:
            res = requests.get(url)
            data = res.json()
            if 'flowSegmentData' in data:
                current_speed = data['flowSegmentData'].get('currentSpeed', 0)
                free_flow = data['flowSegmentData'].get('freeFlowSpeed', 50)
                congestion = max(0, min(10, 10 * (1 - current_speed / free_flow)))

                records.append({
                    'latitude': lat,
                    'longitude': lon,
                    'jam_factor': round(congestion, 2)
                })
        except Exception as e:
            st.warning(f"Error at point {lat},{lon}: {e}")

        progress_bar.progress((i + 1) / total_points)

    df = pd.DataFrame(records)

    if not df.empty:
        coords = df[['latitude', 'longitude']]
        db = DBSCAN(eps=0.01, min_samples=3).fit(coords)
        df['cluster'] = db.labels_
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        df['cluster'] = []
        df['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return df

def jam_color(jam):
    if 0 <= jam <= 1:
        return [0, 255, 0, 160]
    elif 1 < jam <= 2:
        return [255, 255, 0, 160]
    elif 2 < jam <= 3:
        return [255, 165, 0, 160]
    else:
        return [255, 0, 0, 160]

def run_traffic_hotspot_view():
    st.title("🚦 Real-Time Traffic Congestion Hotspots (TomTom API)")
    st.markdown("Enter a city name to visualize congestion hotspots in real time.")

    city_name = st.text_input("Enter City Name", "Delhi")

    if city_name:
        if "traffic_data_cache" not in st.session_state:
            st.session_state.traffic_data_cache = {}

        if city_name in st.session_state.traffic_data_cache:
            st.success(f"Using cached data for **{city_name}**")
            df = st.session_state.traffic_data_cache[city_name]
        else:
            bbox = get_city_bbox(city_name)
            if bbox:
                min_lat, max_lat, min_lon, max_lon = bbox
                st.success(f"Fetching live traffic data for **{city_name}**...")
                df = fetch_tomtom_data(min_lat, max_lat, min_lon, max_lon)
                st.session_state.traffic_data_cache[city_name] = df
            else:
                return

        if df.empty:
            st.warning("No traffic data available.")
        else:
            st.metric("Total Clusters", df['cluster'].nunique())
            st.metric("Avg. Congestion (0-10)", round(df['jam_factor'].mean(), 2))
            st.metric("Last Updated", df['timestamp'].iloc[0])

            st.subheader("🗺️ Traffic Congestion Hotspots Map")

            df['color'] = df['jam_factor'].apply(jam_color)

            layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position='[longitude, latitude]',
                get_color='color',
                get_radius='jam_factor * 300',
                pickable=True,
                auto_highlight=True,
            )

            view_state = pdk.ViewState(
                latitude=df["latitude"].mean(),
                longitude=df["longitude"].mean(),
                zoom=11,
                pitch=0,
            )

            tooltip = {
                "html": "<b>Cluster:</b> {cluster}<br/><b>Congestion:</b> {jam_factor}",
                "style": {"color": "white"}
            }

            r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip=tooltip)
            st.pydeck_chart(r)

            with st.expander("📋 Raw Congestion Data"):
                st.dataframe(df)
