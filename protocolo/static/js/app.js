function activeMenuLink() {
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
}
activeMenuLink();

function expandMenu() {
  const sidebar = document.querySelector(".sidebar");
  const bars = document.querySelector(".bars");
  const barsIcon = bars.querySelector(".bars-icon");
  const cIcon = bars.querySelector(".c-icon");
  bars.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    barsIcon.classList.toggle("active");
    cIcon.classList.toggle("active");
  });
}
expandMenu();

const triggerButtons = document.querySelectorAll(".js-modal-button");
const closeButtons = document.querySelectorAll(".close");
console.log(closeButtons)
triggerButtons.forEach((button) => {
  const target = button.dataset.target;
  const modal = document.querySelector(`.${target}`);
  console.log(modal);
  button.addEventListener("click", () => {
    modal.classList.add("is-active");
  });

  closeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      modal.classList.remove("is-active");
    });
  });
});

// const addButton = document.querySelector(".add-button-modal");
// const addModal = document.querySelector(".add-modal");
// const closeModalButton = document.querySelector(".modal-close");
// addButton.addEventListener("click", () => {
//   addModal.classList.add("is-active");
// });
// closeModalButton.addEventListener("click", () => {
//   addModal.classList.remove("is-active");
// });
