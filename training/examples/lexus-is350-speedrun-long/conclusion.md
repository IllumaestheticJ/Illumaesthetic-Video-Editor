# L1 conclusion (slot 4:36.8-5:04.8, then the 5 s end card)

Written 2026-11-13 by the conclusion agent. Recommended version as data: `conclusion_edl.json` (ids `CON_*`, replaces event E71).
Hand-off: E70 ends on the reflector-removed pocket with P8 resolving. Hand-off to: E72 end card (G15), hard cut.
Every number below is the owner's (32, 20), the STL header (24,999,992) or said on camera (15, 541 [00:26.3]). No accuracy, spec, price or comparison.

## Material checked (frames pulled with `ive frame` / `ive sheet`)

- **FX30555** (4K, 31.0 s): host (navy "Berkeley" tee) holds scanner + spray gun, crew member in black polo with lanyard behind him, car with powder fading on the hood. Frames at 11.6, 14.0, 15.5, 15.8 show the host speaking to camera, no plate visible (hidden by his legs / below frame).
- **Plate:** legible in 555 at 3.2 s and 4.0 s (`...488`), at **25.86 s bottom-left (`9JT...`)**, a fragment at 26.5 s, and fully on the end pan from ~28 s. The recommended cut uses 25.70-27.30, so CON_03 needs a tracked blur. Nothing else in the cut shows it.
- **Silent "pose" shot not used:** the pose with both tools raised (555 5.2-6.5) overlaps "Caleb", and the quiet frames at 3-5 s show the plate and an open mouth with no audio. The pose on "fast" (27.15) does the job.
- **FX30553 sheet:** phone stopwatch legible at **553 @16.14 = 32:53.18**. It supports "32 minutes" (truncated), but 553 is taken (E61-E65, audio of 13.7-18.1 in E62), so it is NOT used. Owner: if you want a legible 32 on screen, this is the frame (see questions).
- **Not used and why:** 555 5.38-7.52 "Caleb" (name); 8.50-11.00 "30 minutes actual" (conflicts with 32); 16.02-21.20 "10 minutes if I just did the exterior, with the power of a spray gun, AESUB Violet, and the Artec Leo" (ambiguous 10, brands); 21.70-25.10 "any other scanner out there that can do it faster" (excluded claim); no ad line.

## Version A (recommended): host-sync led, 28.0 s

Rail = HUD rail frozen at CLOCK 1 "32 MIN" / TIMER 2 "20 MIN" on IRL and cards; hidden on the scan (as E68-E70). Captions in the rail only. Timeline times pre-beat-snap.

| id | time in-out | source (clip in-out s) | see | hear | HUD rail | gfx cue (exact text) | blur |
|---|---|---|---|---|---|---|---|
| CON_01 | 4:36.81-4:40.95 (4.14) | FX30555 11.64-15.78 | Host to camera outdoors, scanner + spray gun in hands, crew member behind | "If we ignore the scanner crashing on me... 20 minutes. 20 minutes for the whole car," [555 [00:11.6]-[00:15.8]] | frozen C1 32 MIN / T2 20 MIN; RESULT | RAIL_CAP: "If we ignore the scanner crashing on me..." / "20 minutes. 20 minutes for the whole car." | none visible |
| CON_02 | 4:40.95-4:45.95 (5.0) | gfx:CON_G1 | Answer card on black | music only (bed back up) | frozen; RESULT | CON_G1: **HOW FAST?** / **32 MIN · FROM "GO"** / **20 MIN · WITHOUT THE CRASH** / small: **THE BET WAS 15** (one line per beat) | - |
| CON_03 | 4:45.95-4:47.55 (1.6) | FX30555 25.70-27.30 | Host leans in, lifts the scanner | "Yeah, this thing's fast." [555 [00:25.9]-[00:27.1]] | frozen | RAIL_CAP: "Yeah, this thing's fast." | front plate bottom-left at 25.86: track + blur |
| CON_04 | 4:47.55-4:53.05 (5.5) | gfx:CON_G2 | So-what card on black | music only (swell) | frozen | CON_G2: **A FULL CAR IN ABOUT A COFFEE BREAK** / sub **24,999,992 TRIANGLES: THE STARTING POINT FOR NEW PARTS** | - |
| CON_05 | 4:53.05-5:04.81 (11.76) | SC_CON_HERO (new request, 11.76 s) | Full car, satin silver on black, one slow pull-back, no turntable; lower-left black kept clear | music only; P7 tail enters ~4:55.6 | hidden | CON_G3 (appears +4.8 s): **LINK IN THE DESCRIPTION** (bottom-left, halo) | plate flattened in render |

Story in one breath: the host says it in his own voice, the card makes it unmistakable (and keeps the bet visible), one beat of personality, the "so what", and a clean last picture of the product for the CTA. The viewer saw G08 at 3:50, so CON_G1 only restates it as the answer, tied to the bet. If the owner thinks it is too repetitive, drop the "32" row only after confirming (it would then not be spoken or shown here).

**Scan request for the 3D agent (no `scan_shots.md` existed):** `SC_CON_HERO`, 11.76 s, full-frame 1920x1080, whole car from a front three-quarter, slow continuous pull-back (not a turntable, no rotation of more than a gentle drift), plate flattened, car above y=900 not needed (rail hidden), black lower-left kept clean. If it does not arrive: hold card CON_G2 and extend it, and run the CTA label on that card (loses the last product picture; flag it).

**Music:** P8 bed continues from the reveal (ducked -12 dB under the two sync lines, back to full on cards). P7 tail (1082.3-1096.5) comes in on a bar line near 4:55.6 so its native fade (1090-1096.5) lands across the end card. Beat-snap cuts to the nearest accent within +-0.15 s; CON_01 out and CON_03 in/out have 0.2-0.6 s air, never cut inside a word.

## Version B: scan/graphics led, music only, 28.0 s

| id | time in-out | source | see | hear | HUD rail | gfx cue (exact text) | blur |
|---|---|---|---|---|---|---|---|
| B1 | 4:36.81-4:41.81 (5.0) | gfx card | Answer card on black | music only | frozen C1 32 MIN / T2 20 MIN; RESULT | **HOW FAST?** / **32 MIN · FROM "GO"** / **20 MIN · WITHOUT THE CRASH** / **THE BET WAS 15** | - |
| B2 | 4:41.81-4:52.81 (11.0) | SC_CON_HERO (new) | Full car, slow pull-back | music only | hidden | label **A FULL CAR IN ABOUT A COFFEE BREAK** (+1.0 to +5.5 s), then **THE STARTING POINT FOR NEW PARTS** (+6.0 to +10.5 s), bottom-left over black | plate flattened |
| B3 | 4:52.81-5:04.81 (12.0) | SC_CON_SIDE (new) | Second scan move: car side-on, slow lateral drift, mesh not shown (G11 already did) | music only; P7 tail from ~4:55.6 | hidden | CTA label **LINK IN THE DESCRIPTION** (+5.0 to +11.5 s) | plate flattened |

B has no host and one card, so it needs two new scan shots, and the host's face disappears for the last 33 s. It is the safe fallback if the owner dislikes the "thing's fast" line or 555 audio is unusable.

## Recommendation

**Version A.** It is the only one with the host's real voice at the end of the video, it needs one new scan shot instead of two, and the 20-minute line lands as spoken words with the frozen rail showing 20 MIN at the same moment. Length **28.0 s exactly** (26.4 s if CON_03 is dropped without extending). Logged in `editlog.jsonl`.

## CTA line (pick one; one per video)

1. **Scan listing:** "Get this Lexus IS350 scan: link in the description." (listing: illumaesthetic.com/products/lexus-is-xe30-3d-scan-facelift-2020, owner decides whether to show the URL)
2. **Scanning service:** "Want your car scanned? Link in the description."
3. **Engagement, neutral:** "Which car should we scan next? Tell us below."

Generic default in the EDL: **LINK IN THE DESCRIPTION** (works for 1 and 2 until the owner picks; swap the text for the chosen line).

## End-card text (G15 sub line; logo stays 700+ px)

1. Listing: **ILLUMAESTHETIC** / **THE SCAN IS IN THE DESCRIPTION**
2. Service: **ILLUMAESTHETIC** / **SCAN YOUR CAR: LINK BELOW**
3. Neutral: **ILLUMAESTHETIC** / **SUBSCRIBE FOR THE NEXT SCAN**

Keep it consistent with the CTA chosen (1 with 1, 2 with 2, 3 with 3). No URL on screen unless the owner asks.

## Optional pickup line (host records later; the video works without it)

PU7 (replaces the CON_G1 "HOW FAST?" row, as VO over CON_02 and CON_04): "So how fast can you scan a whole car? Thirty-two minutes from 'go', twenty without the crash. And now you have the car to design around." Host's own voice, no new numbers.

## For the owner

1. **CTA / end card:** scan listing or scanning service? Pick one pair above.
2. **"About a coffee break"** (CON_G2) is your framing and is not in the footage. Is it OK for 20 or 32 minutes? If not, the card keeps only the triangle count line.
3. **"Yeah, this thing's fast."** (CON_03) is praise for the scanner in the host's voice, with no comparison. Keep or drop?
4. **The 10-minute figure** ("10 minutes if I just did the exterior") is cut: it is ambiguous (with or without spraying) and appears with a brand line. Do you want it added? It would need a verified definition.
5. **32 on screen:** the rail and card use your "32 MIN". The only legible reading in frame is 32:53.18 (553 @16.14). Both agree if truncated; 555 says "30 minutes actual", which is cut.
6. The two crew members stay unnamed ("Caleb" is cut). The crew member in the polo appears behind the host in CON_01.
7. 555 front plate at 25.86 is blurred in CON_03.
