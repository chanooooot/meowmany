# STATUS

**Goal:** Fair, responsive single-round mic gameplay with reliable retry and recovery.

**Now:** Approved pixel-garden design applied. 23 regression checks, 12 rendered states, narrow-screen bubble movement, and Web Audio synthetic win/cleanup verified.

**Next:** Verify actual voice feel, interruptions, and LINE fallback on iPhone Safari and Android Chrome over HTTPS.

**Easier input:** Pitch acceptance widened to 100–900Hz and call duration to
0.15–2.5s after reported pitch/length rejections. Quality still peaks at 0.9s;
phone volume floors remain unchanged. Expanded synthetic checks cover low/high
tones, short/long calls, and noise rejection. Actual phone feel needs verification.

**Sprite update:** Matching pixel-tabby scare pose and curled sleeping win row
embedded; original four-frame walk restored at the user's request. Sprite-gen extraction/composition checks
and 23 gameplay regressions pass. Source and GIF previews: `pixel-art/cat-upgrade`.
Local browser preview was blocked by browser URL policy; updated phone/landscape
rendering and live animation still need manual verification.

**Blocked:** No implementation blocker. Real-device audio/LINE verification needs actual phones.

_Updated: 2026-10-04_
