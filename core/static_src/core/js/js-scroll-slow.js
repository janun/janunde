// make certain links scroll slow
// those with the class js-scroll-slow
// add the value of data-scroll-slow-offset as an offset for the target
(function () {
  // gets the data and calls scrollSmooth
  function scrollSlow(event) {
    event.preventDefault();

    // get target pos
    var target = document.querySelector(this.hash);
    if (!target) return;
    var pos = target.offsetTop;

    // add offset
    if ( this.getAttribute('data-scroll-slow-offset') ) {
      pos += parseInt( this.getAttribute('data-scroll-slow-offset') );
    }

    // do the scrolling
    scrollSmooth(pos);
  }

  // add the event listeners to the elements
  var elements = document.querySelectorAll('.js-scroll-slow');
  for (i = 0; i < elements.length; ++i) {
    elements[i].addEventListener('click', scrollSlow);
  }
}());
