$(document).ready(function() {
  var betabanner = $('.betabanner');
  var close = $('.betabanner__close');

  close.click(function (e){
    e.preventDefault();
    betabanner.slideUp();
    var d = new Date();
    d.setTime(d.getTime() + 5*60*1000); // 5 minutes
    document.cookie = 'hide-betabanner=1;path=/;expires='+d.toGMTString()+';';
    return false;
  });
})
