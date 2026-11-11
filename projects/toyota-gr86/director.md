# Director plan - toyota-gr86 v2 (stage 2 of direction.md; scene order unchanged)

Frame: Blender metres, car4 prep (`--like car4.json`). Nose -Y (y -2.13), tail +Y (2.13), ground z 0.19, roof z 1.43-1.47,
car's left = -X. Camera sensor 20.25 mm horizontal (shot.py default): at 30 mm, horizontal coverage = 0.675 x distance,
vertical = 1.2 x distance. Part `loc` = offset in m from home; `rot` = deg XYZ about the part's bbox centre (no `pivot`):
front bumper centre (-0.07, -1.818, 0.605), rear bumper centre (0.064, 1.817, 0.638), hood centre (-0.04, -1.25, 1.01).
All new shots: base `comp_explode.blend`, 75 % res, 12 spp, 15 fps, persistent data OFF, `seconds` = slot + 0.2
(3 spare frames for the minterpolate tail). Times below are LOCAL shot time (t=0 at the cut); absolute = local + start.
Bar = 2.449 s, beat = 0.612 s.

## Shot table

| section | shot | start-end (abs) | focus | camera (loc -> target, focal) | part action (local t) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | **A `a_open`** | 0.000-4.962 | whole car, front-right 3/4 | t0 (5.16,-7.67,1.35)->(0,-0.30,0.70) f30; t5.162 (3.54,-7.25,1.25)->(0,-0.45,0.70) f30, ease inout. Car 72 % -> 80 % of width, nothing clipped | none | establishes the car whole (user rule 4); motion from frame 1 (dolly-in + 8 deg arc, not a turntable) | NEW, 5.162 s = 78 f |
| front | **B `s3_headlight`** | 4.962-7.411 | right headlight, slat grille, intake | as rendered | none | the front's signature detail at 2 mm | REUSE s3 in 2.4 s (f_0037-f_0074), 1x |
| front | **C `d_front`** | 7.411-17.207 | hood off -> engine bay -> front bumper off -> front structure | K0 t0 (2.20,-4.90,2.00)->(0.10,-1.40,0.80) f30 (whole front end + right front wheel); K1 t2.449 (1.60,-4.00,2.70)->(0.05,-1.20,0.75) f30 (above the bay, hood seen from ABOVE leaving top of frame); K2 t4.898 (0.90,-3.30,2.50)->(0.00,-1.10,0.70) f32 (bay fills frame, ~1.9 m); K3 t7.347 (2.10,-4.70,1.70)->(0.10,-2.10,0.50) f30 (bumper low in front, structure exposed); K4 t9.996 (1.00,-3.60,1.20)->(0.00,-1.85,0.55) f30 (front structure ~1.45 m wide fills frame). ease inout between keys | **hood_m**: home 0-0.612; 0.612->2.449 loc (0,-0.10,1.20) ease out (lands 9.860); hold. **front_bumper**: home 0-5.510; 5.510->7.347 loc (0.30,-0.90,-0.45) rot (110,0,0) ease inout (lands 14.758: inner face turns up/toward the lens); 7.347->9.996 loc (0.30,-0.90,-0.42) rot (110,0,0). **rear_bumper**: home | the hero beat (user rule C): two real state scans revealed in order, each part moved into clear black space toward the lens/down, never across the body; bumper tipped only because its inside IS scanned | NEW, 9.996 s = 150 f |
| rear | **D `g_rear`** | 17.207-24.554 | rear bumper off -> rear bumper beam + exhaust | K0 t0 (2.30,5.00,2.00)->(0.00,1.50,0.80) f30 (whole rear + right rear wheel, ~2.9 m coverage); K1 t2.449 (2.10,4.80,1.70)->(0.10,2.10,0.50) f30; K2 t4.898 (1.00,3.60,1.20)->(0.05,1.95,0.50) f30 (beam + right exhaust fill ~1.37 m); K3 t7.547 (-0.60,3.50,1.10)->(-0.15,1.95,0.45) f32 (slide along the beam to the left tip). ease inout | **rear_bumper**: home 0-0.612; 0.612->2.449 loc (0.30,0.90,-0.45) rot (-110,0,0) ease inout (lands 19.656; inside faces up/back to the lens; min y clear of the body by ~15 cm); 2.449->7.547 loc (0.30,0.90,-0.42). **hood_m** (0,-0.10,1.20) hold; **front_bumper** (0.30,-0.90,-0.42) rot (110,0,0) hold (C's end pose) | second state-scan beat; rear-RIGHT keeps the holed left tail lamp small and at the top edge | NEW, 7.547 s = 114 f |
| top | **E `s_stack`** | 24.554-31.901 | the three removed parts as one layered stack over the opened car | K0 t0 (0.30,1.30,7.30)->(0,-0.10,0.80) f34 (near top-down, nose UP in frame, 6.9 m vertical coverage > 6.15 m part span); K1 t2.449 (0.50,1.60,7.00)->(0,-0.10,0.85) f36; K2 t7.547 (1.80,4.60,4.60)->(0,-0.20,1.00) f36 (high rear-right ~35 deg down, layers read; ~3.5 m horizontal coverage vs ~2.6 m car) ease inout | **front_bumper**: 0 (0.30,-0.90,-0.42) rot (110,0,0) -> 2.449 (0,-0.50,0.78) rot 0 inout. **rear_bumper**: 0-0.612 (0.30,0.90,-0.42) rot (-110,0,0) -> 2.449 (0,0.50,0.78) rot 0 inout. **hood_m**: 0 (0,-0.10,1.20) -> 2.449 (0,-0.10,1.22). Then all drift to t 7.547: hood (0,-0.10,1.253), bumpers (0,+-0.50,0.803) - exactly s7's poses at its f111, so F continues the stack | the top rung shows something new: the layout of every removed part; the end poses hand over to the existing reassembly render | NEW, 7.547 s = 114 f |
| whole | **F `s7_explode` tail** | 31.901-36.799 | reassembly of the whole car | as rendered (high front-right) | as rendered: drift, all home at s7 t 9.796 = **34.350**, settle | the payoff on the loud return; then fade to black 36.30-36.80 | REUSE s7 f_0111-f_0185 (in 7.347 s), 1x |
| end | **G logo** | 36.799-39.248 | ILLUMAESTHETIC logo | static, small | fade in 36.80-37.30 | Temerario ending | remake card with logo ~30 % of frame width |

Absolute check: C hood lands 7.411+2.449 = **9.860**; C bumper lands 7.411+7.347 = **14.758**; D bumper lands
17.207+2.449 = **19.656**; E stack formed 24.554+2.449 = **27.003**; F parts home **34.350**.

## Labels (ScanHUD `label`, Inter Display, #e8ecf2, top band y 160-320 px, 80 px inside edges, outside the silhouette; enter on a beat, leave before the cut; max one on screen)
| text | over | in -> out (abs) |
|---|---|---|
| `FRONT BUMPER + HOOD REMOVED` | C (K3->K4 push-in on the front structure) | 15.064 -> 16.950 |
| `REAR BUMPER REMOVED` | D (K1->K2 push-in) | 19.962 -> 21.850 |
| `REAR CRASH BEAM` | D (K2->K3 slide along the beam) | 22.411 -> 24.300 |
Wording comes from the Drive state-scan names (`Bomex Bumper Hood Removed`, `Bomex Rear Bumper Removed`) and the
holed full-width beam visible in `reg/states/Rear_Bumper_Removed.png`. No numbers. Confirm the beam is in frame on D's
t 4.9 still before keeping label 3.

## Cut list (from v1)
- s1_front34: tail cropped (not a whole-car opener), turntable; same view as s2 (`ive director` IoU 0.75).
- s2_rear34: orbit, nose cropped, broken rear tyre; side section has no state/part data.
- s4_tail: black scan hole on the left tail lamp in every frame; also ~s3 (IoU 0.87).
- s5_hood: hinge swing of the closed hood skin = faked opening (open hood never captured); its first 0.6 s re-showed the whole car.
- s6_top: rotating intact top-down, nothing new.
- s7 f1-110: all parts off at once in one wide orbit + 2.4 s dead frames (`ive director`).
- C/D/E have no rotation-for-its-own-sake: every camera move goes TO a subject (bay, structure, beam, stack).

## Hold list (> 0.75 s)
- C 7.411-8.023 (0.61 s, below threshold) whole front before the hood moves - camera already moving.
- C 9.860-12.921: no part moves (3.1 s) - camera travels over the real Hood Open engine bay to read it (K1->K2).
- C 14.758-17.207: bumper parked (2.45 s) - push-in to read the exposed front structure + label (user rule C: hold long enough).
- D 19.656-24.554: bumper parked (4.9 s) - push-in then slide along the rear beam/exhaust + two labels.
- E 27.003-31.901: parts drift only (+3 cm) - camera cranes from top-down to the layered 3/4.
- F 34.350-36.799: settled car (2.45 s incl. 0.5 s fade) - the assembled payoff on the loud return.
- G 2.45 s logo.

## Render budget (15 fps, 75 %, 12 spp, ~12-16 s/frame)
| shot | frames | ~time |
|---|---|---|
| C d_front (render first: hero) | 150 | 30-40 min |
| D g_rear | 114 | 23-30 min |
| E s_stack | 114 | 23-30 min |
| A a_open (car4 only, faster) | 78 | 12-20 min |
| pre-checks: C stills t2.45/t4.9, D still t4.9, E still t7.5 | 4 | 1 min |
| **total new** | **~460** | **~1.5-2 h** |
Reused unchanged: s3 f37-74; s7 f111-185 (s7 must finish to f186 first; luma-check every frame of every shot).
First/mid/last frame of every shot: check that nothing is clipped (wheels, bumpers, roof, parts) and no dead black on
the subject (cowl holes in C, left lamp in D).
