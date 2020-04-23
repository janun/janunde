// fade in when half visible
document.querySelectorAll(".js-fade-in").forEach(function (elem) {
  elem.classList.add("opacity-0");

  var observer = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting === true) {
      elem.classList.add("fade-in");
      elem.classList.remove("opacity-0");
    }
  }, { threshold: [0.5] });
  observer.observe(elem);
});