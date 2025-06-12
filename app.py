# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
<<<<<<< Updated upstream
from utils.air_quality import run_air_quality_view
from utils.sentiment import analyze_sentiment
=======
from sentiment_analysis import run_sentiment_analysis_view
>>>>>>> Stashed changes
from traffic_congestion import run_traffic_hotspot_view
from crimeanalysis import run_crime_analysis_view

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
    "Dashboard Overview": image_to_base64("assets/home.png"),
    "Traffic Congestion": image_to_base64("assets/traffic.png"),
    "Air Quality": image_to_base64("assets/airquality.png"),
    "Public Transport": image_to_base64("assets/transport.png"),
    "Sentiment Analysis": image_to_base64("assets/sentiment.png"),
    "Crime Analysis": image_to_base64("assets/crime.png")
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
    - 🚨 **Crime Analysis**: AI-based analysis of crimes and criminal trends.

    Use the sidebar to navigate to each section.
    """)

elif section == "Traffic Congestion":
    run_traffic_hotspot_view()

elif section == "Air Quality":
    run_air_quality_view()

elif section == "Public Transport":
    st.title("🚌 Public Transport Usage")
    transport_df = pd.DataFrame({
        "route": ["Route A", "Route B", "Route C"],
        "passenger_count": [100, 150, 90]
    })
    fig3 = px.bar(transport_df, x="route", y="passenger_count", color="route")
    st.plotly_chart(fig3, use_container_width=True)

elif section == "Sentiment Analysis":
    run_sentiment_analysis_view()


elif section == "Crime Analysis":
    run_crime_analysis_view()