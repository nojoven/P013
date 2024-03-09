import pytest  # noqa F401

from locations.utils.helpers import get_continent_from_code


def test_get_continent_from_code():
    assert get_continent_from_code("AF") == "Africa"
    assert get_continent_from_code("NA") == "North America"
    assert get_continent_from_code("OC") == "Oceania"
    assert get_continent_from_code("AN") == "Antarctica"
    assert get_continent_from_code("AS") == "Asia"
    assert get_continent_from_code("EU") == "Europe"
    assert get_continent_from_code("SA") == "South America"
    assert get_continent_from_code("XX") is None
    assert get_continent_from_code(165723) is None
