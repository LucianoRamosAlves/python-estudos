/* ==========================
   TowDate — Memories
   Premium interactions
========================== */

const SELECTORS = Object.freeze({
    page: '.memories-page',
    revealTargets: '.memories-stat-card, .memories-featured__card, .memories-grid-card',
    collectionCards: '.memories-collection-card',
    collectionTitle: '.memories-collection-card__title',
    memoryCards: '.memories-grid-card',
    memoryTitle: '.memories-grid-card__title'
});

document.addEventListener('DOMContentLoaded', bootstrapMemoriesPage);

function bootstrapMemoriesPage() {
    const reduceMotion = prefersReducedMotion();

    setPageMotionState(reduceMotion);
    initializeRevealAnimations(reduceMotion);
    initializeCollectionCards();
    initializeMemoryCards();
}

function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function setPageMotionState(reduceMotion) {
    if (reduceMotion) {
        return;
    }

    const page = document.querySelector(SELECTORS.page);
    page?.classList.add('is-motion-ready');
}

function initializeRevealAnimations(reduceMotion) {
    const elements = document.querySelectorAll(SELECTORS.revealTargets);

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

function initializeCollectionCards() {
    const cards = document.querySelectorAll(SELECTORS.collectionCards);

    cards.forEach((card) => {
        const title = getCardTitle(card, SELECTORS.collectionTitle);

        makeCardAccessible(card, `Coleção ${title}`, () => {
            openCollection(card.dataset.collection);
        });
    });
}

function initializeMemoryCards() {
    document.querySelectorAll(SELECTORS.memoryCards).forEach((card) => {
        const title = getCardTitle(card, SELECTORS.memoryTitle);

        makeCardAccessible(card, `Memória: ${title}`, () => {
            openMemory(title, card);
        });
    });
}

function getCardTitle(card, titleSelector) {
    return card.querySelector(titleSelector)?.textContent.trim() || '';
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

function openCollection(collection) {
    window.location.href = `/memorias/colecao/${collection}`;
}

function openMemory(title, card) {
    document.dispatchEvent(
        new CustomEvent('towdate:memory-open', {
            detail: { title, card }
        })
    );
}
