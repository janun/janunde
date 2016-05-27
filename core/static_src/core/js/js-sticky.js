// needs this in css:
// .sticky-wrapper {
//   float: left;
// }
$(".js-sticky").each(function () {
  $(this).sticky({
    'widthFromWrapper': false,
    'topSpacing': 20,
  });
});
