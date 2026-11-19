# Review: "Day in the life of an average track guy" (ditl-time-attack-larper), v2 review cut

Cut: `/home/user/media/ditl-time-attack-larper/cuts/track-guy_v2.mp4` (media, not committed). Numbers come from
`tools/inspect_cut.py`, ffmpeg `ebur128`, and a Blender pass over every car shot. Measured 2026-11-19.

## 1. Layout
| Check | Result |
|---|---|
| Canvas | 1080x1920, 30 fps, 1086 frames (expected 1086), H.264 High yuv420p, AAC LC 48 kHz stereo, faststart (moov first) |
| Picture | 1080x1080 at y=420-1499 on every frame. Row 419 mean luma max 1.3 and row 1500 mean max 1.5 (black), so the picture edges are exact |
| Bands | Max luma outside the title box 16 (encoder ringing beside the picture edge; the bands are black, 0-16) |
| Title | "Day in the life of an / average track guy", bbox x 290-790, y 196-317: inside the 80 px margins |

## 2. Cuts
- **Cut diffs:** all 14 hard cuts land on the planned frames (66, 114, 161, 256, 304, 352, 399, 471, 519, 567, 729, 777, 825, 906). Their picture diffs are 28.5-138.5 (mean abs luma), against an in-shot 99th percentile of 31.3.
- **Lowest cut:** the weakest cut is 2→3 (28.5). Both shots are the same phone in the same hand, so this is expected.
- **No duplicated frames:** no two consecutive frames are identical anywhere. Static render holds at shot ends were removed with a subtle handheld drift in the assembler (two-frequency crop of at most 7 px).
  - Two near-static spots remain: the end of shot 2 (phone on black, mean diff 0.001-0.009) and the first two frames of shot 13 (mean diff 0.001).
- **No dark frames:** minimum picture mean luma is 15.4. The last frame mean is 47.9, then the hard cut to black.
- **"Flash" flags:** all of these are intended action, not glitches:
  - 139 and 151-157: the Confirm spam.
  - 226-227: both gloves land on the endplate.
  - 796: the phone drops away in shot 13.

## 3. Voice
| Line | Take edges (first / last 50 ms) | Ends before its cut |
|---|---|---|
| "Aero's working." (take 1 solo) | -74.9 / -89.6 dB | 6.3 frames (moved 4 frames earlier for this check; it was 2.4) |
| Exchange: "Do you actually race?" / "Next season." / "You said that last season." (take 1) | -90.6 / -87.7 dB | 12.3 frames |
| Sigh + "...next season." (take 2) | -63.8 / -88.5 dB | 14.4 frames before the cut to black |
No line starts or ends inside a phoneme, and every line ends more than 4 frames before its cut.

## 4. Sound
- **Loudness:** -14.0 LUFS integrated, true peak -3.9 dBFS (target below -1). A limiter runs before the two-pass linear loudnorm, so no SFX clip.
- **Engine:** the turbo-four plays only while the car is running: shots 6, 7, 8, 9, 10, 14, and the passing track cars in 14.
  - Removed for this check: the idle under shot 15 (parked; he revs with his mouth) and an overlap of shot 6's idle into shot 7.
  - None under 11 (parked, window down), 12 or 13 (car off). Shots 7 and 9 got their missing idle.
- **No music** (owner, 2026-11-19).

## 5. Product
- **TC wing:** the configurator export (`tc-1689`: lofted TC element, TC endplates, `tc-swan-typer` uprights, `swan` cradles, `base-fk8-sheet` bases, 1139.7 mm spacing). All 9 parts are present in all 11 car shots (4, 6-15). Each part's matrix relative to the car matches mounted shot 4 with a maximum deviation of 0.0.
- **Wheels:** 4 TE37-style rims (bronze) on every car.
- **Cart:** re-checked the live store on 2026-11-19. Title "[BACKORDER] TC Wing - Honda Civic Type R/Sport FK7/FK8", variant '[BACKORDER] 66.5"', SKU TCW-FK8-665, $1,200.00. The cart screen shows exactly this.
- **Branding:** no Epsilon branding anywhere; the store is generic.
- **No invented numbers:** the glove reads "PSI: ok", the weather says "one (1) cloud", and the lap timer runs at walking pace.

## 6. Rubric (training/rubric.md; written for scan reels, so the scan-specific rows are adapted)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | Alarm slap at frame 6, whip-pan by 0.5 s, the suit-and-helmet mirror reveal at 1.1 s |
| 2 | Beat sync | n/a (4 on pacing) | No music. Cuts follow SFX and gags, 1.5-6 s per shot, as on the approved WRX format |
| 3 | 1:1 match | n/a | No IRL-to-scan cut in this format |
| 4 | Model quality (was scan quality) | 3 | FK8 scan holes filled (2954 to 956 open edges), smooth shading, glass projected from the scan's own drawing. Lower bumper is still a little rough up close; no H badge in the scan |
| 5 | Story | 4 | Ready for track (suit, wing, trophies, timer) but never drives on one: ATTENDEE plaques, U-turn at the gate, "...next season." |
| 6 | Grade | 4 | One posterised game look on every shot (crunch, banding); interiors darker than exteriors |
| 7 | Text | 5 | Only diegetic screens and signs, with true listing data; the title band is the only overlay |
| 8 | Ending | 4 | Hard cut to black after the sigh line (series rule: no logo card) |
| 9 | Technical | 5 | 1080x1920, 30 fps, yuv420p, AAC, faststart, no black or identical frames at cuts |

## Open
- Whether review sheets and other media get committed: the parent asked the owner.
- The owner's notes on v2.
