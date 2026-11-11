# Ferrari 296 GTB - director's plan v3

Inputs: feedback.jsonl (newest: "needs to focus on specific sections"; "if you open the hood, hold that shot and also pull
the front bumper out and show off the bumper"; "minimize redundant frames"), director_report_v2.md (no focus tags;
s1_wide ~ s8c_wide IoU 0.68), contact sheets of every v2 render (`/tmp/claude-0/director/*.jpg`), lessons.md, Temerario
notes, shots.py / shot.py (part `pivot` defaults to the part's bbox centre; `loc` moves the pivot, `rot` is XYZ degrees
about it).

## Diagnosis of v2 (from the sheets, not just the report)
- The FRONT is told three times in three separate shots: s4_nose (lamp/intake), s5_hood (hood opens, then ~2 s of a
  static open hood), s8a_front (bumper slides, fender, and the hood flies off *again*). The hood opening is shown twice.
- s8c_wide: parts are home by ~1/2 of the shot, then a low rear-right 3/4 of the assembled car holds ~2.3 s - the
  report's repeat of s1_wide.
- s8b_side starts with the fender already gone and front parts at the old offsets - no continuity with anything before.
- Good and reusable as-is: s1_wide (whole car, clean), s2_rear (rear-left 3/4 orbit to left flank), s3_wheel (extreme
  close-up, brake through the spokes), s6_engine (louvre lift is readable), s7_top (rear-high to top-down).

## Structure v3 (one section per stretch; the front is ONE held shot)
WHOLE -> REAR -> TOP -> WHEEL -> FRONT (hood open, bumper out + turned, ~8.7 s, no cut) -> ENGINE -> SIDE explode ->
WHOLE explode + reassembly LOCK on 32.350 -> LOGO. Disassembly runs 14.9-32.35 s (about half the reel, like the
Temerario) and is progressive: front, then rear lid, then right flank, then everything flies home.

Cut frames (round(t*30)): 0, 152, 292, 361, 431, 692, 762, 901, 1040, end 1170.
`beats: [5.067, 9.733, 12.033, 14.367, 23.067, 25.4, 30.033, 34.667]`

| # | section | shot id | video s (frames) | focus | camera (scan frame, m) | part action (video s) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|---|
| 1 | whole | s1_wide | 0.000-5.067 (0-152) | whole car, front-right 3/4 | unchanged: orbit r 7.4, -36 -> -66 deg, h 1.25-1.35, 30 mm | - | establishes the car whole (v1 note "too cropped") | REUSE (77 fr) |
| 2 | rear | s2_rear | 5.067-9.733 (152-292) | rear haunch + left flank | unchanged: orbit r 5.2->5.0, 148 -> 120 deg, h 0.85->1.3 | - | only rear/left-side view in the reel | REUSE (71 fr, uses 70) |
| 3 | top | s7_top | 9.733-12.033 (292-361) | roofline / planform | unchanged: high rear-LEFT (2.2,4.6,4.0) -> straight down (0,0.25,6.9) | - | moved up from 20.7: starts on the rear-left where s2 ends (same screen side), so it reads as one move; top-down is a requested beat | REUSE (36 fr, uses 35) |
| 4 | wheel | s3_wheel | 12.033-14.367 (361-431) | front-right wheel, carbon-ceramic disc through the spokes | unchanged: (-2.25,-0.95,0.42) -> (-2.15,-1.75,0.40), target wheel (-0.95,-1.45,0.36), 40 mm | - | extreme close-up on the music drop (12.04); ends looking forward along the right fender = hand-off to the front | REUSE (36 fr, uses 35) |
| 5 | front | **f5_front** (new) | 14.367-23.067 (431-692), 8.70 s, NO CUT | 14.37-14.94 headlamp; 14.94-16.68 hood -> frunk; 16.68-23.07 **front bumper, inner face** | keyed table below: starts low front-right on the lamp, rises as the hood opens to look into the frunk, drops and swings round to the car's right side of the pulled bumper as it turns, then pushes in on its inner face | hood (pivot (0,-0.86,0.88)) opens 14.940->16.100 to rot X -58 (ease inout) and STAYS open; bumper slides forward/down 16.681->17.842 to loc (0,-1.00,-0.10) (ease out); on the 18.423 accent it travels on to (0,-1.70,-0.10) while turning about the VERTICAL axis to rot Z +90 by 20.164 (ease inout), inner face now facing the camera (-X); slow lin creep to rot Z +105 by 23.067 | the reviewer's request verbatim: hold the hood shot, pull the bumper out and show it off; merges s4 + s5 + s8a (three front shots) into one. Inner skin was scanned, so the turn shows real data | NEW 132 fr |
| 6 | rear (engine) | s6_engine | 23.067-25.400 (692-762) | engine-cover louvre lifting off the engine bay | unchanged: high rear (1.35,3.6,2.55) -> (0.75,3.35,2.75), target (0,1.75,0.8) | louvre lifts 23.65 -> 24.81 (beats 1-3 of the shot, already rendered) | cut on 23.066, the loudest accent: the hard jump from front to rear lands on the lift. Front is out of frame, so the reset to an assembled car is not visible | REUSE (36 fr, uses 35) |
| 7 | side | **x_side** (new) | 25.400-30.033 (762-901) | right flank: front fender, side skirt, then rear bumper + diffuser | low along the right sill, ~18 deg down (lesson: level cameras make panels slivers): (-3.30,-1.60,0.95) tgt (-0.70,-0.60,0.40) -> (-3.40,1.20,1.05) tgt (-0.60,1.90,0.45), 28 mm, ease inout; key every 0.58 s (lerp) | static from shot start: hood open (rot X -58), bumper at its f5 end pose, louvre open (rot X 85 about (0,1.63,0.9)) - i.e. the car as the previous shots left it. Fender 25.400->26.548 to (-0.50,0,+0.45) rot (0,-10,0) [out and UP, not at the lens]; skirt 25.981->27.129 to (-0.40,0,-0.28) [down]; rear bumper 27.708->28.868 to (0,0.95,0.05) on the accent; diffuser 28.288->29.449 to (0,0.75,-0.35). all ease out | progressive explode the reviewer asked for on v1 ("zoom in on bumpers/side skirts"); one subject per beat, camera tracks front-to-rear with the order parts come off | NEW 71 fr |
| 8 | whole (explode) | **x_lock** (new) | 30.033-34.667 (901-1040) | every part out, then the reassembly LOCK | high right side, looking down ~27 deg: arc() c (0,0.2,0.5)->(0,0.1,0.5), r 7.6->6.4, angle -95 -> -105, h 4.2->3.4, 30 mm, tz 0.4, 8 keys. NOT a low 3/4 (that is s1) | all parts at their out poses x1.00 at 30.033, drift to x1.04 by 31.189 (lin); fly home 31.189->32.350 ease in, LOCK on 32.350; bumper first un-turns: 31.189->31.770 rot Z 105->0 at loc (0,-1.00,-0.10), then home 31.770->32.350; hood and louvre close (rot -> 0) 31.189->32.350 ease in | the only view of the whole exploded car + the requested reassembly; high side-on is a new angle (planform + profile), not the opening | NEW 71 fr |
| 9 | logo | logo | 34.667-39.000 (1040-1170) | Illumaesthetic logo | logo_card.mp4 unchanged | - | brief; over the track's fade | REUSE |

Section seconds: whole 5.07 + explode-whole 4.63, rear 4.67, top 2.30, wheel 2.33, front 8.70, engine 2.33, side 4.63,
logo 4.33 = 38.97 s (unchanged length, unchanged music).

### f5_front camera keys (video s; shot t = video - 14.367; key every ~1 beat, ease inout unless noted)
| video s | shot t | loc | target | focal | what is in frame |
|---|---|---|---|---|---|
| 14.367 | 0.000 | (-1.60,-3.60,0.85) | (-0.55,-2.00,0.68) | 32 | right headlamp + hood edge (lamp, not the ragged grille) |
| 14.940 | 0.573 | (-1.75,-3.85,1.05) | (-0.40,-1.90,0.65) | 32 | hood starts to lift |
| 16.100 | 1.733 | (-2.05,-4.35,1.90) | (0.00,-1.40,0.70) | 30 | hood fully open, looking down into the frunk |
| 16.681 | 2.314 | (-2.25,-4.40,1.85) | (0.00,-1.50,0.65) | 30 | frunk (1 beat, camera keeps drifting - frunk has dark holes, do not dwell) |
| 17.842 | 3.475 | (-2.80,-4.55,1.35) | (-0.05,-2.55,0.50) | 30 | bumper slid out in front of the open nose |
| 18.423 | 4.056 | (-3.05,-4.45,1.25) | (-0.05,-2.75,0.48) | 30 | turn begins on the accent |
| 19.003 | 4.636 | (-3.35,-4.15,1.15) | (-0.05,-3.05,0.46) | 30 | |
| 19.584 | 5.217 | (-3.55,-3.75,1.05) | (-0.05,-3.30,0.45) | 30 | |
| 20.164 | 5.797 | (-3.60,-3.45,1.00) | (-0.05,-3.45,0.45) | 30 | bumper side-on, whole inner face, nose + open hood behind (screen-left) |
| 21.326 | 6.959 | (-3.05,-3.45,0.90) | (-0.05,-3.43,0.44) | 31 | push in |
| 23.067 | 8.700 | (-2.45,-3.40,0.80) | (-0.05,-3.40,0.42) | 34 (ease out) | crops into the inner skin / mounting edges |

Parts for f5_front: base `comp_explode.blend`; animated `x_hood` with pivot (0,-0.86,0.88) (same hinge as v2 s5_hood) and
`x_fbumper` with pivot (0,-1.775,0.475) (its bbox centre); `x_fender`, `x_skirt`, `x_ecover`, `x_rbumper`, `x_diffuser`
present with all-zero keys so the car is complete apart from the hood/bumper. Clearance checked: hood tip opens to
~(y -1.47, z 1.86); with the bumper centre at y >= -2.78 before the turn starts and -3.48 at 20.16, its +X wing swings
to y ~ -2.5 (nose at -2.27) - nothing sweeps into the car; nearest bumper point to the camera stays >= 1.9 m, and the
bumper moves forward-across, never down the lens axis. Editor: verify frame 1 of f5_front against s3_wheel's last frame
for a clean comp (no seams at the bumper/fender joints) before the full render.

Implementation hint (shots.py): add `T8.update({"f5_front": 431/30, "x_side": 762/30, "x_lock": 901/30})`, a v3
`PARTS_G3` dict with per-part key lists in video seconds (the out/turn/home keys above), and reuse `parts_for` with
the per-part pivot passed through. Hood/louvre stay hinged (rot about their pivots) - they are not translated in v3.

## Cut list (v2 -> v3)
| v2 shot | v2 time | verdict | reason |
|---|---|---|---|
| s4_nose | 12.03-14.37 | CUT (merged) | front subject #1 of 3; its lamp detail becomes the first 0.6 s of f5_front. The intake in it shows the ragged grille gaps |
| s5_hood | 14.37-18.43 | CUT (merged) | front subject #2; ~2 s of static open hood. Replaced by f5_front, where the open hood leads into the bumper |
| s8a_front | 23.07-27.70 | CUT | front subject #3, and it opens the hood a second time (flies it up) - pure repeat |
| s8b_side | 27.70-30.03 | CUT (re-staged as x_side) | fender already gone at frame 1 and front parts at the old offsets: no continuity; v3 side shot starts with the car as f5/s6 left it |
| s8c_wide | 30.03-34.67 | CUT (replaced by x_lock) | low rear-right 3/4 assembled hold = repeat of s1_wide (IoU 0.68) |
| s6_engine | was 18.43 | MOVED to 23.07 | unchanged frames; now the hard cut front->rear sits on the loudest accent |
| s7_top | was 20.74 | MOVED to 9.73 | unchanged frames; continues s2's rear-left side instead of following the engine |

## Hold list (> 0.75 s with little or no part motion)
| shot | video s | length | reason |
|---|---|---|---|
| f5_front | 20.164-23.067 | 2.90 s | the "show off the bumper" beat: the camera pushes ~1.2 m in on the scanned inner face and the bumper creeps +15 deg - the reviewer asked for exactly this; it is never static |
| x_lock | 32.350-34.667 | 2.32 s | the assembled car after the lock on the heaviest bass, seen high side-on (new angle); camera keeps pushing in; ends on the logo cut |
| logo | 34.667-39.000 | 4.33 s | end card over the track's fade (brief) |
Nothing else holds: frunk view is 0.58 s with camera moving; every reused shot is a continuous move.

## Render budget (15 fps, 810x1440, 12 spp, final settings unchanged)
- NEW: f5_front 132 fr, x_side 71 fr, x_lock 71 fr = **274 frames** (~50-115 min at 11-25 s/frame). Render one at a
  time, in fresh Blender processes of <= 40 frames each (comp_explode + 7 parts: Cycles persistent data went black
  after ~48 frames in v1), then run the per-frame max-luma scan. Order: f5_front first (the feedback shot), preview
  at 30 % before the final.
- REUSED unchanged: s1_wide (77), s2_rear (71), s7_top (36), s3_wheel (36), s6_engine (36), logo_card.mp4.
- Retired: s4_nose, s5_hood, s8a_front, s8b_side, s8c_wide (keep the folders; do not delete).

## Notes for the editor
- Tag every clip in project.yaml with `section:` and `focus:` exactly as the table says, so `ive director` stops flagging.
- No text, no HUD, no dissolves; all transitions are hard cuts on the frames above.
- Log each change with `ive log ... --why` citing the 09:36 feedback notes.
