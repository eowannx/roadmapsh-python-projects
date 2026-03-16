# Weather API

A Flask-based REST API that fetches weather data from the Visual Crossing Weather API with Redis caching and rate limiting.

## Features

- Fetches current weather data for any city via Visual Crossing Weather API
- Caches responses in Redis for 12 hours to reduce external API calls
- Rate limiting: 10 requests per minute, 100 per day

## Requirements

- Python 3.9+
- Visual Crossing API Key https://www.visualcrossing.com/weather-api
- Cache server:
  - Windows: [Memurai](https://www.memurai.com/)
  - Linux/macOS: [Redis](https://redis.io/)

All Python dependencies are listed in `requirements.txt` and installed in step 3 of Setup.

## Setup

1. This project is part of a larger repository with multiple projects. Clone the whole repo and navigate to this folder:

```bash
git clone https://github.com/eowannx/roadmapsh-python-projects.git
cd weather-api
```

2. Create and activate virtual environment
```
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate
```

3. Install dependencies
```
pip install -r requirements.txt
```

4. Create `.env` file
```
WEATHER_API_KEY=your_visual_crossing_api_key
REDIS_URL=redis://localhost:6379/0
```

5. Run the application
```
python app.py
```

## Usage
```
GET http://localhost:5000/weather?city=London
```

Example response:
```json
{
  "data": {
    "city": "London",
    "description": "Partially cloudy",
    "feels_like": 6.7,
    "humidity": 85.9,
    "temperature": 8.4,
    "wind_speed": 10.5
  },
  "source": "api"
}
```

`source` will be `"api"` on the first request, and `"cache"` on subsequent requests until the cache expires.

## Project Source

This project is based on the [Weather API](https://roadmap.sh/projects/weather-api-wrapper-service) challenge from [roadmap.sh](https://roadmap.sh).