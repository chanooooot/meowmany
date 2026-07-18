# HANDSON.md — next-session handoff

## Current state

- Live: `https://chanooooot.github.io/meowmany/`
- Latest implementation commit before this handoff: `c1c456b`
  (`fix(a11y): 44px touch target on copy-link button, hide decorative hearts
  from screen readers`)
- One-file app: all game work stays in `index.html`.
- No external assets, framework, backend, analytics, SFX, PWA, settings,
  levels, leaderboard, or share API.

## Completed this session

- A11y pass on `index.html`: `#copyLinkBtn` now meets 44px min touch target;
  spawned heart divs marked `aria-hidden`.
- Explored a full visual redesign (theme/animation/icons) as throwaway
  prototypes — **not applied to `index.html`, exploration only.** Three
  direction mockups built as standalone Artifacts (canvas-rendered, not
  committed to repo):
  1. **Pixel** — 30x20 grid, `image-rendering:pixelated`, blocky retro-console
     chrome.
  2. **Doodle** — chalkboard bg, hand-drawn linework redrawn with per-frame
     jitter ("boil" effect), chalk-hatch UI chrome.
  3. **Clay** — claymorphism, radial-gradient shaded blobs (no outline
     strokes), squish-bounce animation, soft-UI double-shadow chrome.
  All three keep the marigold-on-navy palette; only rendering technique
  differs. User has not picked a direction yet.

## Must verify on real phone

1. Play full win, lose, and retry flows. Confirm microphone indicator turns off
   on end/restart and permission/reacquisition feels acceptable.
2. Background the browser mid-round, return, and confirm timer remains fair.
3. Check calibration and meow-feedback copy feels playful—not distracting.
4. Recheck denied mic, LINE in-app fallback, clipboard failure, and notch/home
   indicator spacing.

## Deferred visual work

Redesign direction undecided — see the three mockups above. Next session:
get a pick from the user, then port the chosen technique (pixel/doodle/clay)
into `index.html`'s inline `<svg>`/CSS, replacing the current cat/player art
and animation classes. Do not add new game systems until real-phone behavior
above is confirmed and a redesign direction is locked in.

## Orientation

Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before changes. The deployed
branch is `main`; GitHub Pages updates after pushes to it.
