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

const sidebar = document.querySelector('.sidebar');
const bars = document.querySelector(".bars");
console.log(bars);
bars.addEventListener("click", () => {
  sidebar.classList.toggle('active');
})