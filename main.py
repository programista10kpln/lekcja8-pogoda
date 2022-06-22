import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request

load_dotenv('venv/.env')

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/forecast', methods=['POST', 'GET'])
def get_weather():
    # step 1
    input_city = request.form['city_name'].lower().capitalize()
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"

    geo_querystring = {"q": input_city, "limit": "1", "appid": os.getenv('api_key')}

    geo_response = requests.request("GET", geo_url, params=geo_querystring)
    # step 2

    try:
        lat = geo_response.json()[0]['lat']
        lon = geo_response.json()[0]['lon']

        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

        forecast_querystring = {"lat": lat, "lon": lon, "units": "metric", "lang": "pl",
                                "appid": os.getenv('api_key')}
        forecast_response = requests.request("GET", forecast_url, params=forecast_querystring)

        city = forecast_response.json()['city']
        forecast = forecast_response.json()['list']
        return render_template('forecast.html', input_city=input_city, city=city, forecast=forecast)

    except IndexError:
        return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=True)
