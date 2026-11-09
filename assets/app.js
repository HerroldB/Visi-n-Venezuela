(() => {
  'use strict';
  const menuBtn = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.main-nav');
  const groups = Array.from(document.querySelectorAll('.nav-group'));
  function closeGroups(except = null) {
    groups.forEach(group => {
      if (group !== except) {
        group.classList.remove('is-open');
        group.querySelector('.nav-trigger')?.setAttribute('aria-expanded', 'false');
      }
    });
  }
  function closeMenu() {
    nav?.classList.remove('menu-open');
    menuBtn?.setAttribute('aria-expanded', 'false');
    menuBtn?.setAttribute('aria-label', 'Abrir menú de navegación');
    closeGroups();
  }
  menuBtn?.addEventListener('click', () => {
    const opened = nav.classList.toggle('menu-open');
    menuBtn.setAttribute('aria-expanded', String(opened));
    menuBtn.setAttribute('aria-label', opened ? 'Cerrar menú de navegación' : 'Abrir menú de navegación');
    if (!opened) closeGroups();
  });
  groups.forEach(group => {
    const trigger = group.querySelector('.nav-trigger');
    trigger.addEventListener('click', event => {
      event.stopPropagation();
      const opened = group.classList.contains('is-open');
      closeGroups(group);
      group.classList.toggle('is-open', !opened);
      trigger.setAttribute('aria-expanded', String(!opened));
    });
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.nav-group')) closeGroups();
    if (window.matchMedia('(max-width: 980px)').matches && !event.target.closest('.header-inner')) closeMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      closeMenu();
      menuBtn?.focus();
    }
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 980) closeMenu();
  });
  nav?.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    if (window.innerWidth <= 980) closeMenu();
  }));
})();
