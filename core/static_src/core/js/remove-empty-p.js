// the halo.js editor likes to create blank p tags...
// but margin-bottom of p tags breaks layout.
$(document).ready(function () {
  $('p').each(function() {
      var $this = $(this);
      if($this.html().replace(/\s|&nbsp;/g, '').length == 0)
          $this.remove();
  });
});
