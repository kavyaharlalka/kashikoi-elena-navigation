from flask import render_template, request
import controller.route_manager as route_manager
import controller.api.google_maps_client as gmap_client
import osmnx as ox

def home():
    return render_template("index.html")

def help():
    return render_template("help.html")

def getroute():
    # try:
    data = request.get_json(force=True)
    graph = route_manager.create_graph("University of Massachusetts Amherst", dist=700)
    graph = route_manager.populate_graph(graph)
    graph = route_manager.modify_graph_elevate(graph)
    source_coordinates = gmap_client.get_coordinates(data['source'])
    source = ox.nearest_nodes(graph, source_coordinates['lat'], source_coordinates['lng'])
    destination_coordinates = gmap_client.get_coordinates(data['destination'])
    destination = ox.nearest_nodes(graph, destination_coordinates['lat'], destination_coordinates['lng'])
    return route_manager.get_shortest_path(graph, source, destination, float(data['path_percentage']), bool(data['minimize_elevation_gain']))
    # except Exception as e:
    #    print(e)