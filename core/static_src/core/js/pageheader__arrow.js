$(document).ready(function () {

  function scroll(event) {
    event.preventDefault();
    $("html, body").animate({
      scrollTop: $(window).height() - 65
    });
  }

  $('.pageheader__arrow').each(function() {
    $(this).click(scroll);
  });

});
