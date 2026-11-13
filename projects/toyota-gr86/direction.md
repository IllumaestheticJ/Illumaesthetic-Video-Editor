# Scene direction - toyota-gr86 (BRZ gen 2 hero scan), v5

Scene director, 2026-11-13. Inputs: lessons.md (all), v4 direction (below), feedback.jsonl (2 newest notes), tools/shots_v4.py,
project.yaml (v4 timeline), tools/markers_v5.py, editlog (v5 music + marker entries), part bboxes (`blend/*.json`, parts/side_marker_*.stl),
v4 delivered file `/home/user/media/work/gr86/out/toyota_gr86_v4.mp4` (20-frame sheet). The explode offsets and cameras below were checked
numerically (pinhole projection of comp/explode4 + every part STL, 3D nearest-neighbour clearances; scratch script
`/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/3cfcf361-f3bb-5161-ab4d-e736dbd8d31c/scratchpad/v5/explode_check.py`). This is not
a render check. Every new shot still needs a first/mid/last preview.

## v4 -> v5 changelog
| # | user note on v4 | v5 answer |
|---|---|---|
| 1 | "use this music instead" (GT2 East City) | 122.05 BPM, one shot per BAR (59 frames = 1.967 s; v4 was 2.45 s). 19 one-bar shots + logo, cuts at frames 59n. Two bars of build (bars 0-1, camera-only), the first part move is ON the drop (bar 2) |
| 2 | "make sure all parts are highlighted" | Every scanned part / cut panel gets its OWN bar with its own label (v4 labelled only 7 state beats; the hood, front bumper, lid and rear bumper moved unlabelled; the side markers were never shown). New bar 4 for the side markers. Then a 3-angle exploded view with every part out at once, a reassembly, and the clean car |

## 1. Feature inventory (v5)
| Region | Signature | States (registered, clips.md) | Parts that move | Weak data | Richness -> bars |
|---|---|---|---|---|---|
| **Front** | slat grille, LED headlights, corner intakes | Hood Open (engine bay, 48 %, 3.8 mm); Bumper Hood Removed (front structure, 27.6 %, 3.9 mm); **Side Markers Removed** (90 %, recess fill in front_bumper_v5) | hood_t (cut from car, hinged); front_bumper_v5 (part scan, markers out); **side_marker_R / _L** (part scan "Bomex Side Markers", median 3.5 mm to the bumper) | hood underside never scanned (hinge-side cameras only) | 3 states + 3 part groups -> **5 bars** (2-6) |
| Side | profile | Side Mirrors Removed (92 %, mount) | mirror_R | mirror_L = thin broken capture: never in a close-up, stays home in the explode | 1 state + 1 part -> 1 bar (7) |
| **Rear** | ducktail lid + BRZ badge, twin exhausts | Trunk Open (cargo, z < 875 mm); Rear Bumper Removed (crash beam, 63 %, 3.2 mm) | lid_v4 (cut from car, hinged); rear_bumper_v4 (part scan); reverse_light (part scan, socket side); plate_light (part scan, 2.3 mm) | cargo is a black void from above (<= 30 deg down); propped lid never scanned | 2 states + 4 parts -> **6 bars** (8-13), the richest region |
| Whole | all of the above | - | every part at once | composite base shows every state at once (c5 v3 lesson: check for shards) | explode 3 bars + reassembly 1 + clean hero 1 |
| Top / wheels / interior | - | - | - | nothing new / not scanned | only the closing hero |

Note on rules (unchanged from v4): the hood and lid come OFF only because the user asked for it (v3 note). There is no lid-removed scan. In the explode the lid is shown off the car for the same reason. No other opening is shown without its scan.
Side markers: the car itself is asymmetric at the marker station (car4 x -0.936..0.820 at y -1.70..-1.58, z 0.55-0.75), so the right
marker at x 0.758-0.812 sits ON the skin, the same as the left one at -0.942..-0.865. Not a registration error.

## 2. Order: your proposal is kept, with refinements
Front -> side -> rear -> whole car -> logo, camera always on the car's RIGHT. Why this order holds up against the inventory:
- **Opener**: front-right 3/4 (grille + headlights = signature). Bars 0-1 are the pre-drop build, so they get camera-only moves and no part move (lesson: no transformation on a quiet build).
- **Drop (bar 2)** = the first part move, the hood hinge. **Phrase 2 (bar 10)** = the rear bumper coming off, the bumper-removed hero beat of the richest region.
  **Half-phrase (bar 14)** = the explode. **Phrase 3 (bar 18)** = the clean car. (Phrases assumed every 8 bars from the drop: see open question 1.)
- **Markers before the bumper (bar 4 before bar 5)** is right physically: they are clipped into the bumper corners. They come out first, then the bumper (now markerless) comes off. m1 also stays on the front-right corner, so the travel does not jump.
- **No labels on bars 0-1 or on the explode/reassembly/hero (14-18).** Every part already had its own labelled bar. Ten labels on a 2 s wide would cover the silver and could not be read (0.9 frame/char typewriter). "ALL PART SCANS" would be false, because the hood and lid are cut panels.

## 3. Scene list (bar n starts on frame 59n; Blender m: nose -Y, car's right +X, z up; cam = loc -> target, focal mm, sensor 20.25)
| bar | frames | id | scans / parts | section | ONE action / feature | why here | render | label (title / sub), window local s |
|---|---|---|---|---|---|---|---|---|
| 0 | 0-58 | a_open | car4 | whole | front-right 3/4 arc + push, motion from frame 1 | signature end, build bar | REUSE: PNG 1-59 @30, no interpolate (2x) | - |
| 1 | 59-117 | b_headlight | det_front | front | slide across headlight + slat grille + intake | signature detail next to its wide, build bar | REUSE: s3_wheel trim_start 2.4, 15 fps + minterpolate, 59 frames | - |
| 2 DROP | 118-176 | c1_hood_hinge | hood_t on comp_explode4 | front | hood hinges -50 deg (t 0.05-0.85), holds open | first part move on the drop | REUSE: PNG 1-59 @30 | HOOD / HINGE OPEN, 0.35-1.90 |
| 3 | 177-235 | c2_hood_off | Hood Open fill | engine bay | hood lifts off (gone by 1.10), push into the bay | state the hood reveals | REUSE: PNG 1-59 @30 (camera reaches ~90 % of its push) | ENGINE BAY / HOOD REMOVED, 0.75-1.90 |
| 4 | 236-294 | **m1_side_marker** NEW | side_marker_R/L out of front_bumper_v5 (+ Side Markers Removed recess) | front corner | right marker pops straight out +X 0.15 (t 0.05-0.30, exits its recess), then rises/moves forward to (+0.15,-0.30,+0.30) (t 0.30-0.75, ease out) and holds on black; left marker mirrored (-0.15,-0.30,+0.30), hidden by the car. Lens face toward the camera, **no spin** (turn only if a render shows a scanned back worth showing) | the one part never shown in v1-v4 | NEW, 30 fps, 59+3 frames, persist OFF. Cam (1.70,-2.40,0.55)->(0.80,-1.62,0.75) f30 -> end (1.62,-2.30,0.58)->(0.80,-1.62,0.78) f32 (slow push). Checked: end pose 0 % over silver, 0.30 m clear of the body, ~258 px tall, inside the frame (x -0.64..-0.32, y +0.31..+0.58 of half-frame). Hood at HOOD_GONE, rear group home, mirrors home | SIDE MARKER / PART SCAN, 0.40-1.90 (singular: only the right one is on screen) |
| 5 | 295-353 | **c3b_front_bumper_off** NEW | front_bumper_v5 | front | v4 c3 keys: pull straight -Y 0.30 (0.05-0.40), tip +110 deg X and drop out bottom-right (0.40-1.10) | bumper part scan, now without its markers | NEW (v4 c3 camera + keys, front_bumper_v5, both markers parked at +Z 9 = out of frame), 30 fps, 62 frames | FRONT BUMPER / PART SCAN, 0.35-1.90, in the band the departing bumper does NOT cross (measure) |
| 6 | 354-412 | c4_front_structure | Bumper Hood Removed | front structure | push-in, decelerating hold | bumper-removed hero beat (rule C) | REUSE: 15 fps + minterpolate, **trim_start 0.48** (keeps the readable near-still end) | FRONT BUMPER REMOVED / CRASH BEAM, 0.10-1.90 (v4 wording, user did not object) |
| 7 | 413-471 | d_mirror4 | mirror_R, Side Mirrors Removed | side | right mirror off (0.05-0.85), push on the mount | travel back along the right side | REUSE: PNG 1-59 @30 | SIDE MIRROR REMOVED / MIRROR MOUNT, 0.40-1.90 |
| 8 | 472-530 | e1_lid_hinge | lid_v4 | rear deck | lid hinges +65 deg (0.05-0.85) | rear opens with its own phrase-half | REUSE: PNG 1-59 @30 | TRUNK LID / HINGE OPEN, 0.35-1.90 |
| 9 | 531-589 | e2_lid_off_cargo | Trunk Open | cargo | lid lifts off (gone 1.05), camera to cargo <= 30 deg down | trunk-open state | REUSE: PNG 1-59 @30 | TRUNK OPEN / CARGO AREA, 0.80-1.90 |
| 10 PHRASE | 590-648 | e3_rear_bumper_off | rear_bumper_v4 (+ lights) | rear | pull +Y 0.30, tip, drop (0.05-1.10) | richest region's hero on phrase 2 | REUSE: PNG 1-59 @30 | REAR BUMPER / PART SCAN, 0.35-1.90 |
| 11 | 649-707 | e4_rear_beam | Rear Bumper Removed | rear structure | push-in on the holed beam + silencer, hold | bumper-removed hero beat (rule C) | REUSE: 15 fps + minterpolate, **trim_start 0.48** | REAR BUMPER REMOVED / CRASH BEAM, 0.10-1.90 |
| 12 | 708-766 | f1_reverse_light | reverse_light | rear part | lifts off the parked bumper (0.05-0.65) | part scan | REUSE: PNG 1-59 @30 | REVERSE LIGHT / PART SCAN, 0.40-1.90 (v4: bottom band) |
| 13 | 767-825 | f2_plate_light | plate_light | rear part | lamp lifts, turns upright, lands (0.05-1.20) | part scan, the last single part | REUSE: PNG 1-59 @30 (0.77 s hold after landing) | LICENSE PLATE LIGHT / PART SCAN, 0.60-1.90 |
| 14 HALF | 826-884 | **x1_explode_fr** NEW | all parts, comp_explode4 base | whole | every part flies to its exploded offset (section 4), motion from frame 1 | half-phrase = the all-parts moment | NEW, cam (2.30,-6.40,4.60)->(-0.38,-0.45,0.59) f30 -> f31.7 (push; f31.7 = exact fit) | - |
| 15 | 885-943 | **x2_explode_rr** NEW | same animation, window 1.967-3.933 | whole | parts hold (slow outward drift +6 %), rear end toward the lens | rear group (lights, bumper, lid) reads here | NEW, cam (2.50,6.60,4.40)->(0.02,0.45,0.34) f34 -> f35.8 | - |
| 16 | 944-1002 | **x3_explode_high** NEW | same animation, window 3.933-5.900 | whole / top | parts hold, drift; car length along the frame height, nose up (A90 lesson) | only near-top view of the exploded set; fills 9:16 (y +-0.76) | NEW, cam (1.70,5.60,7.00)->(0.11,0.33,0.17) f40 -> f42.8 (~51 deg down, never overhead) | - |
| 17 | 1003-1061 | **h1_reassemble_v5** NEW | same animation, window 5.900-7.867 | whole | all parts home; last (hood) lands ON frame 1062 | closes the explode on the bar | NEW, cam (4.40,1.15,9.10)->(0.12,-0.05,0.80) f26 -> **exactly h2's first camera** (2.80,0.70,6.20)->(0,-0.05,0.80) f26 (push-in as the parts close in) | - |
| 18 PHRASE | 1062-1120 | h2_hero | car4 (clean) | whole / top | swap to the clean car on the cut, rise, fade | c5 lesson: clean car on a kick | REUSE: 15 fps + minterpolate, first 59 frames, fade st 0.95 d 0.95 | - |
| 19 | 1121-~1195 | logo | logo_card_v3.mp4 | end | 860 px logo | energy falls at frame ~1180, logo rides the decay | REUSE | - |

Label rules (all part/state bars): title in at the given local start, out 2 frames before the cut, subs <= 12 chars, `sub` never empty,
`shadow: true`, band chosen by measured scan coverage over 4 samples of the window. Every label is over scan only, with wording from the scan file names.

## 4. Exploded arrangement (offsets in Blender m from each part's home; one part animation, local t from frame 826)
| part | offset (dx, dy, dz) | route out (straight unless stated) | clearance to body / nearest part (m) |
|---|---|---|---|
| hood_t | (0, -0.25, +0.85) | flat, straight up/forward (away from the glass), no hinge | 0.74 / 0.86 |
| lid_v4 | (0, +0.25, +0.75) | flat, straight up/back | 0.45 / 0.82 |
| front_bumper_v5 | (0, -0.80, 0) | straight out -Y | 0.20 / 0.51 |
| side_marker_R | (+0.55, -0.75, +0.30) | +X 0.12 first (out of recess), then to its pose | 0.90 / 0.52 |
| side_marker_L | (-0.55, -0.75, +0.30) | mirrored | 0.87 / 0.51 |
| mirror_R | (+0.60, 0, +0.40) | +X first, then up | 0.64 / >1 |
| mirror_L | (0, 0, 0) stays home | broken capture; mostly hidden by the car from all four cameras (55-100 %) | - |
| rear_bumper_v4 | (0, +0.80, 0) | straight out +Y | 0.23 / 0.29 |
| reverse_light | (0, +1.20, -0.25) | rides the bumper to t 0.25, then out of its slot +Y and down below the bumper | >1 / 0.36 |
| plate_light | (+0.50, +1.05, +0.20) | rides the bumper to t 0.25, then down out of its recess, then +X/+Y | >1 / 0.29 |
Timing: big panels (hood, lid, both bumpers) t 0.00-0.50 ease out; small parts (markers, mirror, lights) t 0.10-0.60. All of them are out by 0.6 s.
From 0.60 to 5.90, every offset grows linearly by 6 % so that no frame is dead, with no rotation.
Reassembly (h1, local 5.90-7.867): lights back into the bumper 5.90-6.35, rear bumper home 6.10-6.65, lid 6.30-6.85, mirror_R 6.50-7.00,
markers 6.70-7.20, front bumper 6.95-7.45, hood 7.25-7.867 lands on frame 1062. Landings ease "in", reversing the routes above.
Projected fit (all parts + base, half-frame units, target +-0.92): x1 x +-0.88 / y +-0.47; x2 +-0.88 / +-0.55; x3 +-0.88 / +-0.76; h1 start +-0.93 / +-0.29.
What reads in each view: x1 shows the front group (bumper 2 % over silver, markers on black, mirror on black, hood 58 % over the glass:
check that its edge reads). x2 shows the rear group (bumper 1 %, both lights 0 %, lid 55 % over the deck). x3 shows everything except mirror_L,
with the lid 78 % over the deck. Parts at the far end are hidden by the car in x1/x2 (rear bumper 61 % in x1, front bumper 28 % in x2), which is intended.
Run `projects/porsche-gt3rs-992/tools/clipcheck.py` on the fly-out and reassembly paths (lights and markers exit recesses).

## 5. Music map (122.05 BPM, bar 1.9664 s; video frame 59n vs song bar drifts 0.3 ms/bar = 6 ms by bar 19)
| bar | frame | video s | song s | music | shot |
|---|---|---|---|---|---|
| 0 | 0 | 0.000 | 79.402 | build | a_open |
| 1 | 59 | 1.967 | 81.368 | build | b_headlight |
| 2 | 118 | 3.933 | 83.335 | **DROP** | c1 hood hinge |
| 3-9 | 177..531 | 5.900..17.700 | 85.301..97.100 | phrase 1 | c2, m1, c3b, c4, d, e1, e2 |
| 10 | 590 | 19.667 | 99.066 | **phrase 2** | e3 rear bumper off |
| 11-13 | 649..767 | 21.633..25.567 | 101.032..104.965 | | e4, f1, f2 |
| 14 | 826 | 27.533 | 106.932 | **half-phrase** | x1 explode |
| 15-17 | 885..1003 | 29.500..33.433 | 108.898..112.831 | | x2, x3, h1 |
| 18 | 1062 | 35.400 | 114.797 | **phrase 3** | h2 clean hero |
| 19 | 1121 | 37.367 | 116.764 | energy falls 118.73 = frame ~1180 | logo to ~1195 |
Every clip is 59 frames. Use exact frames per clip with plain concat (`projects/honda-s2000/tools/concat_assemble.py`), or keep the v4 rule that the first clip is one frame short with `ive assemble`.
Then put each cut on the measured onset of the decoded audio. Note: the lessons say kick-band onsets on rolling-bass tracks sit 30-110 ms off the grid.

## 6. Diff vs v4 and render reuse
- Moved / trimmed only (13 reused): a_open, b_headlight, c1, c2, c4, d_mirror4, e1, e2, e3, e4, f1, f2, h2. All now 1 bar. Part-move shots use PNG 1-59. Camera-only c4/e4 use trim_start 0.48.
- Added: m1_side_marker (bar 4), x1/x2/x3 explode (bars 14-16, ONE animation rendered from 3 cameras in t0 windows).
- Re-rendered: c3b (front_bumper_v5, markers parked out of frame), h1_reassemble_v5 (new timing, starts from the explode poses, ends on h2's first camera).
- Dropped: v4 h1 (rear-right high reassembly, which hinged the hood and lid shut). Its view is now x3's job.
- New renders: 6 shots, about 7 bars at 30 fps, persist OFF for all part moves, +3 frames each, luma scan of every frame. First do 30 % / 8 spp first/mid/last previews of all 6, plus m1 at t 0.30 and x1 at t 0.30.
- Expected `ive director` flags to log, not cut: a_open vs x1 (both front-right; x1 is 35 deg higher and exploded); h1 end == h2 start (deliberate clean-car swap);
  x2 vs x3 (both behind-right; 35 vs 51 deg down, length horizontal vs vertical); c4/e4 close-up silhouettes as in v4.

## 7. Open questions for the editor
1. Phrase lines: is bar 10 a real section lift and bar 14 a sub-lift in East City? Make a per-bar brightness table (2-6 kHz / 6-11 kHz, STI eurobeat lesson). If the lift is at bar 12 or 16 instead, move the explode start to it and give the spare bar to the rear beam hold (e4 2 bars). Do not stretch the explode.
2. Side marker back side: render side_marker_R alone from behind. If the socket/clip side was scanned, a 90 deg turn in m1 (t 0.75-1.20) is justified. Otherwise keep it as a pure translate.
3. front_bumper_v5 recess (Side Markers Removed fill): look at the m1 last frame at final res. If the recess is a hole or shards, crop m1 tighter on the marker and keep the corner out of the label band.
4. comp_explode4 base shows the bay, front structure, cargo and beam at once. In x3 (near-top), check for duplicate-skin shards (c5 v3 lesson). If they appear, swap to car4 minus the parts for x3 only.
5. h1 start pose (4.40,1.15,9.10) fits at +-0.93 by projection, which is on the edge. If the preview clips the reverse/plate light, move the target +0.05 toward them or go to f25.

---

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
