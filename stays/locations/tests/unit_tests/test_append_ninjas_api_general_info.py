import pytest
import json
import os
from locations.utils.helpers import append_ninjas_api_general_info
from icecream import ic

def test_append_ninjas_api_general_info():
    # Get the base directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Build the path to the JSON file for general_info_dict
    json_file_path_general_info = os.path.join(base_dir, 'utils', 'general_info_initial_dict.json')

    # Load initial general_info_dict from JSON file
    with open(json_file_path_general_info, 'r', encoding='utf-8') as f:
        general_info_dict = json.load(f)

    # Build the path to the JSON file for api_response
    json_file_path_api_response = os.path.join(base_dir, 'utils', 'ninjas_api_countries_fr_response.json')

    # Load api_response from JSON file
    with open(json_file_path_api_response, 'r', encoding='utf-8') as f:
        api_response = json.load(f)
        ic(api_response[0].keys())
    
    # Check if api_response is a list
    assert isinstance(api_response, list)

    # Call the function
    result = append_ninjas_api_general_info(general_info_dict, api_response)

    # Check if the keys of general_info_dict have been modified
    assert "ISO2 CODE" in result
    assert "GDP" in result
    assert "GDP GROWTH" in result
    assert "HOMICIDE RATE" in result
    assert "EMPLOYMENT_AGRICULTURE" in result
    assert "_" not  in result

    # Check corresponding values
    assert result["ISO2 CODE"] == "FR"
    assert "%" in result["HOMICIDE RATE"] == "1.2 %"
    assert all("%" in v for k, v in result.items() if "GROWTH" in k or "RATE" in k)