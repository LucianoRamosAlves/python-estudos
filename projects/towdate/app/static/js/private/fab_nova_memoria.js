document.addEventListener('DOMContentLoaded', () => {
    const trigger = document.querySelector('[data-memory-fab-trigger]');
    const modal = document.querySelector('[data-memory-fab-modal]');
    const closeButtons = document.querySelectorAll('[data-memory-fab-close]');

    if (!trigger || !modal) return;

    const openModal = () => {
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
    };

    const closeModal = () => {
        modal.hidden = true;
        document.body.style.overflow = '';
    };

    trigger.addEventListener('click', openModal);
    closeButtons.forEach((button) => button.addEventListener('click', closeModal));

    modal.addEventListener('click', (event) => {
        if (event.target === modal) closeModal();
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && !modal.hidden) closeModal();
    });
});
