document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-goal-progress-range]').forEach((input) => {
        input.addEventListener('input', () => {
            const value = input.value;
            const label = input.closest('.goal-progress-form__controls')?.previousElementSibling;
            if (label) {
                label.textContent = `Atualizar progresso (${value}%)`;
            }
        });
    });
});
