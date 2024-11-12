import streamlit as st
import pandas as pd
import altair as alt
import requests
from datetime import datetime

conn = st.connection("postgresql")
df = conn.query('SELECT * FROM archive_student.ar_weather;', ttl="340m")

st.title("London Weather & Air Quality")

last_update = df.iloc[[-1]]['update_time'].to_string(index=False)
current_temp = df.iloc[[-1]]['temperature'].to_string(index=False)
current_feel = df.iloc[[-1]]['feelslike'].to_string(index=False)
current_precip = df.iloc[[-1]]['precipitation'].to_string(index=False)
condition_pic = df.iloc[[-1]]['condition_pic'].to_string(index=False)
condition_desc =df.iloc[[-1]]['condition_desc'].to_string(index=False)
current_humidity = df.iloc[[-1]]['humidity'].to_string(index=False)
current_cloud = df.iloc[[-1]]['cloud_cover'].to_string(index=False)
wind_dir = df.iloc[[-1]]['wind_direction'].to_string(index=False)
wind_speed =df.iloc[[-1]]['wind_speed'].to_string(index=False)
windchill = df.iloc[[-1]]['windchill'].to_string(index=False)
defra_index = df.iloc[[-1]]['defra_index'].to_string(index=False)
air_qual = df.iloc[[-1]]['air_quality'].to_string(index=False)
co =df.iloc[[-1]]['co'].to_string(index=False)
no2 = df.iloc[[-1]]['no2'].to_string(index=False)
o3 = df.iloc[[-1]]['o3'].to_string(index=False)
pm10 = df.iloc[[-1]]['pm10'].to_string(index=False)
pm2_5 =df.iloc[[-1]]['pm2_5'].to_string(index=False)
so2 = df.iloc[[-1]]['so2'].to_string(index=False)

if air_qual == 'Low air pollution':
    aq_color = 'green'
elif air_qual == 'Moderate air pollution':
    aq_color = 'orange'
elif air_qual == 'High air pollution':
    aq_color = 'red'
else:
    aq_color = 'grey'
    
with st.sidebar:
    st.title("Current weather")
    st.caption(f'Last updated: {last_update}')
    col1, col2 = st.columns(2)
    with col1:
        temp_cont=st.container(border=True)
        temp_cont.subheader(f'**{current_temp}°C**')
        temp_cont.write(f'{condition_desc}')
    with col2:
        st.image(f'https:{condition_pic}',width=120)
    
    st.write(f'**Feels like:** {current_feel}°C')
    st.write(f'**Current precipitation:** {current_precip}mm')
    st.write(f'**Humidity:** {current_humidity}%')
    st.write(f'**Cloud cover:** {current_cloud}%')
    st.divider()
    st.write(f'**Wind direction:** {wind_dir}')
    st.write(f'**Wind speed:** {wind_speed} mph')
    st.write(f'**Windchill:** {windchill} °C')

weather_cont = st.container(border=True)
tab1, tab2 = weather_cont.tabs(["Past weather", "3-day Forecast"])
with tab1:
    base = alt.Chart(df).encode(alt.X('update_time').title("Date"))
    line =  base.mark_line(color='red').encode(alt.Y('temperature').title("Temperature (°C)"))
    bar = base.mark_bar(color='blue').encode(alt.Y('precipitation').title("Precipitation (mm)"))

    comb = alt.layer(line,bar).resolve_scale(
        y = 'independent').properties(title='Weather tracker')
    st.altair_chart(comb, use_container_width=True)

with tab2:
    api_key = st.secrets['api_key']
    response = requests.get(f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q=London&days=3&aqi=yes').json()
    forecast_days=response['forecast']['forecastday']

    dates = [day['date'] for day in forecast_days]
    max_temps = [day['day']['maxtemp_c'] for day in forecast_days]
    min_temps = [day['day']['mintemp_c'] for day in forecast_days]
    precipitations = [day['day']['totalprecip_mm'] for day in forecast_days]
    rain_chances = [day['day']['daily_chance_of_rain'] for day in forecast_days]
    condition_pics = [day['day']['condition']['icon'] for day in forecast_days]
    #defra_indexes = [day['day']['air_quality']['gb-defra-index'] for day in forecast_days]
    air_qual_fcs= []
    #for each in defra_indexes:
    #    if each <= 3:
    #        air_qual_fcs.append('Low air pollution')
    #    elif each <= 6:
    #        air_qual_fcs.append('Moderate air pollution')
    #    elif each <= 9:
    #        air_qual_fcs.append('High air pollution')
    #    else:
    #        air_qual_fcs.append('Very high air pollution')
    datetime_dates = [datetime.strptime(date, '%Y-%m-%d').date() for date in dates]
    formatted_dates = [date.strftime("%a %d %b %Y") for date in datetime_dates]
    #for fc_aq in air_qual_fcs:
    #    if fc_aq == 'Low air pollution':
    #        aq_color = 'green'
    #    elif fc_aq == 'Moderate air pollution':
    #        aq_color = 'orange'
    #    elif fc_aq == 'High air pollution':
    #        aq_color = 'red'
    #    else:
    #        aq_color = 'grey'

    cola,colb,colc=st.columns(3)
    with cola:
        day0 = st.container(border=True)
        day0.subheader(formatted_dates[0])
        day0.write(f'**Maximum: {max_temps[0]}°C**')
        day0.write(f'**Minimum: {min_temps[0]}°C**')
        day0.write(f'Chance of rain: {rain_chances[0]}% :grey[({precipitations[0]}mm)]')
        day0.image(f'https:{condition_pics[0]}')
    #    day0.write(f':{aq_color}[{air_qual_fcs[0]}]')
    with colb:
        day1 = st.container(border=True)
        day1.subheader(formatted_dates[1])
        day1.write(f'**Maximum: {max_temps[1]}°C**')
        day1.write(f'**Minimum: {min_temps[1]}°C**')
        day1.write(f'Chance of rain: {rain_chances[1]}% :grey[({precipitations[1]}mm)]')
        day1.image(f'https:{condition_pics[1]}')
    #    day1.write(f':{aq_color}[{air_qual_fcs[1]}]')
    with colc:
        day2 = st.container(border=True)
        day2.subheader(formatted_dates[2])
        day2.write(f'**Maximum: {max_temps[2]}°C**')
        day2.write(f'**Minimum: {min_temps[2]}°C**')
        day2.write(f'Chance of rain: {rain_chances[2]}% :grey[({precipitations[2]}mm)]')
        day2.image(f'https:{condition_pics[2]}')
    #    day2.write(f':{aq_color}[{air_qual_fcs[2]}]')

pollutants_df = {
    'Pollutant':['Carbon monoxide (CO)','Nitrogen dioxide (NO2)',
                 'Ozone (O3)','Sulfur dioxide (SO2)',
                 'Coarse particulate matter (<10 microns) (PM10)',
                 'Fine particulate matter (<2.5 microns) (PM2.5)'],
    'Limit (μg/m3)':['10000','40',
             '120','20',
             '40','20'],
    'Current (μg/m3)':[co,no2,o3,so2,pm10,pm2_5]
}
st.divider()

air_qual_cont = st.container(border=True)
air_qual_cont.subheader("Current air quality")
air_qual_cont.write(f'**:{aq_color}[{air_qual}]** (DEFRA index: {defra_index})')
air_qual_cont.dataframe(pollutants_df, use_container_width=True)
with air_qual_cont.expander("More about pollutants"):
    st.write("Carbon monoxide (CO) prevents uptake of oxygen by blood & reduces supply to heart, affecting people with :red[heart disease].")
    st.write("Nitrogen dioxide (NO<sub>2</sub>), ozone (O<sub>3</sub>) & sulfur dioxide (SO<sub>2</sub>) irritate lung airways, affecting those with :red[lung disease].", unsafe_allow_html=True)
    st.write("Particulate matter can deposit into nose/throat (PM<sub>10</sub>) or deep into lungs (PM<sub>2.5</sub>) & cause inflammation, worsening :red[lung & heart conditions].", unsafe_allow_html=True)

air_qual_cont.line_chart(df, x='update_time', y=['co','no2','o3','so2','pm10','pm2_5'], 
                x_label="Date", y_label="Concentration (μg/m3)",
                color=['#53ff00','#b800ff','#0400ff','#ff8700','#ff0000','#ecff00'])
air_qual_cont.caption("Information from [DEFRA UK](https://uk-air.defra.gov.uk)")

