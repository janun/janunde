// js-scrolls
// js helpers for the scrolls element

$(document).ready(function () {
  var scrolls = $('.js-scroll-horizontal');
  if (!scrolls.length) return;

  // set paddingLeft of scrolls by offsetLeft of .js-scrolls__offsetElement
  function setJsScrollsOffset() {
    if (window.matchMedia('(min-width: 768px)').matches) {
      scrolls.css('padding-left', offsetElement.offset().left + "px" );
    } else {
      scrolls.css('padding-left', "" );
    }
  }
  var offsetElement = $('.js-scroll-horizontal__offsetElement');
  if (offsetElement.length) {
    $(window).on('resize', setJsScrollsOffset);
    $(window).on('scroll', setJsScrollsOffset);
    setJsScrollsOffset();
  }


  // arrow right
  var buttonNext = $('.js-scroll-horizontal__right');
  if (buttonNext) {
    buttonNext.on('click', function (event) {
      event.preventDefault();
      scrolls.animate({
        scrollLeft: Math.floor(scrolls.scrollLeft() / 400)*400 + 400
      }, 200);
    });

    // hide button when farest right
    scrolls.on('scroll', function (event) {
      if (scrolls.scrollLeft() >= scrolls[0].scrollWidth - $(document).width()) {
        buttonNext.hide();
      } else {
        buttonNext.show();
      }
    });

    // flash button hover state after page load
    window.setTimeout(function () {
      $('.horizontal-scroll__arrow--right').addClass('hover');
      window.setTimeout(function () {
        $('.horizontal-scroll__arrow--right').removeClass('hover');
      }, 250);
    }, 250);
  }

  // arrow left
  var buttonPrev = $('.js-scroll-horizontal__left');
  if (buttonPrev) {
    // hide button unless scrolled right
    scrolls.on('scroll', function (event) {
      if (this.scrollLeft > 0) {
        buttonPrev.show()
        $(document.body).trigger("sticky_kit:recalc");
      } else {
        buttonPrev.hide()
      }
    });

    // actually scroll
    buttonPrev.on('click', function (event) {
      event.preventDefault();
      scrolls.animate({
        scrollLeft: Math.ceil(scrolls.scrollLeft() / 400)*400 - 400
      }, 200);
    });
  }

});
