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

## v4 (Epsilon)

Written 2026-11-12 (scene-director). Inputs: v3 timeline/review, feedback.jsonl (v3: "logo takes too long, whole video paced
too slowly ... turn this into an epsilon video ... once the parts are opened up, we install the front lip, side skirts, rear
apron, new wheels, and the rear wing through the scan data. then end the video with one of the render shots Ron has"),
frames of every reusable render (N1, s3_rev, s4, N2_m, N3_m, N4_m), Ron's render sheet + render 1 at full size,
checks/kit_fit.png, and a fresh onset measurement of the track. Nothing was rendered.

### 0. Music finding that changes the map (measured, 1 ms RMS half-rise within 60 ms before the peak)
The v1-v3 "kickless breakdown k53-k79" does not exist. The track's real bar is **3.31 s (8 beats at ~145 BPM, not 143.56)**;
the 143.56 grid drifts up to 0.15 s after 22 s, so `kicks.py`'s +-40 ms windows missed the hits. Every bar from the drop has
the same four equally strong hits at +0 / +1.5 / +3 / +5 beats (a b c d). "k42", "k72", "k80", "k88" are b/c hits, not downbeats.

| bar | a (downbeat) | b | c | d |
|---|---|---|---|---|
| pre | 10.370, 10.785, 12.026, 12.855 (light, high-band hits; no kick) | | | |
| B1 | **13.295 DROP** | 13.916 | 14.542 | 15.358 |
| B2 | 16.600 | 17.216 | 17.851 | 18.675 |
| B3 | 19.923 | 20.529 | 21.159 | 21.996 |
| B4 | 23.227 | 23.848 | 24.469 | 25.100 (+25.299) |
| B5 | 26.521 | 27.171 | 27.783 | 28.612 |
| B6 | 29.847 | 30.454 | 31.088 | 31.920 |
| B7 | 33.161 | 33.800 | 34.408 | 35.241 |
| B8 | 36.471 | 37.086 | 37.707 | 38.323 (+38.530) |

Audio is gone at 39.80 s. Usable cut spacings: a->d 2.07 s (5 beats), d->a 1.24 s (3), d->c' 2.48 s (6), c->a' 2.06 s (5).

### 1. Where the video starts
**Audio in-point 12.026 s** (the hit 3 beats before the drop). Video = 27.77 s (833 frames). The whole car gets 1.27 s, the
first transformation (doors) is ON the drop at 1.27 s. v3 sat 13.3 s on the intro; lessons: start ~2 hits before the drop.
Video frame = round((t - 12.026) * 30).

### 2. Inventory additions (v4)
| Region | New data | Registered? | Richness note |
|---|---|---|---|
| Front | Epsilon front_lip (lookbook eps-honda-civic-sedan-fe-facelift-v9) | ICP to scan, median 10 mm (model, not a scan of this car) | 1 part |
| Sides | side_skirts L+R | same | 1 part; reads only from a low grazing view |
| Wheels | new wheels L+R (gold rims, tyres, brakes) + scanned wheels as separate parts + car_nowheels | same | richest install: 2 actions (off / on); **left side has both scanned wheels complete, right-rear is a tyre ring** |
| Rear | rear_lip (apron), sport_wing (on the lid) | same | 2 parts = two shots in one continuous rear run |
| Ending | Ron render 1 (front-right 3/4, whole car, 1920 sq, pure black top/bottom rows; car bbox x 283-1685, y 746-1250) | camera being solved by the editor | 1:1 cut target |

The kit parts are CAD from the lookbook, not scan data: no labels claiming "scanned", and no specs.

### 3. Doors / trunk during the installs: CLOSED (recommendation)
Order: open doors -> open trunk -> look in -> close (existing N4_m, slam on a kick) -> installs on the closed car.
Reasons: (a) the wing is fitted to the closed lid; on a lid standing at 94 deg it would point at the sky and cannot seat where
the render shows it. (b) Skirts sit under the doors: the open doors (64-68 deg) hang over the sill, and any view that sees the sill
past them looks at the doors' inner faces, which have no scan data (v3 review). (c) The end is a 1:1 cut to a closed car.
(d) All kit assets (car_nowheels, parts) are built on the closed full car; an open-state no-wheels base does not exist.
(e) The closing costs no render time and gives the installs a clean starting state. I read "once the parts are opened up" as
sequence (after the opening section), not as "while open" - see open question 1.

### 4. Scene order (travel: whole -> right side -> rear -> [close] -> front -> left side -> rear -> front-right hero)
Kit accumulates: every part stays on in all later shots (lip from shot 7 on, gold wheels from 9, skirts from 10, apron from 11,
wing from 12). Install shots use car_nowheels + wheels at home (scanned wheels until shot 9, new wheels after).
User's list order was lip, skirts, apron, wheels, wing; I moved wheels next to skirts so side and rear are each ONE run
(rule B / travel). Wing stays last. Each install is self-contained, so the order can be swapped without re-rendering only if
the accumulated parts in frame still match (wheels<->skirts swap needs both re-rendered).

| # | id | section / single focus | source | track in-out (s) | dur s / frames | cut-in hit | part motion | camera |
|---|---|---|---|---|---|---|---|---|
| 1 | N1 | whole car (stock scan), front-left 3/4 | reuse final/N1_open f68-105 played 1:1 at 30 fps (= 3x; no minterpolate) | 12.026-13.295 | 1.27 / 38 | audio start (hit 12.026) | none | as rendered: push + rise, car 70-71 % of width, whole |
| 2 | N2 | right side: doors open on hinges | reuse final3/N2_m f3-64 | 13.295-15.358 | 2.06 / 62 | **B1a DROP** | front door from the drop (open by +0.8), rear door on B1c (14.542), fully open 1-2 frames before the cut | as rendered (front-right, door height) |
| 3 | N3 | rear: trunk lid opens on its hinge | reuse final3/N3_m f26-100 (skip the 0.84 s closed hold) | 15.358-17.851 | 2.49 / 75 | B1d | lid starts on the cut, open at +2.09, 0.4 s open | as rendered (rear, slightly left) |
| 4 | N3b | rear: trunk interior (Trunk Open scan) | reuse final3/N3_m f271-332 (later window of the same move = a cut-in, no frame used twice) | 17.851-19.923 | 2.07 / 62 | B2c | none (lid stays open) | as rendered: tail fills the width, pushes toward the interior; stop before the last 1.5 s (ragged floor data) |
| 5 | N4 | whole car: doors + lid close | reuse final3/N4_m f41-102 | 19.923-21.996 | 2.07 / 62 | B3a | rear door, front door, lid close; all shut ~2 frames before the cut (verify the shut frame, slide the window if needed) | as rendered (high front-right wide) |
| 6 | s4 | front: headlight / grille / lower bumper, stock ("before" for the lip) | reuse final/s4_lamp (15 fps, trim_start ~0.6, interpolate) | 21.996-23.227 | 1.23 / 37 | B3d | none | as rendered, slides across the nose |
| 7 | I1_lip | front: FRONT LIP install | **NEW** | 23.227-25.100 | 1.87 / 56 | B4a | lip starts 0.45 m ahead (+Y) and 0.15 m low, in black, moving from frame 1; seats ON B4b (+0.62, ease out); hold 1.25 s (trimmable) | low front, ~15 deg to the car's left, h ~0.45 m, focal 35: bumper width = ~85 % of frame width, lip in the lower-middle third, hood line at top. Push ~6 %. Start r ~3.0 m from the nose, check first/mid/last |
| 8 | s3 | left side: stock front-left wheel + brake ("before" for the wheels) | reuse final/s3_wheel_rev f1-23 (15 fps, interpolate; these frames show wheel + arch only, no bumper corner, so the missing lip cannot be seen) | 25.100-26.521 | 1.42 / 43 | B4d | none | as rendered |
| 9 | I2_wheels | left side: WHEEL swap (both left wheels) | **NEW** (car_nowheels + scanwheels_L/R -> rims/tyres/brakes) | 26.521-28.612 | 2.09 / 63 | B5a | scanned wheels pull straight outboard (-X) 1.0 m from the cut and keep going out of the bottom of frame (hide when out); new wheels are in frame by B5b (27.171), slide in along the axle and seat ON B5c (27.783, +1.26); hold 0.83 s (trimmable) | car's LEFT, ~65 deg off the nose, elevated ~30 deg so "outboard" reads as down-screen into clear black (not at the lens, not across the body). Frame = front arch to rear arch + margin (bumpers cropped on purpose), wheels in the middle third, black below for the travel. Right-side wheels swap at the same time (seen through nothing, but must match later shots) |
| 10 | I3_skirt | left side: SIDE SKIRT install | **NEW** | 28.612-31.088 | 2.48 / 74 | B5d | skirt hovers 0.40 m outboard / 0.05 m low beside the sill in black, creeping in (~10 %) for 0.8 s, then snaps home in 1 beat, seated ON B6a (29.847, +1.24); hold 1.24 s. Hover and hold are both trimmable | low grazing front-left: cam ~(-2.3, 3.2, 0.35) looking back along the sill to (-0.95, -0.3, 0.30), focal 35; sill runs diagonally through the frame, gold front wheel big at the left edge, outboard side of the image is clear black. Glide 0.3 m rearward along the sill. (A side-on view loses the skirt against the door - gt3 lesson) |
| 11 | I4_apron | rear: REAR APRON install | **NEW** | 31.088-33.161 | 2.07 / 62 | B6c | apron starts 0.45 m behind (-Y) and 0.15 m low; seats ON B6d (31.920, +0.83); hold 1.24 s | low rear-left 3/4 (~20 deg off the tail to the left, h ~0.5 m, focal 35): bumper width ~85 % of frame, apron + exhausts in the lower-middle third, lid edge at top; left gold rear wheel at the frame edge. Push ~6 %. Right-rear wheel stays out of the centre |
| 12 | I5_wing | rear/top: REAR WING install | **NEW** | 33.161-35.241 | 2.08 / 62 | B7a | wing starts 0.6 m above its seat (+Z, slightly rearward), in black above the lid; drops and seats ON B7b (33.800, +0.64, ease out; no spin); hold 1.44 s | rear-RIGHT 3/4, raised (h ~1.9 m, ~35 deg off the tail to the right, focal 35): lid + wing + rear glass fill the width, tail lamps at the bottom third, free black above for the drop. Slow rise/push 6 %. Leads round to the right side for the hero |
| 13 | W_kit | whole car, all kit, front-right 3/4 (Ron render 1 camera) | **NEW**: one still per layer from the solved camera on the render's square canvas + shared Ken Burns (kenburns.py pattern) - 1 render frame | 35.241-36.471 | 1.23 / 37 | B7d | none (all parts home) | exactly Ron's camera. 9:16 window: scale the 1920 sq to 1296 px, centre crop 1080 wide, black pad above/below (render rows 0 and 1919 are pure black, so no seam): car 946 px = 87.5 % of width, y ~816-1156. Push 1.000 -> 1.022 |
| 14 | R_ron | Ron render 1 (white car, full kit, gold wheels) | ron/render/1FinalSedanFL.jpg, same window | 36.471-39.800 | 3.33 / 100 | **B8a downbeat: hard 1:1 cut** | none | same Ken Burns continues at the same rate, 1.022 -> 1.08 (car locked across the cut) |
| - | wordmark | Epsilon+ wordmark (white, Drive "EPSILON+ Logos") | overlay on shot 14 only, not scaled by the push | 38.323-39.800 | 1.48 / 44 | B8d (in ON the hit, 4-frame fade) | - | ~300 px wide (28 % of frame), centred, y ~1370 (black under the car, above the bottom caption zone at 1536). Fades out with the picture + music over the last 0.5 s. No Illumaesthetic logo anywhere |

Cut frames @30 (from video start): 38, 100, 175, 237, 299, 336, 392, 435, 498, 572, 634, 696, 733; wordmark 789; end 833.
Clip lengths: 38, 62, 75, 62, 62, 37, 56, 43, 63, 74, 62, 62, 37, 100. Use concat_assemble (exact `frames:`) and verify
each cut against the decoded audio (|err| <= 1/2 frame); rounding errors above are -16..+16 ms.
14 shots, mean 1.98 s, longest scan shot 2.49 s. The render holds 3.33 s but has the wordmark event at +1.85 s.

Sections (rule B): whole (1) | right side (2) | rear, opened (3-4) | whole, closing (5) | front (6-7) | left side (8-10) |
rear, kit (11-12) | whole + render (13-14). The rear appears twice on purpose: once as the scan's Trunk Open state, once as
the product install after the car is shut; they are separated by a state change, not a repeated view. Same for whole-car
wides 1 / 5 / 13 (front-left stock, high front-right closing, front-right with kit). Log this for the `ive director` flags.

### 5. New footage and re-timing rules
- New screen time: 1.87 + 2.09 + 2.48 + 2.07 + 2.08 = 10.6 s of animation (159 frames at 15 fps + 3 tail frames per shot
  = ~174, ~58 min at 20 s/frame) + true 30 fps in-betweens for the part-motion windows only (~4 s total, ~60 frames, ~20 min;
  minterpolate smears fast part moves - civic lesson) + 2 stills for shot 13. Under the 15 s budget.
- Every install is built as: [optional hover] -> move <= 1 beat (<= 0.6 s) -> hold. Render the table's length plus 0.2 s.
  If the user's replacement track arrives, re-time by trimming holds/hovers and shifting the clip so the SEAT frame sits on a hit. Seat frames (clip-local): lip 19, wheels 38
  (old wheels clear by 19), skirt 37, apron 25, wing 19.
- Persistent data OFF for all five installs; per-frame luma scan; first/mid/last contact sheet + edge-touch test per shot (rule A).
- Kit parts gloss black, rims gold on the silver scan as planned (they must read against silver). No labels: the parts are
  named by the picture; if labels are wanted later, use only FRONT LIP / SIDE SKIRTS / REAR APRON / WHEELS / REAR WING in black.

### 6. Diff against v3
| v3 | v4 | change |
|---|---|---|
| N1 0-10.37 (10.3 s) | N1 1.27 s | reuse, last 38 source frames at 3x |
| s3 wheel, s4 lamp before the drop | s4 before the lip, s3 before the wheels | reuse, moved: each is now the "before" of its install |
| N2 4.57 s | 2.06 s | reuse, trimmed to the two door swings |
| N3 12.6 s | N3 2.49 s + N3b 2.07 s | reuse, two non-overlapping windows |
| N4 6.63 s + baked fade | N4 2.07 s, closing only | reuse N4_m (not N4_fade30), no fade |
| Illumaesthetic logo 2.73 s | dropped | Epsilon+ wordmark 1.48 s over Ron's render |
| - | I1-I5, W_kit, R_ron | new |

### 7. Open questions (not decided here)
1. **Closed vs open during installs** is my reading of the user's sentence. If the user wants parts going on while the doors
   and trunk are open, only the lip and wheels can be done honestly (needs an open-state no-wheels base); skirts and wing
   still need the car shut. Ask before rendering if in doubt.
2. **Kit colour vs the render**: in render 1 the lip, skirts, apron and wing are body-colour white; the scan shows them gloss
   black. At the 1:1 cut the parts change colour with the car. Acceptable to me (everything changes material on that cut), but
   it is a visible difference - confirm, or render the kit in the scan's silver with a darker tint for shot 13 only.
3. **Part versions**: confirm front_lip / sport_wing / rear_lip / wheel design in the v9 lookbook model are the ones in Ron's
   render (QX80/GR Corolla lesson: lookbook models carry several versions). kit_fit.png looks consistent for the wing; I could
   not verify the lip and apron versions from it.
4. **Order of installs** differs from the user's list (wheels moved before the apron). Say so in the delivery note.
5. **Grid**: project.yaml's 143.56 BPM grid and the "k" numbers should be retired for this track; use the bar table above.
   If the user's replacement track arrives, re-measure and re-map; shot content does not change.
6. Shot 9 exit path for the scanned wheels (down-screen and out) needs a 30 % preview: if the empty arches read as the
   subject for more than ~0.3 s, start the new wheels earlier so both sets are in frame together.
7. Shot 13 depends on the render-1 camera solve; verify with an onion overlay (silhouette), not the score. If the solve
   cannot get wheels and roof within a few px, cut on the best-aligned region (front wheel + nose) and keep the push.
