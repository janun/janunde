
$(document).ready(function () {
  $('.js-sticky').stick_in_parent();
})


$(document).ready(function () {
  var sticky = $('.js-sticky\\@medium');

  function updateSticky() {
    if (window.matchMedia('(min-width: 768px)').matches) {
      sticky.stick_in_parent();
    } else {
      sticky.trigger("sticky_kit:detach");
    }
  }

  if (sticky.length) {
    $(window).resize(updateSticky);
    updateSticky();
  }
})


$(document).ready(function () {
  var sticky = $('.js-sticky\\@until-medium');

  function updateSticky() {
    if (window.matchMedia('(max-width: 767px)').matches) {
      sticky.stick_in_parent({
        sticky_class: "is_stuck@until-medium",
      });
    } else {
      sticky.trigger("sticky_kit:detach");
    }
  }

  if (sticky.length) {
    $(window).resize(updateSticky);
    updateSticky();
  }
})
