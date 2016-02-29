// activate isotope
// on .masonry containers
// for .panel items
var $grid = $('.masonry').isotope({
  itemSelector: '.masonry>article, .masonry>div',
  percentPosition: true,
  transitionDuration: 0,
});
// relayout after each image loads
$grid.imagesLoaded().progress( function() {
  $grid.isotope('layout');
});

// TODO
// de/activate isotope depending on screen-size
//.masonry-small

//.masonry-medium

//.masonry-large
