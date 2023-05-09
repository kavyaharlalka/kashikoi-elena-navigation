import config

from googlemaps import Client

gmaps_client = Client(key=config.GMAP_API_KEY)

def get_coordinates(location):
    geo_code = gmaps_client.geocode(location)
    geo_code_coordinates = geo_code[0]['geometry']['location']

    # Use 'lat' to get latitude and 'lng' to get longitude
    return geo_code_coordinates