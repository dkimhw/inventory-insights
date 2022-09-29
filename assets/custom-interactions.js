
// Dashboard title section becomes sticky as user scrolls so that filters are always visible to users
window.onscroll = function() {
  let titleSection = document.getElementById('dashboard-title-section');
  console.log(titleSection);
  if (window.pageYOffset > 100) {
    titleSection.classList.add("floating-nav");
  } else {
    titleSection.classList.remove("floating-nav");
  }
}
