/* ==========================================
   CREDIFÁCIL - Meu Cartão Page JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // CARD DATA
    // ==========================================

    const userData = {
        nome: 'LUCAS RAMOS',
        numero: '5489 1234 5678 9012',
        validade: '12/28',
        cvv: '123',
        desde: '2024'
    };

    const cardTypes = {
        basico: {
            nome: 'Básico',
            bandeira: 'CrediFácil'
        },
        grafite: {
            nome: 'Grafite',
            bandeira: 'CrediFácil'
        },
        metalico: {
            nome: 'Metálico',
            bandeira: 'CrediFácil'
        }
    };

    // ==========================================
    // RENDER CARD - 3D FLIP
    // ==========================================

    function renderCard(tipo) {
        const card = cardTypes[tipo] || cardTypes.basico;
        const display = document.getElementById('cardDisplay');

        // Se já tem flip, não animar novamente
        display.classList.remove('flipped');

        // Small animation reset
        display.style.animation = 'none';
        void display.offsetHeight; // reflow
        display.style.animation = '';

        display.className = `card-display ${tipo}`;

        display.innerHTML = `
            <!-- FRENTE -->
            <div class="cd-face cd-front ${tipo}">
                <div class="cd-brilho" style="top:2rem;left:3rem;"></div>

                <div class="cd-chip">
                    <svg width="36" height="26" viewBox="0 0 36 26" fill="none">
                        <rect x="0.5" y="0.5" width="35" height="25" rx="3" fill="rgba(176,176,176,0.9)" stroke="rgba(255,255,255,0.15)"/>
                        <rect x="8" y="5" width="6" height="16" rx="1" fill="rgba(255,255,255,0.08)"/>
                        <rect x="16" y="5" width="14" height="16" rx="1" fill="rgba(255,255,255,0.05)"/>
                        <line x1="8" y1="13" x2="30" y2="13" stroke="rgba(255,255,255,0.1)" stroke-width="1"/>
                    </svg>
                </div>

                <div class="cd-contactless">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M6 8c0 2.5 2 4.5 4 4.5s4-2 4-4.5"/>
                        <path d="M2 6c0 4 3 7 6 7s6-3 6-7"/>
                        <path d="M18 10c0 2 1.5 4 3.5 4s3.5-2 3.5-4"/>
                    </svg>
                </div>

                <div class="cd-sinal">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
                <span class="cd-tipo-badge">${card.nome}</span>

                <div class="cd-numero">${userData.numero}</div>
                <div class="cd-info">
                    <div class="cd-info-item">
                        <span>Titular</span>
                        <span>${userData.nome}</span>
                    </div>
                    <div class="cd-info-item">
                        <span>Validade</span>
                        <span>${userData.validade}</span>
                    </div>
                    <span class="cd-bandeira">${card.bandeira}</span>
                </div>

                <span class="cd-flip-hint">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2"/>
                    </svg>
                    Passar o mouse para virar
                </span>
            </div>

            <!-- VERSO -->
            <div class="cd-face cd-back">
                <div class="cd-faixa"></div>

                <div class="cd-assinatura">
                    <div class="cd-codigo-wrapper">
                        <span class="cd-cvv-label">CVV</span>
                        <span class="cd-cvv">${userData.cvv}</span>
                    </div>
                    <span class="cd-assinatura-texto">${userData.nome}</span>
                </div>

                <div class="cd-back-seguranca">
                    Este cartão é de propriedade exclusiva do titular.
                    Em caso de perda ou roubo, ligue imediatamente para 0800 123 4567.
                </div>

                <div class="cd-back-info">
                    <div class="cd-back-item">
                        <span>Titular</span>
                        <span>${userData.nome}</span>
                    </div>
                    <div class="cd-back-item">
                        <span>Validade</span>
                        <span>${userData.validade}</span>
                    </div>
                    <span class="cd-back-bandeira">${card.bandeira}</span>
                </div>
            </div>
        `;

        // Update dados do titular (fora do cartão)
        document.getElementById('dadosTitular').textContent = userData.nome;
        document.getElementById('dadosNumero').textContent = userData.numero;
        document.getElementById('dadosValidade').textContent = userData.validade;
        document.getElementById('dadosCvv').textContent = userData.cvv;
    }

    // ==========================================
    // FLIP ON HOVER
    // ==========================================

    function setupFlip() {
        const cardDisplay = document.getElementById('cardDisplay');

        cardDisplay.addEventListener('mouseenter', function() {
            this.classList.add('flipped');
        });

        cardDisplay.addEventListener('mouseleave', function() {
            this.classList.remove('flipped');
        });
    }

    // ==========================================
    // BACKGROUND ANIMADO
    // ==========================================

    const bgParticulas = document.getElementById('bgParticulas');
    let partInterval = null;
    let currentBgType = 'basico';

    function criarParticula(tipo) {
        const part = document.createElement('div');
        part.className = `part part-${tipo}`;

        const size = tipo === 'metalico'
            ? Math.random() * 6 + 2
            : Math.random() * 4 + 1.5;

        part.style.width = `${size}px`;
        part.style.height = `${size}px`;
        part.style.left = `${Math.random() * 100}%`;
        part.style.animationDuration = `${Math.random() * 15 + 10}s`;
        part.style.animationDelay = `${Math.random() * 5}s`;

        if (tipo === 'grafite') {
            part.style.filter = 'blur(0.5px)';
        }

        if (tipo === 'metalico') {
            part.style.borderRadius = Math.random() > 0.5 ? '50%' : '2px';
        }

        return part;
    }

    function gerarParticulas(tipo, quantidade) {
        if (!bgParticulas) return;

        // Clear existing
        bgParticulas.innerHTML = '';

        for (let i = 0; i < quantidade; i++) {
            bgParticulas.appendChild(criarParticula(tipo));
        }
    }

    function mudarBackground(tipo) {
        if (tipo === currentBgType) return;
        currentBgType = tipo;

        const bg = document.getElementById('bgAnimado');
        if (!bg) return;

        // Remove all bg classes
        bg.classList.remove('bg-basico', 'bg-grafite', 'bg-metalico');
        // Force reflow
        void bg.offsetWidth;
        // Add new
        bg.classList.add(`bg-${tipo}`);

        // Different particle densities per card
        const quantidades = {
            basico: 25,
            grafite: 15,
            metalico: 40
        };

        gerarParticulas(tipo, quantidades[tipo] || 20);
    }

    // ==========================================
    // CARD SELECTOR
    // ==========================================

    const selectorBtns = document.querySelectorAll('.selector-btn');

    selectorBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            selectorBtns.forEach(b => b.classList.remove('ativo'));
            this.classList.add('ativo');
            renderCard(this.dataset.card);
            setupFlip();
            mudarBackground(this.dataset.card);
        });
    });

    // ==========================================
    // SIDEBAR TOGGLE (MOBILE)
    // ==========================================

    const toggleBtn = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');

            const spans = this.querySelectorAll('span');
            if (sidebar.classList.contains('mobile-open')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
            }
        });

        // Close sidebar on outside click
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024 &&
                sidebar.classList.contains('mobile-open') &&
                !sidebar.contains(e.target) &&
                !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
                toggleBtn.querySelectorAll('span').forEach(s => {
                    s.style.transform = '';
                    s.style.opacity = '';
                });
            }
        });
    }

    // ==========================================
    // INIT
    // ==========================================

    renderCard('basico');
    setupFlip();
    mudarBackground('basico');

});
