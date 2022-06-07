import os

import requests
from dotenv import load_dotenv
from flask import Flask, render_template

load_dotenv('venv/.env')

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_weather():
    url = "https://api.openweathermap.org/data/2.5/forecast"

    querystring = {"lat": "54.3520500", "lon": "18.6463700", "units": "metric", "lang": "pl",
                   "appid": os.getenv('api_key')}
    response = requests.request("GET", url, params=querystring)

    city = response.json()['city']
    forecast = response.json()['list']
    return render_template("main.html", city=city, forecast=forecast)


if __name__ == "__main__":
    app.run()
