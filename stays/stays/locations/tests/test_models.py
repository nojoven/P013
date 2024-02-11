from ..models import StayCountry

# Create your tests here.

def test_can_select_all_locations():
    stay_country_table  = StayCountry.objects.all()
    assert stay_country_table is not None



