const byId = (id) => document.getElementById(id);

function bindConfirmSubmission({ button, form, type, title, message, confirmText, cancelText }) {
    if (!button || !form || typeof ToDate === "undefined") {
        return;
    }

    button.addEventListener("click", () => {
        ToDate.showConfirm({
            type,
            title,
            message,
            confirmText,
            cancelText,
        }).then((confirmed) => {
            if (confirmed) {
                form.submit();
            }
        });
    });
}

function bindPasswordToggle(toggleId, inputId, iconId) {
    const toggle = byId(toggleId);
    const input = byId(inputId);
    const icon = byId(iconId);

    if (!toggle || !input || !icon) {
        return;
    }

    const eyeOpen = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
    const eyeClosed = '<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';

    toggle.addEventListener("click", () => {
        const hidden = input.type === "password";
        input.type = hidden ? "text" : "password";
        icon.innerHTML = hidden ? eyeClosed : eyeOpen;
    });
}

const profileForm = byId("profileForm");
const saveProfileButton = byId("btnSalvar");

bindConfirmSubmission({
    button: saveProfileButton,
    form: profileForm,
    type: "info",
    title: "Salvar alterações",
    message: "Tem certeza que deseja salvar as alterações?",
    confirmText: "Salvar",
    cancelText: "Cancelar",
});

const photoForm = byId("photoForm");
const photoInput = byId("fotoPerfil");
const changePhotoButton = byId("btnAlterarFoto");

if (photoForm && photoInput) {
    if (changePhotoButton) {
        changePhotoButton.addEventListener("click", () => {
            photoInput.click();
        });
    }

    photoInput.addEventListener("change", () => {
        if (!photoInput.files.length || typeof ToDate === "undefined") {
            return;
        }

        ToDate.showConfirm({
            type: "warning",
            title: "Alterar foto de perfil",
            message: "Tem certeza que deseja alterar sua foto de perfil?",
            confirmText: "Alterar",
            cancelText: "Cancelar",
        }).then((confirmed) => {
            if (confirmed) {
                photoForm.submit();
            } else {
                photoInput.value = "";
            }
        });
    });
}

const removePhotoButton = byId("btnRemoverFoto");
const photoFormTypeInput = byId("formType");

if (removePhotoButton && photoForm && photoFormTypeInput && typeof ToDate !== "undefined") {
    removePhotoButton.addEventListener("click", () => {
        ToDate.showConfirm({
            type: "warning",
            title: "Remover foto de perfil",
            message: "Tem certeza que deseja remover sua foto de perfil?",
            confirmText: "Remover",
            cancelText: "Cancelar",
        }).then((confirmed) => {
            if (confirmed) {
                photoFormTypeInput.value = "remove_photo";
                photoForm.submit();
            }
        });
    });
}

const changePasswordForm = byId("changePasswordForm");
const changePasswordButton = byId("btnChangePassword");

bindConfirmSubmission({
    button: changePasswordButton,
    form: changePasswordForm,
    type: "warning",
    title: "Alterar senha",
    message: "Tem certeza que deseja alterar sua senha?",
    confirmText: "Alterar",
    cancelText: "Cancelar",
});

const logoutSessionsForm = byId("logoutSessionsForm");
const logoutSessionsButton = byId("btnLogoutSessions");

bindConfirmSubmission({
    button: logoutSessionsButton,
    form: logoutSessionsForm,
    type: "warning",
    title: "Encerrar todas as sessões",
    message: "Tem certeza que deseja encerrar todas as sessões?",
    confirmText: "Encerrar",
    cancelText: "Cancelar",
});

const deleteAccountForm = byId("deleteAccountForm");
const deleteAccountButton = byId("btnDeleteAccount");
const deletePasswordInput = byId("deleteAccountPassword");
const deletePasswordWrap = byId("deletePasswordWrap");

if (deleteAccountForm && deleteAccountButton && deletePasswordInput) {
    let deleteAccountArmed = false;

    deleteAccountButton.addEventListener("click", () => {
        if (!deleteAccountArmed) {
            if (typeof ToDate === "undefined") {
                return;
            }

            ToDate.showConfirm({
                type: "danger",
                title: "Excluir conta",
                message: "Tem certeza que deseja excluir sua conta? Esta ação é irreversível.",
                confirmText: "Continuar",
                cancelText: "Cancelar",
            }).then((confirmed) => {
                if (!confirmed) {
                    return;
                }

                deleteAccountArmed = true;
                if (deletePasswordWrap) {
                    deletePasswordWrap.classList.add("is-visible");
                }
                deleteAccountButton.textContent = "Confirmar exclusão";
                deletePasswordInput.focus();
            });

            return;
        }

        if (!deletePasswordInput.value.trim()) {
            deletePasswordInput.focus();
            deletePasswordInput.setCustomValidity("Informe sua senha para excluir a conta.");
            deletePasswordInput.reportValidity();
            return;
        }

        deletePasswordInput.setCustomValidity("");
        deleteAccountForm.submit();
    });

    deletePasswordInput.addEventListener("input", () => {
        deletePasswordInput.setCustomValidity("");
    });
}

bindPasswordToggle("currentPasswordToggle", "currentPassword", "currentPasswordEyeIcon");
bindPasswordToggle("newPasswordToggle", "newPassword", "newPasswordEyeIcon");
bindPasswordToggle("confirmPasswordToggle", "confirmPassword", "confirmPasswordEyeIcon");
bindPasswordToggle("deletePasswordToggle", "deleteAccountPassword", "deletePasswordEyeIcon");
