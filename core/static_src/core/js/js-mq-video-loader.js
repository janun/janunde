// Media Query video loader
//
// @example markup
//   <video class="js-mq-video-loader">
//     <source data-src="..." media="(min-device-width: 1280px)">
//   </video>
//
document.addEventListener('DOMContentLoaded', function () {
  var sources = document.querySelectorAll(
    '.js-mq-video-loader source[data-src]'
  );

  for (var i = 0, length=sources.length; i < length; ++i) {
    var source = sources[i];
    var media = source.getAttribute('media');

    if (!media || window.matchMedia(media).matches) {
      source.setAttribute('src', source.getAttribute('data-src'));
      source.parentNode.load();
    }
  }
});


// $('.js-mq-video-loader').each(function () {
//   var video = this;
//   $(document).click(function () {
//     video.play();
//   })
//   $(window).scroll(function () {
//     video.play();
//   })
// })
