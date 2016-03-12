// activate isotope
// on .js-masonry containers
var $grid = $('.js-masonry').isotope({
  itemSelector: '.js-masonry__element, .js-masonry__element',
  percentPosition: true,
  transitionDuration: 0,
});
// relayout after each image loads
$grid.imagesLoaded().progress( function() {
  $grid.isotope('layout');
});

// TODO
// de/activate isotope depending on screen-size
// so we dont activate it in mobile where it is unneeded
