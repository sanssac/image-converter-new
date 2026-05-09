export function initFooterBranding() {
  const footerEl = document.querySelector('footer');
  if (footerEl && !footerEl.querySelector('.footer-brand')) {
    const brand = document.createElement('div');
    brand.className = 'footer-brand';
    brand.innerHTML = `
      <div class="footer-logo"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>
      <div class="footer-name">Image <span>Converter</span></div>
    `;
    footerEl.insertBefore(brand, footerEl.firstChild);
  }
}
