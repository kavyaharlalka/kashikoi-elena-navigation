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


            // Event listener for source input change
      sourceInput.addEventListener('change', function() {
        showMap();
      });

      // Event listener for destination input change
      destinationInput.addEventListener('change', function() {
        showMap();
      });


}
      // Initialize the map

    // Show the map with the source and destination markers

  function showMap() {
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