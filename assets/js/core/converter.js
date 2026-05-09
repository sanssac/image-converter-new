import { showToast } from '../ui/toast.js';
import { escapeHtml } from '../utils/helpers.js';
import { fmtBytes } from '../utils/formatters.js';
import { getTranslations } from '../config/translations.js';

export function initConverter() {
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

  const t = getTranslations();

  // Inject clear button into result card once
  const clearBtn = document.createElement('button');
  clearBtn.id = 'clearBtn';
  clearBtn.className = 'btn-clear';
  clearBtn.innerHTML = `<svg aria-hidden="true" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4.5"/></svg>`;
  clearBtn.appendChild(document.createTextNode(' ' + t.convertMore));

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
  let isCompression = document.body.dataset.mode === 'compress' || document.body.dataset.compressMode === 'true'; 

  const btnLocal = document.getElementById('btnLocal');
  if (btnLocal) btnLocal.addEventListener('click', (e) => { e.stopPropagation(); fileInput.click(); });

  document.body.addEventListener('dragover', (e) => { 
    e.preventDefault(); 
    if (dropZone) dropZone.classList.add('dragging'); 
  });
  document.body.addEventListener('dragleave', (e) => { 
    if (!e.relatedTarget && dropZone) dropZone.classList.remove('dragging'); 
  });
  document.body.addEventListener('drop', (e) => {
    e.preventDefault(); 
    if (dropZone) dropZone.classList.remove('dragging');
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
}
