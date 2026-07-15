# AGENTS.md — Meow Me

Context for any agent (Codex, Claude, etc.) picking up this repo cold.

## What this is

"Meow Me" — a single-file browser game. Player meows into their mic to lure a
cat closer across the screen; screaming scares it back; silence makes it
drift away. Win when the cat reaches the player zone. Shared as a link via
LINE to friends. Playful, bilingual (EN/Thai) cat-servant (ทาสแมว) humor.

Read `SPEC.md` (what + why, locked decisions) and `PLAN.md` (8-step build
order with verify gates) for full background — both are still accurate.
`CLAUDE.md` has the original build constraints (single file, CONFIG object,
no backend, etc.) — still binding.

## Status

All 8 PLAN.md steps are done and verified on a real phone (not just
localhost). Live at `https://chanooooot.github.io/meowmany/` (GitHub Pages,
public repo, deploys automatically on push to `main`).

Sound (Step 5, synthesized mrrp/scare/purr SFX) was built, tested, didn't
play reliably on the user's device (likely iOS silent-switch), and was
**removed entirely** at the user's request. No SFX code remains.

Visuals were reworked once past the placeholder-gray-shapes stage into a
committed "marigold cat vs. indigo night sky" look (moon + CSS starfield,
proper cat SVG with per-state eyes, pill buttons, rank-colored win glow).
Confirmed fitting the user's real phone screen.

## Everything is one file

`index.html`. No build step, no npm, no external assets/fonts/CDN. All
markup, CSS, inline SVG, and JS live in that one file. Keep it that way.

## Where things live in index.html

- `<style>` block: `:root` custom properties hold the palette
  (`--sky-top`, `--marigold`, `--rank-S/A/B/C`, etc.) — change the look by
  editing these, not by hunting for hardcoded colors.
- `CONFIG` object (top of `<script>`): every tunable number — pitch range,
  volume thresholds, timing, step sizes. **Change gameplay feel here, not
  inline in logic.**
- Audio pipeline: `startAudio()`, `calibrate()`, `rms()`, `detectPitch()`
  (autocorrelation), `classify()` — turns mic input into
  silence/talk/meow/scream per frame.
- Meow event detection: `updateMeowTracking()` — turns per-frame
  classifications into discrete `{duration, glide, quality}` events, gated
  by duration range + cooldown.
- Game state machine: `startGame()`, `endRound()`, `checkWinLose()`,
  `gameTick()`, `applyGoodMeow()`, `applyScream()` — states are
  `landing → calibrating → playing → won | lost`. `catPos` is 0–100 (0 =
  off-screen/lose, 100 = reached player/win).
- Rendering: `renderScene()` positions the cat/mic-meter/timer each frame.
  Cat SVG has three `<g>` groups (`eyes-idle` / `eyes-scared` / `eyes-happy`)
  toggled by CSS classes on `#catWrap` (`walking` / `scared` / `happy`).
- Scoring: `showEndScreen()` — S/A/B/C rank from avg meow quality +
  completion-time bonus, bilingual titles, localStorage best time
  (`meowme_best_time`).
- Fallbacks: `showError()` — mic-denied and no-getUserMedia (with LINE
  in-app-browser detection + copy-link button) screens. No blank-screen
  paths.

## Debug mode

`?debug=1` on the URL shows a fixed top panel: live label/volume/pitch,
computed thresholds, meow event count, game state. Keyboard shortcuts (only
bound in debug mode): `m` = simulate a good meow, `s` = simulate a scream —
lets you test the state machine without 500 real meows. **Note:** these
bypass the cooldown/duration gates in `updateMeowTracking` since they call
`applyGoodMeow`/`applyScream` directly.

## Known gotchas (learned the hard way this session)

- **Mic auto-gain-control must stay disabled** (`autoGainControl: false` in
  the `getUserMedia` constraints). With it on, talk/meow/scream all get
  normalized to the same loudness and classification breaks.
- **Volume thresholds are phone-tuned, not laptop-tuned.** Phone mics report
  much lower RMS than laptops. `scareVolFloor`/`minVolFloor` in CONFIG
  currently reflect real values measured on the user's device — don't
  "fix" them back toward laptop-scale numbers without re-testing on a
  phone.
- **Debug label uses a 500ms hold** (`heldLabel`/`heldAt` in the frame
  loop) because raw classification flickers faster than the eye can read
  at 60fps — a real scream can classify correctly for 2 frames and still
  look like nothing happened without this.
- Testing on desktop via browser automation: no real mic. Mock
  `navigator.mediaDevices.getUserMedia` to resolve with a real (silent)
  `MediaStreamDestination` stream from an `AudioContext` — an empty/fake
  `MediaStream` will fail when `createMediaStreamSource` runs.
- GitHub Pages needs the repo **public** on the free plan — it's already
  public; don't flip it private without expecting Pages to break.

## Testing

No real automated test suite (game logic is inherently mic-driven).
Verification has been: manual real-phone testing for audio/gameplay feel,
and browser-automation screenshots (with the mic mock above) for visual
regressions. If you change audio thresholds or the state machine, the
right verify step is a real phone, not just code review.
