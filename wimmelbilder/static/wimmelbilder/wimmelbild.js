function renderWimmelbild(mapContainerId, data) {
    // map
    var map = L.map(mapContainerId, {
        minZoom: 1,
        maxZoom: L.Browser.retina ? 5 : 6,
        crs: L.CRS.Simple,
        attribution: false,
        fullscreenControl: true,
        zoomDelta: 0.25,
        zoomSnap: 0
    })

    // tiles
    var tileZoom = 6;
    L.tileLayer(data.tileUrl, {
        tms: true,
        detectRetina: true,
        maxZoom: tileZoom
    }).addTo(map)

    // bounds
    var width = data.width
    var height = data.height
    var southWest = map.unproject([0, height], tileZoom)
    var northEast = map.unproject([width, 0], tileZoom)
    var bounds = new L.LatLngBounds(southWest, northEast)
    map.setMaxBounds(bounds)
    map.fitBounds(bounds)

    // markers
    data.points.forEach(function (point) {
        var latlnt = map.unproject([point.lat, point.lng], tileZoom)
        var marker = L.marker(latlnt, { title: point.tooltip }).addTo(map)
        if (point.content) {
            marker.on("click", function () {
                map.openModal({ content: point.content })
            });
        }
    })
}