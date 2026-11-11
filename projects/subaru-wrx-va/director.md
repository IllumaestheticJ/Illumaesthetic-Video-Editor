# Subaru WRX VA v2: director's shot plan (stage 2)

Follows `.claude/agents/director.md`. This plan keeps the scene order from `direction.md` (stage 1) and does not reorder
anything. The v1 director report (`python -m ive director projects/subaru-wrx-va/project.yaml`, written to a scratch path)
flagged these repeated views: s01~s02, s01~s07, s01~s08, s02~s08. It also flagged s09 dead frames (1.1 s) and "no focus"
on every clip. v2 removes s02 and s08, and trims s07 to its first 28 source frames. Every clip now carries
`section:` and `focus:`. **Re-run the director report on the v2 yaml after assembly.** If s01~s07 is still flagged,
render the fallback `n5_trunk` (spec at the end).

Scan frame: metres, nose +X (2.32), tail -X (-2.29), left +Y, ground 0, roof 1.445.
`az` is in degrees from +X toward +Y, and `z` is absolute camera height.
Part centres (from `blend/*.json` bboxes): bumper (1.86, 0.04, 0.40), size 0.93 x 1.88 x 0.64. fogL (2.10, 0.67, 0.33).
fogR (2.10, -0.70, 0.33). scoop (1.89, -0.01, 0.82). wing (-1.97, 0, 1.18).
Part `loc` values are offsets from home and `rot` is in degrees about the part centre (tools/shots.py). Keys use
`t = (frame-1)/(N-1)`, so a beat offset of s seconds from the clip start is `t = 15*s/(N-1)`. Every new shot renders
3 extra frames (`seconds = dur + 0.2`) to cover the minterpolate tail (lesson).

## Shot table

| section | shot | beats / s | focus | camera | part action (beats) | why it earns its time | source |
|---|---|---|---|---|---|---|---|
| whole car | s01_front34 | b0-b6, 0-2.73 | whole car, front 3/4 | v1: low front 3/4 turntable az 22->~35, 3.0 m, z 0.7, lens 32 (src frames 0-41 at 1.0x) | - | Whole car with motion from frame 1. Frames 1, 21 and 42 checked: the whole car is in frame (the tail nears the edge only after f42, which is cut) | reuse |
| engine bay | s06_hood | b6-b12, 2.73 | engine bay under the propped hood | v1: high front 3/4 crane az 40->18, z 1.5->2.1, lens 30 (1.32x, all frames) | captured state | Real hood-open scan (1.7 mm). Frames 1, 28 and 56 checked: whole car in frame, wing tip inside the edge | reuse |
| front bumper (hero) | **n1_bumper** | b12-b26, 6.33 | front bumper, then the front end behind it | front 3/4, push-in, lens 35, keys below | Bezels out b12.5-b13.5. Bumper forward b13.6-b15, up b15-b16, over the nose b16-b16.5, **flip 180 deg about Y b17-b18.4 (scanned inside to camera)**, hold to b20.3, rises out the top b20.3-b22. Camera pushes in on the bumper-removed capture b20-b26 | Addendum C: hero beat, longest scene, labelled | NEW 98 f |
| hood | **n2_scoop** | b26-b30, 1.83 | hood scoop + scoop opening | high front 3/4 -> lower, lens 40 | Scoop rises +0.85 m (translate only, no spin: its underside is not confirmed scanned) b26.5-b28.4, then holds on black | Second front state (scoop removed, 1.7 mm). Silver part lifted clear of the silver hood (Miata NA lesson) | NEW 31 f |
| side | **n_side** | b30-b34, 1.80 | left side, rear wheel | lateral dolly along the left side, lens 35 | - | Travel front -> rear, through the side's only data (doors, skirt, rear wheel). Moves sideways instead of rotating. The body runs off both edges on purpose because the camera is tracking | NEW 30 f |
| rear | **n3_wing** | b34-b42, 3.63 | STI wing uprights + blade | rear-left, rises from under the blade to blade level, push, lens 35 | none (no wing-removed state) | Section change -> rear signature. Starts under the blade where `Wing.stl` (underside + uprights) carries the data. The whole wing stays in frame, replacing the edge-clipped v1 s05 | NEW 58 f |
| rear | s07_trunk | b42-b46, 1.80 | open trunk lid + cavity | v1: high rear az -162->~-157, lens 30 (src frames 0-27, 1.0x) | captured state | Real trunk-open scan (1.9 mm). Short because the cavity is ragged. Frames 1-28 keep the car whole; frames >40 push the nose off the right edge, so they are cut | reuse |
| top / whole car | **n4a_reassemble** | b46-b54, 3.63 | whole car reassembling | high left overhead, nose up the frame, lens 45 | Fully exploded hold b46-b48. Bumper unflips b48-b49.6, comes down and forward b49.6-b51.6, home b51.6-b53.3. Scoop home b49.6-b51.2. Fogs in b49.3-b50.6, then slot home **b53.3-b54 (last lock on the b54 kick)** | Temerario: progressive explode -> wide -> reassembly. Only top view in the reel | NEW 58 f |
| top / whole car | **n4b_clean** | b54-b58, 1.80 | whole car, assembled | continues n4a's camera (+3 % push) | - (clean car_4mm swapped in on the lock) | C5 lesson: clean last frame. Fade to black b56-b58 | NEW 30 f |
| end | logo | b58-end, 4.47 | small logo | - | - | Rule 7: fade, then a small logo. Length is set by the track tail | rebuild card |

## New shot JSONs (ready for `shots/`; add the same dicts to `tools/plan.py`)

B = `/home/user/media/subaru-wrx-va/blend`. Use `"ease": "linear"` where a camera has more than 2 keys (Catmull-Rom
smooths the path; the global ease would warp the key times). Use `"sine"` for 2-key cameras.

### n1_bumper: 6.5333 s -> 98 frames, b12 = t 0. Beat -> t: b13 .070, b14 .140, b15 .210, b16 .280, b17 .351, b18 .421, b19 .491, b20 .561, b21 .631, b22 .701, b24 .841, b26 .981
```json
{"seconds": 6.5333, "lens": 35, "ease": "linear", "objects": [
 {"blend": "B/explode_base_4mm.blend"},
 {"blend": "B/scoop_2mm.blend"},
 {"blend": "B/wingfull_2mm.blend"},
 {"blend": "B/fogL_2mm.blend", "keys": [
  {"t":0,"loc":[0,0,0]}, {"t":0.035,"loc":[0,0,0]}, {"t":0.105,"loc":[0.7,0,0],"ease":"ease_out"},
  {"t":0.16,"loc":[0.7,0.55,0]}, {"t":0.56,"loc":[0.7,0.55,0]}, {"t":0.66,"loc":[0.7,1.6,0]}, {"t":1,"loc":[0.7,1.6,0]}]},
 {"blend": "B/fogR_2mm.blend", "keys": [
  {"t":0,"loc":[0,0,0]}, {"t":0.035,"loc":[0,0,0]}, {"t":0.105,"loc":[0.7,0,0],"ease":"ease_out"},
  {"t":0.16,"loc":[0.7,-0.55,0]}, {"t":0.56,"loc":[0.7,-0.55,0]}, {"t":0.66,"loc":[0.7,-1.6,0]}, {"t":1,"loc":[0.7,-1.6,0]}]},
 {"blend": "B/fbump_nofog_2mm.blend", "keys": [
  {"t":0,"loc":[0,0,0],"rot":[0,0,0]}, {"t":0.12,"loc":[0,0,0],"rot":[0,0,0]},
  {"t":0.21,"loc":[1.0,0,0.10],"rot":[0,0,0],"ease":"ease_out"},
  {"t":0.28,"loc":[1.0,0,1.15],"rot":[0,0,0]},
  {"t":0.33,"loc":[0.5,0,1.15],"rot":[0,0,0]}, {"t":0.351,"loc":[0.5,0,1.15],"rot":[0,0,0]},
  {"t":0.45,"loc":[0.5,0,1.15],"rot":[0,180,0]},
  {"t":0.60,"loc":[0.5,0,1.15],"rot":[0,180,0]},
  {"t":0.72,"loc":[0.5,0,2.6],"rot":[0,180,0],"ease":"ease_in"}, {"t":1,"loc":[0.5,0,2.6],"rot":[0,180,0]}]}],
 "cam": [
  {"t":0,   "az":26, "dist":3.5, "z":1.45, "look":[2.0,0,0.75]},
  {"t":0.30,"az":22, "dist":3.7, "z":1.65, "look":[2.15,0,1.05]},
  {"t":0.55,"az":20, "dist":3.4, "z":1.55, "look":[2.2,0,1.0]},
  {"t":0.80,"az":16, "dist":2.5, "z":1.15, "look":[2.05,0,0.55]},
  {"t":1,   "az":12, "dist":2.2, "z":1.0,  "look":[2.0,0,0.45]}]}
```
Clearances (checked against the bboxes): the bumper moves forward 1.0 m before rising, so its wheel-arch wraps
(x 1.39) clear the fenders and headlights. It passes between the bezels (bumper |y| <= 0.98, bezel inner edges at
|y| 1.08 / 1.10). The 180 deg Y-flip at centre (2.36, 0.04, 1.55) has a swept radius of ~0.57 m, so its lowest point
is z ~0.98, above the hood front (~0.85). The flip is about the width axis, not a Z-spin (240SX / A90 lessons). Clear
background: the bezels sit forward and outside the nose on black, and the bumper flips above the nose against black.
Both leave frame on purpose (bezels sideways b20-b21, bumper up b20.3-b22) while the camera pushes in on the exposed
front end. End framing: ~2.3 m of visible width at the look point, so the front end fills about 85 % of the width.
The camera stops at 2.2 m because the explode base is 4 mm (open question 4 in direction.md).

### n2_scoop: 2.0333 s -> 31 frames, b26 = t 0. b27 .227, b28 .453, b29 .680, b30 .917
```json
{"seconds": 2.0333, "lens": 40, "ease": "sine", "objects": [
 {"blend": "B/explode_base_4mm.blend"},
 {"blend": "B/wingfull_2mm.blend"},
 {"blend": "B/fbump_nofog_2mm.blend", "keys": [{"t":0,"loc":[0.5,0,2.6],"rot":[0,180,0]}, {"t":1,"loc":[0.5,0,2.6],"rot":[0,180,0]}]},
 {"blend": "B/fogL_2mm.blend", "keys": [{"t":0,"loc":[0.7,1.6,0]}, {"t":1,"loc":[0.7,1.6,0]}]},
 {"blend": "B/fogR_2mm.blend", "keys": [{"t":0,"loc":[0.7,-1.6,0]}, {"t":1,"loc":[0.7,-1.6,0]}]},
 {"blend": "B/scoop_2mm.blend", "keys": [
  {"t":0,"loc":[0,0,0]}, {"t":0.10,"loc":[0,0,0]}, {"t":0.55,"loc":[0.15,0,0.85],"ease":"ease_out"}, {"t":1,"loc":[0.15,0,0.85]}]}],
 "cam": [
  {"t":0, "az":32, "dist":2.3, "z":2.05, "look":[1.85,0,0.85]},
  {"t":1, "az":20, "dist":2.0, "z":1.5,  "look":[1.95,0,1.3]}]}
```
At t 0 the camera looks down on the hood, so the scoop and then its opening read against the hood. By t 1 the
camera has dropped to z 1.5, so the raised scoop (z ~1.6-1.75) silhouettes on black above the roof line. The bumper at
z 2.7-3.3 sits ~30-43 deg above the frame's top edge, and the bezels are ~60 deg off-axis, so neither is in frame.
Confirm with the still check below.

### n_side: 2.0 s -> 30 frames (clean car_2mm; nose never in frame)
```json
{"seconds": 2.0, "lens": 35, "ease": "sine", "objects": [{"blend": "B/car_2mm.blend"}],
 "cam": [
  {"t":0, "pos":[-0.3,3.0,0.7],  "look":[-0.6,0.9,0.55]},
  {"t":1, "pos":[-2.6,2.6,0.85], "look":[-1.6,0.85,0.6]}]}
```
Check f1: no part of the front bumper (x > 1.39 m) is visible. If any shows, shift both `pos` and `look` x by -0.3.

### n3_wing: 3.8333 s -> 58 frames, b34 = t 0 (car_2mm; no removal)
```json
{"seconds": 3.8333, "lens": 35, "ease": "sine", "objects": [{"blend": "B/car_2mm.blend"}],
 "cam": [
  {"t":0, "az":150, "dist":2.3, "z":0.85, "look":[-1.95,0,1.2]},
  {"t":1, "az":185, "dist":1.9, "z":1.6,  "look":[-1.95,0,1.2]}]}
```
The camera starts just below the blade (blade z 1.01-1.35), which shows the scanned underside and the inside faces of
the uprights. It then rises to blade level behind the car while pushing in. The wing is 1.34 m wide and the visible width
is ~1.9-2.3 m, so it fills 60-70 % of the width with margins on both tips. The plate is deplated; check it stays a blank
slab. The lower bumper running out of the bottom edge is a deliberate detail crop.

### n4a_reassemble: 3.8333 s -> 58 frames, b46 = t 0. b48 .239, b49 .358, b50 .477, b51 .596, b52 .716, b53 .835, b54 .954
```json
{"seconds": 3.8333, "lens": 45, "ease": "sine", "objects": [
 {"blend": "B/explode_base_4mm.blend"},
 {"blend": "B/wingfull_2mm.blend"},
 {"blend": "B/fbump_nofog_2mm.blend", "keys": [
  {"t":0,"loc":[0.5,0,2.6],"rot":[0,180,0]}, {"t":0.239,"loc":[0.5,0,2.6],"rot":[0,180,0]},
  {"t":0.38,"loc":[0.5,0,2.6],"rot":[0,0,0]},
  {"t":0.55,"loc":[1.0,0,1.15],"rot":[0,0,0]},
  {"t":0.68,"loc":[1.0,0,0.10],"rot":[0,0,0]},
  {"t":0.84,"loc":[0,0,0],"rot":[0,0,0],"ease":"ease_in"}, {"t":1,"loc":[0,0,0],"rot":[0,0,0]}]},
 {"blend": "B/scoop_2mm.blend", "keys": [
  {"t":0,"loc":[0.15,0,0.85]}, {"t":0.36,"loc":[0.15,0,0.85]}, {"t":0.60,"loc":[0,0,0],"ease":"ease_in"}, {"t":1,"loc":[0,0,0]}]},
 {"blend": "B/fogL_2mm.blend", "keys": [
  {"t":0,"loc":[0.7,1.6,0]}, {"t":0.30,"loc":[0.7,1.6,0]}, {"t":0.45,"loc":[0.7,0.55,0]}, {"t":0.84,"loc":[0.7,0.55,0]},
  {"t":0.90,"loc":[0.7,0,0]}, {"t":0.954,"loc":[0,0,0],"ease":"ease_in"}, {"t":1,"loc":[0,0,0]}]},
 {"blend": "B/fogR_2mm.blend", "keys": [
  {"t":0,"loc":[0.7,-1.6,0]}, {"t":0.30,"loc":[0.7,-1.6,0]}, {"t":0.45,"loc":[0.7,-0.55,0]}, {"t":0.84,"loc":[0.7,-0.55,0]},
  {"t":0.90,"loc":[0.7,0,0]}, {"t":0.954,"loc":[0,0,0],"ease":"ease_in"}, {"t":1,"loc":[0,0,0]}]}],
 "cam": [
  {"t":0, "pos":[0.35,3.2,5.4], "look":[0.35,0.1,0.7],  "up":[1,0,0]},
  {"t":1, "pos":[0.25,2.8,4.8], "look":[0.30,0.05,0.65], "up":[1,0,0]}]}
```
The nose points up the 9:16 frame (A90 lesson). Content spans x -2.3 to ~3.0 m, about 5.3 m of a ~8 m tall view, so
the whole car and every part stay in frame with ~15 % margins. The unflip happens at z ~3 m, clear of everything.
The bumper's descent passes between the bezels, which are still at |y| 0.55. The bumper is home before the bezels slot
in (bezel scans duplicate the bumper's bezel openings, so they go last).

### n4b_clean: 2.0 s -> 30 frames, b54 = t 0
```json
{"seconds": 2.0, "lens": 45, "ease": "sine", "objects": [{"blend": "B/car.blend"}],
 "cam": [
  {"t":0, "pos":[0.25,2.8,4.8],   "look":[0.30,0.05,0.65], "up":[1,0,0]},
  {"t":1, "pos":[0.22,2.68,4.62], "look":[0.30,0.05,0.65], "up":[1,0,0]}]}
```
The first frame matches n4a's last pose, so the swap on b54 is invisible apart from the composite trim lines
disappearing. Both cameras ease to zero speed at the join.

## Labels (Remotion ScanHUD `kind: label`; absolute output frames; x 0.08, y 0.74, align left; max one on screen)

| title | sub | beats | from, duration (frames) |
|---|---|---|---|
| HOOD OPEN | - | b7-b11 | 97, 54 |
| FRONT BUMPER REMOVED | - | b13-b17 | 178, 55 |
| BUMPER | SCANNED INSIDE + OUT | b17-b20 | 233, 41 |
| BEHIND THE BUMPER | *decided by still V1, below* | b21-b25 | 287, 55 |
| HOOD SCOOP REMOVED | - | b27-b29 | 369, 27 |
| TRUNK OPEN | - | b43-b45 | 586, 28 |

"SCANNED INSIDE + OUT" was checked: the bumper-only solo render from behind (`regcheck/fbump_2mm_solo_1.00.png`)
shows the inner face with brackets and fog housings, and clips.md lists the scan as "outside + inside".
**V1 (behind-bumper label):** render `n1_bumper --still 1.0` (and `0.8`) and look at the front end:
- If a continuous horizontal beam spans the nose between the frame-rail ends **and** the headlight housings read from
  below/behind: sub = `BUMPER BEAM · HEADLIGHT HOUSINGS`.
- If only the headlight housings are clear: sub = `HEADLIGHT HOUSINGS · FRONT STRUCTURE`.
- Otherwise: sub = `AS SCANNED`. Do not name a part you cannot point to in the still. In v1 s09 f25-30 I can see the
  housings, a horizontal member and a lower finned panel, but at 4 mm / 810 px I cannot confirm what they are.
No numbers on screen. Labels go over scan shots only (there is no IRL footage) and sit in the black area below the car.
Move y per shot if a still shows overlap with the silhouette.

## Cut list (v1 -> removed)
- **s02_rear34**: repeated view (director IoU 0.78 vs s01, 0.67 vs s08). A turntable that adds nothing the opener lacks; the rear is now wing + trunk.
- **s03_wheel**: off-section and continuity (front bumper in frame while it is off in v2). The wheel and fender are cut at the frame edges and read as a clip.
- **s04_front**: same subject as n1 (grille, fog bezels, bumper face), merged into n1's opening frames.
- **s05_wing**: cuts the car and wing at the frame edge (user example). Replaced by n3 with the whole wing in frame.
- **s08_topdown**: rotating top-down with nothing new (director flags vs s01 and s02). The only top view is now the n4 reassembly.
- **s09_explode**: every part separates at once in one wide orbit, the bumper Z-spins, and there are 1.1 s of dead frames. Replaced by sectioned close shots (n1, n2) and the wide reassembly (n4a/b).
- **s01 frames 42-74, s07 frames 28-55**: the car nears or crosses the frame edge.

## Hold list (> 0.75 s)
- n1, b18.4-b20.3 (~0.9 s): bumper flipped, inner face to camera, label "SCANNED INSIDE + OUT". This is the show-off hold the reviewers asked for. The camera keeps easing.
- n1, b22-b26 (1.8 s): camera push-in on the bumper-removed front end with the label, held long enough to read the detail (addendum C). Not static: the camera moves 2.5 -> 2.2 m.
- n2, b28.4-b30 (~0.7 s): raised scoop on black over the opening. Just under the threshold; listed for review.
- n4a, b46-b48 (0.9 s): fully exploded wide, every removed part visible at once before the return. Camera drifting.
- n4b, b54-b56 (0.9 s) then fade b56-b58: assembled car, clean. Short on purpose (rule 7).
- logo, b58-end (4.47 s): forced by the music tail (b64 at 29.07 s, audio fade). Small logo, fade in 0.5 s, fade out over the last 1.6 s.

## Render budget (15 fps, 75 % res, 12 spp, `--no-persist`, one job at a time, ~12 s/frame)
| shot | frames | est. |
|---|---|---|
| 4 verification stills (n1 t 0.45 + 1.0, n2 t 0, n4a t 0) | 4 | ~1 min |
| n1_bumper | 98 | ~20 min |
| n2_scoop | 31 | ~6 min |
| n_side | 30 | ~6 min |
| n3_wing | 58 | ~12 min |
| n4a_reassemble | 58 | ~12 min |
| n4b_clean | 30 | ~6 min |
| **total** | **309** | **~62 min** |
Render order: stills, then n1 (hero), n2, n4a, n4b, n3, n_side. After each shot, run the per-frame luma scan
(persistent-data dropout lesson). Reused unchanged: s01_front34 (src 0-41), s06_hood, s07_trunk (src 0-27).
Rebuild the logo card at ~30 % width (`tools/logo_card.sh`: `scale=324:-1`, add `fade=t=in:st=0:d=0.5`).
Not used: s02, s03, s04, s05, s08, s09 (kept on disk).

Fallback only if the v2 director report still flags s07 against s01. **n5_trunk**, 2.0 s -> 30 frames, `B/trunk_4mm.blend`,
lens 35, sine: `{"t":0,"az":-170,"dist":3.0,"z":2.3,"look":[-1.75,0,1.0]}` -> `{"t":1,"az":-150,"dist":2.6,"z":2.1,"look":[-1.75,0,0.95]}`.
This is a push into the open lid, with the lid + rear filling ~75 % of the width. About 6 min.
