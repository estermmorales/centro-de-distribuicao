export default function expandMenu() {
    const sidebar = $(".sidebar");
    const bars = $(".bars");
    const barsIcon = bars.find(".bars-icon");
    const cIcon = bars.find(".c-icon");

    bars.on("click", function () {
      sidebar.toggleClass("active");
      barsIcon.toggleClass("active");
      cIcon.toggleClass("active");
    });
}