import os
import json
from datetime import datetime
from locations.utils.helpers import add_weather_to_context
from icecream import ic


class TestAddWeatherToContext:
    def test_add_weather_to_context(self):
        # Get the base directory
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Build the path to the JSON file for the API response
        json_file_path_weather = os.path.join(
            base_dir, "utils", "ninjas_api_weather_paris_response.json"
        )

        # Load the API response from the JSON file
        with open(json_file_path_weather, "r", encoding="utf-8") as f:
            weather_response = json.load(f)
            ic(weather_response)
        # Call the function
        result = add_weather_to_context(weather_response)
        ic(result.keys())
        # Check the result
        assert "Clouds" in result and "%" in result["Clouds"]
        assert "Perceived" in result and "°C" in result["Perceived"]
        assert "Humidity" in result and "%" in result["Humidity"]
        assert "Max" in result and "°C" in result["Max"]
        assert "Min" in result and "°C" in result["Min"]
        assert "Temperature" in result and "°C" in result["Temperature"]
        assert "Wind Degrees" in result and "°" in result["Wind Degrees"]
        assert "Wind Speed" in result and "km/h" in result["Wind Speed"]
        assert "Sunrise" in result and isinstance(
            datetime.strptime(result["Sunrise"], "%H:%M:%S"), datetime
        )
        assert "Sunset" in result and isinstance(
            datetime.strptime(result["Sunset"], "%H:%M:%S"), datetime
        )
        assert "citroen" not in result
        assert 87240 not in result
        assert all(result.values())

    def test_add_weather_to_context_with_empty_dict(self):
        # Call the function with an empty dict
        result = add_weather_to_context({})

        # Check the result
        assert result == {}

    def test_add_weather_to_context_with_none(self):
        # Call the function with None
        result = add_weather_to_context(None)

        # Check the result
        assert result == {}
