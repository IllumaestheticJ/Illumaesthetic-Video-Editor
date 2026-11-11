# Scene direction - toyota-gr86 (BRZ gen 2 hero scan), v3

Scene director, 2026-11-11. Inputs: lessons.md (all), style-guide, clips.md (incl. "v3 additions"), project.yaml (v2),
editlog, feedback.jsonl (5 v2 notes), review.md, v2 direction/director.md, v2 sheets (`/home/user/media/work/gr86/out/sheet_*.jpg`),
state renders (`reg/states_sheet.jpg`) and NEW check stills of the v3 assets, 30 % res / 8 spp, in
`/home/user/media/work/gr86/reg/v3dir/t1..t10.png` (spec next to each png):
t1 lid lifted over comp_trunkopen (rear-right high) · t2 rear bumper tipped -110 deg with reverse light (red) + plate light (cyan)
riding on its inner face · t3/t6 lights + mirrors coloured on car4 · t4/t5 Side Mirrors Removed, right/left mount ·
t7 comp_trunkopen near top-down · t8 Trunk Open scan alone · t9 comp_trunkopen rear-right 3/4 at ~25 deg down ·
t10 comp_hoodopen + hood_t lifted (windshield intact).

## v2 -> v3 changes (user feedback 2026-11-11)
| # | v2 note | v3 answer |
|---|---|---|
| 1 | Logo too small (330 px card) | New card at ~860 px wide (80 % of 1080; `ferrari-296/tools/logo_card.py --width 860`), centred, 2.47 s |
| 2 | Hood shot cut the windshield | hood_t (trimmed at the cowl gap) replaces hood_m everywhere; base rebuilt with the hood hole limited to hood_t (t10: glass intact). c_front + reassembly re-rendered |
| 3 | Use the trunk-open scan | NEW rear beat: the closed lid (lid.blend) LIFTS OFF straight up/back (no hinge: the raised lid was never scanned) and reveals the scanned cargo opening. Label TRUNK OPEN |
| 4 | Explode the rear lights | NEW f_lights: on the tipped rear bumper, the reverse-light bar comes off the INNER face toward the lens (only its socket side is captured - shown socket side only, no spin), then ONE licence-plate lamp lifts out. Labels REVERSE LIGHT, LICENSE PLATE LIGHT |
| 5 | Use the side-mirror-removed scans | NEW d_mirror between front and rear: framed on the RIGHT A-pillar (good capture); both mirrors fly out/up, the left one off-screen (thin broken capture); push in on the scanned right mirror mount. Label SIDE MIRROR REMOVED |
| - | (budget) | Top stack (v2 e_stack) dropped: the rear is now the richest region and needs the screen time; the reassembly is restaged progressively (rear -> front) instead of one slam |

## 1. Feature inventory (v3)

| Region | Signature / what the data holds | States (registered to BRZ Full Car) | Parts (registered) | Weak data | Richness |
|---|---|---|---|---|---|
| **Rear** | Ducktail lid with BRZ badge, twin exhausts, diffuser, plate recess | **Rear Bumper Removed** (63 %, 3.2 mm: holed full-width crash beam, silencer, lamp backs); **Trunk Open** (74 %, 2.8 mm: cargo opening/floor only, z < 875 mm); Trunk Open Bumper Off (fill < 750 mm); License Plate Lights Removed (ICP 75 mm = NOT registered, unused) | **rear bumper** (part scan, inner face scanned); **lid** (cut from the car's own skin, outer only); **reverse light** (median 9.8 mm, socket side only, sits on the bumper inner face - t2); **plate light** (one lamp, 2.3 mm, good) | Cargo is a black void from above (t7) - readable only from a rear 3/4 at <= ~30 deg down (t9); left tail lamp has a scan hole (keep rear-RIGHT); plate kept as scanned (plate rule: IS300 only) | **Highest**: 2 usable states + 4 parts |
| **Front** | Slat grille, LED headlights, corner intakes | **Hood Open** (engine bay, 48 %, 3.8 mm); **Bumper Hood Removed** (front structure < 650 mm, 27.6 %, 3.9 mm) | **front bumper** (inner face scanned); **hood_t** (car skin, trimmed at cowl) | Open hood never captured (lift off, never hinge); Side Markers (ICP 84 mm) not registered -> unused | High: 2 states + 2 parts + best detail (s3) |
| **Side** | Profile, doors, A-pillar | **Side Mirrors Removed** (92 %, 2.6 mm): both mount bosses captured (t4 right: clean bracket stub; t5 left: mount with a dark hole) | **mirror_R** (decent); mirror_L (thin broken capture, 0.68 m long bbox = junk attached) | left mirror + left mount weak; wheels/tyres rough | Medium-low: 1 state + 1 good part -> one short scene, right side only |
| Top | Roof, glass | - | - | sprayed glass, nothing new | none (v2 stack dropped) |
| Wheels / interior | - | - | - | rough / not scanned | none |

## 2. Scene order (front -> side -> rear -> reassembly -> logo)

Travel: front-right 3/4 -> front detail -> front states -> right A-pillar -> rear-right -> under/behind the rear bumper ->
high rear-right whole car. The camera stays on the car's RIGHT side throughout (left mirror/left lamp are the weak data).

| # | id | section | scans used | feature shown | why here (inventory) | bars | camera note |
|---|---|---|---|---|---|---|---|
| A | `a_open` REUSE | whole | car4 | whole car, front-right 3/4, arc + push | opener = whole car, motion from frame 1, front-right toward the first section | 2 | as rendered |
| B | `b_headlight` REUSE (s3 from 2.4 s) | front | det_front | right headlight + slat grille + intake | front signature detail, best close-up in the set | 1 | as rendered |
| C | `c_front` NEW | front | comp_v3 + hood_t + front_bumper | hood lifts off -> engine bay (Hood Open) -> front bumper off, tipped -> FRONT BUMPER REMOVED structure | 2 states + 2 parts, hero beat; windshield now intact | 3 | v2 d_front path compressed 4 -> 3 bars |
| D | `d_mirror` NEW | side | comp_v3 + mirror_R/L | right mirror flies out -> SIDE MIRROR REMOVED mount | 1 state + 1 good part = short scene; physically between front and rear | 1 | right A-pillar, push in on the mount |
| E | `e_rear` NEW | rear | comp_v3 + lid + rear_bumper (+ lights riding in it) | lid lifts off -> TRUNK OPEN cargo -> rear bumper off, tipped -> REAR BUMPER REMOVED crash beam | richest region: one continuous 4-bar shot over two phrase kicks (19.62, 24.52) | 4 | rear-right, ~25 deg down for the cargo (never top-down), low for the beam |
| F | `f_lights` NEW | rear | comp_v3 + rear_bumper + reverse_light + plate_light | the two light scans come off the tipped bumper's inner face | the rear's last layer = the explode zoomed in on one assembly; lands on 29.42 | 2 | looking down at the parked bumper from rear-right; lights lift toward the lens |
| H | `h_reassemble` NEW | reassembly | comp_v3 + all 8 parts | parts fly home rear -> front, last one on the loud return 34.32, fade | payoff on the biggest musical moment; progressive, not one wide separation | 2 | high rear-right, nose up in frame, slow push (no orbit) |
| I | `logo` NEW card | end | logo | ILLUMAESTHETIC logo, LARGER | user note 1 | 1 | static |

## 3. Shot specs (for director.md / shot JSON)

Frame: Blender m, car4 prep. Nose -Y (-2.13), tail +Y (2.13), ground z 0.19, roof ~1.45, car's RIGHT = +X.
Part `loc` = world offset from home; `rot` deg XYZ about `pivot` (default = part bbox centre). All new shots: base
`comp_v3.blend` (see Q1), 15 fps, 75 %, 12 spp, persistent data OFF, `seconds` = slot + 0.2 (3 spare frames for the
minterpolate tail). Local t = 0 at the shot's first frame. Ease inout unless noted.
Pivots: front bumper (-0.07,-1.818,0.605), rear bumper RB = (0.064,1.817,0.638). **reverse_light and plate_light use pivot RB and
repeat the rear bumper's keys** (they ride in the bumper), plus their own extra offset in f_lights.

Kicks (s / frame @30): k1 4.931/148 · k2 7.380/221 · k3 9.83/295 · k4 12.28/368 · k5 14.73/442 · k6 17.174/515 · k7 19.62/589 ·
k8 22.07/662 · k9 24.523/736 · k10 26.97/809 · k11 29.42/883 · k12 31.873/956 · k13 34.32/1030 (loud return) · k14 36.766/1103 · end 39.24/1177.

### A `a_open` - whole - f0-148 (148 f) - 0 -> k1 - REUSE /home/user/media/work/gr86/shots/a_open
Whole car front-right 3/4, ~20 deg arc + push from frame 1. No parts, no label. dur 4.9 (first clip one frame short).

### B `b_headlight` - front - f148-221 (73 f) - k1 -> k2 - REUSE s3_wheel from 2.4 s
Right headlight + slat grille + intake (2 mm). No label.

### C `c_front` - front - f221-442 (221 f; 111+3 new @15) - k2 -> k5
Focus: hood off -> engine bay -> front bumper off -> front structure.
Camera: K0 t0 (2.20,-4.90,2.00)->(0.10,-1.40,0.80) f30 whole front end incl. right wheel ·
K1 t2.45 (1.40,-3.90,2.70)->(0.05,-1.15,0.75) f30 above the bay, hood leaving the top ·
K2 t3.37 (1.20,-3.60,2.40)->(0.00,-1.10,0.70) f32 bay fills frame (windshield base in, intact) ·
K3 t4.90 (2.10,-4.70,1.70)->(0.10,-2.10,0.50) f30 bumper low in front, structure exposed ·
K4 t7.37 (1.00,-3.60,1.20)->(0.00,-1.85,0.55) f30 front structure ~1.45 m fills frame.
Parts: **hood_t** home to t0.15; t0.15 -> t2.45 loc (0,-0.10,1.20) ease out (**lands k3 9.83**); hold (exits top as camera drops).
**front_bumper** home to t3.37; t3.37 -> t4.90 loc (0.30,-0.90,-0.45) rot (110,0,0) (**lands k4 12.28**, scanned inner face up to the lens); hold.
mirrors, lid, rear bumper + lights: home.
Label: `FRONT BUMPER REMOVED` / sub `HOOD REMOVED`, 12.43 -> 14.58 (f373-437), over the K3->K4 push-in, on black above the car.

### D `d_mirror` - side - f442-515 (73 f; 37+3 new) - k5 -> k6
Focus: right mirror flies off -> scanned right mirror mount.
Camera: K0 t0 (2.10,-1.75,1.55)->(0.80,-0.30,1.05) f30 (~2 m: right A-pillar, mirror, fender top, windshield edge; the open bay
may show at frame left - that is continuity) · K1 t2.43 (1.55,-1.05,1.30)->(0.80,-0.32,1.03) f35 (~1.1 m: the mount fills the centre).
Parts: **mirror_R** home to t0.10; t0.10 -> t1.00 loc (0.40,-0.10,0.45) ease out (out and up above the roofline onto black);
t1.00 -> t2.43 loc (0.55,-0.05,0.95) (keeps rising, leaves frame top-right as the camera pushes in). **mirror_L** same times,
loc (-0.40,-0.10,0.45) -> (-0.55,-0.05,0.95): must stay OUT of frame (behind the cabin) - check first/mid/last.
hood_t (0,-0.10,1.20) and front_bumper (0.30,-0.90,-0.45) rot (110,0,0) parked (out of frame - check).
Label: `SIDE MIRROR REMOVED` / sub `MIRROR MOUNT`, 15.88 -> 17.02 (f476-511), top-LEFT (mirror exits top-right).

### E `e_rear` - rear - f515-809 (294 f; 147+3 new) - k6 -> k10 (one continuous shot, cut at k8 removed)
Focus: lid lifts off -> TRUNK OPEN cargo -> rear bumper off, tipped -> crash beam.
Camera: K0 t0 (2.40,4.70,2.00)->(0.05,1.45,0.85) f30 whole rear half incl. right rear wheel, room above for the lid ·
K1 t2.45 (1.80,4.30,1.80)->(0.05,1.50,0.80) f30 · K2 t4.60 (1.30,3.90,1.55)->(0.05,1.55,0.72) f30 (= t9: cargo opening, ~25 deg down;
do not go higher/closer - t7 shows a black void from above) · K3 t7.35 (2.10,4.90,1.50)->(0.15,2.20,0.45) f30 (whole rear end low, bumper
tipped in front) · K4 t9.80 (1.05,3.70,1.15)->(0.05,1.95,0.68) f30 (crash beam + right exhaust fill frame; targets as v2 g_rear end).
Parts: **lid** home to t0.15; t0.15 -> t2.45 loc (0,0.30,0.95) ease out (straight up and back toward the lens, no rotation;
**lands k7 19.62**); t2.45 -> t4.60 loc (0,0.35,1.40) (rises out of the frame top, cargo stays clear); hold.
**rear_bumper** (+ reverse_light + plate_light, pivot RB, same keys) home to t5.20; t5.20 -> t7.35 loc (0.30,0.95,-0.45) rot (-110,0,0)
(**lands k9 24.52**, scanned inner face turns up/back to the lens, ~15 cm clear of the body); hold (should sit below frame at K4 -
if it pokes the bottom edge, park it at z -0.55).
Labels: `TRUNK OPEN`, 19.77 -> 21.92 (f593-658) · `REAR BUMPER REMOVED` / sub `CRASH BEAM`, 24.67 -> 26.82 (f740-805).

### F `f_lights` - rear - f809-956 (147 f; 74+3 new) - k10 -> k12
Focus: the two light scans leave the tipped bumper's inner face.
Bumper parked as E's end (loc (0.30,0.95,-0.45) rot (-110,0,0) about RB; centre ~ (0.36,2.77,0.19); inner-face normal ~ (0,0.34,0.94)).
Camera: K0 t0 (1.05,4.55,1.65)->(0.36,2.75,0.25) f28 (whole tipped bumper, inner face up) · K1 t2.45 (0.75,4.05,1.30)->(0.36,2.80,0.32) f32
(centre section ~1.1 m) · K2 t4.90 (0.60,3.75,1.15)->(0.30,2.85,0.40) f35 (both lights fill frame). Looking down steeply so the
background behind the bumper is black (below the car), not the body.
Parts (extra offset ON TOP of the bumper keys): **reverse_light** t0.15 -> t1.00 +(0,0.15,0.35) ease out (straight off the inner face,
socket side toward the lens, NO spin - its lens side is not captured); t1.00 -> t4.90 drift +(0,0.18,0.40).
**plate_light** t1.85 -> t2.45 +(0.25,0.15,0.30) ease out (**lands k11 29.42**, offset +X so it clears the reverse light); t2.45 -> t4.90 drift
+(0.27,0.17,0.33). Translate only. Both lights must read on black or with clear separation from the bumper skin - check mid/last;
if they sit over the bumper, add more toward-lens offset.
Labels: `REVERSE LIGHT`, 28.05 -> 29.27 (f842-878) · `LICENSE PLATE LIGHT`, 29.57 -> 31.72 (f887-952).

### H `h_reassemble` - reassembly - f956-1103 (147 f; 74+3 new) - k12 -> k14
Focus: every removed part flies home, rear -> front, the last on the loud return; the car complete; fade.
Start poses = each part's landed pose from its own section: hood_t (0,-0.10,1.20) · front_bumper (0.30,-0.90,-0.45) rot (110,0,0) ·
mirror_R (0.40,-0.10,0.45) · mirror_L (-0.40,-0.10,0.45) · lid (0,0.30,0.95) · rear_bumper (0.30,0.95,-0.45) rot (-110,0,0) about RB ·
lights on the bumper keys + their f_lights t4.90 offsets.
Camera: K0 t0 (1.80,4.60,4.60)->(0,-0.20,0.90) f34 (high rear-right ~35 deg down, nose up in frame, all parts in frame - v2 stack end pose)
-> K1 t4.90 (1.60,4.20,4.20)->(0,-0.20,0.90) f34 (slow push, no orbit).
Homing (each to 0 with ease in = slam): lights t0.15 -> 0.90 back into the bumper · rear_bumper (+lights) t0.60 -> 1.50 · lid t1.00 -> 1.85 ·
mirrors t1.30 -> 2.10 · front_bumper t1.50 -> 2.45 · hood_t t1.60 -> 2.45 (**k13 34.32**). From 34.32 (local 2.45) optionally render
the base as clean car4 with no parts (c5 lesson: swap to the clean car on the kick; check the plate/bumper pop is hidden by the slam).
Fade: `fade=t=out:st=2.9:d=1.95` (black by ~36.72). No label.

### I `logo` - end - f1103-1177 (74 f) - k14 -> end
ILLUMAESTHETIC logo ~860 px wide (80 % of frame width), centred, fade in 0.3 s, holds to the end of the audio (39.24).

## 4. Music map
| shot | start -> end (s) | frames | lands on |
|---|---|---|---|
| A a_open | 0.000 -> 4.931 | 0-148 | - |
| B b_headlight | 4.931 -> 7.380 | 148-221 | k1 |
| C c_front | 7.380 -> 14.73 | 221-442 | hood k3 9.83, bumper k4 12.28 |
| D d_mirror | 14.73 -> 17.174 | 442-515 | cut on phrase k5; mirror off by 15.73 |
| E e_rear | 17.174 -> 26.97 | 515-809 | lid k7 19.62 (phrase), bumper k9 24.52 (phrase) |
| F f_lights | 26.97 -> 31.873 | 809-956 | plate lamp k11 29.42 (phrase) |
| H h_reassemble | 31.873 -> 36.766 | 956-1103 | last part home on k13 34.32 (loud return) |
| I logo | 36.766 -> 39.24 | 1103-1177 | k14 |
Total 1177 frames / 39.23 s. Cuts at f148, 221, 442, 515, 809, 956, 1103 (first clip one frame short; frames as above).

## 5. Diff vs v2 and render reuse
| v2 clip | v3 | why |
|---|---|---|
| a_open | **REUSE as-is** | whole car, motion from frame 1; intact car4 unaffected by the hood change |
| b_headlight (s3 from 2.4 s) | **REUSE as-is** | det_front unaffected |
| c_front (d_front, 9.8 s) | **NEW** c_front, 7.37 s | hood_t (windshield fix); compressed from 4 to 3 bars to make room for side + rear additions |
| - | **ADDED** d_mirror | user note 5 |
| d_rear (g_rear, 7.37 s) | **NEW** e_rear, 9.8 s | adds the lid lift-off / TRUNK OPEN before the bumper (user note 3); one continuous shot so the two rear-right views don't repeat across a cut |
| - | **ADDED** f_lights | user note 4 |
| e_stack | **DROPPED** | top-down stack of all parts at once; time and budget go to the richest region (rear) |
| f_reassemble (s7 tail) | **NEW** h_reassemble | s7 has the old hood and none of the new parts; progressive rear -> front homing |
| logo small | **NEW** card ~860 px | user note 1 |
New render frames @15 fps: c 114 + d 40 + e 150 + f 77 + h 77 = **458** (+ ~15 check stills at 25 %). ~65-80 min at 8-10 s/frame, one at a time.
Required before assembly: first/mid/last still of every new shot (cropping rule A), per-frame luma check of every render (black-frame lesson).

## 6. Open questions / blockers for the editor
1. **Base `comp_v3` does not exist yet.** comp_explode has the old hood hole (windshield cut); comp_trunkopen/comp_hoodopen still have bumpers/mirrors.
   Build ONE base so every v3 shot shares it: full car minus hood_t, lid, front + rear bumper, both mirrors; fills only inside each
   panel's own zone: Hood Open (hood_t zone, glass stays), Bumper Hood Removed (< 650 mm), Rear Bumper Removed, Trunk Open (lid zone,
   cargo), Side Mirrors Removed (mirror zones). Check a front still (windshield intact), t4/t5-style mount stills, and t9-style cargo still.
2. rear_bumper still contains the plate lamp (2.3 mm match) and probably reverse-light geometry: delete rear_bumper tris within ~3 mm of
   plate_light and ~10 mm of reverse_light (at their registered poses) or the lamps double when they lift out. The recess left behind is real.
3. Which plate lamp is plate_light (x +0.03..+0.15 = the car's right one)? The other lamp stays in the bumper; label is singular.
4. mirror_L carries junk (bbox 0.68 m in y): keep it off-screen in D; clean to its largest island before H, where it is on the far side.
5. Not used (not registered): License Plate Lights Removed (ICP 75 mm), Side Markers (ICP 84 mm). If Side Markers registers < 3 mm, a
   front side-marker explode off the tipped front bumper is a candidate for a later version - not in v3.
6. Label wording is from scan names only (Bomex Bumper Hood Removed / Side Mirrors Removed / Trunk Open / Rear Bumper Removed /
   Reverse Light / License Plate Light) plus CRASH BEAM (holed beam visible in the Rear Bumper Removed scan, v2) and MIRROR MOUNT
   (bracket stub visible in t4). Confirm each in the rendered frame before burning it in.
