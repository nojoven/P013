import os
import json
from locations.utils.helpers import add_time_to_context


class TestAddTimeToContext:
    def test_add_time_to_context(self):
        # Get the base directory
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

        # Build the path to the JSON file for the API response
        json_file_path_time = os.path.join(
            base_dir, "utils", "ninjas_api_time_paris_response.json"
        )

        # Load the API response from the JSON file
        with open(json_file_path_time, "r", encoding="utf-8") as f:
            time_response = json.load(f)

        # Call the function
        result = add_time_to_context(time_response)

        # Check the result
        assert (
            "Local_Time" in result and result["Local_Time"] == time_response["datetime"]
        )
        assert (
            "Time_Zone" in result and result["Time_Zone"] == time_response["timezone"]
        )

    def test_add_time_to_context_with_empty_dict(self):
        # Call the function with an empty dict
        result = add_time_to_context({})

        # Check the result
        assert result == {}

    def test_add_time_to_context_with_none(self):
        # Call the function with None
        result = add_time_to_context(None)

        # Check the result
        assert result == {}
