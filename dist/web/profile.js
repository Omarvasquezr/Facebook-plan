/* Una sola scheda personale, migliorata da sezione a dialogo. Nessun dato inviato. */
(() => {
  'use strict';
  const card = document.getElementById('about-omar');
  if (!card || typeof HTMLDialogElement === 'undefined' || !HTMLDialogElement.prototype.showModal) return;

  const dialog = document.createElement('dialog');
  dialog.id = 'profile-dialog';
  dialog.className = 'profile-dialog';
  dialog.setAttribute('aria-labelledby', 'profile-title');
  dialog.append(card);
  document.body.append(dialog);
  const close = card.querySelector('[data-profile-close]');
  close.hidden = false;
  // Il pulsante rimane fuori dal contenuto scorrevole della scheda.
  dialog.prepend(close);
  let opener;
  let scrollPosition = 0;
  let backdropStart = false;
  const root = document.documentElement;
  const syncViewport = () => {
    if (dialog.open) root.style.setProperty('--profile-viewport-height', `${Math.round(window.visualViewport?.height || innerHeight)}px`);
  };

  const openProfile = link => {
    if (dialog.open) return;
    opener = link;
    scrollPosition = scrollY;
    root.style.setProperty('--profile-scroll-top', `${-scrollPosition}px`);
    root.classList.add('profile-is-open');
    dialog.showModal();
    syncViewport();
    card.scrollTop = 0;
    dialog.scrollTop = 0;
    close.focus({ preventScroll:true });
  };

  document.querySelectorAll('[data-profile-open]').forEach(link => {
    link.setAttribute('aria-haspopup', 'dialog');
    link.setAttribute('aria-controls', dialog.id);
    link.addEventListener('click', event => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      openProfile(link);
    });
  });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('pointerdown', event => { backdropStart = event.target === dialog; });
  dialog.addEventListener('click', event => {
    if (backdropStart && event.target === dialog) {
      const bounds = dialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
    }
    backdropStart = false;
  });
  dialog.addEventListener('close', () => {
    root.classList.remove('profile-is-open');
    root.style.removeProperty('--profile-scroll-top');
    root.style.removeProperty('--profile-viewport-height');
    if (opener?.isConnected) opener.focus({ preventScroll:true });
    window.scrollTo(0, scrollPosition);
  });
  addEventListener('resize', syncViewport, { passive:true });
  window.visualViewport?.addEventListener('resize', syncViewport, { passive:true });
  if (location.hash === '#about-omar') openProfile(document.getElementById('profile-open'));
})();
