export function initFaqAccordion() {
  document.querySelectorAll('.faq-item').forEach((item, i) => {
    const question = item.querySelector('.faq-question');
    if (!question) return;
    // Open first item by default
    if (i === 0) item.classList.add('open');
    
    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');
      // Close all others
      document.querySelectorAll('.faq-item').forEach(el => el.classList.remove('open'));
      if (!isOpen) {
        item.classList.add('open');
      }
    });
  });
}
