# Accessibility audit — final local build

Target: http://127.0.0.1:4195/ (generated production folder). Chromium with axe-core 4.10.3, fetched from its official npm distribution and used only by development checks.

## Final observed results

- **10 axe states passed without detected WCAG A/AA violations:** Italian, Spanish and English main page in day/night themes, plus Spanish expanded business tools and personal dialog in both themes. Rules selected: WCAG 2.0/2.1 A/AA and WCAG 2.2 AA tags.
- **6 reflow/keyboard states passed:** 320 × 568, 375 × 812, 390 × 844, 412 × 915, 812 × 375 landscape and 640 × 450. No horizontal document overflow or obscured keyboard targets were observed.
- The portrait loads with meaningful localized alternative text. The dialog keeps focus inside, permits scrolling its content, and leaves its close button clickable at the end of that content.
- Mail and phone remain ordinary `mailto:` / `tel:` links. Both public PDFs returned HTTP 200 and valid PDF headers.
- With JavaScript disabled, all four competency sections and the personal section remain readable. Each tools disclosure still opens through native HTML interaction.
- The new language-movement control was separately verified with keyboard Enter and Space: manual pause persists after focus leaves the control, and resuming restores animation. This resolves the baseline concern about automatically moving informative content without a touch/keyboard pause mechanism.
- The contact links now have a 44 px minimum height in the final compatibility stylesheet, improving their previous 32–33 px mobile targets.
- Search visibility is intentionally unchanged: the owner expressly chose to retain `noindex,nofollow`.

## Automated review limitations

Axe leaves contrast on gradients/transparency/overlays incomplete; these entries are not reported as proven passes. It also requests review of `aria-controls` references to the closed native profile dialog: the referenced target exists, opens and works. No missing-ID violation was detected.

The reflow checks cover narrow CSS viewports. Native headless Chromium zoom shortcuts did not change the viewport or pixel ratio, so this report does not describe them as a real 200% browser zoom test.

These results do not certify full WCAG compliance, physical-device behavior, VoiceOver/TalkBack operation, or Instagram's current in-app browser. The separate browser matrix is owned by the parent agent and should be read alongside this report. The pre-existing PDFs were preserved, not audited for PDF tagging or document accessibility.

## Reusable verification

`checks/accessibility_smoke.py` accepts a served URL plus optional `--axe /path/to/axe.min.js` and `--report /path/to/results.json`. The axe script is not a website dependency and is not copied into the production build.

Final output: `/workspace/review/accessibility-final-results.txt`.
Machine-readable final results: `/workspace/review/accessibility-final-results.json`.

The final full check was run before adding the explicit pause/resume assertions to the reusable script; those same assertions were then run as a targeted browser check in `/workspace/review/verify_pause_access.py`. No product files were modified by this audit agent.

## Targeted checks after final responsive refinements

- **Reduced-motion languages:** 12 states passed at 320/375/390/812 CSS px, in Italian, Spanish and English. Assertions measure each original language name and level through DOM Range fragments, requiring them to fit inside the strip track and horizontal viewport. All three remain visible while animation is disabled. This verifies the fix for the static third-language clipping found in visual review. Results: `/workspace/review/reduced-language-reflow-results.json` and `.txt`. The semantic regression helper is now part of `checks/accessibility_smoke.py`.
- **Landscape portrait:** at 812 × 375, light and dark, the complete original portrait fits inside the modal on first opening. Its natural 9:16 ratio is preserved with `object-fit:contain`, no cropping, and zero initial card scroll. The close control remains reachable both before and after scrolling the inner card. Results: `/workspace/review/landscape-portrait-results.json` and `.txt`.

These were targeted checks after the two corresponding CSS refinements; the 10-state axe audit and broad browser matrix were not repeated unnecessarily.
