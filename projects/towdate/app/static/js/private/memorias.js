/* ==========================
   TowDate - Memories Page JS
========================== */

document.addEventListener('DOMContentLoaded', () => {
    initializeIntersectionObserver();
    initializeCollectionCards();
    initializeMemoryGridCards();
    initializeNetflixEffects();
    initializeRippleEffects();
});

/**
 * Initialize Intersection Observer for scroll animations
 */
function initializeIntersectionObserver() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe stat cards
    document.querySelectorAll('.memories-stat-card').forEach((card) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Observe grid cards
    document.querySelectorAll('.memories-grid-card').forEach((card) => {
        observer.observe(card);
    });
}

/**
 * Netflix-style effects for collection cards
 */
function initializeNetflixEffects() {
    const collectionCards = document.querySelectorAll('.memories-collection-card');

    collectionCards.forEach((card) => {
        card.addEventListener('mouseenter', function() {
            applyNetflixEffect(this);
        });

        card.addEventListener('mouseleave', function() {
            removeNetflixEffect(this);
        });

        // Mouse move for tilt effect
        card.addEventListener('mousemove', function(e) {
            if (window.innerWidth > 768) {
                const rect = this.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const centerX = rect.width / 2;
                const centerY = rect.height / 2;

                const rotateX = (y - centerY) / 10;
                const rotateY = (centerX - x) / 10;

                this.style.setProperty('--rotateX', rotateX + 'deg');
                this.style.setProperty('--rotateY', rotateY + 'deg');
                
                this.style.transform = `
                    perspective(1000px) 
                    rotateX(var(--rotateX, 0deg)) 
                    rotateY(var(--rotateY, 0deg))
                    scale(1.06)
                    translateY(-8px)
                `;
            }
        });
    });
}

/**
 * Apply Netflix hover effect
 */
function applyNetflixEffect(card) {
    const icon = card.querySelector('.memories-collection-card__icon');
    const title = card.querySelector('.memories-collection-card__title');
    const info = card.querySelector('.memories-collection-card__info');

    if (icon) {
        icon.style.animation = 'none';
        setTimeout(() => {
            icon.style.animation = 'bounceIn 0.4s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
        }, 10);
    }
}

/**
 * Remove Netflix effect
 */
function removeNetflixEffect(card) {
    if (window.innerWidth > 768) {
        card.style.transform = 'scale(1.06) translateY(-8px)';
    } else {
        card.style.transform = '';
    }
}

/**
 * Initialize collection card interactions
 */
function initializeCollectionCards() {
    const collectionCards = document.querySelectorAll('.memories-collection-card');

    collectionCards.forEach((card) => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            const collection = card.getAttribute('data-collection');
            handleCollectionClick(collection, card);
        });

        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                const collection = card.getAttribute('data-collection');
                handleCollectionClick(collection, card);
            }
        });

        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Coleção ${card.querySelector('.memories-collection-card__title')?.textContent || ''}`);
    });
}

/**
 * Handle collection card click
 */
function handleCollectionClick(collection, card) {
    card.style.animation = 'none';
    setTimeout(() => {
        card.style.animation = '';
    }, 10);
    
    console.log(`Coleção aberta: ${collection}`);
}

/**
 * Initialize memory grid card interactions
 */
function initializeMemoryGridCards() {
    const memoryCards = document.querySelectorAll('.memories-grid-card');

    memoryCards.forEach((card) => {
        card.addEventListener('click', (e) => {
            e.preventDefault();
            handleMemoryCardClick(card);
        });

        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleMemoryCardClick(card);
            }
        });

        card.setAttribute('tabindex', '0');
        card.setAttribute('role', 'button');
        card.setAttribute('aria-label', `Memória: ${card.querySelector('.memories-grid-card__title')?.textContent || ''}`);
    });
}

/**
 * Handle memory card click
 */
function handleMemoryCardClick(card) {
    const title = card.querySelector('.memories-grid-card__title').textContent;
    console.log(`Memória aberta: ${title}`);
}

/**
 * Initialize ripple effect on cards
 */
function initializeRippleEffects() {
    const interactiveCards = document.querySelectorAll(
        '.memories-collection-card, .memories-grid-card, .memories-stat-card'
    );

    interactiveCards.forEach((card) => {
        card.addEventListener('click', function(e) {
            createRipple(e, this);
        });
    });
}

/**
 * Create ripple effect on click
 */
function createRipple(e, card) {
    const ripple = document.createElement('span');
    const rect = card.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = e.clientX - rect.left - size / 2;
    const y = e.clientY - rect.top - size / 2;

    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.classList.add('ripple');

    card.appendChild(ripple);
    
    ripple.style.position = 'absolute';
    ripple.style.background = 'rgba(200, 168, 95, 0.5)';
    ripple.style.borderRadius = '50%';
    ripple.style.pointerEvents = 'none';
    ripple.style.animation = 'rippleEffect 0.6s ease-out';

    ripple.addEventListener('animationend', () => {
        ripple.remove();
    });
}

/**
 * Add CSS animations
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes bounceIn {
        0% { transform: scale(0.8); opacity: 0; }
        50% { transform: scale(1.1); }
        100% { transform: scale(1); opacity: 1; }
    }

    @keyframes rippleEffect {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }

    .memories-collection-card:hover {
        z-index: 10;
    }
`;
document.head.appendChild(style);

console.log('Página de memórias iniciada com sucesso ✨');


