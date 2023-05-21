import pytest
import src.controller.route_manager as route_manager
import pickle as p
import networkx as nx
import osmnx as ox

@pytest.fixture
def input_for_test():
    """Create a dummy graph with origin and destination locations for testing
    
    """
    graph = create_graph("University of Massachusetts Amherst", dist=700)
    origin_node = ox.nearest_nodes(graph, 42.3878210, -72.5239110)
    destination_node = 5850477768

def test_cost_function():
    """Test function for the cost function. The assertion should pass if the cost function works correctly.

    """
    length, gradient = 10, 2
    assert route_manager.cost_function(length, gradient) == 1600, "incorrect cost"


# def create_graph(location, distance, transportation_mode):
#     return ox.graph_from_address(location, dist=distance, network_type=constants.TRANSPORTATION_MODES[transportation_mode])