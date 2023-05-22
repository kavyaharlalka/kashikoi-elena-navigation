import requests

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT


def test_valid_input():
    """Test that valid input sent to the getroute API corresponds to a 200 OK response code
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 200

def test_illegal_source():
    """Test that a 400 Bad Request response status code is returned when an illegal source address is sent to the API
    An illegal source address is any location outside a 30km radius around Amherst.
    """
    request_json = {
                    "source": "Delhi, India",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_illegal_destination():
    """Test that a 400 Bad Request response status code is returned when an illegal destination address is sent to the API
    An illegal destination address is any location outside a 30km radius around Amherst.
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "Delhi, India",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_empty_source():
    """Test that a 400 Bad Request response status code is returned when an empty source address is sent to the API
    """
    request_json = {
                    "source": "",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_empty_destination():
    """Test that a 400 Bad Request response status code is returned when an empty destination address is sent to the API
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_illegal_algorithm_id():
    """Test that a 400 Bad Request response status code is returned when an illegal algorithm ID is sent to the API.
    An illegal algorithm ID is one which is outside the set {0,1,2,3,4,5}
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 8,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_illegal_path_percentage():
    """Test that a 400 Bad Request response status code is returned when an illegal path percentage is sent to the API.
    An illegal path percentage is outside the range [100,500]
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 0,
                    "path_percentage": 700,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 1
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400

def test_illegal_transportation_mode():
    """Test that a 400 Bad Request response status code is returned when an illegal transportation mode is sent to the API.
    An illegal transportation mode is one which is outside the set {0,1}
    """
    request_json = {
                    "source": "1039 North Pleasant Street, Amherst, MA, USA",
                    "destination": "12 Brandywine, Amherst, MA, USA",
                    "algorithm_id": 0,
                    "path_percentage": 100,
                    "minimize_elevation_gain": True,
                    "transportation_mode": 4
                    }
    response = requests.post(f'{server_url}/getroute', json= request_json)
    assert response.status_code == 400