/**
 * Sticky Header Module
 * Enhances header with a 'scrolled' class on page scroll, with requestAnimationFrame throttling for maximum performance.
 */
(function() {
  function initStickyHeader() {
    const headerEl = document.querySelector('header');
    if (!headerEl) return;

    let scrolling = false;
    window.addEventListener('scroll', () => {
      if (!scrolling) {
        window.requestAnimationFrame(() => {
          if (window.scrollY > 40) {
            headerEl.classList.add('scrolled');
          } else {
            headerEl.classList.remove('scrolled');
          }
          scrolling = false;
        });
        scrolling = true;
      }
    }, { passive: true });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initStickyHeader);
  } else {
    initStickyHeader();
  }
})();
