import pytest

from locations.models import StayCountry


class TestStayCountryModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.stay_country = StayCountry(
            continent_name="Asia", country_name="Japan", country_code_of_stay="JP"
        )

    def test_stay_country_continent_name(self):
        assert self.stay_country.continent_name == "Asia"

    def test_stay_country_country_name(self):
        assert self.stay_country.country_name == "Japan"

    def test_stay_country_country_code_of_stay(self):
        assert self.stay_country.country_code_of_stay == "JP"
