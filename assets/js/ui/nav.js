export function initNavHighlight() {
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('header nav a').forEach(link => {
    try {
      const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
      if (linkPath === currentPath) link.classList.add('nav-active');
    } catch(e) {}
  });
}

export function initStickyHeader() {
  const headerEl = document.querySelector('header');
  if (headerEl) {
    let lastScroll = 0;
    window.addEventListener('scroll', () => {
      const scrollY = window.scrollY;
      if (scrollY > 40) headerEl.classList.add('scrolled');
      else headerEl.classList.remove('scrolled');
      lastScroll = scrollY;
    }, { passive: true });
  }
}

export function initFeatureBadges() {
  const trustBadge = document.querySelector('.trust-badge');
  if (trustBadge && !document.querySelector('.feature-badges')) {
    const badgesDiv = document.createElement('div');
    badgesDiv.className = 'feature-badges';
    badgesDiv.innerHTML = `
      <div class="feature-badge"><span class="badge-icon">⚡</span> Lightning Fast <span class="badge-dot"></span></div>
      <div class="feature-badge"><span class="badge-icon">🔒</span> 100% Private <span class="badge-dot"></span></div>
      <div class="feature-badge"><span class="badge-icon">♾️</span> Unlimited Files <span class="badge-dot"></span></div>
    `;
    trustBadge.insertAdjacentElement('afterend', badgesDiv);
  }
}
