$(document).ready(function () {
  var betabanner = $('.betabanner');
  var close = $('.betabanner__close');

  close.click(function (e){
    e.preventDefault();
    betabanner.slideUp();
  });
});
