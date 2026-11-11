# Toyota Sera - scene direction (v3)

Scene-director stage (.claude/agents/scene-director.md). Inputs read: lessons.md (all), style-guide.md, clips.md,
project.yaml, editlog.jsonl, review.md, director_report.md, tools/shots.py + shot.py, prep/*.json bboxes, hinge jsons,
contact sheets sheet_v1 / sheet_s5_hood / sheet_s6_doors / sheet_s8v2, reg/ front_bumper_alone, front_bumper_removed_alone,
rear_bumper_only_alone, fb_sheet, rear_sheet, explode_base_fr/rl. v2 brief (parent session, 9 points) applied throughout.
Stage 2 (shot specs, camera numbers, part keys) is in `director.md`.

## 1. Feature inventory (this car's scans)

Scan frame: nose -Y, car's right -X, ground z 0. Car bbox x +-0.86, y +-1.92, z 0.02-1.26 m.

| Region | What the data holds | States (registered, this car) | Parts (registered) | Signature | Weak data | Richness |
|---|---|---|---|---|---|---|
| Front | nose, headlamps, Toyota badge, front wheel | 'front bumper removed' (crash bar, radiator support, lamps; 0.8-1.3 mm); 'Hood open' (real engine bay) + fitted hood hinge (-X axis, 56 deg, 1.5 mm) | 'front bumper' part 3.0 mm, inner face scanned (reg/front_bumper_alone.png) | - | grille/vent black plastic = scan holes (s4_nose shows them); a few hood specks | **5 (richest)**: 2 states + 1 part + hinge |
| Front wheel | tyre tread, 6-spoke rim, centre badge - detailed | - | - | - | none seen (s3_wheel sheet) | 2 |
| Side | butterfly doors, canopy glass line, interior | 'Door Open' (BOTH doors open; real interior + door openings) + 2 fitted hinges (+-0.60,0.68,0.41), 56/-57 deg, 1.05 mm | door / door2 panels (outer skin + captured trim) | **yes - butterfly doors + glass canopy** | door inner face is thin (29-39k inner tris): show the swing and the cabin, not the door's back | 4 |
| Rear | tail, spoiler, tail lamps | 'rear bumper removed' (rear panel structure, lamp housings; reg/rear_sheet.jpg) | 'rear bumper only' part 3.1 mm, inner face scanned (reg/rear_bumper_only_alone.png) | spoiler (stays on: 'spoiler removed' is patchy) | **no hatch-open capture** (state max z ~0.92 m) - hatch never opens; plate holder on the rear panel (blank) | 3 |
| Top | canopy roof | - | - | canopy | rotating top-down showed nothing new (v2 s7) | 1 |
| Engine bay | real 'Hood open' data | (front region) | - | - | - | counted in Front |
| Not usable | 'light' (fragments), 'steered right' (partial), underbody halves (not fetched), Low Definition (dup) | | | | | 0 |

## 2. Scene order (travel front -> side -> rear, then the progressive explode)

| # | scene | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | Whole car | car4 | entire car incl. canopy, front-right 3/4 | brief 4: whole car, motion from frame 1; front-right 3/4 opens the travel at the front | 8 (b0-8) | push-in 7.2 -> 6.3 m with 12 deg drift, car 79-84 % width |
| 2 | Front wheel ECU | car3 (reuse s3_wheel) | tyre + rim + centre badge, slides to the nose | wheels are clean, detailed data; front corner = next step of the travel | 4 (b8-12) | existing render |
| 3 | Front section | front_base + hood_panel + front_bumper_3mm | hood opens -> engine bay; bumper pulls toward camera, tips to show its inner face over the exposed crash structure | richest region (2 states + part + hinge) -> longest scene, hood fully open ON the 9.635 phrase downbeat | 12 (b12-24) | ONE held shot, high front-right, moves in to the bumper |
| 4 | Side - butterfly doors | doors_base + door/door2 panels | both doors swing up, cabin revealed | signature feature; side = middle of the travel; real 'Door Open' interior | 8 (b24-32) | side-on (right), drifts rearward and in |
| 5 | Rear section | rear_base + rear_bumper_only_3mm | rear bumper slides back toward camera, tips to show its inner face; rear panel structure behind | rear part + state; continue the travel to the tail. Hatch stays shut (no data) | 8 (b32-40) | low rear-right -> high straight-behind |
| 6 | Progressive explode, 3 angles | explode_base + 5 panels; car4 for the final second | G1 front assembly lifts (front-left) -> G2 doors + rear bumper lift (left side) -> G3 everything flies home, lock, clean car, fade (rear-left) | brief 7 (Temerario progressive explode over several angles); the explode re-travels front -> side -> rear on the LEFT side (never shown before) | 20 (b40-60) | each angle frames its own assembly, not one wide orbit |
| 7 | Logo | logo card <= 480 px wide | - | brief 7: small logo, short | b60-end (3.27 s, fades with the decay) | static |

Dropped: top-down (s7: rotating, nothing new - brief 3), nose/grille slide (s4: grille holes; the nose is covered by scene 3),
rear turntable in slot 2 (s2: ping-pong front->rear->front).

## 3. Music map (kick grid t = 0.0355 + 0.59999 n; phrases every 8 beats)

| beat | t (s) | frame @30 | event |
|---|---|---|---|
| 0 | 0.036 | 0 | scene 1 starts moving |
| 8 | 4.835 | 145 | phrase (bass up) - cut to wheel |
| 12 | 7.235 | 217 | cut to front section |
| 16 | 9.635 | 289 | phrase: hood fully open, bumper starts out |
| 24 | 14.435 | 433 | phrase: cut to doors (open b25-29) |
| 32 | 19.235 | 577 | phrase: cut to rear section |
| 40 | 24.035 | 721 | phrase: explode starts (G1), hood lifts on the downbeat |
| 42-46 | 25.2-27.6 | - | kick break: front panels float, no cut inside the break |
| 46 | 27.635 | 829 | kicks return: cut G2 (doors lift) |
| 52 | 31.235 | 937 | cut G3, reassembly starts |
| 56 | 33.635 | 1009 | phrase: last panel LOCKS; base swaps to clean car4 on this kick (same camera) |
| 58-60 | 34.835-36.035 | 1045-1081 | fade to black |
| 60 | 36.035 | 1081 | logo fades in (small) |
| 64 | 38.435 | - | music stops; logo fades with the decay; end 39.30 s (frame 1179) |

## 4. Diff against v2 timeline

| v2 clip | v3 | why |
|---|---|---|
| s1_turntable | **replaced** by new S1 whole-car push | cropped (r 3.9 m); a turntable (brief 3, 4) |
| s2_rear | **dropped** | rear in slot 2 = ping-pong (brief 1); rotation that shows nothing new; rear now = scene 5 |
| s3_wheel | **reused unchanged**, moved to slot 2, 2.4 s | right content and framing; front corner |
| s4_nose | **dropped** | grille scan holes; nose subject merged into front section |
| s5_hood | **merged** into new S3 (hood + bumper in one held shot) | brief 2: stay on the section; v2 s5 ~ s1/s6 repeated view |
| s6_doors | **re-rendered** side-on | v2 front-right 3/4 repeats S1/S3's view (report: s1~s6, s5~s6) |
| s7_top | **dropped** | rotating top-down, nothing new (brief 3); report s6~s7 |
| s8_explode(_v1) | **replaced** by G1/G2/G3 | all panels at once in one wide orbit (brief 2, 7) |
| logo 760 px, 4.47 s | 480 px, 3.27 s | brief 7 |

New renders: S1, S3, S4, S5, G1, G2, G3a, G3b = 525 frames at 15 fps (~1.5 h). New bases: `front_base`, `rear_base` (see director.md).

## 5. Open questions for the editor (don't guess - check and log)
- Rear base: the rear panel carries a (blank) plate holder from the state scan - confirm it is not legible at the S5 end framing.
- `front_base` fill order: 'Hood open' was captured with the front bumper ON - keep the KEEP_OUT rule from explode_base.py
  so its bumper does not ghost in front of the crash structure; check a still at S3 t=7.2 s.
- If the tipped front bumper's top edge still overlaps the nose structure at S3's last frame, raise the camera (more top-down),
  don't move the bumper sideways across the body.

## Revision for the user's addendum (2026-11-11) - implemented by the editor
Addendum: crops deliberate; each section in ONE continuous sequence; bumper-removed data is the hero beat (bumper comes
off, camera moves in on what is behind it, holds, short factual label); openings only from real state scans.
Changes against the plan above: G1 (front lift) and G2 (side/rear lift) re-showed the front and side sections and cropped
the car, so they became ONE progressive whole-car explode (E1) with the whole car in frame. The front and rear sections
get longer and end close on the bumper-removed structure, and the doors section shrinks to 6 beats.

| shot | beats | section (only here) | scans | label |
|---|---|---|---|---|
| v3_s1_whole | 0-8 | whole car (exterior, front-right 3/4) | full car 4 mm | - |
| s3_wheel | 8-12 | front-right wheel | full car 3 mm | - |
| v3_front | 12-28 | FRONT: hood/engine bay, front bumper + inner face, structure behind the bumper | front_base (front-bumper-removed + hood-open states), hood panel, front bumper part | FRONT BUMPER / INNER FACE · 1,800,000 TRIANGLES; FRONT BUMPER REMOVED / 1,999,999 TRIANGLES |
| v3_s4_doors | 28-34 | SIDE: butterfly doors + cabin | doors_base (Door Open state), door panels | - |
| v3_rear | 34-44 | REAR: rear bumper + inner face, structure behind the bumper | rear_base (rear-bumper-removed state), rear bumper part | REAR BUMPER / INNER FACE · 4,999,998 TRIANGLES; REAR BUMPER REMOVED / 1,500,000 TRIANGLES |
| v3_e1_explode | 44-52 | whole car, every scanned panel lifting in turn | explode_base + 5 panels | - |
| v3_g3a_home + v3_g3b_clean | 52-60 | reassembly -> clean car -> fade | explode_base + panels, then full car | - |
| logo | 60-end | - | - | (small logo) |
No section appears twice: the front corner (wheel) sits next to the front section, the side is shown once (doors), the rear
once, and only the explode and reassembly show the whole car again, as one continuous sequence. No trunk/hatch shot:
there is no hatch-open scan.
