from flask import render_template, request, abort
import controller.route_manager as route_manager
import controller.api.google_maps_client as gmap_client
import controller.helpers.constants as constants
import osmnx as ox
from werkzeug.exceptions import BadRequest

def home():
    return render_template("index.html")

def help():
    return render_template("help.html")

def getroute():
    data = request.get_json(force=True)
    if constants.REQUEST_JSON_SOURCE_KEY not in data or len(data[constants.REQUEST_JSON_SOURCE_KEY]) == 0:
        raise BadRequest(description="Source is required and should not be empty")
    if constants.REQUEST_JSON_DESTINATION_KEY not in data or len(data[constants.REQUEST_JSON_DESTINATION_KEY]) == 0:
        raise BadRequest(description="Destination is required and should not be empty")
    if constants.REQUEST_JSON_ALGORITHM_ID_KEY not in data \
            or not isinstance(data[constants.REQUEST_JSON_ALGORITHM_ID_KEY], int) \
            or data[constants.REQUEST_JSON_ALGORITHM_ID_KEY] < 0 \
            or data[constants.REQUEST_JSON_ALGORITHM_ID_KEY] > 6:
        raise BadRequest(description="Given algorithm is not supported")
    if constants.REQUEST_JSON_PATH_PERCENTAGE_KEY not in data \
            or not isinstance(data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY], (int, float)) \
            or data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY] < 100.0 \
            or data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY] > 200.0:
        raise BadRequest(description="Path percentage is required and should be valid")
    if constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY not in data \
            or not isinstance(data[constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY], bool):
        raise BadRequest(description="Minimize elevation gain is required and should be valid")

    try:
        graph = route_manager.create_graph("University of Massachusetts Amherst", 700)
        graph = route_manager.populate_graph(graph)
        graph = route_manager.modify_graph_elevate(graph)
        source_coordinates = gmap_client.get_coordinates(data[constants.REQUEST_JSON_SOURCE_KEY])
        source = ox.nearest_nodes(graph, source_coordinates[constants.COORDINATES_LATITUDE], source_coordinates[constants.COORDINATES_LONGITUDE])
        destination_coordinates = gmap_client.get_coordinates(data[constants.REQUEST_JSON_DESTINATION_KEY])
        destination = ox.nearest_nodes(graph, destination_coordinates[constants.COORDINATES_LATITUDE], destination_coordinates[constants.COORDINATES_LONGITUDE])
        return route_manager.get_shortest_path(data[constants.REQUEST_JSON_ALGORITHM_ID_KEY], graph, source,
                                               destination, data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY],
                                               data[constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY])
    except Exception as e:
        abort(500, description="Resource not found")
        # return handle_exception(e)