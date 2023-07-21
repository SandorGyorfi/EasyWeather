from flask import Flask, render_template, request, jsonify
import requests
import random
from env import API_KEY

app = Flask(__name__)

weather_data = {}

def get_weather(user_input):
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={API_KEY}")

    if weather_data.json()['cod'] == '404':
        return None
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        return weather, temp
