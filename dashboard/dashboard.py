import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
import os
sns.set(style='dark')

path = os.path.join(os.getcwd(), 'day.csv')

day = pd.read_csv(path)

def create_year_wind(df,year):
    year_windspeed = day_df[day_df.dteday.dt.year == year]
    year_windspeed = year_windspeed.resample(rule='M', on='dteday').agg({
        "windspeed": "mean"
        })
    
    year_windspeed.index = year_windspeed.index.strftime('%B')
    
    return year_windspeed

def number_to_month(nmbr):
    name_mnth = ['Januari','February','March','April','May',
            'June','July','August','September','October',
            'November','Desember']
    return name_mnth[nmbr - 1]

def get_year(df):
    years = df['yr'].unique()
    
    return years

def get_month(df, year):
    year_df = df[df['yr'] == year]
    month = sorted(year_df['mnth'].unique())
    month = [number_to_month(montth) for montth in month]
    return month

def get_temp_atemp_hum_wind():
    return ["temp","atemp","hum","windspeed"]

def show_temp_atemp_hum_wind(df,year):
    new_df = df[(df['yr'] == year)]
    mean_df = new_df.agg({
        'temp' : 'mean',
        'atemp' : 'mean',
        'hum'   : 'mean',
        'windspeed' : 'mean'
    })
    return round(mean_df,2)

def temp_year(df,year):
    new_df = df[(df['yr'] == year)]
    avg_temp = new_df.groupby(by=['mnth']).agg({
        'temp' : 'mean'
    })
    
    avg_temp.index = [number_to_month(month) for month in avg_temp.index]
    avg_temp.reset_index(drop=True)
    return round(avg_temp, 2)

def hum_year(df, year):
    new_df = df[(df['yr'] == year)]
    avg_hum = new_df.groupby(by=['mnth']).agg({
        'hum' : 'mean'
    })
    
    avg_hum.index = [number_to_month(month) for month in avg_hum.index]
    avg_hum.reset_index(drop=True)
    return round(avg_hum, 2)

def wind_year(df, year):
    new_df = df[(df['yr'] == year)]
    avg_wind = new_df.groupby(by=['mnth']).agg({
        'windspeed' : 'mean'
    })
    
    avg_wind.index = [number_to_month(month) for month in avg_wind.index]
    avg_wind.reset_index(drop=True)
    return round(avg_wind, 2)

#header
st.header('Bike Share Dashboard')

col1, col2, col3, col4 = st.columns(4)

with col1:
    years = get_year(day)
    year = st.selectbox(label="year", label_visibility='collapsed', options=years)
    
with col2:
    temp_recap = temp_year(day,year).values[0]
    st.metric("Temperature in Celcius", value=temp_recap)
    
with col3:
    hum_recap = hum_year(day, year).values[0]
    st.metric("Humidity", value=hum_recap)

with col4:
    wind_recap = wind_year(day, year).values[0]
    st.metric("Windspeed", value=wind_recap)
    
with st.container():
    temperature = temp_year(day, year)
    fig = px.line(temperature, title="Average Temperature by Month",
                  labels={
                      'index' : 'Month',
                      'value' : 'Average Temperatur'})
    fig.update_traces(showlegend =False, mode="lines+markers")
    st.write(fig)
    
with st.container():
    humidity = hum_year(day, year)
    fig = px.line(humidity, title="Average Humidity by Month",
                  labels={
                      'index' : 'Month',
                      'value' : 'Average Humidity'})
    fig.update_traces(showlegend =False, mode="lines+markers")
    st.write(fig)

with st.container():
    wind = wind_year(day, year)
    fig = px.line(wind, title="Average Windspeed by Month",
                  labels={
                      'index' : 'Month',
                      'value' : 'Average Windspeed'})
    fig.update_traces(showlegend =False, mode="lines+markers")
    st.write(fig)
    
with st.container():
    temp_wind_hum = show_temp_atemp_hum_wind(day, year)
    
    fig = px.bar(temp_wind_hum,
                 orientation='h',
                 title="Average Temperature,Humidity,Windspeed",
                 labels={"index": "Temperature,Humidity,Windspeed", "value":"Average"},
                 color=temp_wind_hum.index,
                 color_discrete_sequence=["#ef3456", "#f18218", "#092123", "#234567"])
    fig.update_traces(showlegend=False)
    st.write(fig)
