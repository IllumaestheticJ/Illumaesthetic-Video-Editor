# Director plan v3 - Toyota MR2 Spyder scan-process reel (stage 2 of direction.md v3)

2026-11-13. Keeps direction.md's scene order unchanged. Scan frame: Top Down frame, +Y = nose, +X = car right, Z up, metres.
Camera keys are given as location / look-at and as spherical keys (az in degrees from +X toward +Y, el, dist, target) in the
form `projects/toyota-mr2-spyder/tools/shot3.py` takes; `lens` is on a 36 mm-wide sensor, sensor fit horizontal, 1080x1920.
`ive director` was not run: the only assembled cut is v2, which this plan replaces. Run it on the v3 project.yaml after
assembly (expected false positives listed at the end).

## Shot table (30 fps, frames from the grid t_video = (n - 21) x 0.53535 s; music.start 11.757 s before measuring)

| section | shot | frames (beats) | focus | camera | part action | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| hardtop piece | irl_wide | 0-32 (n21-23) | crew with the scanner walking to the piece, whole car | DJI_0030 from 28.50 s, native portrait | - | only real view of the whole car with the piece on; motion from frame 1 | new IRL cut, 32 frames |
| hardtop piece | irl_screen | 32-64 (n23-25) | scanner screen showing the live scan | DJI_0030 from 44.50 s | - | the scan being made | new IRL cut, 32 frames |
| hardtop piece | irl_rear | 64-128 (n25-29) | scanner on the piece, pull-back to full rear | existing irlB_0030_1293-1343.mp4 (ends on 56.0 s = camB) | - | sets up the 1:1 | **reuse**, 64 frames |
| hardtop piece | **sP** scan_piece | 128-257 (n29-37) | the printed piece seated on hoop + deck | 1:1 on camB, crane up and in (spec below) | none, piece at home | the transformation, on the drop, into the shoot-day scan; move ends with the piece filling the frame | **new**, 68 frames @15 |
| hardtop piece | irl_over | 257-321 (n37-41) | scanner sweeping over the piece | DJI_0030 from 47.50 s | - | same subject and angle as sP's last frame, now real | new IRL cut, 64 frames |
| hardtop piece | irl_lift | 321-385 (n41-45) | two crew lifting the piece off | existing irlH_FX30636_20.9_wide.mp4, in 0 | - | the physical removal | **reuse**, first 64 frames |
| hardtop piece | **sL** scan_off | 385-450 (n45-49) | the piece clear of the car; hoop + deck it sat on | rear-right 3/4, low (spec below) | piece rises 0.08 -> 0.45 m, translate only | continues the real lift across the cut on the strongest kick; shows the seat | **new**, 36 frames @15 |
| hardtop piece | irl_down | 450-514 (n49-53) | piece set on the floor, printed underside | FX30636 from 27.5 s, LUT + 3:4 window on blurred fill as irlH | - | ends the removal; the underside exists only here | new IRL cut, 64 frames |
| whole car | **sH** scan_on | 514-658 (n53-62) | full hardtop landing, then the whole car | high rear-right orbit + pull-out to the listing pose (spec below) | ht_full descends 0.60 m, home at frame 578 (n57) | the second hardtop state; the reel's one whole-car wide; hands over to the listing | **new**, 75 frames @15 + 27 clay frames |
| end | website | 643-738 (dissolve 643-658, complete on n62) | listing, title, logo, URL | existing webzoom_mr2_v2.mp4 (95 frames) | - | end card, ends with the music | **reuse** |

Clip frame counts for a concat assemble: 32, 32, 64, 129, 64, 64, 65, 64, 144, then web 95 overlapping the last 15 of sH.
Total 738 frames = 24.60 s. Measure every cut on the decoded audio of the delivered file and move it to the onset
(lessons: n29 read about +58 ms from the grid, n45 / n62 about -15 ms; n23 has no kick on the grid). When a cut moves,
change the clip's `in` (IRL) or `src_fps` (renders), never `speed`. irl_rear: move `in` only, it must end on frame 1343.

## Render specs

Scene files: `/home/user/media/work/mr2/scan/topdown.blend`, `ht_rear.blend`, `ht_full.blend`. All three shots: silver on
black, 1080x1920 at 75 %, 12 spp, 15 fps. Light rig pinned to the topdown bbox in all three. Render 3 source frames past the
cut and set `src_fps = (N - 1) / (dur + 0.1)`.

### sP - scan_piece (129 output frames, 4.30 s) - camera only, persistent data may stay on
Objects: topdown + ht_rear (at home, off 0,0,0).

| key | output frame | location | look-at | spherical | lens | roll |
|---|---|---|---|---|---|---|
| K0 | 0 | exactly `match/camB.json` (-0.309, -3.092, 1.338), solved rotation matrix | (-0.328, -0.418, 1.043) | az -89.6, el 6.3, dist 2.69 | 22 mm on 20.25 mm sensor = 39.1 mm on 36 | as solved (about 11.6 deg) |
| K1 | 64 (n33) | 72 % of the way K0 -> K2 | - | - | 39.1 | about 3 deg |
| K2 | 129 | (0.449, -2.150, 2.251) | (0.0, -0.45, 0.95) | az -75.2, el 36.5, dist 2.19 | 39.1 | 0 |

Interpolate position along the spherical path and slerp the rotation from the solved matrix to the K2 look-at; zero
velocity only at K0, no stop at K1, ease out into K2. shot3.py has no roll: add a roll key (nissan-frontier shot.py has
one) or bake the keys from the two matrices. Frame 1 must equal the camB render: onion it over DJI_0030 at 56.0 s at
full resolution and check the piece's window opening, tail lamps and plate recess (the wing is in no scan and will vanish).
At K2 the piece is 1.42 m wide in a 1.96 m-wide view = 72 % of the width; hoop, both deck legs and the window opening in frame.

### sL - scan_off (65 output frames, 2.17 s) - persistent data OFF
Objects: topdown + ht_rear.

| key | output frame | location | look-at | spherical | lens |
|---|---|---|---|---|---|
| K0 | 0 | (1.657, -3.321, 1.749) | (0.0, -0.45, 1.20) | az -60, el 9.4, dist 3.36 | 50 |
| K1 | 65 | (1.554, -3.141, 1.714) | same | az -60, el 9.4, dist 3.15 | 50 |

Camera: linear push, moving from frame 1. ht_rear offset (x, y, z) m: (0, 0, 0.08) at frame 0 (it is already in the
crew's hands at the cut), (0, 0, 0.45) at frame 40 ease-out, (0, 0, 0.50) at frame 65 linear. Translate only. No spin, no
tilt: the underside was not scanned. Camera z 1.75 stays above the piece's top (1.16 + 0.50 = 1.66) so only the scanned
side faces the lens, and low enough that the piece rises against black, not across the body. View width 2.4 m: piece
about 78 % of the width.
Gate before the full run: render frames 0, 32, 65 at 30 % and ht_rear alone from this camera. If its edges are ragged or
it shows holes, do the fallback: render sL with topdown only (piece gone, same camera, same push), no floating part - the
state changes across irl_lift. Label unchanged.

### sH - scan_on (144 output frames, 4.80 s) - persistent data OFF
Objects: topdown + ht_full. Target T = (-0.124, 0.091, 0.489) throughout, lens 70.78.

| key | output frame | location | spherical |
|---|---|---|---|
| K0 | 0 | (1.339, -5.367, 3.494) | az -75, el 28, dist 6.40 |
| K1 | 114 | exactly `match/cam_listing_v.json` (6.365, -4.622, 3.003), solved matrix | az -36.0, el 17.4, dist 8.405 |
| hold | 114-144 | K1 | - |

Camera: moving from frame 1, ease out to rest exactly on K1 at frame 114. ht_full offset: (0, 0, 0.60) at frame 0 ->
(0, 0, 0) at frame 64 (n57, video frame 578), ease in-out; it is already descending in frame 0. Whole car inside the frame
on every frame: at K0 the car reads about 77 % of the width with the raised hardtop fully in; at K1 it matches the listing.
Ending: silver -> listing grey between output frames 96 and 126, then rest, dissolve 129-144. `--morph-to-clay` does not
change the background with the silver look: render output frames 96-144 a second time in clay (clay 0.075, 0.078, 0.075,
background 0.012, 0.015, 0.012 as in v2's sX) and crossfade in post, or grade with na-miata-grimace `tools/greygrade.py`.
Check the last frame against WebZoom frame 0 (redo match/check_listing.jpg): body, wheels and now the roof must overlay.
If the topdown + ht_full seam shows at the header or deck in the K1 frame, render frames 114-144 from fullcar.blend
instead (same camera) and check for a luma or geometry step at the swap.

## HUD (ScanHUD labels, `shadow: true`, only over scan shots, no brackets, no triangle counts)

| shot | from | duration | title | sub | position |
|---|---|---|---|---|---|
| sP | 134 | 112 (off at 246) | PRINTED HARDTOP | REVISION 1 TEST-FIT SCAN | x 0.08, y 0.10 (black above the car in both K0 and K2) |
| sL | 389 | 56 (off at 445) | HARDTOP OFF | ROLL HOOP + REAR DECK | x 0.08, y 0.84 (the piece rises through the top band) |
| sH | 582 | 44 (off at 626) | HARDTOP ON | FULL CAR SCAN | x 0.08, y 0.10 |

Wording sources: Drive `Print Evaluation/Mr2 hardtop revision 1.stl`; the test fit is in the footage; hoop and deck are
visible in topdown renders; `Full Car.stl`. Before finalising, look at sL's frames and confirm the hoop is what shows under
the piece. Sample each label box at 4 frames across its window for scan pixels underneath and move it if any.
durationInFrames 738. concat_assemble composites `overlays:` itself - no second HUD pass.

## Cut list (from v2)

| removed | why |
|---|---|
| irl_scan_front + scan_front (sA3), cut A | hood mismatch in the centre of the frame; piece still on the car after the lift; no shoot-day scan of the front (direction.md) |
| scan_rear (sB) | replaced by sP: sB lacked the hardtop piece that is in the footage frame |
| scan_lid (sC2) | 2024 lid state, off-story; the Z spin goes with it |
| scan_xray (sX) | nothing to reassemble; roof mismatch into the listing |
| both triangle-count labels, "ENGINE LID" label, brackets | banned / shots gone |
| irlH frames 64-96 | carry-away is now told by irl_down |

## Hold list (> 0.75 s)

None. Longest rest: sH on the listing pose, output frames 114-129 (0.5 s), so the dissolve starts from a still frame.
sP, sL and sH cameras move from their first frame. Labels are the only static elements.

## Render budget

sP 68 + sL 36 + sH 75 + sH clay tail 27 = 206 frames at 15 fps, about 85 min serial at 25 s/frame (sL and sH slower with
persistent data off). Order: sL gate previews first (decides the fallback), then sP, sL, sH. Part moves are under
4 px/frame, so 15 fps + minterpolate should hold; look at the piece's edges mid-move and re-render that window at 30 fps
if they double. Reused unchanged: irlB, irlH (trimmed), webzoom_mr2_v2.mp4, camB.json, cam_listing_v.json.
Optional quality step if RAM allows: sP and sL are close-ups (2-3 m). Build their scene from topdown_4mm_al and re-carve
ht_rear from a 2 mm decimation of htrev1 (`--like` topdown); keep the 6 mm scene for sH.

## Checks before assembly

- First / middle / last frame sheet of every shot incl. IRL, with an edge-touch test (non-black pixels in the outer 3 px)
  on sH (must be clean on all frames) and on the raised parts in sL and sH frame 0.
- Per-frame mean luma of sP, sL, sH for a step (lighting dropout).
- Frames +-2 around all nine cuts; sP frame 0 onion; sH last frame vs listing.
- `ive director` expected flags to review, not cut: sP end vs sL (same part, continuous sequence), sH rest frames
  (0.5 s, intentional), sH vs website (same pose by design).
