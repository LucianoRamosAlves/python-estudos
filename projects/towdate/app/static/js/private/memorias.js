/* ==========================
   TowDate — Memories
   Premium interactions
========================== */

document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const page = document.querySelector('.memories-page');

    if (!reduceMotion) {
        page?.classList.add('is-motion-ready');
    }

    initializeRevealAnimations(reduceMotion);
    initializeCollectionCards(reduceMotion);
    initializeMemoryCards();
});

function initializeRevealAnimations(reduceMotion) {
    const elements = document.querySelectorAll(
        '.memories-stat-card, .memories-featured__card, .memories-grid-card'
    );

    if (reduceMotion || !('IntersectionObserver' in window)) {
        elements.forEach((element) => element.classList.add('is-visible'));
        return;
    }

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            });
        },
        {
            threshold: 0.12,
            rootMargin: '0px 0px -36px'
        }
    );

    elements.forEach((element) => observer.observe(element));
}

function initializeCollectionCards(reduceMotion) {
    const cards = document.querySelectorAll('.memories-collection-card');
    const canTilt = window.matchMedia('(hover: hover) and (pointer: fine)');

    cards.forEach((card) => {
        const title = card.querySelector('.memories-collection-card__title')?.textContent.trim() || '';

        makeCardAccessible(card, `Coleção ${title}`, () => {
            openCollection(card.dataset.collection, card);
        });

        card.addEventListener('pointermove', (event) => {
            if (reduceMotion || !canTilt.matches) {
                return;
            }

            const bounds = card.getBoundingClientRect();
            const x = (event.clientX - bounds.left) / bounds.width;
            const y = (event.clientY - bounds.top) / bounds.height;

            card.style.setProperty('--pointer-x', `${x * 100}%`);
            card.style.setProperty('--pointer-y', `${y * 100}%`);
            card.style.setProperty('--tilt-x', `${(0.5 - y) * 5}deg`);
            card.style.setProperty('--tilt-y', `${(x - 0.5) * 7}deg`);
        });

        card.addEventListener('pointerleave', () => {
            card.style.setProperty('--tilt-x', '0deg');
            card.style.setProperty('--tilt-y', '0deg');
            card.style.setProperty('--pointer-x', '50%');
            card.style.setProperty('--pointer-y', '50%');
        });
    });
}

function initializeMemoryCards() {
    document.querySelectorAll('.memories-grid-card').forEach((card) => {
        const title = card.querySelector('.memories-grid-card__title')?.textContent.trim() || '';

        makeCardAccessible(card, `Memória: ${title}`, () => {
            openMemory(title, card);
        });
    });
}

function makeCardAccessible(card, label, activate) {
    card.tabIndex = 0;
    card.setAttribute('role', 'button');
    card.setAttribute('aria-label', label);

    card.addEventListener('click', (event) => {
        createRipple(card, event);
        activate();
    });

    card.addEventListener('keydown', (event) => {
        if (event.key !== 'Enter' && event.key !== ' ') {
            return;
        }

        event.preventDefault();
        createRipple(card);
        activate();
    });
}

function createRipple(card, event = null) {
    const bounds = card.getBoundingClientRect();
    const x = event?.clientX ? event.clientX - bounds.left : bounds.width / 2;
    const y = event?.clientY ? event.clientY - bounds.top : bounds.height / 2;
    const ripple = document.createElement('span');

    ripple.className = 'memories-ripple';
    ripple.style.setProperty('--ripple-x', `${x}px`);
    ripple.style.setProperty('--ripple-y', `${y}px`);
    card.appendChild(ripple);
    ripple.addEventListener('animationend', () => ripple.remove(), { once: true });
}

function openCollection(collection, card) {
    document.dispatchEvent(
        new CustomEvent('towdate:collection-open', {
            detail: {
                collection,
                count: Number(card.dataset.count || 0)
            }
        })
    );

    console.log(`Coleção selecionada: ${collection}`);
}

function openMemory(title, card) {
    document.dispatchEvent(
        new CustomEvent('towdate:memory-open', {
            detail: { title, card }
        })
    );

    console.log(`Memória selecionada: ${title}`);
}
