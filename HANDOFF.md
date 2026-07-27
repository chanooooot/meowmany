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
- `scared` and `happy` states currently **reuse** idle/walk frames plus
  the existing whole-body shake/bounce transforms (no dedicated sprite
  frames yet — user chose to ship now rather than block on more art).

## Must verify on real phone

1. Play full win, lose, and retry flows. Confirm microphone indicator turns off
   on end/restart and permission/reacquisition feels acceptable.
2. Background the browser mid-round, return, and confirm timer remains fair.
3. Check calibration and meow-feedback copy feels playful—not distracting.
4. Recheck denied mic, LINE in-app fallback, clipboard failure, and notch/home
   indicator spacing.
5. New: confirm the sprite cat renders correctly on real phones (base64
   inline image, no CORS/network dependency, but worth confirming
   `image-rendering`/animation timing feels right at actual screen size).

## Deferred visual work

- If the user wants proper `scared`/`happy` sprite frames (not reused
  idle/walk), get a matching 4-frame strip per state from the same
  source (ChatGPT image gen), same crop/clean/base64 pipeline used for
  idle/walk, then wire in analogous to the existing `catIdleFrames`/
  `catWalkFrames` keyframes in `index.html`.
- Three earlier throwaway redesign prototypes (pixel/doodle/clay,
  marigold-on-navy palette) were explored and **not used** — the sky/
  marigold direction implemented this session is the picked one.

## Orientation

Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before changes. The deployed
branch is `main`; GitHub Pages updates after pushes to it.
