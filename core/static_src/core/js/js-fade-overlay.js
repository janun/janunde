// js-fade-overlay
function jsFadeOverlay() {
  var target = document.querySelector('.js-fade-overlay__inner');
  var endPos = 480 - 65;
  var currrentPos = document.body.scrollTop || document.documentElement.scrollTop;
  var alpha = 0.0;

  if (currrentPos > endPos) {
    alpha = 1.0;
  } else {
    alpha = Math.sqrt(1 - (endPos - currrentPos) / endPos, 2);
  }

  target.style.backgroundColor = 'rgba(70, 187, 0, '+ alpha +')';
};


// register event handler
window.addEventListener('scroll', jsFadeOverlay);
