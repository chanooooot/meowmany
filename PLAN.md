# PLAN.md — Current verification gates

The original build and visual redesign are complete. SFX were deliberately
removed; do not restore them. Current work repairs the gameplay/lifecycle
review documented in REVIEW.md. Follow these gates for future changes.

1. Trace the actual input/round path before changing it. Put tunables in CONFIG.
2. Run `node tools/test-game.cjs`; add a targeted regression for new logic bugs.
   Keep one shipped HTML file and no runtime/test dependencies.
3. Check rendered landing, play, all result ranks, loss, and error states at
   phone widths and short landscape heights. Cat must finish inside the viewport,
   retreat offscreen, and keep keyboard/touch controls reachable. Check readable
   text, reduced motion, and inspectable timing/status.
4. Test actual voices on iPhone Safari and Android Chrome over HTTPS. Confirm
   gentle/low/high meows, glides, brief pitch gaps, distinct and sustained loud
   calls, calibration, drift, timeout, win/loss, and repeated retry.
5. Test lifecycle: cancel pending permission/calibration, retry, background/return,
   suspended context and tap-to-resume, input-device loss, rejected setup,
   mic indicator shutoff, denied permission, LINE fallback, and clipboard failure.
6. Commit and push when authorized. Verify the remote commit and deployment.
   Do not claim device verification from headless Chrome or mocked audio.

Phone-tuned volume floors must not change based on desktop measurements alone.
