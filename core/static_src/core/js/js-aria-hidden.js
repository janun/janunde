// js-aria-hidden
// This sets aria-hidden depending on mediaquery
// if the mediaquery matches aria-hidden is set to true
// if not its set to false
//
// @example markup
//   <div class="js-aria-hidden"
//        data-js-aria-hidden-media="(max-width: 1023px)"></div>
function jsAriaHidden(){
  var targets = document.querySelectorAll('.js-aria-hidden');

  for (i = 0; i < targets.length; ++i) {
    var target = targets[i];
    var media = target.getAttribute('data-js-aria-hidden-media');

    if (window.matchMedia(media).matches) {
      target.setAttribute('aria-hidden', true);
    } else {
      target.setAttribute('aria-hidden', false);
    }
  }
};

// register event handler
// TODO: throttle 200ms
window.addEventListener('resize', jsAriaHidden);
jsAriaHidden();
