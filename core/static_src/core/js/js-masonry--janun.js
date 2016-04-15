// activate isotope
// on .js-masonry--janun containers on .js-masonry__element elements
//
// .js-masonry seems already be used by masonry itself thats why the --janun
//
// if an attribute of data-js-masonry-media is specified,
// masonry is only applied if that media query matches
//
// @example markup:
//   <div class="js-masonry--janun" data-js-masonry-media="(min-width: 40rem)">
//     <div class="js-masonry__element"></div>
//     <div class="js-masonry__element"></div>
//   </div>
(function () {
  // TODO: use browserify or sth. to keep track of dependencies?
  //var Isotope = require('isotope-layout');
  //var imagesLoaded = require('imagesLoaded');

  // get all relevant container elements
  var elements = document.querySelectorAll('.js-masonry--janun');
  for (i = 0; i < elements.length; ++i) {
    var element = elements[i];
    var media = element.getAttribute('data-js-masonry-media');

    if (!media || window.matchMedia(media).matches) {
      // activate isotope
      var iso = new Isotope(element, {
        itemSelector: '.js-masonry__element',
        //percentPosition: true,
        transitionDuration: 0,
      });

      // relayout after image loading is complete
      imagesLoaded(element, function() {
        iso.layout();
      });
    }
  }
}());
