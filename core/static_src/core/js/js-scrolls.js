// js-scrolls
// js helpers for the scrolls element

(function () {
  var scrolls = $('.js-scrolls');
  if (!scrolls) return;

  // set paddingLeft of scrolls by offsetLeft of .js-scrolls__offsetElement
  var offsetElement = $('.js-scrolls__offsetElement');
  function setJsScrollsOffset() {
    scrolls.css('padding-left', offsetElement.offset().left + "px" );
  }
  if (offsetElement) {
    $(window).on('resize', setJsScrollsOffset);
    setJsScrollsOffset();
  }

  // button next
  var buttonNext = $('.js-scrolls__button-next');
  if (buttonNext) {
    buttonNext.on('click', function (event) {
      event.preventDefault();
      scrolls.animate({
        scrollLeft: Math.floor(scrolls.scrollLeft() / 390)*390 + 390
      });
    });

    // hide button when farest right
    scrolls.on('scroll', function (event) {
      if (scrolls.scrollLeft() == scrolls[0].scrollWidth - $(document).width()) {
        buttonNext.hide();
      } else {
        buttonNext.show();
      }
    });
  }

  // button prev
  var buttonPrev = $('.js-scrolls__button-prev');
  if (buttonPrev) {

    // hide button unless scrolled right
    scrolls.on('scroll', function (event) {
      if (this.scrollLeft > 0) {
        buttonPrev.show()
      } else {
        buttonPrev.hide()
      }
    });

    // actually scroll
    buttonPrev.on('click', function (event) {
      event.preventDefault();
      scrolls.animate({scrollLeft: Math.ceil(scrolls.scrollLeft() / 390)*390 - 390});
    });
  }
})();
