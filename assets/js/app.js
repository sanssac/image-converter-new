// ── HTML Escape Helper ────────────────
function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// ── Toast System ──────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  const span = document.createElement('span');
  span.textContent = message;
  el.appendChild(span);
  container.appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toastFadeOut 0.3s forwards';
    setTimeout(() => el.remove(), 300);
  }, 3000);
}

// ── PWA Service Worker ────────────────
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(err => {
      console.warn('SW registration failed: ', err);
    });
  });
}

window.addEventListener('unhandledrejection', (event) => {
  // Log only, don't show toast to user as it's often caused by 3rd party scripts (ads, analytics)
  console.error('Unhandled rejection:', event.reason);
});

window.addEventListener('error', (event) => {
  if (event.message === 'ResizeObserver loop limit exceeded') return;
  console.error('Global error:', event.error || event.message);
});

document.addEventListener('DOMContentLoaded', () => {
  const dropZone    = document.getElementById('dropZone');
  const fileInput   = document.getElementById('fileInput');
  const fileGallery = document.getElementById('fileGallery');
  const convertBtn  = document.getElementById('convertBtn');
  const convertBtnText = document.getElementById('convertBtnText');
  const resultCard  = document.getElementById('resultCard');
  const downloadBtn = document.getElementById('downloadBtn');
  const copyBtn     = document.getElementById('copyBtn');
  const downloadText= document.getElementById('downloadText');
  const canvas      = document.getElementById('canvas');
  
  // ── Theme Manager ─────────────────────
  const headerElem = document.querySelector('header');
  if (headerElem) {
    const toggleBtn = document.createElement('button');
    toggleBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
    toggleBtn.style = "background:none; border:none; color:inherit; cursor:pointer; margin-left:12px; display:flex; align-items:center; transition:0.2s;";
    headerElem.appendChild(toggleBtn);
    
    toggleBtn.addEventListener('click', () => {
      const newTheme = document.body.dataset.theme === 'light' ? 'dark' : 'light';
      document.body.dataset.theme = newTheme;
      localStorage.setItem('theme', newTheme);
      toggleBtn.innerHTML = newTheme === 'light' 
        ? `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`
        : `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>`;
    });
    
    if (localStorage.getItem('theme') === 'light') {
      document.body.dataset.theme = 'light';
      toggleBtn.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;
    }

    // ── Navigation & Tools Mega Menu ──────
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
              <h4>Tools & Filters</h4>
              <a href="${langPrefix}/resize-image" class="mega-link">
                <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg></div>
                <div class="mega-link-text"><span class="mega-link-name">Resize Image</span><span class="mega-link-desc">Change dimensions</span></div>
              </a>
              <a href="${langPrefix}/watermark-image" class="mega-link">
                <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg></div>
                <div class="mega-link-text"><span class="mega-link-name">Watermark</span><span class="mega-link-desc">Add text overlays</span></div>
              </a>
              <a href="${langPrefix}/jpg-to-pdf" class="mega-link">
                <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
                <div class="mega-link-text"><span class="mega-link-name">JPG to PDF</span><span class="mega-link-desc">Document compiler</span></div>
              </a>
              <a href="${langPrefix}/compress-image" class="mega-link">
                <div class="mega-icon-wrap"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg></div>
                <div class="mega-link-text"><span class="mega-link-name">Compress</span><span class="mega-link-desc">Auto quality optimizer</span></div>
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

    // ── Language Switcher Component ──────
    if (navContainer && !document.querySelector('.lang-switcher')) {
      const langNames = { en: 'English', es: 'Español', fr: 'Français', zh: '中文', hi: 'हिन्दी' };
      const currentLangName = langNames[currentDocLang] || 'English';

      const switcherDiv = document.createElement('div');
      switcherDiv.className = 'lang-switcher';
      
      const path = window.location.pathname; 
      let pathWithoutLang = path;
      if(path.match(/^\/(es|fr|zh|hi)(\/|$)/)) {
        pathWithoutLang = path.replace(/^\/(es|fr|zh|hi)/, '') || '/';
      }

      switcherDiv.innerHTML = `
        <button class="lang-btn" aria-expanded="false" aria-haspopup="true">
          <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span>${currentLangName}</span>
          <svg class="lang-chev" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
        <div class="lang-menu">
          ${Object.entries(langNames).map(([code, name]) => {
             let newPath = code === 'en' ? pathWithoutLang : `/${code}${pathWithoutLang === '/' ? '/' : pathWithoutLang}`;
             newPath = newPath.replace(/\/\//g, '/'); // fix double slashes
             return `<a href="${newPath}" class="lang-opt ${code === currentDocLang ? 'active' : ''}">${name}</a>`;
          }).join('')}
        </div>
      `;
      navContainer.appendChild(switcherDiv);
      
      const langBtn = switcherDiv.querySelector('.lang-btn');
      const langMenu = switcherDiv.querySelector('.lang-menu');
      
      langBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const isExpanded = langBtn.getAttribute('aria-expanded') === 'true';
        langBtn.setAttribute('aria-expanded', !isExpanded);
        langMenu.classList.toggle('open');
      });
      
      document.addEventListener('click', (e) => {
        if(!switcherDiv.contains(e.target)) {
           langBtn.setAttribute('aria-expanded', 'false');
           langMenu.classList.remove('open');
        }
      });
    }
  }

  // ── Active Nav Link Highlight ─────────
  const currentPath = window.location.pathname.replace(/\/$/, '') || '/';
  document.querySelectorAll('header nav a').forEach(link => {
    try {
      const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/$/, '') || '/';
      if (linkPath === currentPath) link.classList.add('nav-active');
    } catch(e) {}
  });

  // ── UI Enhancement: Sticky Header Scroll ──
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

  // ── UI Enhancement: Feature Badges ──
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

  // ── UI Enhancement: FAQ Accordion ──
  document.querySelectorAll('.faq-item').forEach((item, i) => {
    const question = item.querySelector('.faq-question');
    if (!question) return;
    // Open first item by default
    if (i === 0) item.classList.add('open');
    question.addEventListener('click', () => {
      item.classList.toggle('open');
    });
  });

  // ── UI Enhancement: Footer Branding ──
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

  // ── UI Enhancement: Scroll Reveal ──
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

  if (!dropZone || !convertBtn) return; // Not a converter page
  
  const dropZoneH2 = dropZone.querySelector('h2');
  const defaultDropText = dropZoneH2 ? dropZoneH2.textContent : 'Drop images here';
  
  const progressContainer = document.getElementById('progressContainer');
  const progressFill = document.getElementById('progressFill');

  // Inject progress label element dynamically so we don't need to edit all HTML files
  let progressLabel = document.createElement('div');
  progressLabel.id = 'progressLabel';
  progressLabel.className = 'progress-label';
  progressContainer.insertAdjacentElement('afterend', progressLabel);

  // Inject clear button into result card once
  const clearBtn = document.createElement('button');
  clearBtn.id = 'clearBtn';
  clearBtn.className = 'btn-clear';
  clearBtn.innerHTML = `<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.5"/></svg>`;
  clearBtn.addEventListener('click', () => {
    queuedFiles.forEach(q => { if (q.thumbUrl) URL.revokeObjectURL(q.thumbUrl); });
    queuedFiles = [];
    convertedFiles = [];
    const baContainer = document.getElementById('beforeAfterContainer');
    if (baContainer) baContainer.querySelectorAll('img').forEach(img => URL.revokeObjectURL(img.src));
    resultCard.classList.remove('visible');
    progressContainer.classList.remove('visible');
    progressLabel.textContent = '';
    convertBtn.disabled = false;
    convertBtnText.textContent = isCompression ? t.compressImages : t.convertImages;
    renderGallery();
    dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
  resultCard.appendChild(clearBtn);

  // Settings logic (Tabs)
  let selectedMime = document.body.dataset.targetMime || 'image/jpeg';

  // ── i18n for dynamic UI strings ─────
  const lang = document.documentElement.lang || 'en';
  const i18nStrings = {
    en:  { converting: 'Converting', of: 'of', filesSelected: 'file(s) selected - Drop more?', convertMore: 'Convert More Images', compressImages: 'Compress Images', convertImages: 'Convert Images', success: 'Success!', filesProcessed: 'file(s) processed', original: 'Original', processed: 'Processed', smaller: 'smaller', larger: 'larger', downloadZip: 'Download ZIP', download: 'Download', zipping: 'Zipping', copiedClipboard: 'Image copied to clipboard!', copyBlocked: 'Browser blocked clipboard copy.', copyNotSupported: 'Clipboard copy not supported on this browser.', heicNotLoaded: 'Loading HEIC library... Please wait.', heicFailed: 'Failed to process HEIC', zipNotLoaded: 'JSZip library has not loaded yet.' },
    es:  { converting: 'Convirtiendo', of: 'de', filesSelected: 'archivo(s) — ¿más?', convertMore: 'Convertir más', compressImages: 'Comprimir imagen', convertImages: 'Convertir', success: '¡Éxito!', filesProcessed: 'archivo(s)', original: 'Original', processed: 'Procesado', smaller: 'más pequeño', larger: 'más grande', downloadZip: 'Descargar ZIP', download: 'Descargar', zipping: 'Comprimiendo', copiedClipboard: '¡Imagen copiada!', copyBlocked: 'Copia bloqueada por el navegador.', copyNotSupported: 'Copia no soportada.', heicNotLoaded: 'Librería HEIC no cargada.', heicFailed: 'Error HEIC', zipNotLoaded: 'JSZip no cargado.' },
    fr:  { converting: 'Conversion', of: 'de', filesSelected: 'fichier(s) — plus ?', convertMore: 'Convertir plus', compressImages: 'Compresser', convertImages: 'Convertir', success: 'Succès !', filesProcessed: 'fichier(s)', original: 'Original', processed: 'Traité', smaller: 'plus petit', larger: 'plus grand', downloadZip: 'Télécharger ZIP', download: 'Télécharger', zipping: 'Compression', copiedClipboard: 'Image copiée !', copyBlocked: 'Copie bloquée.', copyNotSupported: 'Copie non supportée.', heicNotLoaded: 'Bibliothèque HEIC non chargée.', heicFailed: 'Erreur HEIC', zipNotLoaded: 'JSZip non chargé.' },
    zh:  { converting: '转换中', of: '/', filesSelected: '文件已选 — 添加更多?', convertMore: '转换更多', compressImages: '压缩图片', convertImages: '转换', success: '成功！', filesProcessed: '个文件', original: '原始', processed: '处理后', smaller: '更小', larger: '更大', downloadZip: '下载 ZIP', download: '下载', zipping: '压缩中', copiedClipboard: '已复制到剪贴板！', copyBlocked: '浏览器阻止了复制。', copyNotSupported: '浏览器不支持复制。', heicNotLoaded: 'HEIC 库未加载。', heicFailed: 'HEIC 转换失败', zipNotLoaded: 'JSZip 未加载。' },
    hi:  { converting: 'कनवर्ट हो रहा है', of: 'में से', filesSelected: 'फाइल चुनी — और जोड़ें?', convertMore: 'और कनवर्ट करें', compressImages: 'कंप्रेस करें', convertImages: 'कनवर्ट करें', success: 'सफल!', filesProcessed: 'फाइल', original: 'मूल', processed: 'प्रोसेस्ड', smaller: 'छोटा', larger: 'बड़ा', downloadZip: 'ZIP डाउनलोड', download: 'डाउनलोड', zipping: 'ज़िप हो रहा', copiedClipboard: 'कॉपी हो गया!', copyBlocked: 'ब्राउज़र ने कॉपी ब्लॉक किया।', copyNotSupported: 'कॉपी सपोर्ट नहीं है।', heicNotLoaded: 'HEIC लाइब्रेरी लोड नहीं हुई।', heicFailed: 'HEIC एरर', zipNotLoaded: 'JSZip लोड नहीं हुआ।' },
  };
  const t = i18nStrings[lang] || i18nStrings.en;
  clearBtn.appendChild(document.createTextNode(' ' + t.convertMore));

  // Language Switcher Component has been moved up to run on all pages
  const tabs = document.querySelectorAll('.format-tabs .tab');
  if (tabs.length > 0) {
    // If tabs exist, preselect based on dataset
    tabs.forEach(tab => {
        if (tab.getAttribute('data-target') === selectedMime) {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
        }
        tab.addEventListener('click', (e) => {
            tabs.forEach(t => t.classList.remove('active'));
            e.target.classList.add('active');
            selectedMime = e.target.getAttribute('data-target');
        });
    });
  }

  const batchCountText = document.getElementById('batchCountText');
  const batchSizeOrig  = document.getElementById('batchSizeOrig');
  const batchSizeNew   = document.getElementById('batchSizeNew');

  const sizePresets = document.querySelectorAll('.preset-pill, .preset');
  const customSizeWrapper = document.getElementById('customSizeWrapper');
  const customSizeInput = document.getElementById('customSizeInput');
  const customSizeUnit = document.getElementById('customSizeUnit');
  // Default to 500 KB limit if in compress mode
  let targetSizeValue = 500; 
  
  if (sizePresets.length > 0) {
    sizePresets.forEach(pill => {
      pill.addEventListener('click', (e) => {
        sizePresets.forEach(p => p.classList.remove('active'));
        const pillElem = e.currentTarget;
        pillElem.classList.add('active');
        const val = pillElem.getAttribute('data-size');
        if (val === 'custom') {
          if (customSizeWrapper) customSizeWrapper.style.display = 'block';
          targetSizeValue = 'custom';
        } else {
          if (customSizeWrapper) customSizeWrapper.style.display = 'none';
          targetSizeValue = parseInt(val, 10);
        }
      });
    });
  } else if (document.body.hasAttribute('data-target-size')) {
    targetSizeValue = parseInt(document.body.getAttribute('data-target-size'), 10);
  }

  let queuedFiles = [];
  let convertedFiles = [];
  let isCompression = false; // hoisted so download handler can read it 

  function fmtBytes(b) {
    if (!b || b < 0) return '0 B';
    const k = 1024, units = ['B','KB','MB','GB'];
    const i = Math.min(Math.floor(Math.log(b) / Math.log(k)), units.length - 1);
    return (b / k ** i).toFixed(1) + ' ' + units[i];
  }

  const btnLocal = document.getElementById('btnLocal');
  if (btnLocal) btnLocal.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });

  document.body.addEventListener('dragover', (e) => { 
    e.preventDefault(); 
    if (dropZone) { dropZone.classList.add('dragging'); dropZone.classList.add('drag-over'); }
  });
  document.body.addEventListener('dragleave', (e) => { 
    if (!e.relatedTarget && dropZone) { dropZone.classList.remove('dragging'); dropZone.classList.remove('drag-over'); }
  });
  document.body.addEventListener('drop', (e) => {
    e.preventDefault(); 
    if (dropZone) { dropZone.classList.remove('dragging'); dropZone.classList.remove('drag-over'); }
    if (e.dataTransfer.files.length) handleFiles(e.dataTransfer.files);
  });
  
  // Keyboard Shortcuts
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && convertBtn && !convertBtn.disabled && queuedFiles.length > 0 && !queuedFiles.some(q => q.processing) && !queuedFiles.every(q => q.result !== null)) {
      convertBtn.click();
    }
    if (e.key === 'Escape' && queuedFiles.length > 0) {
      const existingClearBtn = document.getElementById('clearBtn');
      if (existingClearBtn && resultCard.classList.contains('visible')) {
        existingClearBtn.click();
      } else {
        queuedFiles.forEach(q => { if (q.thumbUrl) URL.revokeObjectURL(q.thumbUrl); });
        queuedFiles = [];
        renderGallery();
      }
    }
  });
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFiles(e.target.files);
    e.target.value = '';
  });

  async function handleFiles(files) {
    const wasEmpty = queuedFiles.length === 0;
    progressContainer.classList.remove('visible');
    resultCard.classList.remove('visible');
    resultCard.classList.remove('success-anim');
  
    for (let f of files) {
      const ext = f.name.split('.').pop().toLowerCase();
      
      if (!f.type.startsWith('image/') && !['heic', 'heif', 'ico', 'svg'].includes(ext)) {
         showToast(t.error || 'Invalid file type: ' + f.name, 'error');
         continue;
      }
      
      let fileToQueue = f;
      const queueId = Math.random().toString(36).substr(2, 9);
      if (ext === 'heic' || ext === 'heif') {
         if (typeof heic2any === 'undefined') {
           showToast(t.heicNotLoaded, 'error');
           continue;
         }
         try {
           queuedFiles.push({ file: f, result: null, id: queueId, processing: true, thumbUrl: '' });
           renderGallery();
           
           const conversionResult = await heic2any({ blob: f, toType: 'image/jpeg' });
           const blob = Array.isArray(conversionResult) ? conversionResult[0] : conversionResult;
           fileToQueue = new File([blob], f.name.replace(/\.[^.]+$/, '.jpg'), { type: 'image/jpeg' });
           
           const qItem = queuedFiles.find(q => q.id === queueId);
           if (qItem) { qItem.file = fileToQueue; qItem.processing = false; qItem.thumbUrl = URL.createObjectURL(fileToQueue); renderGallery(); }
           
           // Throttling / GC yielding for older iOS Safari limits
           await new Promise(resolve => setTimeout(resolve, 50));
           continue;
         } catch (e) {
           showToast(t.heicFailed + ': ' + f.name, 'error');
           queuedFiles = queuedFiles.filter(q => q.id !== queueId);
           continue;
         }
      }
      queuedFiles.push({ file: fileToQueue, result: null, id: queueId, processing: false, thumbUrl: URL.createObjectURL(fileToQueue) });
    }
    renderGallery();
    if (wasEmpty && queuedFiles.length > 0) {
      setTimeout(() => {
        convertBtn.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }, 100);
    }
  }

  function removeFile(id) {
    const qItem = queuedFiles.find(q => q.id === id);
    if (qItem && qItem.thumbUrl) URL.revokeObjectURL(qItem.thumbUrl);
    queuedFiles = queuedFiles.filter(q => q.id !== id);
    renderGallery();
  }

  // Event delegation for remove buttons (avoids global function + inline onclick)
  fileGallery.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('.btn-remove');
    if (removeBtn && removeBtn.dataset.fileId) {
      removeFile(removeBtn.dataset.fileId);
    }
  });

  function renderGallery() {
    if (queuedFiles.length === 0) {
      fileGallery.classList.remove('visible');
      convertBtn.classList.remove('visible');
      if (dropZoneH2) dropZoneH2.textContent = defaultDropText;
      return;
    }
    if (dropZoneH2) dropZoneH2.textContent = `${queuedFiles.length} ${t.filesSelected}`;
    
    fileGallery.innerHTML = '';
    queuedFiles.forEach((q, index) => {
      const div = document.createElement('div');
      div.className = `file-item ${q.result ? 'done' : ''}`;
      div.id = `item-${q.id}`;
      div.style.animationDelay = `${index * 0.05}s`;
      
      const url = q.processing ? '' : q.thumbUrl;
      const thumbElement = q.processing 
          ? `<div class="skeleton-loader"></div>`
          : `<img src="${url}" />`;
          
      const safeName = escapeHtml(q.file.name);
      const metaText = q.processing ? 'Decoding HEIC...' : fmtBytes(q.file.size);
      const resultText = q.result ? '→ ' + (q.result.error ? '<span style="color:#ef4444">Failed</span>' : fmtBytes(q.result.size)) : '';
      div.innerHTML = `
        <div class="thumb">${thumbElement}</div>
        <div class="info">
          <div class="name" title="${safeName}">${safeName}</div>
          <div class="meta">${metaText} ${resultText}</div>
        </div>
        <div class="status">Done</div>
        <button class="btn-remove remove" aria-label="Remove file" data-file-id="${q.id}" ${q.processing ? 'disabled' : ''}>
           <svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      `;
      fileGallery.appendChild(div);
    });
    fileGallery.classList.add('visible');
    convertBtn.classList.add('visible');
    
    const isProcessing = queuedFiles.some(q => q.processing);
    const allConverted = queuedFiles.every(q => q.result !== null);
    convertBtn.disabled = isProcessing || allConverted;
  }

  convertBtn.addEventListener('click', async () => {
    convertBtn.disabled = true;
    convertBtnText.innerHTML = `<span class="spinner" style="margin-right:6px; vertical-align:middle;"></span>${t.converting}...`;
    progressContainer.classList.add('visible');
    progressFill.style.width = '0%';
    
    isCompression = document.body.dataset.mode === 'compress' || document.body.dataset.compressMode === 'true';

    convertedFiles = [];
    let totalOrigSize = 0;
    let totalNewSize = 0;
    let lastTargetExt = 'jpg';

    for (let i = 0; i < queuedFiles.length; i++) {
      let q = queuedFiles[i];

      // In compress mode, keep original format; in convert mode, use tab selection
      let targetMime = selectedMime;
      if (isCompression) {
        const origType = q.file.type;
        if (origType === 'image/png') targetMime = 'image/png';
        else if (origType === 'image/webp') targetMime = 'image/webp';
        else targetMime = 'image/jpeg'; // default for jpg/heic/unknown
      }
      const targetExtMap = { 'image/jpeg':'jpg', 'image/png':'png', 'image/webp':'webp', 'image/avif':'avif', 'image/x-icon':'ico' };
      const targetExt = targetExtMap[targetMime] || 'jpg';
      lastTargetExt = targetExt;

      if (q.result) {
         convertedFiles.push({ name: `${q.file.name.replace(/\.[^.]+$/, '')}.${targetExt}`, blob: q.result });
         totalOrigSize += q.file.size;
         totalNewSize += q.result.size;
      } else {
         await new Promise(resolve => setTimeout(resolve, 15)); // Yield to main thread for UI animations
         totalOrigSize += q.file.size;
         const objUrl = URL.createObjectURL(q.file);
         
         const getBlob = (imgObj, w, h, outMime, outQuality) => new Promise(res => {
             let targetW = w;
             let targetH = h;
             if (outMime === 'image/x-icon') {
                 const size = Math.min(w, h, 256);
                 targetW = size;
                 targetH = size;
             }
             canvas.width = targetW; canvas.height = targetH;
             const ctx = canvas.getContext('2d');
             if (document.body.dataset.mode === 'bw') {
                 ctx.filter = 'grayscale(100%)';
             }
             if (outMime === 'image/jpeg') {
                 ctx.fillStyle = '#ffffff';
                 ctx.fillRect(0, 0, targetW, targetH);
             }
             if (outMime === 'image/x-icon') {
                 const minDim = Math.min(imgObj.naturalWidth, imgObj.naturalHeight);
                 const sx = (imgObj.naturalWidth - minDim) / 2;
                 const sy = (imgObj.naturalHeight - minDim) / 2;
                 ctx.drawImage(imgObj, sx, sy, minDim, minDim, 0, 0, targetW, targetH);
             } else {
                 ctx.drawImage(imgObj, 0, 0, targetW, targetH);
             }
             ctx.filter = 'none'; // reset filter
             
             if (document.body.dataset.mode === 'watermark') {
                 const wText = document.getElementById('watermarkText') ? document.getElementById('watermarkText').value.trim() : '';
                 if (wText) {
                     const wSize = parseInt(document.getElementById('watermarkSize').value, 10) || 32;
                     const wPos = document.getElementById('watermarkPos') ? document.getElementById('watermarkPos').value : 'bottom-right';
                     
                     ctx.font = `bold ${wSize}px sans-serif`;
                     ctx.fillStyle = 'rgba(255, 255, 255, 0.6)'; // semi-transparent white
                     const padding = 20;
                     const metrics = ctx.measureText(wText);
                     const textWidth = metrics.width;
                     
                     let wx = padding, wy = padding + wSize;
                     if (wPos === 'bottom-right') {
                         wx = targetW - textWidth - padding;
                         wy = targetH - padding;
                     } else if (wPos === 'bottom-left') {
                         wx = padding;
                         wy = targetH - padding;
                     } else if (wPos === 'top-right') {
                         wx = targetW - textWidth - padding;
                         wy = padding + wSize;
                     } else if (wPos === 'center') {
                         wx = (targetW - textWidth) / 2;
                         wy = (targetH + wSize) / 2;
                     }
                     
                     // Text shadow for contrast
                     ctx.shadowColor = "rgba(0,0,0,0.8)";
                     ctx.shadowBlur = 6;
                     ctx.shadowOffsetX = 2;
                     ctx.shadowOffsetY = 2;
                     
                     ctx.fillText(wText, wx, wy);
                     
                     // Reset shadow
                     ctx.shadowBlur = 0;
                     ctx.shadowOffsetX = 0;
                     ctx.shadowOffsetY = 0;
                 }
             }
             
             if (outMime === 'image/x-icon') {
                 canvas.toBlob(pngBlob => {
                     if (!pngBlob) { res(null); return; }
                     pngBlob.arrayBuffer().then(pngBuffer => {
                         const pngBytes = new Uint8Array(pngBuffer);
                         const icoBuffer = new ArrayBuffer(22 + pngBytes.length);
                         const view = new DataView(icoBuffer);
                         view.setUint16(0, 0, true);
                         view.setUint16(2, 1, true);
                         view.setUint16(4, 1, true);
                         const icoW = targetW >= 256 ? 0 : targetW;
                         const icoH = targetH >= 256 ? 0 : targetH;
                         view.setUint8(6, icoW);
                         view.setUint8(7, icoH);
                         view.setUint8(8, 0);
                         view.setUint8(9, 0);
                         view.setUint16(10, 1, true);
                         view.setUint16(12, 32, true);
                         view.setUint32(14, pngBytes.length, true);
                         view.setUint32(18, 22, true);
                         const icoBytes = new Uint8Array(icoBuffer);
                         icoBytes.set(pngBytes, 22);
                         res(new Blob([icoBytes], { type: 'image/x-icon' }));
                     });
                 }, 'image/png');
             } else {
                 canvas.toBlob(b => res(b), outMime, outMime !== 'image/png' ? outQuality : undefined);
             }
         });

         const blob = await new Promise((resolve) => {
           const img = new Image();
           img.onerror = () => {
             URL.revokeObjectURL(objUrl);
             resolve({ error: true });
           };
           img.onload = async () => {
             let baseW = img.naturalWidth;
             let baseH = img.naturalHeight;
             
             const hasSizePresets = document.querySelector('.size-presets, .preset-pill, .preset') !== null;
             const hasBodyTargetSize = document.body.hasAttribute('data-target-size');
             
             if (document.body.dataset.mode === 'resize') {
                 const rWInput = document.getElementById('resizeWidth');
                 const rHInput = document.getElementById('resizeHeight');
                 const maintain = document.getElementById('maintainRatio') ? document.getElementById('maintainRatio').checked : true;
                 
                 let newW = parseFloat(rWInput.value) || 0;
                 let newH = parseFloat(rHInput.value) || 0;
                 
                 if (!newW && !newH) {
                     newW = baseW; newH = baseH;
                 } else if (maintain) {
                     if (newW && !newH) newH = Math.round(baseH * (newW / baseW));
                     else if (newH && !newW) newW = Math.round(baseW * (newH / baseH));
                     else {
                         // both defined but maintain ratio is checked.
                         // we'll fit within the box.
                         const ratio = Math.min(newW / baseW, newH / baseH);
                         newW = Math.round(baseW * ratio);
                         newH = Math.round(baseH * ratio);
                     }
                 } else {
                     if (!newW) newW = baseW;
                     if (!newH) newH = baseH;
                 }
                 
                 const b = await getBlob(img, newW, newH, targetMime, 0.95);
                 URL.revokeObjectURL(objUrl);
                 resolve(b);
                 return;
             }

             if (!isCompression || (!hasSizePresets && !hasBodyTargetSize)) {
               // Normal conversion path
               const b = await getBlob(img, baseW, baseH, targetMime, 0.92);
               URL.revokeObjectURL(objUrl);
               resolve(b);
               return;
             }

             // --- Target Size Compression Logic ---
              let targetBytes = targetSizeValue;
              if (targetSizeValue === 'custom') {
                  const customVal = parseFloat(customSizeInput ? customSizeInput.value : 500) || 500;
                  targetBytes = (customSizeUnit && customSizeUnit.value === 'MB') ? customVal * 1024 * 1024 : customVal * 1024;
              } else if (targetSizeValue >= 10000) {
                  // Localized pages store data-size in bytes directly
                  targetBytes = targetSizeValue;
              } else {
                  // EN compress page stores data-size in KB
                  targetBytes = targetSizeValue * 1024;
              }
             
             let bestBlob = null;
             if (targetMime === 'image/png') {
                  // PNG is lossless HTML-wise. To compress, we must scale dimensions.
                  let scale = 1.0;
                  let lastPngBlob = null;
                  while (scale >= 0.1) {
                      lastPngBlob = await getBlob(img, baseW * scale, baseH * scale, targetMime, 1);
                      if (lastPngBlob.size <= targetBytes) { bestBlob = lastPngBlob; break; }
                      scale *= 0.8;
                  }
                  if (!bestBlob) bestBlob = lastPngBlob; // best effort: smallest tried
             } else {
                 // JPEG/WEBP Quality Binary Search
                 let finalBlob = await getBlob(img, baseW, baseH, targetMime, 0.9);
                 if (finalBlob.size <= targetBytes) {
                     bestBlob = finalBlob;
                 } else {
                     let minQ = 0.01;
                     let maxQ = 0.9;
                     let q = 0.45;
                     for (let attempt = 0; attempt < 6; attempt++) {
                         let tempBlob = await getBlob(img, baseW, baseH, targetMime, q);
                         if (tempBlob.size <= targetBytes) {
                             bestBlob = tempBlob;
                             minQ = q; // Can we do higher quality?
                         } else {
                             maxQ = q; // Need lower quality
                         }
                         q = (minQ + maxQ) / 2;
                     }
                     
                     // If still null (meaning even Q=0.01 is too large), engage dim scaling
                     if (!bestBlob) {
                         let scale = 0.85;
                         while (scale >= 0.1) {
                             const scaledBlob = await getBlob(img, baseW * scale, baseH * scale, targetMime, 0.1);
                             bestBlob = scaledBlob; // guarantee we return something
                             if (scaledBlob.size <= targetBytes) break;
                             scale *= 0.8;
                         }
                     }
                 }
             }
             
             URL.revokeObjectURL(objUrl);
             resolve(bestBlob);
           };
           img.src = objUrl;
         });

         if (blob && !blob.error) {
           q.result = blob;
           let baseName = q.file.name.replace(/\.[^.]+$/, '');
           convertedFiles.push({ name: `${baseName}.${targetExt}`, blob: blob });
           totalNewSize += blob.size;
         } else {
           q.result = { error: true };
         }
         renderGallery();
      }
      
      progressFill.style.width = `${((i + 1) / queuedFiles.length) * 100}%`;
      progressLabel.textContent = `${t.converting} ${i + 1} ${t.of} ${queuedFiles.length}...`;
    }

    convertBtnText.textContent = isCompression ? t.compressImages : t.convertImages;

    batchCountText.innerHTML = `<strong>${convertedFiles.length}</strong> ${t.filesProcessed}`;
    batchSizeOrig.innerHTML = `${t.original}: <strong>${fmtBytes(totalOrigSize)}</strong>`;

    const savingsPct = totalOrigSize > 0 ? Math.round((1 - totalNewSize / totalOrigSize) * 100) : 0;
    const pillClass = savingsPct >= 0 ? 'savings-pill' : 'savings-pill worse';
    const pillText = savingsPct >= 0 ? `↓ ${savingsPct}% ${t.smaller}` : `↑ ${Math.abs(savingsPct)}% ${t.larger}`;
    batchSizeNew.innerHTML = `${t.processed}: <strong style="color:#d8b4fe">${fmtBytes(totalNewSize)}</strong> <span class="${pillClass}">${pillText}</span>`;
    
    progressLabel.textContent = '';
    
    if (document.body.dataset.mode === 'pdf') {
        downloadText.textContent = 'Download PDF Document';
        if (copyBtn) copyBtn.style.display = 'none';
    } else {
        downloadText.textContent = convertedFiles.length > 1 ? t.downloadZip : `${t.download} ${lastTargetExt.toUpperCase()}`;
        if (copyBtn) copyBtn.style.display = convertedFiles.length === 1 ? 'flex' : 'none';
    }

    // Before/After visual comparison injected natively for Compress Mode single files
    if (isCompression && convertedFiles.length === 1 && queuedFiles[0] && queuedFiles[0].file) {
       let baContainer = document.getElementById('beforeAfterContainer');
       if (!baContainer) {
         baContainer = document.createElement('div');
         baContainer.id = 'beforeAfterContainer';
         baContainer.className = "ba-container";
         resultCard.insertBefore(baContainer, resultCard.querySelector('.action-row'));
       }
       const origUrl = URL.createObjectURL(queuedFiles[0].file);
       const newUrl = URL.createObjectURL(convertedFiles[0].blob);
       // Revoke old URLs from previous compress runs to prevent memory leaks
       const oldImgs = baContainer.querySelectorAll('img');
       oldImgs.forEach(img => { if(img.src.startsWith('blob:')) URL.revokeObjectURL(img.src); });
       baContainer.innerHTML = `
         <img src="${origUrl}" class="ba-img ba-img-orig" />
         <div class="ba-label ba-label-orig">Original</div>
         
         <img id="afterImg" src="${newUrl}" class="ba-img ba-img-new" />
         <div class="ba-label ba-label-new">Optimized</div>
         
         <div id="baLine" class="ba-line">
           <div class="ba-slider-thumb">
             <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
           </div>
         </div>
         <input type="range" class="ba-slider" min="0" max="100" value="50" oninput="document.getElementById('afterImg').style.clipPath = 'inset(0 0 0 ' + this.value + '%)'; document.getElementById('baLine').style.left = this.value + '%';">
       `;
    }

    resultCard.classList.add('visible');
    resultCard.classList.add('success-anim');
    showToast(t.success, 'success');
    setTimeout(() => progressContainer.classList.remove('visible'), 1000);
    
    // Auto-download if only 1 file
    if (convertedFiles.length === 1) {
       setTimeout(() => { if (downloadBtn) downloadBtn.click(); }, 600);
    }
  });

  if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        if (convertedFiles.length !== 1) return;
        try {
          const item = new ClipboardItem({ [convertedFiles[0].blob.type]: convertedFiles[0].blob });
          navigator.clipboard.write([item]).then(() => {
            copyBtn.classList.add('success');
            const origIcon = copyBtn.innerHTML;
            copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
            showToast(t.copiedClipboard, 'success');
            setTimeout(() => { 
                copyBtn.classList.remove('success'); 
                copyBtn.innerHTML = origIcon;
            }, 2000);
          }).catch(err => {
            showToast(t.copyBlocked, 'error');
          });
        } catch (err) {
          showToast(t.copyNotSupported, 'error');
        }
      });
  }

  downloadBtn.addEventListener('click', async () => {
    if (convertedFiles.length === 0) return;

    if (document.body.dataset.mode === 'pdf') {
        if (typeof window.jspdf === 'undefined') {
            showToast('PDF Library not loaded. Please refresh.', 'error');
            return;
        }
        downloadText.textContent = 'Building PDF...';
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({ format: 'a4', unit: 'mm' });
        
        for (let i = 0; i < convertedFiles.length; i++) {
            if (i > 0) doc.addPage();
            const base64data = await new Promise(resolve => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(convertedFiles[i].blob);
            });
            const imgProps = doc.getImageProperties(base64data);
            const pdfWidth = doc.internal.pageSize.getWidth();
            let pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
            
            // If image is taller than A4 page, scale to fit height instead
            const pageHeight = doc.internal.pageSize.getHeight();
            let x = 0;
            let y = 0;
            let finalW = pdfWidth;
            let finalH = pdfHeight;
            
            if (pdfHeight > pageHeight) {
                finalH = pageHeight;
                finalW = (imgProps.width * pageHeight) / imgProps.height;
                x = (pdfWidth - finalW) / 2; // center horizontally
            } else {
                y = (pageHeight - pdfHeight) / 2; // center vertically
            }
            
            doc.addImage(base64data, 'JPEG', x, y, finalW, finalH);
        }
        doc.save('Converted_Images.pdf');
        downloadText.textContent = 'Download PDF Document';
        return;
    }

    if (convertedFiles.length === 1) {
      const url = URL.createObjectURL(convertedFiles[0].blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = convertedFiles[0].name;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 500);
    } else {
      const startZip = async () => {
        downloadText.textContent = `${t.zipping} 0%...`;
        const zip = new JSZip();
        convertedFiles.forEach(cf => zip.file(cf.name, cf.blob));
        const zipBlob = await zip.generateAsync({ type: 'blob' }, (metadata) => {
           downloadText.textContent = `${t.zipping} ${Math.round(metadata.percent)}%...`;
        });
        downloadText.textContent = t.downloadZip;
        const url = URL.createObjectURL(zipBlob);
        const a = document.createElement('a');
        a.href = url;
        a.download = isCompression ? 'Compressed_Images.zip' : 'Converted_Images.zip';
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 500);
      };

      if (typeof JSZip === 'undefined') {
        downloadText.textContent = 'Loading ZIP Library...';
        const script = document.createElement('script');
        script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js';
        script.onload = () => startZip();
        script.onerror = () => showToast(t.zipNotLoaded, "error");
        document.head.appendChild(script);
      } else {
        startZip();
      }
    }
  });
});
