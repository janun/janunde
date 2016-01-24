if (window.matchMedia("(min-width: 40em)").matches) {
  $('video source').each(function () {
    $(this).attr('src', $(this).attr('data-src'));
  });
  $('video').load();
}
