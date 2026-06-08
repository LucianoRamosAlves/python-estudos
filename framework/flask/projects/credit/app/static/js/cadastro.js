/* ==========================================
   CREDIFÁCIL - Cadastro Page JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // TOGGLE PASSWORD VISIBILITY
    // ==========================================

    document.querySelectorAll('.toggle-senha').forEach(btn => {
        btn.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const input = document.getElementById(targetId);

            if (!input) return;

            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);

            const svg = this.querySelector('svg');
            if (type === 'text') {
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
    });

    // ==========================================
    // INPUT MASKS
    // ==========================================

    // CPF mask
    const cpfInput = document.getElementById('cpf');
    if (cpfInput) {
        cpfInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);

            if (value.length > 9) {
                value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
            } else if (value.length > 6) {
                value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
            } else if (value.length > 3) {
                value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2');
            }

            this.value = value;
        });
    }

    // Telefone mask
    const telInput = document.getElementById('telefone');
    if (telInput) {
        telInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);

            if (value.length > 7) {
                value = value.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/(\d{2})(\d{1,5})/, '($1) $2');
            } else if (value.length > 0) {
                value = value.replace(/(\d{1,2})/, '($1');
            }

            this.value = value;
        });
    }

    // Data mask
    const dataInput = document.getElementById('nascimento');
    if (dataInput) {
        dataInput.addEventListener('input', function() {
            let value = this.value.replace(/\D/g, '');
            if (value.length > 8) value = value.slice(0, 8);

            if (value.length > 4) {
                value = value.replace(/(\d{2})(\d{2})(\d{1,4})/, '$1/$2/$3');
            } else if (value.length > 2) {
                value = value.replace(/(\d{2})(\d{1,2})/, '$1/$2');
            }

            this.value = value;
        });
    }

    // ==========================================
    // PASSWORD STRENGTH
    // ==========================================

    const senhaInput = document.getElementById('senha');
    const strengthItems = document.querySelectorAll('.strength-item');

    if (senhaInput && strengthItems.length) {
        senhaInput.addEventListener('input', function() {
            const value = this.value;
            let strength = 0;

            // Reset
            strengthItems.forEach(item => {
                item.className = 'strength-item';
            });

            if (value.length === 0) return;

            // Length check
            if (value.length >= 8) strength++;
            if (value.length >= 12) strength++;

            // Has number
            if (/\d/.test(value)) strength++;

            // Has special char or uppercase
            if (/[!@#$%^&*(),.?":{}|<>]/.test(value) || /[A-Z]/.test(value)) strength++;

            // Apply classes
            const levels = ['active-weak', 'active-medium', 'active-strong'];
            for (let i = 0; i < Math.min(strength, 4); i++) {
                if (i < 2) strengthItems[i].classList.add('active-weak');
                else if (i < 3) strengthItems[i].classList.add('active-medium');
                else strengthItems[i].classList.add('active-strong');
            }
        });
    }

    // ==========================================
    // PASSWORD CONFIRMATION
    // ==========================================

    const confirmSenha = document.getElementById('confirmar-senha');

    if (senhaInput && confirmSenha) {
        confirmSenha.addEventListener('input', function() {
            if (this.value.length === 0) {
                this.style.borderColor = '';
                return;
            }

            if (this.value === senhaInput.value) {
                this.style.borderColor = '#4caf50';
            } else {
                this.style.borderColor = '#f44336';
            }
        });

        senhaInput.addEventListener('input', function() {
            if (confirmSenha.value.length > 0) {
                if (confirmSenha.value === this.value) {
                    confirmSenha.style.borderColor = '#4caf50';
                } else {
                    confirmSenha.style.borderColor = '#f44336';
                }
            }
        });
    }

    // ==========================================
    // FORM SUBMIT
    // ==========================================

    const cadForm = document.querySelector('.cad-form');

    if (cadForm) {
        cadForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const senha = document.getElementById('senha').value;
            const confirmar = document.getElementById('confirmar-senha').value;

            if (senha !== confirmar) {
                alert('As senhas não conferem. Por favor, verifique.');
                return;
            }

            if (senha.length < 8) {
                alert('A senha deve ter no mínimo 8 caracteres.');
                return;
            }

            // Get selected card
            const cartaoSelecionado = document.querySelector('input[name="tipo-cartao"]:checked');
            const tipoCartao = cartaoSelecionado ? cartaoSelecionado.value : 'basico';

            console.log('Cartão selecionado:', tipoCartao);

            const btn = this.querySelector('.btn-cadastro');
            const originalText = btn.innerHTML;

            const nomes = { basico: 'Básico', grafite: 'Grafite', metalico: 'Metálico' };
            btn.innerHTML = `Criando conta ${nomes[tipoCartao] || ''}...`;
            btn.disabled = true;

            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                window.location.href = 'login.html';
            }, 2000);
        });
    }

    // ==========================================
    // FADE IN ANIMATION
    // ==========================================

    const fadeElements = document.querySelectorAll('.cad-content > *');

    fadeElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.5s ease ${index * 0.06}s, transform 0.5s ease ${index * 0.06}s`;

        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100);
    });

});
