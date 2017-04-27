$(document).ready(function () {
  $(".image-gallery").each(function (index, gallery) {
    var activeImage = $(gallery).find(".image-gallery__active-image");
    var activeImageLink = $(gallery).find(".image-gallery__active-image-link");
    var activeAttribution = $(gallery).find(".image-gallery__attribution");
    var links = $(gallery).find(".image-gallery__image-list a");

    links.each(function (index, link) {
      $(link).click(function (event) {
        event.preventDefault();
        var image = $(link).find("img");
        var attribution = $(image).attr('data-attribution');
        $(activeImage).attr('src', $(image).attr('data-src'));
        $(activeAttribution).html(attribution);
        $(activeImageLink).attr('href', $(image).attr('data-huge-src'));
      });
    });

  });
});
