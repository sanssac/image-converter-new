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
      console.log('SW registration failed: ', err);
    });
  });
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

    // ── Language Switcher Component ──────
    const navContainer = document.querySelector('header nav');
    if (navContainer && !document.querySelector('.lang-switcher')) {
      const currentDocLang = document.documentElement.lang || 'en';
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
    en:  { converting: 'Converting', of: 'of', filesSelected: 'file(s) selected - Drop more?', convertMore: 'Convert More Images', compressImages: 'Compress Images', convertImages: 'Convert Images', success: 'Success!', filesProcessed: 'file(s) processed', original: 'Original', processed: 'Processed', smaller: 'smaller', larger: 'larger', downloadZip: 'Download ZIP', download: 'Download', zipping: 'Zipping', copiedClipboard: 'Image copied to clipboard!', copyBlocked: 'Browser blocked clipboard copy.', copyNotSupported: 'Clipboard copy not supported on this browser.', heicNotLoaded: 'HEIC library not loaded yet.', heicFailed: 'Failed to process HEIC', zipNotLoaded: 'JSZip library has not loaded yet.' },
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

  dropZone.addEventListener('click', () => fileInput.click());
  dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('dragging'); });
  dropZone.addEventListener('dragleave', (e) => { if (!dropZone.contains(e.relatedTarget)) dropZone.classList.remove('dragging'); });
  dropZone.addEventListener('drop', (e) => {
    e.preventDefault(); dropZone.classList.remove('dragging');
    if (e.dataTransfer.files.length) handleFiles(e.dataTransfer.files);
  });
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFiles(e.target.files);
    e.target.value = '';
  });

  async function handleFiles(files) {
    const wasEmpty = queuedFiles.length === 0;
    progressContainer.classList.remove('visible');
    resultCard.classList.remove('visible');
  
    for (let f of files) {
      const ext = f.name.split('.').pop().toLowerCase();
      
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
    convertBtnText.textContent = `${t.converting}...`;
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
      const targetExtMap = { 'image/jpeg':'jpg', 'image/png':'png', 'image/webp':'webp' };
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
             canvas.width = w; canvas.height = h;
             const ctx = canvas.getContext('2d');
             if (outMime === 'image/jpeg') {
                 ctx.fillStyle = '#ffffff';
                 ctx.fillRect(0, 0, w, h);
             }
             ctx.drawImage(imgObj, 0, 0, w, h);
             canvas.toBlob(b => res(b), outMime, outMime !== 'image/png' ? outQuality : undefined);
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
             
             if (!isCompression || !document.querySelector('.size-presets, .preset-pill, .preset')) {
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
    downloadText.textContent = convertedFiles.length > 1 ? t.downloadZip : `${t.download} ${lastTargetExt.toUpperCase()}`;
    if (copyBtn) copyBtn.style.display = convertedFiles.length === 1 ? 'flex' : 'none';

    // Before/After visual comparison injected natively for Compress Mode single files
    if (isCompression && convertedFiles.length === 1 && queuedFiles[0] && queuedFiles[0].file) {
       let baContainer = document.getElementById('beforeAfterContainer');
       if (!baContainer) {
         baContainer = document.createElement('div');
         baContainer.id = 'beforeAfterContainer';
         baContainer.style = "position:relative; width:100%; height:250px; background:rgba(0,0,0,0.2); overflow:hidden; border-radius:10px; margin-top:10px; box-shadow: inset 0 0 0 1px rgba(255,255,255,0.05);";
         resultCard.insertBefore(baContainer, resultCard.querySelector('.action-row'));
       }
       const origUrl = URL.createObjectURL(queuedFiles[0].file);
       const newUrl = URL.createObjectURL(convertedFiles[0].blob);
       // Revoke old URLs from previous compress runs to prevent memory leaks
       const oldImgs = baContainer.querySelectorAll('img');
       oldImgs.forEach(img => { if(img.src.startsWith('blob:')) URL.revokeObjectURL(img.src); });
       baContainer.innerHTML = `
         <img src="${origUrl}" style="position:absolute; width:100%; height:100%; object-fit:contain;" />
         <div style="position:absolute; top:8px; left:8px; background:rgba(0,0,0,0.6); padding:4px 8px; font-size:11px; border-radius:4px; font-weight:600; color:#fff; z-index:5;">Original</div>
         
         <img id="afterImg" src="${newUrl}" style="position:absolute; width:100%; height:100%; object-fit:contain; clip-path: inset(0 0 0 50%);" />
         <div style="position:absolute; top:8px; right:8px; background:rgba(168,85,247,0.9); padding:4px 8px; font-size:11px; border-radius:4px; font-weight:600; color:#fff; z-index:5;">Optimized</div>
         
         <div id="baLine" style="position:absolute; top:0; left:50%; width:2px; height:100%; background:#fff; pointer-events:none; box-shadow:0 0 10px rgba(0,0,0,0.8); z-index:10; display:flex; align-items:center; justify-content:center;">
           <div style="width:24px; height:24px; border-radius:50%; background:#fff; box-shadow:0 2px 6px rgba(0,0,0,0.3); display:flex; align-items:center; justify-content:center;">
             <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6366f1" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg>
           </div>
         </div>
         <input type="range" class="ba-slider" min="0" max="100" value="50" style="position:absolute; top:0; left:0; width:100%; height:100%; outline:none; margin:0; opacity:0; cursor:ew-resize; z-index:20; touch-action: pan-y;" oninput="document.getElementById('afterImg').style.clipPath = 'inset(0 0 0 ' + this.value + '%)'; document.getElementById('baLine').style.left = this.value + '%';">
       `;
    }

    resultCard.classList.add('visible');
    showToast(t.success, 'success');
    setTimeout(() => progressContainer.classList.remove('visible'), 1000);
  });

  if (copyBtn) {
      copyBtn.addEventListener('click', () => {
        if (convertedFiles.length !== 1) return;
        try {
          const item = new ClipboardItem({ [convertedFiles[0].blob.type]: convertedFiles[0].blob });
          navigator.clipboard.write([item]).then(() => {
            copyBtn.classList.add('success');
            showToast(t.copiedClipboard, 'success');
            setTimeout(() => copyBtn.classList.remove('success'), 2000);
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

    if (convertedFiles.length === 1) {
      const url = URL.createObjectURL(convertedFiles[0].blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = convertedFiles[0].name;
      document.body.appendChild(a);
      a.click();
      setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 500);
    } else {
      if (typeof JSZip === 'undefined') {
        showToast(t.zipNotLoaded, "error"); return;
      }
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
    }
  });
});
