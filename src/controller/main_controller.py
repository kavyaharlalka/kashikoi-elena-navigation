from flask import render_template, request
import controller.route_manager as route_manager
import controller.api.google_maps_client as gmap_client
import osmnx as ox
import controller.helpers.constants as constants

def home():
    return render_template("index.html")

def help():
    return render_template("help.html")

def getroute():
    # try:
    # assert constants.REQUEST_JSON_SOURCE_KEY in data, "Source is required"

    # try:
    data = request.get_json(force=True)
    graph = route_manager.create_graph("University of Massachusetts Amherst", 700)
    graph = route_manager.populate_graph(graph)
    graph = route_manager.modify_graph_elevate(graph)
    source_coordinates = gmap_client.get_coordinates(data[constants.REQUEST_JSON_SOURCE_KEY])
    source = ox.nearest_nodes(graph, source_coordinates['lat'], source_coordinates['lng'])
    destination_coordinates = gmap_client.get_coordinates(data['destination'])
    destination = ox.nearest_nodes(graph, destination_coordinates['lat'], destination_coordinates['lng'])
    return route_manager.get_shortest_path(data['algorithm_id'], graph, source, destination, float(data['path_percentage']), bool(data['minimize_elevation_gain']))
    # except Exception as e:
    #    print(e)

# @app.errorhandler(Exception)
# def handle_exception(e):
#     """Return JSON instead of HTML for HTTP errors."""
#     # start with the correct headers and status code from the error
#     response = e.get_response()
#     # replace the body with JSON
#     response.data = json.dumps({
#         "code": e.code,
#         "name": e.name,
#         "description": e.description,
#     })
#     response.content_type = "application/json"
#     return response
