import requests
import time
import numpy as np
import matplotlib.pyplot as plt

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT
min_elev_response_times = []
max_elev_response_times = []

source = "Brittany Manor Drive, Amherst, MA, USA"
path_percentage = 400
destination = "Hadley Scoop at the Silos, Mill Valley Road, Hadley, MA, USA"
algos=[0,1,2]


minimize_elevation_gain = True
for algo in algos:
    request_json = {
                                                     "source": source,
                                                     "destination": destination,
                                                     "algorithm_id": algo,
                                                     "path_percentage": path_percentage,
                                                     "minimize_elevation_gain": minimize_elevation_gain,
                                                     "transportation_mode": 1
                                                     }

    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/getroute', json= request_json)
    post_time_end = time.time()
    print("Hhh",server_response)
    server_json = server_response.json()
    if not "message" in server_json:
        min_elev_response_times.append(post_time_end - post_time_start)


minimize_elevation_gain =  False
for algo in algos:
    request_json = {
                                                     "source": source,
                                                     "destination": destination,
                                                     "algorithm_id": algo,
                                                     "path_percentage": path_percentage,
                                                     "minimize_elevation_gain": minimize_elevation_gain,
                                                     "transportation_mode": 1
                                                     }

    post_time_start = time.time()
    server_response = requests.post(f'{server_url}/getroute', json= request_json)
    post_time_end = time.time()
    print("Hhh",server_response)
    server_json = server_response.json()
    if not "message" in server_json:
        max_elev_response_times.append(post_time_end - post_time_start)

print(f"Algos:{algos}")

print(f"min_elevation_reesponse_time:{min_elev_response_times}")
print(f"max_elevation_response_time:{max_elev_response_times}")


fig = plt.figure(figsize = (10, 5))

algo=["Dijkstra", "Bidirectional Dijkstra", "A*"]

x = np.arange(3)
width = 0.2

# plot data in grouped manner of bar type
plt.bar(x-0.2, min_elev_response_times, width, color='cyan')
plt.bar(x+0.2, max_elev_response_times, width, color='green')
plt.xticks(x, ["Dijkstra", "Bidirectional Dijkstra", "A*"])
plt.xlabel("Algorithm")
plt.ylabel("API Response Time")
plt.legend(["Minimum Elevation", "Maximum Elevation"])
plt.show()