# Subaru WRX VB scan reel v3: self-review (training/rubric.md)

Output: `/home/user/media/work/wrx/out/subaru_wrx_vb_v3.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p + AAC, 33.3 s (999 frames). v2: `review_v2.md`, `project_v2.yaml`, `overlay_v2.json`.

The v2 feedback this version addresses (feedback.jsonl):
- **Music:** cut to the user's track, Roni Size – The Streets, from track 146.80 s. The breakdown plays under the opener and the drop lands on the front teardown.
- **The front bumper comes apart further:** the grille, lower garnish and bumper shell are separate scans, so they come off one at a time. The shell flips to show its scanned inner face. The shot holds on FRONT BUMPER REMOVED.
- **Trunk open:** the lid is built from the 'VB Trunk' open-lid capture and rotated back about a refitted hinge (median 6.7 mm, 64 % of points within 10 mm). It swings up to the captured open pose and then the rear bumper comes off.
- **The ragged front bumper cut-out:** the part scans cover only about 50 % of the bumper skin on the car. `tools/build_v3.py` also removes car skin that the bumper-off state scans see behind (45k triangles). The plate box is protected.

What was checked:
- Per-frame mean-luma scan of all four new finals. The largest steps are 7.9 (front, a part flying out) and 5.3 (side). There are no dropouts.
- Contact sheets of all four finals: `chk/v3f_*.jpg`.
- The reassembly base swap (b3 → full car) at f41/42 has a mean diff of 2.1 and is invisible.
- Frames around every cut and every label: `chk/v3cut/cuts.jpg`, `labels.jpg`.
- `tools/cutcheck.py` on the delivered file.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Moving whole car from frame 1. The breakdown is quiet until 4.1 s. |
| 2 | Beat sync | 5 | Cut minus onset on the decoded delivered audio: +7.0, +1.7 (drop), +2.3, +6.0, +9.0 ms. The logo comes in on the 30.00 s hit after the fade. The first assembly was +36/+39/+76 ms late (see below) and was re-cut. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 4 | No bumper slivers left at the front cut-out. Real scan gaps remain in the front structure and the trunk floor, so the rear camera stays low. On the fast garnish fly-out, minterpolate smears the in-between frames (about 3 frames). |
| 5 | Story | 5 | Front → side → rear → reassembly, one continuous sequence each. Nothing opens without a state scan: the trunk now has one. |
| 6 | Grade | 5 | One house look; the logo is on the same black. |
| 7 | Text | 3 | Six labels, all over scan shots, no numbers, one per part. That is more than the rubric's ≤2. It was chosen because the user asked for the bumper to come apart part by part. Each label is up for 1.2–1.8 s. |
| 8 | Ending | 4 | The grille locks, the shot fades, and the small logo lands on the 30.00 s hit. The music fades with it. |
| 9 | Technical | 5 | Spec-correct, 999 frames, per-clip `src_fps = 30N/(slot+4)` from the actual frame counts (seconds·15 + 1). |

## Things the reviewer may push on
- Six labels may be too many for the house style. The sub-lines could go and leave only the part names.
- The garnish fly-out smears in the interpolated frames. A slower key, or rendering that one shot at 30 fps, would fix it.
- The opener and scoop are reused from v2/v1, sped up 1.25x and 1.3x.

## For the next agent
- Don't trust `ive beats`' period on breakbeat tracks. This one is 176.0 BPM (0.34095 s), and the 0.3418 s grid drifted 76 ms by 26 s. Fit the period across the whole section, then put each cut on the measured broadband hit (the `cutcheck.py` onset), not on a rigid grid.
- Bumper part scans don't cover the whole bumper skin on the car. Use the bumper-off state scans to clear what is behind (`build_v3.py` step 2).
