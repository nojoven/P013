from unittest.mock import mock_open, patch
from locations.utils.helpers import get_continent_from_code


def test_get_continent_from_code():
    mock_mapping = {
        "AF": "Africa",
        "NA": "North America",
        "OC": "Oceania",
        "AN": "Antarctica",
        "AS": "Asia",
        "EU": "Europe",
        "SA": "South America",
    }

    with patch("builtins.open", mock_open()):
        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = mock_mapping

            assert get_continent_from_code("AF") == "Africa"
            assert get_continent_from_code("NA") == "North America"
            assert get_continent_from_code("OC") == "Oceania"
            assert get_continent_from_code("AN") == "Antarctica"
            assert get_continent_from_code("AS") == "Asia"
            assert get_continent_from_code("EU") == "Europe"
            assert get_continent_from_code("SA") == "South America"
            assert get_continent_from_code("XX") is None
            assert get_continent_from_code(2589) is None
