# HANDSON.md — implementation handoff

## Status

Game complete and deployed: `https://chanooooot.github.io/meowmany/`.
Single-file app: all changes stay in `index.html`. No external assets,
frameworks, backend, analytics, SFX, PWA, settings, levels, or leaderboard.
Read `AGENTS.md`, `SPEC.md`, and `CLAUDE.md` before editing.

## Review outcome

Core concept, palette, and LINE/microphone fallback copy are strong. Biggest
gaps: audio detection is hard for players to understand; resource lifecycle
and a few score paths need hardening; end screen misses screenshot/share
payoff.

## Implement in this order

1. Correctness and lifecycle
   - Capture completion time in `endRound()` before 900ms win delay; current
     score and best time include animation delay.
   - Retain `MediaStream` and animation-frame ID. Stop tracks/loop on end or
     exit; do not keep microphone and pitch detection running on end screen.
   - Pause game timer on `visibilitychange`; resume without penalizing phone
     interruptions.

2. Make audio feedback legible
   - During calibration show `Listening to the room…`.
   - In play show one compact status: `Nice meow!`, `Too quiet`, `Too loud`,
     or `Try a longer meow`.
   - Label mic meter. Keep feedback playful, not technical.

3. Accessibility and control
   - Add `aria-live` game status, focus management when screens change,
     visible `:focus-visible`, and `lang="th"` on Thai copy.
   - Add unobtrusive Restart/Exit control during play.
   - Use `100dvh` and safe-area padding for mobile edges.

4. End-screen payoff
   - Show `New best!` when applicable.
   - Add screenshot/share hint only; do not add Web Share API or share cards.
   - Give useful loss coaching based on actual state where possible.

5. Small hardening/polish
   - Catch clipboard and `localStorage` failures.
   - Move remaining gameplay thresholds/score cutoffs into `CONFIG`.
   - Add debug-only `console.assert` checks for score/state boundaries.
   - Remove repeating ground stripes; replace platform-dependent player emoji
     with matching inline art; use palette variables in cat SVG.

## Existing visual note

Cat may still need a cuteness pass: chubbier body, larger head/eyes, softer
eye shape. Preserve current marigold/indigo identity and inline SVG approach.

## Verification

- Test lifecycle, timing, feedback, and interruption behavior on real iPhone.
- Test win, lose, retry, denied mic, LINE fallback, and private/restricted
  storage/clipboard failure paths.
- Keep `?debug=1`, `m`, and `s` shortcuts working.
