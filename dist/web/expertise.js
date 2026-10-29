/* Progressive enhancement: senza JavaScript tutti i contenuti restano leggibili. */
(() => {
  'use strict';
  const section = document.getElementById('expertise');
  if (!section || section.classList.contains('expertise-ready')) return;
  const buttons = [...section.querySelectorAll('button[data-area]')];
  if (!buttons.length) return;
  const entries = buttons.map(button => ({
    button,
    panel: section.querySelector(`#area-${CSS.escape(button.dataset.area)}`)
  }));
  // Keep the unenhanced document intact if the expected markup is incomplete.
  if (entries.some(({ panel }) => !panel || !panel.hasAttribute('data-area-panel')) ||
      new Set(entries.map(({ panel }) => panel)).size !== entries.length) return;
  let selected = null;
  const revealButton = button => {
    const nav = button.closest('.area-nav');
    if (!nav) return;
    const bounds = nav.getBoundingClientRect();
    const target = button.getBoundingClientRect();
    // Keep the focused option and its outline inside the horizontal viewport.
    // Only this strip moves; the page is not scrolled or animated.
    if (target.left < bounds.left + 8) nav.scrollLeft -= bounds.left + 8 - target.left;
    else if (target.right > bounds.right - 8) nav.scrollLeft += target.right - bounds.right + 8;
  };
  const closeAll = () => {
    entries.forEach(({ button, panel }) => {
      button.setAttribute('aria-expanded', 'false');
      panel.hidden = true;
    });
    selected = null;
  };
  entries.forEach(({ button, panel }) => {
    if (!button.id) button.id = `area-toggle-${button.dataset.area}`;
    button.type = 'button';
    button.disabled = false;
    button.setAttribute('aria-controls', panel.id);
    panel.setAttribute('role', 'region');
    panel.setAttribute('aria-labelledby', button.id);
    button.addEventListener('focus', () => revealButton(button));
    button.addEventListener('click', () => {
      revealButton(button);
      const wasSelected = selected === button;
      closeAll();
      if (!wasSelected) {
        button.setAttribute('aria-expanded', 'true');
        panel.hidden = false;
        selected = button;
      }
    });
  });
  section.addEventListener('keydown', event => {
    if (event.defaultPrevented) return;
    if (event.key === 'Escape' && selected) {
      event.preventDefault();
      const trigger = selected;
      closeAll();
      trigger.focus({ preventScroll:true });
      return;
    }
    const current = buttons.indexOf(document.activeElement);
    if (current < 0 || !['ArrowLeft','ArrowRight','Home','End'].includes(event.key)) return;
    event.preventDefault();
    const index = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1 :
      (current + (event.key === 'ArrowRight' ? 1 : -1) + buttons.length) % buttons.length;
    buttons[index].focus({ preventScroll:true });
    revealButton(buttons[index]);
  });
  closeAll();
  section.classList.add('expertise-ready');
})();
