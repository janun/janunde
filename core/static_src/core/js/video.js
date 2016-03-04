// video source media query "polyfill"
// copies data-src to src if no media attribute or media matches
document.addEventListener('DOMContentLoaded', function () {
  var sources = document.querySelectorAll('video source[data-src]');

  for (var i = 0, length=sources.length; i < length; ++i) {
    var source = sources[i];
    var media = source.getAttribute('media');

    if (!media || window.matchMedia(media).matches) {
      source.setAttribute('src', source.getAttribute('data-src'));
      source.parentNode.load();
    }
  }
});
