# Subaru WRX VB scan reel v4: self-review (training/rubric.md)

Output: `/home/user/media/work/wrx/out/subaru_wrx_vb_v4.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p + AAC, 33.3 s (999 frames). v3: `review_v3.md`, `project_v3.yaml`, `overlay_v3.json`.

The v3 feedback this version addresses (feedback.jsonl):
- **Rear trunk cut wrong:** v3 cut the lid on a 15 mm grid and kept only the top skin. The lid's rear face stayed on the car and the edges were stair-stepped. `tools/seg_v4.py` seeds the lid from the 'VB Trunk' open-lid capture rotated closed about the fitted hinge, mirrors it, then smooths it on the mesh (majority passes, opening, hole fill, largest component). The lid now has its rear face and a clean edge. `No Trunk` is the left rear quarter only, so it can't define the lid.
- **Front bumper artifacts:** v3 removed car skin by point distance, which speckled the hood edge and headlights and left double skins (mottling). v4 cuts the bumper region on the mesh as one smooth area. The fill comes from Front Removed All / Bumpers Removed only where it is more than 6 mm from kept skin, and small islands are dropped (`tools/build_v4.py`).
- **Teardown order:** the whole bumper (shell + grille + garnish + plate) comes off first on the drop. Then the grille pulls forward, the garnish drops, and the shell flips. In the reassembly the grille and garnish rejoin the shell in the air before the assembly locks on.

What was checked:
- Luma scan of all four finals. The largest steps are 4.1 (front), 5.3 (side), 2.3 (rear) and 1.8 (reassemble). There are no dropouts.
- Contact sheets `chk/v4f_*.jpg`, plus close-ups `chk/v4r40.jpg` (open trunk) and `chk/v4f60.jpg` (front parts apart).
- Frames around every cut and label: `chk/v4cut/cuts.jpg`, `labels.jpg`.
- `tools/cutcheck.py` on the delivered file.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Moving whole car from frame 1. |
| 2 | Beat sync | 5 | Cut minus onset: +7.0, +1.7 (drop), +2.3, +6.0, +9.0 ms. Detections at 14.13–14.27 s are motion inside the side shot, not cuts. |
| 3 | 1:1 match | n/a | Scan-only reel. |
| 4 | Scan quality | 4 | Hood, headlights and fenders are clean, with no mottling. The exposed front structure is rough because the bumper-off scan is rough. There is a small dark sliver at the right tail-light edge of the trunk opening. |
| 5 | Story | 5 | The bumper comes off as one, then comes apart. Front → side → rear → reassembly. |
| 6 | Grade | 5 | One house look. |
| 7 | Text | 3 | Five labels, all over scan shots, no numbers. That is more than the rubric's ≤2; it follows the part-by-part teardown. |
| 8 | Ending | 4 | Fade, then the small logo on the 30.00 s hit. |
| 9 | Technical | 5 | 999 frames. `src_fps = 30N/(slot+4)` from the actual counts (113/83/103/62). |

## Things the reviewer may push on
- The roughness of the exposed front structure is in the bumper-off scan itself. Only a cleaner scan pass would fix it.
- The dark sliver at the right edge of the trunk opening.
- Five labels.

## For the next agent
- Segment parts on the car mesh (smoothing plus island absorption), never by point distance to part scans. Fill holes from state scans only where they are more than 6 mm from kept skin, or you get double-skin mottling.
- Check what a state scan actually covers before using it as a "panel off" state. `No Trunk` is one quarter.
