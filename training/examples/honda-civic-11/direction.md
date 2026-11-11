# Direction - Honda Civic FE1 Si scan reel, v2 (scene-director, stage 1)

Written 2026-11-11 from clips.md, project.yaml, editlog.jsonl, tools/shots.py, the v1 contact sheet
(`/home/user/media/work/civic/checks/final_sheet.jpg`), single frames of every v1 render, a silhouette-bounds pass
over s1/s5, the `ive director` report on v1, and the per-beat kick table of the track (tools/kicks.py).
User notes for v2 (relayed by the parent, 1-9 and A-D) are applied throughout; they override v1 and shots.py.
No feedback.jsonl exists yet for this project.

## 1. Feature inventory

| Region | Scans (registered?) | States | Parts | Signature features (seen in renders) | Weak data | Richness |
|---|---|---|---|---|---|---|
| Front | Full Car (base, 4 mm / 2 mm fl2 crop) | none (no hood-open scan) | none | headlights, hex-mesh grille + lower intake, front-left wheel w/ brake through the spokes | none seen | 2 (features only) |
| Left side | Full Car | none | none | both left wheels fully captured (rim + brake), mirror, shoulder line | none | 1 (hero wheels; flank is plain) |
| Right side | Full Car + **Door Open** (30 % within 6 mm, registered; sill + A/B/C jambs up to ~0.85 m, part of the cabin) | **doors open** (jambs/sill revealed) | front + rear door panels **cut from the full car** (outer skin only, no scanned inner face) | door jambs, sill, hinge/striker area | **right-rear wheel = tyre ring only**; Door Open has no data above ~0.85 m (check for black holes above the beltline) | 3 (state + 2 derived panels) |
| Rear | Full Car + **Trunk Open** (37 % within 6 mm, registered; lid hinge-fitted, skin p50 1.8 mm) | **trunk open** (real interior: floor, trim, wells) | trunk lid **from the Trunk Open scan** - real outer skin + inner trim + goose-neck hinges | decklid spoiler lip, tail lamps, CIVIC/H badges, exhausts | **licence plate legible** on the lid in s2/s5/s6/s7 (read "8SZK575"-like at 810 px) -> must be flattened; "Trunk Open no trim" exists but would imply a trim-removal state - not used | **4 (richest: real state + real part with real inner face + hinge)** |
| Top | Full Car | none | none | roof, sunroof-less panel | **hood + rear-glass holes were filled** (patched, not captured) | 0 (weak) |
| Engine bay | none | none (no hood-open scan) | none | - | no data | 0 - no scene |
| Bumpers | none (CHB rear bumper/lip = printed prototype, skipped) | none | none | - | - | 0 - no scene (note C) |

Not in this car's data, so not in the reel: hood open, engine bay, bumper removal, wheels off, separate registered part scans.

## 2. Scene order (travel front -> side -> rear, then reassemble)

Section column = the one section the shot covers (note B: each section appears in one continuous run only).

| # | scene | section | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | **N1_open** (NEW) | whole car | Full Car 4 mm | whole car, front-left 3/4, nose + left wheels | Note 4: open on the WHOLE car with motion. Front-left because the front carries the car's face and both best-captured wheels are on the left; the rear's strongest content is a *state* that belongs later on the ladder - opening on it would force rear -> front -> rear. v1 s1 clips the nose from frame 6 (silhouette touches x=0 for frames 6-113) and is a turntable, so it cannot be reused | 17 (quiet intro) | slow push + rise, <= 8 deg orbit, car whole with margin on every frame |
| 2 | **s3_wheel** (reuse, played reversed) | front (front-left wheel) | fl2 2 mm | rim spokes + brake caliper/disc | Front details sit next to the front wide; reversed, the camera slides forward along the flank toward the nose, leading into the lamp | 7 | as rendered, reversed |
| 3 | **s4_lamp** (reuse) | front (headlight / grille corner) | fl2 2 mm | headlight, grille mesh, lower intake | Ends the front section moving across the nose toward the car's right - the way we travel next | 7 | as rendered |
| 4 | **N2_doors** (NEW) | right side | Door Open state + door panels cut from Full Car | doors translate out; real jambs, sill, hinge/striker area underneath | Side section on THE DROP: the doors-open state is registered (note D). Doors only translate (inner faces are the full car's shell = no scanned data, note 5) | 11 (k31-k42) | close front-right 3/4 at door height, push toward B-pillar jamb |
| 5 | **N3_trunk** (NEW) | rear | Trunk Open state (trunk_base) + lid (Trunk Open, hinge fit) | lid opens on its fitted hinge, lifts off, inner trim + goose-necks face the camera, then the real interior | Richest region (state + real part with real inner face) gets the longest run and the drop section's k44 kick plus the k52 kick and the whole breakdown | 30 (k42-k72) | rear, slightly left of centre (right-rear wheel is weak), section fills the frame |
| 6 | **N4_reassemble** (NEW) | whole car | explode_base -> clean car4f at lock; doors + lid | doors and lid fly home, lock on the big kick, fade | Temerario ending: reassembly, fade, small logo. The one wide of all parts together - only for the return, never for the separation (note 2) | 16 (k72-k88) | high right-rear 3/4 (looks down ~45 deg, hides the weak RR wheel), whole car fills ~75 % width |
| 7 | logo | - | - | SMALL logo on black | note 7 | 6.5 beats to the end | remake card: current logo_card.mp4 is 79 % of frame width; target ~30 % |

Dropped: **s1_front34** (clipped nose, turntable), **s2_rear34** (rear-left orbit: rear section would appear twice, same
silhouette as s1 - IoU 0.74, legible plate), **s6_top** (rotating top-down = note 3; shows only the filled hood/rear glass;
IoU 0.64 with s5; plate visible), **s5_trunk** (camera fine but the plate on the lid is legible; folded into N3 so the rear is
one continuous sequence), **s7_explode** (one wide orbit with all panels separating at once - note 2; car ~60 % width in the
lower half with dead black above; plate legible; frames 91-165 black).
No top-down scene: the top has no state/part and its glass/hood are filled holes.

## 3. Music map (kick table measured with tools/kicks.py; grid t(k) = 0.2899 + 0.41794 k)

| cut | kick | t (s) | frame @30 | measured kick / broadband | lands |
|---|---|---|---|---|---|
| 0 | - | 0.000 | 0 | quiet pad | N1 opens (moving) |
| 1 | k17 | 7.395 | 222 | 0.0 / 0.00 (no hit measured - see Q1) | N1 -> s3 |
| 2 | k24 | 10.320 | 310 | 0.2 / 1.35 (riser accent) | s3 -> s4 |
| 3 | k31 | 13.246 | 397 | **85.1 / 4.04 DROP** | s4 -> N2 (front door moves on this kick) |
| - | k34 | 14.500 | (in shot) | 72.7 | rear door moves |
| 4 | k42 | 17.843 | 535 | 66.4 | N2 -> N3 |
| - | k44 / k52 | 18.679 / 22.023 | (in shot) | 85.3 / 71.7 | lid starts opening / lid lifts off |
| 5 | k72 | 30.381 | 911 | 12.3 (strongest accent in the k53-71 breakdown) | N3 -> N4 |
| - | k80 | 33.725 | (in shot) | **59.1 big kick** | doors + lid LOCK; base swaps to the clean car |
| 6 | k88 | 37.068 | 1112 | **72.8 big kick** | logo |
| end | - | 39.800 | 1194 | audio ends | - |

## 4. Diff against v1 (project.yaml)

| v1 | v2 | change |
|---|---|---|
| s1_front34 0-7.395 | N1_open 0-7.395 | **re-render** (whole car, no orbit) |
| s2_rear34 7.395-13.246 | - | dropped (rear duplicate, plate) |
| s3_wheel 13.246-15.336 | s3_wheel 7.395-10.320 | **reuse**, reversed, moved before the drop |
| s4_lamp 15.336-17.843 | s4_lamp 10.320-13.246 | **reuse**, moved |
| - | N2_doors 13.246-17.843 | **new** (side section on the drop) |
| s5_trunk 17.843-22.023 | N3_trunk 17.843-30.381 | **new** (merges trunk open + lid lift-off; deplated lid) |
| s6_top 22.023-26.202 | - | dropped (rotating top-down) |
| s7_explode 26.202-37.068 | N4_reassemble 30.381-37.068 | **new** (return + lock only; closer, deplated) |
| logo 37.068-39.8 | logo 37.068-39.8 | keep timing, **smaller logo card** |

Reused as-is (order/speed only): s3_wheel, s4_lamp. Everything else is forced to re-render by notes 2-4/A or the plate lesson.
New render budget: **481 frames at 15 fps** (N1 114 + N2 72 + N3 191 + N4 104) = ~96 min at ~12 s/frame, plus 3-frame 30 %
previews per shot. Details in director.md.

## 5. Open questions for the editor
1. **k17 has no measurable hit** (low band 0.0, broadband 0.00; the riser starts ~k20, accents at k24 1.35, k25 2.10, k28 1.33).
   The plan keeps k17 as you specified. If you'd rather cut on a real accent, the alternative is N1 0-k24 and s3 k24-k28,
   s4 k28-k31 (N1 then needs 8 more beats = +52 frames).
2. **Blank space above the door beltline.** Door Open only reaches ~0.85 m. If the 30 % preview of N2 shows black holes
   between the beltline and the roof rail once the doors are out, keep the camera framed on sill + lower jambs (top of frame
   at the beltline) - do not fill from the full car.
3. **Plate:** the lid's plate is legible. Flatten it on `lid.blend` (deplate as in infiniti-g35 / subaru-sti-blobeye) before
   N3/N4; check N3's first frame at full res.
4. The explode_base composite: confirm the trim lines are not visible after lock (N4 swaps to car4f + parts on k80 anyway).
