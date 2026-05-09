export function initScrollReveal() {
  document.querySelectorAll('.related-tools, .seo-article').forEach(el => {
    el.classList.add('scroll-reveal');
  });
  if ('IntersectionObserver' in window) {
    const revealObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          revealObserver.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    document.querySelectorAll('.scroll-reveal').forEach(el => revealObserver.observe(el));
  } else {
    document.querySelectorAll('.scroll-reveal').forEach(el => el.classList.add('in-view'));
  }
}
