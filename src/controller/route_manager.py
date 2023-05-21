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
    return [(graph.nodes[node][constants.COORDINATES_Y], graph.nodes[node][constants.COORDINATES_X]) for node in nodes_to_convert]

def get_shortest_path(algorithm_id, graph, start, end, path_percentage, minimize_elevation_gain: bool):
    # algorithms = ["Dijkstra", "Bidirectional Dijkstra", "A *", "Bellman - Ford", "Goldberg - Radzik", "Johnson", "Floyd - Warshall"]
    assert algorithm_id in [e.value for e in Algorithms], "Invalid Algorithm ID"
    assert graph is not None, "Invalid Location"
    assert start is not None, "Invalid Source"
    assert end is not None, "Invalid Destination"
    assert path_percentage in range(100, 201), "Invalid Path Percentage"

    print(start)
    print(end)
    shortest_path_distance, short_path = 0, 0

    nx_graph = networkx.Graph(graph)
    shortest_path_distance = networkx.dijkstra_path_length(nx_graph, source=start, target=end, weight='length')
    max_distance = path_percentage * shortest_path_distance

    def custom_weight_func(u, v, data):
        current_distance = data['length']
        elevation_gain = abs(nx_graph.nodes[v]['elevation'] - nx_graph.nodes[u]['elevation'])

        if current_distance > max_distance or elevation_gain < 0:
            return None  # Ignore paths that exceed the max_distance

        # You can customize how elevation gain is prioritized (minimized or maximized)
        return 1.0/elevation_gain if (not minimize_elevation_gain and not elevation_gain == 0) else elevation_gain

    # Dijkstra
    if algorithm_id == Algorithms.DIJKSTRA.value:
        short_path = networkx.dijkstra_path(nx_graph, source=start, target=end, weight=custom_weight_func)
    # Bi-Directional Dijkstra
    elif algorithm_id == Algorithms.BI_DIJKSTRA.value:
        short_path = networkx.bidirectional_dijkstra(nx_graph, start, end, weight=custom_weight_func)[1]
    # A *
    elif algorithm_id == Algorithms.ASTAR.value:
        short_path = networkx.astar_path(nx_graph, start, end, weight=custom_weight_func)
    # Bellman-Ford
    elif algorithm_id == Algorithms.BELLMANFORD.value:
        short_path = networkx.bellman_ford_path(nx_graph, start, end, weight=custom_weight_func)
    # Goldberg-Radzik
    elif algorithm_id == Algorithms.GOLDBERG_RADZIK.value:
        short_path = [end]
        if not start == end:
            # goldberg_radzik algorithm
            predecessors, distances = networkx.goldberg_radzik(networkx.DiGraph(graph), start, weight=custom_weight_func)
            while short_path[-1] != start:
                short_path.append(predecessors[short_path[-1]])
    # Floyd-Warshall
    elif algorithm_id == Algorithms.FLOYD_WARSHALL.value:
        short_path = [end]
        if not start == end:
            predecessors, distance = networkx.floyd_warshall_predecessor_and_distance(nx_graph, weight=custom_weight_func)
            short_path = networkx.reconstruct_path(start, end, predecessors)

    coord_path = get_coordinates_from_nodes(graph, short_path)
    return {"nodes": short_path, "coordinates": coord_path}


def create_graph(location, distance, transportation_mode):
    assert location is not None, "Invalid Location"
    assert distance is not None, "Invalid Distance"
    assert transportation_mode in constants.TRANSPORTATION_MODES, "Invalid Transportation Mode"

    return ox.graph_from_address(location, dist=distance, network_type=constants.TRANSPORTATION_MODES[transportation_mode])


def get_map_graph(source, destination, transportation_mode):
    assert source is not None, "Invalid Location"
    assert destination is not None, "Invalid Distance"
    assert transportation_mode in constants.TRANSPORTATION_MODES, "Invalid Transportation Mode"

    transportation_mode_str = constants.TRANSPORTATION_MODES[transportation_mode]
    cached_graph_file_name = f"./graph_{transportation_mode_str}.p"
    if os.path.exists(cached_graph_file_name):
        print("Loading cached graph")
        map_graph = pickle.load(open(cached_graph_file_name, "rb"))
    else:
        print("Cached graph not found. Downloading and caching, please wait")
        map_graph = ox.graph_from_point(source, dist=30000, dist_type="network", network_type=transportation_mode_str)
        map_graph = ox.elevation.add_node_elevations_google(map_graph, api_key=GMAP_API_KEY)
        pickle.dump(map_graph, open(cached_graph_file_name, "wb"))
        print("Download complete")

    end_node = ox.nearest_nodes(map_graph, destination[1], destination[0], return_dist=False)
    end_location = map_graph.nodes[end_node]
    latitude_1 = end_location[constants.COORDINATES_Y]
    longitude_1 = end_location[constants.COORDINATES_X]
    for node, data in map_graph.nodes(data=True):
        latitude_2 = map_graph.nodes[node][constants.COORDINATES_Y]
        longitude_2 = map_graph.nodes[node][constants.COORDINATES_X]
        data['distance_from_destination'] = get_distance_from_destination(latitude_1, longitude_1, latitude_2, longitude_2)
    return map_graph


def get_distance_from_destination(latitude_1, longitude_1, latitude_2, longitude_2, multiplier=6371008.8):
    # Convert degrees to radians
    coordinates = latitude_1, longitude_1, latitude_2, longitude_2
    phi_1, lambda_1, phi_2, lambda_2 = [
        np.radians(c) for c in coordinates
    ]

    # Haversine formula
    haversine_result = (np.square(np.sin((phi_2 - phi_1) / 2)) + np.cos(phi_1) * np.cos(phi_2) *
                        np.square(np.sin((lambda_2 - lambda_1) / 2)))
    distance = 2 * multiplier * np.arcsin(np.sqrt(haversine_result))

    return distance


def calculate_and_get_elevation(graph, path_nodes, elevation_mode, return_individual_costs = False):
    """ Computes the cost of a route which is the elevation of the route.
    Parameters:
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
    """ defines the cost between two nodes """
    assert node_1 is not None and node_2 is not None, "Invalid node inputs"
    assert elevation_mode in constants.ELEVATION_MODES, "Invalid elevation mode"

    if elevation_mode == "gain":
        return max(0.0, graph.nodes[node_2][constants.KEY_ELEVATION] - graph.nodes[node_1][constants.KEY_ELEVATION])
    elif elevation_mode == "drop":
        if graph.nodes[node_2][constants.KEY_ELEVATION] - graph.nodes[node_1][constants.KEY_ELEVATION] > 0:
            return 0.0
        else:
            return graph.nodes[node_1][constants.KEY_ELEVATION] - graph.nodes[node_2][constants.KEY_ELEVATION]
    else:
        return abs(graph.nodes[node_1][constants.KEY_ELEVATION] - graph.nodes[node_2][constants.KEY_ELEVATION])


def populate_graph(graph):
    assert graph is not None, "Invalid Location"

    graph = ox.add_edge_grades(graph)
    return graph


def cost_function(path_length, gradient):
    penalty_term = gradient ** 2
    return (path_length * penalty_term) ** 2


# add cost function to graph
def modify_graph_elevate(graph):
    assert graph is not None, "Invalid Location"

    for _, __, ___, data in graph.edges(keys=True, data=True):
        data['impedance'] = -cost_function(data['length'], data['grade'])
        data['rise'] = data['length'] * data['grade']
    return graph
