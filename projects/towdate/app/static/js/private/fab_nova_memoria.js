document.addEventListener("DOMContentLoaded", () => {
    const trigger = document.querySelector("[data-memory-fab-trigger]");
    const modal = document.querySelector("[data-memory-fab-modal]");

    if (!trigger || !modal) return;

    const backdrop = modal.querySelector(".td-memory-fab-modal__backdrop");
    const closeButtons = modal.querySelectorAll("[data-memory-fab-close]");
    const fileInput = modal.querySelector("#memoryFileInput");
    const previewGrid = modal.querySelector(".memory-new__preview-grid");
    const formWrapper = modal.querySelector("[data-form-wrapper]");
    const stepPanels = Array.from(modal.querySelectorAll("[data-step-panel]"));
    const stepCounter = modal.querySelector("[data-step-counter]");
    const progressFill = modal.querySelector("[data-progress-fill]");
    const stepBackButton = modal.querySelector("[data-step-back]");
    const stepNextButton = modal.querySelector("[data-step-next]");
    const stepSaveButton = modal.querySelector("[data-memory-save]");
    const titleInput = modal.querySelector("[data-memory-title]");
    const descriptionInput = modal.querySelector("[data-memory-description]");
    const descriptionCounter = modal.querySelector("[data-description-counter]");
    const dateInput = modal.querySelector("[data-memory-date]");
    const locationInput = modal.querySelector("[data-memory-location]");
    const tagInput = modal.querySelector(".memory-new__tag-input");
    const tagList = modal.querySelector(".memory-new__tag-list");
    const starButtons = modal.querySelectorAll(".memory-new__star");
    const ratingShell = modal.querySelector(".memory-new__rating");
    const collectionButtons = modal.querySelectorAll(".memory-new__collection-card");
    const errorList = modal.querySelector(".memory-new__error-list");
    const toast = modal.querySelector(".memory-new__toast");
    const photoActionButtons = modal.querySelectorAll("[data-photo-action]");

    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    let expanded = false;
    let currentStep = 1;
    let selectedFiles = [];
    let tags = [];
    let rating = 0;
    let selectedCollection = null;

    function setDefaultDate() {
        if (!dateInput || dateInput.value) return;
        dateInput.value = new Date().toISOString().slice(0, 10);
    }

    function clearErrorList() {
        if (!errorList) return;
        errorList.innerHTML = "";
    }

    function showError(message) {
        if (!errorList) return;

        errorList.innerHTML = "";

        const item = document.createElement("div");
        item.className = "memory-new__error-item";
        item.textContent = message;
        errorList.appendChild(item);
    }

    function resetValidation() {
        clearErrorList();
        titleInput?.classList.remove("memory-new__input--invalid");
        descriptionInput?.classList.remove("memory-new__textarea--invalid");
        collectionButtons.forEach(button => button.classList.remove("memory-new__collection-card--invalid"));
        toast?.setAttribute("hidden", "true");
    }

    function showToast(message) {
        if (!toast) return;
        const messageNode = toast.querySelector(".memory-new__toast-message");
        if (messageNode) {
            messageNode.textContent = message;
        }
        toast.removeAttribute("hidden");
        toast.classList.add("memory-new__toast--visible");

        window.setTimeout(() => {
            toast.classList.remove("memory-new__toast--visible");
            toast.setAttribute("hidden", "true");
        }, 3200);
    }

    function updatePreview() {
        if (!previewGrid) return;
        previewGrid.innerHTML = "";

        selectedFiles.forEach((file, index) => {
            const item = document.createElement("div");
            item.className = "memory-new__preview-item";

            const img = document.createElement("img");
            img.src = URL.createObjectURL(file);
            img.alt = file.name;
            img.onload = () => URL.revokeObjectURL(img.src);

            const removeButton = document.createElement("button");
            removeButton.type = "button";
            removeButton.className = "memory-new__preview-remove";
            removeButton.textContent = "✕";
            removeButton.addEventListener("click", () => {
                selectedFiles = selectedFiles.filter((_, fileIndex) => fileIndex !== index);
                updatePreview();
                updateWizardState();
            });

            item.appendChild(img);
            item.appendChild(removeButton);
            previewGrid.appendChild(item);
        });
    }

    function addFiles(files) {
        const chosenFiles = Array.from(files).filter(file => file.type.startsWith("image/"));
        if (!chosenFiles.length) return;

        // Single-image flow: keep only one photo per modal session.
        selectedFiles = [chosenFiles[0]];
        updatePreview();
        updateWizardState();
        clearErrorList();
    }

    function openFilePicker(capture = false) {
        if (!fileInput) return;

        if (capture) {
            fileInput.setAttribute("capture", "environment");
        } else {
            fileInput.removeAttribute("capture");
        }

        fileInput.click();
    }

    function renderTags() {
        if (!tagList) return;
        tagList.innerHTML = "";

        tags.forEach((tag, index) => {
            const chip = document.createElement("span");
            chip.className = "memory-new__tag-chip";
            chip.textContent = tag;

            const remove = document.createElement("button");
            remove.type = "button";
            remove.className = "memory-new__tag-remove";
            remove.textContent = "✕";
            remove.addEventListener("click", () => {
                tags = tags.filter((_, tagIndex) => tagIndex !== index);
                renderTags();
            });

            chip.appendChild(remove);
            tagList.appendChild(chip);
        });
    }

    function handleTagInput(event) {
        if (event.key !== "Enter") return;
        event.preventDefault();

        const value = tagInput.value.trim();
        if (!value) return;

        const normalized = value.startsWith("#") ? value : `#${value}`;
        if (!tags.includes(normalized)) {
            tags.push(normalized);
            renderTags();
        }

        tagInput.value = "";
    }

    function updateRating(value) {
        rating = value;
        ratingShell?.setAttribute("data-rating", value);

        starButtons.forEach(button => {
            const starValue = Number(button.dataset.star);
            button.classList.toggle("memory-new__star--active", starValue <= value);
        });
    }

    function handleCollectionSelection(event) {
        collectionButtons.forEach(button => button.classList.remove("memory-new__collection-card--selected", "memory-new__collection-card--invalid"));
        const target = event.currentTarget;
        selectedCollection = target.dataset.collectionOption || null;
        target.classList.add("memory-new__collection-card--selected");
        clearErrorList();
    }

    function focusCurrentStep() {
        const currentPanel = stepPanels.find(panel => Number(panel.dataset.stepPanel) === currentStep);
        if (!currentPanel) return;

        const focusSelector = currentStep === 1
            ? ".memory-new__photo-button"
            : currentStep === 2
                ? "[data-memory-title]"
                : currentStep === 3
                    ? ".memory-new__collection-card"
                    : ".memory-new__tag-input";

        const target = currentPanel.querySelector(focusSelector);
        if (target && typeof target.focus === "function") {
            target.focus({ preventScroll: true });
            return;
        }

        currentPanel.focus({ preventScroll: true });
    }

    function updateFooterButtons() {
        if (stepBackButton) {
            stepBackButton.hidden = false;
        }

        if (stepNextButton) {
            stepNextButton.hidden = currentStep === 4;
            stepNextButton.disabled = currentStep === 1 && !selectedFiles.length;
            stepNextButton.setAttribute("aria-disabled", String(stepNextButton.disabled));
        }

        if (stepSaveButton) {
            stepSaveButton.hidden = currentStep !== 4;
        }
    }

    function updateStepIndicators() {
        if (stepCounter) {
            stepCounter.textContent = `${currentStep} de 4`;
        }

        if (progressFill) {
            progressFill.style.width = `${(currentStep / 4) * 100}%`;
        }
    }

    function updateWizardState() {
        stepPanels.forEach(panel => {
            const isActive = Number(panel.dataset.stepPanel) === currentStep;
            panel.classList.toggle("memory-new__step--active", isActive);
            panel.setAttribute("aria-hidden", String(!isActive));

            if ("inert" in panel) {
                panel.inert = !isActive;
            }
        });

        updateStepIndicators();
        updateFooterButtons();
    }

    function goToStep(stepNumber, direction = "next") {
        currentStep = Math.min(4, Math.max(1, stepNumber));

        if (formWrapper) {
            formWrapper.style.setProperty("--step-enter-x", direction === "prev" ? "-18px" : "18px");
        }

        updateWizardState();

        window.requestAnimationFrame(() => {
            focusCurrentStep();
        });
    }

    function canAdvanceFromCurrentStep() {
        if (currentStep === 1 && !selectedFiles.length) {
            showError("Adicione pelo menos uma foto para continuar.");
            return false;
        }

        clearErrorList();
        return true;
    }

    function openModal() {
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        setDefaultDate();
        resetValidation();
        goToStep(1, "next");
    }

    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = "";
        trigger.classList.remove("is-expanded");
        expanded = false;
    }

    function toggleExpanded() {
        openModal();
    }

    function validateForm() {
        const errors = [];
        resetValidation();

        if (!selectedFiles.length) {
            errors.push("Adicione pelo menos uma foto para registrar a memória.");
        }

        if (!titleInput?.value.trim()) {
            errors.push("O título da memória é obrigatório.");
            titleInput?.classList.add("memory-new__input--invalid");
        }

        if (!selectedCollection) {
            errors.push("Escolha uma coleção para a memória.");
            collectionButtons.forEach(button => button.classList.add("memory-new__collection-card--invalid"));
        }

        if (!rating) {
            errors.push("A avaliação da memória é obrigatória.");
        }

        if (descriptionInput?.value.length > 280) {
            errors.push("A descrição pode ter no máximo 280 caracteres.");
            descriptionInput?.classList.add("memory-new__textarea--invalid");
        }

        if (!errorList) return errors.length === 0;
        errorList.innerHTML = "";
        errors.forEach(error => {
            const item = document.createElement("div");
            item.className = "memory-new__error-item";
            item.textContent = error;
            errorList.appendChild(item);
        });

        return errors.length === 0;
    }

    function resetForm() {
        selectedFiles = [];
        tags = [];
        rating = 0;
        selectedCollection = null;

        if (titleInput) titleInput.value = "";
        if (descriptionInput) descriptionInput.value = "";
        if (locationInput) locationInput.value = "";
        if (tagInput) tagInput.value = "";
        if (descriptionCounter) descriptionCounter.textContent = "0 / 280";

        collectionButtons.forEach(button => button.classList.remove("memory-new__collection-card--selected", "memory-new__collection-card--invalid"));
        updateRating(0);
        updatePreview();
        renderTags();
        resetValidation();
        setDefaultDate();
        goToStep(1, "next");
    }

    trigger.addEventListener("click", toggleExpanded);
    closeButtons.forEach(button => button.addEventListener("click", closeModal));

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

    if (fileInput) {
        fileInput.addEventListener("change", event => {
            addFiles(event.target.files);
            fileInput.value = "";
            fileInput.removeAttribute("capture");
        });
    }

    photoActionButtons.forEach(button => {
        button.addEventListener("click", () => {
            const action = button.dataset.photoAction;
            openFilePicker(action === "camera");
        });
    });

    const dropzone = modal.querySelector(".memory-new__dropzone");
    if (dropzone) {
        dropzone.addEventListener("dragover", event => {
            event.preventDefault();
            dropzone.classList.add("memory-new__dropzone--active");
        });

        dropzone.addEventListener("dragleave", () => {
            dropzone.classList.remove("memory-new__dropzone--active");
        });

        dropzone.addEventListener("drop", event => {
            event.preventDefault();
            dropzone.classList.remove("memory-new__dropzone--active");
            addFiles(event.dataTransfer.files);
        });
    }

    tagInput?.addEventListener("keydown", handleTagInput);

    starButtons.forEach(button => {
        button.addEventListener("click", () => updateRating(Number(button.dataset.star)));
        button.addEventListener("pointerenter", () => {
            const hoverRating = Number(button.dataset.star);
            starButtons.forEach(inner => inner.classList.toggle("memory-new__star--active", Number(inner.dataset.star) <= hoverRating));
        });
        button.addEventListener("pointerleave", () => updateRating(rating));
    });

    collectionButtons.forEach(button => button.addEventListener("click", handleCollectionSelection));

    descriptionInput?.addEventListener("input", () => {
        const count = descriptionInput.value.length;
        if (descriptionCounter) {
            descriptionCounter.textContent = `${count} / 280`;
        }
    });

    stepBackButton?.addEventListener("click", () => {
        if (currentStep > 1) {
            goToStep(currentStep - 1, "prev");
            return;
        }

        closeModal();
    });

    stepNextButton?.addEventListener("click", () => {
        if (!canAdvanceFromCurrentStep()) return;
        goToStep(currentStep + 1, "next");
    });

    stepSaveButton?.addEventListener("click", () => {
        if (validateForm()) {
            resetForm();
            showToast("Memória registrada com sucesso! (Modo demonstração)");
        }
    });

    updatePreview();
    renderTags();
    updateRating(0);
    updateWizardState();
});
