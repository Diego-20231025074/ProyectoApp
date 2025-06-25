var map = L.map('map').setView([4.6282, -74.0657], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap'
}).addTo(map);

// Explicaciones por tipo
const explicaciones = {
  'Buses': 'Problemas relacionados con exceso de buses, rutas mal organizadas o bloqueos.',
  'Carros': 'Congestión vehicular por vehículos particulares o estacionados indebidamente.',
  'TransMilenio': 'Incidentes con estaciones, buses articulados o mala frecuencia.',
  'Peatones': 'Cruces peligrosos, aceras bloqueadas o falta de pasos seguros.',
  'Bicicletas': 'Falta de ciclorrutas o conflictos con otros modos de transporte.'
};

map.on('click', function (e) {
  const latlng = e.latlng;

  const popupContent = `
    <b>¿Qué tipo de problema?</b><br>
    <select id="tipo-problema" onchange="actualizarExplicacion()">
      <option value="">-- Selecciona --</option>
      <option value="Buses">Buses</option>
      <option value="Carros">Carros</option>
      <option value="TransMilenio">TransMilenio</option>
      <option value="Peatones">Peatones</option>
      <option value="Bicicletas">Bicicletas</option>
    </select><br><br>

    <div id="explicacion" style="font-size: 0.9rem; color: #333;"></div>
    <br>
    <textarea id="comentario" rows="3" cols="25" placeholder="Comentario opcional..."></textarea><br>
    <button onclick="guardarReporte(${latlng.lat}, ${latlng.lng})">Guardar Reporte</button>
  `;

  const marker = L.marker(latlng).addTo(map).bindPopup(popupContent).openPopup();
});

// Función global para mostrar explicación
window.actualizarExplicacion = function () {
  const tipo = document.getElementById("tipo-problema").value;
  const explicacion = explicaciones[tipo] || '';
  document.getElementById("explicacion").innerText = explicacion;
};

// Función global para guardar el reporte
window.guardarReporte = function (lat, lng) {
  const tipo = document.getElementById("tipo-problema").value;
  const comentario = document.getElementById("comentario").value.trim();

  if (!tipo) {
    alert("Debes seleccionar un tipo de problema.");
    return;
  }

  const textoPopup = `<b>Tipo:</b> ${tipo}<br><b>Comentario:</b> ${comentario || 'Sin comentario.'}`;
  const marcadorFinal = L.marker([lat, lng]).addTo(map);
  marcadorFinal.bindPopup(textoPopup).openPopup();

  // Aquí podrías guardar en Firebase u otra base de datos
  console.log("Reporte guardado:", {
    tipo,
    comentario,
    coordenadas: { lat, lng }
  });
};
