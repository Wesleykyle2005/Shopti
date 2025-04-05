var map = L.map('map').setView([0, 0], 2); 

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);


var customIcon = L.icon({
    iconUrl: '/static/stores/images/custom-marker.png',
    iconSize: [60, 60], 
    iconAnchor: [30, 60], 
    popupAnchor: [0, -60]
});


var stores = JSON.parse(document.getElementById('store-data').textContent);
console.log(stores);

stores.forEach(function(store) {
    var marker = L.marker([store.lat, store.lng], { icon: customIcon }).addTo(map); 
    marker.bindPopup(
        `<b>${store.name}</b><br>${store.description}<br><a href="${store.url}" class="btn btn-primary btn-sm mt-2">Ver productos</a>`
    );
    console.log(store);
});

var bounds = L.latLngBounds(stores.map(store => [store.lat, store.lng]));
map.fitBounds(bounds);