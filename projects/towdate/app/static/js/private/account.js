(() => {
    const byId = (id) => document.getElementById(id);

    const EYE_OPEN_ICON = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
    const EYE_CLOSED_ICON = '<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';

    document.addEventListener("DOMContentLoaded", initializeAccountPage);

    function initializeAccountPage() {
        initProfileFormConfirmation();
        initProfilePhotoChange();
        initRelationshipPhotoChange();
        initPartnerPage();
        initProfilePhotoRemoval();
        initSecurityConfirmButtons();
        initEndRelationshipFlow();
        initDeleteAccountFlow();
        initPasswordToggles();
    }

    function hasToDateConfirm() {
        return typeof ToDate !== "undefined" && typeof ToDate.showConfirm === "function";
    }

    function bindConfirmSubmission({ button, form, type, title, message, confirmText, cancelText }) {
        if (!button || !form) {
            return;
        }

        button.addEventListener("click", () => {
            if (!hasToDateConfirm()) {
                form.submit();
                return;
            }

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

        toggle.addEventListener("click", () => {
            const isHidden = input.type === "password";
            input.type = isHidden ? "text" : "password";
            icon.innerHTML = isHidden ? EYE_CLOSED_ICON : EYE_OPEN_ICON;
        });
    }

    function initProfileFormConfirmation() {
        bindConfirmSubmission({
            button: byId("btnSalvar"),
            form: byId("profileForm"),
            type: "info",
            title: "Salvar alterações",
            message: "Tem certeza que deseja salvar as alterações?",
            confirmText: "Salvar",
            cancelText: "Cancelar",
        });
    }

    function initProfilePhotoChange() {
        bindPhotoUploadAutoSubmit({
            formId: "photoForm",
            inputId: "fotoPerfil",
            buttonId: "btnAlterarFoto",
            title: "Alterar foto de perfil",
            message: "Tem certeza que deseja alterar sua foto de perfil?",
        });
    }

    function initRelationshipPhotoChange() {
        bindPhotoUploadAutoSubmit({
            formId: "relationshipPhotoForm",
            inputId: "couplePhoto",
            buttonId: "btnAlterarFotoRelacionamento",
            title: "Alterar foto do relacionamento",
            message: "Tem certeza que deseja alterar a foto do relacionamento?",
        });
    }

    function initPartnerPage() {
        initPartnerCodeCopy();
        initPartnerCodeShare();
        initPartnerDisconnectFlow();
    }

    function initPartnerCodeCopy() {
        const button = byId("btnCopyPartnerCode");
        const input = byId("inviteCode");

        if (!button || !input || button.disabled) {
            return;
        }

        button.addEventListener("click", async () => {
            const value = input.value?.trim();
            if (!value) {
                return;
            }

            try {
                await navigator.clipboard.writeText(value);
                showClientToast("success", "Código copiado", "O código do convite foi copiado.");
            } catch {
                const wasDisabled = input.disabled;
                if (wasDisabled) {
                    input.removeAttribute("disabled");
                }
                input.select();
                document.execCommand("copy");
                input.setSelectionRange(0, 0);
                if (wasDisabled) {
                    input.setAttribute("disabled", "disabled");
                }
                showClientToast("success", "Código copiado", "O código do convite foi copiado.");
            }
        });
    }

    function initPartnerCodeShare() {
        const button = byId("btnSharePartnerCode");
        const input = byId("inviteCode");

        if (!button || !input || button.disabled) {
            return;
        }

        button.addEventListener("click", async () => {
            const value = input.value?.trim();
            if (!value) {
                return;
            }

            const shareText = `Use este código para conectar seu parceiro no ToDate: ${value}`;

            if (navigator.share) {
                try {
                    await navigator.share({
                        title: "Convite ToDate",
                        text: shareText,
                    });
                    return;
                } catch {
                    // Fallback para cópia abaixo.
                }
            }

            try {
                await navigator.clipboard.writeText(shareText);
                showClientToast("info", "Convite pronto", "O texto do convite foi copiado para compartilhar.");
            } catch {
                showClientToast("warning", "Compartilhamento indisponível", "Não foi possível compartilhar o convite neste dispositivo.");
            }
        });
    }

    function initPartnerDisconnectFlow() {
        bindConfirmSubmission({
            button: byId("btnDisconnectPartner"),
            form: byId("disconnectPartnerForm"),
            type: "danger",
            title: "Desconectar parceiro",
            message: "Tem certeza que deseja remover o vínculo entre as duas contas?",
            confirmText: "Desconectar",
            cancelText: "Cancelar",
        });
    }

    function showClientToast(type, title, message) {
        if (typeof ToDate === "undefined" || typeof ToDate.presentToastElement !== "function") {
            return;
        }

        const toast = document.createElement("div");
        toast.className = `todate-toast todate-toast-${type}`;
        toast.innerHTML = `
            <div class="todate-toast-body">
                <div class="todate-toast-title">${title}</div>
                <div class="todate-toast-message">${message}</div>
            </div>
            <button class="todate-toast-close" type="button" aria-label="Fechar notificação">✕</button>
            <span class="todate-toast-progress"></span>
        `;

        ToDate.presentToastElement(toast);
    }

    function bindPhotoUploadAutoSubmit({ formId, inputId, buttonId, title, message }) {
        const form = byId(formId);
        const input = byId(inputId);
        const button = byId(buttonId);

        if (!form || !input || !button) {
            return;
        }

        button.addEventListener("click", () => input.click());

        input.addEventListener("change", () => {
            if (!input.files.length) {
                return;
            }

            if (!hasToDateConfirm()) {
                form.submit();
                return;
            }

            ToDate.showConfirm({
                type: "warning",
                title,
                message,
                confirmText: "Alterar",
                cancelText: "Cancelar",
            }).then((confirmed) => {
                if (confirmed) {
                    form.submit();
                    return;
                }

                input.value = "";
            });
        });
    }

    function initProfilePhotoRemoval() {
        const button = byId("btnRemoverFoto");
        const form = byId("photoForm");
        const formTypeInput = byId("formType");

        if (!button || !form || !formTypeInput) {
            return;
        }

        button.addEventListener("click", () => {
            const submitRemoval = () => {
                formTypeInput.value = "remove_photo";
                form.submit();
            };

            if (!hasToDateConfirm()) {
                submitRemoval();
                return;
            }

            ToDate.showConfirm({
                type: "warning",
                title: "Remover foto de perfil",
                message: "Tem certeza que deseja remover sua foto de perfil?",
                confirmText: "Remover",
                cancelText: "Cancelar",
            }).then((confirmed) => {
                if (confirmed) {
                    submitRemoval();
                }
            });
        });
    }

    function initSecurityConfirmButtons() {
        bindConfirmSubmission({
            button: byId("btnChangePassword"),
            form: byId("changePasswordForm"),
            type: "warning",
            title: "Alterar senha",
            message: "Tem certeza que deseja alterar sua senha?",
            confirmText: "Alterar",
            cancelText: "Cancelar",
        });

        bindConfirmSubmission({
            button: byId("btnLogoutSessions"),
            form: byId("logoutSessionsForm"),
            type: "warning",
            title: "Encerrar todas as sessões",
            message: "Tem certeza que deseja encerrar todas as sessões?",
            confirmText: "Encerrar",
            cancelText: "Cancelar",
        });
    }

    function initEndRelationshipFlow() {
        const form = byId("endRelationshipForm");
        const button = byId("btnEndRelationship");
        const passwordInput = byId("endRelationshipPassword");
        const passwordWrap = byId("endRelationshipPasswordWrap");

        if (!form || !button || !passwordInput) {
            return;
        }

        let isArmed = passwordInput.classList.contains("is-invalid");

        if (isArmed) {
            if (passwordWrap) {
                passwordWrap.style.display = "block";
            }
            button.textContent = "Confirmar encerramento";
        }

        button.addEventListener("click", () => {
            if (!isArmed) {
                confirmEndRelationship().then((confirmed) => {
                    if (!confirmed) {
                        return;
                    }

                    isArmed = true;
                    if (passwordWrap) {
                        passwordWrap.style.display = "block";
                    }
                    button.textContent = "Confirmar encerramento";
                    passwordInput.focus();
                });
                return;
            }

            if (!passwordInput.value.trim()) {
                passwordInput.focus();
                passwordInput.setCustomValidity("Informe sua senha para encerrar o relacionamento.");
                passwordInput.reportValidity();
                return;
            }

            passwordInput.setCustomValidity("");
            form.submit();
        });

        passwordInput.addEventListener("input", () => {
            passwordInput.setCustomValidity("");
        });
    }

    function confirmEndRelationship() {
        if (hasToDateConfirm()) {
            return ToDate.showConfirm({
                type: "danger",
                title: "Encerrar relacionamento",
                message: "Tem certeza que deseja encerrar o relacionamento? Esta ação é irreversível.",
                confirmText: "Continuar",
                cancelText: "Cancelar",
            });
        }

        return Promise.resolve(
            window.confirm("Tem certeza que deseja encerrar o relacionamento? Esta ação é irreversível.")
        );
    }

    function initDeleteAccountFlow() {
        const form = byId("deleteAccountForm");
        const button = byId("btnDeleteAccount");
        const passwordInput = byId("deleteAccountPassword");
        const passwordWrap = byId("deletePasswordWrap");

        if (!form || !button || !passwordInput) {
            return;
        }

        let isArmed = false;

        button.addEventListener("click", () => {
            if (!isArmed) {
                if (!hasToDateConfirm()) {
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

                    isArmed = true;
                    if (passwordWrap) {
                        passwordWrap.hidden = false;
                        passwordWrap.classList.add("is-visible");
                    }
                    button.textContent = "Confirmar exclusão";
                    passwordInput.focus();
                });

                return;
            }

            if (!passwordInput.value.trim()) {
                passwordInput.focus();
                passwordInput.setCustomValidity("Informe sua senha para excluir a conta.");
                passwordInput.reportValidity();
                return;
            }

            passwordInput.setCustomValidity("");
            form.submit();
        });

        passwordInput.addEventListener("input", () => {
            passwordInput.setCustomValidity("");
        });
    }

    function initPasswordToggles() {
        bindPasswordToggle("currentPasswordToggle", "currentPassword", "currentPasswordEyeIcon");
        bindPasswordToggle("newPasswordToggle", "newPassword", "newPasswordEyeIcon");
        bindPasswordToggle("confirmPasswordToggle", "confirmPassword", "confirmPasswordEyeIcon");
        bindPasswordToggle("deletePasswordToggle", "deleteAccountPassword", "deletePasswordEyeIcon");
    }
})();
