import config

from googlemaps import Client

gmaps_client = Client(key=config.GMAP_API_KEY)

def get_coordinates(location):
    """ Gets the coordinates for an address using Google maps API.
    Parameters:
        location -> The address for which coordinates are to be fetched
    Returns:
        Dictionary of coordinates. Use 'lat' to get latitude and 'lng' to get longitude.
    """
    geo_code = gmaps_client.geocode(location)
    geo_code_coordinates = geo_code[0]['geometry']['location']
    return geo_code_coordinates