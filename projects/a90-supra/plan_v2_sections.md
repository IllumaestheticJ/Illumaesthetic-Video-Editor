# A90 Supra v2 - section-by-section disassembly plan (implementable)

Request: "thoroughly plan this video, splitting and highlighting each individual section of the car as we disassemble
it", Temerario style. Scene order and data inventory: `direction.md` (scene-director stage). This file is the
director stage: every shot, part motion, highlight, label, music cue, render budget and risk. **Plan only - nothing
here has been final-rendered.** Framing was checked at 30 % (sheets listed at the end).

Source of truth for all numbers below: `tools/plan_v2.py` (generates `shots_v2/*.json`). Change the plan there and
re-run `python3 projects/a90-supra/tools/plan_v2.py`; never hand-edit the JSONs (the explode state is computed once
on the reel timeline so it stays continuous across cuts).

## 0. Rules this plan follows (and how)
| Rule (source) | How |
|---|---|
| Temerario: ~4 s shots, soft ~0.3 s transitions, explode starts in a front-corner close-up and runs ~half the reel over several angles, layers clear of the body, reassembly, fade, small logo (user, plan_v2.md) | 9 shots, 0.3 s blends on bar lines, first separation 7.0 s, explode 7-36 s (29 s of 41.5) across 6 angles, reassembly lock 36.0, fade 37-38, logo 38-41.5 |
| Travel, no ping-pong; each section ONE continuous sequence (scene-director, coordinator B) | whole -> front bumper -> front corner -> right side -> rear bumper -> rear corner -> line-up -> reassembly |
| Camera stays on the section being removed, moves in, shows the part off (lessons mazda-miata-nc, director.md) | each section shot is framed on its section; bumpers tip to show their scanned insides; push-ins on the revealed structure |
| Bumper-removed data = hero beat, hold on what is behind (coordinator C) | v03 and v06 are 6-8 s; 2.1-2.4 s push-in + hold on Under Front Bumper / Under Rear Bumper |
| Only show states that were scanned (lessons honda-s2000, coordinator D) | no hood, trunk, door, roof opening. Every removed panel has a registered part scan AND the state scan of what is under it (below) |
| Spin/flip only when the back is worth showing (lessons c5, gt3rs) | only the two bumpers rotate (115 deg, inside verified in v1). Side panels/fender tilt 35 deg toward the lens (lesson s2000: panels from a level camera read as slivers) - a tilt, not a flip. Corner parts only translate |
| Parts move into clear background, not across the body (gt3rs) | bumpers up + fore/aft; corner parts outboard (-Y, toward the camera) and below/forward of the arch; side panels down + outboard |
| Whole car in wide shots, detail shots fill the frame (coordinator A) | v01, v09 whole car with margin; section shots crop into the car on purpose (checked first/mid/last frames) |
| No ground, house silver on black | unchanged house look; only the optional highlight material is new |

## 1. Timeline (120 BPM, beat 0.5 s, bar 2.0 s; total 41.5 s)
`ive beats` must confirm 120 BPM on the rendered score (shared engine; v1 read an octave error - trust the onset list).

| Shot | Reel s | Window rendered (pre-roll + 0.1 s tail) | Focus (ONE) | Transition in |
|---|---|---|---|---|
| v01_whole | 0.0-4.0 | 0.0-4.1 | whole car with wheels + suspension | fade up from black 0-1.2 s |
| v03_fbump | 4.0-12.0 | 3.7-12.1 | front end: front bumper -> radar module -> crash structure behind | 0.3 s dissolve ending on 4.0 |
| v04_fcorner | 12.0-16.0 | 11.7-16.1 | front corner: fender section, FR wheel, caliper, rotor, coilover | 0.3 s dissolve ending on 12.0 |
| v05_side | 16.0-20.0 | 15.7-20.1 | right side: door trim, upper skirt, lower skirt -> structure under them | 0.3 s dissolve on 16.0 |
| v06_rbump | 20.0-26.0 | 19.7-26.1 | rear bumper -> structure behind it (Under Rear Bumper) | 0.3 s dissolve on 20.0 |
| v07_rcorner | 26.0-30.0 | 25.7-30.1 | rear corner: RR wheel, caliper, rotor, spring, damper | 0.3 s dissolve on 26.0 |
| v08_lineup | 30.0-34.0 | 29.7-34.1 | full exploded line-up (the only shot that shows every section at once) | 0.3 s dissolve on 30.0 |
| v09a_reasm | 34.0-36.0 | 33.7-36.1 | reassembly, everything locks on 36.0 | 0.3 s dissolve on 34.0 |
| v09b_clean | 36.0-38.0 | 36.0-38.1 | clean car (car.blend), fade to black 37.0-38.0 | **hard cut on 36.0** (same camera: the swap from composite to clean scan is invisible, lesson c5) |
| logo | 38.0-41.5 | - | ILLUMAESTHETIC logo, ~25 % width (270 px), centred on black | fade in 38.2-38.9, hold, fade out 40.6-41.5 |

Transitions: each dissolve starts 0.3 s before the bar line and ENDS on it, so the incoming shot's first full frame and
the music hit coincide; that is why every window starts 0.3 s early (the pre-roll is the same parked state - continuity
is exact because both shots sample one timeline). Lesson: a dissolve overlaps clips - give each incoming clip the
0.3 s extra `dur` or the reel ends short.

## 2. Sections - parts, motion, end position, highlight
Coordinates: car frame (m), nose +X, right side -Y, floor z=0. `loc` = offset from the assembled position; `rot` =
degrees about the part's own bbox centre (x,y,z). Ease per segment. Releases are on beats (cue list section 5).

### A. Front bumper (v03, 4.0-12.0) - hero 1
| Part (.blend) | Motion | Parked at (from 9.6 / 10.2 s) |
|---|---|---|
| `n_fbump_norad` (Front Bumper Outside+Inside union, radar module carved out; lite `L_fbump_norad` after v03) | 7.0-8.0 slide forward +0.40 (ease_out); 8.0-9.6 rise and tip: loc [1.20,-0.10,1.25], rot [0,115,0] (ease_in_out) - the scanned INNER face turns up toward the camera | [1.20,-0.10,1.25] rot y115: above and in front of the nose (leaves the top of frame during the push-in) |
| `n_radar_mod` (Radar Cover + Radar Mounting Grille) | 7.0-8.0 rides out with the bumper (+0.40 x); 9.0-10.2 drops out of it and slides to [0.70,+1.25,-0.02] (left-front, clear black; fully out of frame by the end of the push-in) | left of the nose, at intake height |
Revealed: `base_v2` front = Under Front Bumper state scan (crash beam, radiators/condenser, ducts, mounts) + liners.
Camera (reel-time keys): 3.7 az-33 d4.6 z0.70 look(1.10,-0.05,0.45) -> 6.6 az-40 d3.0 z1.0 look(1.75,-0.20,0.42) [push
on the face] -> 8.7 az-38 d4.6 z1.7 look(2.40,-0.15,0.80) [rise with the bumper, whole nose + tipped bumper in frame]
-> 9.9 az-34 d4.4 z1.6 [hold: inside of the bumper + radar module readable] -> 12.1 az-24 d1.45 z0.62
look(2.00,-0.15,0.30) [push IN on the crash structure; bumper leaves the top of frame]. Lens 35, linear time + Catmull.
Highlight: bumper rim pulse 7.0 (0 -> 1 in 0.25 s, 0.3 by 8.4, holds to 12.0, off by 12.5); radar module pulse 9.0.

### B. Front corner (v04, 12.0-16.0)
| Part | Motion | Parked |
|---|---|---|
| `fender` (Supra Fender = lower-rear section of the RH front fender) | 12.5-13.5 out -0.80 y, -0.05 z, tilt -35 deg about X (outer face toward the lens) | outboard of the door, below sill height |
| `p_FR_wheel` (lite `L_FR_wheel`) | 13.0-14.0 [+0.50,-0.80,-0.05] | forward-outboard of the arch (clears the hub for the camera) |
| `p_FR_caliper` | 13.5-14.0 lift off the disc [0,-0.08,+0.28] (ease_out), 14.0-14.6 out to [0,-0.55,+0.30] | above the rotor, outboard |
| `p_FR_rotor` | 14.0-14.8 out -0.62 y | outboard of the hub |
| `p_FR_coilover` | 14.5-14.9 drop -0.14 z (clears the strut tower), 14.9-15.5 out to [0,-0.36,-0.14] | in front of the arch, lowered |
| `L_corner_FL` (left corner, one unit = mirrored right scans) | 13.0-14.2 +0.85 y | outboard left (seen in v08) |
Revealed: Under Fender state (inner fender structure / washer bottle area) + arch liner; hub area of the stripped car.
Camera: az-55 d2.5 z2.1 look(1.15,-0.95,0.25) -> t.55 az-68 d2.4 z1.9 -> t1 az-78 d2.0 z1.45 look(1.20,-1.15,0.22). Lens 32.
Highlight: each part pulses on its release (12.5, 13.0, 13.5, 14.0, 14.5); bumper + radar dim to 0.6 from 12.0.

### C. Right side (v05, 16.0-20.0)
| Part | Motion | Parked |
|---|---|---|
| `n_dtrim` (Supra Door Trim = side-intake trim behind the door) | 16.5-17.4 [0,-0.62,+0.10], rot x-35 | outboard of the door |
| `n_uskirt` (Supra Upper Skirt) | 17.5-18.5 [0,-0.50,-0.38], rot x-35 | below + outboard of the sill |
| `n_lskirt` (Supra Lower Skirt) | 18.5-19.5 [0,-0.42,-0.70], rot x-35 | lowest layer |
Revealed: `Supra Under Door Trim` + `Supra Chassis Under Upper Skirt` spliced into base_v2 (sill/rocker and door structure).
Camera: az-90 d2.5 z2.3 look(0.10,-1.10,0.05) -> az-90 d2.3 z2.1 look(-0.45,-1.10,0.05): high side, ~43 deg down, tracks
rearward with the releases. Lens 38. Highlight: pulses 16.5 / 17.5 / 18.5; all front parts dimmed 0.6.

### D. Rear bumper (v06, 20.0-26.0) - hero 2
| Part | Motion | Parked |
|---|---|---|
| `rbump` (Rear Bumper Outside+Inside union; lite `L_rbump` elsewhere) | 21.0-22.0 slide aft -0.40 (ease_out); 22.0-23.6 rise + tip to [-1.20,-0.25,1.00], rot [0,-115,0] - inner face up | above and behind the tail |
Revealed: **Supra Under Rear Bumper** (843 k tris spliced, fills v1's hollow tail: rear crash beam, exhaust, mounts).
Camera: az-150 d2.6 z1.05 look(-1.95,-0.10,0.45) [rear end fills the frame] -> t.40 az-150 d4.0 z1.75
look(-2.50,-0.10,0.80) [rise, bumper + tail in frame with margins] -> t.62 az-152 d3.9 z1.65 [hold on the inside] -> t1 az-156 d1.45 z0.62 look(-2.0,-0.15,0.32) [push IN, hold on the
under-rear-bumper structure 24.5-26.0]. Lens 35. Highlight: pulse 21.0; front + side parts dimmed.

### E. Rear corner (v07, 26.0-30.0)
| Part | Motion | Parked |
|---|---|---|
| `p_RR_wheel` (lite `L_RR_wheel`) | 26.5-27.5 [-0.25,-0.85,0] | aft-outboard of the arch |
| `p_RR_caliper` | 27.0-27.5 lift [0.06,-0.06,0.26], 27.5-28.1 out to [0.06,-0.55,0.28] | |
| `p_RR_rotor` | 27.5-28.3 -0.62 y | |
| `p_RR_spring` | 28.0-28.4 drop -0.10, 28.4-29.0 to [0.12,-0.42,-0.10] | |
| `p_RR_damper` | 28.5-28.9 drop -0.16, 28.9-29.5 to [-0.12,-0.30,-0.16] | |
| `L_corner_RL` | 26.5-27.7 +0.85 y | |
Camera: az-125 d2.5 z2.1 look(-1.20,-0.95,0.25) -> t.55 az-112 d2.5 z1.9 -> t1 az-104 d2.2 z1.5 look(-1.35,-1.15,0.20). Lens 32.
Highlight: pulses 26.5 / 27.0 / 27.5 / 28.0 / 28.5; everything else dimmed; all dims release 29.4-30.0 for the line-up.

### F. Line-up (v08, 30.0-34.0)
Every part parked as above; no motion except the camera: high over the right side, ~64 deg down, up vector = nose
(car length along the 9:16 height - v1 lesson), az-97 -> -83, d2.3, z4.8 -> 4.7, look(0,-0.1,0.3), lens 31 (tighter clips the bumpers: the set is tall, not wide). Reads as the
exploded diagram: front bumper + radar module ahead of the nose, rear bumper behind the tail, wheels/brakes/suspension
outboard on both sides, side panels in a strip along the right sill. No glow, no dim.

### G. Reassembly + ending (v09a/b, 34.0-38.0)
All parts fly home with ease_in, staggered by section (side 34.2, rear corner 34.35, front corner 34.5, bumpers +
radar 34.65) and **all lock on 36.0** (the `big` hit). Camera rear 3/4 high: az-140 d7.0 z3.2 look(-0.55,0.10,0.55) (exploded set ~80 % of the width)
-> az-134 d6.9 z2.7 look(-0.1,0,0.4) (assembled car small, like the Temerario), lens 35; v09b continues the same path with the clean `car.blend` + 4 corners (hard cut on
36.0, invisible: composite seams disappear). Fade to black 37.0-38.0 (assembler `vf: fade=t=out:st=1.0:d=1.0` on v09b).
Logo: `remotion/public/illumaesthetic_logo.png` scaled to 270 px wide (25 % of 1080), centred, on black, fade in
38.2-38.9 s, hold, fade out 40.6-41.5 (reuse tools/logo_card.sh with the smaller scale and fades).

### Edge rule: parked parts hidden per shot
No half-clipped pieces at frame edges (reviewer: "consistently poorly cropped"). Parked parts of OTHER sections that a
section camera would cut at an edge are hidden in that shot only (`HIDE` in plan_v2.py; they are still parked, and v08
shows everything): v04 hides front bumper + radar; v05 hides all front parts; v06 hides front + side parts and the FL
corner; v07 hides front + side parts, rear bumper and FL corner. The section's own parts are always fully in frame or
leave it while moving. Section close-ups (v03 end, v04, v05, v06 end, v07) crop INTO the car body on purpose.

### Interior
`n_interior6` (Interior_(2.4m), 6 mm) sits in the cabin in EVERY shot as a static fill, so the glassless window openings
show seats/dash instead of an empty shell. It is never exploded (no roof/door-off scan; lifting it would leave a hollow
shell). Center Console is inside it and not used separately.

## 3. Highlight method (new, `tools/shots.py`)
Optional per-object keys, default look unchanged when absent (`highlight_mat()`):
- `"glow": [{t, v}]` - warm-white **rim** emission (Layer Weight facing^1.5 mask, strength 5.0 x v). On release the part
  pulses 0 -> 1 in 0.25 s, decays to 0.3 over ~1.2 s and keeps that faint rim while its section is the focus; off 0.5 s
  after the section ends. Reads as the part catching the light as it separates; colour stays neutral silver.
- `"dim": [{t, v}]` - Mix Shader toward black (0.85 x v). Parked parts of finished sections ramp to 0.6 (~-20 % display
  after AgX) so the current section reads; all dims lift 29.4-30.0 for the line-up.
Tested (`/home/user/media/work/a90/plan/tests/hl_compare2.jpg`, `dim_compare3.jpg`, 50 % / 12 spp): glow on the bumper at
7.25 s is visible but soft; skirts in focus +14 % brighter, parked fender visibly darker. A base-colour dim was tried
first and did nothing on the metallic silver (176 -> 170) - that is why dim is a shader mix. No text-free alternative
needed; if the reviewer finds the glow too much, scale `GLOW_GAIN` (5.0) down - one constant.

## 4. Labels (user confirmed: ADD) - Remotion ScanHUD `label` items, overlay track
House style: Inter Display title + JetBrains Mono sub, `#e8ecf2`, 80 px inside the edges (x 0.074-0.926), max two on
screen, enter on a beat, leave >= 0.3 s before the next cut, never over the subject. Positions read off the 30 % framing
sheets (black areas); recheck on the final renders. Wording = what the scan files show (file names in brackets).

| # | from-to (s) | frames @30 | title | sub | x, y, align | Backed by |
|---|---|---|---|---|---|---|
| 1 | 7.0-9.5 | 210-285 | FRONT BUMPER | INSIDE + OUTSIDE SCANNED | 0.08, 0.76, left | Front Bumper Outside / Inside scans; inside verified (v1 regcheck/inside_cmp.jpg) |
| 2 | 9.0-10.5 | 270-315 | RADAR COVER | + MOUNTING GRILLE | 0.92, 0.70, right | Supra Radar Cover, Supra Radar Mounting Grille |
| 3 | 10.5-11.7 | 315-351 | FRONT BUMPER REMOVED | CRASH BEAM · RADIATORS | 0.08, 0.78, left | Supra Under Front Bumper (confirm "radiators" on the full-res frame; else "CRASH BEAM · MOUNTS") |
| 4 | 13.0-15.7 | 390-471 | FRONT SUSPENSION | WHEEL · BRAKE · COILOVER | 0.08, 0.10, left | wheel/rotor/caliper/coilover bench scans |
| 5 | 16.5-19.7 | 495-591 | SIDE TRIM REMOVED | DOOR TRIM · UPPER + LOWER SKIRT | 0.08, 0.08, left | Supra Door Trim, Upper Skirt, Lower Skirt (+ Under Door Trim / Chassis Under Upper Skirt) |
| 6 | 21.0-23.5 | 630-705 | REAR BUMPER | INSIDE + OUTSIDE SCANNED | 0.92, 0.76, right | Rear Bumper Outside / Inside; inside verified v1 |
| 7 | 24.3-25.7 | 729-771 | REAR BUMPER REMOVED | CRASH BEAM · EXHAUST | 0.08, 0.78, left | Supra Under Rear Bumper (confirm on the full-res frame) |
| 8 | 26.5-29.7 | 795-891 | REAR SUSPENSION | WHEEL · BRAKE · SPRING · DAMPER | 0.08, 0.10, left | RR wheel/rotor/caliper/spring/damper scans |
No labels on v01, v08, v09, logo. No numbers (none needed; if a count is ever added, read it from the STL header and
pass value/(1-2^-10) - ScanHUD counter stops at 99.9 %). Draft props already written: `projects/a90-supra/overlay_v2.json`
(ScanHUD: 1080x1920, 30 fps, 1245 frames, accent #e8ecf2, 8 `label` items; max-two-on-screen checked).

## 5. Music (cues_v2.json, shared engine projects/ferrari-296/tools/music.py)
`python projects/ferrari-296/tools/music.py projects/a90-supra/cues_v2.json /home/user/media/work/a90/music/a90_score_v2.wav`
- 120 BPM, 41.5 s, D minor (Dm-Bb-Gm-A), same palette as v1 so the set sounds alike.
- Riser 4.0 -> 7.0 into the first separation; `impact` 7.0 (front bumper), 21.0 (rear bumper).
- `cut` hits on every shot line (4, 12, 16, 20, 26, 30, 34) and every part release (9.0, 12.5, 13.0, 13.5, 14.0, 14.5,
  16.5, 17.5, 18.5, 26.5, 27.0, 27.5, 28.0, 28.5 - softer gain 0.5-0.7 so they read as ticks).
- `whoosh` on the two bumper tips (8.0, 22.0); `swell` + `big` on the reassembly lock 36.0; logo chord 38.0; fade 40.0-41.5.
- Verify after rendering: kick-peak grid (lessons: G35, FG2), and measure every cut against the decoded audio.

## 6. Cut list (from v1, `python -m ive director` report: projects/a90-supra/director_report.md)
| v1 clip | Fate | Why |
|---|---|---|
| s01_front34 (4.97 s turntable) | cut -> v01 side profile with wheels | turntable shows nothing new (mazda lesson); v1 had no wheels |
| s02_rear34 | cut | rear belongs in its own section (v06/v07); no ping-pong |
| s03_arch | cut | report: repeats s06 (IoU 0.71); empty arch - corner now shown with real suspension in v04 |
| s04_headlight, s05_taillight | cut | details that do not come apart; time goes to the disassembly |
| s06_side | replaced by v05 | same subject, now with panels coming off |
| s07_topdown | cut | report: 1.2 s dead frames, nothing new |
| s08_explode (all parts at once, 7.5 s) | replaced by v03-v09 | user: section by section |
| logo (6 s, large, hard cut) | replaced | report: 4.33 s dead; Temerario ending (fade, small logo) |
No v1 render is reusable.

## 7. Hold list (holds > 0.75 s) and why
| Shot | Hold | Reason |
|---|---|---|
| v03 9.6-10.2 | bumper parked, camera drifting | read the scanned inside of the bumper + radar module separating (label 1/2) |
| v03 10.5-12.0 | slow push only | hero data: crash beam / cooling stack behind the bumper (label 3) |
| v05 19.5-20.0 | camera track | let the third panel settle before the cut |
| v06 23.6-26.0 | camera push | hero data: Under Rear Bumper (label 7) |
| v07 29.5-30.0 | camera push | last part settles |
| v08 30.0-34.0 | camera drift only | the one complete line-up (Temerario 28-32 s) |
| v09b 36.0-37.0 | clean car, drift | the lock reads before the fade (Temerario 34-35 s) |
Every hold has camera motion; none is static. Tag clips with `focus:`/`section:`/`hold: true` in project_v2.yaml so
`ive director` can re-check.

## 8. Render budget (finals by the next agent)
Measured on this box today: v08 line-up (9.2 M tris, 20 objects) at **75 %, 12 spp, persistent data OFF: 13.5 s/frame**
after an 11 s scene load (3 stills in 52 s). Close-ups cover more pixels: budget 15-25 s/frame.

| Shot | frames @15 | tris | est. min |
|---|---|---|---|
| v01_whole | 61 | 5.3 M | 12 |
| v03_fbump | 126 | 9.7 M | 42 |
| v04_fcorner | 66 | 9.6 M | 22 |
| v05_side | 66 | 9.2 M | 20 |
| v06_rbump | 96 | 9.9 M | 32 |
| v07_rcorner | 66 | 9.8 M | 22 |
| v08_lineup | 66 | 9.2 M | 15 |
| v09a_reasm | 36 | 9.2 M | 9 |
| v09b_clean | 32 | 5.3 M | 6 |
| **total** | **615** | | **~3 h** |
Mesh plan (already built): base_v2 re-decimated to 4 mm (4.23 M); bumpers full (1.1-1.35 M) only in their own shot, 4 mm
lite (0.57-0.68 M) elsewhere; right-side wheel/brake/suspension parts full only in their corner shot, wheels at 3.5 mm
lite elsewhere; left corners always lite (0.36-0.42 M); interior at 6 mm (0.44 M). Peak ~10 M tris per explode shot
(v1 s08 rendered 8 M). If RAM gets tight: drop `n_interior6` from v04/v07 (cabin not visible) and use `L_fbump_norad`
in v03 after 10.5 s (split render).
Procedure: one Blender job at a time; `--persistent auto` (now the default: OFF when any part is keyed - v1 s08 lights
dropout); render in 40-frame chunks with `--frames a-b` in fresh processes; after each shot scan per-frame mean luma for
a step drop and re-render bad ranges. 15 fps + minterpolate: set `src_fps = (N-1)/(dur + 3/30)` (N = frames) or the clip
freezes 3 frames at the end. Fast moves (bumper tips 8.0-9.6 / 22.0-23.6, ~1 m/s) may ghost in minterpolate: check those
frames; fallback = render v03 6.8-9.8 s and v06 20.8-23.8 s at 30 fps (+~25 min).
Assembly: cut-only lessons don't apply (soft blends) - use `ive assemble` with `transition: dissolve 0.3` and
whole-frame `dur`s; first clip one frame short; measure every cut against the decoded audio.

## 9. Plate
Rear plate checked at full res (`tests/plate_compare.jpg`): the car scan has a plate FRAME with mushy dealer text and a
blobby plate face - no legible characters; the Rear Bumper scan has an empty plate recess. No deplate pass needed; the
v06 push-in ends on the Under Rear Bumper structure, not on a plate. Re-check the v06 final frames at full res anyway.

## 10. Risks and fallbacks
| Risk | Fallback |
|---|---|
| Corners are bench scans on engineering hardpoints, left side mirrored; knuckles/arms not placed | never close on the left corners; if the reviewer objects to mirrored left corners, leave FL/RL on the car (remove `fl_corner`/`rl_corner` keys) |
| Composite seams (carved panels / spliced state scans) visible in close-ups | close-ups are on the state scans themselves; clean-car swap at 36.0. If a seam shows in v05, widen `--cut` in composite_v2.py to 12 mm |
| Glow reads as "effect" | GLOW_GAIN 5 -> 3, or drop glow and keep dim only |
| Cycles lights dropout / black frames | persistent OFF + luma scan + `--frames` re-render |
| Minterpolate ghosting on the bumper tips | 30 fps for those ranges (above) |
| "Radiators" / "crash beam" wording not visible enough on the full-res frame | sub-line falls back to "MOUNTS" / plain "FRONT BUMPER REMOVED" |
| Total 41.5 s slightly over the ~38-40 s brief | if asked: shorten the logo to 2.5 s (ends 40.5), or cut v08 to one bar (30-32) and pull everything after it 2 s earlier (39.5 s) |
| Temerario has ~12 s of intact car; we have 7 s | deliberate: user-wide rule "no redundant turntables"; front push in v03 4-7 s gives the intact front 3 s more |

## 11. Files
- Plan generator: `projects/a90-supra/tools/plan_v2.py`; shots: `projects/a90-supra/shots_v2/*.json`
- Framing: `projects/a90-supra/tools/framing_v2.sh "<ids>"` -> `/home/user/media/work/a90/plan/sheet_<id>.jpg`,
  all-shot sheet `/home/user/media/work/a90/plan/sheet_all_v2.jpg`
- Composite: `projects/a90-supra/tools/composite_v2.py` (base_explode + side states + under rear bumper)
- Cues: `projects/a90-supra/cues_v2.json`; scene direction: `projects/a90-supra/direction.md`
- New blends (all `--like car.json`, /home/user/media/work/a90/blend/): base_v2, n_lskirt, n_uskirt, n_uskirt_under,
  n_dtrim, n_udtrim, n_radar, n_radargrille, n_radar_mod, n_fbump_norad, L_fbump_norad, L_rbump, n_urb, n_interior,
  n_interior6, n_console, n_car_lefthalf (check only), L_corner_{FL,FR,RL,RR}, L_FR_wheel, L_RR_wheel,
  p_FR_{wheel,rotor,caliper,coilover}, p_RR_{wheel,rotor,caliper,spring,damper}.
