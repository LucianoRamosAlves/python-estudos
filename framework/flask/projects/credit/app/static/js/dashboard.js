/* ==========================================
   CREDIFÁCIL - Dashboard JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // DADOS DA CONTA (único)
    // ==========================================

    const dados = {
        saldo: 4582.90,
        limite: 'R$ 3.000,00',
        fatura: 1234.56,
        vencimento: '15/04/2025',
        cashback: 45.80
    };

    function carregarDashboard() {
        const data = dados;

        // Saldo com animação de contagem
        const saldoEl = document.getElementById('saldoNumero');
        saldoEl.textContent = data.saldo.toFixed(2).replace('.', ',');
        saldoEl.classList.add('contando');
        setTimeout(() => saldoEl.classList.remove('contando'), 300);

        // Limite
        document.getElementById('infoLimite').textContent = data.limite;

        // Fatura
        const faturaFormatada = data.fatura.toFixed(2).replace('.', ',');
        document.getElementById('infoFatura').textContent = `R$ ${faturaFormatada}`;

        // Barra de progresso
        const limiteNum = parseFloat(data.limite.replace('R$ ', '').replace('.', '').replace(',', '.'));
        const percentual = Math.min((data.fatura / limiteNum) * 100, 100);

        // Animação da barra
        setTimeout(() => {
            document.getElementById('infoBarFill').style.width = `${percentual}%`;
            document.getElementById('infoBarLabel').textContent = `${Math.round(percentual)}% do limite`;
        }, 200);

        // Vencimento
        document.getElementById('infoVencimento').textContent = data.vencimento;

        // Cashback
        const cashbackFormatado = data.cashback.toFixed(2).replace('.', ',');
        document.getElementById('infoCashback').textContent = `R$ ${cashbackFormatado}`;
    }

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

    carregarDashboard();

});
