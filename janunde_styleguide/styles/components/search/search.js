$(".search.animate .search-button").click(function( event ) {
  var $form = $(this).parent();
  var $searchField = $(this).siblings('input[type=search]');

  event.preventDefault();

  $searchField.focus();
})
