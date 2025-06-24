var map = L.map('map').setView([4.628199552170864, -74.06569003375023], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

function onMapClick(e) {
     var marker = L.marker(e.latlng).addTo(map);
}

map.on('click', onMapClick);
