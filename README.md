# 🏙️ Smart City Dashboard

An interactive, real-time data dashboard for smart city monitoring and decision-making. This Streamlit-based application integrates live APIs and CSV datasets to visualize key urban metrics like **traffic congestion**, **air quality**, **ICT infrastructure**,**public sentiment**,**crime analysis**

---

## 📁 Project Structure
SMART_CITY_DASHBOARD/
│
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml
│
├── assets/                        # UI icons/images used in the dashboard
│   ├── airquality.png
│   ├── crime.png
│   ├── home.png
│   ├── ict.png
│   ├── sentiment.png
│   └── traffic.png
│
├── data/                          # Datasets used by different modules
│   ├── air_quality.csv
│   ├── City_ict_scores.csv
│   ├── crime_data.csv
│   └── ict_data.csv
│
├── utils/                         # Python modules for each feature
│   ├── _pycache_/
│   ├── air_quality.py
│   ├── crime_analysis.py
│   ├── ict_infrastructure.py
│   ├── sentiment_analysis.py
│   └── traffic_congestion.py
│
├── venv/                          # Virtual environment (not uploaded to GitHub)
│
├── app.py                         # Main Streamlit dashboard entry point
├── requirements.txt               # Required Python packages
└── README.md                      # Project overview and documentation
---

## 🔧 Features by Module

### 🚦 Traffic Congestion Hotspots
- Uses TomTom API to retrieve real-time traffic speed data.
- Clusters low-speed zones using DBSCAN.
- Visualizes hotspots on a pydeck map with congestion intensity.

### 🧠 Twitter Sentiment Analysis
- Fetches live tweets using Tweepy and Bearer Token.
- Analyzes sentiments using TextBlob.
- Displays bar charts, emoji summaries, and word clouds.

### 🌫️ Air Quality Index (AQI) Trends
- Reads AQI and pollutant data from tab-separated CSV.
- Plots AQI trends and pollutant averages using Plotly.

### 📡 ICT Infrastructure Comparison
- Visualizes ICT metrics like broadband coverage across cities.
- Compares overall ICT readiness scores.

###  🚨 Crime Analysis : 
- AI-based analysis of crimes and criminal trends.
---

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run app.py
```

---

## 🤝 Contributors
- Rohit Gope, Akash Kumar Saw, Nikhil Kumar, Venkatesh shashidhar

## Tech Stack
- Python,Streamlit,Plotly, Pydec,Metplotlib, Numpy, Pandas, 

## API (Tom tom, Twitter API)
---


