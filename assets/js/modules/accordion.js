/**
 * Accordion Components Module
 * Manages transition controls for FAQ accordion items and mobile drawer navigation categories.
 */
(function() {
  function initAccordions() {
    // ── Drawer Accordion Transition Controls ──
    const accordionBtns = document.querySelectorAll('.drawer-accordion-btn');
    accordionBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const isExpanded = btn.getAttribute('aria-expanded') === 'true';
        const content = btn.nextElementSibling;
        btn.setAttribute('aria-expanded', !isExpanded);
        
        if (content) {
          if (!isExpanded) {
            content.style.maxHeight = content.scrollHeight + 'px';
          } else {
            content.style.maxHeight = '0px';
          }
        }
      });
    });

    // ── UI Enhancement: FAQ Accordion ──
    document.querySelectorAll('.faq-item').forEach((item, i) => {
      const question = item.querySelector('.faq-question');
      if (!question) return;
      
      // Open first FAQ item by default
      if (i === 0) {
        item.classList.add('open');
      }
      
      question.addEventListener('click', () => {
        item.classList.toggle('open');
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAccordions);
  } else {
    initAccordions();
  }
})();
