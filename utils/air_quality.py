
import streamlit as st
import pandas as pd
import plotly.express as px

def run_air_quality_view():
    st.title("🌫️ Air Quality Levels (CSV-based)")

    try:
       df = pd.read_csv("data/air_quality.csv", sep='\t')

    except FileNotFoundError:
        st.error("The file 'data/air_quality.csv' was not found.")
        return

    # Convert Date column to datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Drop rows with missing dates or AQI
    df = df.dropna(subset=['Date', 'AQI'])

    # Let user select city
    city = st.selectbox("Select a City", df["City"].unique())

    city_df = df[df["City"] == city].sort_values(by="Date")

    st.write(f"Showing air quality data for **{city}**:")
    st.dataframe(city_df[['Date', 'AQI', 'AQI_Bucket', 'PM2.5', 'PM10']].tail(10))

    # Plot AQI over time
    st.subheader("📈 AQI Trend Over Time")
    fig = px.line(
        city_df, 
        x="Date", y="AQI", 
        color="AQI_Bucket",
        title=f"Air Quality Index (AQI) Over Time - {city}",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)

    # Bar plot of pollutant averages
    st.subheader("🧪 Average Pollutant Levels")
    pollutant_cols = ['PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']
    means = city_df[pollutant_cols].mean().sort_values(ascending=False)
    fig2 = px.bar(
        x=means.index,
        y=means.values,
        labels={'x': 'Pollutants', 'y': 'Average Value'},
        title=f"Average Pollutant Levels in {city}"
    )
    st.plotly_chart(fig2, use_container_width=True)
