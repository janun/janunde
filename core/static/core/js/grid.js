// activate isotope
// on .masonry containers
// for .panel items
var $grid = $('.masonry').isotope({
  itemSelector: '.panel',
  percentPosition: true,
});
// relayout after each image loads
$grid.imagesLoaded().progress( function() {
  $grid.isotope('layout');
});

// TODO
// activate isotope depending on screen-size
//.masonry-small

//.masonry-medium

//.masonry-large
