document.addEventListener("DOMContentLoaded", function () {
  // location bias for Hanover
  var api = "https://photon.komoot.de/api/?&lat=52.3892058&lon=9.7412133&lang=de&limit=5&q=";

  var nameField = document.querySelector("#id_location_name");
  var addressField = document.querySelector("#id_location_address");
  var postalcodeField = document.querySelector("#id_location_postcode");
  var cityField = document.querySelector("#id_location_city");
  var countryField = document.querySelector("#id_location_country");

  // create search field
  var fieldsUl = document.querySelector(".location-panel .fields");
  var searchMarkup = document.createElement("li");
  searchMarkup.innerHTML = "<div class=\"field iconfield\"><div><div class=\"input icon-search\"><input autocomplete=\"off\" autocorrect=\"off\" type=\"text\" placeholder=\"Such auf OpenStreetMap…\" id=\"location_search\"></div></div></div>";
  fieldsUl.insertAdjacentElement("afterbegin", searchMarkup);

  // create dropdown
  var searchField = document.querySelector("#location_search");
  searchField.parentElement.style.position = "relative";
  var dropdown = document.createElement("div");
  dropdown.className = "mydropdown";
  searchField.parentElement.appendChild(dropdown);

  // close dropdown on click outside
  document.addEventListener("click", function (event) {
    if (event.target === dropdown || event.target === searchField || dropdown.contains(event.target)) {
      return;
    }
    dropdown.classList.add("close");
    dropdown.classList.remove("open");
  });

  // select first result on ArrowDown
  searchField.addEventListener("keydown", function (event) {
    if (event.key === "ArrowDown" || event.key === "Down") {
      event.preventDefault();
      dropdown.querySelectorAll(".myitem")[0].focus();
    }
  });

  // cycle results and inputs on ArrowDown / ArrowUp
  dropdown.addEventListener("keydown", function (event) {
    if (event.key === "ArrowDown" || event.key === "Down") {
      event.preventDefault();
      var nextSibling = document.activeElement.nextElementSibling;
      if (nextSibling) nextSibling.focus();
    }
  });
  dropdown.addEventListener("keydown", function (event) {
    if (event.key === "ArrowUp" || event.key === "Up") {
      event.preventDefault();
      var prevSibling = document.activeElement.previousElementSibling;
      if (prevSibling) prevSibling.focus();
      else searchField.focus();
    }
  });

  function formatResult(props) {
    return [
      props.name,
      props.street || props.housenumber ? (props.street || "") + " " + (props.housenumber || "") : null,
      props.postcode || props.city ? (props.postcode || "") + " " + (props.city || "") : null,
      props.country
    ].filter(Boolean).join(", ");
  }

  // response
  function handleResponse() {
    var data = JSON.parse(this.responseText);
    var results = data.features;
    dropdown.innerHTML = "";
    dropdown.classList.add("open");

    if (results.length === 0) {
      var item = document.createElement("div");
      item.className = "myitem";
      item.innerHTML = "Keine Suchergebnisse auf OpenStreetMap. Versuch es mit einem kürzeren Suchbegriff.";
      dropdown.appendChild(item);
    }

    results.forEach(function (result) {
      var item = document.createElement("button");
      item.setAttribute("type", "button");
      var props = result.properties;
      item.className = "myitem";
      item.innerHTML = formatResult(props);
      dropdown.appendChild(item);

      // on item click
      item.addEventListener("click", function () {
        nameField.value = props.name || "";
        addressField.value = (props.street || "") + " " + (props.housenumber || "");
        postalcodeField.value = props.postcode || "";
        cityField.value = props.city || "";
        countryField.value = props.country || "";
        dropdown.classList.add("close");
        dropdown.classList.remove("open");
      });
    });
  }

  function handlError() {
    dropdown.innerHTML = "<div class=\"myitem\">Sorry, beim Suchen ist ein Fehler aufgetreten.</div>";
  }

  // do the search
  var xhr = null;
  function search() {
    var url = api + searchField.value;
    if (xhr) xhr.abort();
    dropdown.innerHTML = "<div class=\"loading-mask loading myitem\">Suche …</div>";
    xhr = new XMLHttpRequest();
    xhr.addEventListener("load", handleResponse);
    xhr.addEventListener("error", handlError);
    xhr.open("GET", url);
    xhr.send();
  }

  // open dropdown on search focus
  searchField.addEventListener("focus", function () {
    dropdown.classList.add("open");
  });

  // on search input
  var debounceTimeout = null;
  searchField.addEventListener("input", function () {
    if (searchField.value.length === 0) dropdown.innerHTML = "";
    if (searchField.value.length < 3) return;

    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(search, 250);
  });
});
