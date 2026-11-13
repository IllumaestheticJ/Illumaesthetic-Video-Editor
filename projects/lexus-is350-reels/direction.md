# IS350 speed-run reels R1 / R2 / R3: direction

Director/editor, 2026-11-13. Three 9:16 reels, 1080x1920, 30 fps, built from the approved long-form (`projects/lexus-is350-speedrun-long`).
Contract: `brief.md`. Machine-readable spans: `spans.json` (the build reads it). Build: `python projects/lexus-is350-reels/tools/build.py`.

**What I read:** brief.md, CLAUDE.md, the style guide, the [story]/[pacing]/[text]/[audio] lessons, script_v2.md, timeline_v4.json, captions_v4.srt,
the word-level transcripts (`is350-long/transcripts/` large-v3 + `transcripts_medium/`), scan_shots.md + match/, the long-form feedback.jsonl, gfx.md,
assemble_long.py, and the smart-450 reel (direction, build.py, concat_assemble.py, review).
**What I looked at:** graded proxy frames (LUT `fx3a_slog3cine_to_709.cube`) with an x ruler, 4-6 frames per candidate span (sheets in
`/home/user/media/work/is350-reels/look/`). The crop keyframes below come from those sheets. I have not seen any 4K frame, music piece or vertical render yet.

## Rules applied (from the owner's long-form notes and the lessons)
- Dialogue is never clipped. Every kept line is a whole sentence with its word times checked on large-v3 and medium.en and on a 20 ms energy envelope.
  Exceptions are tight but in measured silence (listed per shot). Every spoken line is captioned.
- Plates are not blurred. No triangle counts, no reflector. Overlays sit on the footage (no black bars). One music piece per reel, no switching.
- IRL -> scan is a hard 1:1 cut on a beat, solved frame to solved frame, with the 3D agent's window on the IRL side.
- Safe area: no text in the top 220 px, the bottom 420 px or the right 120 px. Usable text box x 60-960, y 220-1500.
- No shot is reused inside a reel. Each car section appears in one continuous run per reel.
- Numbers on screen: 32 MIN from "go", 20 MIN without the crash (TIMER 2), the bet 15. Clock values only where a phone or watch is legible, or
  where the long-form already derived them (541 is one continuous take: CLOCK 1 = src - 74.57 s, checked against the phone 04:58.86 at 541@373.4).
- Ending on every reel: logo card (logo >= 720 px wide, >= 1.6 s) on the last downbeat, with "SCANS AVAILABLE AT ILLUMAESTHETIC.COM" under it.

## Crop method
Each 16:9 frame (1920x1080 coords) gives a 608x1080 window at `x0`, cut from the 4K original (1216x2160 px, scaled to 1080x1920, so no upscaling).
Moving subjects get keyframed `x0` (linear between keyframes, source time). Intermediates keep the full 16:9 width (3414x1920), so a crop can change later
without fetching the original again. No punch-out with blurred fill is used anywhere.

---

## R1 "THE CRASH" (story reel, about 30 s)

Hook (0-1.5 s): the host to camera, mid-sentence of his bet, "I think I can do it in less than the length of a YouTube video..." with the question
**HOW LONG TO 3D-SCAN A WHOLE CAR?** on screen from frame 0. Music under, low.

| # | reel t (approx) | source, in-out (orig. s) | crop x0 (1080p coords) | heard (transcript time) | overlay / caption | what is lost in the crop |
|---|---|---|---|---|---|---|
| 1 | 0.00-4.45 | FX30541 26.10-30.55 | 740 fixed (face at x 990-1080 in every checked frame) | "I think I can do it in less than the length of a YouTube video. 15 minutes." [26.26-30.24]; tail 0.31 s in room tone (-47 dB) | title top (y 260); pill **THE BET: 15 MIN** at "15" (29.62); captions | the shop to his left; the spread hands at 30.0 are cut at the wrists |
| 2 | 4.45-7.75 | FX30541 71.45-74.75 | tracks the phone: 886 -> 736 -> 666 -> 756 (71.6/72.8/74.0/74.7) | "Yeah. Three, two, one, go." [71.55-74.57] | captions; timer plate appears at "go" with CLOCK 1 00:00 | the blue car at the frame edge |
| 3 | 7.75-8.95 | FX30541 120.30-121.50 | 760 -> 650 | room sound + music (spray hiss) | timer plate CLOCK 1 00:45 -> 00:46 | the far side of the door opening |
| 4 | 8.95-15.50 | FX30541 376.70-383.25 | 690, 840, 420, 480, 720, 500, 630, 660 (at 376.0/377/378.5/380/381/381.8/382.6/383.2) | "How you feeling halfway through it?" "It just crashed." "It's never crashed on me before." [376.94-382.70] (lead 0.24, tail 0.55 s) | timer plate CLOCK 1 05:02 -> 05:08; at "crashed" (379.6) the plate turns red with a **CRASHED** pill; captions | the red Smart behind him; a fast handheld swing at 377-378.5 that the window follows |
| 5 | 15.50-17.85 | FX30542 12.40-14.75 | 800 -> 700 -> 700 | "Start a secondary timer. Now." [12.60-14.30] (lead 0.20 s in a measured -40 dB gap after "Alright, let's start there.") | pill **REBOOTED · TIMER 2**; TIMER 2 00:00 appears on "Now." (13.96); captions | nothing important: the camera spins onto the watch |
| 6 | 17.85-26.05 | FX30553 9.35-17.55 | 120 (watch), 600, 720 (host, arm up), 700, 650, 600, 650 (phone 32:53) | "20 minutes." "Done." "And the other one, 32 minutes." [9.70-17.13] + "Yep." to 18.03 is cut after "minutes" ends (tail 0.42 s) | timer plate: TIMER 2 20:24 (stopped, legible 553@9), CLOCK 1 32:53 on "32" (legible 553@16.14); captions | the car on the jack while he celebrates |
| 7 | 26.05-28.55 | V_RES_FULL (vertical render) 0-2.5 s | - | music | result card: **32 MIN FROM GO / 20 MIN WITHOUT THE CRASH / THE BET WAS 15** (rows staged on beats) | - |
| 8 | 28.55-30.2 | logo card | - | music ending | logo 760 px + CTA | - |

Music: the music agent's R1 piece (`music/R1/`): the run from "go" with the wind-up into a **dead stop on "crashed"** (shot 4, ~11.6 s),
the comeback on "Now." (shot 5), the run to the end. Ducked under every line. The reel is dialogue-led: cuts sit in the gaps between lines and are
nudged to the nearest accent only where no word moves.
Why this order: question -> bet -> go -> confident spray -> crash -> reboot -> answer is the whole story in 7 shots; the long-form needed 45 s for the
crash set-piece, here the host's own laugh carries it. Dropped for length: "Five minutes on the dot" (541 373.6) and the floor shots.

## R2 "REAL -> SCAN" (music reel, about 21 s)

Hook (0-1.5 s): the host scanning the powdered rear deck, **REAL CAR -> 3D SCAN** on screen from frame 0, then the first hard 1:1 cut at ~1.6 s.

| # | beats (approx) | source, in-out | crop x0 | heard | overlay |
|---|---|---|---|---|---|
| 1 | 0.0-1.6 | FX30541 233.60-235.319 (ends on f5641) | the 3D agent's V_PAIR_2 window (proposal 500: trunk lid, C-pillar, tail lamp) | music only | **REAL CAR -> 3D SCAN** (top band) |
| 2 | 1.6-3.6 | V_PAIR_2 | - | music | title stays to 2.6 s |
| 3 | 3.6-5.2 | FX30542 45.70-47.381 (ends on f1135) | V_MATCH_REAR window (proposal 450: plate, emblem, scanner) | music | - |
| 4 | 5.2-7.2 | V_MATCH_REAR | - | music | - |
| 5 | 7.2-8.8 | FX30542 223.60-225.309 (ends on f5401) | V_PAIR_3 window (proposal 500: hood + headlamp) | music | - |
| 6 | 8.8-10.8 | V_PAIR_3 | - | music | - |
| 7 | 10.8-12.4 | FX30554 9.40-11.053 (ends on f264) | V_MATCH_FRONT window (proposal 610: whole front, car centred) | music | - |
| 8 | 12.4-14.8 | V_MATCH_FRONT | - | music | - |
| 9 | 14.8-18.8 | V_RES_FULL | - | music | **LEXUS IS350 · FULL SCAN** / **32 MIN FROM GO · 20 WITHOUT THE CRASH** |
| 10 | 18.8-20.8 | logo card | - | music ending | logo + CTA |

Order rear quarter -> rear bumper -> hood -> front walk-out (as in the brief): alternates sides and heights and saves the strongest match (front, RMSE 0.4 px)
for last. Source sound is muted (music-driven; nothing spoken is kept, so nothing needs a caption). Lead-ins shorten if the music's bar is shorter;
every IRL lead-in ENDS on the solved frame (frame mapping in the build, not by trimming the end).

## R3 "HOW LONG DOES IT TAKE?" (question reel, about 21 s)

Hook (0-1.5 s): the clean blue IS350 front (before powder) with **HOW LONG DOES IT TAKE TO 3D-SCAN A WHOLE CAR?** on screen, the question heard over it.
The three takes of the question all start on a whip pan, so the question audio (541 14.75-17.45) is laid under a sharp car shot (J-cut) and we cut to
the guessers' faces for the answers only.

| # | reel t (approx) | source, in-out | crop x0 | heard | overlay |
|---|---|---|---|---|---|
| 1 | 0.00-2.70 | picture FX30541 37.00-39.70; sound FX30541 14.75-17.45 | 840 -> 1010 -> 900 (grille centred) | "How long do you think it'll take to scan this car?" [15.00-17.26] | title top; caption |
| 2 | 2.70-3.80 | FX30541 17.45-18.55 | 730 (face) | "I'll say two hours." [17.50-18.14] | pill **2 HOURS?**; caption |
| 3 | 3.80-4.70 | FX30541 22.06-22.95 | 730 | "Maybe 30 minutes." [22.08-22.68]; in-point in an 80 ms gap after "car?" (-45 dB), 2-frame fade-in, verified by re-transcription | pill **30 MIN?**; caption |
| 4 | 4.70-6.00 | FX30541 29.35-30.65 | 740 | "15 minutes." [29.62-30.24] (said quietly; lead 0.27, tail 0.41) | pill **15 MIN** (red: the host's bet); caption |
| 5-9 | 6.0-9.5 (one beat each) | 541 98.40-99.10 front spray (1000->1180); 541 175.00-175.70 hood spray (420->680); 542 111.00-111.70 scanner screen (700->740); 547 37.80-38.50 scanner light on the fender (650); 551 85.50-86.20 on the floor under the jacked car (730->700) | see left | music + room | none |
| 10 | 9.5-13.0 | FX30547 122.45-125.95 | 850 (head + scanner + front bumper) | "Is this the most optimal scanning position?" "Yeah." [122.73-125.63] | caption |
| 11 | 13.0-14.2 | FX30553 7.05-8.25 | 200 (rear badge and plate, the jack) | "Time." [7.33-7.81] | caption |
| 12 | 14.2-15.4 | FX30554 9.90-11.053 (ends on f264) | V_MATCH_FRONT window | music | - |
| 13 | 15.4-19.0 | V_MATCH_FRONT, hard 1:1 cut on a beat | - | music | answer card **32 MIN FROM GO / 20 MIN WITHOUT THE CRASH / THE BET WAS 15** |
| 14 | 19.0-20.8 | logo card | - | music | logo + CTA |

Sections: front (1), faces (2-4), process (5-9, each a different part: front, hood, screen, fender, underside), floor (10), rear (11), front (12-13, the
same front as shot 1 but now powdered and then scanned: the bookend is the answer). R3 shares the front pair with R2 on purpose (strongest pair);
R1 ends on V_RES_FULL, so each reel ends on a different scan.

## Assets and placeholders
- Vertical renders from `/home/user/media/work/is350-reels/renders/<id>/` as listed in `scan_shots.md`. Until a render exists the build uses a tagged
  placeholder (the IRL match frame, darkened, with "PLACEHOLDER <id>"), so a re-run swaps the real render in.
- Music from `/home/user/media/work/is350-reels/music/R*/` + `music.md`. Until it exists: a silent bed and an even grid.
- Graphics: one transparent ProRes 4444 overlay per reel from a new Remotion composition `ReelGfx` (1080x1920, 30 fps) in `remotion/src/gfx/reel/`
  that reuses the long-form's theme, the content-sized plate with equal padding and the red bar, the result-card rows and the caption style.
