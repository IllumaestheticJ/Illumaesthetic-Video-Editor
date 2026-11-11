# Mazda Miata ND - scene direction v2 (scene-director, 2026-11-11)

Inputs: v2 brief (relayed), the later user feedback A-D (cropping, one sequence per section, bumper-removed data as the
hero beat with short factual labels, openings only for registered states), lessons.md, clips.md, editlog, director_report
(s1 ~ s2 IoU 0.79), and contact sheets of every v1 render in `/home/user/media/work/miata/renders/final/`.
I also rendered check stills (30 %, 6 spp; scratch, not for the reel) to answer the open data questions:
- **x_fbumper back side**: the inside IS scanned: grille back, inner ribs, mounting tabs. It is rougher than the rear
  bumper and has the known ragged top edge, but it is real data, so a flip is justified.
- **x_rbumper back side**: excellent inner face (ribs, clips, brackets). Flip justified.
- **x_mirror_r inboard side**: mounting plate with studs + the wiring harness are scanned. A turn is justified (small part).
- **'Rear End Trunk Open Bumper Removed' open lid**: only fragments of the lid were captured. x_trunk is a single outer
  skin with **no underside data**, so its underside must never face the lens (camera rules below). Same for x_hood.
- **comp_front, looked at from the front with the bumper off**: front crash beam with bolt-on end brackets, a finned cooling
  core below it, the engine bay behind. **comp_rear from behind**: rear panel with tabs, dual exhaust tips, lower bar,
  and the trunk interior.

## 1. Feature inventory

| Region | Scans (registered) | States | Parts | Signature features | Weak data | Richness |
|---|---|---|---|---|---|---|
| Front | car2_front (2 mm), comp_front | **Bumper off + hood open** ('Bumper Off Hood Open', hinge 3.0 mm) | x_fbumper (inside scanned; 4.8 mm median, 78 % overlap, red overlay sits), x_hood (outer skin only, hinge fit) | headlights, grille, **crash beam + brackets**, cooling core, **engine bay** | hood speckle holes (top-down), bumper top edge ragged, hood has no underside | **highest**: 1 state, 2 parts, 3 structures |
| Wheels | car2_front 2 mm, v1 s3 | - | - | 6-spoke wheel, brake behind, tyre sidewall lettering | - | medium (detail only) |
| Side (right) | comp_explode ('Side Skirt Off' sill fill, 'Mirrors Removed' fill) | skirt off, mirrors off | x_mirror_r/l (1.3 mm, mount plate + harness scanned), x_skirt (single skin strip) | mirror mount | skirt single skin; **no door scan** (door-open scan has no door) | medium |
| Rear | comp_rear (3-4 mm) | **Bumper off**, **trunk open** ('Rear bumper removed trunk closed', 'Rear End Trunk Open Bumper Removed', hinge 7.6 mm) | x_rbumper (inside + outside, 2.8 mm, plate flattened), x_trunk (outer skin only) | **dual exhaust**, rear panel tabs, lower bar, trunk interior | trunk lid has no underside; lid fragments in the open-state scan (removed in comp_rear) | **high**: 2 states, 2 parts |
| Top | car4np | - | - | roof/soft top | **speckle holes on the hood** | low -> cut |
| Interior/doors | - | - | - | - | no data | none -> never shown |
| Small parts | Front Bumper Markers, Rear Markers, Plate Lights | - | registered 2-4 mm but tiny | - | ~20 px in any shot | not used |

## 2. Scene order (travel: front-right -> front -> right front wheel -> right side -> rear -> finale on the left side)

Front = richest region (state + 2 parts + crash beam + engine bay), so the opener frames the **front end** in a whole-car
front-right 3/4 and the reel travels front -> side -> rear down the car's right side, then the finale moves to the
**left side**, which has not been seen yet (so no view repeats). Each section appears in one continuous run of shots.

| # | Shot id | Section | Scans used | Feature shown (focus) | Why here (inventory) | Beats (n = kicks from 8.336 s) | Camera note |
|---|---|---|---|---|---|---|---|
| 1 | v2_a_open | whole car | car4np | the WHOLE car, front-right 3/4 | front is the richest end; brief rule 4 (whole car, motion from frame 1) | 4 pad beats, n -4..0 | low 3/4, slow push + 12 deg orbit toward the nose, car 75-85 % of width |
| 2 | s4_lamp (reuse) | front | car2_front | right headlight + grille (2 mm) | signature front detail; "lamps are fine" | n 0..4 | v1 slide across the nose |
| 3 | v2_f_bumper | front | comp_front + x_fbumper | front bumper comes off -> its **inner face / mounting points** -> camera moves in on the **crash beam** | feedback C hero beat #1 | n 4..12 (8) | tight on the nose; bumper goes forward and down into black below the nose and flips to face the lens |
| 4 | v2_f_bay | front (engine bay) | comp_front + x_hood (+ x_fbumper parked) | hood swings to its captured open pose -> **engine bay** | registered hood-open state; hood lands ON the lift (n16) | n 12..18 (6) | high (>= 55 deg) so the hood's missing underside never faces the lens |
| 5 | s3_wheel (reuse, **reversed**) | wheels | car2_front | front-right wheel, brake, tyre | the only wheel shot; reversed it slides rearward, continuing the travel to the side | n 18..22 | v1 frames played last -> first |
| 6 | v2_s_side | side | comp_explode + x_mirror_r, x_skirt (+ hood open, rear parts home) | right mirror off, turned to show its **mount plate + harness**; then the **sill skirt** slides out | mirror backside is real data; skirt is single skin -> translate only | n 22..28 (6) | starts close on the mirror, pulls back and down onto the sill |
| 7 | v2_r_bumper | rear | comp_rear + x_rbumper (+ x_trunk home) | rear bumper off -> **inner face** -> camera in on **exhaust / rear structure** | feedback C hero beat #2; best-registered part (2.8 mm, inside + outside) | n 28..34 (6) | rear-right; bumper goes back and down into black, flips to face the lens |
| 8 | v2_r_trunk | rear (trunk) | comp_rear + x_trunk (+ x_rbumper parked) | trunk lid swings to its captured pose -> **trunk interior** | registered trunk-open state | n 34..38 (4) | high right side (~47 deg): the lid stays edge-on/top-facing, underside never seen |
| 9 | v2_x_front | explode | comp_explode + all 7 parts | front assembly rises into layers above the nose (hood, front bumper inner-face up, mirrors) | progressive explode, angle 1 (rule 7) | n 38..42 (4) | high front-LEFT 3/4, tight on the front stack |
| 10 | v2_x_rear | explode | same, same part clock | rear assembly in layers (trunk, rear bumper inner-face up, skirt), then return starts | progressive explode, angle 2 | n 42..46 (4) | high rear-LEFT 3/4, tight on the rear stack |
| 11 | v2_x_home | reassembly | same -> car4np at lock | parts fly home, lock ON the last hit; clean car; fade | rule 7: reassembly -> fade | n 46..48 + 0.4 s tail | left side profile, whole car (new view) |
| 12 | logo | - | logo_card --width 300 | small logo on black | rule 7 (v1 was 860 px) | after the last hit, 2.2 s | - |

Dropped from v1: s1 (cropped nose; replaced by v2_a_open), s2 (same view as s1, IoU 0.79; a rotation with no new subject;
the rear is covered by the rear section), s7 top-down (a rotation onto the weakest data, the hood speckle holes), s8 (all
parts separating at once in a wide orbit, disallowed by rule 2).

## 3. Music map (track `mazda-miata-nd_track.mp3`, 116.01 BPM, beat 0.51721 s, kick anchor 8.336 s)

**Music start changes to 6.2672 s** (4 pad beats before the first kick; lessons: "long kick-less intro: start 4 beats
before the drop"). Video t(n) = 2.0688 + 0.51721 n; frame = round(30 t). 0.3 s fade-in on the pads.

| Shot | n | Track s | Video s | Frames (30 fps) | Music |
|---|---|---|---|---|---|
| v2_a_open | -4..0 | 6.267-8.336 | 0.000-2.069 | 0-62 | pads |
| s4_lamp | 0..4 | 8.336-10.405 | 2.069-4.138 | 62-124 | **first kick = first cut** |
| v2_f_bumper | 4..12 | 10.405-14.543 | 4.138-8.275 | 124-248 | kicks, even-beat accents |
| v2_f_bay | 12..18 | 14.543-17.646 | 8.275-11.379 | 248-341 | lift n14-16 (15.58-16.61); **hood lands on n16 (frame 310)** |
| s3_wheel rev | 18..22 | 17.646-19.715 | 11.379-13.447 | 341-403 | louder section |
| v2_s_side | 22..28 | 19.715-22.818 | 13.447-16.551 | 403-497 | |
| v2_r_bumper | 28..34 | 22.818-25.921 | 16.551-19.654 | 497-590 | |
| v2_r_trunk | 34..38 | 25.921-27.990 | 19.654-21.723 | 590-652 | |
| v2_x_front | 38..42 | 27.990-30.059 | 21.723-23.792 | 652-714 | |
| v2_x_rear | 42..46 | 30.059-32.128 | 23.792-25.860 | 714-776 | return starts n45 (frame 760) |
| v2_x_home | 46..48 + 0.4 s | 32.128-33.562 | 25.860-27.295 | 776-819 | **parts lock on the last hit 33.162 (frame 807)**, fade 807-819 |
| logo | - | 33.562-35.762 | 27.295-29.495 | 819-885 | decay; audio fade-out 0.4 s at the end |

Every cut is on an even (accented) kick: n 0, 4, 12, 18, 22, 28, 34, 38, 42, 46. The reassembly lands on the last hit.
Total 885 frames = 29.5 s (v1 32.4 s).

Labels: the original brief said "no text". The later user feedback C overrides that for six short factual labels in
the two bumper-removed sections only. Their text, beats and positions are in director.md.

## 4. Diff vs v1

| v1 | v2 | Reuse or re-render | Why |
|---|---|---|---|
| s1_turntable | v2_a_open | **re-render** (new id) | v1 cropped the nose (brief rule 4, feedback A) |
| s2_rear | - | cut | same view as s1 (IoU 0.79); rotation without a new subject |
| s3_wheel | s3_wheel, reversed, moved from 2nd detail to after the front section | **reuse** (order + direction only) | real 2 mm data; reversed motion carries the travel rearward |
| s4_lamp | s4_lamp, first shot after the opener | **reuse** (order only) | front detail, sits with its section |
| s5_front | v2_f_bumper + v2_f_bay | **re-render** | v1 too wide; bumper showed its outer face only; hood underside (no data) faced the lens |
| s6_rear_open | v2_r_bumper + v2_r_trunk | **re-render** | too wide and cropped at the frame edge; bumper inner face not shown; open lid's empty underside faced the lens |
| s7_top | - | cut | rotation onto the weakest data (hood speckle) |
| s8_explode | v2_x_front + v2_x_rear + v2_x_home | **re-render** | all-at-once wide orbit is disallowed; now progressive, two tight angles, then reassembly |
| logo 860 px | logo 300 px | re-make card | rule 7 |
| no text | 6 factual labels in the two bumper sections | Remotion ScanHUD `label` items | feedback C overrides "no text" for these labels only |

New renders: 356 frames at 15 fps (see director.md). Reused unchanged: s3_wheel (32), s4_lamp (32).

## 5. Open questions for the editor (don't guess; check the render)
1. **Rear "CRASH BAR" label**: clips.md says 'Rear bumper removed trunk closed' shows the crash bar. In my check still the
   lower rear bar is visible but partly hidden behind the exhaust. Add the label `REAR CRASH BAR` at n32.5-33.75 only if the bar reads
   clearly in v2_r_bumper's last frames; otherwise keep only `EXHAUST`.
2. **x_fbumper registration**: 4.8 mm median / 78 % overlap is above the ~3 mm guideline. The red overlay sat on the car in
   v1, and the part locks home in the finale in front of the camera, so check the lock frame of v2_x_home for a visible seam.
   If one shows, end the lock 1 frame later on car4np (the clean-car swap hides it).
3. **v2_s_side** shows comp_explode around the mirror and sill. If the 'Mirrors Removed' fill looks frayed at the mount, keep
   the camera on the part (move the target 0.1 m outboard) rather than on the mount hole.
