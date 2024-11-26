# Date: 2024-11-26

import streamlit as st

import os
import pandas as pd

import requests
import json


### Parse wind direction
def direction_num2word(d):
    offset = 11.25
    # Determine wind direction based on received number
    if d >= (360-offset) or d < (0+offset):
        human_direction = "N"
    elif d >= (337.5-offset) and d < (337.5+offset):
        human_direction = "N/NW"
    elif d >= (315-offset) and d < (315+offset):
        human_direction = "NW"
    elif d >= (292.5-offset) and d < (292.5+offset):
        human_direction = "W/NW"
    elif d >= (270-offset) and d < (270+offset):
        human_direction = "W"
    elif d >= (247.5-offset) and d < (247.5+offset):
        human_direction = "W/SW"
    elif d >= (225-offset) and d < (225+offset):
        human_direction = "SW"
    elif d >= (202.5-offset) and d < (202.5+offset):
        human_direction = "S/SW"
    elif d >= (180-offset) and d < (180+offset):
        human_direction = "S"
    elif d >= (157.5-offset) and d < (157.5+offset):
        human_direction = "S/SE"
    elif d >= (135-offset) and d < (135+offset):
        human_direction = "SE"
    elif d >= (112.5-offset) and d < (112.5+offset):
        human_direction = "E/SE"
    elif d >= (90-offset) and d < (90+offset):
        human_direction = "E"
    elif d >= (67.5-offset) and d < (67.5+offset):
        human_direction = "E/NE"
    elif d >= (45-offset) and d < (45+offset):
        human_direction = "NE"
    elif d >= (22.5-offset) and d < (22.5+offset):
        human_direction = "N/NE"

    return human_direction


### Page title and header
st.title("TODAY'S WEATHER :sun_behind_rain_cloud:")
st.write(
    "Location:"
)

### Read and parse predefined city information
fpath = os.path.join("assets", "worldcities.csv")
data = pd.read_csv(fpath)

#country_set = set(data.loc[:,"country"])
country_list = list(data.loc[:,"country"])
print(len(country_list))
default_idx = country_list.index("Vietnam")

country = st.selectbox('Select a country', options=country_list, index=default_idx)
country_data = data.loc[data.loc[:,"country"] == country,:]
city_set = country_data.loc[:,"city_ascii"]
city = st.selectbox('Select a city', options=city_set, index=1)

### Get city coordinates (lat, lng)
lat = float(country_data.loc[data.loc[:,"city_ascii"] == city, "lat"])
lng = float(country_data.loc[data.loc[:,"city_ascii"] == city, "lng"])

### Fetch the weather information from api open-meteo
response_current = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current_weather=true')

result_current = json.loads(response_current._content)
current = result_current["current_weather"]
temp = current["temperature"]
speed = current["windspeed"]
wd = current["winddirection"]
direct = direction_num2word(wd)

### Show the weather information
st.subheader("Current weather:")
st.info(f"The current temperature is {temp} °C. \n The wind speed is {speed} m/s. \n The wind is coming from {direct}.")


### Weather prediction
st.subheader("Week ahead")
st.write("Temperature and rain forecast one week ahead", unsafe_allow_html=True)

with st.spinner('Loading...'):
    response_hourly = requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&hourly=temperature_2m,precipitation,relative_humidity_2m,wind_speed_10m')
    result_hourly = json.loads(response_hourly._content)
    hourly = result_hourly["hourly"]
    hourly_df = pd.DataFrame.from_dict(hourly)

    ### convert 'time' column to datetime format
    hourly_df['dt'] = pd.to_datetime(hourly_df['time'], format="%Y-%m-%dT%H:%M")
    #st.dataframe(data=hourly_df)

    ### convert to date df
    daily_df = hourly_df.groupby([hourly_df['dt'].dt.date])
    #st.dataframe(data=daily_df)


    st.line_chart(hourly_df['temperature_2m'])
    #st.bar_chart(hourly_df['relative_humidity_2m'])


