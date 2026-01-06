import requests

# 🔑 OpenWeather API Key
# (Later you can move this to .env)
API_KEY = "YOUR_OPENWEATHER_API_KEY"


def fetch_environment_by_city(city: str):
    """
    Fetch temperature & humidity using city name
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city},IN&appid={API_KEY}&units=metric"
    )

    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise ValueError("City not found")

    data = response.json()

    return {
        "temperature": round(data["main"]["temp"], 2),
        "humidity": data["main"]["humidity"],
    }


def fetch_environment_by_coords(lat: float, lon: float):
    """
    Fetch environment & weather using latitude and longitude
    """
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise ValueError("Weather data unavailable for this location")

    data = response.json()

    return {
        "temperature": round(data["main"]["temp"], 2),
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": round(data["wind"]["speed"], 2),
        "location": data.get("name", "Unknown")
    }
