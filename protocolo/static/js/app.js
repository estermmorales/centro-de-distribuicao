const linksMenu = document.querySelectorAll(".menu li");

function handleLink(event) {
  linksMenu.forEach((link) => {
    link.classList.remove("active");
  });
  event.currentTarget.classList.add("active");
}
linksMenu.forEach((link) => {
  link.addEventListener("click", handleLink);
});

const sidebar = document.querySelector(".sidebar");
const bars = document.querySelector(".bars");
const barsIcon = bars.querySelector(".bars-icon");
const cIcon = bars.querySelector(".c-icon");
console.log(barsIcon);
bars.addEventListener("click", () => {
  sidebar.classList.toggle("active");
  barsIcon.classList.toggle("active");
  cIcon.classList.toggle("active");
});
