# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from utils.sentiment import analyze_sentiment
from traffic_congestion import run_traffic_hotspot_view

def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"

st.set_page_config(page_title="Smart City Dashboard", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #1c1f26;
        }
        .sidebar-title {
            color: #fff;
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
        }
        .nav-button {
            display: flex;
            align-items: center;
            gap: 10px;
            width: 100%;
            padding: 8px 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            font-weight: bold;
            color: #fff;
            text-align: left;
            background-color: transparent;
            border: none;
        }
        .nav-button:hover {
            background-color: #31333F;
            cursor: pointer;
        }
        .nav-selected {
            background-color: #31333F !important;
        }
    </style>
""", unsafe_allow_html=True)

icons = {
    "Dashboard Overview": image_to_base64("assets/dashboard.png"),
    "Traffic Congestion": image_to_base64("assets/traffic.png"),
    "Air Quality": image_to_base64("assets/airquality.png"),
    "Public Transport": image_to_base64("assets/transport.png"),
    "Sentiment Analysis": image_to_base64("assets/sentiment.png"),
    "Accident Prediction": image_to_base64("assets/accident.png")
}

if "active_section" not in st.session_state:
    st.session_state.active_section = "Dashboard Overview"

st.sidebar.markdown('<div class="sidebar-title">🔎 Explore Metrics</div>', unsafe_allow_html=True)

for section, icon_path in icons.items():
    selected = st.session_state.active_section == section
    col1, col2 = st.sidebar.columns([1, 5])
    with col1:
        st.markdown(
        f"""
        <img src="{icon_path}" style="width: 37px; max-width: 100%; border: 1px solid grey; border-radius: 6px;
        margin: 2px 2px 0 10px; background-color: #ffffff10; padding: 2px;">
        """,
        unsafe_allow_html=True
    )
    with col2:
        button_label = f"**{section}**" if selected else section
        if st.button(button_label, key=section, use_container_width=True):
            st.session_state.active_section = section

# =============================
# Module Logic Based on State
# =============================

section = st.session_state.active_section

if section == "Dashboard Overview":
    st.title("🌇 Smart City Dashboard Overview")
    st.markdown("""
    Welcome to the Smart City Dashboard. Here's what each section offers:

    - 🚦 **Traffic Congestion**: Real-time congestion hotspots using TomTom API and DBSCAN clustering.
    - 🌫️ **Air Quality**: Visualize PM2.5/PM10 pollution levels across city locations.
    - 🚌 **Public Transport**: Passenger statistics across major public transit routes.
    - 💬 **Sentiment Analysis**: Public sentiment analysis on city-related tweets.
    - 🚨 **Accident Prediction**: AI-based cluster detection of road accident risks.

    Use the sidebar to navigate to each section.
    """)

elif section == "Traffic Congestion":
    run_traffic_hotspot_view()

elif section == "Air Quality":
    st.title("🌫️ Air Quality Trends")
    air_df = pd.DataFrame({
        "timestamp": pd.date_range(start="2023-01-01", periods=5, freq='D'),
        "PM2.5": [35, 40, 30, 25, 45],
        "location": ["Loc1", "Loc1", "Loc2", "Loc2", "Loc1"]
    })
    fig2 = px.line(air_df, x="timestamp", y="PM2.5", color="location")
    st.plotly_chart(fig2, use_container_width=True)

elif section == "Public Transport":
    st.title("🚌 Public Transport Usage")
    transport_df = pd.DataFrame({
        "route": ["Route A", "Route B", "Route C"],
        "passenger_count": [100, 150, 90]
    })
    fig3 = px.bar(transport_df, x="route", y="passenger_count", color="route")
    st.plotly_chart(fig3, use_container_width=True)

elif section == "Sentiment Analysis":
    st.title("💬 Citizen Sentiment")
    tweets_df = pd.DataFrame({
        "text": ["Good city", "Bad traffic", "Love the park"]
    })
    tweets_df["sentiment"] = tweets_df["text"].apply(analyze_sentiment)
    sentiment_counts = tweets_df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]
    fig4 = px.pie(sentiment_counts, names="sentiment", values="count")
    st.plotly_chart(fig4, use_container_width=True)

elif section == "Accident Prediction":
    st.title("🚨 Accident Prediction")
    accident_df = pd.DataFrame({
        "lat": np.random.uniform(40.7, 40.8, 50),
        "lon": np.random.uniform(-74.02, -73.95, 50),
        "severity": np.random.randint(1, 4, 50),
        "predicted_risk": np.random.choice(["Low", "Medium", "High"], 50),
        "location": ["Loc " + str(i) for i in range(50)]
    })
    fig_accident = px.scatter_mapbox(
        accident_df, lat="lat", lon="lon", color="predicted_risk", size="severity",
        mapbox_style="carto-darkmatter", zoom=12, hover_name="location"
    )
    st.plotly_chart(fig_accident, use_container_width=True)
