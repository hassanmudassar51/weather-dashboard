import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Weather Dashboard", page_icon="🌤️", layout="wide")
st.title("🌤️ Live Weather Dashboard")
st.markdown("Yeh dashboard **Open-Meteo API** (Free) ka istamal karta hai.")

st.sidebar.header("City Settings")
city_name = st.sidebar.text_input("Enter City Name:", "Lahore")

def get_coordinates(city):
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&format=json"
    response = requests.get(geocode_url).json()
    if "results" in response:
        location = response["results"][0]
        return location["latitude"], location["longitude"], location["name"], location["country"]
    return None, None, None, None

def get_weather(lat, lon):
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(weather_url).json()
    return response

if city_name:
    lat, lon, name, country = get_coordinates(city_name)
    if lat and lon:
        st.success(f"Location Found: **{name}, {country}**")
        weather_data = get_weather(lat, lon)
        current = weather_data["current_weather"]
        
        st.subheader("Current Weather")
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{current['temperature']} °C")
        col2.metric("Wind Speed", f"{current['windspeed']} km/h")
        col3.metric("Wind Direction", f"{current['winddirection']}°")
        
        st.subheader("🌡️ 24-Hour Temperature Forecast")
        hourly_data = weather_data["hourly"]
        df = pd.DataFrame({
            "Time": pd.to_datetime(hourly_data["time"]),
            "Temperature (°C)": hourly_data["temperature_2m"],
            "Humidity (%)": hourly_data["relative_humidity_2m"]
        })
        df_24h = df.head(24)
        fig = px.line(df_24h, x="Time", y="Temperature (°C)", title=f"Temperature in {name} (Next 24 Hours)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("City not found. Please check the spelling.")
