(function () {
    const TOAST_DURATION = 5200;
    let toastContainer = null;
    let confirmBackdrop = null;
    const catalog = {
        success: [
            'Login realizado com sucesso.',
            'Conta criada com sucesso.',
            'Alteracoes salvas com sucesso.',
            'Meta criada com sucesso.',
            'Evento criado com sucesso.',
            'Foto enviada com sucesso.',
            'Carta enviada com sucesso.',
            'Operacao concluida.'
        ],
        error: [
            'Email ou senha incorretos.',
            'Usuario nao encontrado.',
            'Email ja cadastrado.',
            'Senhas nao coincidem.',
            'Erro ao salvar dados.',
            'Erro ao enviar imagem.',
            'Erro interno do servidor.',
            'Falha na operacao.'
        ],
        warning: [
            'Preencha todos os campos obrigatorios.',
            'Dados incompletos.',
            'Sessao prestes a expirar.',
            'Arquivo muito grande.',
            'Acao requer confirmacao.'
        ],
        info: [
            'Verifique seu email.',
            'Nova funcionalidade disponivel.',
            'Atualizacao realizada.',
            'Informacao importante do sistema.'
        ]
    };

    function ensureToastContainer() {
        if (toastContainer) return toastContainer;
        toastContainer = document.createElement('div');
        toastContainer.className = 'todate-toast-container';
        document.body.appendChild(toastContainer);
        return toastContainer;
    }

    function iconForType(type) {
        const icons = {
            success: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polyline points="20 6 9 17 4 12"></polyline></svg>',
            error: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
            warning: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>',
            info: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>'
        };

        return icons[type] || icons.info;
    }

    function titleForType(type) {
        const map = {
            success: 'Sucesso',
            error: 'Erro',
            warning: 'Atenção',
            info: 'Informação'
        };

        return map[type] || 'Notificação';
    }

    function removeToast(toast) {
        if (!toast || toast.dataset.removing === 'true') return;
        toast.dataset.removing = 'true';
        toast.classList.add('todate-toast-leave');
        window.setTimeout(() => toast.remove(), 280);
    }

    function scheduleRemoval(toast, duration) {
        let timeoutId = null;
        let startedAt = Date.now();
        let remaining = duration;

        function startTimer() {
            startedAt = Date.now();
            timeoutId = window.setTimeout(() => removeToast(toast), remaining);
        }

        function pauseTimer() {
            if (!timeoutId) return;
            window.clearTimeout(timeoutId);
            timeoutId = null;
            remaining -= Date.now() - startedAt;
        }

        function resumeTimer() {
            if (toast.dataset.removing === 'true' || timeoutId || remaining <= 0) return;
            startTimer();
        }

        toast.addEventListener('mouseenter', pauseTimer);
        toast.addEventListener('mouseleave', resumeTimer);
        startTimer();
    }

    function showToast(type, message, duration = TOAST_DURATION) {
        if (!message) return null;

        const container = ensureToastContainer();
        const toast = document.createElement('div');
        toast.className = `todate-toast todate-toast-${type}`;
        toast.innerHTML = `
            <div class="todate-toast-icon">${iconForType(type)}</div>
            <div class="todate-toast-body">
                <div class="todate-toast-title">${titleForType(type)}</div>
                <div class="todate-toast-message"></div>
            </div>
            <button class="todate-toast-close" type="button" aria-label="Fechar notificação">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
            </button>
            <span class="todate-toast-progress"></span>
        `;

        toast.querySelector('.todate-toast-message').textContent = message;
        toast.querySelector('.todate-toast-progress').style.animationDuration = `${duration}ms`;
        toast.querySelector('.todate-toast-close').addEventListener('click', () => removeToast(toast));

        container.prepend(toast);
        scheduleRemoval(toast, duration);
        return toast;
    }

    function showByType(type, message, duration) {
        return showToast(type, message, duration);
    }

    function closeConfirm(callback, confirmed) {
        if (!confirmBackdrop) return;

        const modal = confirmBackdrop;
        confirmBackdrop = null;
        modal.classList.add('todate-confirm-hidden');

        window.setTimeout(() => {
            modal.remove();
            if (typeof callback === 'function') {
                callback(Boolean(confirmed));
            }
        }, 200);
    }

    function showConfirm(title, message, callback) {
        if (confirmBackdrop) {
            confirmBackdrop.remove();
            confirmBackdrop = null;
        }

        confirmBackdrop = document.createElement('div');
        confirmBackdrop.className = 'todate-confirm-backdrop';
        confirmBackdrop.innerHTML = `
            <div class="todate-confirm-modal" role="dialog" aria-modal="true" aria-labelledby="todateConfirmTitle">
                <h3 class="todate-confirm-title" id="todateConfirmTitle"></h3>
                <p class="todate-confirm-message"></p>
                <div class="todate-confirm-warning">Esta ação não poderá ser desfeita.</div>
                <div class="todate-confirm-actions">
                    <button type="button" class="btn btn-outline" data-action="cancel">Cancelar</button>
                    <button type="button" class="btn btn-primary" data-action="confirm">Confirmar</button>
                </div>
            </div>
        `;

        confirmBackdrop.querySelector('.todate-confirm-title').textContent = title || 'Confirmar ação';
        confirmBackdrop.querySelector('.todate-confirm-message').textContent = message || 'Deseja continuar?';

        const cancelBtn = confirmBackdrop.querySelector('[data-action="cancel"]');
        const confirmBtn = confirmBackdrop.querySelector('[data-action="confirm"]');

        cancelBtn.addEventListener('click', () => closeConfirm(callback, false));
        confirmBtn.addEventListener('click', () => closeConfirm(callback, true));
        confirmBackdrop.addEventListener('click', event => {
            if (event.target === confirmBackdrop) {
                closeConfirm(callback, false);
            }
        });

        const escHandler = event => {
            if (event.key === 'Escape' && confirmBackdrop) {
                document.removeEventListener('keydown', escHandler);
                closeConfirm(callback, false);
            }
        };

        document.addEventListener('keydown', escHandler);
        document.body.appendChild(confirmBackdrop);
    }

    function messageFor(type, fallbackIndex = 0) {
        return catalog[type]?.[fallbackIndex] || catalog.info[3];
    }

    function handleDemoToastClick(button) {
        const type = button.dataset.demoToast || 'info';
        const message = button.dataset.demoMessage || messageFor(type, 0);
        showByType(type, message);
    }

    function handleDemoConfirmClick(button) {
        const title = button.dataset.confirmTitle || 'Confirmar acao?';
        const message = button.dataset.confirmMessage || 'Deseja continuar?';
        const successMessage = button.dataset.confirmSuccess || catalog.success[7];
        const cancelMessage = button.dataset.confirmCancel || catalog.info[3];
        const cancelType = button.dataset.confirmCancelType || 'info';

        showConfirm(title, message, confirmed => {
            if (confirmed) {
                showSuccess(successMessage);
                return;
            }

            showByType(cancelType, cancelMessage);
        });
    }

    function bindDemoTriggers() {
        document.querySelectorAll('[data-demo-toast]').forEach(button => {
            button.addEventListener('click', () => handleDemoToastClick(button));
        });

        document.querySelectorAll('[data-demo-confirm]').forEach(button => {
            button.addEventListener('click', () => handleDemoConfirmClick(button));
        });
    }

    function bindLoginDemoForm(form) {
        form.addEventListener('submit', event => {
            event.preventDefault();
            const submitButton = form.querySelector('[type="submit"]');
            if (!submitButton) return;

            submitButton.textContent = 'Entrando...';
            submitButton.disabled = true;

            window.setTimeout(() => {
                submitButton.textContent = 'Entrar na conta';
                submitButton.disabled = false;
                showSuccess(form.dataset.successMessage || 'Login demonstrado com sucesso.');
            }, 1800);
        });
    }

    function bindRegisterDemoForm(form) {
        form.addEventListener('submit', event => {
            event.preventDefault();

            const passwordInput = document.getElementById('regPassword');
            const confirmInput = document.getElementById('regPasswordConfirm');
            const submitButton = form.querySelector('[type="submit"]');
            if (!passwordInput || !confirmInput || !submitButton) return;

            if (passwordInput.value !== confirmInput.value) {
                confirmInput.style.borderColor = 'var(--danger)';
                confirmInput.focus();
                showError(form.dataset.errorMessage || 'As senhas nao coincidem.');
                return;
            }

            confirmInput.style.borderColor = '';
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Criando conta...';
            submitButton.disabled = true;

            window.setTimeout(() => {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                showSuccess(form.dataset.successMessage || 'Conta demonstrada com sucesso.');
            }, 1800);
        });
    }

    function bindContactForm(form) {
        form.addEventListener('submit', event => {
            event.preventDefault();
            showSuccess(form.dataset.successMessage || 'Mensagem enviada com sucesso.');
            form.reset();
        });
    }

    function bindForms() {
        document.querySelectorAll('[data-notify-form]').forEach(form => {
            const mode = form.dataset.notifyForm;
            if (mode === 'login-demo') {
                bindLoginDemoForm(form);
                return;
            }

            if (mode === 'register-demo') {
                bindRegisterDemoForm(form);
            }
        });

        const contactForm = document.getElementById('contactForm');
        if (contactForm && !contactForm.dataset.notifyBound) {
            contactForm.dataset.notifyBound = 'true';
            bindContactForm(contactForm);
        }
    }

    function initNotifications() {
        bindDemoTriggers();
        bindForms();
    }

    function showSuccess(message) {
        return showToast('success', message || catalog.success[7]);
    }

    function showError(message) {
        return showToast('error', message || catalog.error[7]);
    }

    function showWarning(message) {
        return showToast('warning', message || catalog.warning[0]);
    }

    function showInfo(message) {
        return showToast('info', message || catalog.info[3]);
    }

    initNotifications();

    window.showSuccess = showSuccess;
    window.showError = showError;
    window.showWarning = showWarning;
    window.showInfo = showInfo;
    window.showConfirm = showConfirm;
    window.toDateNotificationCatalog = catalog;
})();