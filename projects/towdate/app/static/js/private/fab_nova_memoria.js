document.addEventListener("DOMContentLoaded", () => {

    const trigger = document.querySelector("[data-memory-fab-trigger]");
    const modal = document.querySelector("[data-memory-fab-modal]");

    if (!trigger || !modal) return;

    const backdrop = modal.querySelector(".td-memory-fab-modal__backdrop");
    const closeButtons = modal.querySelectorAll("[data-memory-fab-close]");

    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    let expanded = false;

    function openModal() {
        modal.hidden = false;
        document.body.style.overflow = "hidden";
    }

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        trigger.classList.remove("is-expanded");
        expanded = false;
    }

    function toggleExpanded() {
        if (isMobile && !expanded) {
            trigger.classList.add("is-expanded");
            expanded = true;
        } else {
            openModal();
        }
    }

    trigger.addEventListener("click", toggleExpanded);

    closeButtons.forEach(button => {
        button.addEventListener("click", closeModal);
    });

    if (backdrop) {
        backdrop.addEventListener("click", closeModal);
    }

    document.addEventListener("click", event => {
        if (!trigger.contains(event.target) && !modal.contains(event.target) && expanded) {
            closeModal();
        }
    });

    document.addEventListener("keydown", event => {
        if (event.key === "Escape" && !modal.hidden) {
            closeModal();
        }
    });

});