Original review at commit `d0e52152682cc9f6128323bec643d82a5f89fed5`. Evidence links below are pinned to that version; findings describe the pre-fix code.

Review goal: make the existing single-round microphone game responsive, fair, readable, and easy to retry.

Simpler approach: keep the one-file game and existing heuristic. Stabilize input events, resolve penalties and deadlines before rewards, and explain the rules. More content would multiply the current detection and fairness problems. Levels, models, dependencies, sound, and sharing APIs are unnecessary for this pass.

Scope: traced startup, calibration, RMS/pitch classification, event segmentation, movement, scream/drift penalties, timeout, ranking, best-time storage, win/loss, restart, backgrounding, error screens, accessibility, sprites, and project instructions. No gameplay source was changed.

Verification: executed the actual inline script in Node with a controlled clock and small DOM/audio mocks. Checked real Chrome layout in a 390px iframe at heights 844px and 320px. Inspected the rendered screenshot and decoded cat sprite. Synthetic audio confirms algorithm behavior; it does not establish real-phone detection quality or Safari audio recovery.

The original reproduction artifacts were temporary. Current regressions are retained in `tools/test-game.cjs`; run `node tools/test-game.cjs`.

**1. Major — loudness flicker can turn one loud sound into an instant loss.**

Evidence: [index.html:576](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L576) applies a penalty on every transition into `scream`. There is no hysteresis or rearm interval. With the quiet-room thresholds, seven frames alternating RMS 0.0041 and 0.0039 produce four penalties. Starting at 50, the cat loses. Each penalty is 15 ([index.html:179](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L179)).

Why: punishment depends on threshold jitter, rather than distinct player actions. A player cannot learn a consistent rule.

Change: latch a scream event; rearm only after a short, sustained period below a lower threshold. Put the margin and rearm time in CONFIG. Check a sustained shout, flickering volume, and two separate shouts.

**2. Major — one rejected audio frame destroys an otherwise valid meow.**

Evidence: [index.html:540](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L540) ends tracking on every non-meow label. A 0.55s attempt with a single `talk` frame at 0.25s splits into two segments below 0.3s. Actual result: zero accepted events and “Try a longer meow.”

Why: pitch-estimation glitches become false negatives. The feedback blames duration when the attempt was long enough.

Change: tolerate a brief unvoiced/out-of-range gap before ending a meow. Keep scream handling immediate. Test one-frame gaps and two genuinely separate meows so tolerance does not merge them.

**3. Major — a scream-ending meow can win before its penalty is processed.**

Evidence: [index.html:575](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L575) calls tracking before the scream handler. Tracking counts any non-meow ending ([index.html:546](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L546)). At cat position 96, 0.5s of meow followed by `scream` adds 8 and wins. `applyScream()` then returns because the state is already `won` ([index.html:415](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L415)). Away from the finish, the same input receives both reward and penalty.

Why: the game rewards the very input it says scares the cat.

Change: process scream before meow completion and discard the current candidate when a scream occurs. A scream-ending candidate should produce one penalty and no reward.

**4. Major — the deadline is checked after the winning input.**

Evidence: [index.html:577](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L577) runs `gameTick()` after event processing. A finishing candidate at 60.01s wins; `gameTick()` cannot change the ended state. Reproduced with cat position 96 and a candidate started at 59.7s. Timeout itself is at [index.html:436](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L436).

Why: the visible countdown is not the effective deadline.

Change: resolve timeout before accepting that frame's audio events. Test completion immediately before, at, and after 60s.

**5. Major — retry can show no controls; audio setup errors can leave it stuck.**

Evidence: [index.html:270](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L270) hides error/results before awaiting context resume and mic permission. After a completed round, landing and scene are already hidden. A pending retry therefore hides all four screens. Separately, source/analyser creation at [index.html:292](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L292) and calibration at line 303 are outside the catch. Injecting a source-setup failure rejects `startAudio()`, leaves `isStarting=true`, and leaves every screen hidden.

Why: a player sees only scenery and cannot retry again when setup fails.

Change: keep a visible starting screen and put the entire setup/calibration flow inside error handling with guaranteed guard cleanup. Keep a cancel action available during acquisition. Test delayed permission, rejection, setup failure, and retry after each.

**6. Moderate — the winning cat is clipped on phone widths.**

Evidence: [index.html:424](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L424) maps position 100 to left 80%, without accounting for the 130px sprite ([index.html:81](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L81)). Chrome measured x=312 and right=442 in a 390px viewport: 52px beyond the screen. The cat sprite contains opaque pixels nearly to the frame edge. `#world` clips overflow ([index.html:25](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L25)). The screenshot confirms visible clipping.

Why: the success moment loses the cat's face/body instead of placing it naturally on the bed.

Change: map progress between pixel bounds that account for cat width and bed position. Also make position 0 visually retreat offscreen: the current mapping still puts the cat's left edge at 5% when it loses.

**7. Moderate — background frame callbacks can grant free progress after resume.**

Evidence: [index.html:431](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L431) updates `lastTickAt` even while paused. Resume then adds the full hidden duration to that timestamp ([index.html:613](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L613)). Reproduction: hide at 7s, run one paused tick at 8s, resume at 9s. Next delta is -1s, so drift adds 3 to cat position.

Why: browsers that deliver a callback during the hidden interval can change round balance. This is conditional on callback timing; it is not a claim that every phone does it.

Change: set `lastTickAt = now` on resume instead of shifting it. Shift round/drift clocks by paused duration. Test both no hidden callback and one hidden callback.

**8. Moderate — replay inherits the previous round's meow cooldown.**

Evidence: [index.html:316](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L316) resets candidate state but does not reset `lastCountedMeowAt`, declared at [index.html:527](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L527). A new-round candidate ending 350ms after the previous counted event is rejected with “Let the cat listen...”.

Why: a round reset does not reset every gameplay gate. Default calibration usually masks this timing, so it is lower priority than the faults above.

Change: reset the counted-event timestamp along with candidate state. Reset obsolete animation timeouts at the same lifecycle boundary.

**9. Moderate — result colors are difficult to read against the world.**

Evidence: rank colors are defined at [index.html:13](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L13), used on the title at [index.html:50](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L50), and on small “New best!” text at [index.html:97](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L97). Calculated contrast for S gold against the two sky endpoints is about 1.03:1 and 1.32:1. B pink against the light sky is about 2.00:1. The short-screen screenshot shows pink result text over green scenery.

Why: the rank and reward are core screenshot content, but color treatment makes them hard to scan.

Change: use dark ink for readable text and keep rank color in a badge/border. A small opaque result panel would also make contrast independent of screen height. Check every rank and loss state.

**10. Gameplay improvement — teach the actual accepted action and its timing.**

Evidence: landing instructions only mention meowing and screaming ([index.html:123](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L123)). Actual acceptance requires 150–600Hz, 0.3–1.5s, and a narrow volume band ([index.html:169](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L169), [index.html:512](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L512)). Reward arrives only when the candidate ends ([index.html:540](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L540)). `talk`/silence do not provide ongoing normal-mode detection guidance in the frame loop ([index.html:568](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L568)).

Why: players can repeat an ineffective sound without knowing whether it is too low, too quiet, too loud, or unfinished.

Change: add one short instruction: “Gentle meow for about a second, then pause.” During calibration say “Stay quiet.” Show candidate feedback such as “Hearing you…” and explain the specific reason for rejected attempts. Keep feedback stable enough to read.

**11. Gameplay improvement — retain forgiving detection, but acknowledge what it measures.**

Evidence: classification only checks loudness and fundamental pitch ([index.html:512](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L512)). A pure 220Hz tone at RMS approximately 0.00212 returns `meow`. There is no voicing-confidence check in the autocorrelation search ([index.html:493](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L493)); deterministic uncorrelated noise produced in-range estimates on 44 of 100 synthetic frames. That is frame-level evidence, not proof noise wins a full round.

Why: this is a pitch game, not semantic meow recognition. Humming exploits are acceptable under the stated forgiving design; confusing noise and voice is less useful.

Change: prioritize tolerant event segmentation over strict recognition. If phone tests show noise-triggered events, add a modest periodicity/confidence gate. Do not add a model or reject ordinary human meows to enforce authenticity.

**12. Gameplay improvement — make drift pressure visible and explain losses accurately.**

Evidence: drift starts four seconds after the last accepted event, regardless of current `talk`/meow candidate ([index.html:437](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L437)). At start position 50 and speed 3/s, complete silence loses around 20.7s, although the round timer is 60s. A position-based loss always says “The cat got bored” ([index.html:337](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L337)), even when four scream penalties caused it.

Why: players cannot distinguish patience, silence drift, and scare penalties. Increasing the timer would not solve this.

Change: show “The cat is wandering…” when drift begins, teach that only accepted calls reset it, and track a minimal loss reason for scream versus drift. Playtest current balance after input fixes: one scream costs roughly two plain meows; five gliding or seven plain accepted meows win without penalties.

**13. Gameplay improvement — expose the skill behind rank before the result.**

Evidence: movement gives glide a +4 bonus ([index.html:407](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L407)), while quality peaks at 0.9s and adds glide credit ([index.html:554](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L554)). Rank mixes 60% average quality with 40% time ([index.html:185](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L185), [index.html:354](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L354)). The normal player never sees these criteria before the end.

Why: unexplained grades make replay feel arbitrary. The player needs a learnable improvement, not more modes.

Change: distinguish a glide reward with brief feedback, then show one end-screen tip: “Smooth one-second meows earn better ranks.” Keep the existing rank/time system. Do not add scream penalties to scoring until playtests show a need; retreat already costs time.

**14. Performance improvement — constrain pitch work after measuring phones.**

Evidence: [index.html:494](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L494) computes all lags with nested loops. At 2047 retained samples this is 2,096,128 products per voiced frame, plus per-frame allocations. The frame loop even detects pitch when volume already qualifies as a scream ([index.html:572](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L572)). Node VM measured approximately 9ms per call here; that is not a phone benchmark.

Why: CPU cost can delay feedback and produce sparse timing samples on weaker devices.

Change: skip pitch on scream frames first. Measure real-phone frame time. If needed, search only useful pitch lags or run pitch detection at a lower fixed cadence while keeping RMS/meter responsive. Verify accuracy before adopting optimization.

**15. Reliability/accessibility improvement — handle device interruptions and label screens correctly.**

Evidence: the visibility handler only shifts clocks ([index.html:603](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L603)); there is no stream-track `ended` handling or AudioContext state recovery. The startup catch labels every acquisition/context failure “Mic access denied” ([index.html:287](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L287)). The timer is hidden from assistive technology ([index.html:150](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L150)). English A/B titles receive `lang='th'` ([index.html:355](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L355), line 361).

Why: a removed/suspended mic can look like player silence; failure guidance may describe the wrong remedy. Screen readers lack round timing and may pronounce English titles incorrectly.

Change: show a recoverable pause/error when input actually ends. Check context state on return and show a tap-to-resume action if necessary. Distinguish denial, no input device, and device/setup failure. Make time inspectable without announcing every second. Apply Thai language metadata only to Thai titles. Test these behaviors on Safari and Chrome phones; mocks cannot establish them.

**16. Maintenance improvement — preserve scope and replace misleading verification claims.**

Evidence: [AGENTS.md:10](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/AGENTS.md#L10) says SPEC/PLAN remain accurate, while [HANDOFF.md:10](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/HANDOFF.md#L10) records removed SFX, renamed game, and a pixel sprite world. PLAN still requests SFX. Existing executable checks only cover rank thresholds in debug mode ([index.html:593](https://github.com/chanooooot/meowmany/blob/d0e52152682cc9f6128323bec643d82a5f89fed5/index.html#L593)); debug movement keys bypass detection gates.

Why: another contributor can restore intentionally removed behavior or call the game verified after bypassing its hardest path.

Change: update the status/architecture notes to the shipped behavior. Keep a small runnable regression harness for event jitter, scream order, deadline, pause, retry, and failures. Preserve one HTML file, embedded assets, no backend/analytics, and no new runtime dependencies. Current source processes mic data locally; there is no application upload path in the reviewed script. Continue real-phone voice testing alongside synthetic checks.

Recommended order: (1) fix event segmentation, scream rearming/order, deadline, and startup recovery; (2) fix cat bounds, pause/reset behavior, and contrast; (3) improve feedback and loss/rank explanations; (4) playtest and tune CONFIG on phones; (5) update documentation and retain regression checks. Tune thresholds only after the event faults are fixed so tuning does not hide logic bugs.

Verdict: fix-then-ship — unstable event handling can punish a valid attempt or turn a scream into a win.


Resolution update (2026-10-04):

- Findings 1–4: added a sustained-quiet scream rearm latch, 100ms candidate-gap tolerance, scream candidate discard, and deadline-first frame processing.
- Finding 5: setup/retry now show status and a cancel button; the full audio/calibration flow handles failures. Session tokens prevent cancelled work from changing newer attempts and stop late-granted streams.
- Findings 6–8: cat progress now uses sprite/bed bounds, pause resume resets the tick timestamp, and retries reset event gates/animation timers.
- Finding 9: dark text, rank accent, and an opaque result card replace low-contrast colored text. Short screens get compact result spacing.
- Findings 10–13: landing/calibration teach the action; stable input/rejection/glide/drift feedback, specific loss reasons, and a result rank tip explain gameplay. The existing round length, steps, rank weights, and phone volume floors remain unchanged pending device evidence.
- Finding 14: scream/recovery frames skip pitch work. Further detector/cadence optimization remains conditional on actual phone profiling, as the review recommended.
- Findings 11 and 15: a configurable correlation gate rejects the tested unvoiced noise; mic loss, context interruption, tap-to-resume, and error classification now have recovery paths. Timer is inspectable without per-second announcements; result language metadata matches text.
- Finding 16: current specification, plan, agent instructions, status, and handoff now agree. The app remains one embedded-asset HTML file with no runtime dependencies, audio uploads, or SFX.

Verification: the retained Node harness passes 21 regression checks. Chrome checks phone/landscape layout, result readability, cat bounds, and visible short-screen retry. A real Web Audio synthetic-stream integration completed five gliding calls, won at S rank, and stopped the microphone track. Actual phone voice feel, Safari recovery policy, LINE behavior, and device performance still require the real-device gate in PLAN.md.
