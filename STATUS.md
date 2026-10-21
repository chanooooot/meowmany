# STATUS

**Goal:** Fair, responsive single-round mic gameplay with reliable retry and recovery.

**Now:** Review fixes deployed 2026-10-21: 120ms scare hold, median calibration, one-time LINE external-browser redirect, link-preview meta and favicon, 64-color cat sprite (page 300KB → 97KB), portable build scripts, derived sprite-gen files untracked. Copy pass deployed: one instruction phrase reused verbatim, silence no longer nags, rank joke is the win headline. 28 regression checks pass; landing, play, win and loss renders checked in headless Chrome, including short phones.

**Next:** On iPhone Safari and Android Chrome over HTTPS, open `?debug=1` and fill SPEC.md's phone tuning log (quiet, gentle meow, shout, screen tap). Then confirm voice feel and the LINE redirect (opens the system browser, no repeated reloads).

**Blocked:** Nothing in code. Device checks and threshold tuning need real phones.

_Updated: 2026-10-21 (Mac)_
