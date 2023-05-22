import sys

import networkx
import numpy as np
import osmnx as ox
from config import GMAP_API_KEY
from enum import Enum
import pickle
import os
import controller.helpers.constants as constants


class Algorithms(Enum):
    DIJKSTRA = 0
    BI_DIJKSTRA = 1
    ASTAR = 2
    BELLMANFORD = 3
    GOLDBERG_RADZIK = 4
    FLOYD_WARSHALL = 5

def get_coordinates_from_nodes(graph, nodes_to_convert):
    """ Gets the coordinates for an array of nodes.
    Parameters:
        graph -> The graph of the map containing the nodes
        nodes_to_convert -> Array of nodes from which coordinates are to be fetched
    Returns:
        Array of coordinates
    """
    return [(graph.nodes[node][constants.COORDINATES_Y], graph.nodes[node][constants.COORDINATES_X]) for node in nodes_to_convert]

def get_best_path(algorithm_id, graph, source_nearest_nodes, destination_nearest_nodes, path_percentage, minimize_elevation_gain: bool):
    """ Get the best path between two nodes as per the given algorithm.
    Parameters:
        algorithm_id -> Id of the algorithm to be used to get the best path
        graph -> The graph of the map containing the nodes
        source_nearest_nodes -> Nodes nearest to the source
        destination_nearest_nodes -> Nodes nearest to the destination
        path_percentage -> Percentage of the shortest path
        minimize_elevation_gain -> Will minimize elevation gain if set to true
    Returns:
        Array of nodes and array of coordinates for the best path
    """
    # algorithms = ["Dijkstra", "Bidirectional Dijkstra", "A *", "Bellman - Ford", "Goldberg - Radzik", "Johnson", "Floyd - Warshall"]
    assert algorithm_id in [e.value for e in Algorithms], "Invalid Algorithm ID"
    assert graph is not None, "Invalid Location"
    assert source_nearest_nodes is not None, "Invalid Source"
    assert destination_nearest_nodes is not None, "Invalid Destination"
    assert path_percentage in range(100, 501), "Invalid Path Percentage"

    print(source_nearest_nodes)
    print(destination_nearest_nodes)

    nx_graph = networkx.Graph(graph)
    shortest_path_distance = networkx.dijkstra_path_length(nx_graph, source=source_nearest_nodes, target=destination_nearest_nodes, weight='length')
    max_distance = (path_percentage * shortest_path_distance) / 100.0

    is_algorithm_with_not_supporting_none = algorithm_id == Algorithms.BELLMANFORD.value or algorithm_id == Algorithms.GOLDBERG_RADZIK.value
    destination_node = graph.nodes[destination_nearest_nodes]
    def custom_weight_func(u, v, data):
        elevation_gain = abs(nx_graph.nodes[v]['elevation'] - nx_graph.nodes[u]['elevation'])

        current_node = nx_graph.nodes[v]
        distance_from_destination = get_distance_from_destination(destination_node[constants.COORDINATES_Y],
                                                                  destination_node[constants.COORDINATES_X],
                                                                  current_node[constants.COORDINATES_Y],
                                                                  current_node[constants.COORDINATES_X])

        if distance_from_destination > max_distance or elevation_gain < 0:
            return sys.maxsize if is_algorithm_with_not_supporting_none else None  # Ignore paths that exceed the max_distance

        # You can customize how elevation gain is prioritized (minimized or maximized)
        return 1.0/elevation_gain if (not minimize_elevation_gain and not elevation_gain == 0) else elevation_gain

    best_path = []
    # Dijkstra
    if algorithm_id == Algorithms.DIJKSTRA.value:
        best_path = networkx.dijkstra_path(nx_graph, source=source_nearest_nodes, target=destination_nearest_nodes, weight=custom_weight_func)
    # Bi-Directional Dijkstra
    elif algorithm_id == Algorithms.BI_DIJKSTRA.value:
        best_path = networkx.bidirectional_dijkstra(nx_graph, source_nearest_nodes, destination_nearest_nodes, weight=custom_weight_func)[1]
    # A *
    elif algorithm_id == Algorithms.ASTAR.value:
        best_path = networkx.astar_path(nx_graph, source_nearest_nodes, destination_nearest_nodes, weight=custom_weight_func)
    # Bellman-Ford
    elif algorithm_id == Algorithms.BELLMANFORD.value:
        best_path = networkx.bellman_ford_path(nx_graph, source_nearest_nodes, destination_nearest_nodes, weight=custom_weight_func)
    # Goldberg-Radzik
    elif algorithm_id == Algorithms.GOLDBERG_RADZIK.value:
        best_path = [destination_nearest_nodes]
        if not source_nearest_nodes == destination_nearest_nodes:
            # goldberg_radzik algorithm
            predecessors, distances = networkx.goldberg_radzik(networkx.DiGraph(graph), source_nearest_nodes, weight='elevation')
            while best_path[-1] != source_nearest_nodes:
                best_path.append(predecessors[best_path[-1]])
    # Floyd-Warshall
    elif algorithm_id == Algorithms.FLOYD_WARSHALL.value:
        best_path = [destination_nearest_nodes]
        if not source_nearest_nodes == destination_nearest_nodes:
            predecessors, distance = networkx.floyd_warshall_predecessor_and_distance(nx_graph, weight='length')
            best_path = networkx.reconstruct_path(source_nearest_nodes, destination_nearest_nodes, predecessors)

    return {"nodes": best_path, "coordinates": get_coordinates_from_nodes(graph, best_path)}


def get_map_graph(source_coordinates, destination_coordinates, transportation_mode):
    print(os.getcwd())
    """ Get the graph object for a map depending on the source
    Parameters:
        source_coordinates -> Tuple of the latitude and longitude coordinates of the source
        destination_coordinates -> Tuple of the latitude and longitude coordinates of the destination
        transportation_mode -> The mode of transportation, either 'walk' or 'bike'
    Returns:
        Graph object for the map
    """
    assert source_coordinates is not None, "Invalid Location"
    assert destination_coordinates is not None, "Invalid Distance"
    assert transportation_mode in constants.TRANSPORTATION_MODES, "Invalid Transportation Mode"

    transportation_mode_str = constants.TRANSPORTATION_MODES[transportation_mode]
    cached_graph_file_name = f"graph_{transportation_mode_str}.p"
    if os.path.exists(cached_graph_file_name):
        print("Loading cached graph")
        map_graph = pickle.load(open(cached_graph_file_name, "rb"))
    else:
        print("Cached graph not found. Downloading and caching, please wait")
        map_graph = ox.graph_from_point(source_coordinates, dist=30000, dist_type="network", network_type=transportation_mode_str)
        map_graph = ox.elevation.add_node_elevations_google(map_graph, api_key=GMAP_API_KEY)
        pickle.dump(map_graph, open(cached_graph_file_name, "wb"))
        print("Download complete")

    return map_graph


def get_distance_from_destination(destination_latitude, destination_longitude, node_latitude, node_longitude):
    """ Get the spherical distance from destination to the given node using the Haversine formula
    Parameters:
        destination_latitude -> Latitude coordinate of the destination
        destination_longitude -> Longitude coordinate of the destination
        node_latitude -> Latitude coordinate of the node to which the distance is to be calculated
        node_longitude -> Longitude coordinate of the node to which the distance is to be calculated
    Returns:
        Spherical distance from the destination to the given node
    """
    # Convert degrees to radians
    coordinates = destination_latitude, destination_longitude, node_latitude, node_longitude
    phi_1, lambda_1, phi_2, lambda_2 = [
        np.radians(c) for c in coordinates
    ]

    # Haversine formula
    multiplier = 6371008.8
    haversine_result = (np.square(np.sin((phi_2 - phi_1) / 2)) + np.cos(phi_1) * np.cos(phi_2) *
                        np.square(np.sin((lambda_2 - lambda_1) / 2)))
    distance = 2 * multiplier * np.arcsin(np.sqrt(haversine_result))

    return distance


def calculate_and_get_elevation(graph, path_nodes, elevation_mode, return_individual_costs=False):
    """ Computes the elevation cost of a route.
    Parameters:
        graph -> The graph of the map containing the nodes
        path_nodes -> Array of Node IDs
        elevation_mode -> Mode of elevation
        return_individual_costs -> If true, returns individual Costs of nodes as well
    Returns:
        total_cost -> total cost
        individual_costs -> Array of individual costs if return_individual_costs is set to true
    """
    assert elevation_mode in constants.ELEVATION_MODES, "Invalid elevation mode"

    total_cost = 0
    individual_costs = []
    for i in range(len(path_nodes) - 1):
        cost_between_nodes = get_cost_between_nodes(graph, path_nodes[i], path_nodes[i + 1], elevation_mode)
        total_cost += cost_between_nodes
        individual_costs.append(cost_between_nodes)
    return (total_cost, individual_costs) if return_individual_costs else total_cost


def get_cost_between_nodes(graph, node_1, node_2, elevation_mode="vanilla"):
    """ Computes the elevation cost between two nodes.
    Parameters:
        graph -> The graph of the map containing the nodes
        node_1 -> The first node
        node_2 -> The second node
        elevation_mode -> Mode of elevation
    Returns:
        Cost between the two nodes
    """
    assert node_1 is not None and node_2 is not None, "Invalid node inputs"
    assert elevation_mode in constants.ELEVATION_MODES, "Invalid elevation mode"

    if elevation_mode == "gain":
        return max(0.0, graph.nodes[node_2][constants.KEY_ELEVATION] - graph.nodes[node_1][constants.KEY_ELEVATION])
    else:
        if graph.nodes[node_2][constants.KEY_ELEVATION] - graph.nodes[node_1][constants.KEY_ELEVATION] > 0:
            return 0.0
        else:
            return graph.nodes[node_1][constants.KEY_ELEVATION] - graph.nodes[node_2][constants.KEY_ELEVATION]


def get_route_edge_attributes(graph, path_nodes, attribute_name):
    """
    Reference - https://osmnx.readthedocs.io/en/stable/osmnx.html#osmnx.utils_graph.get_route_edge_attributes
    Get a list of attribute values for each edge in a path.
    Parameters:
        graph -> input graph
        path_nodes -> list of nodes IDs constituting the path
        attribute_name -> the name of the attribute to get the value of for each edge.
    Returns:
        attribute_values -> list of edge attribute values
    """
    minimize_key = "length"
    attribute_values = []
    for u, v in zip(path_nodes[:-1], path_nodes[1:]):
        edge_data = graph.get_edge_data(u, v)
        if graph.get_edge_data(u, v) is None:
            continue
        else:
            # if there are parallel edges between two nodes, select the one with the lowest value of minimize_key
            data = min(edge_data.values(), key=lambda x: x[minimize_key])
        attribute_value = data[attribute_name]
        attribute_values.append(attribute_value)
    return attribute_values
