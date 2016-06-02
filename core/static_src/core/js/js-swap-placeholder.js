$(document).ready(function () {
  function swapPlaceholder (elem) {
    if (window.matchMedia('(max-width: 768px)').matches) {
      elem.attr('data-placeholder-small', elem.attr('placeholder'));
      elem.attr('placeholder', elem.attr('data-placeholder-small'));
    } else {

    }

  }

  $('.js-swap-placeholder').each(function () {
    swapPlaceholder()
  })
});
