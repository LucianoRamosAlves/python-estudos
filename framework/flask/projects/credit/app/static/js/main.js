/* ==========================================
   CREDIFÁCIL - Main JavaScript
   ========================================== */

document.addEventListener('DOMContentLoaded', function() {

    // ==========================================
    // HEADER SCROLL EFFECT
    // ==========================================

    const header = document.querySelector('header');
    let lastScroll = 0;

    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }

        lastScroll = currentScroll;
    });

    // ==========================================
    // MOBILE MENU
    // ==========================================

    const menuBtn = document.querySelector('.menu-mobile-btn');
    const nav = document.querySelector('nav');

    menuBtn.addEventListener('click', function() {
        nav.classList.toggle('mobile-open');
        this.classList.toggle('active');

        if (this.classList.contains('active')) {
            this.querySelectorAll('span').forEach((span, i) => {
                if (i === 0) span.style.transform = 'rotate(45deg) translate(5px, 5px)';
                if (i === 1) span.style.opacity = '0';
                if (i === 2) span.style.transform = 'rotate(-45deg) translate(5px, -5px)';
            });
        } else {
            this.querySelectorAll('span').forEach(span => {
                span.style.transform = '';
                span.style.opacity = '';
            });
        }
    });

    // Close menu on link click
    nav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', function() {
            nav.classList.remove('mobile-open');
            menuBtn.classList.remove('active');
            menuBtn.querySelectorAll('span').forEach(span => {
                span.style.transform = '';
                span.style.opacity = '';
            });
        });
    });

    // ==========================================
    // ACTIVE NAV LINK ON SCROLL
    // ==========================================

    const sections = document.querySelectorAll('section, main.hero');
    const navLinks = document.querySelectorAll('nav a');

    window.addEventListener('scroll', function() {
        let current = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop - 200;
            const sectionHeight = section.clientHeight;

            if (pageYOffset >= sectionTop && pageYOffset < sectionTop + sectionHeight) {
                current = section.getAttribute('id') || 'inicio';
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('ativo');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('ativo');
            }
        });
    });

    // ==========================================
    // ANIMATED COUNTERS
    // ==========================================

    function animateCounters() {
        const counters = document.querySelectorAll('.stat-numero');

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-target'));
            const duration = 2000;
            const step = Math.ceil(target / (duration / 16));
            let current = 0;

            const updateCounter = () => {
                current += step;
                if (current < target) {
                    counter.textContent = current;
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            updateCounter();
        });
    }

    // Trigger counters when hero stats are visible
    const heroStats = document.querySelector('.hero-stats');
    let countersAnimated = false;

    const observerOptions = {
        threshold: 0.3,
        rootMargin: '0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !countersAnimated) {
                animateCounters();
                countersAnimated = true;
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    if (heroStats) {
        observer.observe(heroStats);
    }

    // ==========================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ==========================================

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));

            if (target) {
                const headerHeight = header.offsetHeight;
                const targetPosition = target.offsetTop - headerHeight;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ==========================================
    // PARALLAX EFFECT ON HERO CARD
    // ==========================================

    const heroCard = document.querySelector('.hero-card');

    if (heroCard) {
        document.querySelector('.hero-visual').addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / centerY * -5;
            const rotateY = (x - centerX) / centerX * 5;

            heroCard.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });

        document.querySelector('.hero-visual').addEventListener('mouseleave', function() {
            heroCard.style.transform = 'perspective(1000px) rotateY(-5deg) rotateX(5deg)';
        });
    }

    // ==========================================
    // FADE IN ANIMATIONS ON SCROLL
    // ==========================================

    const animateElements = document.querySelectorAll('.solucao-card, .sobre-container, .cartao-card, .section-header');

    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animateElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(el);
    });

    // ==========================================
    // CARTÕES CARDS STAGGER ANIMATION
    // ==========================================

    const cartaoCards = document.querySelectorAll('.cartao-card');

    cartaoCards.forEach((card, index) => {
        card.style.transitionDelay = `${index * 0.1}s`;
    });

});
