// scrollSmooth
// Yet another smooth scrolling js lib

//function scrollSmoothToAnchor(where) {}

// scrollSmooth
//
// @arg pos        - absolute or relative position
// @arg direction  - right or down
//                   default: down
// @arg duration   - the duration in ms the scroll should take
//                   default: 500
// @arg isAbsolute - wether pos is absolute or relative
//                   default: true meaning absolute
// @arg element    - the element that should be scrolled
//                   default: the body element
function scrollSmooth(pos, direction, duration, isAbsolute, element) {
  direction = direction || 'down';
  duration = duration || 500;

  // construct relative coord from absolute
  if (isAbsolute == false) {
    pos = getScrollPos() + pos;
  }

  function getScrollPos() {
    if (element) {
      if (direction == 'down') {
        return element.scrollTop;
      } else {
        return element.scrollLeft;
      }
    } else {
      if (direction == 'down') {
        return document.documentElement.scrollTop;
        return document.body.scrollTop;
      } else {
        return document.documentElement.scrollLeft;
        return document.body.scrollLeft;
      }
    }
  }

  function setScrollPos(pos) {
    if (element) {
      if (direction == 'down') {
        element.scrollTop = pos;
      } else {
        element.scrollLeft = pos;
      }
    } else {
      if (direction == 'down') {
        document.documentElement.scrollTop = pos;
        document.body.scrollTop = pos;
      } else {
        document.documentElement.scrollLeft = pos;
        document.body.scrollLeft = pos;
      }
    }
  }

  animate(setScrollPos, getScrollPos(), pos, duration);
}
