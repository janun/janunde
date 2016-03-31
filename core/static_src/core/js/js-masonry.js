// activate isotope
// on .js-masonry containers
(function () {
  // TODO: use browserify or sth. to keep track of dependencies
  //var Isotope = require('isotope-layout');
  //var imagesLoaded = require('imagesLoaded');

  // get all relevant elements
  var elements = document.querySelectorAll('.js-masonry');
  for (i = 0; i < elements.length; ++i) {
    var element = elements[i];

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
}());
