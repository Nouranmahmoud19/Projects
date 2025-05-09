
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike sharing Dashboard", layout="wide")

df = pd.read_csv(r"C:\Users\noura\OneDrive\Desktop\Ai Msc\hour.csv")  


# Data preprocessing
df['dteday'] = pd.to_datetime(df['dteday'])
df['season'] = df['season'].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})
df['weekday'] = df['weekday'].map({0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"})
df['yr'] = df['yr'].map({0: 2011, 1: 2012})
df['weathersit'] = df['weathersit'].map({1: "Clear", 2: "Mist", 3: "Light Snow", 4: "Heavy Rain"})
df['mnth'] = df['mnth'].map({1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"})

# Sidebar filters using selectbox
st.sidebar.header("📊 Filter the Data")
year = st.sidebar.selectbox("Select Year", sorted(df['yr'].unique()), index=0)
month = st.sidebar.selectbox("Select Month", sorted(df['mnth'].unique()), index=0)
weekday = st.sidebar.selectbox("Select Weekday", sorted(df['weekday'].unique()), index=0)
weather = st.sidebar.selectbox("Select Weather", sorted(df['weathersit'].unique()), index=0)

# Filter the data based on sidebar selections
df_filtered = df.copy()
df_filtered = df_filtered[df_filtered['yr'] == year]
df_filtered = df_filtered[df_filtered['mnth'] == month]
df_filtered = df_filtered[df_filtered['weekday'] == weekday]
df_filtered = df_filtered[df_filtered['weathersit'] == weather]

# KPIs Section
st.title("🚲 Bike Sharing Dashboard")
st.markdown("### Overview of Bike Sharing")

col1, col2, col3 = st.columns(3)
col1.metric("Total Rides", f"{df_filtered['cnt'].sum():,}")
col2.metric("Casual Users", f"{df_filtered['casual'].sum():,}")
col3.metric("Registered Users", f"{df_filtered['registered'].sum():,}")

# Daily trend - Line chart
st.markdown("### 📅 Daily Ride Trend")
daily = df_filtered.groupby('dteday')['cnt'].sum().reset_index()
fig1 = px.line(daily, x='dteday', y='cnt', title="Total Rides per Day", template="plotly_dark")
fig1.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Date", yaxis_title="Total Rides")
st.plotly_chart(fig1, use_container_width=True)

# Season distribution - Bar chart
st.markdown("### 🌦️ Rides by Season")
season_df = df_filtered.groupby('season')['cnt'].sum().reset_index()
fig2 = px.bar(season_df, x='season', y='cnt', color='season', title="Total Rides per Season", template="plotly_dark")
fig2.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Season", yaxis_title="Total Rides")
st.plotly_chart(fig2, use_container_width=True)

# Temperature scatter plot with trendline
st.markdown("### 🌡️ Temperature Effect on Rides")
fig3 = px.scatter(df_filtered, x='temp', y='cnt', color='season', title="Temperature vs Ride Count", trendline='ols', template="plotly_dark")
fig3.update_layout(title_font_size=24, title_x=0.5, xaxis_title="Temperature (Normalized)", yaxis_title="Total Rides")
st.plotly_chart(fig3, use_container_width=True)


st.markdown("### 🕒 Hourly Ride Distribution")
hourly_df = df_filtered.groupby('hr')['cnt'].sum().reset_index()
fig5 = px.bar(hourly_df, x='hr', y='cnt', title="Total Rides by Hour of the Day", labels={"hr": "Hour", "cnt": "Ride Count"}, template="plotly_dark")
st.plotly_chart(fig5, use_container_width=True)

st.markdown("### 🧍‍♂️ User Type Distribution")
user_counts = df_filtered[['casual', 'registered']].sum().reset_index()
user_counts.columns = ['User Type', 'Count']
fig6 = px.pie(user_counts, values='Count', names='User Type', title='User Type Proportion', template="plotly_dark")
st.plotly_chart(fig6, use_container_width=True)

st.markdown("### 💧 Humidity vs Ride Count")
fig7 = px.scatter(df_filtered, x='hum', y='cnt', color='season', title="Humidity vs Ride Count", trendline='ols', labels={"hum": "Humidity", "cnt": "Ride Count"}, template="plotly_dark")
st.plotly_chart(fig7, use_container_width=True)

st.markdown("### 📦 Ride Count Distribution by Month")
fig9 = px.box(df_filtered, x='mnth', y='cnt', color='mnth', title="Distribution of Ride Counts by Month", template="plotly_dark")
st.plotly_chart(fig9, use_container_width=True)

# Download filtered data
st.download_button("📥 Download Filtered Data", df_filtered.to_csv(index=False), file_name="filtered_bike_data.csv")
