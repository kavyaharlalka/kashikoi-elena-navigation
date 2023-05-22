import requests

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT


def test_valid_input():
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