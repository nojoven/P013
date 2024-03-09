import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from locations.utils.helpers import fetch_air_weather_time


class TestFetchAirWeatherTime:
    @pytest.mark.asyncio
    @patch("locations.utils.helpers.fetch_additional_data", new_callable=AsyncMock)
    async def test_fetch_air_weather_time(self, mock_fetch_additional_data):
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

        # Build the paths to the JSON files for the API responses
        json_file_path_air_quality = os.path.join(
            base_dir, "utils", "ninjas_api_air_paris_response.json"
        )
        json_file_path_weather = os.path.join(
            base_dir, "utils", "ninjas_api_weather_paris_response.json"
        )
        json_file_path_world_time = os.path.join(
            base_dir, "utils", "ninjas_api_time_paris_response.json"
        )

        # Load the API responses from the JSON files
        with open(json_file_path_air_quality, "r", encoding="utf-8") as f:
            air_quality_response = json.load(f)
        with open(json_file_path_weather, "r", encoding="utf-8") as f:
            weather_response = json.load(f)
        with open(json_file_path_world_time, "r", encoding="utf-8") as f:
            world_time_response = json.load(f)

        # Create mock response objects with the json method returning the mocked data
        mock_response_air_quality = MagicMock()
        mock_response_air_quality.json.return_value = air_quality_response
        mock_response_weather = MagicMock()
        mock_response_weather.json.return_value = weather_response
        mock_response_world_time = MagicMock()
        mock_response_world_time.json.return_value = world_time_response

        # Set the return value of the mock fetch_additional_data function
        mock_fetch_additional_data.return_value = (
            mock_response_air_quality,
            mock_response_weather,
            mock_response_world_time,
        )

        # Call the function
        result = await fetch_air_weather_time(general_info)

        # Check the result
        assert all(response is not None for response in result.values())
        assert "air" in result
        assert "weather" in result
        assert "time" in result
        assert "koko" not in result

        assert all(len(response) > 0 for response in result.values())
        assert all(isinstance(response, dict) for response in result.values())
        assert result["air"] == air_quality_response
        assert result["weather"] == weather_response
        assert result["time"] == world_time_response
