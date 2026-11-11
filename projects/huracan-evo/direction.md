# Huracan EVO - direction (v3 HP, revision 2026-11-11)

Scene-director (stage 1) + director (stage 2) in one file. Fixed by the user and NOT changed here: HP car-select opening on the
COUPE, start-up 0.3 s, hush, narration 4.3-39.2 s, `vo/soundtrack_v3hp.wav`, beats `t = 3.0768 + 0.60006*n`, lift n=64 (41.481 s),
music stop n=108 (67.883 s), tail to 71.85 s. h0 stays first (n0-3). Logo after n108 as now.
Frame: prepped Spyder frame, ground z=0, nose -Y (y=-2.253), car's right = -X. Camera az: 0 = in front of the nose, -90 = car's
right (-X), +-180 = behind. **az is interpolated numerically**: a path that crosses behind the car must keep going past -180
(write -210, not +150).

## 1. Feature inventory (from clips.md, the blend/*.json bboxes and the contact sheets I looked at)
| region | coupe 2023 (`coupe2_np`, 2 mm) | Spyder 2026 (`base` + parts, 2/3 mm) | richness |
|---|---|---|---|
| front | nose, intakes, shield on hood; windscreen glass = holes (visible at el < ~45 deg) | **front bumper** part (inner 25 %), **hood** part on fitted hinge (inner 50 %), **3 cowls** under the hood (top surface only, 0-1 % inner -> translate only), APR structure under all of them | **richest (5 parts + hinge state)** |
| wheels | **rims captured** (spokes read) | hollow (tyre rings only); Front Wheel Wells state (disc/caliper/hub) exists but only as `fww_zone` spliced into `car_nowheelzone`, not into the exploded base | coupe only |
| side (-X) | side slide; door/quarter glass holes | **fender** part (inner 31 %), **side skirt** part (inner 31 %), one side only (-X) | 2 parts |
| top | roof/windscreen = biggest glass holes (h6 frame) | soft top -> engine-deck step | weak |
| rear | tail lights, louvres, exhausts, diffuser; plate removed (flat dark rectangle) | **rear bumper** part (inner 29 %, plate removed `_np`) | 1 part |
Inner-face shares are the coordinator's measurement (normals facing into the car vs out) - a tip toward the lens is earned
for both bumpers, fender, skirt, hood; cowls never flip.

## 2. Coupe section n0-64 (re-ordered: front -> side -> rear, one continuous direction of travel)
Dropped: **h6_high** (high 3/4 over the roof). Why: it is the only angle whose subject is the roof/windscreen, where the coupe
glass is unscanned - the framing test shows the holes mid-frame - and it is a third whole-car 3/4 after h0 and before h7
(redundant view). Its 9 beats go to the four remaining 9-beat angles (+2 each -> 11) and h1 (+1 -> 10): 3+11+11+11+11+10+7 = 64.
Angles at 11 beats = 6.6 s, which is the HP reference's ~6.5 s cadence.

| # | shot | n | t (s) | focus | camera change vs current CAMS (pre-render, zero cost) | render |
|---|---|---|---|---|---|---|
| 1 | h0_select | 0-3 | 0-4.877 | whole car, lights up | none | reuse as rendered (73 fr) |
| 2 | h2_front | 3-14 | 4.877-11.478 | nose + intakes, low | none (az -42 -> -26 already sweeps toward the nose; h3 continues the sweep) | render 99 fr (11 beats native) |
| 3 | h3_hood | 14-25 | 11.478-18.078 | down the hood to the shield | **blocker:** the re-framed test (`framing_hp3/chk.png`) still shows the windscreen holes across the top ~25 % of frame. Raise el to >= 48, target [0,-1.85,0.62], lens 70; check one frame at 30 % before the full render | render 99 fr |
| 4 | h4_wheel | 25-36 | 18.078-24.679 | front-left wheel (real rims) | reverse the az sweep: 60 -> 76 (moves rearward, toward h5); keep dist 1.7 -> 1.4 | render 99 fr |
| 5 | h5_side | 36-47 | 24.679-31.280 | left side slide | reverse the slide: target y -1.1 -> +1.1 (front -> rear, into h1) | render 99 fr |
| 6 | h1_tail | 47-57 | 31.280-37.280 | left tail light + louvres | none (az 150 -> 164 keeps travelling) | the job running now (81 fr), stretched 9 -> 10 beats (src_fps = 80/(6.0+0.1)) |
| 7 | h7_rear | 57-64 | 37.280-41.481 | wide rear 3/4 (crossing behind to the right) | none (164 -> 180 -> -150 -> -144 is one direction) | render 63 fr |
Dips to black 0.6 s between angles as now; hard cut at the lift. In `shots.py` HP_BEATS becomes
`h0 0-3, h2 3-14, h3 14-25, h4 25-36, h5 36-47, h1 47-57, h7 57-64` (h1 keeps its 81 rendered frames).
Also: a small white debris island floats above the roof/tail in h0, h1, h2 and the h1 test frame - drop it from `coupe2_np`
(islands in numpy) before rendering h2-h7, or paint it out of h0/h1.

## 3. Spyder section n64-108 (44 beats, 26.4 s): progressive teardown travelling front -> side -> rear, then reassembly
Order follows the inventory: the richest region (front, 5 parts + hinge) gets the lift and 22 of the 44 beats; side (2 parts)
6 beats; rear (1 part) 6 beats; reassembly + hero 10 beats. Each part moves into clear black (forward of the nose / outboard /
behind the tail), tips its scanned inner face toward the lens once, then holds. Nothing separates outside its section's shot.
Use 2 mm parts (`EXPLODED2`) for every new shot; `persistent: False` on all; luma-scan every frame.

Part rest centres (from bbox): fb (-0.01,-1.79,0.42); hood hinged at p (0.09,-1.31,0.97) axis X; tc (-0.01,-1.34,0.76);
lc (-0.34,-1.77,0.64) and rc (+0.32,-1.78,0.64) (note: `left_cowl` sits on -X); fe (-0.71,-1.32,0.52); sk (-0.83,0.14,0.30);
rb (0.02,2.00,0.57). `spin` = [deg, ax, ay, az] about the rest centre; give every part a `spin [0,...]` key before its first spin
key so it interpolates from 0.

| # | shot | n | t (s) | frames @15 | focus | camera (start -> end) | part action (shot fractions) | render |
|---|---|---|---|---|---|---|---|---|
| S1 | s5_frontopen | 64-72 | 41.481-46.281 | 72 | front end opens on the start-up | as rendered (az -42 el 10 d 5.6 -> az -24 el 16 d 6.2, target ~[-0.1,-1.5,0.55], 40 mm) | fb off -> [0,-0.95,-0.02]; fe -> [-0.55,-0.05,0.02]; hood deg -66 (OPEN) | **reuse as-is** |
| S2 | sp_bumper | 72-80 | 46.281-51.082 | 72 | front bumper, inner face/mounts | az -45 el 25 d 3.6 target [0,-2.70,0.45] 45 mm -> az -60 el 35 d 2.6 target [0,-3.30,0.65] 50 mm (push in; open nose + crash structure at frame edge) | fb t0-0.08 hold OPEN; t0.08-0.70 off -> [0,-1.55,0.30], spin -> [125,1,0,0] (inner face (+Y) turns to (0,-0.57,0.82), ~45 deg to the lens); 0.70-1 drift to [0,-1.60,0.33]. Others hold OPEN | new |
| S3 | sp_hood | 80-86 | 51.082-54.682 | 54 | under the hood: hood underside + cowls lifting off the scanned structure | az -20 el 28 d 3.2 target [0,-1.55,0.95] 45 mm -> az -14 el 36 d 2.7 target [0,-1.55,0.90] | hood t0.05-0.45 deg -66 -> -78 and off -> [0,0.05,0.60] (underside faces forward = toward lens; no spin); tc t0.30-0.70 off -> [0,0,0.45]; lc t0.40-0.80 -> [-0.22,-0.10,0.35]; rc t0.45-0.85 -> [0.22,-0.10,0.35] (translate only). fb holds S2 end pose - if it intrudes at the bottom edge on frame 1, add a key to [0,-1.90,0.10] in S2's last 20 % | new |
| S4 | sp_side | 86-92 | 54.682-58.282 | 54 | right side: fender then skirt, real sill/arch structure beneath | az -95 el 22 d 3.4 target [-1.0,-0.90,0.55] 50 mm -> az -88 el 20 d 3.2 target [-1.0,0.35,0.35] (slide rearward) | fe t0.05-0.50 off [-0.55,-0.05,0.02] -> [-0.95,-0.15,0.40], spin -> [-120,0,1,0] (inner face +X turns to (-0.5,0,0.87), up/out to the lens); sk t0.40-0.85 off -> [-0.55,0,-0.15], spin -> [-120,0,1,0]. Keep the hollow front wheel at the frame edge (see blockers) | new |
| S5 | sp_rear | 92-98 | 58.282-61.883 | 54 | rear bumper, inner face, diffuser/exhaust structure behind | az -115 el 25 d 3.8 target [0,2.80,0.65] 45 mm -> az -125 el 30 d 3.2 target [0,3.00,0.75] | rb t0.10-0.70 off -> [0,1.00,0.35], spin -> [-125,1,0,0] (inner face -Y turns to (0,0.57,0.82)); seen from az -115 it sits on black past the tail. Others hold | new |
| S6 | sp_finale | 98-108 | 61.883-67.883 | 90 | whole exploded Spyder -> reassembled hero -> fade | t0 az -105 el 48 d 8.8 target [0,0,0.90] 40 mm; t0.35 az -150 el 34 d 8.2 target [0,0.20,0.75]; t1 az -210 el 16 d 7.2 target [0,0.25,0.55] (rear 3/4 from the car's LEFT, not h7's angle) | t0-0.30 everything holds its section end pose (the one full-explode view, ~1.8 s, slow crane); return in reverse travel order, spins back to 0: rb 0.30-0.50, sk+fe 0.36-0.56, tc/lc/rc 0.44-0.60, hood (off then deg -> 0) 0.48-0.68, fb 0.54-0.74; `visible`: base+parts [0,0.80], `car2` [0.80,1.01] (clean car swap on n106, c5 lesson); fade out last 0.9 s in assembly | new |
| - | logo | 108- | 67.883-71.85 | still | small logo on black | as now | - | reuse |

### Music map
Lift n64 = S1 (second start-up catches here). Section changes every 8/8/6/6/6 beats on n72/80/86/92/98, each a bar line or half
bar of the groove; reassembly starts ~n101, clean-car swap n106, fade into the music stop n108. Every part move starts on a beat:
editor, place the t-fractions on whole beats when writing the keys (S2: 1 beat = 0.125, S3-S5: 1 beat = 0.167, S6: 0.1).

## 4. Diff vs current project.yaml
- Coupe: h6_high dropped; h2/h3/h4/h5 moved earlier and lengthened to 11 beats; h1_tail moved from 2nd to 6th (10 beats).
- Spyder **reused as-is:** s5_frontopen (S1), logo. **Dropped:** s7_explode (all parts at once in one wide orbit - against the
  rules), s8_float (wide side, all exploded, drift only - redundant with S6's exploded view and far too small), s4_wheel (bumper
  and fender ON - contradicts the state after S1; the coupe h4 already owns the wheel subject), old/s9_reassemble_plate (legible
  plate, rear 3/4 repeats h7), s1-s3/s6 v2 renders (not in this cut). z1-z4 already deleted.
- **New:** sp_bumper, sp_hood, sp_side, sp_rear, sp_finale.

## 5. Render budget (15 fps)
New Spyder: 72 + 54 + 54 + 54 + 90 = **324 frames** (~45-65 min at 8-12 s/frame). Coupe still to render (already planned):
h2/h3/h4/h5 99 each + h7 63 = 459 (was 81x5+63; dropping h6 nets -9). Reused unchanged: h0_select, h1_tail (running),
s5_frontopen, logo. Test each new Spyder shot at 30 % on frames 1/mid/last before the full render (one job at a time).

## Hold list (> 0.75 s with nothing new entering)
- S2 t0.70-1 (1.4 s): bumper tipped, camera still pushing in on the inner face - the subject of the shot.
- S5 t0.70-1 (1.1 s): same for the rear bumper.
- S6 t0-0.30 (1.8 s): the only full-explode view; camera cranes from high side toward the rear. Justified once.
- S6 t0.80-1 (1.2 s): clean assembled hero into the fade.

## Blockers / open questions
1. **h3_hood**: current re-frame still shows the windscreen holes (top ~25 % of `framing_hp3/chk.png`). Re-frame as in section 2
   before rendering.
2. **Hollow Spyder wheels in S4/S6**: S4 is close on the right side where the front wheel sits behind the fender. Keep it at the
   frame edge/in shadow; if it reads as a hollow ring, either start S4 behind the wheel (target y -0.6) or splice the FWW
   wheel-off zone into the base for this shot only (but it is a different captured state - ask before doing that).
3. Debris island above the coupe (h0/h1/h2) - remove before the remaining coupe renders.
4. `spin` signs above are derived from `Matrix.Rotation` (right-hand rule) on the rest pose; confirm the inner face is the one
   facing the lens on the 30 % test frames before the full renders.
