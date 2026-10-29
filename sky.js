/* Local interaction only; no star or pointer positions are sent over the network. */
(() => {
  'use strict';
  const map = document.getElementById('celestial-map');
  const trigger = document.querySelector('[data-sky-trigger]');
  if (!map || !trigger) return;
  const root = document.documentElement;
  const lines = map.querySelector('.virgo-lines');
  const paths = [...lines.querySelectorAll('path')];
  const originalStars = map.querySelector('.sky-stars');
  const svg = 'http://www.w3.org/2000/svg';
  const node = (tag, attributes = {}) => {
    const element = document.createElementNS(svg, tag);
    Object.entries(attributes).forEach(([name, value]) => element.setAttribute(name, value));
    return element;
  };
  const definitions = node('defs');
  const revealGradient = node('radialGradient', { id:'ov-day-star-gradient', gradientUnits:'userSpaceOnUse', cx:0, cy:0, r:1 });
  revealGradient.append(node('stop', { offset:0, 'stop-color':'white' }),
                        node('stop', { offset:'.45', 'stop-color':'white' }),
                        node('stop', { offset:1, 'stop-color':'black' }));
  const revealMask = node('mask', { id:'ov-day-star-mask', maskUnits:'userSpaceOnUse', x:-2000, y:-2000, width:5000, height:5000 });
  revealMask.append(node('rect', { x:-2000, y:-2000, width:5000, height:5000, fill:'url(#ov-day-star-gradient)' }));
  definitions.append(revealGradient, revealMask);
  map.prepend(definitions);
  const starGlints = originalStars.cloneNode(true);
  starGlints.setAttribute('class', 'sky-stars-hover');
  starGlints.setAttribute('fill', '#FFF');
  starGlints.setAttribute('mask', 'url(#ov-day-star-mask)');
  starGlints.dataset.active = 'false';
  map.insertBefore(starGlints, lines);
  let hovered = false, focused = false, signatureHovered = false, raf = 0, pointer = null, starPointer = null;
  let segments = [];
  const paintStars = () => {
    const matrix = map.getScreenCTM();
    const active = starPointer && matrix && !document.hidden && root.dataset.theme !== 'dark';
    starGlints.dataset.active = String(Boolean(active));
    if (!active) return;
    const local = new DOMPoint(starPointer.x, starPointer.y).matrixTransform(matrix.inverse());
    revealGradient.setAttribute('cx', local.x);
    revealGradient.setAttribute('cy', local.y);
    revealGradient.setAttribute('r', Math.min(190, innerWidth * .4) / Math.hypot(matrix.a, matrix.b));
  };
  const update = () => {
    root.dataset.virgoVisible = String(hovered || focused || signatureHovered);
  };
  function fit() {
    const bounds = lines.getBBox();
    const center = innerWidth <= 640 ? bounds.x + bounds.width / 2 : 600;
    map.setAttribute('viewBox', `${center - 600} 0 1200 1000`);
    const matrix = map.getScreenCTM();
    if (!matrix) return;
    const toScreen = (x, y) => new DOMPoint(x, y).matrixTransform(matrix);
    const sun = toScreen(Number(map.dataset.sunX), Number(map.dataset.sunY));
    root.style.setProperty('--solar-x', `${sun.x / innerWidth * 100}%`);
    root.style.setProperty('--solar-y', `${sun.y / innerHeight * 100}%`);
    segments = [];
    paths.forEach(path => {
      const values = path.getAttribute('d').match(/-?\d+(?:\.\d+)?/g).map(Number);
      const points = [];
      for (let i = 0; i < values.length; i += 2) points.push(toScreen(values[i], values[i + 1]));
      for (let i = 1; i < points.length; i++) segments.push([points[i - 1], points[i]]);
    });
    paintStars();
  }
  const nearSegment = (p, a, b) => {
    const dx = b.x - a.x, dy = b.y - a.y;
    const length = dx * dx + dy * dy;
    const t = length ? Math.max(0, Math.min(1, ((p.x - a.x) * dx + (p.y - a.y) * dy) / length)) : 0;
    return (p.x - a.x - t * dx) ** 2 + (p.y - a.y - t * dy) ** 2 < 32 ** 2;
  };
  const readPointer = () => {
    raf = 0;
    paintStars();
    const next = pointer && segments.some(([a, b]) => nearSegment(pointer, a, b));
    if (Boolean(next) !== hovered) { hovered = Boolean(next); update(); }
  };
  document.addEventListener('pointermove', event => {
    if (event.pointerType !== 'mouse' && event.pointerType !== 'pen') return;
    starPointer = { x:event.clientX, y:event.clientY };
    pointer = event.target.closest('a,button,input,select,textarea') ? null : { x:event.clientX, y:event.clientY };
    if (!raf) raf = requestAnimationFrame(readPointer);
  }, { passive:true });
  document.addEventListener('pointerout', event => {
    if (event.relatedTarget === null) { pointer = null; starPointer = null; paintStars(); hovered = false; signatureHovered = false; update(); }
  });
  trigger.addEventListener('pointerenter', event => { if (event.pointerType !== 'touch') { signatureHovered = true; update(); } });
  trigger.addEventListener('pointerleave', () => { signatureHovered = false; update(); });
  trigger.addEventListener('focus', () => { focused = true; update(); });
  trigger.addEventListener('blur', () => { focused = false; update(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') { hovered = false; focused = false; signatureHovered = false; update(); }
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { pointer = null; starPointer = null; paintStars(); hovered = false; focused = false; signatureHovered = false; update(); }
  });
  addEventListener('blur', () => { starPointer = null; paintStars(); });
  addEventListener('resize', fit, { passive:true });
  root.classList.add('sky-ready');
  fit();
  update();
})();
