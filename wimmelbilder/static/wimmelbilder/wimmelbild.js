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

    // bounds
    var width = data.width
    var height = data.height
    var southWest = map.unproject([0, height], tileZoom)
    var northEast = map.unproject([width, 0], tileZoom)
    var bounds = new L.LatLngBounds(southWest, northEast)
    map.setMaxBounds(bounds)
    map.fitBounds(bounds)
    map.setMinZoom(map.getZoom())

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

}