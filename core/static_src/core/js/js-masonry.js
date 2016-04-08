// activate isotope
// on .js-masonry containers
(function () {
  // TODO: use browserify or sth. to keep track of dependencies?
  //var Isotope = require('isotope-layout');
  //var imagesLoaded = require('imagesLoaded');

  // get all relevant container elements
  var elements = document.querySelectorAll('.js-masonry-dis');
  for (i = 0; i < elements.length; ++i) {
    var element = elements[i];
    var media = element.getAttribute('data-js-masonry-media');

    if (!media || window.matchMedia(media).matches) {
      // activate isotope
      var iso = new Isotope(element, {
        itemSelector: '.js-masonry__element',
        percentPosition: true,
        transitionDuration: 0,
      });

      // relayout after image loading is complete
      imagesLoaded(element, function() {
        iso.layout();
      });
    }
  }
}());
