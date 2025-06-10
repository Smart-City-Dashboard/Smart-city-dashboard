import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import base64
from utils.sentiment import analyze_sentiment


def image_to_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
        return f"data:image/png;base64,{encoded}"
    
# Set page configuration
st.set_page_config(
    page_title="Smart City Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
        /* Sidebar styling */
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

# Sidebar icons
icons = {
    "Traffic Congestion": image_to_base64("assets/traffic.png"),
    "Air Quality": image_to_base64("assets/airquality.png"),
    "Public Transport": image_to_base64("assets/transport.png"),
    "Sentiment Analysis": image_to_base64("assets/sentiment.png"),
    "Accident Prediction":image_to_base64("assets/accident.png")
}



# Initialize session state
if "active_section" not in st.session_state:
    st.session_state.active_section = "Traffic"

# Sidebar layout
st.sidebar.markdown('<div class="sidebar-title">🔎 Explore Metrics</div>', unsafe_allow_html=True)

# Sidebar navigation with icons using st.sidebar.image + st.sidebar.button
for section, icon_path in icons.items():
    selected = st.session_state.active_section == section

    # Create two columns: one for icon, one for the button text
    col1, col2 = st.sidebar.columns([1, 5])
    with col1:
        st.markdown(
        f"""
        <img src="{icon_path}" style="
            width: 37px;
            max-width: 100%;
            border: 1px solid grey;
            border-radius: 6px;
            margin: 2px 2px 0 10px;
            background-color: #ffffff10;
            padding: 2px;
        ">
        """,
        unsafe_allow_html=True
    )



    with col2:
        # Make the button show selected style
        button_label = f"**{section}**" if selected else section
        if st.button(button_label, key=section, use_container_width=True):
            st.session_state.active_section = section

# Load data
@st.cache_data
def load_data():
    traffic = pd.read_csv("data/traffic.csv")
    air = pd.read_csv("data/air_quality.csv")
    transport = pd.read_csv("data/transport.csv")
    tweets = pd.read_csv("data/tweets.csv")
    return traffic, air, transport, tweets

# traffic_df, air_df, transport_df, tweets_df = load_data()

# Dummy data for testing
traffic_df = pd.DataFrame({
    "lat": [40.7128, 40.7138, 40.7148],
    "lon": [-74.0060, -74.0070, -74.0080],
    "congestion_level": ["High", "Medium", "Low"],
    "location": ["Location A", "Location B", "Location C"]
})

air_df = pd.DataFrame({
    "timestamp": pd.date_range(start="2023-01-01", periods=5, freq='D'),
    "PM2.5": [35, 40, 30, 25, 45],
    "location": ["Loc1", "Loc1", "Loc2", "Loc2", "Loc1"]
})

transport_df = pd.DataFrame({
    "route": ["Route A", "Route B", "Route C"],
    "passenger_count": [100, 150, 90]
})

tweets_df = pd.DataFrame({
    "text": ["Good city", "Bad traffic", "Love the park"],
    "sentiment": ["Positive", "Negative", "Positive"]
})

# Main dashboard
st.title("🌆 Smart City Data Science Dashboard")
# Add this right below the title to remove top margin
st.markdown(
    """
    <style>
    h1 {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown("##### An interactive dashboard for visualizing smart city metrics")

row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)
row3_col1, row3_col2 = st.columns(2)


with row1_col1:
    st.subheader("🚦 Traffic Congestion Hotspots")
    fig1 = px.scatter_mapbox(
        traffic_df, lat="lat", lon="lon", color="congestion_level",
        mapbox_style="carto-darkmatter", zoom=6, height=400, width=400
    )
    st.plotly_chart(fig1, use_container_width=True)

# 🌫️ Air Quality
with row1_col2:
    st.subheader("🌫️ Air Quality Trends")
    fig2 = px.line(air_df, x="timestamp", y="PM2.5", color="location", height=400, width=400)
    st.plotly_chart(fig2, use_container_width=True)

# 🚌 Public Transport
with row2_col1:
    st.subheader("🚌 Public Transport Usage")
    fig3 = px.bar(transport_df, x="route", y="passenger_count", color="route",height=400, width=400)
    st.plotly_chart(fig3, use_container_width=True)

# 💬 Sentiment Analysis
with row2_col2:
    st.subheader("💬 Citizen Sentiment")
    tweets_df["sentiment"] = tweets_df["text"].apply(analyze_sentiment)
    sentiment_counts = tweets_df["sentiment"].value_counts().reset_index()
    fig4 = px.pie(sentiment_counts, names="sentiment", values="count", height=400, width=400)

    st.plotly_chart(fig4, use_container_width=True)
    

with row3_col1:
    st.subheader("🚨 Accident Prediction")
    # dummy accident data and plot here
    accident_df = pd.DataFrame({
        "lat": np.random.uniform(40.7, 40.8, 50),
        "lon": np.random.uniform(-74.02, -73.95, 50),
        "severity": np.random.randint(1, 4, 50),
        "predicted_risk": np.random.choice(["Low", "Medium", "High"], 50, p=[0.5, 0.3, 0.2]),
        "location": ["Loc " + str(i) for i in range(50)]
    })
    fig_accident = px.scatter_mapbox(
        accident_df,
        lat="lat", lon="lon",
        color="predicted_risk",
        size="severity",
        mapbox_style="carto-darkmatter",
        zoom=12,
        hover_name="location",
        title="Accident Prediction Hotspots (Dummy)"
    )
    st.plotly_chart(fig_accident, use_container_width=True, height=400, width=400)

# row3_col2 can be left empty or used for future expansion
