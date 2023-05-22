from flask import render_template, request, abort
import controller.route_manager as route_manager
import controller.api.google_maps_client as gmap_client
import controller.helpers.constants as constants
import osmnx as ox
from werkzeug.exceptions import BadRequest
import model.db_manager as db

def home():
    return render_template("index.html")


def help():
    return render_template("help.html")


def about():
    return render_template("about.html")


def get_route():
    """ Get the best and shortest path between two nodes as per the given algorithm"""
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
    if constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY not in data \
            or not isinstance(data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY], int) \
            or data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY] < 0 \
            or data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY] > 1:
        raise BadRequest(description="Given transportation mode is not supported")

    try:
        result_from_db = db.get_navigation_if_exists(data[constants.REQUEST_JSON_SOURCE_KEY],
                                data[constants.REQUEST_JSON_DESTINATION_KEY],
                                data[constants.REQUEST_JSON_ALGORITHM_ID_KEY],
                                data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY],
                                data[constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY],
                                data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY])

        if result_from_db is not None:
            return result_from_db

        source_coordinates = gmap_client.get_coordinates(data[constants.REQUEST_JSON_SOURCE_KEY])
        destination_coordinates = gmap_client.get_coordinates(data[constants.REQUEST_JSON_DESTINATION_KEY])
        graph = route_manager.get_map_graph((source_coordinates[constants.COORDINATES_LATITUDE], source_coordinates[constants.COORDINATES_LONGITUDE]),
                                            (destination_coordinates[constants.COORDINATES_LATITUDE], destination_coordinates[constants.COORDINATES_LONGITUDE]),
                                            data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY])
        source, source_distance = ox.nearest_nodes(graph, source_coordinates[constants.COORDINATES_LONGITUDE], source_coordinates[constants.COORDINATES_LATITUDE], return_dist=True)
        destination, destination_distance = ox.nearest_nodes(graph, destination_coordinates[constants.COORDINATES_LONGITUDE], destination_coordinates[constants.COORDINATES_LATITUDE], return_dist=True)

        if source_distance > 30000 or destination_distance > 30000:
            raise BadRequest(description="Currently the map only supports a 30km radius around Amherst")

        best_path_algorithm_result = route_manager.get_best_path(data[constants.REQUEST_JSON_ALGORITHM_ID_KEY], graph, source,
                                                                 destination, data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY],
                                                                 data[constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY])
        best_path_algorithm_stats = [best_path_algorithm_result['coordinates'],
                                     route_manager.calculate_and_get_elevation(graph, best_path_algorithm_result['nodes'], "gain"),
                                     route_manager.calculate_and_get_elevation(graph, best_path_algorithm_result['nodes'], "drop")]

        shortest_path_nodes = ox.distance.shortest_path(graph, orig=source, dest=destination)
        shortest_path_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, shortest_path_nodes, 'length'))
        shortest_path_stats = [route_manager.get_coordinates_from_nodes(graph, shortest_path_nodes),
                             shortest_path_distance,
                             route_manager.calculate_and_get_elevation(graph, shortest_path_nodes, "gain"),
                             route_manager.calculate_and_get_elevation(graph, shortest_path_nodes, "drop")]

        result = {
            "best_path_route": best_path_algorithm_stats[0],
            "best_path_distance": 0.0,
            "best_path_gain": best_path_algorithm_stats[1],
            "best_path_drop": best_path_algorithm_stats[2],
            "shortest_path_route": shortest_path_stats[0],
            "shortest_path_distance": shortest_path_stats[1],
            "shortest_path_gain": shortest_path_stats[2],
            "shortest_path_drop": shortest_path_stats[3]
         }

        db.insert_into_database(data[constants.REQUEST_JSON_SOURCE_KEY],
                                data[constants.REQUEST_JSON_DESTINATION_KEY],
                                data[constants.REQUEST_JSON_ALGORITHM_ID_KEY],
                                data[constants.REQUEST_JSON_PATH_PERCENTAGE_KEY],
                                data[constants.REQUEST_JSON_MINIMIZE_ELEVATION_GAIN_KEY],
                                data[constants.REQUEST_JSON_TRANSPORTATION_MODE_KEY],
                                result)
        return result
    except Exception as e:
        abort(400, str(e))
