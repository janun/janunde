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
    var tileLayer = L.tileLayer(data.tileUrl, {
        tms: true,
        detectRetina: true,
        maxZoom: tileZoom
    }).addTo(map)

    // workaround for white borders around tiles
    // https://github.com/Leaflet/Leaflet/issues/3575
    function fixTileBorder() {
        document.querySelectorAll(".leaflet-tile").forEach(function (tile) {
            if (tile.style.height.replace('px', '') % 1 === 0) {
                tile.style.height = (tile.clientHeight + 0.5) + 'px'
                tile.style.width = (tile.clientWidth + 0.5) + 'px'
            }
        })
    }
    map.on('load zoomend drag', fixTileBorder)
    tileLayer.on('load', fixTileBorder)

    // bounds
    var width = data.width
    var height = data.height
    var southWest = map.unproject([0, height], tileZoom)
    var northEast = map.unproject([width, 0], tileZoom)
    var bounds = new L.LatLngBounds(southWest, northEast)
    map.setMaxBounds(bounds)
    map.fitBounds(bounds)
    map.setMinZoom(map.getZoom())

    // workaround for too tight maxbounds on fullscreen
    map.on('enterFullscreen', function () {
        map.setMaxBounds(null)
    })
    map.on('exitFullscreen', function () {
        map.setMaxBounds(bounds)
    })


    // default icon
    var questionIconUrl = "/static/wimmelbilder/question-icon.png"
    var questionIcon = L.icon({
        iconUrl: questionIconUrl,
        iconSize: [30, 30]
    });

    // markers
    var layers = {}
    data.groups.forEach(function (group) {
        var groupMarkers = []
        group.points.forEach(function (point) {
            var latlnt = map.unproject(point.latlng.split(","), tileZoom)
            var marker = L.marker(latlnt, { title: point.tooltip, icon: questionIcon }).addTo(map)
            if (group.icon) {
                marker.setIcon(L.icon({
                    iconUrl: group.icon.url,
                    iconSize: [group.icon.width, group.icon.height]
                }))
            }
            if (point.content) {
                marker.on("click", function () {
                    map.openModal({ content: point.content })
                });
            }
            groupMarkers.push(marker)
        })

        // display for layer control
        var iconURl = group.icon ? group.icon.url : questionIconUrl
        var layerDisplay = `<div style="display:inline-flex; align-items: center"><img style="margin-right: 5px; height: 20px" src="${iconURl}"> ${group.name}</div>`
        layers[layerDisplay] = L.layerGroup(groupMarkers).addTo(map)
    })

    // layer control to toggle marker groups
    L.control.layers({}, layers, { collapsed: false }).addTo(map);


    // handler for internal links
    var mapContainer = document.querySelector('#' + mapContainerId)
    mapContainer.addEventListener("click", function (event) {
        if (!event.target.hash) return
        var hash = decodeURIComponent(event.target.hash.replace(/#/, ''))
        var marker = mapContainer.querySelector(`[title="${hash}"]`)
        if (!marker) return
        map.closeModal()
        marker.click()
    })
}