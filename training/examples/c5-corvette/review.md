# C5 Corvette scan reel v1 (Temerario style): agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_corvette_v1.mp4`: 1080x1920, 30 fps, yuv420p, AAC, 39.37 s (music fades to silence by 39.5 s).
Scan only, no text, no IRL (brief). Music: the parent session's generated track only.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | fades up from black (1.2 s) into a slow, low front 3/4 turntable that moves from frame 1, matching the Temerario reference's pace; there is no *transformation* until the hood lifts at ~17.7 s, so it is calm rather than a hook |
| 2 | Beat sync | 5 | all 9 cuts land on round(beat*30) (frames 121, 282, 415, 465, 515, 665, 799, 915, 1065), confirmed by frame-diff peaks; panel motion is keyed to accents too (explode starts on 26.621, targa locks + clean-car snap on the b61 kick 34.402, logo on the b63 hit 35.513) |
| 3 | 1:1 match | n/a | scan-only reel by brief (no IRL→scan cut). The Dropbox IRL dump is noted in clips.md for a 1:1 version |
| 4 | Scan quality | 3 | full car clean apart from small ground scraps under the sills in s1/s2; the exploded shots necessarily show the removed-state composite (exposed structure, ragged trim lines where parts meet), and s9 now swaps to the clean car on the kick once the panels are home; the hood-open engine bay is the raw captured state |
| 5 | Story | 4 | turntables → wheel + tail-lamp close-ups → hood opens on the fitted hinge → top-down spin → panels separate and stack above the car → return → clean car → logo. It follows the Temerario order; there are fewer separating panels (5) than in the reference because only 5 part scans register |
| 6 | Grade | 5 | one look throughout (house satin silver, AgX, exposure -0.5, bg RGB ~1); logo card bg (7,7,9) is close to the render black |
| 7 | Text | 5 | none, by brief (no invented numbers) |
| 8 | Ending | 5 | logo cut on the biggest hit (35.513), fades out with the music (1.4 s audio fade, video fade 3.0-3.9 s) |
| 9 | Technical | 5 | 1080x1920 30 fps yuv420p AAC; no black/dup frames at cuts (the only dark frames are the intentional fade-up, the 0.25 s logo fade-in and the end fade) |

## How it was built (for the next agent)
- Base car = 2023 export (the 2026 export is the same capture, 0.55 mm away, plus scanned ground, so it was used only for levelling).
- Part registration: same-frame parts checked with tools/regcheck.py (2-5 mm median); own-frame scans used
  tools/globalreg.py (FPFH+RANSAC+ICP; hood open 2.7 mm) and tools/fitpanel.py (seeded flip/yaw ICP; targa 1.6 mm,
  since plain FPFH slid the symmetric roof panel down the windscreen). Every part was rendered red over the silver car before use.
- Hood: hinge fitted to the captured hood-open state (tools/hinge.py, 3.8 mm median, 46 deg). The closed hood = the car's own hood
  skin + the open-hood scan's underside (tools/hoodcombo.py), because the rotated open-hood scan alone looked patchy.
- Exploded base = full car trimmed under the parts + "removed" state scans where they add geometry (tools/composite.py).

## Known issues / v2 ideas
- s9 snap: the composite → clean-car swap is a visible change (by design); in the delivered file it lands at 34.33 s (frame 1030, one minterpolate blend frame at 1029), ~2 frames ahead of the 34.402 kick. Set SWAP from the assembled timeline offset, not the shot-local time. A cleaner composite (trim the state
  scans to the part footprints) would let the panels return onto a near-clean body.
- Crop the ground scraps under the sills (tighter `--drop-islands`, or a z-crop just above the tyre contact patch except at the wheels).
- More separating panels would sell the explode better (side skirt, door card, and light scans exist but are in their own frames;
  register them with tools/fitpanel.py).
- The hook could open on the hood lift or a part sliding off instead of a plain turntable.
- 1:1 version: solve a camera on a DJI clip from the C5 dump against car.blend and cut on the 9.393 drop.
