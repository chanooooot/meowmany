# HANDSON.md — next-session handoff

## Current state

- Live: `https://chanooooot.github.io/meowmany/`
- Latest implementation commit before this handoff: `a323e51`
  (`fix(game): harden audio round flow`)
- One-file app: all game work stays in `index.html`.
- No external assets, framework, backend, analytics, SFX, PWA, settings,
  levels, leaderboard, or share API.

## Completed this session

- Fixed scoring time: win animation delay no longer inflates time or rank.
- Mic tracks and frame loop stop after round/end/restart; Retry reacquires mic.
- Round pauses on tab/app interruption via `visibilitychange`.
- Added calibration and in-round feedback, mic label, Start over control,
  focus styling, live status, safe-area-aware scene controls, and inline
  player art.
- Added New best and screenshot challenge copy on wins; useful loss coaching.
- Hardened clipboard/localStorage failure paths.
- Moved remaining game thresholds/rank values into `CONFIG`.
- Added debug rank assertions; `?debug=1`, `m`, and `s` remain available.
- Detector returns clean (`[]`); inline JavaScript syntax check passes.

## Must verify on real phone

1. Play full win, lose, and retry flows. Confirm microphone indicator turns off
   on end/restart and permission/reacquisition feels acceptable.
2. Background the browser mid-round, return, and confirm timer remains fair.
3. Check calibration and meow-feedback copy feels playful—not distracting.
4. Recheck denied mic, LINE in-app fallback, clipboard failure, and notch/home
   indicator spacing.

## Deferred visual work

Cat can still be cuter: chubbier body, larger head/eyes, softer eye shape.
Keep marigold/indigo palette and inline SVG approach. Do not add new game
systems until real-phone behavior above is confirmed.

## Orientation

Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before changes. The deployed
branch is `main`; GitHub Pages updates after pushes to it.
