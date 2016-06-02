$(document).ready(function () {

  function swapPlaceholder (elem) {
    if (window.matchMedia('(max-width: 768px)').matches) {
      elem.attr('placeholder', elem.attr('data-placeholder-small'));
    } else {
      elem.attr('placeholder', elem.attr('data-placeholder-medium'));
    }
  }

  $('.js-swap-placeholder').each(function () {
    var elem = $(this);
    // default for data-placeholder-medium
    if (!elem.attr('data-placeholder-medium')) {
      elem.attr('data-placeholder-medium', elem.attr('placeholder'));
    }

    $(window).resize(function() {
       swapPlaceholder(elem);
    });
    swapPlaceholder(elem);
  })

});
