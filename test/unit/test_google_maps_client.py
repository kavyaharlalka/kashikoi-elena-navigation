import src.controller.api.google_maps_client as google_maps_client
import src.config as config
import pytest


def test_get_coordinates_invalid_location_results_in_error():
    with pytest.raises(AssertionError, match='Invalid location/address'):
        google_maps_client.get_coordinates("")

def test_get_coordinates():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = {'lat': 42.40483030000001, 'lng': -72.52925239999999}
        actual_output = google_maps_client.get_coordinates("1039 North Pleasant Street, Amherst, MA, USA")
        assert actual_output == expected_output
    else:
        # skip assertion since API key is required to test above function
        assert 1 == 1