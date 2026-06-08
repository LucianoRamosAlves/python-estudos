/* ==========================================
   CREDIFÁCIL - Login Page JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // TOGGLE PASSWORD VISIBILITY
    // ==========================================

    const toggleSenha = document.querySelector('.toggle-senha');
    const senhaInput = document.getElementById('senha');

    if (toggleSenha && senhaInput) {
        toggleSenha.addEventListener('click', function() {
            const type = senhaInput.getAttribute('type') === 'password' ? 'text' : 'password';
            senhaInput.setAttribute('type', type);

            // Toggle icon
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
    }

    // ==========================================
    // FORM SUBMIT
    // ==========================================

    const loginForm = document.querySelector('.login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const btn = this.querySelector('.btn-login');
            const originalText = btn.innerHTML;

            btn.innerHTML = 'Entrando...';
            btn.disabled = true;

            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
                window.location.href = 'dashboard.html';
            }, 1500);
        });
    }

    // ==========================================
    // FADE IN ANIMATION
    // ==========================================

    const fadeElements = document.querySelectorAll('.login-content > *');

    fadeElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = `opacity 0.5s ease ${index * 0.08}s, transform 0.5s ease ${index * 0.08}s`;

        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, 100);
    });

});
