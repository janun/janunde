// make certain links scroll slow
// those with the class js-scroll-slow
// add the value of data-scroll-slow-offset as an offset for the target
(function () {

  // perform the actual scroll animation
  function animateScrollTo(yPos, startTime, duration) {
    duration = duration || 400;
    var targetTime = startTime + duration;

    function animate() {
      var nowTime = new Date().getTime();
      var multiplier = 1 - (targetTime - nowTime) / duration;

      if (nowTime >= targetTime ) {
        document.documentElement.scrollTop = document.body.scrollTop = yPos;
        return;
      } else {
        document.documentElement.scrollTop = document.body.scrollTop = yPos * multiplier;
        requestAnimationFrame(animate);
      }
    }

    requestAnimationFrame(animate);
  }

  // gets the data and calls scrollTo
  function scrollSlow(event) {
    event.preventDefault();
    var target = document.querySelector(this.hash);

    // get offset
    var offset = 0;
    if ( this.getAttribute('data-scroll-slow-offset') ) {
      offset += parseInt( this.getAttribute('data-scroll-slow-offset') );
    }

    animateScrollTo( (target.offsetTop + offset), (new Date().getTime()) )
  }

  // add the event listeners to the elements
  var elements = document.querySelectorAll('.js-scroll-slow');
  for (i = 0; i < elements.length; ++i) {
    elements[i].addEventListener('click', scrollSlow);
  }
}());
