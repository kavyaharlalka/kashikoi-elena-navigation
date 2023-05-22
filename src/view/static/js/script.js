var map;
var bounds;
var sourceMarker;
var destinationMarker;
var directionsService;
var directionsRenderer
var line;


document.addEventListener('DOMContentLoaded', function() {
    initMap();

    const slider = document.getElementById('path_percentage');

    const sliderValue = document.getElementById('sliderValue');

    // Update value when slider value changes
    slider.addEventListener('input', function() {
        sliderValue.textContent = this.value;
    });

    // Clear value on mouseout
    slider.addEventListener('mouseout', function() {
        sliderValue.textContent = '';
    });
});

// Scroll to the bottom of the page to show the form and Map for good user experience
function scrollDown() {
    window.scrollTo(0, 680);
}

// Initialize the map
function initMap() {
    resetMap();
    // Autocomplete for source input
    var sourceInput = document.getElementById('source');
    var sourceAutocomplete = new google.maps.places.Autocomplete(sourceInput);
    sourceAutocomplete.bindTo('bounds', map);

    // Autocomplete for destination input
    var destinationInput = document.getElementById('destination');
    var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput);
    destinationAutocomplete.bindTo('bounds', map);

}

// validate the form inputs
function validateInput() {
    var source = document.getElementById("source").value;
    var destination = document.getElementById("destination").value;
    var algorithm = document.getElementById("algorithm").value;
    var minimize_elevation_gain = document.getElementById("minimize_elevation_gain").value;
    var transportation_mode = document.getElementById("transportation_mode").value;

    if (source == "") {
        window.alert("Source Location is required.");
        return false;
    }

    if (destination == "") {
        window.alert("Destination Location is required.");
        return false;
    }

    if (minimize_elevation_gain == "") {
        window.alert("Elevation is required.");
        return false;
    }

    if (algorithm == "") {
        window.alert("Algorithm is required.");
        return false;
    }

    if (transportation_mode == "") {
        window.alert("Transportation mode is required.");
        return false;
    }

    return true;
}

/* Function to call the /getroute api to fetch best path coordinates between source and destination, when user presses the go button*/
function showMap() {

    input_validation = validateInput();

    if (input_validation == true) {

        const result_prompt = document.getElementById('result');
        result_prompt.textContent = 'Map is loading... Please wait !!!'

        var timeoutMilliseconds = 30000; // Set the timeout value for the API response in milliseconds

        // Timeout promise that will reject after the specified timeout duration

        var timeoutPromise = new Promise((resolve, reject) => {
            setTimeout(() => {
                reject(new Error('The request took too long. Please try again later.'));
            }, timeoutMilliseconds);
        });

        const url = '/getroute';
        const data = {
            source: document.getElementById("source").value,
            destination: document.getElementById("destination").value,
            algorithm_id: parseInt(document.getElementById("algorithm").value),
            path_percentage: parseFloat(document.getElementById("path_percentage").value),
            minimize_elevation_gain: document.getElementById("minimize_elevation_gain").value == "1",
            transportation_mode: parseInt(document.getElementById("transportation_mode").value)
        };

        // Make the API call and race it against the timeout promise
        Promise.race([
                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                }),
                timeoutPromise
            ])
            .then(response => {

                // Check if the response is the timeout error
                if (response instanceof Error) {
                    throw response; // Propagate the timeout error
                }
                return response.json();
            })
            .then(data => {
            var best_route_path=data["best_path_route"];
            var best_path_distance=data["best_path_distance"];
            var best_path_gain=data["best_path_gain"];
            var shortest_path_distance=data["shortest_path_distance"];
            var shortest_path_gain=data["shortest_path_gain"];
            var transportation_mode=parseInt(document.getElementById("transportation_mode").value);
             console.log(data);
             showPathOnMap(best_route_path, best_path_distance, best_path_gain,transportation_mode)

            })
            .catch(error => {
                // Handle the timeout error and other catchable errors
                if (error.message == "The request took too long. Please try again later.") {
                    alert(error.message)
                } else {
                    alert("Implementation for this request doesn't exist. Try again with a different configuration!")
                    console.error('Error:', error);
                }
                reset();
            });
    }
}

/* Function to plot the best path coordinates obtained from the /getroute api */
function showPathOnMap(best_route_path, best_route_distance, best_route_elevgain, transportation_mode) {
    resetMap();
    var MAX_WAYPOINTS = 25; // Maximum number of waypoints allowed in current Google MAP free version
    var waypoints = [];
    var numWaypoints = best_route_path.length;
    var step = Math.ceil(numWaypoints / MAX_WAYPOINTS);
    for (var i = 0; i < numWaypoints; i += step) {
        var latLng = new google.maps.LatLng(best_route_path[i][0], best_route_path[i][1]);
        waypoints.push({
            location: latLng,
            stopover: true
        });
        bounds.extend(latLng);
    }

    var travelMode;
    if (transportation_mode == 1)
        travelMode = google.maps.TravelMode.WALKING
    else
        travelMode = google.maps.TravelMode.BICYCLING

    var request = {
        origin: new google.maps.LatLng(best_route_path[0][0], best_route_path[0][1]),
        destination: new google.maps.LatLng(best_route_path[best_route_path.length - 1][0], best_route_path[best_route_path.length - 1][1]),
        waypoints: waypoints,
        travelMode: travelMode
    };

    directionsService.route(request, function(response, status) {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(response);
            // Fit the map to the bounds of the route
            map.fitBounds(bounds);
            if (numWaypoints > 25) {
                alert("We have shown an approximated path as the maximum number of waypoints has been exceeded ")
            }
            const result_prompt = document.getElementById('result');

            result_prompt.textContent = 'We found the best route for you !!  The elevation gain of this path is ' + best_route_elevgain.toFixed(2) + ' m and the distance is ' + best_route_distance.toFixed(2) + ' m.'

        } else {

            if (status === google.maps.DirectionsStatus.NOT_FOUND) {
                alert('Directions not found. Please check the provided locations.');
            } else if (status === google.maps.DirectionsStatus.ZERO_RESULTS) {
                alert('No route could be found between the provided locations.');
            } else if (status === google.maps.DirectionsStatus.MAX_WAYPOINTS_EXCEEDED) {
                alert('The maximum number of waypoints has been exceeded.');
            } else if (status === google.maps.DirectionsStatus.INVALID_REQUEST) {
                alert('Invalid request. Please check the provided directions request.');
            } else if (status === google.maps.DirectionsStatus.OVER_QUERY_LIMIT) {
                alert('The page has exceeded its query limit for the Directions API.');
            } else if (status === google.maps.DirectionsStatus.REQUEST_DENIED) {
                alert('The page is not allowed to use the Directions API.');
            } else if (status === google.maps.DirectionsStatus.UNKNOWN_ERROR) {
                alert('An unknown error occurred while requesting directions.');
            } else {
                alert('An error occurred with the Directions API.');
            }
            console.error('Some error occurred via Google Maps API' + status);
            reset();
        }
    });
}

/* Function to reset all the fields to their default values on the UI **
**  Invoked in case of error from back-end and when user presses the reset button on UI */
function reset() {
    document.getElementById("source").value = "";
    document.getElementById("destination").value = "";
    document.getElementById("minimize_elevation_gain").value = "0";
    document.getElementById("algorithm").value = "0";
    document.getElementById("transportation_mode").value = "0";
    const result_prompt = document.getElementById('result');
    result_prompt.textContent = 'Fill this form to find the best path on the map'
    resetMap()
}

/* Function to reset the Map on the UI */
function resetMap() {

    // Default Coordinates are set to University of Massachusetts
    map = new google.maps.Map(document.getElementById('map'), {
        center: {
            lat: 42.391155,
            lng: -72.526711
        },
        zoom: 12
    });
    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map
    });
    bounds = new google.maps.LatLngBounds();
}