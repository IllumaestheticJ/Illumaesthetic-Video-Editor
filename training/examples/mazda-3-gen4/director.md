# Mazda 3 (gen 4) hatch - director plan v2 (director, 2026-11-11)

Stage 2. Keeps the scene order of `direction.md` (front -> side -> rear -> WING REMOVED hero -> wing part -> top/reassembly -> logo).
Includes the user's 2026-11-11 feedback A-D (framing intent, one sequence per section, removed state = hero with labels,
no faked states). Total 38.223 s = 70 beats at 110 BPM (beat k = 0.050 + 0.5453 k), 1147 frames at 30 fps.
`python -m ive director` was not run for this plan (no v2-feature timeline yet); v1 report: `director_report_v1.md`
(no focus tags; s1~s2 repeated view IoU 0.7). Tag every clip with the `section` + `focus` below.

Scan frame: nose -Y, car's left +X, body z 0.08..1.53, wing x -0.62..0.56, y 1.33..1.69, z 1.25..1.46.
loc / target in metres, focal in mm on the 20.25 mm sensor (tools/shots.py). `orbit()` angle 0 = front, 90 = car's left,
180 = behind. "fit" = fraction of frame width the subject spans (tools/fitcheck.py; 0.86 = 7 % margin each side).
Wing keys are offsets of `rwing.blend` from its registered pose, **no rotation anywhere** (the underside is shown by
putting the camera under it). All renders 15 fps, 75 %, 12 spp, `persist: false`.

## Shot table

| section | shot | start-end (beats / s / frames) | focus | camera | part action | why it earns its time | render |
|---|---|---|---|---|---|---|---|
| front | **m1_open** | b0-b8 / 0.000-4.412 / f0-132 | whole car, front-left 3/4 | azimuth 35 fixed, h 1.15 -> 1.05, target (0, -0.1, 0.65), 35 mm, straight push-in, NO orbit: `arc(4.6, 35, 35, 1.15, 1.05, c=(0,-0.1,0.65), tz=0.65, fit_to=0.74, push=0.86, shape="lin")` -> fit 0.74 -> 0.86; loc ~ (4.7, -6.8, 1.15) -> (4.1, -6.0, 1.05). `lin` = moving from frame 1 | - | user: whole car, motion from frame 1; grille off-centre | NEW (70 fr) |
| side | **m2_flank** | b8-b16 / 4.412-8.775 / f132-263 | left flank surfacing (reflections sliding over the doors) | truck toward the REAR, target fixed: loc (8.6, -0.6, 1.0) -> (8.6, +0.6, 1.3), target (0, 0, 0.68), 35 mm; fit both end keys to 0.86, use the larger distance for both (pure truck). Ease inout | - | travel step 2; surfacing only reads when the camera translates | NEW (69 fr) |
| rear | **m3_rear** | b16-b28 / 8.775-15.319 / f263-460 | rear end: left tail lamp + hatch shoulder | key 0 = `orbit(0, 118, 1.40, c=(0,0.3,0.70))` fitted to 0.86 (whole car); end loc (2.50, 5.42, 1.15) tgt (0.35, 1.70, 0.85), 35 mm (azimuth 150). 8 keys along the circle, ease inout | - | travel step 3, moves in toward the section that matters; tail lamps = best rear detail | NEW (102 fr) |
| rear: hatch top | **m4_wingoff (HERO)** | b28-b46 / 15.319-25.135 / f460-754 | the rear wing on the hatch -> the exposed **mounting points / bolt holes** (Wing Removed scan) | base `comp_wingoff.blend` + `rwing.blend`, 32 mm all keys. t0 loc (1.30, 3.90, 3.00) tgt (0.00, 1.45, 1.30); t 4.362 (b36) loc (1.05, 3.55, 2.70) tgt (0.00, 1.48, 1.33); t 6.544 (b40) loc (0.75, 3.35, 2.45) tgt (0.00, 1.50, 1.35); t 9.816 (b46) loc (0.70, 3.30, 2.40) tgt (0.00, 1.50, 1.35). Ease `in` on key 0, `lin` through b36 (no stop on the drop), `out` into b40, then a 5 cm creep = the hold | seated t 0-4.362; **pops off ON the drop b36**: 4.362 [0,0,0] -> 5.180 (b37.5) [0, 0.05, 0.30] ease out -> 6.544 (b40) [0, 0.35, 1.05] ease inout (rises up and back, out through the top edge into black) -> 9.816 [0, 0.40, 1.15] lin (off frame) | removed-state data is the hero beat; camera frames the section, stays, moves IN on the mounts and holds them **b40-b46 = 3.3 s** to read; labels sit in this hold | NEW (151 fr) |
| rear: the part | **m5_part** | b46-b52 / 25.135-28.408 / f754-852 | the wing's scanned underside / mounting face | low, almost behind, looking UP ~30 deg, 32 mm: t0 loc (0.55, 5.10, 0.75) tgt (0.05, 2.40, 1.75) -> t 3.272 loc (0.45, 4.75, 0.80) tgt (0.00, 2.60, 1.85), ease inout | t0 [0, 0.40, 1.15] -> 2.181 (b50) [0, 1.05, 0.80] ease inout -> 3.272 [0, 1.10, 0.78] lin: translates back toward the camera into clear black behind the bumper (y 2.4-2.8, z 2.0-2.2), never over the body | shows the part's inner face (wing scan is a closed shell, 49 % of its area faces down) | NEW (53 fr) - **gate: check 1** |
| top | **m6_reassemble** | b52-b64 / 28.408-34.951 / f852-1049; fade to black b62-b64 (33.856-34.951, f1016-1049) | the wing returning to its mounts; whole car from above | high behind-left ~55 deg down, 35 mm: `orbit(t, 125, 6.4, c=(0,0.25,0.7), r=4.0, tz=0.7)` loc ~ (3.3, 2.55, 6.4); fit 0.80 -> 0.86 against car + wing at [0,1.10,0.78] (add that PTS set). Slow push only, no orbit | t0 [0, 1.10, 0.78] -> 2.181 (b56) [0, 0.40, 0.50] ease inout -> 4.362 (**b60 32.770 lock**) [0,0,0] ease in; seated to the end. If the lock shows composite seams, render t >= 4.362 with `car4.blend`, no part | Temerario: reassembly, whole car, fade; the only high view; lock on the phrase line | NEW (102 fr) |
| end | **logo** | b64-b70 / 34.951-38.223 / f1049-1147 | small ILLUMAESTHETIC logo | `ferrari-296/tools/logo_card.py --secs 3.3 --width 320` (~30 % of width, was 820) on render black; fade in 10 frames, fade out with the music decay to f1147 | - | brief: fade, then a SMALL logo | re-make card (no Blender) |

Clip lengths (exact frames for `honda-s2000/tools/concat_assemble.py`): **132, 131, 197, 294, 98, 197, 98** = 1147.
With `ive assemble` use the same cut frames (first clip one frame short). Render counts = ceil(dur x 15) + 3 spare;
`src_fps = (N-1)/(dur + 3/30)` per clip. Cuts: 4.412 (b8), 8.775 (b16), 15.319 (b28), 25.135 (b46 kick), 28.408 (b52 kick),
34.951 (b64 kick). Part hits: wing pops off on **b36 19.682 (kick drop)**, wing locks on **b60 32.770**.

## Framing intent (feedback A: wide = whole car with deliberate margins; detail = named section fills the frame)
Verify every one with `tools/fitcheck.py` on the keys AND by looking at first/mid/last preview stills.

| shot | first | mid | last | must never clip |
|---|---|---|---|---|
| m1 | WIDE: whole car, fit 0.74 (13 % margin each side), centred a little low | whole car 0.80 | whole car 0.86 (7 % margins) | nose, rear bumper, both visible tyres, mirror, roof |
| m2 | WIDE: whole left profile 0.86, car a touch forward of centre | profile centred, 0.86 | profile 0.86, a touch rearward | front/rear bumpers, tyre rings (bottom margin under the tyres) |
| m3 | WIDE: whole car from the left rear quarter, 0.86 | rear half ~1.0 wide (front leaving deliberately) | DETAIL: rear end fills the width - left tail lamp, hatch, badge, roof spoiler line, rear tyre | wing tips, top of hatch, bottom of rear bumper; front is cut deliberately only after mid |
| m4 | DETAIL: hatch top + wing ~57 % of width, roof edge above | b36-b40: wing rising out of the top edge (deliberate exit, into black) | DETAIL: mount row (~1.1 m) ~80 % of width in the lower-middle; upper ~25 % = black beyond the roofline (label band) | the mount row ends (both outer bolt holes), hatch glass top edge; no wing half-clipped while it is still seated |
| m5 | DETAIL: whole wing ~50 % width, upper half on black; car's rear in the lower third | wing ~65 %, underside facing camera | wing ~73 % (dist ~2.55 m), fully in frame on black | both wing tips (FOV at end 1.61 m vs 1.18 m wing) |
| m6 | WIDE: whole car + floating wing, fit 0.80 | car + descending wing 0.83 | whole car 0.86, then fade | wing at every frame, nose, rear bumper |
| logo | black | logo 320 px centred | fade out | - |
No dead black where the subject should be: m2 is the only small-in-frame shot (side profile at 0.86 in 9:16 is short
vertically - it stays because the surfacing only reads in profile); everywhere else the subject fills its intent.

## On-screen labels (feedback C; scan shots only, file-backed, max 2, enter on a beat, leave before the cut)
| text | source (file proof) | shot | in | out (fade done) | position / style |
|---|---|---|---|---|---|
| `REAR WING REMOVED` | Drive `Scans/Mazda 3 (Gen 4) Wing Removed.stl` (1Ki8z-P9LEs0VKnHU9U2GOlYX1BE6hNuG), registered 1.05 mm median | m4 | **b40 21.862** (wing has left the frame) | b45 24.590 fade 6 fr -> gone by 24.79 (< cut 25.135) | top band, left-aligned x 80 px, baseline y ~250 px; Inter Display 54 px, tracking +6, #e8ecf2 |
| `MOUNTING POINTS` | the same state scan: the hatch-top holes/bosses in `comp_wingoff` (`checks/reg/wo2_0.png`) - **only if the m4 last-frame still clearly shows the holes** | m4 | **b42 22.954** | b45 24.590, same fade | under the first line, y ~320 px; JetBrains Mono 30 px, #e8ecf2 |
- Both lines must sit on black: check the m4 b40-b46 frames show black above the roofline in the top ~25 % (y 80-480 px).
  If the roof or wing intrudes there, drop the labels rather than put text over the car.
- No numbers in the labels (nothing to invent). Remotion `ScanHUD` with two `label` items; no `counter`.
- No text anywhere else (no IRL in this reel; logo card has no text besides the logo).

## Cut list (removed from v1 / v2-whole-car)
| removed | why |
|---|---|
| final2/s1_front34, final/s1_front34 (turntables) | rotation spends time without new info (sibling Mazda note); v1 version cropped. Replaced by m1 push-in |
| final2/s2_rear34, final/s2_rear34 | rear shown before the side = ping-pong; same view as s1 (IoU 0.7) |
| final2/s3_front, final/s3_lamp | front twice; front has no parts/states; v1 close-up "too cropped" |
| final2/s4_side, final/s4_flank | orbit drift / cropped glide; replaced by the m2 truck (fallback only) |
| final2/s5_rear, final/s5_tail | second rear-end shot; merged into m3 |
| final2/s6_wing, final/s6_wing | wing lift in a wide whole-car view during the build: section not framed, misses the drop, no hold on the mounts. Replaced by m4 |
| final2/s7_top, final/s7_top | rotating top-down: rotation; the top section is now m6 only |
| final2/s8_explode (stopped at 25/186 fr), final/s8_explode | one wide orbit; contains the OEM Aero Kit Spoiler, which does not register to this car (implied data) |
| OEM Aero Kit Spoiler, Hatch Upper Trim Panel | spoiler: not this car's part; trim panel = the same wing |
| any door / hatch / hood opening | no scan of those states (Side Skirt Door Open = sill only) - feedback D |
| logo at 820 px | brief: small logo |

## Hold list (> 0.75 s with little or no motion)
| where | length | reason |
|---|---|---|
| m4 t 0-4.362 (b28-b36): wing seated | 4.36 s | camera pushes through the build so the wing's shape reads before it comes off on the drop |
| **m4 b40-b46: mounting points** | **3.27 s** | hero hold (feedback C): the real bolt holes from the Wing Removed scan, 5 cm creep, labels read here |
| m5 b50-b52: wing near-still behind the bumper | 1.09 s | let the underside read; camera still pushing |
| m6 b60-b62 settled car, fade b62-b64 | 1.09 s + 1.09 s | settle on the clean whole car after the lock; short (s2000 lesson) |
| logo b64-b70 | ~2.9 s visible | music decays to the end |

## Render budget
| shot | seconds | frames @15 fps | base / parts |
|---|---|---|---|
| m1_open | 4.41 | 70 | car4 |
| m2_flank | 4.36 | 69 | car4 |
| m3_rear | 6.54 | 102 | car4 |
| m4_wingoff | 9.82 | 151 | comp_wingoff + rwing |
| m5_part | 3.27 | 53 | comp_wingoff + rwing |
| m6_reassemble | 6.54 | 102 | comp_wingoff + rwing (car4 after the lock if needed) |
| total | | **547** | ~13 s/frame -> ~2 h serial, one Blender job at a time |

Order: previews first (first/mid/last at 30 % for each shot + one still of `rwing.blend` from below), then m4, m5, m6, then
m1-m3. After each final: per-frame mean-luma scan (lighting dropouts), contact sheet. New spec names `m*` and a new output
folder (e.g. `renders/final3/`); do not overwrite final2/.
Reused unchanged: none (every existing render is an orbit, a duplicate subject or a v1 crop). Fallback only:
m2 <- `final2/s4_side` reversed (38 fr, src_fps = 37/(4.363+0.1)).

## Checks before assembly
1. rwing underside still: a real mounting face? If not, drop m5: m4 runs b28-b48 (hold to b48), m6 b48-b64 (wing returns
   b48-b56 from [0,0.40,1.15], lock still b60).
2. m4 last frame: holes clearly readable at 4 mm + Wing Removed fill? If not, drop the MOUNTING POINTS label (keep
   REAR WING REMOVED) and end the push at loc (0.85, 3.45, 2.55) where the row still reads as a pattern.
3. Frames +-2 around every cut and at b36/b60 in the delivered file; cut-to-kick error on decoded audio (<= 1/2 frame).
4. `ive log` each decision; tag `section`/`focus` per clip and run `python -m ive director` on the new timeline - it must
   report no repeated views.
