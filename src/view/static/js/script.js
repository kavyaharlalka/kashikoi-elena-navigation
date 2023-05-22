document.addEventListener('DOMContentLoaded', function() {
initMap();
});

var map;
var bounds;
var sourceMarker;
var destinationMarker;
var directionsService;
var directionsRenderer
var line;

function scrollDown() {
  // Scroll to the bottom of the page
  window.scrollTo(0, 680);
}

// Initialize the map
function initMap() {
      reset();
        // Autocomplete for source input
      var sourceInput = document.getElementById('source');
      var sourceAutocomplete = new google.maps.places.Autocomplete(sourceInput);
      sourceAutocomplete.bindTo('bounds', map);

      // Autocomplete for destination input
      var destinationInput = document.getElementById('destination');
      var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput);
      destinationAutocomplete.bindTo('bounds', map);

}

 // Show the map with the source and destination markers using line matching bw src and dest
 function showMap2() {
 var sourceInput = document.getElementById('source').value;
      var destinationInput = document.getElementById('destination').value;

      var geocoder = new google.maps.Geocoder();

      // Geocode the source location
      geocoder.geocode({ address: sourceInput }, function (results, status) {
        if (status === 'OK' && results.length > 0) {
          var sourceLatLng = results[0].geometry.location;

          // Geocode the destination location
          geocoder.geocode({ address: destinationInput }, function (results, status) {
            if (status === 'OK' && results.length > 0) {
              var destinationLatLng = results[0].geometry.location;

              // Clear previous markers and line
              if (sourceMarker) {
                sourceMarker.setMap(null);
              }
              if (destinationMarker) {
                destinationMarker.setMap(null);
              }
              if (line) {
                line.setMap(null);
              }

              // Set the center of the map based on the source and destination coordinates
              bounds = new google.maps.LatLngBounds();
              bounds.extend(sourceLatLng);
              bounds.extend(destinationLatLng);
              map.fitBounds(bounds);

              // Create markers for the source and destination locations
              sourceMarker = new google.maps.Marker({
                position: sourceLatLng,
                map: map,
                title: 'Source'
              });
              destinationMarker = new google.maps.Marker({
                position: destinationLatLng,
                map: map,
                title: 'Destination'
              });
                // Create a line connecting the source and destination markers
              line = new google.maps.Polyline({
                path: [sourceLatLng, destinationLatLng],
                geodesic: true,
                strokeColor: '#FF0000',
                strokeOpacity: 1.0,
                strokeWeight: 2,
                map: map
              });
            }
          });
        }
      });
    }


var url = 'your_api_endpoint';
var data = {
  // Your request data
};

    function showMap(){
            var short_path;
            var coord_path;
            var validation=true

            if(validation == true) {
var timeoutMilliseconds = 30000; // Set the timeout value in milliseconds (e.g., 10 seconds)

// Create a timeout promise that will reject after the specified timeout duration
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

               console.log(data);

               showPathOnMap(data["best_path_route"], data["shortest_path_distance"],  data["shortest_path_gain"],data["best_path_distance"], data["best_path_gain"],
               parseInt(document.getElementById("transportation_mode").value))

  })
  .catch(error => {

    // Handle the timeout error and other catchable errors
    if(error.message=="The request took too long. Please try again later.")
    {
    alert(error.message)
    }
    else{
         alert("Implementation for this request doesn't exist. Try again with a different configuration!")
                    console.error('Error:', error);
         }

  });
  }}

      function showPathOnMap( route_path, distance, gainShort, elenavDist, gainElenav, transportation_mode) {
         reset();
         var MAX_WAYPOINTS = 25; // Maximum number of waypoints allowed
         var waypoints = [];
         var numWaypoints = route_path.length;
         var step = Math.ceil(numWaypoints / MAX_WAYPOINTS);
         for (var i = 0; i < numWaypoints; i += step) {
           var latLng = new google.maps.LatLng(route_path[i][0], route_path[i][1]);
           waypoints.push({
             location: latLng,
             stopover: true
           });
           bounds.extend(latLng);
         }

            var travelmode;
            if (transportation_mode == 1)
            travelmode=google.maps.TravelMode.WALKING
            else
            travelmode=google.maps.TravelMode.BICYCLING

         var request = {
           origin: new google.maps.LatLng(route_path[0][0], route_path[0][1]),
           destination: new google.maps.LatLng(route_path[route_path.length - 1][0], route_path[route_path.length - 1][1]),
           waypoints: waypoints,
           travelMode: travelmode
         };

         directionsService.route(request, function(response, status) {
           if (status === google.maps.DirectionsStatus.OK) {
             directionsRenderer.setDirections(response);
             // Fit the map to the bounds of the route
             map.fitBounds(bounds);
             if(numWaypoints>25)
             {
             alert("We have shown an approximated path as the maximum number of waypoints has been exceeded ")
             }

           }  else if (status === google.maps.DirectionsStatus.NOT_FOUND) {
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
                   console.error('Directions request failed: ' + status);
                }
         });
        }

        function reset() {
           map = new google.maps.Map(document.getElementById('map'), {
             center: {lat: 42.4047084, lng: -72.5289678},
             zoom: 12
           });
           directionsService = new google.maps.DirectionsService();
           directionsRenderer = new google.maps.DirectionsRenderer({
             map: map
           });
          bounds = new google.maps.LatLngBounds();
        }




