// show hints for inputs with maxlength
$(".form input[maxlength]").on('input', function() {
  if ($(this).siblings(".form__helptext").length == 0) {
    $("<p class=\"form__helptext\"></p>").insertAfter(this);
  }
  if ($(this).siblings(".form__helptext").find(".length").length === 0) {
    $(this).siblings(".form__helptext").prepend("<span class=\"length\"></span>");
  }
  $(this).siblings(".form__helptext").find(".length").html(
    $(this).val().length + "/" + $(this).attr("maxlength")
  );
});


$(".dateinput").each(function (i, elem) {
  var input = $(elem).find('input');
  var isDesktop = window.matchMedia("(min-device-width: 800px)").matches;

  var picker = input.pickadate({
    format: "dd.mm.yyyy",
    formatSubmit: "dd.mm.yyyy",
    editable: isDesktop,
    hiddenName: true,
    clear: input.attr('required') ? "" : "Löschen",
  }).pickadate('picker');

  $(elem).find('.dateinput__open').click(function (e) {
    e.stopPropagation()
    e.preventDefault();
    if (picker.get('open')) {
      picker.close();
    } else {
    picker.set('select', input.val());
      picker.open();
    }
  });
});


$(".timeinput").each(function (i, elem) {
  var input = $(elem).find('input');
  var isDesktop = window.matchMedia("(min-device-width: 800px)").matches;

  var picker = input.pickatime({
    format: "H:i",
    formatSubmit: "H:i",
    editable: isDesktop,
    hiddenName: true,
    interval: 60,
    min: "8:00",
    max: "22:00",
    clear: input.attr('required') ? "" : "Löschen",
  }).pickatime('picker');

  $(elem).find('.timeinput__open').click(function (e) {
    e.stopPropagation()
    e.preventDefault();
    picker.set('select', input.val());
    picker.open();
  });
})
