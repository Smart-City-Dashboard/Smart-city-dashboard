import streamlit as st
import pandas as pd
import plotly.express as px

def run_ict_view():
    st.title("📡 ICT Infrastructure Across Cities")

    try:
        
        df = pd.read_csv("data/ict_data.csv", sep='\t')
        df.columns = df.columns.str.strip()


        score_df = pd.read_csv("data/City_ict_scores.csv", sep='\t')
        score_df.columns = score_df.columns.str.strip()  # Optional cleanup

    except FileNotFoundError:
        st.error("Required ICT data files not found in /data folder.")
        return

    # City selector
    cities = df["City"].unique()
    selected_city = st.selectbox("Select a City", sorted(cities))

    city_df = df[df["City"] == selected_city]

    st.subheader(f"📶 ICT Parameters in {selected_city}")
    st.dataframe(city_df)

    # Bar chart for infrastructure components
    infra_cols = [
    "Household Internet Access (%)",
    "Fixed Broadband Subscriptions (%)",
    "Wireless Broadband Subscriptions (%)",
    "Wireless Broadband Coverage 4G (%)"
]

    

    city_vals = city_df[infra_cols].mean().reset_index()
    city_vals.columns = ['Metric', 'Value']

    fig1 = px.bar(
    city_vals, x='Metric', y='Value', 
    title=f"{selected_city} - ICT Infrastructure Overview", 
    color='Metric'
    )

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🌐 City-wise ICT Score Comparison")
    fig2 = px.bar(score_df, x='City', y='ICT_Score', color='ICT_Score', title="Overall ICT Readiness Score by City")
    st.plotly_chart(fig2, use_container_width=True)
