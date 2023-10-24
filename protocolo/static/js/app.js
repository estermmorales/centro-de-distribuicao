$(document).ready(function () {
  // Função para ativar o link do menu
  function activeMenuLink() {
    const $linksMenu = $(".menu li");

    function handleLink(event) {
      $linksMenu.removeClass("active");
      $(this).addClass("active");
    }

    $linksMenu.on("click", handleLink);
  }

  activeMenuLink();

  // Função para expandir o menu
  function expandMenu() {
    const $sidebar = $(".sidebar");
    const $bars = $(".bars");
    const $barsIcon = $bars.find(".bars-icon");
    const $cIcon = $bars.find(".c-icon");

    $bars.on("click", function () {
      $sidebar.toggleClass("active");
      $barsIcon.toggleClass("active");
      $cIcon.toggleClass("active");
    });
  }

  expandMenu();

  // Lidar com modais
  const $triggerButtons = $(".js-modal-button");
  const $closeButtons = $(".close");

  $triggerButtons.each(function () {
    const target = $(this).data("target");
    const $modal = $(`.${target}`);

    $(this).on("click", function () {
      $modal.addClass("is-active");
    });
  });

  $closeButtons.on("click", function () {
    const target = $(this).data("target");
    const $modal = $(`.${target}`);
    $modal.removeClass("is-active");
  });
});
