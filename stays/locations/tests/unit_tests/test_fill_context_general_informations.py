import json
import os

import pytest

from locations.utils.helpers import fill_context_general_informations


def test_fill_context_general_informations():
    # Get the base directory
    base_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )

    # Build the path to the JSON file
    json_file_path = os.path.join(base_dir, "utils", "restcountries_fr_response.json")

    # Load test data from JSON file
    with open(json_file_path, "r", encoding="utf-8") as f:
        country_details_response = json.load(f)

    # Call the function with the test data
    result = fill_context_general_informations("FR", country_details_response)

    # Check the result
    assert result["Currency"] == "Euro (EUR) - €"
    assert result["Latitude"] == 46
    assert result["Longitude"] == 2
    assert result["Official"] == "French Republic"
    assert result["Native"] == "République française"
    assert result["Capital"] == "Paris"
    assert result["Languages"] == "French"
    assert result["Google"] == "https://goo.gl/maps/g7QxxSFsWyTPKuzd7"
    assert result["OpenStreet"] == "https://www.openstreetmap.org/relation/1403916"
    assert (
        result["coat_of_arms"]
        == "https://mainfacts.com/media/images/coats_of_arms/fr.png"
    )
    assert result["flag"] == "https://flagcdn.com/w320/fr.png"

    # Test error cases
    # Missing key
    del country_details_response[0]["currencies"]
    with pytest.raises(AttributeError):
        fill_context_general_informations("FR", country_details_response)
