import os
import json
from locations.utils.helpers import add_air_to_context
class TestAddAirToContext:
    def test_add_air_to_context(self):
        # Get the base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Build the path to the JSON file for the API response
        json_file_path_air_quality = os.path.join(base_dir, 'utils', 'ninjas_api_air_paris_response.json')

        # Load the API response from the JSON file
        with open(json_file_path_air_quality, 'r', encoding='utf-8') as f:
            air_quality_response = json.load(f)
            overall_aqi = air_quality_response.get("overall_aqi")
        # Call the function
        result = add_air_to_context(air_quality_response)
        # Check the result
        assert "Overall" in result
        assert "overall_aqi" not in result
        assert "Overall" in result
        assert result["Overall"] == overall_aqi