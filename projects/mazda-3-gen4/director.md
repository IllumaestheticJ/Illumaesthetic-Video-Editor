# Mazda 3 (gen 4) hatch - director plan v2 (director, 2026-11-11)

Stage 2. Keeps the scene order of `direction.md` (front -> side -> rear -> wing off -> wing part -> reassembly -> logo).
Total 38.223 s = 70 beats at 110 BPM (beat k = 0.050 + 0.5453 k), 1147 frames at 30 fps. No text.
`python -m ive director` was not run for this plan (no v2-feature timeline exists yet); the v1 report is
`director_report_v1.md` (no focus tags; s1~s2 repeated view IoU 0.7). Tag every clip below with its `section` + `focus`.

Scan frame: nose -Y, car's left +X, body z 0.08..1.53, wing at x -0.62..0.56, y 1.33..1.69, z 1.25..1.46.
Camera notation: loc / target in metres, focal in mm on the 20.25 mm sensor (tools/shots.py). `orbit()` angle
0 = front, 90 = car's left, 180 = behind. Wing keys are offsets of `rwing.blend` from its registered pose, no rotation
anywhere (lessons: don't spin a part unless the backside is the point - here the underside is shown by moving the
camera under it, not by flipping it). All renders 15 fps, 75 %, 12 spp, `persist: false`.

## Shot table

| section | shot | start-end (beats / s / frames) | focus | camera | part action | why it earns its time | render |
|---|---|---|---|---|---|---|---|
| whole | **m1_open** | b0-b8 / 0.000-4.412 / f0-132 | the whole car, front-left 3/4 (Kodo face + flank in one view) | fixed azimuth 35 deg (front-left), h 1.15 -> 1.05, target (0, -0.1, 0.65), 35 mm. Straight push-in, NO orbit: `arc(4.6, 35, 35, 1.15, 1.05, c=(0,-0.1,0.65), tz=0.65, fit_to=0.78, push=0.86, shape="lin")` -> whole car 78 % -> 91 % of width; loc ~ (4.6, -6.6, 1.15) -> (4.0, -5.8, 1.05). `lin` = moving from frame 1 | - | reviewer: "standard full car scan - show the whole car"; brief: whole car, motion from frame 1; grille stays off-centre | NEW (70 fr) |
| side | **m2_flank** | b8-b16 / 4.412-8.775 / f132-263 | left flank surfacing (reflection lines sliding over the doors) | truck along +X side toward the REAR with the target fixed: loc (8.6, -0.6, 1.0) -> (8.6, +0.6, 1.3), target (0, 0, 0.68) fixed, 35 mm; fit both end keys to 0.86 with `fc.extent` and use the larger distance for both (constant distance = pure truck). Ease inout | - | travel step 2, continues the direction of m1; the only new info on the side is the surfacing, which only reads when the camera translates | NEW (69 fr) |
| rear | **m3_rear** | b16-b28 / 8.775-15.319 / f263-460 | rear end: left tail lamp + hatch shoulder | arrive round the left rear corner and push in: key 0 = `orbit(0, 118, 1.40, c=(0,0.3,0.70))` fitted to 0.86 (whole car); end = loc (2.50, 5.42, 1.15) target (0.35, 1.70, 0.85), 35 mm (azimuth 150, rear half fills the width, front cropped out only at the very end). 8 keys along the circle, ease inout | - | travel step 3, moves in toward the section that matters; tail lamps are the best-scanned rear detail (v1 s5_tail). Ends at 3/4 so m5 owns the behind view | NEW (102 fr) |
| wing | **m4_wingoff** | b28-b42 / 15.319-22.954 / f460-689 | the rear wing on the hatch -> its real mounting holes once it is off | base `comp_wingoff.blend` + part `rwing.blend`. High behind-left looking down on the hatch top, 35 mm: t0 loc (1.30, 3.90, 3.00) tgt (0.00, 1.45, 1.30) [wing ~63 % of width]; t 4.362 (b36) loc (1.05, 3.40, 2.75) tgt (0.00, 1.45, 1.32) [~78 %]; t 7.635 (b42) loc (0.70, 2.95, 2.55) tgt (0.00, 1.50, 1.33) [mount row ~1.1 m fills the width]. Ease `in` on the first key, `lin` through b36 (no stop at the drop), `out` into b42 | wing seated t 0-4.362; **lift ON the drop b36**: 4.362 [0,0,0] -> 5.180 (b37.5) [0, 0.05, 0.30] ease out (pops off the mounts on the kick) -> 5.453 (b38) [0, 0.10, 0.45] lin -> 7.635 (b42) [0, 0.35, 1.05] ease inout: rises up and back, leaves through the top edge into black ~b40-b41 | the only registered part + state in the data gets the drop; the camera frames the section, stays on it and moves in on what the removal reveals (brief #2, lessons mazda-miata-nc / c5) | NEW (118 fr) |
| wing | **m5_part** | b42-b52 / 22.954-28.408 / f689-852 | the wing's scanned underside / mounting face | low, almost straight behind (azimuth ~172), looking UP ~30 deg, 32 mm: t0 loc (0.55, 4.90, 0.75) tgt (0.05, 2.40, 1.75) -> t 5.453 loc (0.40, 4.50, 0.85) tgt (0.00, 2.65, 1.90), ease inout. Car's rear end in the lower third, wing against black above it | continues m4's end pose: t0 [0, 0.35, 1.05] -> 4.362 (b50) [0, 1.05, 0.80] ease inout -> 5.453 [0, 1.10, 0.78] lin. Translates back toward the camera into clear background behind the bumper (y 2.4-2.8, z 2.0-2.2), never over the body | brief: show the part's inner face; the wing scan is a closed shell (49 % of its area faces down) - shown by moving under it, not by spinning it | NEW (85 fr) - **gate: open question 1** |
| whole | **m6_reassemble** | b52-b64 / 28.408-34.951 / f852-1049; fade to black b62-b64 (33.856-34.951, f1016-1049) | the wing returning to its mounts; the complete car from above | high behind-left, ~55 deg down, 35 mm: `orbit(t, 125, 6.4, c=(0,0.25,0.7), r=4.0, tz=0.7)` loc ~ (3.3, 2.55, 6.4); fit 0.84 -> 0.90 over the shot against car + wing at [0,1.10,0.78] (add a PTS set for that offset). Slow push only, no orbit | t0 [0, 1.10, 0.78] -> 2.181 (b56) [0, 0.40, 0.50] ease inout -> 4.362 (**b60 32.770 lock**) [0,0,0] ease in; seated to the end. If the lock frame shows composite seams, render t >= 4.362 with `car4.blend` and no part (same frame) | Temerario: reassembly, whole car, fade; the only high view in the reel (not a repeat of m1's low front 3/4 or m3's level rear 3/4); lock on the phrase line | NEW (102 fr) |
| end | **logo** | b64-b70 / 34.951-38.223 / f1049-1147 | small ILLUMAESTHETIC logo | `ferrari-296/tools/logo_card.py --secs 3.3 --width 320` (~30 % of width, was 820) on render black; fade in over 10 frames from black, fade out with the music decay to f1147 | - | brief: fade, then a SMALL logo; music dies ~38.2 | re-make card (no Blender) |

Clip lengths (exact frames for `honda-s2000/tools/concat_assemble.py`): **132, 131, 197, 229, 163, 197, 98** = 1147.
With `ive assemble` use the same cut frames (first clip one frame short). Render counts are ceil(dur x 15) + 3 spare
frames; set `src_fps = (N-1)/(dur + 3/30)` per clip (sti lesson) so no clip ends on frozen frames.
Cut times: 4.412, 8.775, 15.319, 22.954, 28.408, 34.951 - every one a phrase line (b8/b16/b28) or a kick (b42/b52/b64).
Part hits: wing pops off on **b36 19.682 (kick drop)**, wing locks on **b60 32.770**.

## Cut list (removed from v1 / v2-whole-car)
| removed | why |
|---|---|
| final2/s1_front34, final/s1_front34 (turntables) | rotation spends time without new info (sibling Mazda note); v1 version cropped. Replaced by m1 push-in |
| final2/s2_rear34, final/s2_rear34 (rear 3/4 orbits) | rear shown before the side = ping-pong; same view as s1 (IoU 0.7); rear arrival now m3 |
| final2/s3_front, final/s3_lamp | front shown twice; front has no parts/states; v1 close-up "too cropped" |
| final2/s4_side, final/s4_flank | orbit drift / cropped glide; replaced by the m2 truck (fallback only, see below) |
| final2/s5_rear, final/s5_tail | second rear-end shot; merged into m3 |
| final2/s6_wing, final/s6_wing | wing lift in a wide whole-car view during the build: section not framed, misses the drop. Replaced by m4 |
| final2/s7_top, final/s7_top | rotating top-down: rotation, no top-only data |
| final2/s8_explode (stopped at 25/186 fr), final/s8_explode | one wide orbit separating everything; contains the OEM Aero Kit Spoiler, which does not register to this car (implied data). Replaced by m4-m6 |
| OEM Aero Kit Spoiler, Hatch Upper Trim Panel | spoiler: not this car's registered part; trim panel = the same wing |
| logo at 820 px | brief: small logo |

## Hold list (> 0.75 s with little or no motion)
| where | length | reason |
|---|---|---|
| m4 t 0-4.362 (b28-b36): wing seated | 4.36 s | not static: the camera pushes 3.25 -> 2.63 m through the build so the wing's shape reads before it comes off; the removal is saved for the drop |
| m4 b40-b42: wing gone, camera on the mounts | ~1.1 s | the payoff of the removal: the real mounting holes from the Wing Removed scan, camera still pushing |
| m5 b50-b52: wing almost still above the bumper | 1.09 s | let the underside read before the cut; camera keeps pushing |
| m6 b60-b62: car assembled, then fade b62-b64 | 1.09 s + 1.09 s fade | settle on the clean whole car after the lock; short (s2000 lesson: last scenes held too long) |
| logo b64-b70 | ~2.9 s visible | music decay to the end; small logo, fades with the track |

## Render budget
| shot | seconds | frames @15 fps | base / parts |
|---|---|---|---|
| m1_open | 4.41 | 70 | car4 |
| m2_flank | 4.36 | 69 | car4 |
| m3_rear | 6.54 | 102 | car4 |
| m4_wingoff | 7.64 | 118 | comp_wingoff + rwing |
| m5_part | 5.45 | 85 | comp_wingoff + rwing |
| m6_reassemble | 6.54 | 102 | comp_wingoff + rwing (car4 after the lock if needed) |
| total | | **546** | ~13 s/frame -> ~2 h serial, one Blender job at a time |

Order: previews first (3 stills each at 30 %; also one still of `rwing.blend` from below for open question 1), then
m4, m5, m6 (the story), then m1-m3. After each final: per-frame mean-luma scan for lighting dropouts (lessons) and a
contact sheet. Write the specs as new names (`m*`) in a new `tools/shots_v3.py`-style file or new entries; do not overwrite
final2/.

Reused unchanged: none (no existing render has the right content). Fallback only if time runs out:
m2 <- `final2/s4_side` reversed (38 fr, src_fps = 37/(4.363+0.1)); everything else must be new.

## Checks the editor must do before assembly
1. rwing underside still: real mounting face? If not, drop m5 -> m4 b28-b46 (wing keys stretched, ends [0,0.35,1.05]),
   m6 b46-b64 (wing returns over 10 beats, lock still b60).
2. m4 final pose: mount holes sharp enough at 4 mm + Wing Removed fill? If soft, end the push at loc (0.85, 3.15, 2.65).
3. Look at frames +-2 around every cut and at b36/b60 in the delivered file; measure cut-to-kick error on decoded audio.
4. `ive log` each decision; tag `section`/`focus` per clip so `python -m ive director` reports coverage.
