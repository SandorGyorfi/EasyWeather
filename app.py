from flask import Flask, render_template, request, jsonify
import requests
import random
from env import API_KEY

app = Flask(__name__)

weather_data = {}