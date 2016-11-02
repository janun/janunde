$(document).ready(function () {

  function scroll(event) {
    event.preventDefault();
    $("html, body").animate({
      scrollTop: $(window).height() - 60
    });
  }

  $('.js-scroll-window-height').each(function() {
    $(this).click(scroll);
  });

});
