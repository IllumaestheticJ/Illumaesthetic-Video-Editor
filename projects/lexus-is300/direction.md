# Lexus IS300 v2 - direction (scene order + per-shot plan)

Scene-director + director (stage 2) in one file, 2026-11-11. Inputs read: `knowledge/lessons.md` (all), `style-guide.md`,
`training/references/README.md` (Temerario), `clips.md`, `feedback.jsonl`, `editlog.jsonl`, `project.yaml` (editor's v2 draft),
`project_v1.yaml`, `director_report.md`, `tools/shots.py`, `cues.json`. Images looked at: `chk/rearbumper_{0,1}_solo.png`,
`chk/sideskirt_0_solo.png`, `chk/frontendbumperremoved_2_solo.png`, `chk/reartrunkopen_1_solo.png`,
`chk/sideskirtunder_1_solo.png`, `chk/comp_front.png`, `chk/s6crop.png`, `chk/finA.jpg`, `chk/finB.jpg`, `chk/v2_st{A,B,C}.jpg`,
`renders/final/s5_front_off/f_0060.png`.

The brief: scan only, 1080x1920, house silver on black, music fixed (92.0 BPM, beat n = 0.050 + 0.6522 n s). **The user's
addendum (via parent) overrides the earlier brief**: deliberate 9:16 framing, each section in one continuous sequence,
the front-end-bumper-removed state is the HERO beat, short factual text labels now allowed on scan shots, and openings
only where a registered state scan exists.

---

## 1. Feature inventory

| Region | Scan data (registered) | What it actually shows | Quality / weak spots | Richness |
|---|---|---|---|---|
| **Front end** | Full car (2 mm close-up / 4 mm); **front end bumper removed** state (17 % overlap, 3-5 mm where it overlaps); front bumper = DERIVED (car minus state) | State: a large **front-mount intercooler** core with end tanks and charge pipes both sides (clearly readable in s5_front_off f_0060), brackets/structure at both corners, headlights, the wheels behind. An upper member with two round shapes sits behind the grille line (identity unclear, see open questions). Bumper part = outer skin only: from above/behind it reads hollow and ragged (chk/s6crop.png) | Bumper has no inner face, so only show it from the front/below. Grille opening is partly a scan hole (finA row 4) | **Highest**: 1 state with dense real structure + 1 part + headlight/grille signature |
| **Front-right wheel** | Full car 2 mm | Multi-spoke aftermarket wheel, tyre, arch liner, brake/hub visible through spokes (finA row 3) | Good; tyre tread is speckled | Medium (signature wheel) |
| **Right side / sill** | **Side Skirt** PART scan (3.11 mm); **Side Skirt under** state (rmse 2.4 mm) | Skirt: long thin moulding, flared at the rear end. State: the right sill/lower door edges with the skirt off (plain sheet metal + mount line) | Sill state is plain; short scene | Medium-low: 1 part + 1 state |
| **Rear** | **Rear Bumper** PART scan (3.07 mm); **Rear Trunk Open** state (rmse 3.2 mm, = rear bumper off + trunk open); trunk lid = car + OEM Trunk rear face (outer skin + rear face, no inner face) | State: rear bumper beam, trunk floor/interior, tail-lamp backs. Rear bumper: see backside analysis below | Lid has no inner face: lift it, don't flip it. Plates flattened (user request) | **High**: 2 parts + 1 state |
| **Top** | Full car | Roof, hood, trunk lid top - no states | Windscreen is a ragged scan hole edge | Low: only in the finale overview |
| Interior / engine bay / doors | Interior/dash/headlight scans exist but are not in the body set; **no hood-open, door-open state** | - | - | **Excluded** (rule D: no hood/door openings) |

**Backside check (rear bumper, side skirt).** The solo renders (`rearbumper_{0,1}_solo.png`, `sideskirt_0_solo.png`) only show the
OUTER faces, so they cannot answer it. I measured face normals in the levelled STLs instead (area fraction, central band):

| Mesh | faces pointing out | pointing in | verdict |
|---|---|---|---|
| car (same rear box) | 0.70 | 0.01 | one-sided outer skin (reference) |
| fbumper (derived) | 0.86 | 0.02 | one-sided (as expected) |
| **rearbumper** | 0.18 | **0.60** | **two-sided: a large inner/mounting face is scanned** (sign suggests flipped winding; either way both sides exist) |
| **sideskirt** | 0.28 | **0.21** | **two-sided: inner face present** (51 % edges/flanges) |

So: **plan a tip for the rear bumper (its inner face is worth showing)** and **a roll for the side skirt**, BOTH conditional on
one 30 % still each of the part from its back side (editor renders: rear bumper from (0, 0.6, 1.6) looking at (0, 1.9, 0.45);
skirt from (0.2, -0.1, 1.2) looking at (-0.75, -0.15, 0.26)). If the back reads as holes/noise, use the translate fallback
given per shot. Open question 1.

---

## 2. Scene order and why

Opener: **whole car, front-right 3/4** (s1_wide), because the front carries the strongest data (FMIC state + bumper +
headlight/grille signature) and the right side is where the side-skirt data is, so the camera never has to cross the car.
Travel: **front-right wide -> front-right wheel -> nose -> front end (HERO, bumper off on the drop) -> right sill -> rear
(trunk open + rear bumper) -> finale (top/overview -> reassembly, rear-left 3/4) -> logo**. One direction around the car, no
ping-pong. The richest region (front end) gets the drop (beat 16); the second richest (rear, 2 parts + state) gets 8 beats;
the thin sill gets 6; the loudest beat (40) and the triple hit (44/45/46) belong to the finale.

### Scene list (beats tile 0..48 exactly; logo 48 -> 37.4 s)

| # | shot | beats | video s | cut frame in | section covered | scans used | focus | why here (inventory) | render |
|---|---|---|---|---|---|---|---|---|---|
| 1 | s1_wide | 0-8 | 0.000-5.268 | 0 | WHOLE CAR (opener) | car 4 mm | the whole car, front-right 3/4 | user: open on the whole car, motion from frame 1; front = richest end | **reuse** (rendering now) |
| 2 | s3_wheel | 8-10 | 5.268-6.572 | 158 | WHEELS (front-right) | car 2 mm | front-right wheel, spokes + arch | nearest signature feature to the opener's camera; travel starts | **reuse** v1 (21 fr) |
| 3 | s4_nose | 10-14 | 6.572-9.181 | 197 | FRONT (exterior) | car 2 mm | headlight + grille | front exterior right before it comes apart; slide ends front-centre = s5's start | **reuse** (re-rendered, plate flat, 40 fr) |
| 4 | s5_front | 14-24 | 9.181-15.703 | 275 | FRONT (bumper off: HERO) | comp_explode + fbumper | front bumper -> intercooler + structure behind it | richest region, bumper released ON the drop (beat 16); one held shot (merges draft s5+s6) | **NEW** |
| 5 | s6_side | 24-30 | 15.703-19.616 | 471 | SIDE (right sill) | comp_explode + sideskirt | right side skirt + bare sill | travel continues down the right side; 1 part + 1 state = 6 beats | **NEW** |
| 6 | s7_rear | 30-38 | 19.616-24.834 | 588 | REAR (bumper off + trunk open) | comp_explode + rearbumper + lid | rear bumper inner face, bumper beam, trunk floor | second richest (2 parts + Rear Trunk Open), registered state so the trunk may open (rule D) | **NEW** |
| 7 | s8_finale | 38-48 | 24.834-31.356 | 745 | TOP + WHOLE CAR (reassembly) | comp_explode -> car (swap on 46) + 4 parts | all four parts, then the assembled car | Temerario ending: exploded overview from above, parts home on the triple hit, fade | **NEW** |
| 8 | logo | 48-end | 31.356-37.400 | 941 (end 1122) | - | logo png | small logo on black | music tail | reuse logo_card_v2.mp4 |

Frame durations at 30 fps (first clip one frame short, editor's convention): s1 157, s3 39, s4 78, s5 196, s6 117, s7 157,
s8 196, logo 181. Cut frames: 158, 197, 275, 471, 588, 745, 941; end 1122.

**Section check (addendum B):** whole car (1, 7), wheels (2), front exterior (3) + front bumper-off (4) are ONE continuous
front sequence (3 and 4 are adjacent, same section, different subject: closed headlight/grille vs what is behind the bumper),
side (5), rear (6), top (7 only). No section appears in two separated places. Whole-car shots: only #1 (opener: user asked
for the whole car first; the reviewer flagged v1 as clipped) and #7 (the reassembly must show every part landing home; ends
on the rear-left 3/4, a side and height never used before, so it does not repeat the opener).

### Music map
- Beats 0-15: quiet intro (kicks on even beats) - wide, wheel, nose.
- **Beat 16 (10.485 s, drop): front bumper releases** (inside s5, cut was 2 beats earlier on beat 14 so the release itself is the hit).
- Beat 25: skirt releases; beat 31: rear bumper; beat 33: lid.
- **Beat 40 (26.138 s, loudest): all four parts lift into layers above the car** (s8).
- **Triple hit 44 / 45 / 46 (28.75 / 29.40 / 30.05 s): skirt lands, front bumper lands, rear bumper + lid land = LOCK.**
- Beats 46-48: assembled car, clean full-car swap on 46, fade 47.2-48. Logo on beat 48 to 37.4 s.

---

## 3. Per-shot direction

Frame: metres, nose -Y, car's right = -X, Z up. Bumper faces y = -2.24 / +2.24; wheel centres x = +/-0.75, y = -1.40 / +1.32,
z = 0.32. Camera keys are `loc -> target, focal (mm, 20.25 mm sensor width)`. Beat -> shot-local seconds = (0.050 + 0.6522 n) - shot start.
Part offsets are on ONE global timeline (beats), keyed in every new shot so the parts are continuous across cuts.

### 1. s1_wide (beats 0-8) - reuse
- Camera (as rendered): arc r 8.2 -> 7.6 m around (0, -0.4, 0.6), azimuth -42 -> -50 deg (front-right), h 1.2 -> 1.3, 30 mm. Fade up 0.8 s.
- Framing first/mid/last: whole car 68-78 % of width with >= 9 % margin both sides (editor measured), wheels and roof inside,
  car centred slightly above mid-height. Editor: confirm the finished render (16/80 frames done) keeps the margin on the last frame.

### 2. s3_wheel (beats 8-10) - reuse v1
- Camera (as rendered): (-1.95, -0.85, 0.42) -> (-1.95, -1.95, 0.40), target (-0.85, -1.38/-1.45, 0.34), 38 mm; tracks forward past the wheel.
- Framing: first = wheel + arch fill ~85 % width; mid = wheel centred, full tyre visible; last = wheel with the fender above.
  The wheel is deliberately the whole subject (extreme close-up); tyre clipping at the bottom edge is accepted only if it is the
  rendered v1 framing (finA row 3: tyre is inside). No plate in frame.

### 3. s4_nose (beats 10-14) - reuse re-rendered
- Camera (as rendered): (-1.55, -3.35, 0.95) -> (-0.25, -3.6, 0.85), target (-0.55, -2.05, 0.72) -> (-0.3, -2.1, 0.66), 36 mm.
- Framing: first = right headlight fills the left-centre; last = grille + both lamps, front-centre. Plate flattened (no text readable).
  Ends front-centre, where s5 starts wider and lower.

### 4. s5_front - FRONT END HERO (beats 14-24, 196 frames) - NEW
Focus: the front bumper, then **what is behind it**: the front-mount intercooler and its charge pipes, the corner brackets.
- **Camera** (30 mm, 2 mm base where possible / comp_explode):
  - beat 14 (t 0): (0.25, -5.9, 1.15) -> (0, -2.0, 0.45). Low front, ~10 deg down. Whole front end + both front wheels.
  - beat 17.5 (t 2.28): same pose drifted to (0.15, -5.5, 1.10) (slow push while the bumper travels).
  - beat 21 (t 4.57): (0.05, -4.3, 0.95) -> (0, -2.0, 0.42). Push in on the intercooler core. Hold-and-creep, no rotation.
  - beat 24 (t 6.52): (-1.7, -3.9, 1.05) -> (-0.55, -1.9, 0.40). Last 3 beats swing ~35 deg to the front-right corner: shows the
    right charge pipe/bracket and the empty bumper corner, and hands off to the right side (travel).
- **Part action** (front bumper, translate only - derived outer skin has no inner face):
  - beat 16 -> 17.5: offset (0, 0, 0) -> (0, -0.80, -0.30), ease out. Straight forward and down into the black below the
    intercooler; it stays in front of and below the camera's sightline, so only its outer face shows (its hollow back read
    badly from above, chk/s6crop.png). No rotation.
  - holds at (0, -0.80, -0.30), drifting to (0, -0.84, -0.32) by beat 38 (lin), so it never freezes.
- **Framing first/mid/last:** first = whole front end ~67 % width (2.7 m coverage at 3.95 m), bumper on, roof line inside the
  top third; mid (beat 19) = intercooler + both headlight corners ~80 % width, bumper visible in the bottom quarter outer face
  on; last = front-right corner: pipe/bracket + headlight fill the centre, bumper edge bottom-left. No black hole where the
  bumper was: by beat 18 the intercooler/state geometry fills it (verify on the beat-18 still).
- **Labels** (Inter Display, tracking +6, #e8ecf2, ~44 px cap height, top band y 180-320 px over black, centred; check every
  frame of the window is black behind the text; if not, move it to the black band between the bumper and y = 1536):
  - `FRONT BUMPER REMOVED` - in beat 17.5, out beat 20.5 (from the state file name "front end bumper removed").
  - `FRONT-MOUNT INTERCOOLER` - in beat 21, out beat 23.5 (core + end tanks + charge pipes are clearly visible in f_0060;
    clips.md lists FMIC). Do NOT label radiator, crash beam or fans (not identifiable with confidence, open question 2).
- Why it earns 10 beats: the densest real geometry in the set; reviewer wants to see what's behind the removed part, held long enough to read.

### 5. s6_side (beats 24-30, 117 frames) - NEW
Focus: the right side skirt, then the bare sill.
- **Camera** (30 mm): beat 24: (-2.2, -1.7, 1.45) -> (-0.85, 0.15, 0.22), looking rearward along the right sill from just behind
  the front wheel, ~30 deg down; the sill runs diagonally up the 9:16 frame. Beat 30: (-2.3, -0.5, 1.55) -> (-0.85, 0.75, 0.22).
  Pure dolly rearward 1.2 m, no orbit.
- **Part action** (sideskirt, pivot = its centroid (-0.75, -0.14, 0.26)):
  - beat 25 -> 26.5: offset -> (-0.55, 0, -0.08), ease out (out into the black beside the car, toward camera-left, not across the body).
  - if the backside still confirms a scanned inner face: beat 26.5 -> 28.5 roll about its long (Y) axis rot (0, -70, 0) so the
    inner/mounting face (+X) turns up toward the camera; hold to 38.
  - fallback (back is noise): no rotation; instead drift to (-0.60, 0, -0.10) by beat 30.
  - all later beats: keep (-0.55..-0.60, 0, -0.08..-0.10) [+ roll] until the finale.
- **Framing:** first = whole skirt from front to rear end inside the frame (front wheel at most a partial edge at the
  bottom-right, not a subject), ~60 % of the frame height; mid = skirt out, sill state (bare sill / mount line) visible
  between skirt and body; last = sill rear half + rear wheel arch at top, handing off to the rear.
- **Label:** `SIDE SKIRT REMOVED` - in beat 27, out beat 29.5 (state file "Side Skirt under" = sill with the skirt off).
  Top band over black (the car occupies the lower-right diagonal; check).

### 6. s7_rear (beats 30-38, 157 frames) - NEW
Focus: rear bumper (its inner face), then the opened rear: bumper beam, trunk floor.
- **Camera** (30 mm): beat 30: (-2.2, 5.3, 2.4) -> (-0.05, 1.9, 0.6), rear-right high 3/4, ~25 deg down, tail ~60 % width.
  Beat 34: (-1.8, 4.8, 2.6) -> (0, 1.85, 0.55). Beat 38: (-1.2, 4.3, 2.8) -> (0, 1.7, 0.5): rises and moves in over the open
  trunk (~15 deg of orbit total; the move is the push-in, not a rotation).
- **Part actions:**
  - rear bumper (pivot = centroid (-0.04, 1.86, 0.46)): beat 31 -> 32.5 offset -> (0, +0.95, +0.25) ease out (straight back,
    clear of the body); beat 32.5 -> 34.5 tip about the car-width (X) axis to rot (-110, 0, 0) so the inner/mounting face that
    faced the car ends facing up and back at the camera (Rx(-110) maps (0,-1,0) to (0, 0.34, 0.94)); verify sign on a still.
    Lessons: tip about the width axis, never a Z spin. **Fallback** (backside still is noise): no rotation, offset
    (0, +0.90, -0.25) (back and down into black).
  - trunk lid (pivot [0, 1.95, 0.95]): beat 33 -> 34.5 offset -> (0, +0.10, +0.75), rot (0, 0, 0) ease out. Straight lift, no
    tilt (no inner face to show; the draft's 12 deg tilt goes). Reveals the Rear Trunk Open state underneath.
- **Framing:** first = whole tail (both lamps, bumper, spoiler lip) ~60 % width, nothing clipped; mid (beat 34.5) = bumper
  lying inner-face-up in the lower third, beam and trunk opening centre, lid hovering in the upper third, all inside the
  80 px safe margin; last = trunk floor + beam fill the centre ~75 % width, bumper inner face at the bottom edge, lid top
  partly cropped at most.
- **Labels:** `REAR BUMPER REMOVED` in beat 32, out beat 34.5 (part scan "Rear Bumper" + state); `TRUNK OPEN` in beat 35,
  out beat 37.5 (state file "Rear Trunk Open"). Top band if black there; otherwise the black band below the bumper (above y 1536).

### 7. s8_finale (beats 38-48, 196 frames) - NEW (replaces draft s8_side/s9_wide and v1 s8_explode)
Focus: all four parts out at once (the only overview of the explode), then the reassembly landing on the triple hit.
- **Camera** (28 mm, one continuous move, no cut inside):
  - beat 38: (-0.4, 2.0, 7.0) -> (-0.2, -0.1, 0.4). High behind, ~72 deg down, nose at the TOP of the frame, car length along
    the 9:16 height (A90/Temerario layout). This is the TOP section.
  - beat 42: (0.6, 2.6, 6.2) -> (0, 0, 0.45). Slow descent.
  - beat 46: (3.4, 4.6, 3.1) -> (0, 0.3, 0.55). Lands on a high rear-LEFT 3/4 (~40 deg azimuth change + descent over 8 beats).
  - beat 48: (3.25, 4.45, 3.0) -> (0, 0.3, 0.55). Last creep during the fade.
- **Part actions** (global timeline):
  - beat 40 -> 41 (loudest): every part adds +0.40 m Z on top of its current offset (layers above the car), ease out.
  - home (ease in, each lands on a hit): skirt 43 -> **44**; front bumper 43.5 -> **45**; rear bumper (un-tip to rot 0) 44 -> **46**;
    lid 44.5 -> **46**. All offsets/rotations -> 0.
  - **beat 46: swap base comp_explode -> clean car.blend** (lesson C5: last frames must not show frayed composite seams);
    parts hidden at the same frame (render-local frame ~79).
- **Framing:** first = car + all four parts inside the frame, ~72 % of height (6.3 m span over 8.7 m coverage), skirt visible
  on the left of the car's right side; mid (beat 41) = layers above the car, nothing past the 80 px margin; last = whole
  assembled car, rear-left 3/4, 65-75 % width, wheels and roof inside. Different side and height from s1 (front-right, low).
- No labels (whole-car shot; the parts were named in their sections).
- Edit: fade to black 47.2 -> 48 (0.52 s).

### 8. logo (beat 48 -> 37.4 s)
Small logo (380 px, ~35 % width) fades in on black, fades out with the track. Reuse `out/logo_card_v2.mp4`, 181 frames.

---

## 4. Cut list

**vs v1 (project_v1.yaml):**
- s1_front34 - cut: car clipped both sides (reviewer). Replaced by s1_wide.
- s2_rear34 - cut: whole car again (IoU 0.76 with s1, "same view twice") and front->rear->front ping-pong.
- s3_wheel - kept, moved 14-16 -> 8-10.
- s4_nose_v1plate - cut (legible plate); s4_nose re-render kept, moved 16-20 -> 10-14.
- s5_front_off - cut: wide orbit, bumper slid sideways out of frame, IoU 0.62 with the opener; replaced by s5_front (held, in on the intercooler).
- s6_trunk - cut: separate trunk shot; the trunk now opens inside s7_rear with the rear bumper (same section, one sequence).
- s7_top - cut: rotating top-down = wasted rotation (lesson); the top section lives in the finale's first beats.
- s8_explode - cut: all parts separating at once in one wide orbit (lesson: never); replaced by section-by-section separation + s8_finale.

**vs the editor's v2 draft (project.yaml):**
- s2_rear (wide rear 3/4) - cut: second whole-car shot, and the travel ping-pong the editor flagged.
- s5_front + s6_core - merged into one 10-beat s5_front (same subject in two shots).
- s7_rear / s8_side - swapped (side before rear: front -> side -> rear).
- s9_wide - becomes s8_finale with a top-down start; lid tilt and the 12 deg lid rotation dropped.

## 5. Hold list (> 0.75 s with little part motion)
- s5 beats 17.5-21 (2.3 s): bumper parked, camera pushes in on the intercooler - the reading time the addendum asks for.
- s6 beats 28.5-30 (1.0 s): skirt parked, camera dollies along the sill - shows the bare sill state.
- s7 beats 34.5-38 (2.3 s): parts parked, camera rises over the open trunk - reading time for beam/trunk floor.
- s8 beats 38-40 (1.3 s): exploded overview, camera descending - the only frame where all four parts are seen together.
- s8 beats 46-48 (1.3 s): locked clean car + fade - the landing; not longer (reviewer: last scenes held too long).
- logo 6.0 s: music tail (fixed by the brief).

## 6. Render budget (15 fps, +1 frame and +3 tail frames per shot for minterpolate)
| shot | seconds | frames |
|---|---|---|
| s5_front | 6.533 | ~102 |
| s6_side | 3.900 | ~63 |
| s7_rear | 5.233 | ~83 |
| s8_finale | 6.533 | ~102 |
| **new total** | | **~350** (<= 450; ~88 min at 15 s/frame) |
| backside stills (rear bumper, skirt) | 2 stills at 30 % | negligible |

Reused unchanged: s1_wide (in progress), s3_wheel (v1), s4_nose (plate-flattened re-render), logo card.
Render with persistent data off and scan every frame's luma (lessons: lighting dropouts in animated part shots).

## 7. Open questions for the editor
1. **Backsides:** normals say the rear bumper and side skirt part scans are two-sided. Render one 30 % still of each from behind
   (cameras in section 1) and pick tip/roll vs the translate fallback before the final renders.
2. **Front end identification:** the upper member with two round shapes behind the grille line, and anything you'd call a
   radiator or crash beam - I could not identify them with confidence in f_0060 / the solo state render, so they are NOT labelled.
   If a closer still makes the radiator unmistakable, a label may replace `FRONT-MOUNT INTERCOOLER`, never be added as a third.
3. **Sill state coverage:** check on the beat-27 still that comp_explode's right sill (Side Skirt under) has no black hole where the skirt sat.
4. **s3_wheel** has 21 source frames for 39 output frames (as in v1) - fine if it played smoothly in v1; otherwise slow src_fps slightly, don't re-render.
5. **Labels vs the "no text" brief:** labels follow the user's addendum (it overrides); they carry no numbers.
