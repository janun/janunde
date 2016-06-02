// strangely needs this in css:
// .sticky-wrapper {
//   float: left;
// }
$(document).ready(function () {
  function makeSticky(elem) {
    elem.sticky({
      topSpacing: 0,
      center: true,
    });
  }

  $(".js-sticky").each(function () {
    makeSticky($(this));
  });

  function untilMedium(elem) {
    if (window.matchMedia('(max-width: 768px)').matches) {
      makeSticky(elem);
    } else {
      // TODO: remove sticky
    }
  }
  $(".js-sticky-until-medium").each(function () {
    var elem = $(this);
    // if we resize we loose focus when focussing the search...
    // $(window).resize( function () {
    //   untilMedium(elem);
    // });
    untilMedium(elem);
  });


});
