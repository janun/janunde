$(document).ready(function () {
  var scroll = $('.header');
  var items = $('.js-onpagemenu .onpagemenu__item');

  if (!items.length) {
    return;
  }

  var pageOffset = $('.js-onpagemenu').data('offset') || 0;
  var menuOffset = items.eq(0).offset().left;

  var enableMenuScrolling = true;

  var targets = $.map(items, function (item) {
    pos = $($(item).attr('href')).offset().top;
    return {
      pos: pos, // position on the page
      item: item, // menu item
      menuPos: $(item).offset().left - menuOffset // position in the menu
    }
  });


  // smooth scrolling and
  // deactivate menu scrolling when clicked
  items.each(function () {
    $(this).click(function () {
      event.preventDefault();
      enableMenuScrolling = false;
      $.scrollTo($(this.hash), 300, {
        axis: 'y',
        onAfter: function () {
          enableMenuScrolling = true;
        }
      })
    })
  })


  // updates the scroll position of the menu
  function updateScrollPos() {
    if (!enableMenuScrolling) {
      return;
    }
    var pos = $(window).scrollTop();

    // get the target above the current page scroll pos
    var targetsAbovePos = $(targets).filter(function () {
      return this.pos < pos + pageOffset;
    });
    var targetAbove = (targetsAbovePos[ targetsAbovePos.length - 1 ] || targets[0]);

    // get the target below the current page scroll pos
    var targetsBelowPos = $(targets).filter(function () {
      return this.pos >= pos - pageOffset;
    });
    var targetBelow = (targetsBelowPos[0] || targets[targets.length - 1]);

    // get the percentage between the two
    if (targetBelow == targetAbove) {
      percentBetween = 0.0;
    } else {
      percentBetween = Math.abs(pos - targetAbove.pos)/(targetBelow.pos - targetAbove.pos);
    }

    menuPos = targetAbove.menuPos + percentBetween * (targetBelow.menuPos - targetAbove.menuPos);

    scroll.scrollTo(menuPos, 0, {
      axis: 'x',
      interrupt: true,
      margin: true
    })
  }


  // updates the active class in the menu
  function updateActiveItem() {
    var pos = $(window).scrollTop();

    // get the target above the current page scroll pos
    var targetsAbovePos = $(targets).filter(function () {
      return this.pos < pos + pageOffset;
    });
    var targetAbove = (targetsAbovePos[ targetsAbovePos.length - 1 ] || targets[0]);

    $(items).removeClass('active');
    $(targetAbove.item).addClass('active');
  }


  $(window).on('scroll', updateActiveItem);
  updateActiveItem();
  $(window).on('scroll', updateScrollPos);
  updateScrollPos();

});
