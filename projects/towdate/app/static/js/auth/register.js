        // Nav scroll
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) document.getElementById('navbar').classList.add('scrolled');
        });

        // Mobile menu
        const mobileMenuBtn     = document.getElementById('mobileMenuBtn');
        const mobileMenu        = document.getElementById('mobileMenu');
        const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
        const mobileMenuClose   = document.getElementById('mobileMenuClose');

        function openMenu()  { mobileMenu.classList.add('open'); mobileMenuOverlay.classList.add('open'); mobileMenuBtn.classList.add('active'); document.body.classList.add('menu-open'); }
        function closeMenu() { mobileMenu.classList.remove('open'); mobileMenuOverlay.classList.remove('open'); mobileMenuBtn.classList.remove('active'); document.body.classList.remove('menu-open'); }

        mobileMenuBtn.addEventListener('click', openMenu);
        mobileMenuClose.addEventListener('click', closeMenu);
        mobileMenuOverlay.addEventListener('click', closeMenu);
        document.addEventListener('keydown', e => { if (e.key === 'Escape') closeMenu(); });

        // Update submit button when plan changes
        const planLabels = { free: 'Criar conta gratuita', basic: 'Criar conta Basic', premium: 'Criar conta Premium e continuar' };
        document.querySelectorAll('input[name="plan"]').forEach(r => {
            r.addEventListener('change', () => {
                document.getElementById('regSubmitBtn').textContent = planLabels[r.value] || 'Criar conta e continuar';
            });
        });

        // Scroll to form on mobile after plan selection
        document.querySelectorAll('.reg-plan-item').forEach(item => {
            item.addEventListener('click', () => {
                if (window.innerWidth < 992) {
                    setTimeout(() => document.querySelector('.reg-form-wrap').scrollIntoView({ behavior: 'smooth', block: 'start' }), 200);
                }
            });
        });

        // Password toggles
        function makePwToggle(toggleId, inputId, iconId) {
            const toggle = document.getElementById(toggleId);
            const input  = document.getElementById(inputId);
            const icon   = document.getElementById(iconId);
            const eyeOpen   = `<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>`;
            const eyeClosed = `<path d="M17.94 17.94A10.07 10.07 0 0112 20c-7 0-11-8-11-8a18.45 18.45 0 015.06-5.94M9.9 4.24A9.12 9.12 0 0112 4c7 0 11 8 11 8a18.5 18.5 0 01-2.16 3.19m-6.72-1.07a3 3 0 11-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>`;
            toggle.addEventListener('click', () => {
                const hidden = input.type === 'password';
                input.type = hidden ? 'text' : 'password';
                icon.innerHTML = hidden ? eyeClosed : eyeOpen;
            });
        }

        makePwToggle('pwToggle1', 'regPassword', 'eyeIcon1');
        makePwToggle('pwToggle2', 'regPasswordConfirm', 'eyeIcon2');

        // Password strength
        const pwInput     = document.getElementById('regPassword');
        const pwStrength  = document.getElementById('pwStrength');
        const bars        = ['bar1','bar2','bar3','bar4'].map(id => document.getElementById(id));
        const strengthLbl = document.getElementById('strengthLabel');

        pwInput.addEventListener('input', () => {
            const v = pwInput.value;
            if (!v) { pwStrength.style.display = 'none'; return; }
            pwStrength.style.display = 'flex';
            let s = 0;
            if (v.length >= 8) s++;
            if (v.length >= 12) s++;
            if (/[A-Z]/.test(v) && /[a-z]/.test(v)) s++;
            if (/[0-9]/.test(v) && /[^A-Za-z0-9]/.test(v)) s++;
            const cls = ['','active-weak','active-fair','active-strong','active-strong'];
            const lbl = ['','Fraca','Regular','Boa','Forte'];
            bars.forEach((b, i) => { b.className = 'pw-strength-bar'; if (i < s) b.classList.add(cls[s]); });
            strengthLbl.textContent = lbl[s] || '';
        });