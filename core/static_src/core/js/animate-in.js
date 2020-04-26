// animate in when half visible
// using the animation class in the data-animation attribute
document.querySelectorAll(".js-animate-in").forEach(function (elem) {
  elem.classList.add("opacity-0")

  var observer = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting === true) {
      var klass = elem.getAttribute('data-animation')
      elem.classList.add("animated")
      elem.classList.add(klass)
      elem.classList.remove("opacity-0")
    }
  }, { threshold: [0.5] })
  observer.observe(elem)
});