(function () {
    const TOAST_DURATION = 5200;
    const TOAST_EXIT_MS = 280;
    const MODAL_EXIT_MS = 200;

    let toastContainer = null;
    let activeConfirm = null;

    function ensureToastContainer() {
        if (toastContainer && document.body.contains(toastContainer)) {
            return toastContainer;
        }

        toastContainer = document.querySelector(".todate-toast-container");

        if (!toastContainer) {
            toastContainer = document.createElement("div");
            toastContainer.className = "todate-toast-container";
            document.body.appendChild(toastContainer);
        }

        return toastContainer;
    }

    function dismissToast(toast) {
        if (!toast || toast.dataset.todateClosing === "true") {
            return;
        }

        toast.dataset.todateClosing = "true";
        toast.classList.add("todate-toast-leave");

        const cleanup = () => toast.remove();
        toast.addEventListener("animationend", cleanup, { once: true });
        window.setTimeout(cleanup, TOAST_EXIT_MS + 40);
    }

    function wireToastLifecycle(toast, duration) {
        let timer = null;
        let startedAt = Date.now();
        let remaining = duration;

        function startTimer(delay) {
            clearTimeout(timer);
            startedAt = Date.now();
            timer = window.setTimeout(() => dismissToast(toast), delay);
        }

        function pauseTimer() {
            clearTimeout(timer);
            remaining -= Date.now() - startedAt;
            remaining = Math.max(0, remaining);
        }

        function resumeTimer() {
            if (remaining <= 0) {
                dismissToast(toast);
                return;
            }

            startTimer(remaining);
        }

        startTimer(remaining);

        toast.addEventListener("mouseenter", pauseTimer);
        toast.addEventListener("mouseleave", resumeTimer);
    }

    function presentToastElement(toast, duration = TOAST_DURATION) {
        if (!toast || toast.dataset.todateBound === "true") {
            return null;
        }

        toast.dataset.todateBound = "true";
        ensureToastContainer().prepend(toast);

        const progress = toast.querySelector(".todate-toast-progress");
        if (progress) {
            progress.style.animationDuration = `${duration}ms`;
        }

        const closeButton = toast.querySelector(".todate-toast-close");
        if (closeButton) {
            closeButton.addEventListener("click", () => dismissToast(toast));
        }

        wireToastLifecycle(toast, duration);

        return toast;
    }

    function mountFlashes(rootSelector = "[data-todate-flashes]") {
        const source = document.querySelector(rootSelector);
        if (!source) {
            return;
        }

        const toasts = source.querySelectorAll(".todate-toast");
        toasts.forEach((toast) => presentToastElement(toast));
        source.remove();
    }

    function closeActiveConfirm(result) {
        if (!activeConfirm) {
            return;
        }

        const { backdrop, onResolve, escHandler } = activeConfirm;
        document.removeEventListener("keydown", escHandler);

        activeConfirm = null;
        backdrop.classList.add("todate-confirm-hidden");

        window.setTimeout(() => {
            backdrop.remove();
            onResolve(result);
        }, MODAL_EXIT_MS);
    }

    function showConfirm(options = {}) {
        const title = options.title || "Confirmar ação";
        const message = options.message || "Deseja continuar?";
        const cancelText = options.cancelText || "Cancelar";
        const confirmText = options.confirmText || "Confirmar";

        if (activeConfirm) {
            closeActiveConfirm(false);
        }

        const backdrop = document.createElement("div");
        backdrop.className = "todate-confirm-backdrop";
        backdrop.innerHTML = `
            <div class="todate-confirm-modal" role="dialog" aria-modal="true" aria-label="${title}">
                <h3 class="todate-confirm-title">${title}</h3>
                <p class="todate-confirm-message">${message}</p>
                <div class="todate-confirm-actions">
                    <button type="button" class="btn btn-outline" data-confirm-cancel>${cancelText}</button>
                    <button type="button" class="btn btn-primary" data-confirm-ok>${confirmText}</button>
                </div>
            </div>
        `;

        return new Promise((resolve) => {
            const escHandler = (event) => {
                if (event.key === "Escape") {
                    closeActiveConfirm(false);
                }
            };

            activeConfirm = {
                backdrop,
                onResolve: resolve,
                escHandler,
            };

            backdrop.addEventListener("click", (event) => {
                if (event.target === backdrop) {
                    closeActiveConfirm(false);
                }
            });

            const cancelButton = backdrop.querySelector("[data-confirm-cancel]");
            const confirmButton = backdrop.querySelector("[data-confirm-ok]");

            if (cancelButton) {
                cancelButton.addEventListener("click", () => closeActiveConfirm(false));
            }

            if (confirmButton) {
                confirmButton.addEventListener("click", () => closeActiveConfirm(true));
            }

            document.addEventListener("keydown", escHandler);
            document.body.appendChild(backdrop);
        });
    }

    function showConfirmLegacy(title, message, callback) {
        showConfirm({ title, message }).then((confirmed) => {
            if (typeof callback === "function") {
                callback(confirmed);
            }
        });
    }

    document.addEventListener("DOMContentLoaded", () => {
        mountFlashes();
    });

    window.ToDate = Object.freeze({
        mountFlashes,
        presentToastElement,
        showConfirm,
        showConfirmLegacy,
    });
})();