import networkx
import numpy as np
import osmnx as ox
from config import GMAP_API_KEY
from enum import Enum
import pickle as p
import os


COORDINATE_X = 'x'
COORDINATE_Y = 'y'

TRANSPORTATION_MODE = {0: 'bike', 1: 'walk'}

class Algorithms(Enum):
    DIJKSTRA = 0
    BI_DIJKSTRA = 1
    ASTAR = 2
    BELLMANFORD = 3
    GOLDBERG_RADZIK = 4
    FLOYD_WARSHALL = 5

def get_coordinates_from_nodes(graph, nodes_to_convert):
    return [(graph.nodes[node][COORDINATE_Y], graph.nodes[node][COORDINATE_X]) for node in nodes_to_convert]

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
    assert transportation_mode in TRANSPORTATION_MODE, "Invalid Transportation Mode"

    return ox.graph_from_address(location, dist=distance, network_type=TRANSPORTATION_MODE[transportation_mode])

def getGraphOject(start_location, end_location, transportation_mode):
    assert start_location is not None, "Invalid Location"
    assert end_location is not None, "Invalid Distance"
    assert transportation_mode in TRANSPORTATION_MODE, "Invalid Transportation Mode"

    if os.path.exists("./graph.p"):
        G = p.load(open("graph.p", "rb"))
        print("Found Existing Graph")
    else:
        print("Did not find existing Graph. Downloading !!!!")
        G = ox.graph_from_point(start_location, dist=30000, dist_type="network", network_type=TRANSPORTATION_MODE[transportation_mode])
        G = ox.elevation.add_node_elevations_google(G, api_key=GMAP_API_KEY)
        p.dump(G, open("graph.p", "wb"))
        print("Saved Graph !!!!")

    end_node = ox.distance.nearest_nodes(G, end_location[1], end_location[0], return_dist=False)
    end_location = G.nodes[end_node]
    lat1 = end_location['y']
    lon1 = end_location['x']
    for node, data in G.nodes(data=True):
        lat2 = G.nodes[node]['y']
        lon2 = G.nodes[node]['x']
        data['distFromDest'] = calculate_spherical_distance(lat1, lon1, lat2, lon2)
    return G

def calculate_spherical_distance(lat1, lon1, lat2, lon2, r=6371008.8):
    # Convert degrees to radians
    coordinates = lat1, lon1, lat2, lon2
    # radians(c) is same as c*pi/180
    phi1, lambda1, phi2, lambda2 = [
        np.radians(c) for c in coordinates
    ]
    # Apply the haversine formula
    a = (np.square(np.sin((phi2 - phi1) / 2)) + np.cos(phi1) * np.cos(phi2) *
         np.square(np.sin((lambda2 - lambda1) / 2)))
    d = 2 * r * np.arcsin(np.sqrt(a))
    return d

def getElevation(G, route, mode, pairFlag = False):
    """ Computes the cost of a route which is the elevation of the route.
    Parameters:
        route -> List of Node IDs
        mode -> mode of elevation
        pairFlag -> boolean to indicate if individual cost between the nodes needs to be returned
    Returns:
        total -> total cost of the route
        pairElevList -> list of individual costs of the route [Optional]
    """
    total = 0
    if pairFlag : pairElevList = []
    for i in range(len(route)-1):
        if mode == "gain":
            diff = getCost(G, route[i],route[i+1],"gain")
        elif mode == "vanilla":
            diff = getCost(G, route[i],route[i+1],"vanilla")
        else:
            diff = getCost(G, route[i],route[i+1],"drop")
        total += diff
        if pairFlag : pairElevList.append(diff)
    if pairFlag:
        return total, pairElevList
    else:
        return total


def getCost(G, n1, n2, mode="vanilla"):
    """ defines the cost between two nodes """

    if n1 is None or n2 is None: return
    if mode == "gain":
        return max(0.0, G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"])
    elif mode == "drop":
        if G.nodes[n2]["elevation"] - G.nodes[n1]["elevation"] > 0:
            return 0.0
        else:
            return G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"]
    else:
        return abs(G.nodes[n1]["elevation"] - G.nodes[n2]["elevation"])


def populate_graph(graph):
    assert graph is not None, "Invalid Location"

    # graph = ox.add_node_elevations_google(graph, api_key=GMAP_API_KEY)
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
