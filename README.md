# Weather & Air Quality Dashboard

Weather monitoring is vital for forecasting and planning for the general public but also various industries, such as agriculture and energy companies. Air quality information is important for warning people of potential risks and protecting public health. The changes of both weather and air quality can also demonstrate the effects of climate change.

This project tracks the weather and air quality in London using the API from WeatherAPI.com. It stores the data in an SQL database to create a historical record of the weather and air quality (including current data), which a Streamlit application calls from to visualise the data in graphs. The Streamlit application also pulls data directly from the API to display a 3-day forecast.


[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://weather-air-quality-tracker.streamlit.app/)

1) capstone_weather.py fetches current weather & air quality data from the API and populates the data into a student.ar_weather table. The script sits on the job server and runs on a CRON schedule to be executed every hour.
2) The Streamlit application reads from the database & visualises it to show current/past weather and air quality on a dashboard.
3) The Streamlit application calls data from the API to display a 3-day weather forecast.
