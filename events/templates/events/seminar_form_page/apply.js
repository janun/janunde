/*global $ */

// image_copyright is required if image chosen
function updateImageCopyright() {
  var CRlabel = $("#wrapper-id_image_copyright label");
  if ($("#id_image").val() !== "") {
    $("#wrapper-id_image_copyright").show();
    $("#id_image_copyright").attr("required", true);
    CRlabel.html( CRlabel.html().replace(" (optional)", "") );
  } else {
    $("#wrapper-id_image_copyright").hide();
    $("#id_image_copyright").attr("required", false);
    if (CRlabel.html().indexOf(" (optional)") === -1 ) {
      CRlabel.html( CRlabel.html() + " (optional)" );
    }
  }
}
$("#id_image").change(updateImageCopyright);
updateImageCopyright();

// end date picker must be after start date
$("#wrapper-id_end_0 .dateinput__open").click(function () {
  var begin = $("#id_begin_0").val();
  $("#id_end_0").pickadate("picker").set("min", begin);
});

// only show certain fields when publish is true
function updatePublish() {
  if ($("#id_publish").prop("checked")) {
    $("#wrapper-id_image").show();
    $("#wrapper-id_image_copyright").show();
    updateImageCopyright();
    $("#id_publish").parents("fieldset").next().show();
  } else {
    $("#wrapper-id_image").hide();
    $("#wrapper-id_image_copyright").hide();
    $("#id_image_copyright").attr("required", false);
    $("#id_publish").parents("fieldset").next().hide();
  }
}
$("#id_publish").on("change", updatePublish);
updatePublish();

// website_contact_* is prefilled from contact_*
["contact_name", "contact_phone", "contact_mail"].forEach(function (field) {
  var websiteField = $("#id_website_" + field);
  var contactField = $("#id_" + field);
  websiteField.on("input", function() {
    if (websiteField.val() !== "") {
      websiteField.attr("touched", true);
    }
  });
  contactField.on("input", function() {
    if (!websiteField.attr("touched")) {
      websiteField.val(contactField.val());
    }
  });
});

function getFundingAmount(attendees, days, hasGroup) {
  if (days === 1) {
    return attendees * 6.5;
  } else {
    return attendees * days * (hasGroup ? 11.5 : 9.0);
  }
}

function formatNumber(number) {
  return number.toFixed(2)
    .replace(/(\d)(?=(\d{3})+\.)/g, "$1 ")
    .replace(".", ",");
}

function updateFunding() {
  var attendees = parseInt($("#id_attendees").val());
  var days = parseInt($("#id_days").val());
  var hasGroup = $("#id_group").val() !== "";

  if (attendees > 0 && days > 0) {
    var possibleFunding = getFundingAmount(attendees, days, hasGroup);
    if ($("#possibleFunding").length === 0) {
      $("#wrapper-id_requested").prepend("<p id=\"possibleFunding\"></p>");
    }
    $("#possibleFunding").html(
      "Dein Seminar kann mit maximal " +
      formatNumber(possibleFunding) + "&nbsp;€ " +
      "gefördert werden."
    );
    $("#id_requested").attr("max", possibleFunding);
    if (!$("#id_requested").attr("touched") || $("#id_requested").attr("touched") == "false") {
      $("#id_requested").val(possibleFunding);
    }
    $("#checkPossibleFunding").html("von " + formatNumber(possibleFunding) + "&nbsp;€ ");
  } else {
    $("#possibleFunding").html("");
    $("#id_requested").attr("max", "");
    if (!$("#id_requested").attr("touched") || $("#id_requested").attr("touched") == "false") {
      $("#id_requested").val();
    }
    $("#checkPossibleFunding").html();
  }
}

$("#id_attendees").on("input", updateFunding);
$("#id_days").on("input", updateFunding);
$("#id_group").on("input", updateFunding);
$("#id_requested").on("input", function() {
  if ($("#id_requested").val() === "") {
    $("#id_requested").attr("touched", false);
  } else {
    $("#id_requested").attr("touched", true);
  }
});
// updateFunding();

// update deadline checkbox
// $("id_end_0").change(function () {
// TODO
// })

// focus first one with an error:
$(".form__fieldwrapper--has-error input").first().focus();
