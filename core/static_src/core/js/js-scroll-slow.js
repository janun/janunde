// make certain links scroll slow
// those with the class js-scroll-slow
// add the value of data-scroll-slow-offset as an offset for the target
$(document).ready(function () {

  function scroll(event) {
    event.preventDefault();
    var targetElem = $(this.hash);
    if (!targetElem) return;

    var targetPos = targetElem.offset().top;

    if ( this.getAttribute('data-scroll-slow-offset') ) {
      targetPos += parseInt( this.getAttribute('data-scroll-slow-offset') );
    }

    $('body').animate({scrollTop: targetPos});
  }

  $('.js-scroll-slow').each(function() {
    $(this).click(scroll);
  });

});
