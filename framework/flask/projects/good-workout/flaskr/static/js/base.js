document.addEventListener('DOMContentLoaded', () => {

    // =========================
    // MOBILE MENU
    // =========================
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const mobileMenu = document.querySelector('.mobile-menu');
    const mobileMenuOverlay = document.querySelector('.mobile-menu-overlay');
    const mobileMenuClose = document.querySelector('.mobile-menu-close');
    const mobileNavLinks = document.querySelectorAll('.mobile-nav-links a');

    function toggleMobileMenu() {
        if (!mobileMenuBtn || !mobileMenu || !mobileMenuOverlay) return;

        mobileMenuBtn.classList.toggle('active');
        mobileMenu.classList.toggle('open');
        mobileMenuOverlay.classList.toggle('open');
        document.body.classList.toggle('menu-open');
    }

    if (mobileMenuBtn) mobileMenuBtn.addEventListener('click', toggleMobileMenu);
    if (mobileMenuClose) mobileMenuClose.addEventListener('click', toggleMobileMenu);
    if (mobileMenuOverlay) mobileMenuOverlay.addEventListener('click', toggleMobileMenu);

    mobileNavLinks.forEach(link => {
        link.addEventListener('click', toggleMobileMenu);
    });


    // =========================
    // NAV LINK ATIVO
    // =========================
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-links a');

    if (sections.length && navLinks.length) {
        window.addEventListener('scroll', () => {
            let current = '';

            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                if (window.scrollY >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });

            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href')?.slice(1) === current) {
                    link.classList.add('active');
                }
            });
        });
    }


    // =========================
    // NAV SCROLL EFFECT
    // =========================
    const nav = document.querySelector('.nav');

    if (nav) {
        window.addEventListener('scroll', () => {
            nav.classList.toggle('scrolled', window.scrollY > 50);
        });
    }


    // =========================
    // SLIDER
    // =========================
    const testimonialTrack = document.querySelector('.testimonials-track');
    const testimonialItems = document.querySelectorAll('.testimonial-item');
    const dots = document.querySelectorAll('.testimonial-dots .dot');
    const prevBtn = document.querySelector('.testimonial-arrow.prev');
    const nextBtn = document.querySelector('.testimonial-arrow.next');

    let currentSlide = 0;

    function updateSlider() {
        if (!testimonialTrack) return;

        testimonialTrack.style.transform = `translateX(-${currentSlide * 100}%)`;

        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }

    if (prevBtn && nextBtn && testimonialItems.length) {
        prevBtn.addEventListener('click', () => {
            currentSlide = (currentSlide - 1 + testimonialItems.length) % testimonialItems.length;
            updateSlider();
        });

        nextBtn.addEventListener('click', () => {
            currentSlide = (currentSlide + 1) % testimonialItems.length;
            updateSlider();
        });

        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                currentSlide = index;
                updateSlider();
            });
        });

        setInterval(() => {
            currentSlide = (currentSlide + 1) % testimonialItems.length;
            updateSlider();
        }, 8000);
    }


    // =========================
    // BOTÃO PRODUTO
    // =========================
    const productBtns = document.querySelectorAll('.product-btn');

    productBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            const originalText = btn.textContent;
            btn.textContent = '✓';

            btn.style.background = 'var(--success)';
            btn.style.borderColor = 'var(--success)';
            btn.style.color = 'white';

            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.style.borderColor = '';
                btn.style.color = '';
            }, 2000);
        });
    });


    // =========================
    // SMOOTH SCROLL
    // =========================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });


    // =========================
    // ANIMAÇÃO SCROLL
    // =========================
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.fade-in-up').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = '0.8s';

        observer.observe(el);
    });

});