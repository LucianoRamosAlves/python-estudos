document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    if (!registerForm) {
        return;
    }

    const submitButton = document.getElementById('regSubmitBtn');
    const planLabels = {
        free: 'Criar conta gratuita',
        basic: 'Criar conta Basic',
        premium: 'Criar conta Premium'
    };

    if (submitButton) {
        const selected = document.querySelector('input[name="plan"]:checked');
        if (selected) {
            submitButton.textContent = planLabels[selected.value] || 'Criar conta e continuar';
        }

        document.querySelectorAll('input[name="plan"]').forEach((radio) => {
            radio.addEventListener('change', () => {
                submitButton.textContent = planLabels[radio.value] || 'Criar conta e continuar';
            });
        });
    }

    const formWrap = document.querySelector('.reg-form-wrap');
    if (formWrap) {
        document.querySelectorAll('.reg-plan-item').forEach((item) => {
            item.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    window.setTimeout(() => {
                        formWrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }, 200);
                }
            });
        });
    }

    function makePasswordToggle(toggleId, inputId, iconId) {
        const toggle = document.getElementById(toggleId);
        const input = document.getElementById(inputId);
        const icon = document.getElementById(iconId);

        if (!toggle || !input || !icon) {
            return;
        }

        const eyeOpen = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
        const eyeClosed = '<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';

        toggle.addEventListener('click', () => {
            const hidden = input.type === 'password';
            input.type = hidden ? 'text' : 'password';
            icon.innerHTML = hidden ? eyeClosed : eyeOpen;
        });
    }

    makePasswordToggle('pwToggle1', 'regPassword', 'eyeIcon1');
    makePasswordToggle('pwToggle2', 'regPasswordConfirm', 'eyeIcon2');

    const passwordInput = document.getElementById('regPassword');
    const passwordStrength = document.getElementById('pwStrength');
    const strengthBars = ['bar1', 'bar2', 'bar3', 'bar4'].map((id) => document.getElementById(id));
    const strengthLabel = document.getElementById('strengthLabel');

    if (!passwordInput || !passwordStrength || !strengthLabel || strengthBars.some((bar) => !bar)) {
        return;
    }

    passwordInput.addEventListener('input', () => {
        const value = passwordInput.value;
        if (!value) {
            passwordStrength.style.display = 'none';
            return;
        }

        passwordStrength.style.display = 'flex';
        let score = 0;

        if (value.length >= 8) score += 1;
        if (value.length >= 12) score += 1;
        if (/[A-Z]/.test(value) && /[a-z]/.test(value)) score += 1;
        if (/[0-9]/.test(value) && /[^A-Za-z0-9]/.test(value)) score += 1;

        const barClasses = ['', 'active-weak', 'active-fair', 'active-strong', 'active-strong'];
        const labels = ['', 'Fraca', 'Regular', 'Boa', 'Forte'];

        strengthBars.forEach((bar, index) => {
            bar.className = 'pw-strength-bar';
            if (index < score) {
                bar.classList.add(barClasses[score]);
            }
        });

        strengthLabel.textContent = labels[score] || '';
    });
});