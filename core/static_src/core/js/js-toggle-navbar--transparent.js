// js-toggle-navbar--transparent
function jsToggleNavbarTransparentOnScroll(){
  var target = document.querySelector('.js-toggle-navbar--transparent');
  if(!target) { return 1; }

  var changeOnPosition = 480 - 65;
  var currentPos = document.body.scrollTop || document.documentElement.scrollTop;

  if (currentPos >= changeOnPosition) {
    target.classList.remove('navbar--transparent');
  } else {
    target.classList.add('navbar--transparent');
  }

};

// register event handler
// TODO: throttle 200ms
window.addEventListener('scroll', jsToggleNavbarTransparentOnScroll);
