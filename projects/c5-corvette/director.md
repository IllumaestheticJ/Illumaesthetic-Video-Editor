# C5 Corvette v2: director's shot plan (stage 2)

This plan keeps the scene order from `direction.md` (front bumper → hood/engine bay → -X fender → rear bumper → reassembly →
logo). The order follows the scan inventory and travels front → side → rear. It has one focus per shot, each section in one
continuous sequence, and the bumper-removed states as hero beats with labels.

Inputs read:
- lessons.md (bottom = newest cross-reel rules), the Temerario notes, feedback.jsonl (v1 note), project.yaml, editlog.jsonl,
  shots.py, tools/shot.py, review.md, and director_report.md (v1).
- That report flagged repeated views (s1~s2 IoU 0.76, s3~s7 0.83, s3~s9 0.72, s5~s6 0.68) and "no focus" on every shot. v1 cover 10-17 % on the wides.
- Images: v1 sheet, framing strips v2_A/v2_C, the look/all.png composite, and frames 1/34/61 of A and 1/40/80 of B.

## Global settings for every new shot
- Write the new shots in shots.py with their own cut list: `V2CUTS = [0, 4.117, 9.309, 17.024, 22.130, 30.385, 35.496]`.
  Each shot renders its cut length + 0.4 s slack. Animation keys below are **shot-local seconds** (convert with `t/secs`, as `fr()` does).
- 15 fps, 75 %, 12 spp, exposure -0.5, `light_ref="base"`, hinges = HINGES. Persistent data OFF. **First fix
  `tools/shot.py:209`**: it hard-codes `use_persistent_data = True` and ignores the JSON key. Change it to
  `spec.get("persistent", True)`, and set `persistent: false` on every shot.
- Base for all part shots = `V2` objects (base.blend composite + parts). The clean `car.blend` is used only where stated.
  The targa stays home (no roof-off scan).
- Spherical camera: az 0 = in front of the nose, -90 = -X side, ±180 = behind. Lens is on a 24 mm-wide sensor.
- Parts not listed in a shot are held at home (`off [0,0,0]`, `deg 0`, `spin [0,0,0,1]`). "Hidden" = `visible: [0,0]`.
- After each render: per-frame mean-luma scan (no step drops), plus a first/middle/last-frame sheet checked for cropping. The whole car
  must have ≥6 % margin each side on wide frames; the named section must fill detail frames; nothing clipped by accident.

## Shot table

| section | shot id | reel start-end (s) | focus | camera (shot-local keys) | part action (shot-local s; reel time) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| front bumper removed | `v2_a2_open` | 0 – 4.117 | whole car → front bumper coming off | t0: az -28, el 11, dist 7.2, target [0,-0.35,0.55], lens 30 → t=end (4.517): az -28, el 9, dist 3.0, target [0,-2.0,0.42], lens 30 (= the old A end pose). One straight push along one bearing, no orbit. At 7.2 m the car fills ~66 % of the width | fb: home until 1.20; slides straight out toward camera to off [0,-0.9,0.05], spin [0,0,0,1] at 4.517 (same end pose as old A, so B continues). Visibility: `car` (clean) [0, 1.20 s), V2 composite [1.20 s, end]. The swap is on the bumper's first motion | whole car with margins from frame 1 (hook + CROPPING), then straight into the hero data | **re-render** (old A clips the tail at x=0 in frame 1) |
| front bumper removed | `v2_b_fb_inside` | 4.117 – 9.309 | the nose structure behind the bumper, then the bumper's inner face | as rendered: head-on az -6, el 7, push 3.6 → 2.9 m | as rendered (local): bumper rises 0.3-1.9 (4.42-6.02), turns its inside to camera 1.9-4.2 (6.02-8.32), parked above the structure to the cut | 5.2 s on the hero data: structure readable lower frame the whole time, bumper inner face upper frame | **reuse** (first 5.192 s of 86 frames) |
| hood / engine bay | `v2_f2_hood` | 9.309 – 17.024 | hood on its hinge → hood underside → engine bay | t0: az -22, el 24, dist 3.8, target [0,-1.45,0.70], lens 30; t=5.70: az -22, el 30, dist 3.6, target [0,-1.35,0.95]; t=8.115 (end): az -22, el 42, dist 2.5, target [0,-1.10,0.50]. One bearing: crane up + push in | hood: deg 0 at 0.05 (on the drop) → **deg 46 at 1.60** (10.91, the captured open state) → hold to 2.20 → lift straight up and toward camera: off [0,-0.25,1.15] at 4.38 (13.689 accent) → flip: deg 0, off [0,-0.55,1.30], spin [-75,1,0,0] at 5.70 (15.01; front edge up, scanned underside facing the lens). Put spin [0,1,0,0] on the earlier keys. Parked from 5.70 and leaves the top of frame as the camera pushes into the bay. fb hidden; fe, rb home | richest data on the drop: real hinge, captured open state, scanned underside, removed-state bay; no cut-away mid-action | new: 122 frames |
| -X side (front quarter) | `v2_c2_fender` | 17.024 – 22.130 | fender → exposed wheelhouse / headlight bucket / mounts | t0: az -78, el 10, dist 3.9, target [-0.70,-1.40,0.60], lens 30; t=2.40: az -74, el 12, dist 2.6, target [-0.70,-1.55,0.58], lens 32; t=5.506: az -70, el 14, dist 1.9, target [-0.70,-1.65,0.55], lens 35 | fe (translate only, no scanned inside): home at 0.05 (on the cut) → off [-0.85,-0.05,0.80] at 1.50 (out toward camera into black above the roofline) → off [-1.20,0,1.70] at 3.00 (20.02; leaves the top of frame cleanly). fb, hood hidden; rb home | structure behind the fender is the data; it ends as a macro the section fills, held ~2 s for reading | new: 83 frames |
| rear bumper removed | `v2_g2_rear` | 22.130 – 30.385 | rear structure behind the bumper, then the bumper's inner face | t0: az -150, el 10, dist 4.6, target [-0.10,1.95,0.50], lens 30; t=2.90: az -165, el 10, dist 3.6, target [0,2.20,0.60]; t=4.34: az -170, el 9, dist 3.4, target [0,2.30,0.65]; t=8.655: az -172, el 9, dist 3.0, target [0,2.35,0.72]. The 22° swing squares up to the inner face (not a turntable) | rb: home, spin [0,0,0,1] at 0.10 (on the cut) → slides straight back toward camera, off [0,0.9,0.05] at 1.60 → rises clear, off [0,1.3,0.95] at 2.90 → holds while the camera moves in on the structure → at 4.34 (26.471 accent) starts the turn → spin [180,0,0,1] at 6.20 (28.33), inner face square to camera → parked to the end. fb, fe, hood hidden | hero beat 2: removal, readable hold on the structure, then the scanned inside, all in one held shot (old G+H merged) | new: 130 frames |
| whole car (reassembly) | `v2_i2_home` | 30.385 – 35.496 | parts returning → the clean car | t0: az -140, el 22, dist 6.6, target [0,0.10,0.80], lens 32 → t=end (5.511): az -140, el 18, dist 8.4, target [0,0.05,0.55], lens 32 (slow pull back; whole car ~70 % of the width at the end) | start poses at t0, all moving from frame 1: hood off [0,-0.6,1.10] deg 0; fb off [0,-1.0,0.50]; fe off [-0.70,-0.6,0.60]; rb = shot 5's end pose (off [0,1.3,0.95], spin [180,0,0,1]) for continuity. Home: hood 0→1.40; fb 0.30→1.80; fe 0.60→2.93 (33.314); rb 1.20→4.017 (34.402 loud kick), turning back to spin 0 on the way. Visibility: V2 [0, SWAP), `car` [SWAP, end] with SWAP = 4.02 s local. Then check that the swap lands on assembled frame 1032 (v1 was ~0.08 s early; adjust the key, not the cut). Assembly: `fade=t=out:st=4.35:d=0.75` (34.735 → 35.485) | the payoff: clean whole car, then fade; it is never a held exploded wide | new: 83 frames |
| - | `logo_small` | 35.496 – 39.40 | logo | static | - | brand on the biggest hit; it rides the music's decay | build a new card (below) |

### Labels (Remotion `ScanHUD`, `kind: "label"`, title only, no sub, no numbers; overlays on scan shots only)

Style: Inter Display, tracking +6, `#e8ecf2`, one label at a time, 0.2 s fade in/out. Enter within ±0.1 s of the nearest measured kick
and leave ≥0.15 s before the cut.

Placement: default `x 0.08, y 0.86, align left`, over black under the car, 80 px inside the frame edges. On each label's
first and last frame, check that the box sits over black (mean luma < 20) and outside the silhouette. If it doesn't, use `y 0.10`.

| text | in (s) | out (s) | `from` (30 fps frame) | `duration` (frames) | shot |
|---|---|---|---|---|---|
| FRONT BUMPER REMOVED | 4.39 | 6.20 | 132 | 54 | v2_b_fb_inside |
| FRONT BUMPER - INSIDE | 7.73 | 9.15 | 232 | 43 | v2_b_fb_inside |
| HOOD REMOVED | 15.30 | 16.85 | 459 | 47 | v2_f2_hood |
| FENDER REMOVED | 20.05 | 21.95 | 602 | 57 | v2_c2_fender |
| REAR BUMPER REMOVED | 23.90 | 26.30 | 717 | 72 | v2_g2_rear |
| REAR BUMPER - INSIDE | 27.20 | 30.20 | 816 | 90 | v2_g2_rear |

All wording comes from the file names (`front bumper removed`, `front bumper` inside+outside, `front bumper and hood removed`,
`fender and bumper removed`, `Rear bumper removed`, `rear bumper inside`). No component names and no numbers. No label goes
on the hood opening: the captured state is "Hood Open", and a third label in that scene would crowd it. No persistent HUD.

### Logo
New card `/home/user/media/c5-corvette/logo/logo_small.png`, 1080x1920:
- Background: black at the render background level (sample the corner of a render).
- Logo: `IllumaestheticLogoColor-01.png` scaled to **300 px wide (~28 % of the width)**, centred at (540, 960).
- Not `end_card.png`, whose logo is 562 px = 52 %.
- Timeline: `dur 3.9000` (117 frames). `vf: fade=t=in:st=0:d=0.25,fade=t=out:st=2.5:d=0.6`. Logo at full 35.75-38.0, gone by 38.6,
  then black under the music's decay to 39.40.

### Assembly durations (whole frames from round(cut*30))
Cut frames are 124 / 279 / 511 / 664 / 912 / 1065, and the end is 1182.

| clip | dur (s) |
|---|---|
| v2_a2_open | 4.1000 (123 frames, first clip one short as in v1; `fade=t=in:st=0:d=0.4`) |
| v2_b_fb_inside | 5.1667 |
| v2_f2_hood | 7.7333 |
| v2_c2_fender | 5.1000 |
| v2_g2_rear | 8.2667 |
| v2_i2_home | 5.1000 |
| logo_small | 3.9000 |

Measure each cut against the decoded audio afterwards (lesson).

## Cut list

| removed | why |
|---|---|
| v1 s1 front 3/4 turntable, s2 rear 3/4 orbit, s3 high orbit, s7 top-down spin | rotations that show nothing new; s1~s2 and s3~s7/s9 are the same view (director_report IoU 0.72-0.83) |
| v1 s4 wheel ECU, s5 tail-lamp ECU | exterior, not the removed-state data; repeated section |
| v1 s6 hood open (exterior 3/4) | replaced by `v2_f2_hood`, which shows the underside and the bay |
| v1 s8 wide explode of 5 panels, s9 float/reassemble | everything separated in one wide shot at 10-12 % cover; the targa had no roof-off scan |
| v2 draft A `v2_a_fb_off` | frame 1 clips the tail (CROPPING); replaced by `v2_a2_open` with the same end pose |
| v2 draft D fender macro, E nose macro | same section as C / B in a separate shot; D's macro is folded into C2's push |
| v2 draft G + H as two shots, on +X | same section twice; line crossed after the -X fender. Merged into `v2_g2_rear` on -X |
| v2 draft I (front 3/4 wide with all parts off) | opens on an all-parts-off wide; a jump back to the front after the rear |
| `end_card.png` 52 % logo, 3.9 s held | "small logo", "last scenes held too long" |

## Hold list (> 0.75 s)

| shot | span (reel s) | reason |
|---|---|---|
| v2_b_fb_inside | 8.32 – 9.31 (1.0 s) | bumper inside parked over the structure. The camera is still pushing, and the label is being read |
| v2_f2_hood | 15.01 – 17.02 (2.0 s) | hood parked; the camera pushes into the engine bay, reading the HOOD REMOVED data |
| v2_c2_fender | 20.02 – 22.13 (2.1 s) | macro of wheelhouse / mounts, slow push 2.3 → 1.9 m: the reading hold for the fender data |
| v2_g2_rear | 25.03 – 26.47 (1.4 s) | bumper parked high; the camera moves in on the rear structure: the hero-beat hold |
| v2_g2_rear | 28.33 – 30.39 (2.1 s) | inner face square to camera, slow push; second hero-beat hold |
| logo_small | 35.75 – 38.0 (2.25 s) | logo, riding the music's decay |

The hood hold at 46° (10.91-11.51, 0.6 s) is under 0.75 s. It is kept so the captured open state reads.

## Render budget (15 fps)

| item | frames |
|---|---|
| v2_a2_open | 68 |
| v2_f2_hood | 122 |
| v2_c2_fender | 83 |
| v2_g2_rear | 130 |
| v2_i2_home | 83 |
| **Total** | **486 frames ≈ 89-105 min** at 11-13 s/frame |

- Run them in the background, one at a time.
- Before that, run 30 % / 8 spp framing strips (`tools/framing.sh`, first/⅓/⅔/last) for all five, plus a 1-frame flip-sign test
  for the hood at local 5.70 s.
- Reused unchanged: `renders/c5/v2_b_fb_inside` (86 frames, luma clean).
- Not used: `renders/c5/v2_a_fb_off`.
