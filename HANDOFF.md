# HANDOFF.md — next-session handoff

## Current state

- Live: `https://chanooooot.github.io/meowmany/`
- Latest implementation commit before this handoff: `4526c29`
  (`feat(cat): swap SVG cat art for pixel sprite sheet (idle/walk)`)
- One-file app: all game work stays in `index.html`.
- No external assets, framework, backend, analytics, SFX, PWA, settings,
  levels, leaderboard, or share API.

## Completed this session

- Redesign locked in and applied to `index.html`: sky-blue/green/marigold
  palette, sun+cloud decoration, cushion marker replacing the old human
  player figure, bilingual copy refresh. Also fixed corrupted UTF-8
  (mojibake) in emoji/Thai strings left over from a prior edit.
- Cat art switched from hand-drawn inline SVG to a pixel sprite sheet:
  user generated a 4-frame idle + 4-frame walk strip via ChatGPT image
  gen, cropped/cleaned (removed labels, made background transparent,
  normalized frame size) into one 520x240 sheet, embedded as a base64
  `data:` URI in a CSS custom property — stays one file, zero network
  requests. CSS `steps(4)` animation cycles frames per state.
- `scared` now has a dedicated 4-frame sprite row (crouched, wide shocked
  eyes, pinned-back ears, puffed tail, splayed whiskers) authored with the
  `pixel-art-studio` skill to match the existing sprite's palette/style,
  appended as row 3 of the same sheet (now 520x360). Wired via a new
  `catScaredFrames` keyframe on `#catWrap.scared #cat`, playing once
  alongside the existing `scaredShake` wrapper shake. `happy` still
  **reuses** the walk-frame row plus the bounce transform — no dedicated
  happy sprite yet.

## Must verify on real phone

1. Play full win, lose, and retry flows. Confirm microphone indicator turns off
   on end/restart and permission/reacquisition feels acceptable.
2. Background the browser mid-round, return, and confirm timer remains fair.
3. Check calibration and meow-feedback copy feels playful—not distracting.
4. Recheck denied mic, LINE in-app fallback, clipboard failure, and notch/home
   indicator spacing.
5. Confirm the sprite cat renders correctly on real phones (base64
   inline image, no CORS/network dependency, but worth confirming
   `image-rendering`/animation timing feels right at actual screen size).
6. New: trigger a scream (or `?debug=1` + `s` key) and confirm the new
   scared-frame sprite pose shows during the shake, not a stale idle frame.

## Deferred visual work

- If the user wants a proper `happy` sprite row (not the reused walk
  frames + bounce transform), author a matching 4-frame strip with the
  `pixel-art-studio` skill (same approach used for the `scared` row: study
  the existing sheet's palette/proportions, build parametrically, append
  as row 4), then wire in analogous to `catScaredFrames` in `index.html`.
- Three earlier throwaway redesign prototypes (pixel/doodle/clay,
  marigold-on-navy palette) were explored and **not used** — the sky/
  marigold direction implemented this session is the picked one.

## Orientation

Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before changes. The deployed
branch is `main`; GitHub Pages updates after pushes to it.
