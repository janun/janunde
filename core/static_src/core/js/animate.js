// helper function to do a simple linear animation using requestAnimationFrame

// animate
// calls callback using
// @arg callback    - the callback, which should take only one value
// @arg startValue  - the starting value
// @arg endValue    - the ending value
// @arg duration    - the duration in ms
function animate(callback, startValue, endValue, duration) {
  var distance = endValue - startValue;
  var speed = distance / duration;
  var time;
  var value = startValue;

  function doAnimate(now) {
    var dt = now - time || 0;
    time = now;
    value += speed * dt;
    if (value < endValue) {
      callback(value);
      requestAnimationFrame(doAnimate);
    } else {
      callback(endValue);
      return;
    }
  }

  requestAnimationFrame(doAnimate);
}
