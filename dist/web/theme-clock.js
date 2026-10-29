/* Tema automatico secondo l'ora italiana; nessuna rete o posizione del visitatore. */
(() => {
  'use strict';
  let formatter;
  try {
    formatter = new Intl.DateTimeFormat('en-GB', {
      timeZone:'Europe/Rome', hour:'2-digit', hourCycle:'h23'
    });
  } catch (_) { /* Se la zona IANA manca, resta disponibile il tema del sistema. */ }

  const systemTheme = () => {
    try { return matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'; }
    catch (_) { return 'light'; }
  };

  function getTheme(date = new Date()) {
    try {
      const hour = Number(formatter.formatToParts(date).find(part => part.type === 'hour').value) % 24;
      if (!Number.isFinite(hour)) return systemTheme();
      return hour >= 18 || hour < 6 ? 'dark' : 'light';
    } catch (_) { return systemTheme(); }
  }

  function watch(callback) {
    let active = true;
    let timer;
    let previous;
    const check = () => {
      if (!active) return;
      const theme = getTheme();
      if (theme !== previous) { previous = theme; callback(theme); }
    };
    const schedule = () => {
      clearTimeout(timer);
      if (!active) return;
      // Recheck at the next minute, including DST changes and a changed clock.
      const delay = Math.max(50, 60000 - (Date.now() % 60000));
      timer = setTimeout(() => { check(); schedule(); }, delay);
    };
    const refresh = () => { check(); schedule(); };
    const onVisible = () => { if (!document.hidden) refresh(); };
    window.addEventListener('focus', refresh);
    document.addEventListener('visibilitychange', onVisible);
    check();
    schedule();
    return () => {
      active = false;
      clearTimeout(timer);
      window.removeEventListener('focus', refresh);
      document.removeEventListener('visibilitychange', onVisible);
    };
  }

  window.OVThemeClock = Object.freeze({ getTheme, watch });
})();
