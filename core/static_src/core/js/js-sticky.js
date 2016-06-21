
$(document).ready(function () {
  $('.js-sticky').stick_in_parent();
})


$(document).ready(function () {
  function updateSticky(sticky) {
    if (window.matchMedia('(min-width: 768px)').matches) {
      sticky.stick_in_parent();
    } else {
      sticky.trigger("sticky_kit:detach");
    }
  }

  $('.js-sticky\\@medium').each(function () {
    $(window).resize(function () {
      updateSticky($(this));
    });
    updateSticky($(this));
  })
})


$(document).ready(function () {
  function updateSticky(sticky) {
    //var spacerElem = sticky.closest('.js-sticky__spacer');
    if (window.matchMedia('(max-width: 767px)').matches) {
      sticky.stick_in_parent({
        sticky_class: "is_stuck@until-medium",
        spacer: false,//spacerElem.length ? spacerElem : null,
      });
    } else {
      sticky.trigger("sticky_kit:detach");
    }
  }

  $('.js-sticky\\@until-medium').each(function () {
    $(window).resize(function () {
      updateSticky($(this));
    });
    updateSticky($(this));
  });
})
