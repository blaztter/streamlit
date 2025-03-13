import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import sys
import matplotlib


sns.set(style='dark')

# Helper functions untuk bike-sharing data
def create_daily_rentals_df(df):
    # Pastikan menggunakan kolom yang ada di all_df
    daily_rentals = df.resample('D', on='dteday').agg({
        'casual_day': 'sum',
        'registered_day': 'sum',
        'cnt_day': 'sum'
    }).reset_index()
    return daily_rentals

def create_hourly_rentals_df(df):
    hourly_rentals = df.groupby('hr').agg({
        'casual_hour': 'mean',
        'registered_hour': 'mean',
        'cnt_hour': 'mean'
    }).reset_index()
    return hourly_rentals

def create_weather_impact_df(df):
    weather_impact = df.groupby('weathersit_day').agg({
        'cnt_day': 'mean',
        'temp_day': 'mean',
        'hum_day': 'mean'
    }).reset_index()
    return weather_impact

def create_seasonal_analysis_df(df):
    season_analysis = df.groupby('season_day').agg({
        'casual_day': 'sum',
        'registered_day': 'sum',
        'cnt_day': 'sum'
    }).reset_index()
    return season_analysis

# Load data
all_df = pd.read_csv("all_data.csv")

# Konversi datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])



# Sidebar filter
min_date = all_df['dteday'].min().date()
max_date = all_df['dteday'].max().date()

with st.sidebar:
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
main_df = all_df[
    (all_df['dteday'].dt.date >= start_date) & 
    (all_df['dteday'].dt.date <= end_date)
]

# Prepare dataframes
daily_rentals = create_daily_rentals_df(main_df)
hourly_rentals = create_hourly_rentals_df(main_df)
weather_impact = create_weather_impact_df(main_df)
season_analysis = create_seasonal_analysis_df(main_df)


# Dashboard header
st.header('Bike Sharing Analytics Dashboard 🚴')

# 1. Daily Rentals Overview
st.subheader('Daily Rentals Trend')
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Casual", value=f"{daily_rentals['casual_day'].sum():,}")
with col2:
    st.metric("Total Registered", value=f"{daily_rentals['registered_day'].sum():,}")
with col3:
    st.metric("Peak Day", value=daily_rentals.loc[daily_rentals['cnt_day'].idxmax(), 'dteday'].strftime('%d %b %Y'))

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_rentals['dteday'], daily_rentals['cnt_day'], color='#90CAF9')
ax.set_title("Total Peminjaman Harian", fontsize=20)
ax.set_xlabel("Tanggal")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# 2. Hourly Pattern Analysis (Pertanyaan Bisnis 1)
st.subheader('Pola Peminjaman per Jam')
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(data=hourly_rentals, x='hr', y='casual_hour', label='casual_hour', color='#FF6B6B')
sns.lineplot(data=hourly_rentals, x='hr', y='registered_hour', label='registered_hour', color='#4ECDC4')
ax.set_title("Rata-rata Peminjaman per Jam")
ax.set_xlabel("Jam (0-23)")
ax.set_ylabel("Jumlah Peminjaman")
ax.legend()
st.pyplot(fig)

# 3. Weather Impact Analysis (Pertanyaan Bisnis 2)
st.subheader('Dampak Kondisi Cuaca')
col1, col2 = st.columns(2)
with col1:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='weathersit_day', y='cnt_day', data=weather_impact, palette='Blues')
    ax.set_title("Peminjaman berdasarkan Kondisi Cuaca")
    ax.set_xlabel("Skala Cuaca (1: Terbaik)")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(x='temp_day', y='cnt_day', data=all_df, hue='hum_day', palette='viridis')
    ax.set_title("Pengaruh Suhu & Kelembapan")
    ax.set_xlabel("Suhu (Normalized)")
    st.pyplot(fig)

# 4. Seasonal Analysis
st.subheader('Analisis Musiman')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='season_day', y='cnt_day', data=season_analysis, palette='winter')
ax.set_title("Total Peminjaman per Musim")
ax.set_xlabel("Musim (1: Spring, 2: Summer, 3: Fall, 4: Winter)")
ax.set_ylabel("Total Peminjaman")
st.pyplot(fig)

# 5. Peak Hours Analysis
st.subheader('Analisis Jam Sibuk')
peak_hours = hourly_rentals.nlargest(5, 'cnt_hour')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='hr', y='cnt_hour', data=peak_hours, palette='magma')
ax.set_title("5 Jam dengan Peminjaman Tertinggi")
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Peminjaman")
st.pyplot(fig)

st.caption('Analytics Dashboard © 2024 | Bike Sharing Data')
