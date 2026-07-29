# HANDOFF.md — next-session handoff

## Current state

- Live: `https://chanooooot.github.io/meowmany/`
- Latest implementation commit before this handoff: pixel-art world redesign
  (see "Completed this session" below).
- One-file app: all *shipped* game logic stays in `index.html`. The repo now
  also carries `tools/pixel-art/world/build.py` (+ 4 small PNGs it produces),
  which is source art tooling, not something GitHub Pages serves.
- No external assets, framework, backend, analytics, SFX, PWA, settings,
  levels, leaderboard, or share API.

## Completed this session

- Renamed the game from "Meow Me" to "Meow Many" in `index.html` (tab
  title, `<h1>`, scene `aria-label`, mic-denied error copy). `SPEC.md`,
  `PLAN.md`, `AGENTS.md`, `CLAUDE.md` still say "Meow Me" — not touched,
  wasn't asked to; update those too if the rename should be permanent
  project-wide, not just in the shipped page.

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
- Ran an over-engineering/"AI slop" pass with `ui-ux-pro-max` (design
  review, no new deps): removed emoji-as-icon on the h1/Start/Copy-link
  buttons and a decorative unicode heart-marquee row that read as filler
  (`06dd8f1`); fixed the win-rank glow firing on the loss screen too
  (gated `text-shadow` behind a `--rank-glow` var only set on a win) and
  de-uniformed secondary-button radius from `999px` pill to `12px` so
  full-pill stays reserved for primary CTAs (`2f29344`). Claymorphism/
  gradient chrome direction itself was kept — user chose the minimal
  cleanup scope, not a full pixel-art skin.

- Full pixel-art world redesign (grilling skill used to pin down scope,
  headless Chrome used to actually see renders before/after — see below).
  Diagnosis: the CSS gradient sky/ground was a formless orange smear (62%-
  extent radial gradient), the "moon" was two white pill divs that read as
  loading skeletons, `--sky-top`/`--sky-mid`/`--fur-stroke` were dead vars
  from an abandoned purple-night version, the landing screen had no cat at
  all (violates `SPEC.md` §5.1), and `#gameStatus`/`#restartBtn` overlapped
  at 390px width. Root cause: a hand-pixeled cat standing inside CSS-gradient
  chrome nobody had actually looked at rendered.
  - Built `tools/pixel-art/world/build.py` with `pixel-art-studio`: sun +
    2 clouds + cat bed packed into one `--world-sprite` sheet (same
    background-position technique as the cat rows), plus 3 seamless
    repeat-x tiles (`--treeline-tile`, `--grass-tile`, `--path-tile`) using
    a periodic column-height function so they tile with no visible seam.
  - Day palette (blue sky / green grass) — orange cat is complementary
    against it and pops, vs. the old orange-on-orange sunset smear.
  - Landing and gameplay now share one persistent `#world` background
    layer (sky/sun/clouds/treeline/path/grass/cat/bed all always visible);
    Start only swaps the title block for the HUD. Fixes the catless-landing
    gap and the old 55%/58% horizon mismatch in one move.
  - Old inline SVG cushion replaced by the pixel bed (from `--world-sprite`).
  - HUD rebuilt as a flex column (`#hud` > meter bar, then a
    space-between row for label/timer/restart, then status on its own
    line) instead of independently-calculated `top:` offsets — this was
    the actual root cause of the overlap bug, not just a width tweak.
  - Buttons flattened: solid fill + 2px border + hard offset shadow
    (`0 4px 0`) instead of gradient fill + blurred drop-shadow, radius
    999px pill down to 10px, to match the pixel-art world instead of
    reading as generic soft-UI chrome.
  - Typography hierarchy: body copy 600→500 weight, HUD/status text
    700→600, so headings/buttons (800) are the only "shout" tier.
  - Verification method: headless Chrome screenshots
    (`chrome --headless --screenshot`) inside a 390px-wide **iframe**
    harness — loading `index.html` directly via `--window-size=390,844`
    was unreliable (observed `innerWidth=500` despite the flag in one
    run), so the iframe (explicit CSS width) is the trustworthy way to
    verify layout without a real device. Caught and fixed a real bug this
    way (HUD overlap) and a self-inflicted one (hand-typed a large base64
    blob into an Edit call and silently corrupted the PNG — fixed by
    always reading/writing asset bytes through a script, never retyping
    them).

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
6. Trigger a scream (or `?debug=1` + `s` key) and confirm the scared-frame
   sprite pose shows during the shake, not a stale idle frame.
7. New: confirm the new world art (sky/sun/clouds/treeline/path/grass/bed)
   renders correctly at real phone widths and `image-rendering:pixelated`
   doesn't blur on a real display. Headless-Chrome verification this
   session was a synthetic 390px iframe, not a device.

## Deferred visual work

- If the user wants a proper `happy` sprite row (not the reused walk
  frames + bounce transform), author a matching 4-frame strip with the
  `pixel-art-studio` skill (same approach used for the `scared` row: study
  the existing sheet's palette/proportions, build parametrically, append
  as row 4), then wire in analogous to `catScaredFrames` in `index.html`.
- Three earlier throwaway redesign prototypes (pixel/doodle/clay,
  marigold-on-navy palette) were explored and **not used** — the sky/
  marigold direction implemented this session is the picked one.
- Treeline tile reads a bit spiky/mountain-like rather than soft bushes
  (parabolic column-height function in `build.py`'s `build_periodic_tile`).
  Cosmetic only; swap to a sqrt-based curve for rounder tops if it bugs you.

## Orientation

Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before changes. The deployed
branch is `main`; GitHub Pages updates after pushes to it.
