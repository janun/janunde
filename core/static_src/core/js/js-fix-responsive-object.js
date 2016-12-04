// There is currenlty a bug in wagtail 1.7
// https://github.com/torchbox/wagtail/issues/1495
// that is fixed in the next wagtail version > 1.7

$(document).ready(function () {
  $('.responsive-object').each(function (i, elem) {
    if($(elem).css('padding-bottom') == "0px") {
      $(elem).removeClass('responsive-object');
    }
  })

});
