var map = L.map('map').setView([4.628199552170864, -74.06569003375023], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// Función para manejar clics en el mapa
function onMapClick(e) {
    var latlng = e.latlng;
    var marker = L.marker(latlng).addTo(map);

    var popupContent = `
        <b>¿Qué sucede aquí?</b><br>
        <textarea id="popup-msg" rows="3" cols="25" placeholder="Ej: Tráfico, accidente..."></textarea><br>
        <button onclick="window.guardarComentario(${latlng.lat}, ${latlng.lng})">Guardar</button>
    `;

    marker.bindPopup(popupContent).openPopup();
}

map.on('click', onMapClick);

// Función global para guardar el comentario del usuario
window.guardarComentario = function(lat, lng) {
    const textarea = document.getElementById("popup-msg");
    if (!textarea || textarea.value.trim() === "") {
        alert("Escribe un mensaje primero.");
        return;
    }

    const mensaje = textarea.value.trim();

    // Crear un nuevo marcador con el comentario
    const marcadorFinal = L.marker([lat, lng]).addTo(map);
    marcadorFinal.bindPopup(`<b>Reporte:</b><br>${mensaje}`).openPopup();
}
