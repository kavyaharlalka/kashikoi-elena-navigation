import networkx
import osmnx as ox
from config import GMAP_API_KEY

COORDINATE_X = 'x'
COORDINATE_Y = 'y'

def get_coordinates_from_nodes(graph, nodes_to_convert):
    return [(graph.nodes[node][COORDINATE_Y], graph.nodes[node][COORDINATE_X]) for node in nodes_to_convert]


def get_shortest_path(graph, start, end, path_percentage, minimize_elevation_gain):
    print(start)
    print(end)

    nx_graph = networkx.Graph(graph)
    shortest_path_distance = networkx.dijkstra_path_length(nx_graph, source=start, target=end, weight='length')
    max_distance = path_percentage * shortest_path_distance
    def custom_weight_func(u, v, data):
        distance = data['length']
        elevation_gain = abs(nx_graph.nodes[v]['elevation'] - nx_graph.nodes[u]['elevation'])

        if distance > max_distance or elevation_gain < 0:
            return None  # Ignore paths that exceed the max_distance

        # You can customize how elevation gain is prioritized (minimized or maximized)
        return 1.0/elevation_gain if (not minimize_elevation_gain and not elevation_gain == 0) else elevation_gain

    short_path = networkx.dijkstra_path(nx_graph, source=start, target=end, weight=custom_weight_func)
    coord_path = get_coordinates_from_nodes(graph, short_path)
    return {"nodes": short_path, "coordinates": coord_path}


def create_graph(loc, dist, transport_mode='walk', loc_type='address'):
    if loc_type == "address":
        return ox.graph_from_address(loc, dist=dist, network_type=transport_mode)
    elif loc_type == "points":
        return ox.graph_from_point(loc, dist=dist, network_type=transport_mode)
    return None


def populate_graph(graph):
    graph = ox.add_node_elevations_google(graph, api_key=GMAP_API_KEY)
    graph = ox.add_edge_grades(graph)
    return graph


def cost_function(length, gradient):
    penalty_term = gradient ** 2
    return (length *penalty_term)**2

# add cost function to graph
def modify_graph_elevate(graph):
    for _,__,___, data in graph.edges(keys=True, data=True):
        data['impedance'] = -cost_function(data['length'], data['grade'])
        data['rise'] = data['length'] * data['grade']
    return graph

