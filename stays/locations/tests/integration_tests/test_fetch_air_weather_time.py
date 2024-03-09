import json
import os

import pytest

from locations.utils.helpers import fetch_air_weather_time


class TestFetchAirWeatherTimeIntegration:
    @pytest.mark.asyncio
    async def test_fetch_air_weather_time_integration(self):
        # Get the base directory
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Build the path to the JSON file for general_info
        json_file_path_general_info = os.path.join(
            base_dir, "utils", "country_general_info.json"
        )

        # Load general_info from JSON file
        with open(json_file_path_general_info, "r", encoding="utf-8") as f:
            general_info = json.load(f)

        # Call the function
        result = await fetch_air_weather_time(general_info)

        # Check the result
        assert all(response is not None for response in result.values())
        assert 6487132 not in result
        assert isinstance(result, dict)
        assert "air" in result
        assert "weather" in result
        assert "time" in result
        assert "koko" not in result
        assert None not in result

        assert all(len(response) > 0 for response in result.values())
        assert all(isinstance(response, dict) for response in result.values())
