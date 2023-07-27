from flask import Flask, render_template, request, jsonify
import requests
import random
import os


app = Flask(__name__)

weather_data = {}

API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")


def get_weather(user_input):
    weather_data = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=metric&APPID={API_KEY}")

    if weather_data.json().get('cod') == '404':
        return None
    else:
        weather = weather_data.json()['weather'][0]['main']
        temp = round(weather_data.json()['main']['temp'])
        return weather, temp



def get_weather_quote(weather):
    quotes = {
        'Rain': [
            "Let the rain wash away your worries and bring you renewed energy. - Bob Marley",
            "Dance in the rain and let it cleanse your spirit. - Ziggy Marley",
            "Raindrops are nature's melody, listen and find peace within. - Jimmy Cliff",
            "In the rain, find inspiration and let it nourish your soul. - Bob Marley",
            "Rainy days are the perfect time to reflect and grow. - Ziggy Marley",
            "Rain is a reminder that even storms can bring beauty. - Jimmy Cliff"
        ],
        'Drizzle': [
            "In the gentle drizzle, find tranquility and serenity. - Bob Marley",
            "Drizzle is like nature's soft kiss on your skin. - Ziggy Marley",
            "The drizzle is a whisper from nature, inviting you to slow down and appreciate the small moments. - Jimmy Cliff",
            "Even a little drizzle can bring forth new beginnings. - Ziggy Marley",
            "Drizzle is nature's way of showering you with blessings. - Bob Marley"
        ],
        'Thunderstorm': [
            "In the midst of a thunderstorm, find strength and courage. - Bob Marley",
            "Let the thunderstorm ignite your passion and awaken your spirit. - Ziggy Marley",
            "Thunderstorms remind us of the power within and the resilience of the human spirit. - Jimmy Cliff",
            "Embrace the thunderstorm, for it brings clarity and renewal. - Ziggy Marley",
            "When the thunder roars, let it be a reminder of your inner strength. - Bob Marley"
        ],
        'Snow': [
            "In the silence of the snowfall, find peace and tranquility. - Ziggy Marley",
            "Snowflakes are nature's delicate artwork, marvel at their beauty. - Bob Marley",
            "When it snows, let your inner child come out to play. - Ziggy Marley",
            "Snowfall blankets the world, inviting us to find warmth in each other's hearts. - Jimmy Cliff",
            "The snow whispers serenity, listen closely and find solace. - Ziggy Marley"
        ],
        'Mist': [
            "In the misty morning, find clarity and new perspectives. - Ziggy Marley",
            "Mist is nature's veil, revealing only what is meant to be seen. - Bob Marley",
            "Mist holds secrets waiting to be uncovered, let it guide your journey. - Jimmy Cliff",
            "In the mist, find a sense of mystery and embrace the unknown. - Ziggy Marley",
            "Mist is nature's way of reminding us that not everything needs to be clear. - Bob Marley"
        ],
        'Clear': [
            "Let the clear skies remind you of the endless possibilities that lie ahead. - Bob Marley",
            "Under the clear sky, feel the freedom in your soul. - Ziggy Marley",
            "Clear skies reflect the clarity of your mind. - Jimmy Cliff",
            "In the clear sky, find peace and tranquility. - Ziggy Marley",
            "The clear sky is a canvas waiting for you to paint your dreams upon. - Bob Marley"
        ],
        'Clouds': [
            "Behind every cloud, there is a silver lining waiting to be discovered. - Bob Marley",
            "Clouds may cover the sky, but they cannot overshadow your inner light. - Ziggy Marley",
            "In the clouds, find inspiration and let your imagination soar. - Jimmy Cliff",
            "Clouds bring a sense of mystery and opportunity for change. - Ziggy Marley",
            "Even on cloudy days, the sun is still shining above the clouds. - Bob Marley"
        ],
        'Fog': [
            "Foggy mornings, a mystical time when the world slows down and the spirits come alive. Jah bless the fog! - Bob Marley",
            "In the misty fog, I find inspiration, a reminder that even in obscurity, there's beauty to uncover. - Ziggy Marley",
            "Like the fog that rolls in, reggae's rhythms envelop us, bringing unity and peace to all. - Jimmy Cliff",
            "Fog whispers tales of the unknown, just like reggae's lyrics carry messages of hope and freedom. - Toots Hibbert",
            "Fog blankets the world, and in its embrace, reggae's melodies carry us to a higher state of consciousness. - Peter Tosh",
            "As the fog drifts through the air, reggae's beats move through our souls, connecting us all as one love. - Dennis Brown"
        ],
        'Haze': [
            "In the hazy weather, find tranquility as nature's brush strokes paint a dreamlike canvas in the sky. - Bob Marley",
            "Haze wraps the world in a gentle embrace, reminding us of the beauty in subtlety and mystery. - Ziggy Marley",
            "As the haze veils the horizon, let it ignite your imagination, creating stories in the whispers of the mist. - Jimmy Cliff",
            "Haze is like nature's poetry, each suspended particle a delicate verse, expressing the wonder of existence. - Ziggy Marley",
            "In the hazy mist, discover a sense of wonder, where the familiar transforms into something magical. - Bob Marley",
            "Haze envelops the landscape, revealing only fragments of reality, inviting us to seek meaning beyond what meets the eye. - Ziggy Marley"
        ]

     }

    if weather in quotes:
        return random.choice(quotes[weather])
    else:
        return None




@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['cityName']
        weather = get_weather(user_input)
        if weather:
            weather_quote = get_weather_quote(weather[0])
            data = {
                'city': user_input,
                'weather': weather[0],
                'temp': weather[1],
                'quote': weather_quote
            }
            weather_data[user_input] = data
        else:
            error = "Oops! The city name is incorrect or not found. Please try again."
            return render_template("index.html", data=None, error=error)

    return render_template("index.html", data=weather_data.get(request.form.get('cityName')), error=None)




@app.route("/add_weather_data", methods=['POST'])
def add_weather_data():
    city = request.form['cityName']
    if city not in weather_data:
        weather = get_weather(city)
        if weather:
            weather_quote = get_weather_quote(weather[0])
            data = {
                'city': city,
                'weather': weather[0],
                'temp': weather[1],
                'quote': weather_quote
            }
            weather_data[city] = data
            return jsonify(data), 201
        else:
            return jsonify({'message': 'City not found in OpenWeatherMap'}), 404
    else:
        return jsonify({'message': 'City data already exists'}), 409




@app.route("/update_weather_data", methods=['PUT'])
def update_weather_data():
    city = request.form['city']
    if city in weather_data:
        weather = get_weather(city)
        if weather:
            weather_quote = get_weather_quote(weather[0])
            data = {
                'city': city,
                'weather': weather[0],
                'temp': weather[1],
                'quote': weather_quote
            }
            weather_data[city] = data
            return jsonify(data), 200
        else:
            return jsonify({'message': 'City not found in OpenWeatherMap'}), 404
    else:
        return jsonify({'message': 'City data not found'}), 404




@app.route("/delete_weather_data", methods=['DELETE'])
def delete_weather_data():
    city = request.args.get('city')
    if city in weather_data:
        del weather_data[city]
        return jsonify({'message': 'City data deleted successfully'}), 200
    else:
        return jsonify({'message': 'City data not found'}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)