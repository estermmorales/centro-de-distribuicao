export default function activeMenuLink() {
    const linksMenu = $(".menu li");

    function handleLink(event) {
      linksMenu.removeClass("active");
      $(this).addClass("active");
    }
    linksMenu.on("click", handleLink);

    $("li#protocolos").addClass("active");
    const links = ["historico", "usuarios", "funcionarios", "configuracoes"];
    links.forEach((link) => {
      if (window.location.href.includes(link)) {
        $("li#protocolos").removeClass("active");
        $(`li#${link}`).addClass("active");
      }
    });
}