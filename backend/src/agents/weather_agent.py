"""
Weather Agent - Get real weather data
Calls OpenWeatherMap API to get actual weather information.

Uses the free tier current weather endpoint:
https://api.openweathermap.org/data/2.5/weather

User: "What's the weather in Minneapolis?"
Agent: Gets weather data → Formats with LLM → Returns to user
"""

import os
import requests
from dotenv import load_dotenv
from src.agents.base_agent import BaseAgent

# Load environment variables from .env file
load_dotenv()


class WeatherAgent(BaseAgent):
    """
    Weather agent that fetches real weather data using OpenWeatherMap free tier API.

    Uses the data/2.5/weather endpoint (free tier).
    API key should be set in .env file as OPENWEATHER_API_KEY

    JavaScript equivalent:
    class WeatherAgent extends BaseAgent {
        constructor() {
            super("Weather Agent", "...");
            this.apiKey = process.env.OPENWEATHER_API_KEY;
        }

        async process(message) {
            const location = this.extractLocation(message);
            const weather = await this.getWeather(location);
            return this.formatResponse(weather);
        }
    }
    """

    def __init__(self):
        """
        Initialize Weather Agent.

        Sets up OpenWeatherMap API credentials from environment variables.
        Raises ValueError if OPENWEATHER_API_KEY is not set.
        """
        super().__init__(
            name="Weather Agent",
            description="Get real weather data for any city"
        )

        # Get OpenWeatherMap API key from environment variable
        self.api_key = os.getenv("OPENWEATHER_API_KEY")

        # Validate that API key is configured
        if not self.api_key:
            raise ValueError(
                "OPENWEATHER_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )

        # API endpoints
        # Note: One Call 4.0 requires paid subscription
        # Using free tier 2.5 endpoint instead
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"

        # System prompt for LLM
        self.system_prompt = """You are a helpful weather assistant.
When given weather data, present it clearly to the user.
Be friendly and informative.
Include both Celsius and Fahrenheit temperatures."""

    def process(self, message: str, **kwargs) -> str:
        """
        Process weather request.

        Main flow:
        1. Extract location from user message
        2. Fetch weather data using city name
        3. Format with LLM for nice response

        Parameters:
            message: User's weather question

        Returns:
            str: Formatted weather information

        JavaScript equivalent:
        async process(message) {
            try {
                const location = this.extractLocation(message);
                const weather = await this.getWeather(location);
                return this.formatWithLLM(weather, location, message);
            } catch (error) {
                return `Error: ${error.message}`;
            }
        }
        """
        try:
            # Extract location from user message
            # E.g., "What's the weather in Minneapolis?" → "Minneapolis"
            location = self._extract_location(message)

            if not location:
                return "I couldn't find a location in your message. Try asking: 'What's the weather in [city]?'"

            # Fetch real weather data by city name
            weather_data = self._get_weather(location)

            if not weather_data:
                return f"Sorry, I couldn't fetch weather data for {location}. Try another city."

            # Format with LLM for nice response
            response = self._format_weather_response(weather_data, location, message)

            return response

        except Exception as e:
            return f"Error getting weather: {str(e)}"
    
    def _extract_location(self, message: str) -> str:
        """
        Extract city name from user message.

        Examples:
        "What's the weather in London?" → "London"
        "Is it raining in Paris?" → "Paris"
        "Tell me about weather in Tokyo" → "Tokyo"

        Parameters:
            message: User's message

        Returns:
            str: City name (or empty string if not found)

        JavaScript equivalent:
        _extractLocation(message) {
            const keywords = ["in ", "for ", "at "];
            for (const keyword of keywords) {
                if (message.includes(keyword)) {
                    const parts = message.split(keyword);
                    return parts[1].trim();
                }
            }
            return "";
        }
        """

        # Convert to lowercase for easier matching
        message_lower = message.lower()

        # Common patterns: "weather in [city]", "weather for [city]", etc.
        keywords = ["in ", "for ", "at "]

        # Try each keyword
        for keyword in keywords:
            if keyword in message_lower:
                # Split on keyword and get the part after it
                # "weather in London" → ["weather ", "london"]
                parts = message_lower.split(keyword)

                if len(parts) > 1:
                    # Get the location (everything after keyword)
                    location = parts[1].strip()

                    # Remove question mark if present
                    location = location.replace("?", "").strip()

                    # Get first word only (in case of "London and Paris")
                    location = location.split()[0]

                    return location

        # No location found
        return ""

    def _get_weather(self, location: str) -> dict:
        """
        Fetch weather data from OpenWeatherMap API (free tier).

        Uses the data/2.5/weather endpoint which works with free API key.

        Parameters:
            location: City name (e.g., "London", "Tokyo")

        Returns:
            dict: Weather data or empty dict if error

        JavaScript equivalent:
        async _getWeather(location) {
            const params = {
                q: location,
                appid: this.apiKey,
                units: "metric"
            };

            const response = await fetch(
                this.weatherUrl + '?' + new URLSearchParams(params)
            );

            if (!response.ok) return {};
            return await response.json();
        }
        """

        try:
            # Build parameters for weather API
            params = {
                "q": location,        # City name
                "appid": self.api_key, # API key (authentication)
                "units": "metric"     # Use Celsius
            }

            # Make request to OpenWeatherMap Weather API
            response = requests.get(
                self.weather_url,
                params=params,
                timeout=10
            )

            # Check if successful
            if response.status_code != 200:
                print(f"Weather API error: {response.status_code}")
                print(f"Response: {response.text}")
                return {}

            # Parse and return JSON
            return response.json()

        except requests.exceptions.Timeout:
            print("Weather API timeout")
            return {}

        except requests.exceptions.ConnectionError:
            print("Cannot connect to weather API")
            return {}

        except Exception as e:
            print(f"Error fetching weather: {str(e)}")
            return {}
    
    def _format_weather_response(self, weather_data: dict, location: str, original_message: str) -> str:
        """
        Format weather data into a nice response using LLM.

        Parses the data/2.5/weather API response and uses Mistral to format naturally.

        Parameters:
            weather_data: Raw API response from data/2.5/weather endpoint
            location: City name
            original_message: User's original question

        Returns:
            str: Formatted, human-friendly response

        JavaScript equivalent:
        async _formatWeatherResponse(weatherData, location, originalMessage) {
            const temp = weatherData.main.temp;
            const weatherInfo = `
                Location: ${location}
                Temperature: ${temp}°C
                ...
            `;

            const prompt = `Format this weather information nicely...`;
            return await this.generateResponse(prompt);
        }
        """

        # Extract data from data/2.5/weather API response
        try:
            # API 2.5 structure: { "main": { ... }, "weather": [...], "wind": {...} }
            main = weather_data.get("main", {})
            weather = weather_data.get("weather", [{}])[0]

            temp_c = main.get("temp", 0)
            humidity = main.get("humidity", 0)
            description = weather.get("description", "unknown")
            wind_speed = weather_data.get("wind", {}).get("speed", 0)
            feels_like = main.get("feels_like", temp_c)

            # Convert Celsius to Fahrenheit
            temp_f = (temp_c * 9/5) + 32
            feels_like_f = (feels_like * 9/5) + 32

            # Build raw weather information
            weather_info = f"""
Location: {location}
Temperature: {temp_c}°C ({temp_f:.0f}°F)
Feels Like: {feels_like}°C ({feels_like_f:.0f}°F)
Condition: {description.capitalize()}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s
            """.strip()

            # Use LLM to format nicely
            prompt = f"""You are a friendly weather assistant.
Format this weather information as a natural, conversational response:

{weather_info}

User asked: {original_message}

Provide a friendly, natural response about the weather."""

            # Generate formatted response
            response = self.generate_response(prompt)

            return response

        except Exception as e:
            print(f"Error formatting response: {str(e)}")
            # Fallback: return raw data if formatting fails
            try:
                main = weather_data.get("main", {})
                weather = weather_data.get("weather", [{}])[0]
                desc = weather.get("description", "unknown")
                temp = main.get("temp", 0)
                return f"Weather in {location}: {desc}, {temp}°C"
            except:
                return f"Could not format weather data for {location}"


# Example usage:
if __name__ == "__main__":
    # Create agent
    agent = WeatherAgent()

    print(f"Agent: {agent.name}")
    print(f"Description: {agent.description}")
    print("=" * 60)
    print()

    # Test 1: Weather in London
    print("Test 1: 'What's the weather in London?'")
    response = agent.process("What's the weather in London?")
    print(f"Response: {response}\n")

    # Test 2: Weather in New York
    print("Test 2: 'Tell me the weather in New York'")
    response = agent.process("Tell me the weather in New York")
    print(f"Response: {response}\n")

    # Test 3: Weather in Tokyo
    print("Test 3: 'How's the weather in Tokyo?'")
    response = agent.process("How's the weather in Tokyo?")
    print(f"Response: {response}\n")

    # Test 4: No location
    print("Test 4: No location provided")
    response = agent.process("Is it raining?")
    print(f"Response: {response}")