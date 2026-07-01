document.addEventListener("DOMContentLoaded", () => {
    const trigger = document.querySelector("[data-memory-fab-trigger]");
    const modal = document.querySelector("[data-memory-fab-modal]");

    if (!trigger || !modal) return;

    const backdrop = modal.querySelector(".td-memory-fab-modal__backdrop");
    const closeButtons = modal.querySelectorAll("[data-memory-fab-close]");
    const fileInput = modal.querySelector("#memoryFileInput");
    const previewGrid = modal.querySelector(".memory-new__preview-grid");
    const formWrapper = modal.querySelector("[data-form-wrapper]");
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
    const saveButton = modal.querySelector(".memory-new__save");
    const cancelButtons = modal.querySelectorAll(".memory-new__cancel");

    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    let expanded = false;
    let selectedFiles = [];
    let tags = [];
    let rating = 0;
    let selectedCollection = null;

    function openModal() {
        modal.hidden = false;
        document.body.style.overflow = "hidden";
        setDefaultDate();
        resetValidation();
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

    function setDefaultDate() {
        if (!dateInput) return;
        const today = new Date().toISOString().slice(0, 10);
        dateInput.value = today;
    }

    function updateFormVisibility() {
        if (!formWrapper) return;
        formWrapper.classList.add("memory-new__form-wrapper--visible");
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
                updateFormVisibility();
            });

            item.appendChild(img);
            item.appendChild(removeButton);
            previewGrid.appendChild(item);
        });
    }

    function addFiles(files) {
        const chosenFiles = Array.from(files).filter(file => file.type.startsWith("image/"));
        if (!chosenFiles.length) return;
        selectedFiles = selectedFiles.concat(chosenFiles);
        updatePreview();
        updateFormVisibility();
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
    }

    function resetValidation() {
        if (!errorList) return;
        errorList.innerHTML = "";
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

        if (!descriptionInput?.value.trim()) {
            errors.push("A descrição da memória não pode ficar vazia.");
            descriptionInput?.classList.add("memory-new__textarea--invalid");
        }

        if (!selectedCollection) {
            errors.push("Escolha uma coleção para a memória.");
            collectionButtons.forEach(button => button.classList.add("memory-new__collection-card--invalid"));
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
        updateFormVisibility();
        renderTags();
        resetValidation();
        setDefaultDate();
    }

    trigger.addEventListener("click", toggleExpanded);
    closeButtons.forEach(button => button.addEventListener("click", closeModal));
    cancelButtons.forEach(button => button.addEventListener("click", closeModal));

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
        });
    }

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

    saveButton?.addEventListener("click", () => {
        if (validateForm()) {
            showToast("Memória registrada com sucesso! (Modo demonstração)");
            resetForm();
        }
    });
});
