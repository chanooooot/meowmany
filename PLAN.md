# PLAN.md — Build Plan for "Meow Me" 🐱

Build in this order. Each step has a verify gate — do not proceed until it passes.
Riskiest part first: the audio pipeline. If detection doesn't feel good, nothing else matters.

---

## Step 0 — Skeleton
- One `index.html` with `CONFIG` object at top, empty sections for: audio, game state, render, UI screens.
- **Verify:** opens in browser, no console errors.

## Step 1 — Audio pipeline (riskiest — do first)
- Start button → `getUserMedia` → `AudioContext` + `AnalyserNode`.
- 1s ambient calibration → set `minVol` / `scareVol` relative to noise floor.
- Per-frame: RMS volume + pitch via autocorrelation.
- Render a **debug panel**: live volume bar, detected pitch (Hz), classification label (silence / talk / meow / scream). Keep behind a `?debug=1` URL flag after this step.
- **Verify (manual, on laptop + phone):**
  - Meow → label shows "meow" reliably
  - Normal speech → mostly "talk"
  - Shout → "scream"
  - Silence → "silence"
  - Tune CONFIG until the above feels right. **This gate is the whole game — spend time here.**

## Step 2 — Meow event detection
- Turn frame classifications into discrete events: meow start/end, duration check (0.3–1.5s), pitch-glide detection (compare pitch contour start vs end), cooldown (0.7s).
- **Verify:** console logs one clean event per meow, with `{duration, glide: bool, quality: 0–1}`. Rapid-fire meows within cooldown produce one event.

## Step 3 — Game state machine
- States: `landing → calibrating → playing → won | lost`.
- Cat position (0–100), patience timer, event handlers: goodMeow(+), scream(−), silenceDrift(−), win/lose checks.
- **Verify:** with debug panel + keyboard shortcuts simulating events (m = meow, s = scream), cat position number moves correctly and win/lose trigger. Test logic without needing to meow 500 times.

## Step 4 — Visuals
- Inline SVG cat: idle / walking / scared / happy states (CSS animations: tail sway, ear twitch, walk bob).
- Side-view scene, cat position bound to game state, player zone on right.
- Live mic meter in the play UI (small, always visible).
- **Verify:** cat visibly walks when meowed at, jumps back on shout, hearts on win. Looks OK at 375px wide (iPhone) and desktop.

## Step 5 — SFX
- WebAudio-synthesized: soft purr (win), startled sound (scare), tiny "mrrp" acknowledgment on good meow. No audio files.
- **Verify:** sounds play on iOS Safari (must be within user-gesture-unlocked AudioContext).

## Step 6 — Scoring & end screens
- Time tracking, meow quality accumulation → S/A/B/C rank + bilingual title (SPEC §3).
- localStorage best time.
- Win/lose screens + retry (full state reset without page reload).
- **Verify:** play twice; best time persists; retry works cleanly; ranks differ between a sloppy run and a good run.

## Step 7 — Fallbacks & polish
- Mic-denied screen, no-getUserMedia screen with "open in Chrome/Safari" hint (detect LINE UA if easy, else generic).
- Landing screen copy, timer display, responsive pass.
- **Verify:** deny mic → friendly screen. Simulate missing getUserMedia (`navigator.mediaDevices = undefined` in console) → fallback screen.

## Step 8 — Ship
- Deploy to GitHub Pages.
- **Verify:** full SPEC §8 success-criteria checklist on real iPhone Safari + Android Chrome + desktop, over the public URL. Send link to one friend via LINE; confirm the in-app fallback path behaves.

---

## Test checklist (final gate = SPEC §8)

| # | Check | Pass? |
|---|-------|-------|
| 1 | Loads on GH Pages, mobile + desktop | ☐ |
| 2 | Mic meter responds to voice | ☐ |
| 3 | Meow advances cat; talk mostly doesn't; shout retreats | ☐ |
| 4 | 4s silence → drift | ☐ |
| 5 | Win + lose screens, retry, best time | ☐ |
| 6 | Mic-denied + LINE in-app fallbacks | ☐ |
| 7 | Single CONFIG object | ☐ |
| 8 | One file, zero post-load network requests | ☐ |
