/* L'intro è decorativa; il contenuto non attende il completamento dell'animazione. */
(() => {
  const root = document.documentElement;
  const intro = document.querySelector('.brand-intro');
  if (!intro) return;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');
  if (!root.classList.contains('intro-pending') || reduce.matches) {
    intro.remove();
    root.classList.remove('intro-pending');
    return;
  }
  const listeners = new AbortController();
  let timeout;
  const finish = () => {
    clearTimeout(timeout);
    listeners.abort();
    intro.remove();
    root.classList.remove('intro-pending');
  };
  const options = { signal:listeners.signal };
  intro.addEventListener('animationend', event => { if (event.target === intro && event.animationName === 'intro-exit') finish(); }, options);
  document.addEventListener('keydown', finish, options);
  document.addEventListener('pointerdown', finish, options);
  addEventListener('pageshow', event => { if (event.persisted) finish(); }, options);
  reduce.addEventListener('change', event => { if (event.matches) finish(); }, options);
  // Fallback anche con foglio CSS mancante o animazioni disabilitate dal browser.
  timeout = setTimeout(finish, 2400);
})();
