document.querySelectorAll(".js-scroll-spy").forEach(function (container) {
  var sections = container.querySelectorAll(".js-scroll-spy-section");

  var menu = container.querySelector(".js-scroll-spy-menu");
  var menuItems = menu.querySelectorAll("a");
  var classlist = menu.getAttribute("data-js-scroll-spy-class").split(" ");
  var offset = menu.getAttribute("data-offset") || 0;

  function onScroll() {
    var activeSections = [];
    sections.forEach(function (section) {
      if (section.getBoundingClientRect().top < offset) {
        activeSections.push(section);
      }
    });

    menuItems.forEach(function (menuItem) {
      classlist.forEach(function (klass) {
        menuItem.classList.remove(klass);
      });
    });

    if (activeSections.length > 0) {
      var activeSection = activeSections[activeSections.length - 1];
      var activeMenuItem = menu.querySelector("[href=\"#" + activeSection.id + "\"]");

      classlist.forEach(function (klass) {
        activeMenuItem.classList.add(klass);
      });
    }

    // Fix for last element if scrolled to the bottom
    if ((window.innerHeight + window.scrollY) >= document.body.scrollHeight) {
      menuItems.forEach(function (menuItem) {
        classlist.forEach(function (klass) {
          menuItem.classList.remove(klass);
        });
      });

      classlist.forEach(function (klass) {
        menuItems[menuItems.length - 1].classList.add(klass);
      });
    }

  }

  document.addEventListener("scroll", onScroll);
  onScroll();
});