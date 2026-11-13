# Mazda Miata NA scan reel v5 — self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_na_v5.mp4`. Specs: 1080x1920, 30 fps, 20.57 s (617 frames), H.264 + AAC, faststart.
v5 = reviewer on v4: "make the car pink, make the whole thing faster, edit it so the music starts at the beginning". Earlier: review_v4.md, review_v3.md (below).

**Pink.** The scan clips are graded with per-channel curves: black stays black, highlights stay bright, and the mid-tones are hot pink. Nothing was re-rendered. The listing page is the real site, so it keeps its grey cover photo, and the 1:1 cut now changes colour (pink car → grey photo) while keeping the framing.

**Faster.** The same renders are now played faster:

| Shot | Speed | Length |
|---|---|---|
| s1 | 4x | 1.27 s |
| s2, s5, s7 | 2x | 2.57 s each |
| s3_hood, s4b_side | 2x | 1.3 s each |
| s3 (two labels) | 1.35x | 3.87 s |

Cuts come every 4 track beats. The trunk cut lands on the track's first section change (12.87 s). Reel 32.1 → 20.57 s.

**Music from the beginning.** The track plays from its first note at frame 0 (seek 0.70 s). Measured on the decoded picture and audio, all 7 cuts are within −9..+10 ms of an onset.

Scores vs v3:
- Hook 5: the bumper comes off at 1.3 s.
- Beat sync 5.
- Grade 4: pink was requested, but it's a post grade, not a material, so the reflections stay neutral.
- 1:1 match 3: the framing matches, the colour doesn't.
- Text 4: labels are about 1.7–2 s each, still readable.
- Everything else as in v3.

Known: the s7 cover-camera hold is 0.3 s before the 1:1 cut, and s3 has a 3-frame settle before its cut.

---

# Mazda Miata NA scan reel v3 — self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_na_v3.mp4`. Specs: 1080x1920, 30 fps, 36.00 s (1080 frames), H.264 yuv420p + AAC, faststart.
Earlier reviews: review_v1.md, review_v2.md (and project_v2.yaml, timing_v2.json, overlay_v2.json, cta_v2.json).

v3 answers the reviewer:
- "the zoom into the trunk is unnecessary": the s6_trunk_well shot was cut.
- "the front crash beam is partially clipped off": s3_front_removed was re-framed wider and rebuilt on the comp_explode3 base. The base takes the whole front zone from the Front End Bumper Off capture, so the beam is complete.
- "the final ending shot … a 1:1 transition into the cover photo before zooming out": s7 ends on the cover-photo camera, solved from the photo's silhouette, then hard-cuts into the mobile listing at the same framing.
- "re-edit to this music": re-cut on the uploaded track at 186.73 BPM, with cuts on the phrase downbeats.

Order: whole car (s1) → FRONT: the bumper comes off and turns to show its scanned inside (s2) → bumper-removed front end with the complete crash beam, labelled (s3) → hood opens (s3_hood) → SIDE dolly (s4b) → REAR: trunk closed → half → open (s5) → TOP: parts go home and the camera settles on the cover-photo view (s7) → 1:1 cut into the cover photo on the listing → pull back to the phone, MIATA NA SCAN NOW AVAILABLE, logo, URL.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | The whole car is in frame and moving from frame 1. The first transformation (the bumper) lands on the n18 phrase downbeat at 5.17 s. |
| 2 | Beat sync | 5 | Measured on the delivered file's decoded picture and audio: all 7 cuts are within −15..+11 ms of an onset (≤ ½ frame). See the fix below for the hidden +1 frame. |
| 3 | 1:1 match | 4 | s7 last frame vs CTA frame 0: the car silhouettes coincide to a few px (cover solve IoU 0.976). Two visible differences: the photo has a grey backdrop and page UI, and the photo shows the full-car scan's own bumper (round fog lamps) where the reel's car wears the separately scanned removable bumper. |
| 4 | Scan quality | 4 | Real bumper-off capture is the hero, the crash beam is complete, the open lids are the registered open-state scans, and the plate is blanked. |
| 5 | Story | 4 | Front → side → rear → top, one block each. The trunk zoom was removed. The ending now pays off on the actual product photo. |
| 6 | Grade | 5 | Silver on black, AgX. |
| 7 | Text | 4 | Same three factual label cards, on black, never over the car, with no numbers. |
| 8 | Ending | 5 | Parts go home, the camera settles on the cover view, then a hard 1:1 cut into the listing and the pull back. The CTA holds about 2 s for the URL as the music fades. |
| 9 | Technical | 5 | Every rendered frame was luma-checked: no unexpected dark frames. s7's tail is lower luma only because the car is small at the cover framing. First, mid and last frames of every shot checked: nothing clipped. |

## Found while measuring v3 (lesson for the next agent)
- `ive assemble` builds a cut as a 1-frame xfade, so the incoming shot first appears one frame after the summed durations. Measured on the decoded picture, every cut was +33 ms late.
- Fix: shorten the first clip by one frame and lengthen the last clip by one frame. Then all 7 cuts showed on their planned frames.
- Earlier cut-timing numbers (v2) were computed from planned frames, so they were likely also one frame late.

## ive director (v3)
- Repeats s3_hood~s4b_side and s4b_side~s5_trunk: the same false positives as in v2 (different subjects). Kept.
- "Dead" 1.9 s in s3_front_removed: a slow 8 cm creep while the CRASH BEAM label reads. Only 2 frames are fully static.
- CTA 2.2 s hold: reading time for the URL.

## Known weaknesses
- The bumper difference against the cover photo at the 1:1 cut (see #3). The cover was rendered from the full-car scan.
- s2_bumper settles about 0.2 s before its cut.
- The listing's only dataset is "Exterior Only". The bumper-off, engine-bay and trunk state scans in the reel are not a listed dataset.
