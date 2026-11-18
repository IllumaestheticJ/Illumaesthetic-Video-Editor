# BF 9 days-left-countdown: draft v0 notes (2026-11-17)

This is a quick first draft made because the owner asked, through the parent session, for a quick short first draft of every BF video. It is preview quality and **not approved for posting**.

Output: `/home/user/media/work/out/bf-days-left-countdown_v0.mp4` (media is not in git).

## Assumptions (my defaults for the open questions in shotlist.md)
| Q | Default used in v0 |
|---|---|
| Q1 Sale end date | **Unknown.** v0 renders a single sample day, **"3 DAYS LEFT"**. **The 3 is a placeholder number**, not computed from a real end date. |
| Q2 Which days | Only the 3-day sample. |
| Q3 End date on screen | No date anywhere. |
| Q4 Offer line | None. The end card says "BLACK FRIDAY" with no price or percent. |
| Q5 Numeral style | A: a silver numeral built by the cyan scan sweep (Blender geometry from `--text`). |
| Q6 Del's gesture | Tape-roll tap (no watch; the locked sheet has none). In v0 it's only a small dip on the hits. |
| Q7 Music | **Changed:** "BREAKING NEWS" - DJ DF KIT (TikTok CML 7622371201206765569), from 0 s. DJ EV's "BLACK FRIDAY" is quiet until about 27 s, so it has no usable hit in a 9 s reel that starts at the song's beginning. Source file: CML preview download, full length 72.8 s. |
| Q8 Car in shot 1 | Integra DE GLB (`eps-acura-integra-de-v29.glb` from the website zip, Drive 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7). Kit: lip, skirts, spats, Sport Wing, trunk lip; flares hidden. Rendered silver as one still with a 5 % push. The BF 2/3 plates don't exist yet. |

## Placeholders (not final)
- **Del & Eps:** cut-outs of the front views from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`. On screen they are labelled "placeholder art (model sheet), not final".
  - They are static: there is no scan-raise or eye change, and no real tape tap.
  - No Higgsfield credits were spent. That needs your OK in this chat.
- The plate is the website CGI model in the silver look, not the car's real scan.

## Timing (measured on the decoded audio, 30 fps)
| Frame | Time | Event |
|---|---|---|
| 0 | 0.00 | Shot 1: Integra + Del. Tape dips at 0.34 s and 1.23 s (low hits) |
| 59 | 1.967 | Cut on the 1.96 s hit. Shot 2: black, Eps, scan sweep starts |
| 139 | 4.633 | Drop (RMS rise 4.62 s): numeral completes in silver, key-light flare |
| 154 | 5.133 | "DAYS LEFT" slams in (5.13 s hit) |
| 180 | 6.000 | Del slides in (6.01 s hit) |
| 208 | 6.933 | Cut on the 6.92 s hit: wordmark card (720 px), BLACK FRIDAY, EPSILON.PLUS |
| 282 | 9.400 | End (picture fades over the last 14 frames, audio fades from 8.8 s) |

## Render cost measured
- Numeral 1080x1920, Cycles CPU, 16 samples: about 6.5 s/frame, 149 frames, about 16 min per number.
- Plate still: one frame at 64 samples.
- Compositing and encoding: about 1-2 min.

## Checks run on the delivered file
- 1080x1920, 30 fps, 282 frames, 9.40 s, H.264 + AAC.
- Loudness (ebur128 on the encoded file): -13.5 LUFS integrated (target -14), peak -2.6 dBFS.
- Cut sync on the decoded output audio:
  - f59 is +3 ms from its hit, and f208 is +17 ms from its hit.
  - At f139 the numeral completes on the section start (4.62 s). There is a stronger accent inside the drop at 4.82 s; v1 could move the completion flash there.
- Contact sheet reviewed. The first pass had Del and Eps overlapping "DAYS LEFT", so I shrank both to 500 px and moved them below the text.
- Edges: the numeral, text and wordmark are all inside the frame.
- Wordmark is 720 px wide.

## v0.1 (2026-11-17): Del & Eps removed (owner)
The owner's instruction, relayed by the parent: "tell all the black friday agents to not use del & eps, just typical branding content".
- Output: `/home/user/media/work/out/bf-days-left-countdown_v0.1.mp4` (9.4 s, same cuts and audio).
- **Removed:** the Del and Eps placeholders, the "placeholder art" label, Del's tape taps and Del's step-in. `tools/char_placeholders.py` is deleted. No Higgsfield credits were spent at any point.
- **Shot 1:** the plate is re-rendered with the car centred and no Del; the edit crops in 20 % and pushes 6 %.
- **Shots 2-3:**
  - the numeral is re-centred (+72 px; the render had framed it left to make room for Eps);
  - "DAYS LEFT" sits at y 1300;
  - the "BLACK FRIDAY SALE" line fades in on the 6.01 s hit (replacing Del's entrance).
- **Shot 4:** unchanged (720 px wordmark, BLACK FRIDAY, EPSILON.PLUS).
- **Still a placeholder:** the number 3 (no sale end date yet).
- **Checks:** -13.5 LUFS, peak -2.6 dBFS. Cuts are unchanged (+3 / +17 ms; the drop is on the section start at 4.62 s). The contact sheet was reviewed, and nothing overlaps or leaves the frame.

## v0.2 (2026-11-17): safe zones (owner rule, knowledge/safe-zones.md)
- Output: `/home/user/media/work/out/bf-days-left-countdown_v0.2.mp4`.
- **Before (v0.1 sheet):**
  - the car's nose and front wheel were in the right rail;
  - the top of the "3" was in the top/feed-crop band, and its right side was in the right rail;
  - the last "T" of "DAYS LEFT" and "BLACK FRIDAY SALE" were in the right rail.
- **Fix:** the layout is centred on x 484, the centre of the safe box, everything stays inside x 48-920 / y 285-1440, and the numeral render is clipped to the safe box.
  - Shot 1: car push 1.04 → 1.09.
  - Numeral: rendered at 0.72 scale, at y 330-1018.
  - "DAYS LEFT": 118 px at y 1110. "BLACK FRIDAY SALE": 52 px at y 1235.
  - Wordmark: 720 px, block at y 790-1010.
- **Check:** across all 282 frames, the pixel extent is x 47-919 / y 326-1257. The one 1 px touch (the car at frame 58) was fixed; after the fix, frame 58 measures x 51-909.
- The `safezone_check.py` sheet was reviewed: nothing in red or amber.
- Loudness is unchanged: -13.5 LUFS, peak -2.6 dBFS.

## v0.3 (2026-11-17): URL
- The end card reads **WWW.EPSILON.PLUS** (owner: always with www.). It is 42 px, x 195-771 / y 997-1027, inside the safe box.
- Output: `/home/user/media/work/out/bf-days-left-countdown_v0.3.mp4`. The safezone sheet is clean; overall extent is x 51-919 / y 326-1257.

## v0.4 (2026-11-17): drive-over and drift-over variants (user request)
User: "have it be Black friday sale text and then a car driving over it and the text changes to X days left, make another version where a car is drifting over the text to change it to X days".
- `tools/drive_over.py` (Blender) puts "BLACK FRIDAY / SALE" on a black gloss floor as 3D silver type. The Integra GLB enters from the left, and the text is wiped to "3 DAYS / LEFT" right behind the car: the wipe follows the car's x.
  - Drive mode: the car rolls straight across.
  - Drift mode: the car yaws to about 38° with counter-steer, and wheel smoke puffs follow it.
- The swap completes on the drop (f139, 4.62 s). The car is off the text by then and exits right.
- `tools/compose_drive.py`: the render for f0-207, then the same end card on the 6.92 s hit.
- Audio, cuts and loudness are the same as v0.3.
- The drift render was stopped by the task time limit at frame 190, so frames 191-207 hold frame 190 for 0.57 s after the drop. This is a preview only.
- Render: 720x1280 at 12 samples, upscaled. Measured at about 13.5 s/frame, about 47 min per mode.
- Outputs: `/home/user/media/work/out/bf-days-left-countdown_v0.4_drive.mp4` and `_v0.4_drift.mp4`.
- **Known issues in v0.4, fixed in v0.5:**
  - The floor type is Inter Display Black. It should be Unbounded per the new font rule.
  - Triangle streaks on the letters. The cause was the old and new text caps lying in the same plane, which made them z-fight. The fix is to lift the new text 3 mm (v0.5).
  - The text centre is at x 511 instead of 484.

## Font rule (owner, 2026-11-17, `knowledge/fonts.md`)
- Headline floor type is Akira. The owner hasn't uploaded the file, so **Unbounded 900 stands in**.
- The end card sits next to the logo, so it uses Unbounded: "BLACK FRIDAY" at 500 and WWW.EPSILON.PLUS at 400. This is applied to the end card from v0.4.

## v0.5 (2026-11-17): drive and drift, with the fixes
- Outputs: `/home/user/media/work/out/bf-days-left-countdown_v0.5_drive.mp4` and `_v0.5_drift.mp4`. Both are 9.4 s and full renders, with no held frames.
- Floor type is Unbounded 900, standing in for Akira. The new text is lifted 3 mm, so there is no z-fighting. Camera shift_x is 0.0285.
- Checks:
  - Both run at -13.5 LUFS with a -2.6 dBFS peak.
  - The safezone sheets are reviewed. All text and the logo sit inside the box; only the moving car crosses the rails on entry and exit.
  - The text centre measures at x 483.
  - "3 DAYS LEFT" is fully revealed by f139, and the car is clear of the text by then.
- Still open: the Akira file, the real day number (needs the sale end date), and whether the drift smoke should be heavier.

## v0.6 (2026-11-18): Akira
- The floor headline is now **Akira Expanded SuperBold**. The owner holds the licence; Drive ID 1nrF80enolDd9HAu5807kv5XIx0cUSDya, SHA-256 verified. It lives in `assets/fonts/akira/` and is gitignored.
- No missing glyphs: every string renders in the font.
- Tracking is 1.25 and line spacing 1.15. At default tracking the flat, wide glyphs fused at the floor camera angle.
- The end card stays Unbounded 500/400, because it sits next to the logo.
- Outputs: `/home/user/media/work/out/bf-days-left-countdown_v0.6_drive.mp4` and `_v0.6_drift.mp4`.
- Checks:
  - Both run at -13.5 LUFS with a -2.6 dBFS peak.
  - The safezone sheets are clean: text x 80-882, and only the moving car crosses the rails.
- A container restart interrupted the drift render at f108. `drive_over.py` now skips frames already on disk (`use_overwrite=False`), and the drift render resumed from there.

## v0.7 (2026-11-18): text centred (user: "center the text")
- The floor text is centred in the frame. Measured centres:
  - "BLACK FRIDAY SALE": x 537, y 959.
  - "3 DAYS LEFT": x 540, y 963.
- Text width went from 4.6 to 4.35, so the frame-centred block stays inside the x 920 rail (x 156-917). Camera: shift_x 0, shift_y -0.0262.
- End card: centred on x 540 / y 960, block x 180-900 / y 832-1087.
- Outputs: `/home/user/media/work/out/bf-days-left-countdown_v0.7_drive.mp4` and `_v0.7_drift.mp4`.
- Checks: -13.5 LUFS with a -2.6 dBFS peak. The safezone sheets are clean; only the moving car crosses the rails.

## v0.8 (2026-11-18, not delivered; superseded by v0.9)
- Readability rule (owner, via @parent): "3 DAYS LEFT" was held to the 8.16 s hit and the end card ran to 12.6 s. Loudness went to -14 LUFS.
- The user's next notes arrived before delivery, so the design moved on to v0.9.

## v0.9 (2026-11-18): user notes + readability rule + -14 LUFS
**User:** "first one have the car drive from the top down. have the first scene a bit faster, currently just black friday text is too long ... Put the percent deals. also pick a low stock product and say only X left! (you can estimate ...)"

| Time | Frame | Section | Readable |
|---|---|---|---|
| 0-2.48 s | f0-74 | BLACK FRIDAY SALE on the floor. The car enters about 1.2 s (drive: from the top; drift: from the left) and reaches the text on the 2.48 s hit | 2.5 s |
| ~3.4-6.02 s | f100-180 | 3 DAYS LEFT, clear of the car | about 2.6 s |
| 6.02-9.40 s | f181-281 | Card A: **UP TO 60% OFF** (floor still, kick and push) | 3.4 s |
| 9.40-13.84 s | f282-414 | Card B: **ONLY 2 LEFT** with a COROLLA HATCH SIDE SKIRTS label | 4.4 s (7 words needs 4.1) |
| 13.84-17.3 s | f415-518 | End card, fade 16.8-17.3 s | about 2.7 s |

**Where the numbers come from:**
- **60%:** the live Pricing tab (read 2026-11-18). The top tier is 60%, on the Integra rear trunk lip in ABS gloss black and in carbon. Every other priced item is 7-50%.
- **ONLY 2 LEFT** is an **estimate**, as the user allowed:
  - The Corolla Hatchback (E210) PU side skirts have **5 in stock** (Shopify and the sheet's In Stock column) and are 30% off ($400 → $280).
  - Last year's sale (Nov 20 - Dec 2) sold 5 of them, about 0.42 a day.
  - At "3 days left" the sale is about 9 days in, so about 1-2 are left: shown as 2.
  - Per-day formula: `stock_left = max(1, round(5 - 0.42 * days_elapsed))`. Re-check Shopify stock on the morning of each post.
- PRICES.md says "no stock counts unless the owner asks". The user asked for this one in chat.

**Motion:**
- `drive_over.py --mode down`: the car drives toward the camera (yaw 0), from y 12 to y -3 by the drop, at 0.25 m per frame. The wipe runs on world Y.
- `--mode drift --lead 40`: a faster slide, 0.35 m per frame.
- `--mode none` renders the floor text alone (the cards).
- Audio: 0-17.3 s, fade from 16.8 s, two-pass loudnorm to -14.0 LUFS, peak -3.3 dBFS.

**Re-timed (same day): the owner revised the readability rule** to 1.8 s for 1-3 words, +0.3 s per extra word, 2.2 s for prices. Only the edit changes; no re-render. The total is now **13.6 s** (was 17.3 s).

| Time | Frame | Section | Readable / minimum |
|---|---|---|---|
| 0-2.48 s | f0-74 | BLACK FRIDAY SALE | 2.5 s / 1.8 |
| ~3.33-5.14 s | f100-153 | 3 DAYS LEFT | 1.8 s / 1.8 |
| 5.14-7.62 s | f154-228 | UP TO 60% OFF | 2.5 s / 2.2 |
| 7.62-10.82 s | f229-324 | ONLY X LEFT + COROLLA HATCH SIDE SKIRTS | 3.2 s / 3.0 |
| 10.82-13.6 s | f325-407 | End card (fades 13.1-13.6 s) | about 2.1 s / 1.8 |

- Audio is 0-13.6 s, -14.0 LUFS, peak -3.3 dBFS.
- The 7.62 s cut is a lighter onset (0.31). The others are strong hits.

**Stock number:** the parent flagged that "2" is a projection; the data says 5. Both cards are prepared (`cardB2` = "ONLY 2", `cardB5` = "ONLY 5"), and the user picks. The stock line is its own one-minute floor still.
