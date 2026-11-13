# Subaru WRX VB scan reel v5: self-review (training/rubric.md)

Output: `/home/user/media/work/wrx/out/subaru_wrx_vb_v5.mp4`. Specs: 1080x1920, 30 fps, h264 yuv420p + AAC, 36.0 s (1081 frames). v4: `review_v4.md`, `project_v4.yaml`, `overlay_v4.json`.

The v4 feedback this version addresses (feedback.jsonl):
- **List the flares and side skirt as they come off:** FRONT FLARE, DOOR FLARE, REAR FLARE, SIDE SKIRT appear as each part lifts (names from the scan files).
- **"Scanned separately" is redundant:** the sub-lines on FRONT GRILLE and LOWER GARNISH are gone.
- **Rear still had leftover bumper:** v4 removed the rear bumper by point distance to its part scan, and the tub fill from 'Rear Bumper Trunk Open' (bumper on) put bumper skin back. v5 cuts the bumper as a state difference on the car mesh against 'Rear Bumper Removed'. Rear fills must be more than 6 mm from kept and removed skin (`tools/seg_v5.py`, `build_v5.py`). The crash bar and structure now show.
- **Trunk not accurately cut:** on the VB the plate panel between the tail lights is part of the lid. v4 cut that panel in half and ran 50-80 mm onto the rear glass. v5 traces the deck shut lines on a band-passed top-view height map (guide points snapped to the groove) and takes the rear face from the trunk-open state difference.
- **Blend into the Illumaesthetic call to action:** the reassembly ends on the camera of the listing's 360 viewer (solved from the mobile screenshot, IoU 0.983). The last frame shrinks 1:1 onto the car on the phone, then title and URL, then the logo. No "graphify" file exists in the repo; this follows the mobile-CTA lessons in `knowledge/lessons.md`.

What was checked:
- Luma scan and contact sheets of the new finals (`chk/v5f_*.jpg`); close-ups `chk/v5r40.jpg`, `chk/v5r98.jpg`.
- Mask outlines against the scan's panel gaps: `chk/r5/poly3.png`, `m3_rear.png`, `m3_top.png`.
- Scan frame vs listing in alternating bands: `chk/r5/onion_n_0930.png`. Wheels, glass line, pillars and sill run continuously.
- Frames around every cut, label and the CTA: `chk/v5cut/tail_0945.jpg`, `chk/v4cut/labels2.jpg`.
- `tools/cutcheck.py` on the delivered file.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Moving whole car from frame 1. |
| 2 | Beat sync | 5 | Cut minus onset: +7.0, +1.7 (drop), +2.3, +6.0, +9.0, -0.7 ms (logo). The CTA starts on the 30.00 s hit as a continuous move, not a cut. |
| 3 | 1:1 match | 4 | Scan to listing: silhouette IoU 0.983, features line up in the band check. The viewer's 1.83 deg roll is eased in during the shrink. |
| 4 | Scan quality | 4 | Rear bumper fully off, lid on its real gaps. A ragged sliver remains on the lid's right edge by the tail light, and the exposed front structure is as rough as its scan. |
| 5 | Story | 5 | Front, side, rear, reassembly, listing, logo. |
| 6 | Grade | 5 | One house look; the scan is toned to the listing grey as it lands. |
| 7 | Text | 3 | Nine short labels, all over scan shots, no numbers; requested by the reviewer. The CTA shows the listing page as it is, including its price. |
| 8 | Ending | 5 | CTA into logo on the 32.73 s hit, music fades under the logo. |
| 9 | Technical | 5 | 1081 frames; `src_fps = 30N/(slot+4)` from actual counts. |

## Things the reviewer may push on
- The listing screenshot has the viewer's Top / Underside / Spin / Full screen buttons hidden, because Spin sat on the car's roof. Everything else on the page is as captured.
- The listing's price is visible on the phone.
- The front shot is reused from v4.
- The logo is still the small one (380 px).

## For the next agent
- Check which panel a badge or plate belongs to before cutting a lid: a lid seeded from the open-lid capture misses its rear face.
- A state scan used as fill can put a removed panel back. Reject fill within 6 mm of removed skin as well as kept skin.
- Shut lines show as dark grooves in gaussian(1.5 px) minus gaussian(5 px) of a 1.5 mm/px height map. Snap hand guides to the minimum and fit a robust cubic.
