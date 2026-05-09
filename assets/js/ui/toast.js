// ── Toast System ──────────────────────
export function showToast(message, type = 'info') {
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
