export function initLangSwitcher() {
  const navContainer = document.querySelector('header nav');
  const currentDocLang = document.documentElement.lang || 'en';

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
      <div class="lang-menu"></div>
    `;

    const langMenuDiv = switcherDiv.querySelector('.lang-menu');
    Object.entries(langNames).forEach(([code, name]) => {
      let newPath = pathWithoutLang;
      if (code !== 'en') {
        newPath = '/' + code + (pathWithoutLang === '/' ? '/' : pathWithoutLang);
      }
      newPath = newPath.replace(/\/\//g, '/');
      const a = document.createElement('a');
      a.href = newPath;
      a.className = 'lang-opt ' + (code === currentDocLang ? 'active' : '');
      a.textContent = name;
      langMenuDiv.appendChild(a);
    });
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
