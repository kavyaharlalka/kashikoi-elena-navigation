import os

import pytest
import src.controller.route_manager as route_manager
import pickle as p
import networkx as nx
import osmnx as ox

from src.controller.helpers import constants
import src.config as config

def create_graph(location, distance, transportation_mode):
    return ox.graph_from_address(location, dist=distance, network_type=constants.TRANSPORTATION_MODES[transportation_mode])

def input_for_test():
    """Create a dummy graph with origin and destination locations for testing
    
    """
    # graph = create_graph("University of Massachusetts Amherst", dist=700)
    # origin_node = ox.nearest_nodes(graph, 42.3878210, -72.5239110)
    # destination_node = 5850477768

def test_get_coordinates_from_nodes():
    """Test function for the cost function. The assertion should pass if the cost function works correctly.

    """
    graph = create_graph("University of Massachusetts Amherst", 700, 1)
    origin_node = 5850031917
    destination_node = 5850477768
    expected_output = [(42.3831146, -72.5214055), (42.3809924, -72.5295381)]
    actual_output = route_manager.get_coordinates_from_nodes(graph, [origin_node, destination_node])
    assert len(actual_output) == len(expected_output)
    assert all([a == b for a, b in zip(actual_output, expected_output)])

def test_get_best_path():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = {'nodes': [5850031917, 66702069, 66716430, 66657614, 7873723660, 7873723658, 66682598,
                                     1445170567, 5850031602, 8388384018, 8388383988, 2296737893, 1445169892, 66654525,
                                     66669179, 1443766524, 66695928, 66699101, 8504871937, 4268906699, 66704353,
                                     6944996582, 66645750, 6353520419, 6353520417, 6353520414, 7278329711,
                                     7278329716, 7278329712, 6313650321, 8390480484, 5850477768],
                           'coordinates': [(42.3831146, -72.5214055), (42.382913, -72.522148), (42.382637, -72.523183),
                                           (42.383673, -72.52374), (42.3841602, -72.5240321), (42.3843242, -72.5241206),
                                           (42.384405, -72.524164), (42.3844277, -72.5244499), (42.3845188, -72.5244884),
                                           (42.385187, -72.5247775), (42.3852413, -72.524801), (42.3853693, -72.5248564),
                                           (42.3854468, -72.5248899), (42.3854218, -72.5249877), (42.3852457, -72.5257545),
                                           (42.3852249, -72.5258406), (42.3849671, -72.5269808), (42.3849387, -72.527095),
                                           (42.3849105, -72.5272099), (42.3847076, -72.52856), (42.384707, -72.528595),
                                           (42.3846231, -72.5286609), (42.384539, -72.5287223), (42.3844565, -72.5287103),
                                           (42.3844569, -72.5287837), (42.3836623, -72.5286169), (42.3826429, -72.5292619),
                                           (42.3825326, -72.5293216), (42.3824351, -72.5293743), (42.3820827, -72.5293453),
                                           (42.3816378, -72.5295789), (42.3809924, -72.5295381)]}
        graph = create_graph("University of Massachusetts Amherst", 700, 1)
        graph = ox.elevation.add_node_elevations_google(graph, api_key=config.GMAP_API_KEY)
        origin_node = 5850031917
        destination_node = 5850477768
        actual_output = route_manager.get_best_path(0, graph, origin_node, destination_node, 200, True)
        assert 'nodes' in actual_output
        assert 'coordinates' in actual_output
        assert len(actual_output['nodes']) == len(expected_output['nodes'])
        assert len(actual_output['coordinates']) == len(expected_output['coordinates'])
        assert all([a == b for a, b in zip(actual_output['nodes'], expected_output['nodes'])])
        assert all([a == b for a, b in zip(actual_output['coordinates'], expected_output['coordinates'])])
    else:
        # skip assertion since elevation is required for which API key is required
        assert 1 == 1

def test_get_map_graph():
    expected_number_of_nodes_in_graph = 59585
    expected_number_of_edges_in_graph = 159740
    cached_graph_file_name = "graph_walk.p"
    if os.path.exists(cached_graph_file_name):
        graph = route_manager.get_map_graph((42.40483030000001, -72.52925239999999), (42.4067032, -72.5355951), 1)
        assert len(graph.nodes) == expected_number_of_nodes_in_graph
        assert len(graph.edges) == expected_number_of_edges_in_graph
    else:
        # skip assertion since we do not want to download the whole graph
        assert 1 == 1

def test_get_distance_from_destination():
    expected_output = 560.8655027567112
    actual_output = route_manager.get_distance_from_destination(42.4067032, -72.5355951, 42.40483030000001, -72.52925239999999)
    assert actual_output == expected_output

def test_calculate_and_get_elevation_gain():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = 2.551000000000002
        graph = create_graph("University of Massachusetts Amherst", 700, 1)
        graph = ox.elevation.add_node_elevations_google(graph, api_key=config.GMAP_API_KEY)
        best_path = [5850031917, 66702069, 66716430, 9053602688, 9053602678, 6353520438, 66623005, 66769370, 66616045,
                          66763514, 66703574, 6353520414, 7278329711, 7278329716, 7278329712, 6313650321, 8390480484, 5850477768]
        actual_output = route_manager.calculate_and_get_elevation(graph, best_path, "gain")
        assert actual_output == expected_output
    else:
        # skip assertion since elevation is required for which API key is required
        assert 1 == 1

def test_calculate_and_get_elevation_drop():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = 21.744999999999997
        graph = create_graph("University of Massachusetts Amherst", 700, 1)
        graph = ox.elevation.add_node_elevations_google(graph, api_key=config.GMAP_API_KEY)
        best_path = [5850031917, 66702069, 66716430, 9053602688, 9053602678, 6353520438, 66623005, 66769370, 66616045,
                          66763514, 66703574, 6353520414, 7278329711, 7278329716, 7278329712, 6313650321, 8390480484, 5850477768]
        actual_output = route_manager.calculate_and_get_elevation(graph, best_path, "drop")
        assert actual_output == expected_output
    else:
        # skip assertion since elevation is required for which API key is required
        assert 1 == 1

def test_get_cost_between_nodes_gain():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = 0.0
        graph = create_graph("University of Massachusetts Amherst", 700, 1)
        graph = ox.elevation.add_node_elevations_google(graph, api_key=config.GMAP_API_KEY)
        origin_node = 5850031917
        destination_node = 5850477768
        actual_output = route_manager.get_cost_between_nodes(graph, origin_node, destination_node, "gain")
        assert actual_output == expected_output
    else:
        # skip assertion since elevation is required for which API key is required
        assert 1 == 1

def test_get_cost_between_nodes_drop():
    if len(config.GMAP_API_KEY) > 0:
        expected_output = 19.193999999999996
        graph = create_graph("University of Massachusetts Amherst", 700, 1)
        graph = ox.elevation.add_node_elevations_google(graph, api_key=config.GMAP_API_KEY)
        origin_node = 5850031917
        destination_node = 5850477768
        actual_output = route_manager.get_cost_between_nodes(graph, origin_node, destination_node, "drop")
        assert actual_output == expected_output
    else:
        # skip assertion since elevation is required for which API key is required
        assert 1 == 1
