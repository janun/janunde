
$(document).ready(function () {
  $('.js-sticky').stick_in_parent()
    .on("sticky_kit:stick", function(e) {
      $(this).css('width', '')
    });
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
