# AGENTS.md — Meow Many

## Product and constraints

A single-round browser game: gentle, voiced meows lure a cat onto its bed;
loud calls scare it back; four seconds without an accepted call starts drift.
The timer is 60 seconds. Share the HTTPS link with friends, primarily via LINE.
English UI with Thai rank/loss jokes. Detection is a forgiving pitch/volume
heuristic, not semantic recognition of the word “meow”. Humming may qualify.

Everything shipped is in `index.html`: CSS, embedded pixel sprites, markup,
and vanilla JavaScript. No build, runtime dependencies, external assets,
backend, uploads, analytics, sound effects, settings, levels, leaderboard,
PWA, or share API. Audio is processed locally. LocalStorage stores best time.
Source sprite tooling lives in `tools/pixel-art/world/build.py` and
`pixel-art/design-preview/build.py`. The latter directory also preserves the
approved visual prototype and native bush/flower/heart artwork.

`SPEC.md` describes current behavior. `PLAN.md` describes current verification
requirements. `CLAUDE.md` has binding implementation constraints. `HANDOFF.md`
records earlier design history; its historical verification claims are not
proof that current code has passed device tests. `STATUS.md` tracks remaining
verification. `REVIEW.md` preserves the review and its resolution notes.

Origin: `https://github.com/chanooooot/meowmany`. GitHub Pages deploys pushes
to `main`, at `https://chanooooot.github.io/meowmany/`. A user instruction to
commit/push authorizes that deployment; do not ask again.

## Implementation map

- CSS `:root` owns colors and embedded image data. Cat rows: idle, walking,
  scared; happy rests using idle/blink frames. Walking and travel share a
  400ms duration; scare uses a stable frame from its dedicated row. The
  approved pastel garden has rounded bushes, flowers, and pixel hearts.
  World art stays visible across screens. Results use a cream card with dark
  text, a rank badge, and crisp borders/shadows.
- `CONFIG` owns tunable gameplay values. **Keep the phone-tuned volume floors
  and disabled auto gain control.** Desktop measurements cannot retune phones.
- Audio: `startAudio`, `calibrate`, `rms`, `detectPitch`, `classify`.
  Setup remains visible/cancellable. A session counter rejects stale async
  work and stops mic streams granted after cancellation. Errors distinguish
  denial, missing/busy devices, and setup failures.
- Input: `updateMeowTracking` tolerates brief gaps, waits for an ending pause,
  and enforces duration/cooldown. `updateScream` latches a loud event until
  sustained quieter input rearms it. Screams discard an unfinished meow.
- Round: `startGame`, `gameTick`, `applyGoodMeow`, `applyScream`, `endRound`.
  Resolve deadlines before audio rewards. Reset all event gates each round.
- Lifecycle: `stopAudio` cancels frames/calibration/reveal/animation timers
  and stops input tracks. Track loss shows recovery. Hidden/suspended rounds
  pause; context recovery may require the visible tap-to-resume button.
- Rendering: `positionCat` maps progress from fully offscreen to the bed while
  accounting for sprite width; resize updates bounds. `renderScene` updates
  the calibrated quiet/gentle/loud meter and a non-announcing, inspectable timer.
  Reaction bubbles follow the cat, clamp inside the viewport during travel,
  and keep the existing live status announcements. Short screens simplify
  decorative headings and result tips to preserve controls.
- Results: `showEndScreen` mixes average duration/glide quality with time.
  Rank criteria and drift/scare loss reasons are explained to the player.
  Rank title language follows the selected Thai/English text.

## Debug and tests

`?debug=1` shows pitch, volume, thresholds, events, and state. The label holds
for 500ms. Debug `m`/`s` apply movement directly: they bypass detection,
segmentation, cooldown, and scream rearming. Do not use them to verify mic feel.

Run `node tools/test-game.cjs`. It executes the shipped script with controlled
clocks, audio, and DOM mocks; covers segmentation, penalties, deadlines,
scoring, lifecycle cancellation, interruptions, errors, and coordinates.
No npm install or test framework is required.

For Chrome layout testing, use explicitly sized iframes; a headless window
flag alone may not reproduce a phone viewport. For real Web Audio integration
without a mic, return a real `MediaStreamDestination` stream from the mock;
an empty MediaStream is invalid for `createMediaStreamSource`.

Before calling device behavior verified, test actual iPhone Safari and
Android Chrome over HTTPS: voice/glide acceptance, scream rearming, calibration,
win/loss/retry, background/return, tap-to-resume, mic loss, LINE fallback,
clipboard failure, notch/home-indicator spacing, and sprite rendering.
