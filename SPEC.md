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
  ambient calibration; the room level is that second's median, so a stray word
  or tap cannot raise thresholds. Volume floors are tuned for phones; auto gain
  control, echo cancellation, and noise suppression remain disabled.
- An accepted call is voiced, approximately 100–900Hz, between calibrated
  minimum/scare volume, and 0.15–2.5 seconds long. A 100ms ending gap finalizes
  the call; shorter interruptions are tolerated. Cooldown is 0.7 seconds
  between accepted events. A modest correlation gate filters unvoiced noise;
  this is not semantic “meow” recognition. Humming can qualify.
- Start position is 50 on a 0–100 scale. Accepted calls add 8; a pitch change
  of at least 20Hz adds 4 more. Duration quality peaks at 0.9 seconds.
- A loud event must stay above the scare threshold for 120ms (dips shorter
  than 100ms are tolerated). Shorter spikes, such as screen taps, bumps, or
  plosives, are ignored and do not end a call. Each distinct loud event
  subtracts 15 and discards any unfinished call. It rearms after 300ms below
  80% of the scare threshold, so threshold flicker cannot multiply penalties.
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
English A/B titles. The rank title is the win headline; a loss shows one
English title, not a stacked translation. Best time stores successful
completion times only.

Teach one phrase, reused word for word: “Meow for about a second, then pause.”
Call the sound a meow everywhere; no internal terms (accepted, voiced, calls).
Show candidate, rejection, accepted step (“Nice meow! +8”, or “Nice slide! +12”
for a pitch slide), and wandering feedback in a bubble above the cat, without
unreadable frame flicker. Silence never replaces the instruction or scolds the
pause after a meow. Meter bands follow calibrated thresholds. Explain
rank improvement on results. Loss guidance distinguishes timeout, scares,
and wandering. Keep rank color in a readable letter badge with dark text.

## Screens and accessibility

The approved visual direction is a pastel pixel garden: raised cat/bed/path,
rounded bush clusters, small flowers, crisp buttons/cards, and pixel hearts.
Walking and travel share a 400ms step; success uses a dedicated curled sleeping
row. Scared reactions preserve the same tabby identity and pixel style.
The source/approved prototype lives in pixel-art/design-preview; runtime art
is embedded in index.html.

Landing has the cat/world, short instructions, and Start. Starting/calibration
show status and Start over. Play shows mic meter, inspectable countdown,
status, and Start over; interrupted audio shows Tap to resume mic. Results
use a readable card with rank badge, rank-title headline, time/best, tip, retry,
and a screenshot hint. Short screens hide the rank tip and lift the sun so text
and controls stay clear.

LINE's in-app browser is redirected once to the same URL with
`openExternalBrowser=1`, which asks LINE to open the system browser.
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

## Phone tuning log

Read values on the phone with `?debug=1` (thresholds line and 3-second peak).
The debug label says `scream` for any loud frame, even a tap shorter than the
120ms hold; judge taps by whether "Too loud!" appears or catPos drops.
Change CONFIG volume values only from rows recorded here.

| Date | Device / browser | min / scare shown | Gentle meow peak | Shout peak | Screen-tap peak | CONFIG change |
|---|---|---|---|---|---|---|
| 2026-10-04 | not recorded | – | – | – | – | scareVolMultiplier 3.5, scareVolFloor 0.005 set by feel |
