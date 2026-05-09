export function initMegaMenu() {
  const navContainer = document.querySelector('header nav');
  const currentDocLang = document.documentElement.lang || 'en';

  if (navContainer && !document.querySelector('.mega-menu-wrapper')) {
    const megaWrapper = document.createElement('div');
    megaWrapper.className = 'mega-menu-wrapper';
    const langPrefix = currentDocLang === 'en' ? '' : `/${currentDocLang}`;

    megaWrapper.innerHTML = `
      <button class="mega-btn" aria-expanded="false">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect></svg>
        All Tools
        <svg class="mega-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
      </button>
    `;
    navContainer.insertBefore(megaWrapper, navContainer.firstChild);

    const megaDropdown = document.createElement('div');
    megaDropdown.className = 'mega-dropdown';
    megaDropdown.innerHTML = `
        <div class="mega-grid">
          <div class="mega-column">
            <h4>Popular Converters</h4>
            <a href="${langPrefix}/" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">Multi-Format</span><span class="mega-link-desc">Any format to any format</span></div>
            </a>
            <a href="${langPrefix}/jpg-to-png" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">JPG → PNG</span><span class="mega-link-desc">Lossless with transparency</span></div>
            </a>
            <a href="${langPrefix}/png-to-jpg" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">PNG → JPG</span><span class="mega-link-desc">Smaller file size</span></div>
            </a>
            <a href="${langPrefix}/webp-to-jpg" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">WebP → JPG</span><span class="mega-link-desc">Universal compatibility</span></div>
            </a>
            <a href="${langPrefix}/jpeg-to-webp" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">JPEG → WebP</span><span class="mega-link-desc">Modern web format</span></div>
            </a>
          </div>
          <div class="mega-column">
            <h4>Advanced Formats</h4>
            <a href="${langPrefix}/svg-to-png" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">SVG → PNG</span><span class="mega-link-desc">Rasterize vectors</span></div>
            </a>
            <a href="${langPrefix}/svg-to-jpg" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">SVG → JPG</span><span class="mega-link-desc">Vector to photo format</span></div>
            </a>
            <a href="${langPrefix}/heic-to-jpg" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">HEIC → JPG</span><span class="mega-link-desc">iPhone photos support</span></div>
            </a>
            <a href="${langPrefix}/png-to-ico" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M7 7h10v10H7z"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">PNG → ICO</span><span class="mega-link-desc">Favicon generator</span></div>
            </a>
            <a href="${langPrefix}/webp-to-png" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">WebP → PNG</span><span class="mega-link-desc">Lossless from WebP</span></div>
            </a>
          </div>
          <div class="mega-column">
            <h4>Next-Gen Formats</h4>
            <a href="${langPrefix}/jpg-to-avif" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">JPG → AVIF</span><span class="mega-link-desc">Ultra-small files</span></div>
            </a>
            <a href="${langPrefix}/png-to-avif" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">PNG → AVIF</span><span class="mega-link-desc">Next-gen compression</span></div>
            </a>
          </div>
          <div class="mega-column">
            <h4>Compress & Filters</h4>
            <a href="${langPrefix}/compress-image" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">Smart Compress</span><span class="mega-link-desc">Auto quality optimizer</span></div>
            </a>
            <a href="${langPrefix}/compress-image-to-50kb" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="M8 17l4 4 4-4"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">To 50KB</span><span class="mega-link-desc">For forms & uploads</span></div>
            </a>
            <a href="${langPrefix}/compress-image-to-100kb" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="M8 17l4 4 4-4"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">To 100KB</span><span class="mega-link-desc">Web-optimized size</span></div>
            </a>
            <a href="${langPrefix}/photo-to-black-and-white" class="mega-link">
              <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a10 10 0 0 0 0 20z"/></svg></div>
              <div class="mega-link-text"><span class="mega-link-name">B&W Filter</span><span class="mega-link-desc">Grayscale conversion</span></div>
            </a>
          </div>
        </div>
    `;
    document.body.appendChild(megaDropdown);

    const megaBtn = megaWrapper.querySelector('.mega-btn');

    megaBtn.addEventListener('click', (e) => {
      e.preventDefault(); e.stopPropagation();
      const isExpanded = megaBtn.getAttribute('aria-expanded') === 'true';
      megaBtn.setAttribute('aria-expanded', !isExpanded);
      megaDropdown.classList.toggle('open');
    });

    document.addEventListener('click', (e) => {
      if(!megaWrapper.contains(e.target) && !megaDropdown.contains(e.target)) {
         megaBtn.setAttribute('aria-expanded', 'false');
         megaDropdown.classList.remove('open');
      }
    });
  }
}
