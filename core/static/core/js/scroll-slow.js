// make certain links scroll slow
// those with the attribute data-scroll-slow
// add the value of data-scroll-slow-offset as an offset for the target
$('a[data-scroll-slow]').on('click', function(e) {
  e.preventDefault();
  var target = this.hash;
  var $target = $(target);

  var offset = 0;
  if ( this.getAttribute('data-scroll-slow-offset') ) {
    offset =+ parseInt( this.getAttribute('data-scroll-slow-offset') );
  }

  $('html, body').stop().animate(
  {
    'scrollTop': $target.offset().top + offset,
  },
  900, 'swing', function () {
    window.location.hash = target;
  });
});
