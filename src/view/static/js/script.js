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

// Initialize the map
function initMap() {

           map = new google.maps.Map(document.getElementById('map'), {
             center: {lat: 42.4047084, lng: -72.5289678},
             zoom: 12
           });

           directionsService = new google.maps.DirectionsService();
           directionsRenderer = new google.maps.DirectionsRenderer({
             map: map
           });


             bounds = new google.maps.LatLngBounds();

        // Autocomplete for source input
      var sourceInput = document.getElementById('source');
      var sourceAutocomplete = new google.maps.places.Autocomplete(sourceInput);
      sourceAutocomplete.bindTo('bounds', map);

      // Autocomplete for destination input
      var destinationInput = document.getElementById('destination');
      var destinationAutocomplete = new google.maps.places.Autocomplete(destinationInput);
      destinationAutocomplete.bindTo('bounds', map);

}
      // Initialize the map

    // Show the map with the source and destination markers

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

    function showMap(){
            var short_path;
            var coord_path;
            var validation=true

            if(validation == true) {

            const url = '/getroute';
            const data = {
                           source: document.getElementById("source").value,
                           destination: document.getElementById("destination").value,
                           algorithm_id: parseInt(document.getElementById("algorithm").value),
                           path_percentage: parseFloat(document.getElementById("path_percentage").value),
                           minimize_elevation_gain: document.getElementById("minimize_elevation_gain").value == "1",
                           transportation_mode: parseInt(document.getElementById("transportation_mode").value)
                         };

            fetch(url, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
              .then(response => response.json())
              .then(data=> {
                // Handle the response data
                console.log(data);

               showPathOnMap(data["best_path_route"], data["shortest_path_distance"],  data["shortest_path_gain"],data["best_path_distance"], data["best_path_gain"],
               parseInt(document.getElementById("transportation_mode").value))
              })
              .catch(error => {
                // Handle any errors
                console.error('Error:', error);
              });


        }
        }

        function showPathOnMap( route_path, distance, gainShort, elenavDist, gainElenav, transportation_mode) {
         resetMap();
         var waypoints = [];
         for (var i = 0; i < route_path.length; i++) {
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
           } else {
             console.error('Directions request failed: ' + status);
           }
         });
        }

        function resetMap() {
          // Clear the directions
          directionsRenderer.setDirections(null);

          // Reset the bounds
          bounds = new google.maps.LatLngBounds();

          // Fit the map to the empty bounds
          map.fitBounds(bounds);
        }

        // Call the resetMap function when needed



    // Create a function to plot the distance on Google Maps
    function plotDistanceOnMap(coordPath) {
      // Create a new map instance
    /*
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 12,
        center: coordPath[0] // Set the center of the map to the starting point
      });
    */

      // Create an array to store the LatLng objects for the path
      var pathCoords = [];

      // Iterate through the coordinate path and create LatLng objects
      for (var i = 0; i < coordPath.length; i++) {
        var latLng = new google.maps.LatLng(coordPath[i].latitude, coordPath[i].longitude);
        pathCoords.push(latLng);
      }

      // Create a polyline to represent the path
      var path = new google.maps.Polyline({
        path: pathCoords,
        geodesic: true,
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 2,
        map: map
      });

      // Fit the map bounds to the path
      var bounds = new google.maps.LatLngBounds();
      for (var i = 0; i < pathCoords.length; i++) {
        bounds.extend(pathCoords[i]);
      }
      map.fitBounds(bounds);
    }

