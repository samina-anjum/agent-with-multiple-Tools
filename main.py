import re
import requests

# Mock weather data (based on Assignment 3)
MOCK_WEATHER_DATA = {
    "karachi": {"temp_c": 29, "condition": "partly cloudy", "humidity": 83, "wind_kmh": 16, "pressure_mb": 998},
    "london": {"temp_c": 15, "condition": "cloudy", "humidity": 70, "wind_kmh": 10, "pressure_mb": 1012},
    "new york": {"temp_c": 22, "condition": "sunny", "humidity": 65, "wind_kmh": 12, "pressure_mb": 1010}
}

# Tool 1: Math addition function
def add(a, b):
    """Performs addition of two numbers."""
    return a + b

# Tool 2: Weather function
def get_weather(city):
    """
    Fetches weather data for a given city using WeatherAPI.com or mock data.
    Args:
        city (str): Name of the city
    Returns:
        dict: Weather data or error message
    """
    # For real API usage (uncomment and add your API key):
    """
    api_key = "YOUR_WEATHERAPI_KEY"  # Replace with actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return {
            "temp_c": data["current"]["temp_c"],
            "condition": data["current"]["condition"]["text"],
            "humidity": data["current"]["humidity"],
            "wind_kmh": data["current"]["wind_kph"],
            "pressure_mb": data["current"]["pressure_mb"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch weather data for {city}: {str(e)}"}
    """
    
    # Mock implementation
    city = city.lower().strip()
    if city in MOCK_WEATHER_DATA:
        return MOCK_WEATHER_DATA[city]
    else:
        return {"error": f"No weather data available for {city}"}

# Multi-Tool Agent class
class MultiToolAgent:
    def __init__(self):
        self.tools = {
            "add": add,
            "get_weather": get_weather
        }
    
    def process_query(self, query):
        query = query.lower().strip()
        
        # Check for addition pattern (e.g., "What is 5 + 7?")
        addition_pattern = r'what\s*is\s*(\d+)\s*\+\s*(\d+)\??'
        addition_match = re.match(addition_pattern, query)
        
        # Check for weather pattern (e.g., "What's the weather in Karachi?")
        weather_pattern = r'what\'?s\s+the\s+weather\s+(?:in\s+)?([\w\s]+)\??'
        weather_match = re.match(weather_pattern, query)
        
        if addition_match:
            num1, num2 = map(int, addition_match.groups())
            result = self.tools["add"](num1, num2)
            return f"The result of {num1} + {num2} is {result}"
        elif weather_match:
            city = weather_match.group(1).strip()
            weather_data = self.tools["get_weather"](city)
            if "error" in weather_data:
                return weather_data["error"]
            return (f"Weather in {city.title()}: {weather_data['condition'].title()}, "
                    f"Temperature: {weather_data['temp_c']}°C, "
                    f"Humidity: {weather_data['humidity']}%, "
                    f"Wind: {weather_data['wind_kmh']} km/h, "
                    f"Pressure: {weather_data['pressure_mb']} mb")
        else:
            return "Sorry, I can only handle addition queries (e.g., 'What is X + Y?') or weather queries (e.g., 'What's the weather in [city]?')."

# Test the agent
def test_multi_tool_agent():
    agent = MultiToolAgent()
    test_queries = [
        "What is 5 + 7?",
        "What's the weather in Karachi?",
        "What is 10 + 20?",
        "What's the weather in London?",
        "What's the weather in Tokyo?",
        "What is the time now?"
    ]
    
    print("Multi-Tool Agent Interactions:")
    print("-" * 50)
    for query in test_queries:
        print(f"Query: {query}")
        print(f"Response: {agent.process_query(query)}")
        print("-" * 50)

if __name__ == "__main__":
    test_multi_tool_agent()