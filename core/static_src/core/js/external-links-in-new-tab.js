document.querySelectorAll('a[href^="http://"], a[href^="https://"]').forEach(function (elem) {
    elem.setAttribute("target", "_blank")
});