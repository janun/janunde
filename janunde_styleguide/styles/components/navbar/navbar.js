// dropdown open
$('[data-toggle="dropdown"]').parent().on('show.bs.dropdown', function () {
  var $navbar = $(this).parents('.navbar');
  var $navbarContainer = $(this).parents('.navbar-container');
  if (!$navbarContainer) return;

  $navbarContainer.addClass('dropdown-open');
  $('body').addClass('dropdown-open');
});

// dropdown close
$('[data-toggle="dropdown"]').parent().on('hide.bs.dropdown', function () {
  var $navbar = $(this).parents('.navbar');
  var $navbarContainer = $(this).parents('.navbar-container');
  if (!$navbarContainer) return;

  $navbarContainer.removeClass('dropdown-open');
  $('body').removeClass('dropdown-open');
});

// collapse settings
$('[data-toggle="collapse"]').parent().on('show.bs.collapse', function () {
  var $navbar = $(this).parents('.navbar');
  var $navbarContainer = $(this).parents('.navbar-container');
  if (!$navbarContainer) return;

  $navbarContainer.addClass('collapse-open');
  $('body').addClass('collapse-open');
});

// collapse settings
$('[data-toggle="collapse"]').parent().on('hidden.bs.collapse', function () {
  var $navbar = $(this).parents('.navbar');
  var $navbarContainer = $(this).parents('.navbar-container');
  if (!$navbarContainer) return;

  $navbarContainer.removeClass('collapse-open');
  $('body').removeClass('collapse-open');
});
