$(document).ready(function (){
    var search = $('.js-search');
    var noSearch = $('.js-no-search');
    var searchRevealButton = $('.js-search-reveal-button');
    var searchCloseButton = $('.js-search-close-button');
    var searchFocus = $('.js-search-focus');

    searchRevealButton.on('click', function (event) {
      event.preventDefault();
      search.removeClass('hide');
      noSearch.addClass('hide');
      searchFocus.focus();
    });

    searchCloseButton.on('click', function (event) {
      event.preventDefault();
      search.addClass('hide');
      noSearch.removeClass('hide');
    });
});
