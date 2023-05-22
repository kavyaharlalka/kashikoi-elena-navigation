import requests
import time

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT
min_elev_response_times = []
max_elev_response_times = []


source = "115 Brittany Manor Drive, Amherst, MA, USA"
path_percentage = 425
destinations = ["Brittany Manor Drive, Amherst, MA, USA",
"United States Postal Service, University Drive, Amherst, MA, USA",
"University of Massachusetts Amherst, Amherst, MA, USA",
"Brandywine Apartments, Brandywine, Amherst, MA, USA",
"Sunderland, MA, USA" ]


minimize_elevation_gain = True
for destination in destinations:
    request_json = {
                                                     "source": source,
                                                     "destination": destination,
                                                     "algorithm_id": 0,
                                                     "path_percentage": path_percentage,
                                                     "minimize_elevation_gain": minimize_elevation_gain,
                                                     "transportation_mode": 1
}

    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/getroute', json= request_json)
    post_time_end = time.time()
    print(server_response)
    server_json = server_response.json()
    if not "message" in server_json:
        min_elev_response_times.append(post_time_end - post_time_start)


minimize_elevation_gain =  False
for destination in destinations:
    request_json = {
                                                     "source": source,
                                                     "destination": destination,
                                                     "algorithm_id": 0,
                                                     "path_percentage": path_percentage,
                                                     "minimize_elevation_gain": minimize_elevation_gain,
                                                     "transportation_mode": 1
                                                     }

    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/getroute', json= request_json)
    post_time_end = time.time()
    print(server_response)
    server_json = server_response.json()
    if not "message" in server_json:
        max_elev_response_times.append(post_time_end - post_time_start)

print(f"min_elevation_reesponse_time:{min_elev_response_times}")
print(f"max_elevation_response_time:{max_elev_response_times}")