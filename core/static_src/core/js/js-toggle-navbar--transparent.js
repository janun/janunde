// js-toggle-navbar--transparent
function jsToggleNavbarTransparent(){
  var target = document.querySelector('.js-toggle-navbar--transparent');
  var changeOnPosition = 480 - 65;
  var currentPos = document.body.scrollTop || document.documentElement.scrollTop;

  if (currentPos >= changeOnPosition) {
    target.classList.remove('navbar--transparent');
  } else {
    target.classList.add('navbar--transparent');
  }

};

// register event handler
window.addEventListener('scroll', jsToggleNavbarTransparent);
