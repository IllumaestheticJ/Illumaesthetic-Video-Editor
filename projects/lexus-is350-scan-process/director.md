# Director plan - Lexus IS350 scan-process reel, v3 revision

Stage 2 (director). This plan keeps the scene order from `direction.md` (front -> rear + reflector -> side/hero -> listing).
Every time below is on the measured grid: video beat n = 0.50004 n s, drop n6, last kick n54.
Total length: **27.57 s**, unchanged from v1. Music cut points: unchanged. The only change at the end is that the 0.5 s
dissolve at n46 becomes a hard cut.

Conventions used in this plan:
- Scan frame: nose at -Y, tail at +Y, Z up. All cameras sit on the +x side of the car.
- Canvas: 1080x1920. Wide IRL shots use a full-height 16:9 window of W = 1063 source px (1920-wide coordinates; 4K = x2),
  scaled to 1080 wide, so the window is ~1097 px tall. Above and below it is a blurred, darkened fill of the same frame.
- Scan renders at the matched cameras are full-bleed 9:16 on the same canvas: same focal length, sensor =
  35.6 x 1063/1920 = 19.71 mm, lens shift from the window offset (shift is a fraction of the WIDTH). The car stays
  1:1 inside the 16:9 band, and above and below it is real render (black).

## Shot table

| section | shot id | start-end (s, n) | focus | camera | part action (beat times) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| IRL front | `irl_walkout` | 0.000-2.967 (n0-6) | the real powdered car, whole front | FX30554 f193-264 (unchanged in/out; match frame f264 is last). Window W 1063, **x0 ≈ 385** (car spans x 500-1328, so ≥ 115 px margin each side). Mirrors and bumper corners must be fully in | - | hook: camera walks out of the shop onto the car. Lands on the drop | **re-crop** via tools/irl.py (canvas mode). No Blender |
| front | `scan_front` | 3.000-7.000 (n6-14) | **front fascia: mesh grille, headlights, corner vents** | **camW_A re-centred**: cam_A2 with crop x0 385, W 1063 (shift_x ≈ +0.006, essentially centred). Hold the 1:1, then `--move push --move-amount 0.15 --ease ease_in_out`. Camera goes from 5.6 m to ~4.8 m from the grille; mirror-to-mirror grows from ~78 % to ~92 % of the width. No orbit, no rise. Key light ~15 % lower than v1 (the v1 silver read hot) | - | the drop lands on the transformation. The push resolves the scanned grille mesh while the HUD counts 24,999,992. Front shown once | **re-render** (~63 frames) |
| IRL process | `irl_spray` | 7.000-8.001 (n14-16) | powder spray | unchanged | - | process: why the car is white | **reuse** |
| IRL process | `irl_scanner` | 8.001-9.501 (n16-19) | live scan on the scanner screen | unchanged | - | process: the scanner at work | **reuse** |
| IRL rear | `irl_rear_scan` | 9.501-13.001 (n19-26) | crew member scanning the rear bumper | FX30542 f1052-1135, last frame f1135. Window W 1063, digital pan x0 857 -> **0** over the last ~58 % (v1 was 760 -> 40). At x0 0 the plate, left lamp, exhaust and the scanner head are in. The car's far corner is cut off by the source frame itself | - | the 2nd transformation's setup: the real hand-held scan of the exact area we then show | **re-crop** |
| rear | `scan_rear` | 13.001-19.002 (n26-38) | **the rear reflector: out of its vent, lens face, then clip side** | Start **camW_B** = cam_B with crop x0 0, W 1063 (31.1 mm on a 19.71 mm sensor; editor computes the shift). The 1:1 lands on n26. `tools/path_render.py` to **camR_end**: azimuth same as cam_B (behind the +x rear quarter), **~1.0 m from the dropped reflector**, height ≈ part height + 0.15 m (looking ~10° down), lens 31 -> **~50 mm**. At the end, the vent pocket sits small in the top third and the part is centred at ~y 0.6, its long side ≥ 300 px. Path runs 0.08-0.95 of the shot, ease_in_out, so the camera never fully stops | `--explode "refl.blend:0.05,0.20,-0.25:0.10:0.33:z180:0.36:0.80"`: drops out mostly DOWN into the black below the bumper (not toward the lens, not over the body), 13.6-15.0 s. **One 180° turn** shows the clip side, 15.2-17.8 s (starts on phrase n30). Clip side held under the slow creep, 17.8-19.0 | one part + one state = one shot. The camera moves in on the part, and the turn exists to show the scanned back with its 3 mounting tabs (data verified on S2 f52). Labels from data only | **re-render** (~93 frames) |
| side + whole | `scan_xray` | 19.002-23.002 (n38-46) | **reflector seats, then the side and the whole car** | path_render from **camR_end** (identical to S2's last frame, x-ray look) to **camP_L** (unchanged listing pose: 80.1 mm, 9.25,-6.2,4.08). The path's azimuth goes the short way, so the camera travels forward along the +x side. ease_in_out, 4.0 s | `--explode "refl.blend:0.05,0.20,-0.25:r0.0:0.45:z180:r0.0:0.45"`: reverse, so the part starts at S2's end offset and turned 180°, then flies home and un-turns, 19.0-20.8 s. `--morph-to-clay 0.70,0.93` (same clay/bg values as v1). Last ~0.25 s is a still clay frame = WebZoom frame 0 | the side gets its one pass (while moving: the rear wheel is a weak, ragged capture). It ends on the whole car in exactly the listing pose | **re-render** (~63 frames) |
| listing | `website` | 23.002-27.57 (n46 -> last kick n54 + 0.6 fade) | IS350 listing, "SCAN DATA + 2026 BUMPER NOW AVAILABLE", logo, URL | WebZoom unchanged (startScale 1.245, zoomFrames 60) | - | CTA. **Hard cut** on n46, the strongest kick. Same car, same pixels (0.3 px), and the page UI appears around it | **reuse** `webzoom_is350.mp4` |

Transitions:
- n6 and n26: hard 1:1 cuts, as in v1.
- n14, n16, n19, n38: hard cuts. The n38 cut is the S2 -> S3 look change at the same pose.
- **n46: hard cut, replacing the 0.5 s dissolve.** S3's `dur` = 4.0 s (no overlap compensation needed any more).

HUD (`overlay.json`, re-render the ScanHUD overlay). At most 2 items on screen; never over IRL footage.
- Front: brackets 93-205 and counter 96-204, value 25,024,430 (displays 24,999,992). Unchanged.
- Rear brackets: 393-565.
- `REAR REFLECTOR / 408,984 TRIANGLES`: frames ~412-455 (13.7-15.2 s, while the part drops).
- `INSIDE + OUTSIDE / REFLECTOR SCANNED, BOTH SIDES`: frames ~458-565 (15.3-18.8 s, leaves before the n38 cut).
- Placement for both labels: on black beside the part, not on the part or the pocket. Read the new render first and
  pick the side with free black.
- No other text. "REFLECTOR REMOVED" is not added: the pocket is weak data and is not the subject.

## Cut list (from v1/v3)

| removed | why |
|---|---|
| S1's 20° orbit (all 60 frames) | it rotated the view toward the +x front 3/4. That showed the side a first time (S3 shows it again) and ended near the listing pose that closes the reel. Wasted rotation (user, all reels) |
| S2's second half-turn (the v1 `z360` = 2 x 180°) | the second 180° only returns to the lens face we already saw. One turn plus a hold shows both faces |
| S2 frames where the reflector dips past the bottom edge (v1 f36-44) | clipped part (rule A). The new end pose frames the part with margins |
| S3 0.5 s (4.5 -> 4.0 s) and the 0.5 s dissolve | the dissolve doubled the same view (director report: scan_xray ~ website, IoU 0.72). A 1:1 cut shows that pose once and changes the world on the kick |
| v1 crop windows 607.5 px at both matches | mirrors and bumper corners were clipped ("too cropped", director report) |

The repeated-view flag scan_xray ~ website stays on purpose, but now as a **1:1 cut** (the house device), not as overlapping
frames. Note this in the editlog when assembling.

## Hold list (> 0.75 s)

| shot | span | reason |
|---|---|---|
| scan_front | 3.0-~3.8 s (ease-in of the push) | the 1:1 must read as the same car before it moves. The counter starts here |
| scan_rear | 13.0-~13.6 s (1:1, path ease-in) | same reason for the 2nd match. The part starts dropping at 13.6 |
| scan_rear | 17.8-19.0 s (slow creep, part still) | read the clip side and its tabs plus the INSIDE + OUTSIDE label |
| website | ~26.5-27.57 s | URL fully in. Hold to the last kick (27.0) and the 0.6 s music fade. Do not extend |

## Render budget (15 fps, 75 % res, 12 spp, persistent data OFF for S2/S3: animated part)

Frame counts:
- N = 15·(dur + 3/30) + 1, then set `src_fps = (N-1)/(dur + 3/30)`. This avoids the minterpolate tail freeze.
- S1: **63** frames, static mesh. Persistent data may stay on.
- S2: **93** frames. One background job.
- S3: **63** frames. Queue it after S2, never in parallel.
- Before assembly: a first/middle/last contact sheet per shot, and a per-frame mean-luma scan of every render directory
  (lighting-dropout lesson).

Total ≈ 219 frames, against 218 in v1.

**Reused unchanged:**
- `irl/i2_spray.mp4`, `irl/i3_scanner.mp4`
- `out/webzoom_is350.mp4`
- music `is350_reel_d25.wav`
- camP_L and the clay/background morph values

Re-crop only (ffmpeg via tools/irl.py): `i1_open`, `i4_rear`.

Checks the editor must do before assembly:
- Onion of the new camW_A and camW_B renders against the widened IRL last frames: phaseCorrelate < 1 px within the 16:9 band.
- S2 at 25 % res / 4 spp, first/mid/last frames, before the final render. Confirm the part sits on black. If the rear
  tyre or underbody shows behind it, raise camR_end ~0.1 m and tilt down more.
- Look at the pocket at the final framing. If its black holes read as blotches, move it further to the top edge.
