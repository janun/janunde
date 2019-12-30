document.querySelectorAll(".js-zoom-image").forEach(function (elem) {
  var src = elem.getAttribute("href");

  // black background
  var container = document.createElement("div");
  container.className = "hidden transition-opacity opacity-0 fixed inset-0 bg-black-90 p-2 sm:p-10 flex justify-center items-center w-screen h-screen z-50";
  document.body.insertAdjacentElement("beforeend", container);

  // close button
  var closeButton = document.createElement("button");
  closeButton.className = "absolute top-0 right-0 m-2 sm:m-6 p-2 outline-none focus:shadow-outline rounded-full text-white hover:text-gray-300";
  closeButton.setAttribute("type", "button");
  closeButton.setAttribute("title", "Schließen");
  closeButton.innerHTML = "<svg class=\"fill-current h-5 w-5 sm:h-6 sm:w-6\" viewBox=\"0 0 20 20\"><path d=\"M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z\"/></svg>";
  container.insertAdjacentElement("afterbegin", closeButton);

  // image
  var img = document.createElement("img");
  img.setAttribute("src", src);
  container.insertAdjacentElement("beforeend", img);
  img.className = "max-h-full max-w-full rounded-lg";

  var hash = "#zoom-image";

  function open() {
    container.classList.remove("hidden");
    setTimeout(function () {
      container.classList.remove("opacity-0");
      container.classList.add("opacity-100");
    }, 20);
    window.location.hash = hash;
    document.body.classList.add("overflow-y-hidden");
  }

  function close(noback) {
    container.classList.add("opacity-0");
    container.classList.remove("opacity-100");
    container.addEventListener("transitionend", function () {
      container.classList.add("hidden");
    }, { once: true });
    if (!noback) history.back();
    document.body.classList.remove("overflow-y-hidden");
  }

  // close on back
  window.addEventListener("hashchange", function () {
    if (!container.classList.contains("hidden") && window.location.hash !== hash) {
      event.preventDefault();
      close(true);
    }
  });


  // open on click
  elem.addEventListener("click", function (event) {
    event.preventDefault();
    open();
  });

  // close on closeButton
  closeButton.addEventListener("click", close);

  // close on click on background
  container.addEventListener("click", function (event) {
    if (event.target !== img) {
      event.preventDefault();
      close();
    }
  });

  // close on Escape
  document.addEventListener("keydown", function (event) {
    if ((event.key === "Escape" || event.key === "Esc") && !container.classList.contains("hidden")) {
      event.preventDefault();
      close();
    }
  });
});