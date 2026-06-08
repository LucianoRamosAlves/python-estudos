/* ==========================================
   CREDIFÁCIL - Suporte JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // FAQ Accordion
    var perguntas = document.querySelectorAll('.faq-pergunta');

    for (var i = 0; i < perguntas.length; i++) {
        perguntas[i].addEventListener('click', function() {
            var item = this.parentNode;
            var isOpen = item.classList.contains('ativo');

            // Fecha todos
            var todos = document.querySelectorAll('.faq-item');
            for (var j = 0; j < todos.length; j++) {
                todos[j].classList.remove('ativo');
            }

            // Abre se estava fechado
            if (!isOpen) {
                item.classList.add('ativo');
            }
        });
    }

    // Sidebar toggle mobile
    var toggleBtn = document.querySelector('.sidebar-toggle');
    var sidebar = document.querySelector('.sidebar');

    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', function() {
            sidebar.classList.toggle('mobile-open');

            var spans = this.querySelectorAll('span');
            if (sidebar.classList.contains('mobile-open')) {
                spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
                spans[1].style.opacity = '0';
                spans[2].style.transform = 'rotate(-45deg) translate(5px, -5px)';
            } else {
                for (var k = 0; k < spans.length; k++) {
                    spans[k].style.transform = '';
                    spans[k].style.opacity = '';
                }
            }
        });

        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024 &&
                sidebar.classList.contains('mobile-open') &&
                !sidebar.contains(e.target) &&
                !toggleBtn.contains(e.target)) {
                sidebar.classList.remove('mobile-open');
                var spans = toggleBtn.querySelectorAll('span');
                for (var k = 0; k < spans.length; k++) {
                    spans[k].style.transform = '';
                    spans[k].style.opacity = '';
                }
            }
        });
    }

});
