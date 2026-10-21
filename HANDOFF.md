# HANDOFF.md — Meow Many

Session log, newest first. Current behavior lives in SPEC.md, constraints in
CLAUDE.md and AGENTS.md, open work in STATUS.md. Device behavior is unverified
unless an entry says a real phone was used.

## Log

## 2026-10-21 Review fixes (this entry's commit)
Did: 120ms scare hold; median calibration; LINE redirect via `?openExternalBrowser=1`; description/og meta and favicon; 64-color idle/walk rows (page 300KB → 97KB); portable build scripts; derived sprite-gen files untracked; dead CSS removed; REVIEW.md retired to git history; SPEC.md phone tuning log added.
Root cause (if fix): one loud frame (tap, bump, plosive) counted as a scream; calibration mean jumped on any stray sound.
Verified: `node tools/test-game.cjs` 27/27, new checks fail on the old behavior; headless Chrome landing/win at 390x844 and 780x400; build scripts rerun from another folder give identical PNGs.
NOT verified: any real phone; LINE honoring the flag; 120ms hold feel; current scare values (set by feel on 2026-10-04).
Next: fill SPEC.md's phone tuning log on iPhone Safari and Android Chrome, then confirm voice feel and the LINE redirect.

## 2026-10-04 Easier input, new sprite rows, scare retune (bfbe9b3..58c41fe)
Did: pitch 100–900Hz, calls 0.15–2.5s, quality peak 0.9s; sprite-gen scared and curled happy rows, original walk restored; scareVolMultiplier 2.0 → 6.0 → 3.5, scareVolFloor 0.004 → 0.006 → 0.005.
Verified: 24 regression checks.
NOT verified: no recorded phone readings behind the scare values; sprite rendering on phones.

## 2026-10-04 Review fixes and approved garden design (09a528f, fd64618)
Did: resolved the 16-finding gameplay/lifecycle review (`git show 58c41fe:REVIEW.md`); pastel garden, reaction bubbles, calibrated meter bands, rank badge.
Verified: regression harness; Chrome 390px iframe renders; synthetic Web Audio win and mic shutoff.
NOT verified: real phones.

## Earlier
Did: SVG cat replaced by the pixel sprite sheet; pixel-art world (`tools/pixel-art/world/build.py`); renamed Meow Me → Meow Many; SFX removed because they played unreliably on devices.
Lessons: check layout in explicitly sized iframes (headless `--window-size` was unreliable); regenerate embedded art with scripts, never by retyping base64.
