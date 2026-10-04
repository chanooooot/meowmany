# SPEC.md — Meow Many

Current product specification. Historical decisions are summarized in HANDOFF.md.

## Goal

A small, playful browser game: meow into the mic to bring a cat onto its bed.
Gentle calls help; loud calls scare it; neglected calls let it wander away.
The result gives a funny bilingual rank and best completion time.

## Constraints

One HTML file with vanilla JS, Web Audio, CSS, and embedded pixel sprites.
No build, CDN, external assets, backend, uploads, analytics, SFX, accounts,
levels, leaderboard, settings, PWA, or share API. Source art and test tools
may be separate files; the shipped page makes no application asset requests.
Deploy through GitHub Pages. Audio remains local; best time is in localStorage.

## Rules

- Start creates/resumes AudioContext in a user gesture and requests the mic.
  Setup stays visible with a cancel action. Stay quiet during one-second
  ambient calibration. Volume floors are tuned for phones; auto gain control,
  echo cancellation, and noise suppression remain disabled.
- An accepted call is voiced, approximately 150–600Hz, between calibrated
  minimum/scare volume, and 0.3–1.5 seconds long. A 100ms ending gap finalizes
  the call; shorter interruptions are tolerated. Cooldown is 0.7 seconds
  between accepted events. A modest correlation gate filters unvoiced noise;
  this is not semantic “meow” recognition. Humming can qualify.
- Start position is 50 on a 0–100 scale. Accepted calls add 8; a pitch change
  of at least 20Hz adds 4 more. Duration quality peaks at 0.9 seconds.
- Each distinct loud event subtracts 15. A loud event discards any unfinished
  call. It rearms after 300ms below 80% of the scare threshold, so threshold
  flicker cannot multiply penalties.
- Four seconds without an accepted call starts retreat at 3 units/second.
  Talking and incomplete calls do not reset drift. Feedback explains this.
- Reach 100 to win; reach 0 or 60 seconds to lose. Resolve the deadline before
  rewards in that frame. Cat coordinates account for sprite and bed bounds:
  position 0 is offscreen; position 100 is on the bed, inside the viewport.
- Hidden or suspended play pauses clocks and discards unfinished input.
  Resume preserves remaining time and drift grace. Suspended audio may need
  the visible tap-to-resume action. Mic loss gives a recoverable error.
- Every retry resets input gates and animation state. Cancelled async startup
  cannot overwrite a later round or leak a late-granted microphone stream.

All tuning values live in CONFIG. Keep existing phone volume floors unless
new real-phone measurements justify a change.

## Score and feedback

Rank score = 60% average meow quality + 40% completion-time bonus.
Quality = duration fit (80%) + glide bonus (20%). Thresholds: S 0.8,
A 0.6, B 0.35, otherwise C. Titles remain playful, with Thai S/C jokes and
English A/B titles. Best time stores successful completion times only.

Teach “gentle meow for about a second, then pause”. Show candidate, rejection,
accepted step (+8/+12), and wandering feedback in a bubble above the cat,
without unreadable frame flicker. Meter bands follow calibrated thresholds. Explain
rank improvement on results. Loss guidance distinguishes timeout, scares,
and wandering. Keep rank color in a readable letter badge with dark text.

## Screens and accessibility

The approved visual direction is a pastel pixel garden: raised cat/bed/path,
rounded bush clusters, small flowers, crisp buttons/cards, and pixel hearts.
Walking and travel share a 400ms step; success rests using idle/blink frames.
The source/approved prototype lives in pixel-art/design-preview; runtime art
is embedded in index.html.

Landing has the cat/world, short instructions, and Start. Starting/calibration
show status and Start over. Play shows mic meter, inspectable countdown,
status, and Start over; interrupted audio shows Tap to resume mic. Results
use a readable card with rank badge/time/best/tip/retry and a screenshot hint.
Short landscape hides decorative headings and the rank tip to keep controls visible.

Errors explain unsupported/in-app browsers, permission denial, missing/busy
mics, and setup/interruption failures. Copy-link fallback handles clipboard
failure. Buttons have visible keyboard focus and useful touch targets.
Respect reduced motion; avoid per-second timer announcements. Apply language
metadata to the actual language of result text.

## Verification

Run `node tools/test-game.cjs` and review mobile/landscape Chrome renders.
Then test actual iPhone Safari and Android Chrome over the deployed HTTPS
URL. Synthetic signals and DOM/audio mocks establish logic, not voice feel,
Safari recovery policy, mic device calibration, or LINE compatibility.
