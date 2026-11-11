# Toyota GR86 / Subaru BRZ (gen 2) - v3 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v3.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC. Scan-only, so criteria 3 and 6 don't apply.

v2 user feedback addressed:
1. The logo is bigger: an 860 px wide card, up from the small v2 logo.
2. The hood-open composite no longer cuts away the windshield. tools/hood_trim.py trims the hood at the measured cowl gap.
3. The trunk-open scan is used. The lid is masked against both open-lid states (tools/lid_mask.py), and e_rear shows TRUNK OPEN cargo.
4. The rear lights are exploded out of the rear bumper. The reverse light and licence-plate light scans are ICP-registered (tools/register_part.py), and f_lights lifts each out of the tipped bumper with a label.
5. The side-mirror-removed scan is used: d_mirror flies the right mirror off to show the scanned mount.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Same opener as v2: the whole car with motion from frame 0. The first part move is the hood at 7.4 s. |
| 2 | Beat sync | 5 | The cut frames are identical to v2 (f148, 221, 442, 515, 809, 956) and the audio is the same. v2 measured +2 to -13 ms on decoded audio. The v3 cutcheck lists the same 6 cuts. Its onset at 515 (-74 ms) locks to a later transient, the known checker issue; by the first half-rise after the dip it is -7 ms. f1103 is fade-to-logo by design, so it has no spike. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | Every shot passed the luma check. The c_front f58-64 slope is the bumper tipping away onto black, not a lighting dropout (checked on a sheet). The windshield is intact. The tail lamps survive in comp_explode3 (drop-islands 150, not 1500). The plate is kept as scanned (the IS300-only rule). The plate lamp is small and sits at the frame edge in f_lights. |
| 5 | Story | 4 | Front to side to rear on the car's right, each section once. Front: hood, then front bumper. Side: mirror. Rear: lid and cargo, then rear bumper and crash beam, then the lights. Then reassembly, a fade, and the logo. The ive director flags b_headlight vs d_mirror as the same view (silhouette iou 0.78), but they are different subjects (headlight close-up vs door mount), so it is a false positive. |
| 7 | Text | 4 | 6 factual labels, one at a time, on scan shots only, with no numbers. Coverage under each label box was measured at <= 14% scan pixels. The f_lights labels moved to y 0.33 because at y 0.08 they sat on the crash beam. |
| 8 | Ending | 5 | All parts fly home rear to front, the hood lands on the 34.32 return, then a 1.95 s fade and a full-width logo from the 36.766 kick. |
| 9 | Technical | 5 | Spec above, one Blender at a time, persistent data off. |

## Remaining weak spots for the next agent
- The plate lamp is a small part. It reads only as a silver block top-right in f_lights, and a closer push would sell it better.
- The rear bumper pokes the bottom-right of the e_rear end frame.
- There is a small notch at the right quarter edge of the lid.

---
# Toyota GR86 / Subaru BRZ (gen 2) - v2 self-review (training/rubric.md)

Output: `/home/user/media/work/gr86/out/toyota_gr86_v2.mp4` (not in git). 1080x1920, 30 fps, 1177 frames / 39.233 s,
h264 yuv420p + AAC, moov first. Scan-only reel (no IRL footage), so criteria 3 and 6 don't apply.

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | Whole car fully in frame from frame 0, ~20 deg arc + push from the first frame. The v1 0.8 m dolly read as static (ive director: 4.8 s dead), so it was replaced. It is a camera move, not a transformation; the first part move is the hood at 7.4 s. |
| 2 | Beat sync | 5 | Measured on the delivered file's decoded audio (broadband 1 ms RMS, half-rise of the kick): offsets +2, -13, -7, +10, -6, +14 ms (cuts f148, 221, 515, 736, 956, 1103). Target is +-16.7 ms. The accents.py grid sits ~30 ms after the kicks, so every cut moved 1 frame earlier than the grid. |
| 3 | 1:1 match | n/a | Scan only. |
| 4 | Scan quality | 4 | The scanned licence plate is kept as scanned. The user rule in lessons.md allows plate flattening only on the IS300. tools/deplate.py was run, then reverted; g_rear and s_stack were re-rendered from the original scans. No light dropouts: every shot luma-checked (tools/lumacheck.py), no steps > 4. The comp_explode cowl area still shows the scan's dark gaps in the bay at the d_front push-in. Those are real data, not fixed. |
| 5 | Story | 4 | Order is driven by the scan features (direction.md): whole car -> front detail -> front section (hood off, bay, FRONT BUMPER REMOVED structure) -> rear section (REAR BUMPER REMOVED, crash beam push-in) -> top stack -> reassembly -> logo. Each section plays once; no repeated orbits or reused shots; no trunk shot (closed-trunk scan only). |
| 6 | Grade | n/a | No IRL. |
| 7 | Text | 4 | 3 factual labels on scan shots only, each on black above the car: FRONT BUMPER REMOVED / HOOD REMOVED · STATE SCAN, REAR BUMPER REMOVED / STATE SCAN, REAR CRASH BEAM. No numbers. The rubric allows <= 2 items, but the user's v2 brief asked for the bumper-removed data to be labelled, so there are 3 (one at a time). |
| 8 | Ending | 4 | Parts land home at 34.35 s, then a 2 s fade to black starting 0.45 s later (ive director had flagged a 2.4 s dead hold), then a small logo from the 36.766 kick to the end of the audio. |
| 9 | Technical | 5 | Spec above. Frame-diff spikes at every cut (29-78 vs median 0.9), none at the fade->logo, which is a fade by design. No duplicate frames at cuts. |

## Remaining weak spots for the next agent
- The opener's first part transform only comes at 7.4 s. A part move inside 1.5 s would score a 5 hook.
- The ive director still flags f_reassemble's fade as "dead frames": the detector counts a fade as stillness.
- s3_wheel (b_headlight) is a 2.4 s v1 shot reused from 2.4 s; it is the only v1 render left apart from the s7 tail.
