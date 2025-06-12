import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_crime_data():
    df = pd.read_csv("data/crime_data.csv")
    df.dropna(subset=["City", "Crime Description", "Victim Age", "Victim Gender", "Date of Occurrence"], inplace=True)
    df["Date of Occurrence"] = pd.to_datetime(df["Date of Occurrence"], errors='coerce')
    return df

def run_crime_analysis_view():
    st.title("🕵️‍♂️ Crime Analysis by City")

    df = load_crime_data()
    cities = sorted(df["City"].unique())
    selected_city = st.selectbox("Select a City to Analyze", cities)
    city_df = df[df["City"] == selected_city]

    if city_df.empty:
        st.warning("No valid crime data found for this city.")
        return

    # KPIs
    total_crimes = city_df.shape[0]
    solved_cases = city_df[city_df["Case Closed"] == "Yes"].shape[0]
    avg_police = city_df["Police Deployed"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Crimes", total_crimes)
    col2.metric("Solved Cases", solved_cases)
    col3.metric("Avg Police Deployed", f"{avg_police:.1f}")

    # Crime Description Frequency
    st.subheader("🔍 Crime Types in " + selected_city)
    desc_counts = city_df["Crime Description"].value_counts().reset_index()
    desc_counts.columns = ["Crime Description", "Count"]
    fig1 = px.bar(desc_counts.head(10), x="Crime Description", y="Count",
                 title="Top 10 Crime Types", color="Count", text="Count")
    st.plotly_chart(fig1, use_container_width=True)

    # Gender Distribution
    st.subheader("🧑‍🤝‍🧑 Victim Gender Distribution")
    fig2 = px.pie(city_df, names="Victim Gender", title="Gender Distribution of Victims")
    st.plotly_chart(fig2, use_container_width=True)

    # Age distribution by crime
    st.subheader("📊 Victim Age Distribution by Crime Type")
    fig3 = px.box(city_df, x="Crime Description", y="Victim Age",
                  title="Age Distribution", points="all")
    st.plotly_chart(fig3, use_container_width=True)

    # Time series
    st.subheader("🗓️ Crime Trend Over Time")
    time_series = city_df.groupby(city_df["Date of Occurrence"].dt.to_period("M")).size()
    time_series.index = time_series.index.to_timestamp()
    fig4 = px.line(time_series, labels={"value": "Number of Crimes", "index": "Month"},
                  title="Monthly Crime Trend")
    st.plotly_chart(fig4, use_container_width=True)
