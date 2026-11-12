# Scene direction - toyota-gr86 (BRZ gen 2 hero scan), v4

Scene director, 2026-11-12. Inputs: lessons.md (all), v3 direction (below, superseded), clips.md, feedback.jsonl (4 v3 notes),
editlog (v4 geometry entries 00:19-00:22), tools/shots_v3.py, part bboxes (`/home/user/media/work/gr86/blend/*_v4.json`, hood_t.json),
v3 delivered file `/home/user/media/work/gr86/out/toyota_gr86_v3.mp4` (1 fps sheet + frames at 13.9 / 21.5 / 26.0 s).
No v4 render exists yet: every v4 framing below is an intent to be checked on first/mid/last stills.

## v3 -> v4 changelog
| # | v3 user note | v4 answer |
|---|---|---|
| 1 | "the video needs to move faster" | A cut on EVERY kick (~2.45 s, 15 shots + logo, was 8 clips of 2.4-9.8 s). One action per shot; every part move takes 0.4-1.0 s and starts in the first 2 frames; opener plays a_open at 2x (whole 20 deg arc in 2.48 s). Part-move shots render at real 30 fps (minterpolate smears fast moves, Civic lesson) |
| 2 | bumper leftovers | geometry fixed (comp_explode4, front_bumper_v4, rear_bumper_v4). Direction: each bumper first pulls STRAIGHT OUT 0.30 m (a black gap opens all round), then tips and drops out of frame into black, never across the body |
| 3 | "hood needs to hinge open THEN come off" | 2 shots: hood hinges -50 deg (nose up) about pivot [0.0185,-0.7777,1.0441]; next kick it lifts off the open pose. Camera on the hinge side so the scanned outer face of the hood faces the lens |
| 4 | "rear trunk cut correctly / done the same" | lid_v4; 2 shots: lid hinges +65 deg (tail up) about pivot [0.0185,1.5923,1.1491]; next kick it lifts off -> cargo (TRUNK OPEN) at <= 30 deg down |
| - | ending | reassembly split into two cameras over ONE part animation: hood swings shut ON the 34.32 cut, then a clean-car high hero pass fades (v3: one 4.9 s wide shot = the slowest stretch, at the end) |

Note on rules: lessons.md (honda-civic-11) says lids shown OPEN in a scan must only hinge, never detach. For this reel the user asked
in so many words for hinge open THEN off (hood and trunk). The user's request wins here. The hood coming off is also backed by the
Bumper Hood Removed state scan; there is no "trunk lid removed" scan, so the lid coming off rests only on the user's request.

## 1. Feature inventory (v4, unchanged scans, new parts)
| Region | Signature / data | States (registered) | Parts (moving, v4) | Weak data | Richness |
|---|---|---|---|---|---|
| **Rear** | ducktail lid + BRZ badge, twin exhausts, diffuser | Rear Bumper Removed (holed crash beam, silencer: seen in v3 at 26.0 s); Trunk Open (cargo opening/floor, z < 875 mm) | rear_bumper_v4, lid_v4 (outer skin only), reverse_light (socket side only), plate_light (one lamp, 2.3 mm) | cargo = black void from above; left tail lamp hole; propped lid never scanned | **highest**: 2 states + 4 parts -> 6 shots, 3 phrase kicks |
| **Front** | slat grille, LED headlights, corner intakes | Hood Open (engine bay); Bumper Hood Removed (< 650 mm) | hood_t (outer skin only, trimmed at cowl), front_bumper_v4 | propped hood: only a 250 mm strip in Hood Open; front structure still unverified on v4 (v3 frame showed bumper leftovers) | high: 2 states + 2 parts + best detail (s3) -> 5 shots |
| **Side** | profile, A-pillar | Side Mirrors Removed (right mount clean) | mirror_R (mirror_L junk-laden) | left side weak | low: 1 shot, right side only |
| Top | roof/glass | - | - | nothing new | only the closing hero pass on the complete car |
| Wheels / interior | - | - | - | rough / not scanned | none |

## 2. Scene order (front -> side -> rear -> reassembly -> logo, camera always on the car's RIGHT)
Frame (Blender m): nose -Y (-2.13), tail +Y (2.13), car's right = +X, ground z ~0.19, roof 1.45. Open hood front edge reaches
~(y -1.58, z 1.80); open lid tail edge ~(y 2.09, z 1.46-1.6). Cam = loc -> target, focal mm. Local t = shot seconds.

| # | id | start-end s (frames @30) | section | ONE action | camera start -> end intent | label |
|---|---|---|---|---|---|---|
| 1 | `a_open` REUSE | 0.000-2.480 (0-74) | whole | camera only: arc + push on the whole car | front-right 3/4 whole car (as rendered); a_open PNGs 1-74 at src_fps 30, NO interpolate = the full 20 deg arc in 2.48 s, motion from frame 1 | - |
| 2 | `b_headlight` REUSE | 2.480-4.931 (74-148) | front | camera only: slide across the right headlight | s3_wheel from 2.4 s, as v3 (headlight + slat grille + intake fill frame) | - |
| 3 | `c1_hood_hinge` NEW | 4.931-7.380 (148-221) | front / bay | hood hinges open -50 deg, t0.05 -> 0.85 ease out, holds open | START right side behind the front wheel, above the fender (2.30,-0.60,1.55)->(0.10,-1.30,1.05) f28: hood, right fender, headlight, windshield base; END small rise + push (1.85,-0.95,1.85)->(0.05,-1.35,1.10) f30: open hood whole incl. far edge, its top (z 1.8) inside the frame with margin, bay visible under it. Never frontal: the hood underside is not scanned | - |
| 4 | `c2_hood_off` NEW | 7.380-9.830 (221-295) | front / bay | hood lifts off the open pose: +Z 1.30, -Y 0.15 (clear of the glass), no extra rotation, t0.05 -> 0.70, gone through the frame top by ~0.6 | START higher, still on the hinge side (2.05,-1.10,2.35)->(0.05,-1.30,0.95) f30; END push down into the bay (1.35,-1.75,2.15)->(0.00,-1.30,0.80) f32: bay fills the frame, strut tower to radiator support, windshield base intact | `ENGINE BAY` / sub `HOOD REMOVED`, local 0.85-2.35 (f246-291), in whichever band is black over the whole window (measure; v3 lesson: top band is not always black on close-ups) |
| 5 | `c3_front_bumper_off` NEW | 9.830-12.280 (295-368) | front | front_bumper_v4 pulls straight forward -Y 0.30 (t0.05 -> 0.40, black gap all round), then tips +110 deg about X (inner face up) and drops (+0.30 X, -0.90 Z) out the frame bottom-right, t0.40 -> 1.10 | START front-right 3/4 LOW, much closer than the opener (2.10,-4.40,1.35)->(0.10,-1.85,0.60) f30: whole front end + right front wheel, open bay at top; END (1.75,-4.00,1.15)->(0.05,-1.90,0.55) f30. Bumper leaves into black in front/below the nose, never across the body | - |
| 6 | `c4_front_structure` NEW | 12.280-14.730 (368-442) | front | camera only: push-in on what is behind the bumper, decelerating to near-still for the last ~0.8 s (readable hold) | START low, near-frontal (0.95,-3.60,0.95)->(0.00,-1.90,0.60) f30: the whole exposed front ~1.5 m across; END (0.55,-3.05,0.85)->(0.00,-1.95,0.58) f35: centre structure fills the frame. Bumper out of frame (parked below - check last frame) | `FRONT BUMPER REMOVED` / sub `CRASH BEAM` only if the v4 still shows a beam; otherwise sub `STATE SCAN`. Local 0.15-2.35 (f373-438), top black band |
| 7 | `d_mirror` REUSE (if check passes) | 14.730-17.174 (442-515) | side | right mirror flies out/up (0.9 s), push in on the mount | as v3: right A-pillar (2.10,-1.75,1.55)->(1.55,-1.05,1.30); fresh angle after the frontal push, travels back along the right side | `SIDE MIRROR REMOVED` / `MIRROR MOUNT` as v3 |
| 8 | `e1_lid_hinge` NEW | 17.174-19.620 (515-589) | rear | lid hinges open +65 deg, t0.05 -> 0.85 ease out, holds open | continues back along the right side: START behind the C-pillar, above the deck, FORWARD of the lid (2.25,0.70,1.60)->(0.10,1.75,1.00) f28 so the lid's scanned outer face turns toward the lens; END (1.95,0.95,1.85)->(0.05,1.80,1.10) f30: deck, right tail lamp, open lid whole with its top in frame. Never from behind: lid underside not scanned | - |
| 9 | `e2_lid_off_cargo` NEW | 19.620-22.070 (589-662) PHRASE | rear | lid lifts off the open pose +Z 1.30, +Y 0.10, t0.05 -> 0.65, exits the top | START rear-right, more side-on (2.30,2.70,1.75)->(0.05,1.60,0.85) f30 (lid seen 3/4 side as it leaves); END the v3 t9 pose (1.30,3.90,1.55)->(0.05,1.55,0.72) f30: cargo opening ~25 deg down. Do not go higher/closer (black void) | `TRUNK OPEN` / sub `CARGO AREA`, local 0.80-2.35 (f613-659), top-left black (lid has left by then) |
| 10 | `e3_rear_bumper_off` NEW | 22.070-24.523 (662-736) | rear | rear_bumper_v4 (+ both lights riding, pivot RB) pulls straight back +Y 0.30 (t0.05 -> 0.40), then tips -110 deg about X and drops to the v3 park pose loc (0.30,0.95,-0.45) (t0.40 -> 1.10) | START rear-right 3/4 LOW (2.20,4.70,1.40)->(0.15,2.05,0.55) f30: whole rear end + right rear wheel; END (1.85,4.30,1.25)->(0.10,2.00,0.55) f30. Bumper separates over black, inner face ends up toward the lens at the frame bottom | - |
| 11 | `e4_rear_beam` NEW | 24.523-26.970 (736-809) PHRASE | rear | camera only: push-in on the crash beam, decelerating hold | START (1.35,4.10,1.20)->(0.05,1.95,0.68) f30; END (0.80,3.55,1.05)->(0.05,1.98,0.66) f35: holed beam + silencer + right exhaust fill the frame; parked bumper below frame or whole at the bottom, never clipped | `REAR BUMPER REMOVED` / `CRASH BEAM` (seen in v3 frame), local 0.15-2.35 (f741-806), top black band |
| 12 | `f1_reverse_light` NEW | 26.970-29.420 (809-883) | rear | reverse light lifts straight off the parked bumper's inner face +(0,0.15,0.35), socket side to the lens, no spin, t0.05 -> 0.65, then still | camera tilts down from the beam onto the bumper lying just below it: START (1.05,4.55,1.65)->(0.36,2.75,0.25) f28 whole tipped bumper; END (0.80,4.15,1.40)->(0.30,2.80,0.35) f32. Steep enough that the background behind the bumper is black | `REVERSE LIGHT` / `PART SCAN`, local 0.75-2.35, black band between car and bumper (v3: y 0.33) |
| 13 | `f2_plate_light` NEW | 29.420-31.873 (883-956) PHRASE | rear | plate lamp lifts out, turns upright (lens toward the lens, as v3) and lands on black above the bumper, t0.05 -> 0.70 | fresh, closer, lower angle: START (0.55,3.85,1.05)->(0.15,2.85,0.40) f38; END (0.45,3.65,0.95)->(0.15,2.88,0.45) f42: lamp + its recess in the middle third; reverse light either fully in or fully out of frame | `LICENSE PLATE LIGHT` / `PART SCAN`, local 0.80-2.35 |
| 14 | `h1_reassemble` NEW | 31.873-34.320 (956-1030) | whole | every part flies home rear -> front; hood lands LAST on the cut | high rear-right ~35 deg down, nose up in frame, all parts in frame (v3 h pose) (1.80,4.60,4.60)->(0,-0.05,0.75) f29 -> (1.65,4.35,4.35)->(0,-0.20,0.90) f31 | - |
| 15 | `h2_hero` NEW | 34.320-36.766 (1030-1103) LOUD RETURN | whole / top | clean complete car (swap to car4 on the cut frame 1030), camera rise; fade to black local 1.30 -> 2.40 | high right side ~55-60 deg down, 10-15 deg off vertical (never straight overhead), nose up in frame: (2.60,0.60,5.60)->(0,-0.10,0.80) f30 -> (2.30,0.40,6.10) same target. Whole car with margins; the only top view in the reel | - |
| 16 | `logo` REUSE | 36.766-39.240 (1103-1177) | end | logo_card_v3.mp4 (860 px) | static | - |

Shot 14 + 15 share ONE part animation (local t from 31.873): lights back into the bumper 0.05 -> 0.45 · rear_bumper (+lights) 0.35 -> 0.95 ·
lid flies to its OPEN pose 0.70 -> 1.20, hinges shut 1.20 -> 1.55 · mirrors 1.05 -> 1.50 · front_bumper 1.30 -> 1.85 · hood flies to its
open pose 1.60 -> 2.05, hinges shut 2.05 -> 2.447 (shut on frame 1030 = 34.32, the cut). Landings ease "in" (slam). Start poses = each
part's end pose in its own shot; anything out of frame at frame 0 enters within 0.3 s on its way home. Shot 15 renders the clean
car4 only (c5 lesson: swap to the clean car on a kick), so the frayed composite never reaches the end.

Redundancy check: every section is one continuous run (front 2-6, side 7, rear 8-13, whole 14-15). Same-section neighbours differ in
subject and angle: 3 side/hinge vs 4 high bay vs 5 low front 3/4 vs 6 frontal push; 8 side/hinge vs 9 rear 3/4 high vs 10 rear 3/4
low vs 11 beam push vs 12 steep down on the bumper vs 13 close low on the lamp. No shot reuses the opener's angle (5 is close/low;
15 is near-top). Expect `ive director` silhouette flags on 4/6 and 11/13 (frame-filling close-ups); check by eye, log the reason.

## 3. Music map (cuts = measured kicks, frames = round(t*30))
| shot | start s | frame | music |
|---|---|---|---|
| 1 a_open | 0.000 | 0 | intro |
| 2 b_headlight | 2.480 | 74 | half-kick (measured onset) |
| 3 hood hinge | 4.931 | 148 | kick / phrase |
| 4 hood off + bay | 7.380 | 221 | kick |
| 5 front bumper off | 9.830 | 295 | phrase |
| 6 front structure | 12.280 | 368 | kick |
| 7 mirror | 14.730 | 442 | phrase |
| 8 lid hinge | 17.174 | 515 | kick |
| 9 lid off, TRUNK OPEN | 19.620 | 589 | phrase |
| 10 rear bumper off | 22.070 | 662 | kick |
| 11 crash beam, REAR BUMPER REMOVED | 24.523 | 736 | phrase |
| 12 reverse light | 26.970 | 809 | kick |
| 13 plate light | 29.420 | 883 | phrase |
| 14 reassembly | 31.873 | 956 | kick |
| 15 hood shuts / hero | 34.320 | 1030 | loud return |
| 16 logo | 36.766 | 1103 | kick; end 39.24 = 1177 |
Durations 74,74,73,74,73,74,73,74,73,74,73,74,73,74,73,74 = 1177. Use concat_assemble (exact frames per clip). The richest region
(rear) owns three phrase kicks (TRUNK OPEN, REAR BUMPER REMOVED, plate lamp); the hood shutting is the loud return.

## 4. Diff vs v3 and render reuse
| v3 clip | v4 | why |
|---|---|---|
| a_open | REUSE, 2x (PNG 1-74 @30, no interpolate) | faster; real frames, no smear |
| b_headlight | REUSE as v3 trim, moved to 2.48 | unchanged content |
| c_front (7.37 s) | NEW 3,4,5,6 | hinge-then-off (note 3), v4 bumper (note 2), one action per kick (note 1) |
| d_mirror | REUSE as-is IF its first/mid/last frames show no hood/bumper/lid zone (base was comp_explode3); else re-render the same keys on comp_explode4 | mirror move is already 0.9 s |
| e_rear (9.8 s) | NEW 8,9,10,11 | lid_v4 hinge-then-off (note 4), v4 bumper, split per kick |
| f_lights (4.9 s) | NEW 12,13 | bumper is now rear_bumper_v4; one light per shot, new angles |
| h_reassemble (4.9 s) | NEW 14,15 | hinge-shut homing + split at the loud return |
| logo | REUSE logo_card_v3.mp4 | - |
New renders: 12 shots. Part-move shots (3,4,5,8,9,10,12,13,14) at native 30 fps, `seconds` = slot + 0.1 (+3 frames), persistent data OFF;
camera-only shots (6, 11, 15) may be 15 fps + minterpolate with +3 source frames. ~880 frames at 30 fps-equivalent cost; render
one at a time, 30 % / 8 spp first/mid/last stills of all 12 before any final. Per-frame luma scan of every render.

## 5. Open questions / checks for the editor
1. hood_t and lid_v4 are outer skin only. Render one still of each at its open angle from the FRONT (hood) / REAR (lid): if the
   underside reads as a mirrored skin, keep cameras 3/4/8 exactly on the hinge side as specified, and shot 9 must have the lid gone
   before the camera reaches the rear view.
2. lid_v4 starts 5 cm forward of its pivot (bbox y 1.541 < 1.5923): at +65 deg that edge dips ~3 cm into the rear glass. Check a
   mid-swing still; if it clips, nudge the pivot or trim the lip.
3. Front label sub: look at the v4 shot-6 still before writing CRASH BEAM (v3's front frame showed bumper leftovers, not a clear beam).
4. Confirm the 2.48 s half-kick on the decoded audio before cutting there. If it is soft, keep the cut anyway only if it lands
   within 1/2 frame of a clear onset; otherwise move it to the nearest clear onset and re-split frames 0-148 between shots 1 and 2.
5. mirror_L carries junk (0.68 m bbox): in shot 14 it is on the far side; clean to its largest island if it shows.
6. Labels: measure scan coverage under every label box across its whole window (4 samples); short subs, never empty.
