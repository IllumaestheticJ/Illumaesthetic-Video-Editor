# Nissan Frontier Pro-4X v2 - shot plan (director, 2026-11-11)

Scene order is from `direction.md` (unchanged). Newest note: "Better. Highlight and label each unique scan section."
`ive director` on v1: s1_front34 ~ s2_rear34 repeated view (IoU 0.84); no shot had a focus. Every v2 shot below has one.

Frame = prep metres (tools/shots.py): nose -Y (y=-2.68), tail +Y (2.69), car's right = -X, z=0 = lift-pad cut
(ground -0.2), hood rear shut line z~1.04, roof ~1.65. Sensor 20.25 mm horizontal (frame width = 20.25*d/f).
Shot times below are seconds from the reel start; part keys are given as seconds from the SHOT start (as shots.py uses).
All parts that come off **stay off** (parked) in every later shot until S8 brings them home = progressive explode over
several angles. Parked poses: grille (+1.90, -0.45, +0.10); bumper (0, -0.95, -0.60) rot x 120; hood (0, +0.05, +1.25);
flares_r (-0.30, 0, +1.00), flares_l (+0.30, 0, +1.00).

## Shot table

| section | shot | start-end | focus | camera | part action (shot-relative s) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | S1 `v2_s1_wide` | 0.000-4.852 (8 b) | the whole truck | front-right 3/4, `keyed_orbit(r 8.2->7.6, ang -32->-46, h 1.5->1.7, c (0,-0.2,0.75)->(0,-0.3,0.75), focal 26)`; moving from frame 1; truck ~70 % of width, nose, bed, roof and step rails all inside with >=80 px margins | none | hook: the whole scanned truck, front end (where all the data is) towards the lens | NEW, car4, 77 fr |
| front / grille | S2a `s3_grille` | 4.852-7.266 (4 b) | grille + Nissan badge | v1 extreme close-up slide across the nose (40 mm, 2 mm mesh) | none | detail before the teardown starts | **REUSE v1 unchanged**, frames 0-36 of 49 (in=0, dur 2.414) |
| front / grille | S2b `v2_s2_grille` | 7.266-9.681 (4 b) | GRILLE leaving the bumper | starts EXACTLY on s3_grille's last pose (loc -0.15,-3.95,0.88 / tgt -0.2,-2.62,0.74 / f40) so the cut reads as one move; by 1.9 s -> loc (1.5,-5.2,1.1) tgt (1.5,-3.0,0.85) f24 (grille fills ~60 % width, nose corner at left edge), slow drift after | grille: hold 0-0.30; 0.30->0.90 fwd (0,-0.30,0); 0.90->1.80 out to the car's left (+1.90,-0.45,+0.10) ease inout, clear of the fender silhouette into black; parked 1.8->end (holds over the silent beat 9.08). Highlight + label **GRILLE** (sub "SCAN SECTION 01 / 06") 0.604-2.114 (7.870-9.380). Translate only - grille back is thin/dark (backs.png) | the grille is its own part scan; shown coming off and parked in clear space | NEW, base comp_fbrhc + x_bumper (static) + x_grille, 40 fr |
| front / bumper | S3 `v2_s3_bumper` | 9.681-14.509 (8 b) | FRONT BUMPER: off, then its scanned inside | start loc (-1.9,-6.4,1.0) tgt (-0.1,-2.9,0.55) f30 (nose + bumper); 1.2 s tgt (-0.06,-3.6,0.15) following it down; 3.6 s loc (-0.6,-5.6,2.2) tgt (-0.06,-3.65,-0.1) f28; 4.83 s loc (-0.4,-5.2,1.9) (bumper ~90 % width, on black below the truck) | bumper moves ON the drop: 0->0.60 (0,-0.70,-0.05); 0.60->1.206 (0,-0.95,-0.60) - forward then down below the truck into black (lands 10.887); hold; 2.414->3.621 rot x +120 about its own centroid (inner face, which faces +Y, turns to (0,-0.5,0.87) = towards the high camera). Highlight + label **FRONT BUMPER** ("SCAN SECTION 02 / 06") 1.206-3.019 (10.887-12.700) | the drop goes to the richest data; the turn is justified: inside is scanned (ribs, mounting tabs, fog-lamp housings, grille mounting frame - backs.png) | NEW, comp_fbrhc + x_bumper, 76 fr |
| front / bumper-off state | S4 `v2_s4_removed` | 14.509-18.130 (6 b) | what is behind the bumper (fbrhc state) | low, straight-on, slightly left of centre (S3 was right): loc (0.6,-6.0,0.85) tgt (-0.06,-2.6,0.6) f30 -> loc (0.3,-4.4,0.8) tgt (-0.06,-2.55,0.55) f32, ease inout (whole front -> core fills the frame). Parked bumper may sit at the bottom edge on black, never across the core | none moving. Highlight the fbrhc fill (separate object via composite.py `--fills-out`) + label **FRONT BUMPER REMOVED** (no sub) 1.207-3.321 (15.716-17.830). Optional 2nd label **RADIATOR CORE** 2.414-3.321 only if the core fins read in the final frame | rule C hero beat: move in and hold on the bumper-removed data | NEW, comp_fbrhc, 58 fr |
| front / hood | S5 `v2_s5_hood` | 18.130-20.544 (4 b) | HOOD lifting off | front-right 3/4 BELOW the lifted hood so it silhouettes on black above the roofline: loc (-2.8,-5.4,1.5) tgt (-0.06,-2.3,1.2) f26 -> tgt (-0.06,-2.1,1.85), loc (-2.6,-5.2,1.7) | hood: hold 0-0.30; 0.30->1.207 straight up (0,+0.05,+1.15) ease inout (lands on the b32 accent 19.337); 1.207->2.41 drift to +1.25 lin. **No hinge, no flip** (no hood-open scan; outer skin only). Label **HOOD** ("SCAN SECTION 03 / 06") 1.207-2.110 (19.337-20.240) | hood-removed state exists, hood-open does not -> it lifts off | NEW, comp_front + x_hood + parked bumper/grille, 40 fr |
| front / structure | S6 `v2_s6_struct` | 20.544-24.166 (6 b) | FRONT STRUCTURE (bhr): radiator support, core, lower beam, lamp housings | high front, ~35 deg down (never overhead): loc (-1.0,-5.2,2.6) tgt (-0.06,-2.6,0.8) f30 -> loc (-0.5,-4.1,2.2) tgt (-0.06,-2.35,0.75) f32; keep the floating bhr fragments above the support out of frame | struct object highlighted + label **FRONT STRUCTURE** ("SCAN SECTION 04 / 06") 1.207-2.716 (21.751-23.260). Optional **RADIATOR SUPPORT** 2.415-3.316 if readable. Hood parked above, out of frame top | deepest front state, closes the front sequence | NEW, comp_front (struct separate) + parked parts, 58 fr |
| side / flares | S7 `v2_s7_flares` | 24.166-27.787 (6 b) | FENDER FLARES (both right-side arches) | front-right side 3/4, `keyed_orbit(r 6.0->5.8, ang -60->-75, h 1.9->1.8, c (0,-0.2,0.9), focal 26)`; both right arches + flares in frame | flares: hold 0-0.604; 0.604->1.207 up and out (r: -0.30,0,+1.00; l: +0.30,0,+1.00) so each sits above the hood/bed-rail line on black (lands 25.373). Label **FENDER FLARES** ("SCAN SECTION 05 / 06") 1.207-3.314 (25.373-27.480), leader to the front-right flare. Translate only | the only side data; travel front -> side | NEW, comp_explode + all parked parts, 58 fr |
| whole (rear 3/4) | S8 `v2_s8_home` | 27.787-33.822 (10 b) | the truck reassembling -> FULL TRUCK | high rear-right 3/4 descending: `keyed_orbit(r 8.0->7.6, ang -135->-150, h 3.4->1.9, c (0,0.2,0.75), focal 26)`; whole truck in frame every frame | home one per beat on the crash: flares 0->0.604, hood 0.604->1.207, bumper (un-turn + home) 1.207->1.810, grille 1.810->2.414 = lock 30.201; swap to clean car4 on 2.414 (c5 lesson). hl_all + label **FULL TRUCK** ("PRO-4X - SCAN SECTION 06 / 06") 3.621-5.433 (31.408-33.220); fade to black 33.220-33.822 in the assembly | reassembly + the only rear view; travel ends at the rear | NEW, 94 fr |
| logo | logo | 33.822-38.37 | logo | small card (~35 % width, reuse logo_card.py, --width ~380), fade in 0.3 s, out with the track by ~36.3-37.4, black to the end | - | ending | re-make card |

Label rules (all): names only, data-backed; Inter Display title / JetBrains Mono sub, `#e8ecf2`; leader to the part's
projected bbox centre (tools/labels.py anchors), text outside the silhouette, 80 px inside the frame, enter on the
accent, leave >=0.3 s before the cut. Never "CRASH BEAM" (not proven by a scan).

## Cut list (v1 -> v2)
- s1_front34: crops the bed -> replaced by S1 (whole truck).
- s2_rear34: repeated view of s1 (IoU 0.84), no rear data, front->rear->front ping-pong.
- s4_arch: dark/busy, same side region as S7.
- s5_open: hood shown hinged open (no hood-open scan), three parts in one wide shot -> split into S2b/S3/S5, parts parked.
- s6_top: rotating top-down, no feature; also risk of overhead roll.
- s7_explode + v2_check label draft: every part separating at once in one wide orbit -> separation moved into S2b-S7,
  only the reassembly stays wide (S8).
- logo shown ~2.4 s instead of ~4 s.

## Hold list (> 0.75 s)
- S2b 9.0-9.681 (0.9 s): grille parked; covers the track's silent beat 9.08 so the drop cut lands on stillness->motion.
- S3 12.70-14.509 (1.8 s): bumper inner face held under a slow push-in - reading ribs/tabs/fog housings (rule C).
- S4 whole shot (3.6 s): no part moves; continuous push-in to the core = the hero hold (rule C).
- S6 21.75-24.166 (2.4 s): no part moves; push-in over the structure while the label reads.
- S8 30.20-33.22 (3.0 s): car locked, camera keeps descending; FULL TRUCK highlight/label.
- Logo ~2.4 s visible.

## Render budget (15 fps, render secs = slot + 0.2 s)
New: S1 77, S2b 40, S3 76, S4 58, S5 40, S6 58, S7 58, S8 94 = **501 frames** (v1: ~555) -> ~1.8-4.2 h at 13-30 s/frame,
one at a time, persistent data OFF for every shot with parts (S2b-S8), per-frame luma scan after each.
Reused unchanged: **s3_grille only** (frames 0-36). Not reused: s1_front34, s2_rear34, s4_arch, s5_open, s6_top, s7_explode.
New asset before rendering: `comp_fbrhc` = `tools/composite.py parts/comp_fbrhc.stl --remove parts/bumper.stl
parts/grille.stl --fill lev/fbrhc_2mm_C.stl:<same front zone as comp_front> --fills-out parts/fbrhc_fill.stl`, prep
both `--like prep/car4.json`. Before the finals: first/mid/last check sheet of every new shot (rule A).

## Open questions
- S2b shows the grille off with the bumper on; the core seen through the opening is from the fbrhc (bumper-off) scan.
  If the reviewer objects: grille + bumper leave together on the drop and the grille lifts off the bumper in clear space
  inside S3; S2b becomes highlight + GRILLE label only (grille stays on).
- Optional second labels (RADIATOR CORE in S4, RADIATOR SUPPORT in S6) only if readable in the final frames.
