from flask import render_template, request
import controller.route_manager as route_manager
import api.google_maps_client as gmap_client
import osmnx as ox

def home():
    return render_template("index.html")

def help():
    return render_template("help.html")

def getroute():
    data = request.get_json(force=True)
    graph = route_manager.create_graph("University of Massachusetts Amherst", dist=700)
    graph = route_manager.populate_graph(graph)
    graph = route_manager.modify_graph_elevate(graph)
    source = ox.nearest_nodes(graph, gmap_client.get_coordinates(data['source']))
    destination = ox.nearest_nodes(graph, gmap_client.get_coordinates(data['destination']))
    return route_manager.get_shortest_path(graph, source, destination, float(data['path_percentage']), bool(data['minimize_elevation_gain']))