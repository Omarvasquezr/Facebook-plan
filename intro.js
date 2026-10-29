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
  const cleanup = [];
  const on = (target, type, listener) => {
    target.addEventListener(type, listener);
    cleanup.push(() => target.removeEventListener(type, listener));
  };
  let timeout;
  const finish = () => {
    clearTimeout(timeout);
    cleanup.forEach(remove => remove());
    intro.remove();
    root.classList.remove('intro-pending');
  };
  on(intro, 'animationend', event => { if (event.target === intro && event.animationName === 'intro-exit') finish(); });
  on(document, 'keydown', finish);
  on(document, 'pointerdown', finish);
  on(window, 'pageshow', event => { if (event.persisted) finish(); });
  const motionChanged = event => { if (event.matches) finish(); };
  if (reduce.addEventListener) on(reduce, 'change', motionChanged);
  else if (reduce.addListener) { reduce.addListener(motionChanged); cleanup.push(() => reduce.removeListener(motionChanged)); }
  // Fallback anche con foglio CSS mancante o animazioni disabilitate dal browser.
  timeout = setTimeout(finish, 2400);
})();
