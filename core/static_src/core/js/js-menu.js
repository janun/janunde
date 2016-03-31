// This sets aria-hidden=true
function jsAriaHidden(){
  var target = document.querySelector('.js-aria-hidden');
  var media = target.getAttribute('data-js-aria-hidden-media');

  if (window.matchMedia(media).matches) {
    target.setAttribute('aria-hidden', true);
  } else {
    target.setAttribute('aria-hidden', false);
  }
};

// register event handlers
window.addEventListener('resize', jsAriaHidden);
jsAriaHidden();
