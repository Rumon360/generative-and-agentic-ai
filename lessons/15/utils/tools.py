import json
import requests


def get_kanye_quote():
    response = requests.get("https://api.kanye.rest/")
    return response.json()["quote"]


def get_weather(city):
    response = requests.get(f"https://wttr.in/{city}?format=j1")
    data = response.json()
    current = data["current_condition"][0]
    return json.dumps({
        "city": city,
        "temp_c": current["temp_C"],
        "feels_like_c": current["FeelsLikeC"],
        "description": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"],
        "wind_kmph": current["windspeedKmph"],
    })


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_kanye_quote",
            "description": "Get a random Kanye West quote. Call this whenever the user asks for a Kanye quote.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city. Call this whenever the user asks about the weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. 'London' or 'New York'",
                    },
                },
                "required": ["city"],
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "get_kanye_quote": get_kanye_quote,
    "get_weather": get_weather,
}
