// js-scrolls
// js helpers for the scrolls element

(function () {
  var scrolls = document.querySelector('.js-scrolls');
  if (!scrolls) return;

  // offset
  var offsetElement = document.querySelector('.js-scrolls__offsetElement');
  function setJsScrollsOffset() {
    scrolls.style.paddingLeft = offsetElement.offsetLeft + "px";
  }
  if (offsetElement) {
    window.addEventListener('resize', setJsScrollsOffset);
    setJsScrollsOffset();
  }

  // button next
  var buttonNext = document.querySelector('.js-scrolls__button-next');
  if (buttonNext) {
    buttonNext.addEventListener('click', function (event) {
      event.preventDefault();
      scrollSmooth(380, 'right', 200, false, scrolls);
    });
  }
})();
