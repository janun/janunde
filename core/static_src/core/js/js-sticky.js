
$(document).ready(function () {
  $('.js-sticky').stick_in_parent()
    .on("sticky_kit:stick", function(e) {
      $(this).css('width', '')
    });
})


$(document).ready(function () {
  $('.js-sticky\\@until-medium').stick_in_parent({
    sticky_class: "is_stuck@until-medium",
    spacer: false,
  });
})
