import os
import json
import requests
from flask import Flask, jsonify, request
from dotenv import load_dotenv
import redis
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from .env file into the program
load_dotenv()

app = Flask(__name__)
app.json.ensure_ascii = False # allow non-ASCII characters in query string (e.g. Cyrillic)

# Connect to Redis using URL from .env file, decode_responses=True returns strings instead of bytes
r = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

# Configure rate limiter: identify users by IP address, set default limits for all routes
limiter = Limiter(
    get_remote_address,
    app=app, # integrate Limiter into our Flask application
    default_limits=["100 per day", "10 per minute"]
)

API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"


@app.route('/weather', methods=['GET'])
@limiter.limit("10 per minute") # decorator: sets request limit for this route (runs before the function)
def get_weather():
    city = request.args.get('city') # get 'city' value from query string (e.g. /weather?city=Paris)

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    cached = r.get(city) # check if city weather data exists in Redis cache
    if cached:
        return jsonify({"source": "cache", "data": json.loads(cached)}), 200

    url = f"{BASE_URL}/{city}?key={API_KEY}&unitGroup=metric&include=current"

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Weather service is unavailable, please try again later"}), 503

    if response.status_code != 200:
        # Response.text contains error details from Visual Crossing
        return jsonify({"error": "Failed to fetch weather data", "details": response.text}), response.status_code

    data = response.json()

    weather = {
        "city": city,
        "temperature": data["currentConditions"]["temp"],
        "feels_like": data["currentConditions"]["feelslike"],
        "humidity": data["currentConditions"]["humidity"],
        "description": data["currentConditions"]["conditions"],
        "wind_speed": data["currentConditions"]["windspeed"]
    }

    r.set(city, json.dumps(weather, ensure_ascii=False), ex=43200) # 43,200 seconds = 12 hours

    return jsonify({"source": "api", "data": weather}), 200


if __name__ == '__main__':
    app.run(debug=True) # debug=True enables auto-reload and detailed errors, set to False in production