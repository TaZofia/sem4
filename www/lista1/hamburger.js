const fadeInMenu = document.querySelector(".fadeInMenu");
const items = document.querySelectorAll(".item");
const hamburger = document.querySelector(".hamburger");
const closeIcon = document.querySelector(".closeIcon");
const menuIcon = document.querySelector(".menuIcon");

function menuFadeIn() {
  if (fadeInMenu.classList.contains("showMenu")) {
    fadeInMenu.classList.remove("showMenu");
    closeIcon.style.display = "none";
    menuIcon.style.display = "block";
  } else {
    fadeInMenu.classList.add("showMenu");
    closeIcon.style.display ="block";
    menuIcon.style.display = "none";
  }
}
hamburger.addEventListener("click", menuFadeIn);

items.forEach(
  function(menuItem) {
    menuItem.addEventListener("click", menuFadeIn);
  }
)
window.addEventListener("DOMContentLoaded", function() {
  fadeInMenu.classList.remove("showMenu");
  closeIcon.style.display = "none";
  menuIcon.style.display = "block";
});