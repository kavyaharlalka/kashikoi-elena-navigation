import networkx
import osmnx as ox
from config import GMAP_API_KEY
from enum import Enum

COORDINATE_X = 'x'
COORDINATE_Y = 'y'

TRANSPORTATION_MODE = {0: 'bike', 1: 'walk'}

class Algorithms(Enum):
    DIJKSTRA = 0
    BI_DIJKSTRA = 1
    ASTAR = 2
    BELLMANFORD = 3
    GOLDBERG_RADZIK = 4
    JOHNSON = 5
    FLOYD_MARSHALL = 6

def get_coordinates_from_nodes(graph, nodes_to_convert):
    return [(graph.nodes[node][COORDINATE_Y], graph.nodes[node][COORDINATE_X]) for node in nodes_to_convert]

def get_shortest_path(algorithm_id, graph, start, end, path_percentage, minimize_elevation_gain: bool):
    # algorithms = ["Dijkstra", "Bidirectional Dijkstra", "A *", "Bellman - Ford", "Goldberg - Radzik", "Johnson", "Floyd - Marshall"]
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
    # Johnson
    elif algorithm_id == Algorithms.JOHNSON.value:
        short_path = networkx.johnson(nx_graph, weight='length')
    # Floyd-Marshall
    elif algorithm_id == Algorithms.FLOYD_MARSHALL.value:
        predecessors, distance = networkx.floyd_warshall_predecessor_and_distance(nx_graph, weight=custom_weight_func)
        short_path = networkx.reconstruct_path(start, end, predecessors)

    coord_path = get_coordinates_from_nodes(graph, short_path)
    return {"nodes": short_path, "coordinates": coord_path}


def create_graph(location, distance, transportation_mode):
    assert location is not None, "Invalid Location"
    assert distance is not None, "Invalid Distance"
    assert transportation_mode in TRANSPORTATION_MODE, "Invalid Transportation Mode"
    # if location_type == "address":
    return ox.graph_from_address(location, dist=distance, network_type=TRANSPORTATION_MODE[transportation_mode])
    # elif location_type == "points":
    #     return ox.graph_from_point(location, distance=distance, network_type=transportation_mode)
    # return None


def populate_graph(graph):
    assert graph is not None, "Invalid Location"
    graph = ox.add_node_elevations_google(graph, api_key=GMAP_API_KEY)
    graph = ox.add_edge_grades(graph)
    return graph

def cost_function(path_length, gradient):
    penalty_term = gradient ** 2
    return (path_length * penalty_term) ** 2

# add cost function to graph
def modify_graph_elevate(graph):
    for _, __, ___, data in graph.edges(keys=True, data=True):
        data['impedance'] = -cost_function(data['length'], data['grade'])
        data['rise'] = data['length'] * data['grade']
    return graph
