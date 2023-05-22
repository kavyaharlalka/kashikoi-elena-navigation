import requests
import time

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT

# request_json = {
#                  "source": "1039 North Pleasant Street, Amherst, MA, USA",
#                  "destination": "12 Brandywine, Amherst, MA, USA",
#                  "algorithm_id": 0,
#                  "path_percentage": 100,
#                  "minimize_elevation_gain": True,
#                  "transportation_mode": 1
#                  }
# post_time_start = time.time()
# server_response = requests.post(f'{server_url}/getroute', json= request_json)
# post_time_end = time.time()
# server_json = server_response.json()
# # print(server_json)

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
