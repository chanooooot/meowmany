# SPEC.md — "Meow Me" 🐱 (working title)

**Version:** 1.0 · **Date:** 2026-07-15 · **Owner:** Ham
**Status:** Approved for build · Handover to downstream model

---

## 1. Concept

A browser mini-game. The player meows into their microphone to coax a cat across the screen. Good meows bring the cat closer; screaming scares it; silence makes it wander off. Win when the cat reaches you. Built to be shared as a link with friends (primarily via LINE).

**Vibe:** playful, meme-y, ทาสแมว (cat-servant) energy. English UI, Thai flavor in the funny copy.

---

## 2. Locked Decisions (with rationale)

| # | Decision | Choice | Rationale |
|---|----------|--------|-----------|
| D1 | Platform | Single-file HTML (vanilla JS + Web Audio API), deployed to GitHub Pages | Zero cost, zero build step, shareable HTTPS URL (mic requires HTTPS). Mobile-first layout. |
| D2 | Meow detection | Pitch + volume heuristic via Web Audio API (AnalyserNode + autocorrelation pitch detection) | Offline, no model download, tunable, debuggable. Rewards meow-*like* sounds; does not pretend to be real classification. Rejected: Web Speech API (unreliable for non-words, privacy), YAMNet (4MB, trained on real cats). |
| D3 | Game loop | Approach + retreat, single round | Retreat mechanics create tension and a fail state. Levels/personalities → v2 backlog. |
| D4 | Input rules | See §3 ruleset. All thresholds in one `CONFIG` object. | Forgiving by design: false positives OK, false negatives kill fun. |
| D5 | Visuals | Inline SVG cat, 4 states (idle / walking / scared / happy), side-view scene, live mic meter, WebAudio-synthesized SFX | Zero external assets, single-file preserved, charming enough to screenshot. Fallback if SVG struggles: emoji + CSS. |
| D6 | Scoring | Completion time + meow rank (S/A/B/C) + funny title on end screen. localStorage best time. No backend. | Screenshot = the viral hook. Leaderboard → v2. |
| D7 | Language | English UI, Thai flavor in titles/jokes (e.g. "S-Rank: ทาสแมวตัวจริง 🏆") | Thai friends are primary audience; English keeps it shareable wider. |
| D8 | Edge cases | Permission-denied screen, unsupported-browser message, 1s ambient auto-calibration, LINE in-app browser fallback hint | Sharing channel is LINE; in-app browsers have inconsistent getUserMedia support. |

---

## 3. Game Rules

### Cat behavior (per audio frame / event)

| Input | Detection | Cat response |
|-------|-----------|--------------|
| **Good meow** | Voiced sound, fundamental ~150–600 Hz, duration 0.3–1.5s, volume between `minVol` and `scareVol` | Steps closer. Pitch glide detected (rising or falling contour) → bigger step + better rank credit |
| **Scream / too loud** | Volume ≥ `scareVol` | Jumps back + scared animation + 💢 |
| **Silence** | No qualifying sound for > `driftAfterSec` (default 4s) | Slowly drifts away from player |
| **Talking / noise** | Sound outside meow criteria | Cat pauses, "suspicious" look. No hard penalty |
| **Spam meows** | Meows within `cooldownSec` (default 0.7s) of last counted meow | Ignored (diminishing returns) |

### Win / lose

- **Win:** cat reaches player zone → purr SFX + hearts + end screen (time, rank, title, best time, retry, share hint)
- **Lose:** patience timer (`roundSec`, default 60s) expires OR cat retreats fully off-screen → "The cat ignored you 😾 / แมวไม่สนใจคุณ" + retry

### Meow rank (end screen)

Computed from: avg meow quality (glide shape + duration fit) and completion time.
- **S** — ทาสแมวตัวจริง 🏆
- **A** — Certified Cat Whisperer
- **B** — The cat tolerates you
- **C** — แมวมาเพราะสงสาร 😹

(Exact copy: downstream model may improve jokes; keep the bilingual tone.)

---

## 4. CONFIG (single object, top of file — all tunable)

```js
const CONFIG = {
  pitchMinHz: 150, pitchMaxHz: 600,
  meowMinSec: 0.3, meowMaxSec: 1.5,
  minVol: /* set relative to calibration */,
  scareVol: /* set relative to calibration */,
  cooldownSec: 0.7,
  driftAfterSec: 4,
  roundSec: 60,
  stepGood: /* px or % */, stepGlideBonus: /* extra */,
  stepScare: /* retreat */, driftSpeed: /* px/s */,
  calibrationSec: 1
};
```

Volume thresholds are **relative to a 1s ambient-noise calibration** sampled at game start.

---

## 5. UX Flow

1. **Landing:** title, cat SVG idle, "Start meowing 🐱" button (required — iOS Safari needs user gesture to start AudioContext — fact)
2. **Calibration:** 1s "listening to the room…" then round starts
3. **Play:** side-view scene, cat left / player zone right, distance visible, live mic meter, countdown timer
4. **End:** win or lose screen per §3, retry button
5. **Fallbacks:**
   - Mic denied → friendly explainer + retry
   - No getUserMedia (incl. LINE/IG in-app browsers) → "Open in Chrome/Safari" hint with copy-link affordance
   - No blank screens, ever

---

## 6. Non-goals (v1)

- ❌ No backend, no accounts, no leaderboard
- ❌ No levels / multiple cats
- ❌ No external assets (images, audio files, fonts beyond system/one Google font max)
- ❌ No frameworks, no build step
- ❌ No analytics

## 7. v2 Backlog (parked, do not build)

- Multiple cat personalities (shy cat = soft meows, grandma cat = loud)
- Shared leaderboard (needs backend — revisit only if the game gets real traction)
- Share-card image generation (canvas → PNG of your rank)
- PWA install

---

## 8. Success Criteria (verifiable)

1. Loads on GitHub Pages URL on iPhone Safari + desktop Chrome
2. Start → mic prompt → mic meter visibly responds to voice
3. Human "meow~" moves cat closer; normal talking mostly doesn't; a shout scares it back
4. 4s+ silence → cat drifts away
5. Win and lose screens both render with retry; win shows time + rank + title + best time
6. Denied mic and LINE in-app browser both show helpful fallback, no blank screen
7. All thresholds live in the single `CONFIG` object
8. Entire game is ONE .html file, no network requests after page load
