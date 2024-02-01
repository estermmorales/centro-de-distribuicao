export default function toggleModals() {
    const triggerButtons = $(".js-modal-button");
    const closeButtons = $(".close");

    triggerButtons.each(function () {
        const target = $(this).data("target");
        const modal = $(`.${target}`);

        $(this).on("click", function () {
        modal.addClass("is-active");
        });
    });

    closeButtons.each(function () {
        const target = $(this).data("target");
        const modal = $(`.${target}`);
        $(this).on("click", function (event) {
        modal.removeClass("is-active");
        });
    });
}