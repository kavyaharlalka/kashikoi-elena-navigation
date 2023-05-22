import requests
import time
import numpy as np
import matplotlib.pyplot as plt

HOST = "127.0.0.1"
PORT = "5000"
server_url = "http://" + HOST + ":" + PORT
response_times = []
cache_response_times = []
dist=[]


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
        response_times.append(post_time_end - post_time_start)
        dist.append(server_json["best_path_distance"])


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
        cache_response_times.append(post_time_end - post_time_start)

print(f"response_times:{response_times}")
print(f"cache_response_times:{cache_response_times}")


plt.plot(dist,response_times, label ='1st Time API Hit (No Cache)')
plt.plot(dist,cache_response_times, '-.', label ='2nd Time API Hit (Cached)')

plt.xlabel("Path Distance (in meters)")
plt.ylabel("API Response Time (in seconds)")
plt.legend()
plt.title('Response Time for 1st time and 2nd time API Hit for same configuration')
plt.show()