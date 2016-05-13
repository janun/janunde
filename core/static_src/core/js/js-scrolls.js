
function setJsScrollsOffset() {
  var offsetElement = document.querySelector('.js-scrolls__offsetElement');
  var scrolls = document.querySelector('.js-scrolls');
  if (offsetElement) {
    var offset = offsetElement.offsetLeft;
    scrolls.style.paddingLeft = offset + "px";
  }
}

window.addEventListener('resize', setJsScrollsOffset);
setJsScrollsOffset();
