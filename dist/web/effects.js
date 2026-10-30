/* Effetti locali: nessun ciclo di rendering quando la luce è ferma. */
(() => {
  'use strict';
  const root = document.documentElement;
  if (root.dataset.effectsReady === 'true') return;
  root.dataset.effectsReady = 'true';
  root.classList.add('js');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let reduce = motion.matches;
  const hasObserver = typeof IntersectionObserver !== 'undefined';

  // Il browser mantiene il giro; il passaggio del puntatore lo rallenta al 6%
  // senza cambiare durata o posizione. Nessun ciclo JS per l'animazione.
  const marqueeStates = new Map();
  document.querySelectorAll('.marquee-langs').forEach(marquee => {
    const strip = marquee.closest('.language-strip');
    if (!strip || !marquee.firstElementChild || typeof marquee.getAnimations !== 'function' ||
        typeof Animation === 'undefined' || typeof Animation.prototype.updatePlaybackRate !== 'function') return;
    if (!marquee.querySelector('[data-marquee-copy]')) {
      const clone = marquee.firstElementChild.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      clone.setAttribute('inert', '');
      clone.setAttribute('data-marquee-copy', '');
      marquee.append(clone);
    }
    marqueeStates.set(marquee, { strip, hovered:false, visible:!hasObserver });
    strip.classList.add('motion-ready');
    marquee.classList.add('marquee-ready');
  });
  let pageSuspended = false;
  const updateMarquees = () => marqueeStates.forEach((state, marquee) => {
    marquee.style.animationPlayState = reduce || document.hidden || pageSuspended || !state.visible ? 'paused' : 'running';
    const rate = state.hovered ? .06 : 1;
    marquee.getAnimations().forEach(animation => {
      if (animation.animationName === 'marquee' && animation.playbackRate !== rate) animation.updatePlaybackRate(rate);
    });
  });
  marqueeStates.forEach((state) => {
    state.strip.addEventListener('pointerenter', event => {
      if (event.pointerType !== 'mouse' && event.pointerType !== 'pen') return;
      state.hovered = true;
      updateMarquees();
    });
    state.strip.addEventListener('pointerleave', () => {
      state.hovered = false;
      updateMarquees();
    });
  });
  if (hasObserver && marqueeStates.size) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => { marqueeStates.get(entry.target).visible = entry.isIntersecting; });
      updateMarquees();
    });
    marqueeStates.forEach((state, marquee) => observer.observe(marquee));
  }
  updateMarquees();

  const bar = document.querySelector('.bar');
  const spot = document.querySelector('.spot');
  const lit = [...document.querySelectorAll('[data-lit]')];
  const visible = new Set(hasObserver ? [] : lit);
  let tx = 0, ty = 0, lx = 0, ly = 0;
  let hasInput = false, raf = 0, lastFrame = 0;
  const solarPosition = () => {
    const solar = getComputedStyle(root);
    const x = parseFloat(solar.getPropertyValue('--solar-x'));
    const y = parseFloat(solar.getPropertyValue('--solar-y'));
    tx = innerWidth * (Number.isFinite(x) ? x : 50) / 100;
    ty = innerHeight * (Number.isFinite(y) ? y : 25) / 100;
  };
  solarPosition();
  lx = tx; ly = ty;
  const set = (style, name, value) => {
    if (style.getPropertyValue(name) !== value) style.setProperty(name, value);
  };
  const paint = () => {
    if (bar) bar.classList.toggle('scrolled', scrollY > 40);
    // Read geometry as one batch before writing any style properties.
    const cards = [...visible].map(element => ({ element, bounds:element.getBoundingClientRect() }))
      .filter(({ bounds }) => bounds.bottom >= -200 && bounds.top <= innerHeight + 200);
    if (spot) {
      set(spot.style, '--lx', lx.toFixed(1) + 'px');
      set(spot.style, '--ly', ly.toFixed(1) + 'px');
    }
    cards.forEach(({ element, bounds:r }) => {
      const dx = Math.max(r.left - lx, 0, lx - r.right);
      const dy = Math.max(r.top - ly, 0, ly - r.bottom);
      const k = Math.max(0, 1 - Math.hypot(dx, dy) / 700);
      const vx = (r.left + r.width / 2 - lx) / Math.max(r.width, 1);
      const vy = (r.top + r.height / 2 - ly) / Math.max(r.height, 1);
      set(element.style, '--x', (lx - r.left).toFixed(0) + 'px');
      set(element.style, '--y', (ly - r.top).toFixed(0) + 'px');
      set(element.style, '--k', k.toFixed(3));
      set(element.style, '--sx', (Math.max(-1, Math.min(1, vx)) * 22 * k).toFixed(1) + 'px');
      set(element.style, '--sy', (18 + Math.max(-1, Math.min(1, vy)) * 14 * k).toFixed(1) + 'px');
    });
  };
  const stop = () => {
    if (raf) cancelAnimationFrame(raf);
    raf = 0;
    lastFrame = 0;
  };
  const tick = time => {
    raf = 0;
    if (document.hidden || root.classList.contains('profile-is-open')) {
      lastFrame = 0;
      return;
    }
    // sky.js may have refined the Sun position since this file was loaded.
    if (!hasInput) solarPosition();
    const delta = lastFrame ? Math.min(64, Math.max(1, time - lastFrame)) : 1000 / 60;
    lastFrame = time;
    const ease = reduce ? 1 : 1 - Math.exp(-delta / 165);
    lx += (tx - lx) * ease;
    ly += (ty - ly) * ease;
    const moving = Math.abs(tx - lx) + Math.abs(ty - ly) > .5;
    if (!moving || reduce) { lx = tx; ly = ty; }
    paint();
    if (moving && !reduce) raf = requestAnimationFrame(tick);
    else lastFrame = 0;
  };
  const wake = () => {
    if (!raf && !document.hidden && !root.classList.contains('profile-is-open')) raf = requestAnimationFrame(tick);
  };
  if (hasObserver) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => entry.isIntersecting ? visible.add(entry.target) : visible.delete(entry.target));
      wake();
    }, { rootMargin:'200px' });
    lit.forEach(element => observer.observe(element));
  }
  const target = event => {
    if (reduce || root.classList.contains('profile-is-open')) return;
    hasInput = true;
    tx = event.clientX;
    ty = event.clientY;
    wake();
  };
  addEventListener('pointermove', event => {
    if (event.pointerType === 'mouse' || event.pointerType === 'pen') target(event);
  }, { passive:true });
  addEventListener('pointerdown', target, { passive:true });
  addEventListener('scroll', wake, { passive:true });
  addEventListener('resize', wake, { passive:true });
  const refresh = () => { lastFrame = 0; updateMarquees(); wake(); };
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) stop();
    else refresh();
    updateMarquees();
  });
  addEventListener('pagehide', () => { pageSuspended = true; stop(); updateMarquees(); });
  addEventListener('pageshow', () => { pageSuspended = false; refresh(); });
  addEventListener('focus', refresh);

  // Reveal once; unavailable observers or reduced motion always show content.
  const revealed = [...document.querySelectorAll('[data-reveal]')];
  let revealObserver;
  if (!reduce && hasObserver) {
    revealObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.remove('pending');
      revealObserver.unobserve(entry.target);
    }), { threshold:.12, rootMargin:'0px 0px -40px 0px' });
    revealed.forEach(element => {
      if (element.getBoundingClientRect().top < innerHeight) return;
      element.classList.add('pending');
      revealObserver.observe(element);
    });
  } else revealed.forEach(element => element.classList.remove('pending'));
  const onMotion = event => {
    reduce = event.matches;
    if (reduce) {
      stop();
      if (revealObserver) revealObserver.disconnect();
      revealed.forEach(element => element.classList.remove('pending'));
      hasInput = false;
      solarPosition();
      lx = tx; ly = ty;
    }
    updateMarquees();
    wake();
  };
  if (motion.addEventListener) motion.addEventListener('change', onMotion);
  else if (motion.addListener) motion.addListener(onMotion);
  wake();
})();
