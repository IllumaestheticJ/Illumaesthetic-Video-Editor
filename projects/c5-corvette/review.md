# C5 Corvette scan reel v2: agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/c5_corvette_v2.mp4`: 1080x1920, 30 fps, yuv420p, AAC, 39.37 s (1181 frames).
Scan only (brief); 6 title-only labels over scan shots. Music: the parent session's generated track only.
v1 (`c5_corvette_v1.mp4`) review is in git history (commit 7687b36). What changed is in `direction.md` §4 and `editlog.jsonl`.

## What changed from v1 (reviewer: "focus on the removed areas and where the useful data is" + parent V2 brief/addendum)
- Built around the four registered removed states only: front bumper removed, front bumper + hood removed,
  fender + bumper removed, rear bumper removed. The targa has no roof-off scan, so it never comes off. There are no trunk/door scans, so nothing else opens.
- One continuous sequence per section, travelling whole → front (bumper, then hood) → -X side (fender) → rear → whole. v1's
  turntables, top-down spin and all-parts-at-once explode are gone.
- Each removal holds on the exposed structure and moves in. A part spins only where its backside was scanned:
  the front bumper inside, the hood underside and the rear bumper inside. The fender only translates.
- The labels name the scan states, worded from the file names: FRONT BUMPER REMOVED / FRONT BUMPER - INSIDE / HOOD REMOVED /
  FENDER REMOVED / REAR BUMPER REMOVED / REAR BUMPER - INSIDE. They sit over black, below the car.
- Cuts on measured kick onsets, within ½ frame. v1 was 2-4 frames late.
- Clean car → small logo on the biggest hit, then fade.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole clean car moving from frame 1 (0.4 s fade-up). The front bumper starts sliding off at 1.2 s, so the first transformation comes in the first 2 s (v1: 17.7 s) |
| 2 | Beat sync | 5 | cuts at frames 123, 279, 508, 664, 909, 1065. Measured on the decoded output: +10, -9, -5, +25 (broadband; low-band kick onset 22.126-22.130 → +3..+7), +5 ms. Logo on 35.496. The clean-car swap blends over 1031-1032, on the 34.402 kick (frame 1032) |
| 3 | 1:1 match | n/a | scan-only by brief |
| 4 | Scan quality | 4 | every removed state is a registered capture (2.3-4.1 mm median to the car); the composite still shows ragged trim lines where state scans meet the car (most visible on the fender macro); the opening and the ending swap to the clean car |
| 5 | Story | 4 | one section at a time, each holding on its removed-state data, with the bumper/hood/rear-bumper backsides turned to camera; no section repeats. The front gets 12.8 s because it has two states (bumper, then hood + bay) |
| 6 | Grade | 5 | one look (house satin silver, AgX, exposure -0.5); per-frame luma has no dropouts (persistent data off for every moving shot). The steps are all smooth exposure-area changes |
| 7 | Text | 5 | six labels, each a file-backed scan-state name, over scan shots only, no numbers |
| 8 | Ending | 5 | clean car, 1.1 s settle + 0.75 s fade, small logo (300 px) on the biggest hit, gone by 38.6 s |
| 9 | Technical | 5 | 1080x1920 30 fps yuv420p AAC. First/middle/last frame of every shot checked: no accidental clipping. The bumper-inside and fender macros fill the frame on purpose. No plate characters (rear recess is empty) |

## Checks run (for the next agent)
- `projects/porsche-macan/tools/cutcheck.py` and a 40-150 Hz envelope printout on the decoded output.
  `tools/kickcut.py` with a wide window (±0.15 s) picked the *second* hit of a double kick at 17.0 and 30.3.
  Read the envelope around each cut instead of trusting one number.
- The swap frame was located by matching output frames to render frames f_0060/f_0061 (`speed: 0.960` on i2).
- `ive director` "repeated views" flags small centred cars on black (silhouette IoU) even front vs rear. Section/focus tags are in project.yaml.

## Known issues / v3 ideas
- Ragged composite trim lines (fender macro, rear structure): trim each state scan to its part's footprint before compositing.
- The opening wide is small in the 9:16 frame for its first second (car ~40 % of width) so the whole car reads with motion. A lower,
  closer start would fill more.
- 1:1 version: solve a camera on a DJI clip from the C5 dump (clips.md) and cut on the 9.309 drop.
