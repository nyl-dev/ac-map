// Initialize Leaflet map
var map = L.map('map').setView([0, 0], 2); // Set initial map center and zoom level

// Add OpenStreetMap tiles to the map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Load JSON data from file
fetch('/data/output.json')
  .then(response => response.json())
  .then(jsonData => {
    // Loop through the JSON data and add markers to the map
    jsonData.forEach(function(data) {
      if (!data.exif_data || data.exif_data.length === 0) {
        // Skip entries without exif_data
        console.warn('Skipping entry without exif_data:', data);
        return;
      }
      
      var latLng = [data.exif_data[0].latitude, data.exif_data[0].longitude]; // Extract latitude and longitude
      var popupContent = ''; // Initialize popup content
      
      // Add timestamp to popup content
      if (data.timestamp) {
        popupContent += '<b>Timestamp:</b> ' + data.timestamp + '<br>'; 
      } else {
        popupContent += '<i>Timestamp information not available</i><br>';
      }

      // Add artist to popup content
      if (data.artist) {
        popupContent += '<b>Artist:</b> ' + data.artist + '<br>'; 
      } else {
        popupContent += '<i>Artist information not available</i><br>';
      }

      // Add institution to popup content
      if (data.institution) {
        popupContent += '<b>Institution:</b> ' + data.institution; 
      } else {
        popupContent += '<i>Institution information not available</i>';
      }
      
      L.marker(latLng).addTo(map).bindPopup(popupContent); // Add marker with popup
    });
  })
  .catch(error => console.error('Error loading JSON:', error));