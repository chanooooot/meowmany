# CLAUDE.md — Instructions for the executing model

You are building "Meow Me": a single-file browser game where the player meows into the mic to attract a cat. Read `SPEC.md` (what + why) and `PLAN.md` (build order) before writing any code. All design decisions are already made — do not relitigate them.

---

## Hard constraints

1. **ONE file.** Everything (HTML, CSS, JS, SVG) in `index.html`. No build step, no frameworks, no external assets, no CDN scripts, zero network requests after page load.
2. **All tunables in the single `CONFIG` object** at the top of the file. No magic numbers scattered in logic.
3. **No backend, no analytics, no accounts.** localStorage for best time only.
4. **Target:** iOS Safari + Android Chrome + desktop Chrome. AudioContext must be created/resumed inside the Start-button gesture handler (iOS requirement).
5. **No blank-screen failure modes.** Every error path (mic denied, no getUserMedia, in-app browser) renders a friendly screen.

## Core design principle: forgiving detection

False positives (a mediocre meow accepted) are fine. False negatives (a real meow rejected) ruin the game. When tuning, always err toward accepting. The mic meter must feel instantly responsive — perceived responsiveness matters more than classification accuracy.

## Behavioral guidelines (Karpathy)

1. **Think before coding.** If anything in SPEC is ambiguous, state your assumption in a code comment and proceed with the simplest reading — do not invent features to cover ambiguity.
2. **Simplicity first.** Minimum code that passes each PLAN verify-gate. No abstractions for single-use code. No speculative flexibility. If a section balloons past ~50 lines, ask whether it could be 20.
3. **Surgical changes.** When iterating, touch only what the current step requires. Don't restyle or refactor working code from earlier steps.
4. **Goal-driven.** Follow PLAN.md step order exactly. Each step's verify-gate must pass before the next step. Step 1 (audio pipeline + debug panel) is the highest-risk step — get detection feeling right before building anything else.

## What NOT to add (explicitly out of scope)

- ❌ Levels, multiple cats, difficulty settings
- ❌ Leaderboards, sharing APIs, share-card images
- ❌ Sound files, image files, fonts requiring network fetch
- ❌ PWA manifest / service worker
- ❌ TypeScript, bundlers, npm anything
- ❌ Settings menus (CONFIG is developer-facing only)

If you think something outside scope is genuinely needed, note it in a comment as "v2 candidate" and move on.

## Copy tone

English UI, playful. Funny titles bilingual English/Thai with ทาสแมว (cat-servant) humor — see SPEC §3 rank table. You may improve the jokes; keep them short and screenshot-worthy.

## Debug affordances (keep in shipped file)

- `?debug=1` URL param → shows volume/pitch/classification panel
- Keyboard shortcuts in debug mode: `m` = simulate good meow, `s` = simulate scream (lets logic be tested without meowing 500 times)

## Definition of done

All 8 checks in SPEC §8 pass on a real phone over the deployed GitHub Pages URL. Not "it works on localhost."
