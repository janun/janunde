// animate in when half visible
// using the animation class in the data-animation attribute
document.querySelectorAll(".js-animate-in").forEach(function (elem) {
  elem.classList.add("md:opacity-0")

  var observer = new IntersectionObserver(function (entries) {
    if (entries[0].isIntersecting === true) {
      var klass = elem.getAttribute('data-animation')
      elem.classList.add("md:animated")
      elem.classList.add(klass)
      elem.classList.remove("md:opacity-0")
    }
  })
  observer.observe(elem)
});