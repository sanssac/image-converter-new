// ── Vercel Web Analytics Bootstrapper ────────────────
window.va = window.va || function () { (window.vaq = window.vaq || []).push(arguments); };

// ── HTML Escape Helper ────────────────
function escapeHtml(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
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

// ── Dark Mode Initialization & Safeguard ────────────────
try {
  if (localStorage.getItem('theme')) {
    localStorage.removeItem('theme');
  }
} catch (e) {}
if (document.documentElement) document.documentElement.dataset.theme = 'dark';
if (document.body) document.body.dataset.theme = 'dark';

// ── Load Visual & UI Modules dynamically ────────────────
const visualModules = [
  '/assets/js/modules/sticky-header.js?v=20261014',
  '/assets/js/modules/accordion.js?v=20261014'
];
visualModules.forEach(url => {
  const script = document.createElement('script');
  script.src = url;
  script.defer = true;
  document.head.appendChild(script);
});

// ── WebApplication JSON-LD Structured Data Injector ────
if (typeof document !== 'undefined') {
  const existingSchemas = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
  const hasAppSchema = existingSchemas.some(s => s.textContent.includes('"WebApplication"') || s.textContent.includes('"SoftwareApplication"'));
  if (!hasAppSchema) {
    const s = document.createElement('script');
    s.type = 'application/ld+json';
    s.setAttribute('data-app-schema', 'true');
    const appSchema = {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": document.title || "Image Converter",
      "url": window.location.href,
      "applicationCategory": "MultimediaApplication",
      "operatingSystem": "All",
      "browserRequirements": "Requires JavaScript. Requires HTML5 Canvas.",
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
      "description": (document.querySelector('meta[name="description"]') ? document.querySelector('meta[name="description"]').content : "100% private, client-side online image converter.")
    };
    s.textContent = JSON.stringify(appSchema);
    document.head.appendChild(s);
  }
}

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
  let canvas        = document.getElementById('canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    canvas.id = 'canvas';
    canvas.style.display = 'none';
    document.body.appendChild(canvas);
  }


  // ── Navigation & Tools Mega Menu ──────
  const megaWrapper = document.querySelector('.mega-menu-wrapper');
  const megaDropdown = document.querySelector('.mega-dropdown');
  if (megaWrapper && megaDropdown) {
    const megaBtn = megaWrapper.querySelector('.mega-btn');
    if (megaBtn) {
      megaBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const isExpanded = megaBtn.getAttribute('aria-expanded') === 'true';
        megaBtn.setAttribute('aria-expanded', !isExpanded);
        megaDropdown.classList.toggle('open');
      });

      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && megaDropdown.classList.contains('open')) {
          megaBtn.setAttribute('aria-expanded', 'false');
          megaDropdown.classList.remove('open');
          megaBtn.focus();
        }
      });

      document.addEventListener('click', (e) => {
        if (!megaWrapper.contains(e.target) && !megaDropdown.contains(e.target)) {
          megaBtn.setAttribute('aria-expanded', 'false');
          megaDropdown.classList.remove('open');
        }
      });
    }
  }

  // ── Language Switcher Component ──────
  const langSwitcher = document.querySelector('.lang-switcher');
  if (langSwitcher) {
    const langBtn = langSwitcher.querySelector('.lang-btn');
    const langMenu = langSwitcher.querySelector('.lang-menu');
    if (langBtn && langMenu) {
      langBtn.addEventListener('click', (e) => {
        e.preventDefault();
        e.stopPropagation();
        const isExpanded = langBtn.getAttribute('aria-expanded') === 'true';
        langBtn.setAttribute('aria-expanded', !isExpanded);
        langMenu.classList.toggle('open');
      });

      langSwitcher.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
          langBtn.setAttribute('aria-expanded', 'false');
          langMenu.classList.remove('open');
          langBtn.focus();
        }
      });

      document.addEventListener('click', (e) => {
        if (!langSwitcher.contains(e.target)) {
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



  // ── Mobile Slide-out Drawer & Hamburger Toggle ──
  const hamburgerToggle = document.querySelector('.hamburger-toggle');
  const mobileDrawer = document.getElementById('mobileDrawer');
  const drawerBackdrop = document.querySelector('.drawer-backdrop');
  const drawerClose = document.querySelector('.drawer-close');

  if (hamburgerToggle && mobileDrawer && drawerBackdrop) {
    let prevActiveElement = null;

    const openDrawer = () => {
      prevActiveElement = document.activeElement;
      mobileDrawer.classList.add('open');
      drawerBackdrop.classList.add('open');
      hamburgerToggle.setAttribute('aria-expanded', 'true');
      document.body.style.overflow = 'hidden'; // Lock background scrolling
      if (drawerClose) drawerClose.focus();
    };

    const closeDrawer = () => {
      mobileDrawer.classList.remove('open');
      drawerBackdrop.classList.remove('open');
      hamburgerToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = ''; // Unlock background scrolling
      if (prevActiveElement && typeof prevActiveElement.focus === 'function') {
        prevActiveElement.focus();
      } else {
        hamburgerToggle.focus();
      }
    };

    // Trap focus inside drawer when open
    mobileDrawer.addEventListener('keydown', (e) => {
      if (e.key !== 'Tab') return;
      const focusable = mobileDrawer.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
      if (!focusable.length) return;
      const firstEl = focusable[0];
      const lastEl = focusable[focusable.length - 1];

      if (e.shiftKey) {
        if (document.activeElement === firstEl) {
          e.preventDefault();
          lastEl.focus();
        }
      } else {
        if (document.activeElement === lastEl) {
          e.preventDefault();
          firstEl.focus();
        }
      }
    });

    hamburgerToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = mobileDrawer.classList.contains('open');
      if (isOpen) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    if (drawerClose) {
      drawerClose.addEventListener('click', closeDrawer);
    }

    drawerBackdrop.addEventListener('click', closeDrawer);

    // Close drawer on ESC key and restore focus
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileDrawer.classList.contains('open')) {
        closeDrawer();
      }
    });
  }



  // ── UI Enhancement: Top Bar Feature Capsule ──
  const headerEl = document.querySelector('header');
  const headerRight = document.querySelector('header .header-right');
  if (headerEl && headerRight && !document.querySelector('.header-features-capsule')) {
    const pageLang = (document.documentElement.lang || 'en').slice(0, 2);
    const capsuleTexts = {
      en: { fast: 'Fast', priv: '100% Private', unlim: 'Unlimited' },
      de: { fast: 'Schnell', priv: '100% Privat', unlim: 'Unbegrenzt' },
      es: { fast: 'Rápido', priv: '100% Privado', unlim: 'Ilimitado' },
      fr: { fast: 'Rapide', priv: '100% Privé', unlim: 'Illimité' },
      zh: { fast: '高速', priv: '100% 隐私', unlim: '无限制' },
      hi: { fast: 'तेज़', priv: '100% सुरक्षित', unlim: 'असीमित' }
    };
    const cT = capsuleTexts[pageLang] || capsuleTexts.en;
    const capsule = document.createElement('div');
    capsule.className = 'header-features-capsule';
    capsule.innerHTML = `
      <span class="capsule-item"><span class="capsule-icon">⚡</span> ${cT.fast}</span>
      <span class="capsule-dot">•</span>
      <span class="capsule-item"><span class="capsule-pulse-dot"></span><span class="capsule-icon">🔒</span> ${cT.priv}</span>
      <span class="capsule-dot">•</span>
      <span class="capsule-item"><span class="capsule-icon">♾️</span> ${cT.unlim}</span>
    `;
    headerEl.insertBefore(capsule, headerRight);
  }



  // ── Brand Name Update: Image Lab Converter ──
  document.querySelectorAll('.site-title').forEach(el => {
    el.innerHTML = 'Image Lab <span>Converter</span>';
  });
  document.querySelectorAll('.drawer-logo span').forEach(el => {
    el.textContent = 'Image Lab Converter';
  });

  // ── UI Enhancement: Footer Branding ──
  const footerEl = document.querySelector('footer');
  if (footerEl && !footerEl.querySelector('.footer-brand')) {
    const brand = document.createElement('div');
    brand.className = 'footer-brand';
    brand.innerHTML = `
      <div class="footer-logo"><img src="/apple-touch-icon.png" alt="Logo" style="width: 28px; height: 28px; object-fit: contain; border-radius: 8px;"></div>
      <div class="footer-name">Image Lab <span>Converter</span></div>
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
  let defaultDropText = dropZoneH2 ? dropZoneH2.textContent : 'Drop images here';

  // Dropzone keyboard accessibility
  dropZone.setAttribute('aria-label', defaultDropText);
  dropZone.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      fileInput.click();
    }
  });
  
  const progressContainer = document.getElementById('progressContainer');
  const progressFill = document.getElementById('progressFill');

  // Inject progress label element dynamically with ARIA live attributes
  let progressLabel = document.createElement('div');
  progressLabel.id = 'progressLabel';
  progressLabel.className = 'progress-label';
  progressLabel.setAttribute('role', 'status');
  progressLabel.setAttribute('aria-live', 'polite');
  progressContainer.insertAdjacentElement('afterend', progressLabel);

  // Centralized converter state reset function
  function resetConverterState() {
    queuedFiles.forEach(q => { if (q.thumbUrl) URL.revokeObjectURL(q.thumbUrl); });
    convertedFiles.forEach(cf => { if (cf.blobUrl) URL.revokeObjectURL(cf.blobUrl); });
    queuedFiles = [];
    convertedFiles = [];
    if (fileInput) fileInput.value = '';
    const baContainer = document.getElementById('beforeAfterContainer');
    if (baContainer) {
      baContainer.querySelectorAll('img').forEach(img => {
        if (img.src && img.src.startsWith('blob:')) URL.revokeObjectURL(img.src);
      });
      baContainer.remove();
    }
    if (resultCard) {
      resultCard.classList.remove('visible');
      resultCard.classList.remove('success-anim');
    }
    if (progressContainer) progressContainer.classList.remove('visible');
    if (progressLabel) progressLabel.textContent = '';
    if (convertBtn) {
      convertBtn.disabled = false;
      if (convertBtnText) {
        convertBtnText.textContent = isCompression ? t.compressImages : (document.body.dataset.mode === 'pdf' ? (t.compilePdf || 'Compile PDF') : t.convertImages);
      }
    }
    renderGallery();
    if (dropZone) {
      dropZone.classList.remove('has-files');
      dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }

  // Inject clear button into result card once
  const clearBtn = document.createElement('button');
  clearBtn.id = 'clearBtn';
  clearBtn.className = 'btn-clear';
  clearBtn.innerHTML = `<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.5"/></svg>`;
  clearBtn.addEventListener('click', resetConverterState);
  resultCard.appendChild(clearBtn);

  // Settings logic (Tabs)
  let selectedMime = document.body.dataset.targetMime || 'image/jpeg';

  // ── i18n for dynamic UI strings ─────
  const lang = (document.documentElement.lang || 'en').slice(0, 2);
  const i18nStrings = {
    en:  { converting: 'Converting', of: 'of', filesSelected: 'file(s) selected - Drop more?', convertMore: 'Convert More Images', compressImages: 'Compress Images', convertImages: 'Convert Images', compilePdf: 'Compile PDF', success: 'Success!', filesProcessed: 'file(s) processed', original: 'Original', processed: 'Processed', smaller: 'smaller', larger: 'larger', downloadZip: 'Download ZIP', download: 'Download', downloadPdf: 'Download PDF Document', downloadSingle: 'Download file', zipping: 'Zipping', buildingPdf: 'Building PDF...', loadingPdf: 'Loading PDF Library...', pdfNotLoaded: 'Failed to load PDF library.', copiedClipboard: 'Image copied to clipboard!', copyBlocked: 'Browser blocked clipboard copy.', copyNotSupported: 'Clipboard copy not supported on this browser.', heicNotLoaded: 'Loading HEIC library... Please wait.', heicFailed: 'Failed to process HEIC', tiffNotLoaded: 'Loading TIFF library... Please wait.', tiffFailed: 'Failed to process TIFF', zipNotLoaded: 'JSZip library has not loaded yet.', dropZoneCompressSize: 'Drop images here to compress under {size}KB', decodingHeic: 'Decoding HEIC...', failed: 'Failed', clearAll: 'Clear All', done: 'Done', error: 'Invalid file type: ', avifNotSupported: 'AVIF encoding not supported in this browser. Using WebP format.', pastedSuccess: 'Pasted image from clipboard' },
    de:  { converting: 'Wird konvertiert', of: 'von', filesSelected: 'Datei(en) ausgewählt - Mehr ablegen?', convertMore: 'Mehr Bilder konvertieren', compressImages: 'Bilder komprimieren', convertImages: 'Bilder konvertieren', compilePdf: 'PDF erstellen', success: 'Erfolgreich!', filesProcessed: 'Datei(en) verarbeitet', original: 'Original', processed: 'Verarbeitet', smaller: 'kleiner', larger: 'größer', downloadZip: 'ZIP herunterladen', download: 'Herunterladen', downloadPdf: 'PDF-Dokument herunterladen', downloadSingle: 'Datei herunterladen', zipping: 'Komprimieren', buildingPdf: 'PDF wird erstellt...', loadingPdf: 'Lade PDF-Bibliothek...', pdfNotLoaded: 'Fehler beim Laden der PDF-Bibliothek.', copiedClipboard: 'Bild in die Zwischenablage kopiert!', copyBlocked: 'Kopieren in Zwischenablage blockiert.', copyNotSupported: 'Zwischenablage-Kopie von diesem Browser nicht unterstützt.', heicNotLoaded: 'Lade HEIC-Bibliothek... Bitte warten.', heicFailed: 'Fehler beim Verarbeiten von HEIC', tiffNotLoaded: 'Lade TIFF-Bibliothek... Bitte warten.', tiffFailed: 'Fehler beim Verarbeiten von TIFF', zipNotLoaded: 'JSZip-Bibliothek wurde noch nicht geladen.', dropZoneCompressSize: 'Bilder hier ablegen, um sie unter {size}KB zu komprimieren', decodingHeic: 'HEIC wird decodiert...', failed: 'Fehlgeschlagen', clearAll: 'Alle löschen', done: 'Fertig', error: 'Ungültiger Dateityp: ', avifNotSupported: 'AVIF-Kodierung wird nicht unterstützt. WebP wird verwendet.', pastedSuccess: 'Bild aus Zwischenablage eingefügt' },
    es:  { converting: 'Convirtiendo', of: 'de', filesSelected: 'archivo(s) — ¿más?', convertMore: 'Convertir más', compressImages: 'Comprimir imagen', convertImages: 'Convertir', compilePdf: 'Compilar PDF', success: '¡Éxito!', filesProcessed: 'archivo(s)', original: 'Original', processed: 'Procesado', smaller: 'más pequeño', larger: 'más grande', downloadZip: 'Descargar ZIP', download: 'Descargar', downloadPdf: 'Descargar Documento PDF', downloadSingle: 'Descargar archivo', zipping: 'Comprimiendo', buildingPdf: 'Creando PDF...', loadingPdf: 'Cargando librería PDF...', pdfNotLoaded: 'Error al cargar librería PDF.', copiedClipboard: '¡Imagen copiada!', copyBlocked: 'Copia bloqueada por el navegador.', copyNotSupported: 'Copia no soportada.', heicNotLoaded: 'Librería HEIC no cargada.', heicFailed: 'Error HEIC', tiffNotLoaded: 'Cargando librería TIFF... Espere por favor.', tiffFailed: 'Error al procesar TIFF', zipNotLoaded: 'JSZip no cargado.', dropZoneCompressSize: 'Arrastra imágenes aquí para comprimir a menos de {size}KB', decodingHeic: 'Decodificando HEIC...', failed: 'Fallido', clearAll: 'Limpiar todo', done: 'Listo', error: 'Tipo de archivo no válido: ', avifNotSupported: 'Navegador no soporta codificación AVIF. Usando WebP.', pastedSuccess: 'Imagen pegada del portapapeles' },
    fr:  { converting: 'Conversion', of: 'de', filesSelected: 'fichier(s) — plus ?', convertMore: 'Convertir plus', compressImages: 'Compresser', convertImages: 'Convertir', compilePdf: 'Compiler en PDF', success: 'Succès !', filesProcessed: 'fichier(s)', original: 'Original', processed: 'Traité', smaller: 'plus petit', larger: 'plus grand', downloadZip: 'Télécharger ZIP', download: 'Télécharger', downloadPdf: 'Télécharger le Document PDF', downloadSingle: 'Télécharger le fichier', zipping: 'Compression', buildingPdf: 'Création du PDF...', loadingPdf: 'Chargement de la bibliothèque PDF...', pdfNotLoaded: 'Échec du chargement de la bibliothèque PDF.', copiedClipboard: 'Image copiée !', copyBlocked: 'Copie bloquée.', copyNotSupported: 'Copie non supportée.', heicNotLoaded: 'Bibliothèque HEIC non chargée.', heicFailed: 'Erreur HEIC', tiffNotLoaded: 'Chargement de la bibliothèque TIFF... Veuillez patienter.', tiffFailed: 'Échec du traitement du TIFF', zipNotLoaded: 'JSZip non chargé.', dropZoneCompressSize: 'Déposez les images ici pour compresser à moins de {size}KB', decodingHeic: 'Décodage HEIC...', failed: 'Échec', clearAll: 'Tout effacer', done: 'Terminé', error: 'Type de fichier non valide : ', avifNotSupported: 'Encodage AVIF non supporté. Utilisation du format WebP.', pastedSuccess: 'Image collée depuis le presse-papiers' },
    zh:  { converting: '转换中', of: '/', filesSelected: '文件已选 — 添加更多?', convertMore: '转换更多', compressImages: '压缩图片', convertImages: '转换', compilePdf: '生成 PDF', success: '成功！', filesProcessed: '个文件', original: '原始', processed: '处理后', smaller: '更小', larger: '更大', downloadZip: '下载 ZIP', download: '下载', downloadPdf: '下载 PDF 文档', downloadSingle: '下载单个文件', zipping: '压缩中', buildingPdf: '正在生成 PDF...', loadingPdf: '正在加载 PDF 库...', pdfNotLoaded: 'PDF 库加载失败。', copiedClipboard: '已复制到剪贴板！', copyBlocked: '浏览器阻止了复制。', copyNotSupported: '浏览器不支持复制。', heicNotLoaded: 'HEIC 库未加载。', heicFailed: 'HEIC 转换失败', tiffNotLoaded: '正在加载 TIFF 库... 请稍候。', tiffFailed: 'TIFF 处理失败', zipNotLoaded: 'JSZip 未加载。', dropZoneCompressSize: '拖放图片至此以压缩至 {size}KB 以下', decodingHeic: '正在解码 HEIC...', failed: '失败', clearAll: '清空列表', done: '完成', error: '无效的文件类型：', avifNotSupported: '浏览器不支持 AVIF 导出，已自动切换为 WebP。', pastedSuccess: '已从剪贴板粘贴图片' },
    hi:  { converting: 'कनवर्ट हो रहा है', of: 'में से', filesSelected: 'फाइल चुनी — और जोड़ें?', convertMore: 'और कनवर्ट करें', compressImages: 'कंप्रेस करें', convertImages: 'कनवर्ट करें', compilePdf: 'PDF बनाएं', success: 'सफल!', filesProcessed: 'फाइल', original: 'मूल', processed: 'प्रोसेस्ड', smaller: 'छोटा', larger: 'बड़ा', downloadZip: 'ZIP डाउनलोड', download: 'डाउनलोड', downloadPdf: 'PDF दस्तावेज़ डाउनलोड करें', downloadSingle: 'फ़ाइल डाउनलोड करें', zipping: 'ज़िप हो रहा', buildingPdf: 'PDF बन रहा है...', loadingPdf: 'PDF लाइब्रेरी लोड हो रही है...', pdfNotLoaded: 'PDF लाइब्रेरी लोड विफल।', copiedClipboard: 'कॉपी हो गया!', copyBlocked: 'ब्राउज़र ने कॉपी ब्लॉक किया।', copyNotSupported: 'कॉपी सपोर्ट नहीं है।', heicNotLoaded: 'HEIC लाइब्रेरी लोड नहीं हुई।', heicFailed: 'HEIC एरर', tiffNotLoaded: 'TIFF लाइब्रेरी लोड हो रही है... कृपया प्रतीक्षा करें।', tiffFailed: 'TIFF संसाधित करने में विफल', zipNotLoaded: 'JSZip लोड नहीं हुआ।', dropZoneCompressSize: 'इमेज को यहाँ छोड़ें, {size}KB से कम कंप्रेस करने के लिए', decodingHeic: 'HEIC डिकोड हो रहा है...', failed: 'विफल', clearAll: 'सब हटाएँ', done: 'पूर्ण', error: 'अमान्य फ़ाइल प्रकार: ', avifNotSupported: 'ब्राउज़र में AVIF समर्थित नहीं है। WebP का उपयोग किया जा रहा है।', pastedSuccess: 'क्लिपबोर्ड से इमेज पेस्ट की गई' },
  };
  const t = i18nStrings[lang] || i18nStrings.en;
  clearBtn.appendChild(document.createTextNode(' ' + t.convertMore));

  // Dynamic runtime localization for trust badge, result header, and copyBtn accessibility
  const resultHeader = document.querySelector('.result-header');
  if (resultHeader) {
    const successText = t.success || 'Converted successfully!';
    const svgIcon = resultHeader.querySelector('svg');
    if (svgIcon) {
      resultHeader.innerHTML = '';
      resultHeader.appendChild(svgIcon);
      resultHeader.appendChild(document.createTextNode(' ' + successText));
    }
  }

  const trustBadge = document.querySelector('.trust-badge');
  if (trustBadge) {
    const trustTexts = {
      en: '100% secure — images never leave your device',
      de: '100% sicher — Bilder verlassen niemals Ihr Gerät',
      es: '100% seguro — las imágenes nunca salen de su dispositivo',
      fr: '100% sécurisé — les images ne quittent jamais votre appareil',
      zh: '100% 安全 — 图片永远不会离开您的设备',
      hi: '100% सुरक्षित — इमेज कभी आपके डिवाइस से बाहर नहीं जातीं'
    };
    const localizedTrust = trustTexts[lang] || trustTexts.en;
    const svgIcon = trustBadge.querySelector('svg');
    if (svgIcon) {
      trustBadge.innerHTML = '';
      trustBadge.appendChild(svgIcon);
      trustBadge.appendChild(document.createTextNode(' ' + localizedTrust));
    }
  }

  if (copyBtn) {
    copyBtn.setAttribute('aria-label', 'Copy image to clipboard');
  }

  if (document.body.hasAttribute('data-target-size')) {
    const targetSizeVal = document.body.getAttribute('data-target-size');
    const template = t.dropZoneCompressSize || 'Drop bloated images here (Compress under {size}KB)';
    defaultDropText = template.replace('{size}', targetSizeVal);
    if (dropZoneH2) {
      dropZoneH2.textContent = defaultDropText;
    }
  }

  // ── Setup Custom Dropdown for format select ─────
  function setupCustomDropdown(selectId) {
    const nativeSelect = document.getElementById(selectId);
    if (!nativeSelect) return null;

    // Create container
    const container = document.createElement('div');
    container.className = 'custom-select-container tab';
    
    // Create trigger button
    const trigger = document.createElement('button');
    trigger.className = 'custom-select-trigger';
    trigger.type = 'button';
    trigger.setAttribute('aria-haspopup', 'listbox');
    trigger.setAttribute('aria-expanded', 'false');
    
    const labelSpan = document.createElement('span');
    labelSpan.className = 'custom-select-label';
    
    // Set initial label to the text of the selected/placeholder option
    const placeholderOpt = nativeSelect.options[0];
    labelSpan.textContent = placeholderOpt ? placeholderOpt.textContent : 'More...';
    trigger.appendChild(labelSpan);

    // Arrow SVG
    trigger.insertAdjacentHTML('beforeend', `<svg class="custom-select-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>`);
    
    container.appendChild(trigger);

    // Create option menu
    const menu = document.createElement('div');
    menu.className = 'custom-select-menu';
    menu.setAttribute('role', 'listbox');

    // Populate options
    const options = Array.from(nativeSelect.options).filter(opt => !opt.disabled && opt.value !== "");
    options.forEach(opt => {
      const optDiv = document.createElement('div');
      optDiv.className = 'custom-select-option';
      optDiv.setAttribute('role', 'option');
      optDiv.setAttribute('tabindex', '-1');
      optDiv.setAttribute('data-value', opt.value);
      optDiv.textContent = opt.textContent;
      
      optDiv.addEventListener('click', (e) => {
        e.stopPropagation();
        
        // Update selected class
        menu.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
        optDiv.classList.add('selected');
        
        // Update trigger label
        labelSpan.textContent = opt.textContent;
        
        // Close menu
        container.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
        
        // Update native select
        nativeSelect.value = opt.value;
        nativeSelect.dispatchEvent(new Event('change', { bubbles: true }));
      });
      menu.appendChild(optDiv);
    });

    container.appendChild(menu);

    // Toggle menu visibility
    trigger.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = container.classList.contains('open');
      
      // Close other dropdowns if any
      document.querySelectorAll('.custom-select-container').forEach(c => {
        if (c !== container) {
          c.classList.remove('open');
          c.querySelector('.custom-select-trigger').setAttribute('aria-expanded', 'false');
        }
      });
      
      if (isOpen) {
        container.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
      } else {
        container.classList.add('open');
        trigger.setAttribute('aria-expanded', 'true');
      }
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!container.contains(e.target)) {
        container.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
      }
    });

    // Keyboard navigation (Escape to close, Arrows to cycle options)
    container.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        container.classList.remove('open');
        trigger.setAttribute('aria-expanded', 'false');
        trigger.focus();
        return;
      }
      
      const isOpen = container.classList.contains('open');
      const options = Array.from(menu.querySelectorAll('.custom-select-option'));
      const activeIdx = options.findIndex(o => o.classList.contains('selected') || o === document.activeElement);
      
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!isOpen) {
          container.classList.add('open');
          trigger.setAttribute('aria-expanded', 'true');
        }
        const nextIdx = activeIdx === -1 ? 0 : (activeIdx + 1) % options.length;
        options[nextIdx].focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        if (!isOpen) {
          container.classList.add('open');
          trigger.setAttribute('aria-expanded', 'true');
        }
        const prevIdx = activeIdx === -1 ? options.length - 1 : (activeIdx - 1 + options.length) % options.length;
        options[prevIdx].focus();
      } else if ((e.key === 'Enter' || e.key === ' ') && isOpen && activeIdx !== -1) {
        e.preventDefault();
        options[activeIdx].click();
        trigger.focus();
      }
    });

    // Function to sync custom UI based on native value
    const syncCustomSelect = () => {
      const val = nativeSelect.value;
      if (!val) {
        labelSpan.textContent = placeholderOpt ? placeholderOpt.textContent : 'More...';
        menu.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
        container.classList.remove('active');
      } else {
        const matchingOpt = menu.querySelector(`[data-value="${val}"]`);
        if (matchingOpt) {
          labelSpan.textContent = matchingOpt.textContent;
          menu.querySelectorAll('.custom-select-option').forEach(o => o.classList.remove('selected'));
          matchingOpt.classList.add('selected');
          container.classList.add('active');
        }
      }
    };

    // Override value property on native select to detect programmatic changes
    const desc = Object.getOwnPropertyDescriptor(HTMLSelectElement.prototype, 'value');
    Object.defineProperty(nativeSelect, 'value', {
      get: desc.get,
      set: function(val) {
        desc.set.call(this, val);
        syncCustomSelect();
      }
    });

    // Override classList methods to sync active class
    const originalAdd = nativeSelect.classList.add;
    const originalRemove = nativeSelect.classList.remove;
    nativeSelect.classList.add = function(...args) {
      originalAdd.apply(this, args);
      if (args.includes('active')) container.classList.add('active');
    };
    nativeSelect.classList.remove = function(...args) {
      originalRemove.apply(this, args);
      if (args.includes('active')) container.classList.remove('active');
    };

    // Sync custom dropdown when native select receives a change event
    nativeSelect.addEventListener('change', syncCustomSelect);

    // Replace native select's position in DOM but keep it hidden inside container
    nativeSelect.parentNode.insertBefore(container, nativeSelect);
    nativeSelect.style.display = 'none'; // Hide native select
    container.appendChild(nativeSelect); // Move native select inside container so it's kept in DOM

    return container;
  }

  setupCustomDropdown('moreFormatsSelect');

  // ── Reciprocal / Reverse Tool Quick-Switcher ───────
  function setupReverseToolCapsule() {
    const formatTabsEl = document.getElementById('formatTabs');
    if (!formatTabsEl) return;

    // Only apply on dedicated tool pages (which have no multi-format dropdown)
    if (document.getElementById('moreFormatsSelect')) return;

    const pathname = window.location.pathname.replace(/\/+$/, '');
    const segments = pathname.split('/').filter(Boolean);
    if (segments.length === 0) return;

    // Detect language prefix if any (e.g. 'es', 'de', 'fr', 'zh', 'hi')
    let langPrefix = '';
    let toolSlug = segments[0];
    if (['de', 'es', 'fr', 'zh', 'hi'].includes(segments[0])) {
      langPrefix = '/' + segments[0];
      toolSlug = segments[1] || '';
    }

    const reverseMap = {
      'jpg-to-png': { target: 'png-to-jpg', from: 'JPG', to: 'PNG', revText: 'PNG → JPG' },
      'png-to-jpg': { target: 'jpg-to-png', from: 'PNG', to: 'JPG', revText: 'JPG → PNG' },
      'webp-to-jpg': { target: 'jpeg-to-webp', from: 'WebP', to: 'JPG', revText: 'JPEG → WebP' },
      'jpeg-to-webp': { target: 'webp-to-jpg', from: 'JPEG', to: 'WebP', revText: 'WebP → JPG' },
      'webp-to-png': { target: 'png-to-webp', from: 'WebP', to: 'PNG', revText: 'PNG → WebP' },
      'png-to-webp': { target: 'webp-to-png', from: 'PNG', to: 'WebP', revText: 'WebP → PNG' },
      'svg-to-png': { target: 'svg-to-jpg', from: 'SVG', to: 'PNG', revText: 'SVG → JPG' },
      'svg-to-jpg': { target: 'svg-to-png', from: 'SVG', to: 'JPG', revText: 'SVG → PNG' },
      'tiff-to-jpg': { target: 'jpg-to-tiff', from: 'TIFF', to: 'JPG', revText: 'JPG → TIFF' },
      'jpg-to-tiff': { target: 'tiff-to-jpg', from: 'JPG', to: 'TIFF', revText: 'TIFF → JPG' },
      'jpg-to-avif': { target: 'avif-to-jpg', from: 'JPG', to: 'AVIF', revText: 'AVIF → JPG' },
      'avif-to-jpg': { target: 'jpg-to-avif', from: 'AVIF', to: 'JPG', revText: 'JPG → AVIF' },
      'png-to-avif': { target: 'avif-to-png', from: 'PNG', to: 'AVIF', revText: 'AVIF → PNG' },
      'avif-to-png': { target: 'png-to-avif', from: 'AVIF', to: 'PNG', revText: 'PNG → AVIF' }
    };

    const pair = reverseMap[toolSlug];
    if (!pair) return;

    const switchLabels = {
      en: 'Switch to {target}',
      de: 'Zu {target} wechseln',
      es: 'Cambiar a {target}',
      fr: 'Passer à {target}',
      zh: '切换至 {target}',
      hi: '{target} पर स्विच करें'
    };
    const template = switchLabels[lang] || switchLabels.en;
    const buttonText = template.replace('{target}', pair.revText);
    const targetUrl = `${langPrefix}/${pair.target}`;

    formatTabsEl.classList.add('reverse-capsule-bar');
    formatTabsEl.innerHTML = `
      <div class="flow-indicator">
        <span class="fmt-pill from-fmt">${pair.from}</span>
        <span class="fmt-arrow">→</span>
        <span class="fmt-pill to-fmt active">${pair.to}</span>
      </div>
      <a href="${targetUrl}" class="btn-reverse-swap" aria-label="${buttonText}" title="${buttonText}">
        <svg class="swap-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M7 16V4M7 4L3 8M7 4l4 4M17 8v12M17 20l4-4M17 20l-4-4"/>
        </svg>
        <span class="swap-text">${buttonText}</span>
      </a>
    `;
  }

  setupReverseToolCapsule();

  // Language Switcher Component has been moved up to run on all pages
  const tabs = document.querySelectorAll('.format-tabs .tab:not(select):not(.custom-select-container)');
  const selectTab = document.getElementById('moreFormatsSelect');

  let queuedFiles = [];
  let convertedFiles = [];
  let isCompression = false; // hoisted so download handler can read it 

  function invalidateResults() {
    if (queuedFiles.length > 0 && queuedFiles.some(q => q.result !== null)) {
      queuedFiles.forEach(q => { q.result = null; });
      convertedFiles = [];
      const baContainer = document.getElementById('beforeAfterContainer');
      if (baContainer) {
        baContainer.querySelectorAll('img').forEach(img => {
          if (img.src && img.src.startsWith('blob:')) URL.revokeObjectURL(img.src);
        });
        baContainer.remove();
      }
      resultCard.classList.remove('visible');
      progressContainer.classList.remove('visible');
      progressLabel.textContent = '';
      convertBtn.disabled = false;
      convertBtnText.textContent = isCompression ? t.compressImages : (document.body.dataset.mode === 'pdf' ? (t.compilePdf || 'Compile PDF') : t.convertImages);
      renderGallery();
    }
  }

  if (tabs.length > 0) {
    // If tabs exist, preselect based on dataset
    tabs.forEach(tab => {
        if (tab.getAttribute('data-target') === selectedMime) {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            if (selectTab) {
                selectTab.classList.remove('active');
                selectTab.value = "";
            }
        }
        tab.addEventListener('click', (e) => {
            tabs.forEach(t => t.classList.remove('active'));
            if (selectTab) {
                selectTab.classList.remove('active');
                selectTab.value = "";
            }
            e.target.classList.add('active');
            selectedMime = e.target.getAttribute('data-target');
            invalidateResults();
        });
    });
  }

  if (selectTab) {
    selectTab.addEventListener('change', (e) => {
      const val = e.target.value;
      if (val) {
        tabs.forEach(t => t.classList.remove('active'));
        selectTab.classList.add('active');
        selectedMime = val;
        invalidateResults();
      }
    });
    // If initial selectedMime matches a select option, activate the select tab
    const options = Array.from(selectTab.options);
    const hasMatchingOption = options.some(opt => opt.value === selectedMime);
    if (hasMatchingOption) {
      tabs.forEach(t => t.classList.remove('active'));
      selectTab.classList.add('active');
      selectTab.value = selectedMime;
    }
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
        invalidateResults();
      });
    });
  } else if (document.body.hasAttribute('data-target-size')) {
    targetSizeValue = parseInt(document.body.getAttribute('data-target-size'), 10);
  }

  if (customSizeInput) customSizeInput.addEventListener('input', invalidateResults);
  ['watermarkText', 'watermarkSize', 'watermarkPos', 'cropRatio', 'cropX', 'cropY', 'cropW', 'cropH'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', invalidateResults);
      if (el.tagName === 'SELECT' || el.type === 'checkbox') {
        el.addEventListener('change', invalidateResults);
      }
    }
  });

  // ── Dedicated Resize Image Tool Interactive System ──
  const rWidthInput = document.getElementById('resizeWidth');
  const rHeightInput = document.getElementById('resizeHeight');
  const maintainCheckbox = document.getElementById('maintainRatio');
  const resizeFeedback = document.getElementById('resizeFeedback');

  let activeNaturalW = 0;
  let activeNaturalH = 0;

  function updateResizeFeedback() {
    if (!resizeFeedback) return;
    const w = parseInt(rWidthInput.value, 10) || 0;
    const h = parseInt(rHeightInput.value, 10) || 0;
    if (activeNaturalW > 0 && activeNaturalH > 0) {
      resizeFeedback.style.display = 'block';
      if (w > 0 && h > 0) {
        const pctW = Math.round((w / activeNaturalW) * 100);
        const pctH = Math.round((h / activeNaturalH) * 100);
        const pctStr = (pctW === pctH) ? `${pctW}%` : `${pctW}% × ${pctH}%`;
        resizeFeedback.innerHTML = `Original: <strong>${activeNaturalW} &times; ${activeNaturalH} px</strong> &rarr; Target: <strong>${w} &times; ${h} px</strong> <span class="badge" style="background:rgba(99,102,241,0.25); color:#a78bfa; padding:2px 7px; border-radius:4px; font-size:10px; font-weight:700; margin-left:6px;">${pctStr}</span>`;
      } else {
        resizeFeedback.innerHTML = `Original: <strong>${activeNaturalW} &times; ${activeNaturalH} px</strong>`;
      }
    } else {
      resizeFeedback.style.display = 'none';
    }
  }

  if (rWidthInput && rHeightInput) {
    rWidthInput.addEventListener('input', () => {
      const w = parseFloat(rWidthInput.value);
      if (maintainCheckbox && maintainCheckbox.checked && activeNaturalW > 0 && activeNaturalH > 0 && w > 0) {
        rHeightInput.value = Math.round(w * (activeNaturalH / activeNaturalW));
      }
      updateResizeFeedback();
      invalidateResults();
    });

    rHeightInput.addEventListener('input', () => {
      const h = parseFloat(rHeightInput.value);
      if (maintainCheckbox && maintainCheckbox.checked && activeNaturalW > 0 && activeNaturalH > 0 && h > 0) {
        rWidthInput.value = Math.round(h * (activeNaturalW / activeNaturalH));
      }
      updateResizeFeedback();
      invalidateResults();
    });

    if (maintainCheckbox) {
      maintainCheckbox.addEventListener('change', () => {
        if (maintainCheckbox.checked && activeNaturalW > 0 && activeNaturalH > 0) {
          const w = parseFloat(rWidthInput.value);
          if (w > 0) {
            rHeightInput.value = Math.round(w * (activeNaturalH / activeNaturalW));
          }
        }
        updateResizeFeedback();
        invalidateResults();
      });
    }

    // Percentage Presets: 25%, 50%, 75%, 100%, 150%, 200%
    const presetBtns = document.querySelectorAll('.resize-preset-btn');
    presetBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        presetBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const pct = parseFloat(btn.getAttribute('data-pct')) / 100;
        const baseW = activeNaturalW > 0 ? activeNaturalW : (parseFloat(rWidthInput.value) || 1920);
        const baseH = activeNaturalH > 0 ? activeNaturalH : (parseFloat(rHeightInput.value) || 1080);
        rWidthInput.value = Math.round(baseW * pct);
        rHeightInput.value = Math.round(baseH * pct);
        updateResizeFeedback();
        invalidateResults();
      });
    });
  }


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

  // ── Instant Clipboard Paste (Ctrl+V / Cmd+V Anywhere) ──
  document.addEventListener('paste', (e) => {
    // Safeguard: Never intercept when user is typing in form inputs, textareas, or editable elements
    const activeEl = document.activeElement;
    if (activeEl) {
      const tag = activeEl.tagName;
      if (tag === 'TEXTAREA' || activeEl.isContentEditable) return;
      if (tag === 'INPUT' && !['button', 'submit', 'reset', 'file', 'checkbox', 'radio'].includes(activeEl.type)) {
        return;
      }
    }

    if (!e.clipboardData) return;

    const pastedFiles = [];
    const items = e.clipboardData.items;

    if (items && items.length > 0) {
      for (let i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.kind === 'file' && item.type && (item.type.startsWith('image/') || item.type === 'application/pdf')) {
          const blob = item.getAsFile();
          if (blob) {
            const now = new Date();
            const timeStr = `${String(now.getHours()).padStart(2, '0')}-${String(now.getMinutes()).padStart(2, '0')}-${String(now.getSeconds()).padStart(2, '0')}`;
            const subType = blob.type ? blob.type.split('/')[1] : 'png';
            const ext = (subType === 'jpeg') ? 'jpg' : subType;
            const fileName = (!blob.name || blob.name === 'image.png' || blob.name === 'blob')
              ? `screenshot-${timeStr}.${ext}`
              : blob.name;
            pastedFiles.push(new File([blob], fileName, { type: blob.type || 'image/png' }));
          }
        }
      }
    }

    // Fallback if items was empty but files exists
    if (pastedFiles.length === 0 && e.clipboardData.files && e.clipboardData.files.length > 0) {
      for (let i = 0; i < e.clipboardData.files.length; i++) {
        const f = e.clipboardData.files[i];
        if (f.type && (f.type.startsWith('image/') || f.name.match(/\.(png|jpe?g|webp|avif|heic|tiff?|svg|ico|pdf)$/i))) {
          pastedFiles.push(f);
        }
      }
    }

    if (pastedFiles.length > 0) {
      e.preventDefault();
      if (dropZone) {
        dropZone.classList.remove('paste-flash');
        // Force reflow for re-triggering animation if user pastes multiple times
        void dropZone.offsetWidth;
        dropZone.classList.add('paste-flash');
        setTimeout(() => dropZone.classList.remove('paste-flash'), 900);
        dropZone.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      showToast(t.pastedSuccess || 'Pasted image from clipboard', 'info');
      handleFiles(pastedFiles);
    }
  });

  // ── Browser AVIF Canvas Encoding Support Check ─────
  let isAvifSupported = null;
  function checkAvifSupport() {
    if (isAvifSupported !== null) return isAvifSupported;
    try {
      const c = document.createElement('canvas');
      c.width = 1; c.height = 1;
      isAvifSupported = c.toDataURL('image/avif').startsWith('data:image/avif');
    } catch (e) {
      isAvifSupported = false;
    }
    return isAvifSupported;
  }

  // ── PDF Library Lazy Loader ────────────────────────
  const loadPdfLibrary = () => new Promise((resolve, reject) => {
    if (typeof window.jspdf !== 'undefined') {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.crossOrigin = 'anonymous';
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("PDF library load failed"));
    document.head.appendChild(script);
  });

  // ── Multi-Resolution Favicon ICO Generator ─────────
  async function generateMultiSizeIco(imgObj) {
    const sizes = [16, 32, 48, 256];
    const naturalW = imgObj.naturalWidth || imgObj.width;
    const naturalH = imgObj.naturalHeight || imgObj.height;
    const minDim = Math.min(naturalW, naturalH);
    const sx = (naturalW - minDim) / 2;
    const sy = (naturalH - minDim) / 2;

    const pngBlobs = [];
    for (const size of sizes) {
      const c = document.createElement('canvas');
      c.width = size;
      c.height = size;
      const ctx = c.getContext('2d');
      if (!ctx) continue;
      ctx.drawImage(imgObj, sx, sy, minDim, minDim, 0, 0, size, size);
      const pngBlob = await new Promise(resolve => c.toBlob(resolve, 'image/png'));
      c.width = 1; c.height = 1; // Release GPU texture
      if (pngBlob) {
        const buffer = await pngBlob.arrayBuffer();
        pngBlobs.push({ size, bytes: new Uint8Array(buffer) });
      }
    }

    if (pngBlobs.length === 0) return null;

    const count = pngBlobs.length;
    const headerSize = 6;
    const dirEntrySize = 16;
    let dataOffset = headerSize + count * dirEntrySize;

    let totalFileSize = dataOffset;
    for (const item of pngBlobs) {
      totalFileSize += item.bytes.length;
    }

    const icoBuffer = new ArrayBuffer(totalFileSize);
    const view = new DataView(icoBuffer);

    view.setUint16(0, 0, true);
    view.setUint16(2, 1, true); // type 1 = ICO
    view.setUint16(4, count, true);

    const icoBytes = new Uint8Array(icoBuffer);
    let currentDataOffset = dataOffset;

    for (let i = 0; i < count; i++) {
      const item = pngBlobs[i];
      const entryOffset = headerSize + i * dirEntrySize;
      const w = item.size >= 256 ? 0 : item.size;
      const h = item.size >= 256 ? 0 : item.size;

      view.setUint8(entryOffset + 0, w);
      view.setUint8(entryOffset + 1, h);
      view.setUint8(entryOffset + 2, 0);
      view.setUint8(entryOffset + 3, 0);
      view.setUint16(entryOffset + 4, 1, true); // color planes
      view.setUint16(entryOffset + 6, 32, true); // bpp
      view.setUint32(entryOffset + 8, item.bytes.length, true);
      view.setUint32(entryOffset + 12, currentDataOffset, true);

      icoBytes.set(item.bytes, currentDataOffset);
      currentDataOffset += item.bytes.length;
    }

    return new Blob([icoBytes], { type: 'image/x-icon' });
  }

  const loadHeicLibrary = () => new Promise((resolve, reject) => {
    if (typeof heic2any !== 'undefined') {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.crossOrigin = 'anonymous';
    script.src = 'https://cdn.jsdelivr.net/npm/heic2any@0.0.4/dist/heic2any.min.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("HEIC library load failed"));
    document.head.appendChild(script);
  });

  // Prefetch HEIC library on dedicated page for instant conversion
  if (typeof window !== 'undefined' && window.location.pathname.includes('heic-to-jpg')) {
    loadHeicLibrary().catch(() => {});
  }

  const loadTiffLibrary = () => new Promise((resolve, reject) => {
    if (typeof UTIF !== 'undefined') {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.crossOrigin = 'anonymous';
    script.src = 'https://cdn.jsdelivr.net/npm/utif@3.1.0/UTIF.js';
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("TIFF library load failed"));
    document.head.appendChild(script);
  });

  async function convertTiffToPngBlob(file) {
    const buffer = await file.arrayBuffer();
    const ifds = UTIF.decode(buffer);
    if (!ifds || ifds.length === 0) {
      throw new Error("Invalid TIFF file");
    }
    UTIF.decodeImage(buffer, ifds[0]);
    const rgba = UTIF.toRGBA8(ifds[0]);
    const width = ifds[0].width;
    const height = ifds[0].height;
    
    const tempCanvas = document.createElement('canvas');
    tempCanvas.width = width;
    tempCanvas.height = height;
    const tempCtx = tempCanvas.getContext('2d');
    if (!tempCtx) throw new Error("Could not get temporary canvas context");
    
    const imgData = tempCtx.createImageData(width, height);
    imgData.data.set(new Uint8ClampedArray(rgba));
    tempCtx.putImageData(imgData, 0, 0);
    
    return new Promise((resolve, reject) => {
      tempCanvas.toBlob(blob => {
        tempCanvas.width = 1;
        tempCanvas.height = 1;
        if (blob) resolve(blob);
        else reject(new Error("Canvas conversion to Blob failed"));
      }, 'image/png');
    });
  }

  async function handleFiles(files) {
    const wasEmpty = queuedFiles.length === 0;
    progressContainer.classList.remove('visible');
    resultCard.classList.remove('visible');
    resultCard.classList.remove('success-anim');
  
    for (let f of files) {
      const ext = f.name.split('.').pop().toLowerCase();
      
      if (!f.type.startsWith('image/') && !['heic', 'heif', 'ico', 'svg', 'tiff', 'tif'].includes(ext)) {
         showToast(t.error || 'Invalid file type: ' + f.name, 'error');
         continue;
      }
      
      let fileToQueue = f;
      const queueId = Math.random().toString(36).substr(2, 9);
      if (ext === 'svg') {
         // Pre-check and normalize SVG dimensions from viewBox if width/height are absent or percentage
         try {
           const svgText = await f.text();
           const parser = new DOMParser();
           const svgDoc = parser.parseFromString(svgText, 'image/svg+xml');
           const svgEl = svgDoc.querySelector('svg');
           if (svgEl) {
             let sw = parseFloat(svgEl.getAttribute('width'));
             let sh = parseFloat(svgEl.getAttribute('height'));
             const vb = svgEl.getAttribute('viewBox');
             const widthAttr = (svgEl.getAttribute('width') || '').trim();
             const heightAttr = (svgEl.getAttribute('height') || '').trim();
             const isRelative = widthAttr.endsWith('%') || heightAttr.endsWith('%') || widthAttr.endsWith('vw') || heightAttr.endsWith('vh');

             if ((isRelative || !sw || !sh || isNaN(sw) || isNaN(sh)) && vb) {
               const vbParts = vb.trim().split(/[\s,]+/).map(Number);
               if (vbParts.length === 4 && vbParts[2] > 0 && vbParts[3] > 0) {
                 svgEl.setAttribute('width', vbParts[2]);
                 svgEl.setAttribute('height', vbParts[3]);
                 const serializer = new XMLSerializer();
                 const fixedSvg = serializer.serializeToString(svgDoc);
                 fileToQueue = new File([fixedSvg], f.name, { type: 'image/svg+xml' });
               }
             }
           }
         } catch (e) {
           console.warn('SVG dimension normalization bypassed:', e);
         }
      }

      if (ext === 'heic' || ext === 'heif') {
         if (typeof heic2any === 'undefined') {
           showToast(t.heicNotLoaded, 'info');
           try {
             await loadHeicLibrary();
           } catch (err) {
             showToast(t.heicFailed + ': ' + f.name, 'error');
             continue;
           }
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
      } else if (ext === 'tiff' || ext === 'tif') {
         if (typeof UTIF === 'undefined') {
           showToast(t.tiffNotLoaded, 'info');
           try {
             await loadTiffLibrary();
           } catch (err) {
             showToast(t.tiffFailed + ': ' + f.name, 'error');
             continue;
           }
         }
         try {
           queuedFiles.push({ file: f, result: null, id: queueId, processing: true, thumbUrl: '' });
           renderGallery();
           
           const blob = await convertTiffToPngBlob(f);
           fileToQueue = new File([blob], f.name.replace(/\.[^.]+$/, '.png'), { type: 'image/png' });
           
           const qItem = queuedFiles.find(q => q.id === queueId);
           if (qItem) { qItem.file = fileToQueue; qItem.processing = false; qItem.thumbUrl = URL.createObjectURL(fileToQueue); renderGallery(); }
           
           await new Promise(resolve => setTimeout(resolve, 50));
           continue;
         } catch (e) {
           showToast(t.tiffFailed + ': ' + f.name, 'error');
           queuedFiles = queuedFiles.filter(q => q.id !== queueId);
           continue;
         }
      }
      queuedFiles.push({ file: fileToQueue, result: null, id: queueId, processing: false, thumbUrl: URL.createObjectURL(fileToQueue) });

      // Auto-detect and populate natural dimensions for resize tool
      if (document.body.dataset.mode === 'resize' && rWidthInput && rHeightInput) {
        const tempImg = new Image();
        const tempObjUrl = URL.createObjectURL(fileToQueue);
        tempImg.onload = () => {
          if (!activeNaturalW) {
            activeNaturalW = tempImg.naturalWidth;
            activeNaturalH = tempImg.naturalHeight;
            if (!rWidthInput.value || rWidthInput.value === '' || rWidthInput.value === '1080') {
              rWidthInput.value = activeNaturalW;
              rHeightInput.value = activeNaturalH;
            }
            const p100 = document.querySelector('.resize-preset-btn[data-pct="100"]');
            if (p100) {
              document.querySelectorAll('.resize-preset-btn').forEach(b => b.classList.remove('active'));
              p100.classList.add('active');
            }
            updateResizeFeedback();
          }
          URL.revokeObjectURL(tempObjUrl);
        };
        tempImg.src = tempObjUrl;
      }
    }
    renderGallery();
    if (wasEmpty && queuedFiles.length > 0) {
      setTimeout(() => {
        convertBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 350);
    }
  }

  function removeFile(id) {
    const qItem = queuedFiles.find(q => q.id === id);
    if (qItem && qItem.thumbUrl) URL.revokeObjectURL(qItem.thumbUrl);
    queuedFiles = queuedFiles.filter(q => q.id !== id);
    convertedFiles = convertedFiles.filter(cf => cf.id !== id);
    if (queuedFiles.length === 0) {
      if (document.body.dataset.mode === 'resize') {
        activeNaturalW = 0;
        activeNaturalH = 0;
        if (resizeFeedback) resizeFeedback.style.display = 'none';
        document.querySelectorAll('.resize-preset-btn').forEach(b => b.classList.remove('active'));
      }
      resultCard.classList.remove('visible');
      progressContainer.classList.remove('visible');
      progressLabel.textContent = '';
      convertBtn.disabled = true;
    }
    renderGallery();
  }

  // Event delegation for remove and individual download buttons
  fileGallery.addEventListener('click', (e) => {
    const removeBtn = e.target.closest('.btn-remove');
    if (removeBtn && removeBtn.dataset.fileId) {
      removeFile(removeBtn.dataset.fileId);
      return;
    }
    const dlBtn = e.target.closest('.btn-item-download');
    if (dlBtn && dlBtn.dataset.downloadId) {
      const cItem = convertedFiles.find(cf => cf.id === dlBtn.dataset.downloadId);
      if (cItem) {
        if (document.body.dataset.mode === 'pdf') {
          // Compile single-page PDF for this individual item
          (async () => {
             if (typeof window.jspdf === 'undefined') {
                try { await loadPdfLibrary(); } catch(err) { showToast(t.pdfNotLoaded || 'Failed to load PDF library', 'error'); return; }
             }
             const { jsPDF } = window.jspdf;
             const singleDoc = new jsPDF({ format: 'a4', unit: 'mm' });
             const base64data = await new Promise(res => {
                 const reader = new FileReader();
                 reader.onloadend = () => res(reader.result);
                 reader.readAsDataURL(cItem.blob);
             });
             const imgProps = singleDoc.getImageProperties(base64data);
             const pW = singleDoc.internal.pageSize.getWidth();
             const pH = singleDoc.internal.pageSize.getHeight();
             const m = 10;
             const maxW = pW - (m * 2);
             const maxH = pH - (m * 2);
             let fW = maxW;
             let fH = (imgProps.height * maxW) / imgProps.width;
             if (fH > maxH) { fH = maxH; fW = (imgProps.width * maxH) / imgProps.height; }
             const x = m + ((maxW - fW) / 2);
             const y = m + ((maxH - fH) / 2);
             const fmt = cItem.blob.type === 'image/png' ? 'PNG' : (cItem.blob.type === 'image/webp' ? 'WEBP' : 'JPEG');
             singleDoc.addImage(base64data, fmt, x, y, fW, fH);
             singleDoc.save(`${cItem.name.replace(/\.[^.]+$/, '')}.pdf`);
          })();
          return;
        }
        const url = URL.createObjectURL(cItem.blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = cItem.name;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 500);
      }
    }
  });

  function renderGallery() {
    if (queuedFiles.length === 0) {
      fileGallery.classList.remove('visible');
      convertBtn.classList.remove('visible');
      if (dropZone) dropZone.classList.remove('has-files');
      if (dropZoneH2) dropZoneH2.textContent = defaultDropText;
      return;
    }
    if (dropZone) dropZone.classList.add('has-files');
    if (dropZoneH2) dropZoneH2.textContent = `${queuedFiles.length} ${t.filesSelected}`;
    
    fileGallery.innerHTML = '';

    // Create Gallery Header with Clear All button
    const headerDiv = document.createElement('div');
    headerDiv.className = 'gallery-header';
    
    const countSpan = document.createElement('span');
    countSpan.className = 'gallery-title';
    countSpan.textContent = `${queuedFiles.length} ${t.filesSelected}`;
    headerDiv.appendChild(countSpan);

    const clearAllBtn = document.createElement('button');
    clearAllBtn.className = 'btn-clear-all';
    clearAllBtn.id = 'clearAllBtn';
    clearAllBtn.type = 'button';
    clearAllBtn.textContent = t.clearAll || 'Clear All';
    clearAllBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetConverterState();
    });
    headerDiv.appendChild(clearAllBtn);
    fileGallery.appendChild(headerDiv);

    queuedFiles.forEach((q, index) => {
      const div = document.createElement('div');
      div.className = `file-item ${q.result ? 'done' : ''}`;
      div.id = `item-${q.id}`;
      div.style.animationDelay = `${index * 0.05}s`;
      
      const safeName = escapeHtml(q.file.name);
      const url = q.processing ? '' : q.thumbUrl;
      const thumbElement = q.processing 
          ? `<div class="skeleton-loader"></div>`
          : `<img src="${url}" alt="Preview of ${safeName}" />`;
          
      const metaText = q.processing ? t.decodingHeic : fmtBytes(q.file.size);
      
      let resultText = '';
      let statusHtml = '';
      if (q.result) {
        if (q.result.error) {
          resultText = `→ <span style="color:#ef4444">${t.failed}</span>`;
          statusHtml = `<div class="status error">${t.failed}</div>`;
        } else {
          resultText = `→ <strong>${fmtBytes(q.result.size)}</strong>`;
          if (document.body.dataset.mode === 'pdf') {
            statusHtml = `<div class="status ready">✓ PDF</div>`;
          } else {
            const diff = q.file.size - q.result.size;
            const pct = Math.round((diff / q.file.size) * 100);
            if (pct > 0) {
              statusHtml = `<div class="status saved">-${pct}%</div>`;
            } else if (pct < 0) {
              statusHtml = `<div class="status worse">+${Math.abs(pct)}%</div>`;
            } else {
              statusHtml = `<div class="status ready">✓ ${t.done || 'Done'}</div>`;
            }
          }
        }
      } else {
        statusHtml = `<div class="status">${t.done || 'Done'}</div>`;
      }

      let itemDownloadBtn = '';
      if (q.result && !q.result.error) {
        itemDownloadBtn = `
          <button class="btn-item-download" type="button" aria-label="${t.downloadSingle || 'Download file'} - ${safeName}" data-download-id="${q.id}" title="${t.downloadSingle || 'Download file'}">
            <svg aria-hidden="true" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7 10 12 15 17 10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
          </button>`;
      }

      div.innerHTML = `
        <div class="thumb">${thumbElement}</div>
        <div class="info">
          <div class="name" title="${safeName}">${safeName}</div>
          <div class="meta">${metaText} ${resultText}</div>
        </div>
        ${statusHtml}
        ${itemDownloadBtn}
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

    if (selectedMime === 'image/tiff') {
      try {
        await loadTiffLibrary();
      } catch (err) {
        showToast(t.tiffFailed || "Failed to load TIFF library", "error");
        convertBtn.disabled = false;
        convertBtnText.textContent = isCompression ? t.compressImages : t.convertImages;
        progressContainer.classList.remove('visible');
        return;
      }
    }

    convertedFiles = [];
    let totalOrigSize = 0;
    let totalNewSize = 0;
    let lastTargetExt = 'jpg';

    for (let i = 0; i < queuedFiles.length; i++) {
      let q = queuedFiles[i];

      try {
        // In compress mode, keep original format unless targetMime is explicitly locked; in convert mode, use tab selection
        let targetMime = selectedMime;
        if (isCompression) {
          if (document.body.dataset.targetMime) {
            targetMime = document.body.dataset.targetMime;
          } else {
            const origType = q.file.type;
            if (origType === 'image/png') targetMime = 'image/png';
            else if (origType === 'image/webp') targetMime = 'image/webp';
            else targetMime = 'image/jpeg'; // default for jpg/heic/unknown
          }
        }
        
        // AVIF compatibility fallback check
        if (targetMime === 'image/avif' && !checkAvifSupport()) {
          showToast(t.avifNotSupported || 'AVIF encoding not supported by your browser. Using WebP.', 'info');
          targetMime = 'image/webp';
        }

        const targetExtMap = { 'image/jpeg':'jpg', 'image/png':'png', 'image/webp':'webp', 'image/avif':'avif', 'image/x-icon':'ico', 'image/tiff':'tiff' };
        const targetExt = targetExtMap[targetMime] || 'jpg';
        lastTargetExt = targetExt;

        if (q.result) {
           if (q.result.error) {
              // Already failed, do not add to success totals
           } else {
              convertedFiles.push({ id: q.id, name: `${q.file.name.replace(/\.[^.]+$/, '')}.${targetExt}`, blob: q.result });
              totalOrigSize += q.file.size;
              totalNewSize += q.result.size;
           }
        } else {
           await new Promise(resolve => setTimeout(resolve, 15)); // Yield to main thread for UI animations
           totalOrigSize += q.file.size;
           const objUrl = URL.createObjectURL(q.file);
           
           const getBlob = (imgObj, w, h, outMime, outQuality) => new Promise(async res => {
               let targetW = w;
               let targetH = h;

               // AUDIT-007: Safe bounds cap to prevent mobile canvas OOM crashes
               const maxDim = 8192;
               const maxTotalPixels = 16777216; // 16MP safety threshold
               if (targetW > maxDim || targetH > maxDim || (targetW * targetH) > maxTotalPixels) {
                   const ratio = Math.min(maxDim / targetW, maxDim / targetH, Math.sqrt(maxTotalPixels / (targetW * targetH)));
                   targetW = Math.max(1, Math.round(targetW * ratio));
                   targetH = Math.max(1, Math.round(targetH * ratio));
               }

               if (outMime === 'image/x-icon') {
                   const size = Math.min(w, h, 256);
                   targetW = size;
                   targetH = size;
               }
               canvas.width = targetW; canvas.height = targetH;
               const ctx = canvas.getContext('2d');
               if (!ctx) {
                   throw new Error("Could not acquire 2D canvas context.");
               }
               const isBw = document.body.dataset.mode === 'bw';
               const supportsFilter = typeof ctx.filter === 'string';
               if (isBw && supportsFilter) {
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
               if (supportsFilter) {
                   ctx.filter = 'none'; // reset filter
               }
               // AUDIT-011: Direct pixel grayscale fallback if ctx.filter is unsupported
               if (isBw && !supportsFilter) {
                   try {
                       const imgData = ctx.getImageData(0, 0, targetW, targetH);
                       const d = imgData.data;
                       for (let i = 0; i < d.length; i += 4) {
                           const gray = Math.round(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]);
                           d[i] = gray;
                           d[i + 1] = gray;
                           d[i + 2] = gray;
                       }
                       ctx.putImageData(imgData, 0, 0);
                   } catch (e) {
                       console.warn("Direct pixel grayscale conversion fallback failed:", e);
                   }
               }
               
               if (document.body.dataset.mode === 'watermark') {
                   const wText = document.getElementById('watermarkText') ? document.getElementById('watermarkText').value.trim() : '';
                   if (wText) {
                       const rawWSize = parseInt(document.getElementById('watermarkSize').value, 10) || 32;
                       const scaleFactor = Math.max(1, Math.min(targetW, targetH) / 800);
                       const wSize = Math.round(rawWSize * scaleFactor);
                       const wPos = document.getElementById('watermarkPos') ? document.getElementById('watermarkPos').value : 'bottom-right';
                       
                       ctx.font = `bold ${wSize}px sans-serif`;
                       ctx.fillStyle = 'rgba(255, 255, 255, 0.6)'; // semi-transparent white
                       const padding = Math.round(20 * scaleFactor);
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
                       } else if (wPos === 'top-left') {
                           wx = padding;
                           wy = padding + wSize;
                       } else if (wPos === 'center') {
                           wx = (targetW - textWidth) / 2;
                           wy = (targetH + wSize) / 2;
                       }
                       
                       // Text shadow for contrast
                       ctx.shadowColor = "rgba(0,0,0,0.8)";
                       ctx.shadowBlur = Math.round(6 * scaleFactor);
                       ctx.shadowOffsetX = Math.round(2 * scaleFactor);
                       ctx.shadowOffsetY = Math.round(2 * scaleFactor);
                       
                       ctx.fillText(wText, wx, wy);
                       
                       // Reset shadow
                       ctx.shadowBlur = 0;
                       ctx.shadowOffsetX = 0;
                       ctx.shadowOffsetY = 0;
                   }
               }
               
               if (outMime === 'image/x-icon') {
                   try {
                       const icoBlob = await generateMultiSizeIco(canvas);
                       res(icoBlob);
                       return;
                   } catch (icoErr) {
                       console.error("Multi-size ICO conversion error:", icoErr);
                       res(null);
                       return;
                   }
               } else if (outMime === 'image/tiff') {
                   try {
                       const imgData = ctx.getImageData(0, 0, targetW, targetH);
                       const tiffBuffer = UTIF.encodeImage(imgData.data, targetW, targetH);
                       res(new Blob([tiffBuffer], { type: 'image/tiff' }));
                   } catch (err) {
                       console.error("TIFF encoding error:", err);
                       res(null);
                   }
               } else {
                   let effectiveMime = outMime;
                   if (effectiveMime === 'image/avif' && !checkAvifSupport()) {
                       console.warn("AVIF export not supported in browser canvas; falling back to WebP");
                       effectiveMime = 'image/webp';
                   }
                   canvas.toBlob(b => {
                       if (!b && effectiveMime === 'image/avif') {
                           canvas.toBlob(fallbackB => res(fallbackB), 'image/webp', outQuality);
                       } else {
                           res(b);
                       }
                   }, effectiveMime, effectiveMime !== 'image/png' ? outQuality : undefined);
               }
           });

           const blob = await new Promise((resolve, reject) => {
             const img = new Image();
             img.onerror = () => {
               URL.revokeObjectURL(objUrl);
               resolve({ error: true });
             };
             img.onload = async () => {
               try {
                 let baseW = img.naturalWidth || img.width || 800;
                  if (baseW <= 0) baseW = 800;
                 let baseH = img.naturalHeight || img.height || 800;
                  if (baseH <= 0) baseH = 800;
                 
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

                 if (document.body.dataset.mode === 'crop') {
                     const cropRatio = document.getElementById('cropRatio') ? document.getElementById('cropRatio').value : '1:1';
                     let cX = 0, cY = 0, cW = baseW, cH = baseH;
                     if (cropRatio === '1:1') {
                         const dim = Math.min(baseW, baseH);
                         cX = Math.round((baseW - dim) / 2);
                         cY = Math.round((baseH - dim) / 2);
                         cW = dim; cH = dim;
                     } else if (cropRatio === '16:9') {
                         if (baseW / baseH > 16 / 9) {
                             cW = Math.round(baseH * (16 / 9));
                             cX = Math.round((baseW - cW) / 2);
                         } else {
                             cH = Math.round(baseW * (9 / 16));
                             cY = Math.round((baseH - cH) / 2);
                         }
                     } else if (cropRatio === '4:3') {
                         if (baseW / baseH > 4 / 3) {
                             cW = Math.round(baseH * (4 / 3));
                             cX = Math.round((baseW - cW) / 2);
                         } else {
                             cH = Math.round(baseW * (3 / 4));
                             cY = Math.round((baseH - cH) / 2);
                         }
                     } else if (cropRatio === '9:16') {
                         if (baseW / baseH > 9 / 16) {
                             cW = Math.round(baseH * (9 / 16));
                             cX = Math.round((baseW - cW) / 2);
                         } else {
                             cH = Math.round(baseW * (16 / 9));
                             cY = Math.round((baseH - cH) / 2);
                         }
                     } else if (cropRatio === '3:2') {
                         if (baseW / baseH > 3 / 2) {
                             cW = Math.round(baseH * (3 / 2));
                             cX = Math.round((baseW - cW) / 2);
                         } else {
                             cH = Math.round(baseW * (2 / 3));
                             cY = Math.round((baseH - cH) / 2);
                         }
                     } else if (cropRatio === 'custom') {
                         const customCropX = parseInt(document.getElementById('cropX')?.value, 10) || 0;
                         const customCropY = parseInt(document.getElementById('cropY')?.value, 10) || 0;
                         const customCropW = parseInt(document.getElementById('cropW')?.value, 10) || baseW;
                         const customCropH = parseInt(document.getElementById('cropH')?.value, 10) || baseH;
                         cX = Math.max(0, Math.min(baseW - 1, customCropX));
                         cY = Math.max(0, Math.min(baseH - 1, customCropY));
                         cW = Math.max(1, Math.min(baseW - cX, customCropW));
                         cH = Math.max(1, Math.min(baseH - cY, customCropH));
                     }

                     canvas.width = cW; canvas.height = cH;
                     const ctx = canvas.getContext('2d');
                     if (targetMime === 'image/jpeg') {
                         ctx.fillStyle = '#ffffff';
                         ctx.fillRect(0, 0, cW, cH);
                     }
                     ctx.drawImage(img, cX, cY, cW, cH, 0, 0, cW, cH);
                     const cropBlob = await new Promise(r => canvas.toBlob(r, targetMime || 'image/png', 0.95));
                     URL.revokeObjectURL(objUrl);
                     resolve(cropBlob);
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
                          await new Promise(r => setTimeout(r, 0));
                           lastPngBlob = await getBlob(img, Math.round(baseW * scale), Math.round(baseH * scale), targetMime, 1);
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
                             await new Promise(r => setTimeout(r, 0));
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
                                 await new Promise(r => setTimeout(r, 0));
                                  const scaledBlob = await getBlob(img, Math.round(baseW * scale), Math.round(baseH * scale), targetMime, 0.1);
                                 bestBlob = scaledBlob; // guarantee we return something
                                 if (scaledBlob.size <= targetBytes) break;
                                 scale *= 0.8;
                             }
                         }
                     }
                 }
                 
                 URL.revokeObjectURL(objUrl);
                 resolve(bestBlob);
               } catch (err) {
                 URL.revokeObjectURL(objUrl);
                 reject(err);
               }
             };
             img.src = objUrl;
           });

           if (blob && !blob.error) {
             q.result = blob;
             let actualExt = targetExt;
             if (blob.type === 'image/webp' && targetExt === 'avif') actualExt = 'webp';
             let baseName = q.file.name.replace(/\.[^.]+$/, '');
             convertedFiles.push({ id: q.id, name: `${baseName}.${actualExt}`, blob: blob });
             totalNewSize += blob.size;
           } else {
             q.result = { error: true };
           }
           renderGallery();
        }
      } catch (err) {
        console.error("Failed to convert image " + q.file.name + ":", err);
        q.result = { error: true };
        renderGallery();
      }
      
      progressFill.style.width = `${((i + 1) / queuedFiles.length) * 100}%`;
      progressLabel.textContent = `${t.converting} ${i + 1} ${t.of} ${queuedFiles.length}...`;
    }

    // Clean up offscreen canvas to release GPU memory
    canvas.width = 1;
    canvas.height = 1;
    const cleanupCtx = canvas.getContext('2d');
    if (cleanupCtx) cleanupCtx.clearRect(0, 0, 1, 1);

    convertBtnText.textContent = isCompression ? t.compressImages : (document.body.dataset.mode === 'pdf' ? (t.compilePdf || 'Compile PDF') : t.convertImages);

    batchCountText.innerHTML = `<strong>${convertedFiles.length}</strong> ${t.filesProcessed}`;
    batchSizeOrig.innerHTML = `${t.original}: <strong>${fmtBytes(totalOrigSize)}</strong>`;

    const savingsPct = totalOrigSize > 0 ? Math.round((1 - totalNewSize / totalOrigSize) * 100) : 0;
    const pillClass = savingsPct >= 0 ? 'savings-pill' : 'savings-pill worse';
    const pillText = savingsPct >= 0 ? `↓ ${savingsPct}% ${t.smaller}` : `↑ ${Math.abs(savingsPct)}% ${t.larger}`;
    batchSizeNew.innerHTML = `${t.processed}: <strong style="color:#d8b4fe">${fmtBytes(totalNewSize)}</strong> <span class="${pillClass}">${pillText}</span>`;
    
    progressLabel.textContent = '';
    
    if (document.body.dataset.mode === 'pdf') {
        downloadText.textContent = t.downloadPdf || 'Download PDF Document';
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
         <img src="${origUrl}" class="ba-img ba-img-orig" alt="Original image preview before compression" />
         <div class="ba-label ba-label-orig">${t.original || 'Original'}</div>
         
         <img id="afterImg" src="${newUrl}" class="ba-img ba-img-new" alt="Optimized image preview after compression" />
         <div class="ba-label ba-label-new">${t.processed || 'Optimized'}</div>
         
         <div id="baLine" class="ba-line">
           <div class="ba-slider-thumb">
             <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
           </div>
         </div>
         <input type="range" class="ba-slider" id="baSlider" min="0" max="100" value="50" aria-label="Comparison slider">
       `;

       const slider = baContainer.querySelector('.ba-slider');
       const afterImg = baContainer.querySelector('#afterImg');
       const baLine = baContainer.querySelector('#baLine');
       if (slider && afterImg && baLine) {
         slider.addEventListener('input', (e) => {
           const val = e.target.value;
           afterImg.style.clipPath = `inset(0 0 0 ${val}%)`;
           baLine.style.left = `${val}%`;
         });
       }
    }

    resultCard.classList.add('visible');
    resultCard.classList.add('success-anim');
    showToast(t.success, 'success');
    setTimeout(() => progressContainer.classList.remove('visible'), 1000);

    // Smooth transition: bring results and download button directly into center view
    setTimeout(() => {
      const dlBtn = document.getElementById('downloadBtn') || resultCard;
      dlBtn.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 250);
  });

  const getPngBlobForClipboard = async (blob) => {
    if (blob.type === 'image/png') return blob;
    return new Promise((resolve, reject) => {
      const img = new Image();
      const url = URL.createObjectURL(blob);
      img.onload = () => {
        URL.revokeObjectURL(url);
        const c = document.createElement('canvas');
        c.width = img.naturalWidth || img.width;
        c.height = img.naturalHeight || img.height;
        const ctx = c.getContext('2d');
        ctx.drawImage(img, 0, 0);
        c.toBlob((pngBlob) => {
          if (pngBlob) resolve(pngBlob);
          else reject(new Error('Canvas export failed'));
        }, 'image/png');
      };
      img.onerror = (e) => {
        URL.revokeObjectURL(url);
        reject(e);
      };
      img.src = url;
    });
  };

  if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        if (convertedFiles.length !== 1) return;
        try {
          const pngBlob = await getPngBlobForClipboard(convertedFiles[0].blob);
          const item = new ClipboardItem({ 'image/png': pngBlob });
          await navigator.clipboard.write([item]);
          copyBtn.classList.add('success');
          const origIcon = copyBtn.innerHTML;
          copyBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
          showToast(t.copiedClipboard, 'success');
          setTimeout(() => { 
              copyBtn.classList.remove('success'); 
              copyBtn.innerHTML = origIcon;
          }, 2000);
        } catch (err) {
          console.warn('Clipboard write failed:', err);
          showToast(t.copyBlocked, 'error');
        }
      });
  }

  downloadBtn.addEventListener('click', async () => {
    if (convertedFiles.length === 0) return;

    if (document.body.dataset.mode === 'pdf') {
        if (typeof window.jspdf === 'undefined') {
            downloadText.textContent = t.loadingPdf || 'Loading PDF Library...';
            try {
                await loadPdfLibrary();
            } catch (e) {
                showToast(t.pdfNotLoaded || 'Failed to load PDF library. Please refresh.', 'error');
                downloadText.textContent = t.downloadPdf || 'Download PDF Document';
                return;
            }
        }
        downloadText.textContent = t.buildingPdf || 'Building PDF...';
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF({ format: 'a4', unit: 'mm' });
        
        const marginMm = 10; // Standard 10mm margins for print-safe documents
        const margin = marginMm;
        
        for (let i = 0; i < convertedFiles.length; i++) {
            if (i > 0) doc.addPage();
            const blobType = convertedFiles[i].blob.type || 'image/jpeg';
            const base64data = await new Promise(resolve => {
                const reader = new FileReader();
                reader.onloadend = () => resolve(reader.result);
                reader.readAsDataURL(convertedFiles[i].blob);
            });
            const imgProps = doc.getImageProperties(base64data);
            const pdfWidth = doc.internal.pageSize.getWidth();
            const pageHeight = doc.internal.pageSize.getHeight();
            
            const maxW = pdfWidth - (margin * 2);
            const maxH = pageHeight - (margin * 2);
            
            let finalW = maxW;
            let finalH = (imgProps.height * maxW) / imgProps.width;
            
            if (finalH > maxH) {
                finalH = maxH;
                finalW = (imgProps.width * maxH) / imgProps.height;
            }
            
            const x = margin + ((maxW - finalW) / 2);
            const y = margin + ((maxH - finalH) / 2);
            
            let imgFormat = 'JPEG';
            if (blobType === 'image/png') imgFormat = 'PNG';
            else if (blobType === 'image/webp') imgFormat = 'WEBP';

            doc.addImage(base64data, imgFormat, x, y, finalW, finalH);
        }
        const pdfFileName = convertedFiles.length === 1 
            ? `${convertedFiles[0].name.replace(/\.[^.]+$/, '')}.pdf`
            : 'ImgLab_Converted_Documents.pdf';
        doc.save(pdfFileName);
        downloadText.textContent = t.downloadPdf || 'Download PDF Document';
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
        const usedNames = new Set();
        convertedFiles.forEach(cf => {
          let name = cf.name;
          if (usedNames.has(name)) {
            const dotIdx = name.lastIndexOf('.');
            const base = dotIdx !== -1 ? name.slice(0, dotIdx) : name;
            const ext = dotIdx !== -1 ? name.slice(dotIdx) : '';
            let counter = 1;
            while (usedNames.has(`${base} (${counter})${ext}`)) {
              counter++;
            }
            name = `${base} (${counter})${ext}`;
          }
          usedNames.add(name);
          zip.file(name, cf.blob);
        });
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
        script.crossOrigin = 'anonymous';
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
