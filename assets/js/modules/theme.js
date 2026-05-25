/**
 * Theme Manager Module
 * Handles loading initial theme, theme toggling, and synchronizing state/icons.
 */
(function() {
  function initTheme() {
    const themeToggle = document.querySelector('.theme-toggle');
    if (!themeToggle) return;

    const sunIcon = themeToggle.querySelector('.sun-icon');
    const moonIcon = themeToggle.querySelector('.moon-icon');

    const setTheme = (theme) => {
      document.body.dataset.theme = theme;
      try {
        localStorage.setItem('theme', theme);
      } catch (e) {
        console.warn('localStorage is blocked or unavailable:', e);
      }
      if (theme === 'light') {
        if (sunIcon) sunIcon.style.display = 'block';
        if (moonIcon) moonIcon.style.display = 'none';
      } else {
        if (sunIcon) sunIcon.style.display = 'none';
        if (moonIcon) moonIcon.style.display = 'block';
      }
    };

    // Load initial theme safely
    let savedTheme = 'dark';
    try {
      savedTheme = localStorage.getItem('theme') || 'dark';
    } catch (e) {
      console.warn('localStorage is blocked or unavailable:', e);
    }
    setTheme(savedTheme);

    themeToggle.addEventListener('click', () => {
      document.body.classList.add('theme-transitioning');
      const currentTheme = document.body.dataset.theme || 'dark';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      setTheme(newTheme);
      setTimeout(() => {
        document.body.classList.remove('theme-transitioning');
      }, 350);
    });
  }

  // Pre-load theme instantly to prevent light flashes if script is loaded asynchronously
  let initialTheme = 'dark';
  try {
    initialTheme = localStorage.getItem('theme') || 'dark';
  } catch (e) {}
  document.body.dataset.theme = initialTheme;

  // Initialize theme toggle controls
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }
})();
