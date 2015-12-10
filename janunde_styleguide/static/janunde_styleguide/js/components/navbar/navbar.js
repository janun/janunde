// helpers for the navbar


// toggle Transparent
//
// removes the class 'transparent' if user scrolled further than disPos
// and adds it again after scrolling back
//
// elem    - the element to be affected
// disPos  - the position further which .transparent is removed from elem
function toggleTransparent(elem, disPos) {
  if ($(window).scrollTop() > disPos) {
    elem.removeClass('transparent');
  } else {
    elem.addClass('transparent');
  }
}

// use toggleTransparent
//
// gets elem and disPos by looking for the attribute 'data-toggle-transparent-at'
// uses toggleTransparent with every scroll event,
// but also on document ready, so deep links will work
$(document).ready(function() {
  var elem = $('[data-toggle-transparent-at]');
  var disPos = elem.attr('data-toggle-transparent-at')
  if (elem.hasClass('transparent')) {
    toggleTransparent(elem, disPos);
    $(window).scroll(function() {
      toggleTransparent(elem, disPos);
    });
  }
});


// when the dropdown menu is opened
// i.e. the event show.bs.dropdown is fired
// add .dropdown-open to body and .navbar-container
$('[data-toggle="dropdown"]').parent().on('show.bs.dropdown', function () {
  $('.navbar-container').addClass('dropdown-open');
  $('body').addClass('dropdown-open');
});

// when the dropdown menu is closed
// i.e. the event hide.bs.dropdown is fired
// remove .dropdown-open from body and .navbar-container
$('[data-toggle="dropdown"]').parent().on('hide.bs.dropdown', function () {
  $('.navbar-container').removeClass('dropdown-open');
  $('body').removeClass('dropdown-open');
});

// when the collapse menu is opened
// add .collapse-open to body and .navbar-container
$('[data-toggle="collapse"]').parent().on('show.bs.collapse', function () {
  $('.navbar-container').addClass('collapse-open');
  $('body').addClass('collapse-open');
});

// when the collapse menu is closed
// add .collapse-open to body and .navbar-container
$('[data-toggle="collapse"]').parent().on('hidden.bs.collapse', function () {
  $('.navbar-container').removeClass('collapse-open');
  $('body').removeClass('collapse-open');
});
