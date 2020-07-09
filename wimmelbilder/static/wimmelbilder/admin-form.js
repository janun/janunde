function setUpLeafPad(input) {
    var tileZoom = 6;
    var width = document.querySelector("#id_width").value
    var height = document.querySelector("#id_height").value
    var tileUrl = document.querySelector("#id_tile_url").value

    var map = L.map("map", {
        minZoom: 1,
        maxZoom: L.Browser.retina ? 5 : 6,
        crs: L.CRS.Simple,
        attribution: false,
        fullscreenControl: true,
        zoomDelta: 1,
        zoomSnap: 0,
    })

    // tiles
    L.tileLayer(tileUrl, {
        tms: true,
        detectRetina: true,
        maxZoom: tileZoom
    }).addTo(map)

    var southWest = map.unproject([0, height], tileZoom)
    var northEast = map.unproject([width, 0], tileZoom)
    var bounds = new L.LatLngBounds(southWest, northEast)
    map.setMaxBounds(bounds)
    map.fitBounds(bounds)

    // marker
    var questionIcon = L.icon({
        iconUrl: "/static/wimmelbilder/question-icon.png",
        iconSize: [30, 30]
    });
    var loc = input.value ? input.value.split(",") : [width / 2, height / 2]
    var marker = L.marker(map.unproject(loc, tileZoom), {
        draggable: true, icon: questionIcon
    }).addTo(map);

    // apply and close
    document.querySelector("#apply-position").addEventListener("click", function () {
        var latlnt = map.project(marker.getLatLng(), tileZoom)
        input.value = parseInt(latlnt.x) + ", " + parseInt(latlnt.y)
        $('.modal').modal('hide')
    })
}


function openLatLngModal(input) {
    // inspired by https://github.com/wagtail/wagtail/blob/master/wagtail/admin/static_src/wagtailadmin/js/modal-workflow.js
    $('body > .modal').remove()
    var container = $('<div class="modal fade" tabindex="-1" role="dialog" aria-hidden="true">\n    <div class="modal-dialog">\n        <div class="modal-content">\n            <button type="button" class="button close icon text-replace icon-cross" data-dismiss="modal">' + wagtailConfig.STRINGS.CLOSE + '</button>\n            <div class="modal-body"></div>\n        </div><!-- /.modal-content -->\n    </div><!-- /.modal-dialog -->\n</div>');
    $('body').append(container)
    container.modal('hide')
    body = container.find('.modal-body')
    body.html('<header><div class="row nice-padding"><div class="left"><div class="col header-title"><h1>Punkt auswählen</h1></div></div></div></header><div class="nice-padding"><div class="map" style="width: 100%; height: 500px; margin-top: 20px; margin-bottom: 20px;" id="map"></div><div style="display: flex; justify-content: flex-end"><button id="apply-position" type="button" class="button">Übernehmen</button></div></div>')
    container.modal('show')
    setTimeout(function () { setUpLeafPad(input) }, 250);
}

function setUpWimmelbildEditHandler() {
    document.querySelectorAll(".latlng input").forEach(function (input) {
        var exists = input.parentNode.querySelectorAll("a.button")
        console.log(exists)
        if (exists.length) return

        var button = document.createElement("a")
        button.href = "#"
        button.textContent = "Auswählen"
        button.className = "button bicolor icon icon-edit"
        button.style.marginLeft = "20px"
        input.parentNode.appendChild(button)
        input.parentNode.style.display = "flex"
        input.parentNode.style.alignItems = "center"
        input.style.width = "auto"

        button.addEventListener("click", function (event) { event.preventDefault(); openLatLngModal(input) })
    })

    // re-run if add-button clicked
    document.querySelector('#id_points-ADD').addEventListener("click", setUpWimmelbildEditHandler)
}

document.addEventListener("DOMContentLoaded", setUpWimmelbildEditHandler)

