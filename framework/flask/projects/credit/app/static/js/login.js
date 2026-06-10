/* ==========================================
   CREDIFÁCIL - Login Page JavaScript
   ========================================== */

document.addEventListener("DOMContentLoaded", function () {

    // ============================
    // Toggle Senha
    // ============================

    const toggleSenha = document.querySelector(".toggle-senha");
    const senhaInput = document.getElementById("senha");

    if (toggleSenha && senhaInput) {

        toggleSenha.addEventListener("click", function () {

            const type =
                senhaInput.type === "password"
                    ? "text"
                    : "password";

            senhaInput.type = type;

            const svg = this.querySelector("svg");

            if (type === "text") {

                svg.innerHTML = `
                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94"/>
                    <path d="M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19"/>
                    <line x1="1" y1="1" x2="23" y2="23"/>
                    <path d="M14.12 14.12a3 3 0 1 1-4.24-4.24"/>
                `;

            } else {

                svg.innerHTML = `
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                    <circle cx="12" cy="12" r="3"/>
                `;

            }

        });

    }

    // ============================
    // Animação de Entrada da Página
    // ============================

    const fadeElements = document.querySelectorAll(".login-content > *");

    fadeElements.forEach((el, index) => {

        el.style.opacity = "0";
        el.style.transform = "translateY(20px)";
        el.style.transition =
            `opacity .5s ease ${index * .08}s,
             transform .5s ease ${index * .08}s`;

        setTimeout(() => {
            el.style.opacity = "1";
            el.style.transform = "translateY(0)";
        }, 100);

    });

    // ============================
    // ANIMAÇÕES DE ERRO
    // ============================

    const form = document.getElementById("loginForm");

    if (!form) return;

    const emailInput = document.getElementById("email");
    const senhaInput2 = document.getElementById("senha");
    const erroEmail = document.getElementById("erroEmail");
    const erroSenha = document.getElementById("erroSenha");
    const erroGeral = document.getElementById("erroGeral");
    const erroGeralTexto = document.getElementById("erroGeralTexto");

    if (!erroEmail || !erroSenha) return;

    const formGroupEmail = erroEmail.closest(".form-group");
    const formGroupSenha = erroSenha.closest(".form-group");

    /**
     * Anima o surgimento da mensagem de erro com slide + fade
     */
    function animarErroAparecer(el) {
        el.style.animation = "none";
        el.offsetHeight; // reflow
        el.style.animation = "erroSlideFade 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards";
    }

    /**
     * Anima o desaparecimento da mensagem de erro
     */
    function animarErroDesaparecer(el, callback) {
        el.style.animation = "none";
        el.offsetHeight;
        el.style.animation = "erroSlideOut 0.25s ease forwards";
        setTimeout(() => {
            if (callback) callback();
        }, 260);
    }

    /**
     * Tremor sutil no input com erro
     */
    function animarTremorInput(formGroup) {
        const wrapper = formGroup.querySelector(".input-wrapper");
        if (!wrapper) return;
        wrapper.style.animation = "none";
        wrapper.offsetHeight;
        wrapper.style.animation = "erroShake 0.4s ease";
    }

    /**
     * Exibe erro com animação
     */
    function mostrarErroInput(input, erroEl, formGroup, mensagem) {
        // Atualiza texto
        const span = erroEl.querySelector("span");
        if (span) span.textContent = mensagem;

        // Se já está visível, só atualiza texto sem re-animar
        if (erroEl.classList.contains("visivel")) return;

        erroEl.classList.add("visivel");
        formGroup.classList.add("erro");

        animarErroAparecer(erroEl);
        animarTremorInput(formGroup);
    }

    /**
     * Esconde erro com animação
     */
    function esconderErroInput(erroEl, formGroup) {
        if (!erroEl.classList.contains("visivel")) return;

        animarErroDesaparecer(erroEl, function () {
            erroEl.classList.remove("visivel");
            formGroup.classList.remove("erro");
        });
    }

    /**
     * Exibe erro geral com animação
     */
    function mostrarErroGeral(mensagem) {
        erroGeralTexto.textContent = mensagem;

        if (erroGeral.classList.contains("visivel")) return;

        erroGeral.classList.add("visivel");
        animarErroAparecer(erroGeral);
    }

    /**
     * Esconde erro geral com animação
     */
    function esconderErroGeral() {
        if (!erroGeral.classList.contains("visivel")) return;
        animarErroDesaparecer(erroGeral, function () {
            erroGeral.classList.remove("visivel");
        });
    }

    function limparErros() {
        esconderErroInput(erroEmail, formGroupEmail);
        esconderErroInput(erroSenha, formGroupSenha);
        esconderErroGeral();
    }

    function validarEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // ============================
    // Validação ao sair (blur)
    // ============================

    if (emailInput) {
        emailInput.addEventListener("blur", function () {
            const v = this.value.trim();
            if (v !== "" && !validarEmail(v)) {
                mostrarErroInput(this, erroEmail, formGroupEmail, "E-mail inválido.");
            } else if (v === "") {
                esconderErroInput(erroEmail, formGroupEmail);
            } else {
                esconderErroInput(erroEmail, formGroupEmail);
            }
        });
    }

    if (senhaInput2) {
        senhaInput2.addEventListener("blur", function () {
            const v = this.value.trim();
            if (v !== "" && v.length < 3) {
                mostrarErroInput(this, erroSenha, formGroupSenha, "A senha deve ter pelo menos 3 caracteres.");
            } else if (v === "") {
                esconderErroInput(erroSenha, formGroupSenha);
            } else {
                esconderErroInput(erroSenha, formGroupSenha);
            }
        });
    }

    // Limpar erro ao digitar
    if (emailInput) {
        emailInput.addEventListener("input", function () {
            esconderErroInput(erroEmail, formGroupEmail);
            esconderErroGeral();
        });
    }

    if (senhaInput2) {
        senhaInput2.addEventListener("input", function () {
            esconderErroInput(erroSenha, formGroupSenha);
            esconderErroGeral();
        });
    }

    // ============================
    // Validação no submit
    // ============================

    form.addEventListener("submit", function (e) {
        // Se não tiver novalidate, previne padrão também
        if (form.hasAttribute("novalidate")) {
            e.preventDefault();
        }

        limparErros();

        const email = emailInput ? emailInput.value.trim() : "";
        const senha = senhaInput2 ? senhaInput2.value.trim() : "";
        let valido = true;
        let primeiroErro = null;

        if (!email) {
            mostrarErroInput(emailInput, erroEmail, formGroupEmail, "E-mail é obrigatório.");
            valido = false;
            if (!primeiroErro) primeiroErro = emailInput;
        } else if (!validarEmail(email)) {
            mostrarErroInput(emailInput, erroEmail, formGroupEmail, "E-mail inválido.");
            valido = false;
            if (!primeiroErro) primeiroErro = emailInput;
        }

        if (!senha) {
            mostrarErroInput(senhaInput2, erroSenha, formGroupSenha, "Senha é obrigatória.");
            valido = false;
            if (!primeiroErro) primeiroErro = senhaInput2;
        } else if (senha.length < 3) {
            mostrarErroInput(senhaInput2, erroSenha, formGroupSenha, "A senha deve ter pelo menos 3 caracteres.");
            valido = false;
            if (!primeiroErro) primeiroErro = senhaInput2;
        }

        if (!valido) {
            mostrarErroGeral("Verifique os campos destacados abaixo.");
            if (primeiroErro) primeiroErro.focus();
            return;
        }

        // Válido — faz submit real
        form.submit();
    });

    // ============================
    // Animar erros que já vieram do backend
    // ============================

    document.querySelectorAll(".input-erro.visivel").forEach(function (el) {
        animarErroAparecer(el);
        const fg = el.closest(".form-group");
        if (fg) animarTremorInput(fg);
    });

    const erroGeralBackend = document.querySelector(".login-erro-geral.visivel");
    if (erroGeralBackend) {
        animarErroAparecer(erroGeralBackend);
    }

    // ============================
    // Botão de submit
    // ============================

    form.addEventListener("submit", function () {
        const btn = form.querySelector(".btn-login");
        if (btn && !btn.disabled) {
            btn.innerHTML = "Entrando...";
            btn.disabled = true;
        }
    });

});
