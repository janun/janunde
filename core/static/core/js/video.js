/**
 * enable disabled html5 videos on devices greater 64em
 *
 * on devices with a screen width greater than 64em
 * affects all source elements inside video elements
 * that have a data-src attribute.
 * sets src to the value of data-src and uses 'load()' on the video element.
 */
document.addEventListener('DOMContentLoaded', function () {
  if (window.matchMedia("(min-width: 64em)").matches) {
    var sources = document.querySelectorAll('video source[data-src]');
    for (var i = 0, length=sources.length; i < length; ++i) {
      sources[i].setAttribute('src', sources[i].getAttribute('data-src'));
      sources[i].parentNode.load();
    }
  }
});
