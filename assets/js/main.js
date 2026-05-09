// ── Entry Point ───────────────────────
import { initTheme } from './ui/theme.js?v=2';
import { initMegaMenu } from './ui/megaMenu.js?v=2';
import { initLangSwitcher } from './ui/langSwitcher.js?v=2';
import { initNavHighlight, initStickyHeader, initFeatureBadges } from './ui/nav.js?v=2';
import { initFaqAccordion } from './ui/faq.js?v=2';
import { initFooterBranding } from './ui/footer.js?v=2';
import { initScrollReveal } from './ui/scrollReveal.js?v=2';
import { initConverter } from './core/converter.js?v=2';

// PWA Service Worker
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(err => {
      console.log('SW registration failed: ', err);
    });
  });
}

function initApp() {
  initTheme();
  initMegaMenu();
  initLangSwitcher();
  initNavHighlight();
  initStickyHeader();
  initFeatureBadges();
  initFaqAccordion();
  initFooterBranding();
  initScrollReveal();
  initConverter();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initApp);
} else {
  initApp();
}
