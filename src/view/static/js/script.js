document.addEventListener('DOMContentLoaded', function() {
initMap();
});

var map;
var bounds;
var sourceMarker;
var  destinationMarker;
var line;

// Initialize the map
function initMap() {

  map = new google.maps.Map(document.getElementById('map'), {
    center: {lat: 37.7749, lng: -122.4194},
    zoom: 12
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

               showPathOnMap(data["best_path_route"], data["shortest_path_distance"],  data["shortest_path_gain"],data["best_path_distance"], data["best_path_gain"])
              })
              .catch(error => {
                // Handle any errors
                console.error('Error:', error);
              });


        }
        }

        function showPathOnMap(path, distance, gainShort, elenavDist, gainElenav) {
          var source = path[0]
          var dest = path[path.length-1]

          path_points = []
          for (let i = 3; i < path.length-3; i++){
            var lat = path[i][0];
            var long= path[i][1];
            path_points.push({
              location: new google.maps.LatLng(lat,long),stopover: false,
            });
          }

            service = new google.maps.DirectionsService;

          service.route({
            origin: new google.maps.LatLng(source[0], source[1]),
            destination: new google.maps.LatLng(dest[0], dest[1]),
            waypoints: path_points,
            travelMode: 'WALKING'
          }, function(response, status) {
            if (status === 'OK') {
              renderer.setDirections(response);
            } else {
              window.alert('Request failed with error ' + status);
            }
          });
        }


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

