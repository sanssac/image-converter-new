// ── Toast System ──────────────────────
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;
  const el = document.createElement('div');
  el.className = `toast ${type}`;
  el.innerHTML = `<span>${message}</span>`;
  container.appendChild(el);
  setTimeout(() => {
    el.style.animation = 'toastFadeOut 0.3s forwards';
    setTimeout(() => el.remove(), 300);
  }, 3000);
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
  
  if (!dropZone || !convertBtn) return; // Not a converter page
  
  const dropZoneH2 = dropZone.querySelector('h2');
  const defaultDropText = dropZoneH2 ? dropZoneH2.textContent : 'Drop images here';
  
  const progressContainer = document.getElementById('progressContainer');
  const progressFill = document.getElementById('progressFill');

  const urlModal = document.getElementById('urlModal');
  const urlInput = document.getElementById('urlInput');
  const btnUrl = document.getElementById('btnUrl');
  const btnUrlCancel = document.getElementById('btnUrlCancel');
  const btnUrlFetch = document.getElementById('btnUrlFetch');
  
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

  let queuedFiles = [];
  let convertedFiles = []; 

  function fmtBytes(b) {
    if (!b) return '0 B';
    const k = 1024, units = ['B','KB','MB','GB'];
    const i = Math.floor(Math.log(b) / Math.log(k));
    return (b / k ** i).toFixed(1) + ' ' + units[i];
  }

  if (btnUrl) btnUrl.addEventListener('click', (e) => { e.stopPropagation(); urlModal.classList.add('visible'); urlInput.focus(); });
  if (btnUrlCancel) btnUrlCancel.addEventListener('click', (e) => { e.stopPropagation(); urlModal.classList.remove('visible'); });
  if (urlModal) urlModal.addEventListener('click', (e) => e.stopPropagation());
  
  if (btnUrlFetch) btnUrlFetch.addEventListener('click', async (e) => {
    e.stopPropagation();
    const url = urlInput.value.trim();
    if (!url) return;
    btnUrlFetch.textContent = 'Fetching...';
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error('Fetch failed');
      const blob = await res.blob();
      const fname = url.split('/').pop().split('?')[0] || 'downloaded-image';
      const file = new File([blob], fname, { type: blob.type });
      handleFiles([file]);
      urlModal.classList.remove('visible');
      urlInput.value = '';
      showToast('Image fetched successfully!', 'success');
    } catch (err) {
      showToast('CORS Block: The server rejected anonymous access.', 'error');
    }
    btnUrlFetch.textContent = 'Fetch Image';
  });

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
      if (ext === 'heic' || ext === 'heif') {
         if (typeof heic2any === 'undefined') {
           showToast('HEIC library not loaded yet.', 'error');
           continue;
         }
         try {
           const queueId = Math.random().toString(36).substr(2, 9);
           queuedFiles.push({ file: f, result: null, id: queueId, processing: true });
           renderGallery();
           
           const conversionResult = await heic2any({ blob: f, toType: 'image/jpeg' });
           const blob = Array.isArray(conversionResult) ? conversionResult[0] : conversionResult;
           fileToQueue = new File([blob], f.name.replace(/\.[^.]+$/, '.jpg'), { type: 'image/jpeg' });
           
           const qItem = queuedFiles.find(q => q.id === queueId);
           if (qItem) { qItem.file = fileToQueue; qItem.processing = false; renderGallery(); }
           continue;
         } catch (e) {
           showToast(`Failed to process HEIC: ${f.name}`, 'error');
           queuedFiles = queuedFiles.filter(q => q.id !== queueId);
           continue;
         }
      }
      queuedFiles.push({ file: fileToQueue, result: null, id: Math.random().toString(36).substr(2, 9), processing: false });
    }
    renderGallery();
    if (wasEmpty && queuedFiles.length > 0) {
      setTimeout(() => {
        convertBtn.scrollIntoView({ behavior: 'smooth', block: 'end' });
      }, 100);
    }
  }

  window.removeFile = function(id) {
    queuedFiles = queuedFiles.filter(q => q.id !== id);
    renderGallery();
  }

  function renderGallery() {
    if (queuedFiles.length === 0) {
      fileGallery.classList.remove('visible');
      convertBtn.classList.remove('visible');
      if (dropZoneH2) dropZoneH2.textContent = defaultDropText;
      return;
    }
    if (dropZoneH2) dropZoneH2.textContent = `${queuedFiles.length} file(s) selected - Drop more?`;
    
    fileGallery.innerHTML = '';
    queuedFiles.forEach((q, index) => {
      const div = document.createElement('div');
      div.className = `file-item ${q.result ? 'done' : ''}`;
      div.id = `item-${q.id}`;
      div.style.animationDelay = `${index * 0.05}s`;
      
      const url = q.processing ? '' : URL.createObjectURL(q.file);
      const thumbElement = q.processing 
          ? `<div class="skeleton-loader"></div>`
          : `<img src="${url}" />`;
          
      div.innerHTML = `
        <div class="thumb">${thumbElement}</div>
        <div class="info">
          <div class="name" title="${q.file.name}">${q.file.name}</div>
          <div class="meta">${q.processing ? 'Decoding HEIC...' : fmtBytes(q.file.size)} ${q.result ? '→ ' + (q.result.error ? '<span style="color:#ef4444">Failed</span>' : fmtBytes(q.result.size)) : ''}</div>
        </div>
        <div class="status">Done</div>
        <button class="btn-remove remove" aria-label="Remove file" onclick="removeFile('${q.id}')" ${q.processing ? 'disabled' : ''}>
           <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
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
    convertBtnText.textContent = 'Converting...';
    progressContainer.classList.add('visible');
    progressFill.style.width = '0%';
    
    const targetMime = selectedMime; 
    const targetExtMap = { 'image/jpeg':'jpg', 'image/png':'png', 'image/webp':'webp' };
    const targetExt = targetExtMap[targetMime] || 'jpg';
    
    const isCompression = document.body.dataset.mode === 'compress';
    const quality = isCompression ? 0.7 : 0.92;

    convertedFiles = [];
    let totalOrigSize = 0;
    let totalNewSize = 0;

    for (let i = 0; i < queuedFiles.length; i++) {
      let q = queuedFiles[i];
      if (q.result) {
         convertedFiles.push({ name: `${q.file.name.replace(/\.[^.]+$/, '')}.${targetExt}`, blob: q.result });
         totalOrigSize += q.file.size;
         totalNewSize += q.result.size;
      } else {
         totalOrigSize += q.file.size;
         const objUrl = URL.createObjectURL(q.file);
         const blob = await new Promise((resolve) => {
           const img = new Image();
           img.onerror = () => {
             URL.revokeObjectURL(objUrl);
             resolve({ error: true });
           };
           img.onload = async () => {
             let width = img.naturalWidth;
             let height = img.naturalHeight;

             canvas.width = width;
             canvas.height = height;
             const ctx = canvas.getContext('2d');
             
             if (targetMime === 'image/jpeg') {
               ctx.fillStyle = '#ffffff';
               ctx.fillRect(0, 0, width, height);
             }
             
             ctx.drawImage(img, 0, 0, width, height);
             canvas.toBlob((b) => {
               URL.revokeObjectURL(objUrl);
               resolve(b);
             }, targetMime, targetMime !== 'image/png' ? quality : undefined);
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
    }

    convertBtnText.textContent = isCompression ? 'Compress Images' : 'Convert Images';

    batchCountText.innerHTML = `<strong>${convertedFiles.length}</strong> file(s) processed`;
    batchSizeOrig.innerHTML = `Original: <strong>${fmtBytes(totalOrigSize)}</strong>`;
    batchSizeNew.innerHTML = `Processed: <strong style="color:#d8b4fe">${fmtBytes(totalNewSize)}</strong>`;
    
    downloadText.textContent = convertedFiles.length > 1 ? 'Download ZIP' : `Download ${targetExt.toUpperCase()}`;
    if (copyBtn) copyBtn.style.display = convertedFiles.length === 1 ? 'flex' : 'none';

    resultCard.classList.add('visible');
    showToast('Success!', 'success');
    setTimeout(() => progressContainer.classList.remove('visible'), 1000);
  });

  if (copyBtn) {
      copyBtn.addEventListener('click', async () => {
        if (convertedFiles.length !== 1) return;
        try {
          const item = new ClipboardItem({ [convertedFiles[0].blob.type]: convertedFiles[0].blob });
          await navigator.clipboard.write([item]);
          copyBtn.classList.add('success');
          showToast('Image copied to clipboard!', 'success');
          setTimeout(() => copyBtn.classList.remove('success'), 2000);
        } catch (err) {
          showToast('Clipboard copy requires HTTPS or secure context.', 'error');
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
        showToast("JSZip library has not loaded yet.", "error"); return;
      }
      downloadText.textContent = 'Composing ZIP...';
      const zip = new JSZip();
      convertedFiles.forEach(cf => zip.file(cf.name, cf.blob));
      const zipBlob = await zip.generateAsync({ type: 'blob' });
      const url = URL.createObjectURL(zipBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = isCompression ? 'Compressed_Images.zip' : 'Converted_Images.zip';
      document.body.appendChild(a);
      a.click();
      setTimeout(() => { URL.revokeObjectURL(url); document.body.removeChild(a); }, 500);
      downloadText.textContent = 'Download ZIP';
    }
  });
});
