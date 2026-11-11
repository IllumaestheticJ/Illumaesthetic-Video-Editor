# Mazda Miata NC v2: scene direction + shot plan

Written by the scene director (stage 1) and the director (stage 2), 2026-11-11. This file replaces the v2 draft timeline in
project.yaml. The rule set comes from lessons.md, the three user notes on this reel, the parent v2 brief, and the parent's
later notes (cropping, one sequence per section, the bumper-removed state as the hero, opening states, and no cuts on
n=29-32). Where two notes conflict, the newer one wins.

Grid: t(n) = -0.524 + 0.58241·n, cut frame = round(t·30). The kick hits on every n from 1 to 64 **except n=29-32**
(the breakdown, 16.37-18.11 s): **no cut may land on n=29-32**. The drop is n=33 (18.696 s, frame 561). Music is out at
n=65 (37.33 s) and the last audio is about 37.9 s. The video runs 1140 frames (38.0 s).

## 1. Feature inventory (from clips.md, editlog and renders I looked at)

| region | scans / states (registered) | parts | signature / weak data | richness |
|---|---|---|---|---|
| **front: bumper removed** | "Front Bumper Off (Hood Closed)" (identity, p50 1.6 mm) | bumper.blend ("Bumper only": scanned inside + outside) | Behind the bumper (seen in final/s8a_front f_0040 and f_0108, nose crop y 380-940): a **horizontal beam with lightening holes across the nose at bumper height**, the **exposed headlamp housing** (rounded unit, right side), plus radiator-support structure and loose wiring/ducting. The bumper's outer skin shows the grille opening and badge. | **highest**: 1 part + 1 state |
| **engine bay** | "Front Bumper Off (Hood Open)" (bay, no propped hood), "Hood and Bumper Removed" (stands, fills limited to z > 0.23 m) | hood4 (cut from the full car on its seam, **top skin only**: the underside is not scanned), HOOD_PIVOT at the cowl | Dense bay: engine, strut towers, intake (s8a f_0108). The hood-open angle is not captured (no hinge fit); the motion is plausible, not measured. | high: 2 states |
| front exterior | full car (car4 4 mm / car3 3 mm) | none | headlight (Drive: Headlight Project, **Left Bucket** .stl/.stp + RE.xrl), grille mesh, fog lamp | medium (label-backed) |
| wheels | full car | none | Aftermarket 7-spoke wheels. Weak: old_v1/s3_wheel shows **holes in the spokes and a ragged tyre bottom**. The Drive folder `nc fender scoop/` (Straight, Steered out) is not registered. | low; keep it short |
| rear | 2023 "Trunk Closed" / "Trunk Open" (FPFH+ICP, rmse 4.4 mm) | lid4, fitted hinge (74.27°, median 1.0 mm) | Trunk interior + spare-wheel well (s6 f_0038). **The licence plate is LEGIBLE** in final/s6_trunk f_0001 (reads like "NERDLER"). A tail-lamp lens is a dark scan hole (s6 f_0038). There is **no lid-removed scan**. | medium: 1 state |
| side / top | full car only | none | PRHT hardtop; no states | low: no section of its own |

The richest regions are the front bumper-removed state and the engine bay. The front-bumper-removed state is the hero beat
(parent note C). The engine bay takes the drop.

## 2. Scene order and music map

The camera travels front → rear on the car's right side, with one continuous sequence per section. The top view appears
only in the ending. There is no separate side section because the side has no state or part data (scene-director:
"leave out any rung that has no data").

| # | section | shot | frames | t (s) | n | dur | scans used | feature shown | why here |
|---|---|---|---|---|---|---|---|---|---|
| 1 | whole car | OPEN | 0-89 | 0.000-2.970 | 0-6 | 2.970 | car4 | the whole car, front-right 3/4 | The opener frames the end with the richest data (front); it moves from frame 1. |
| 2 | wheels | WHEEL | 89-142 | 2.970-4.718 | 6-9 | 1.767 | car3 | front-right wheel + arch | label-backed detail; weak data, so it stays short |
| 3 | front exterior | LAMP | 142-194 | 4.718-6.465 | 9-12 | 1.733 | car3 | headlight, nose, grille | label-backed detail; this is the last view of the intact nose before it comes apart |
| 4 | **front bumper removed (hero)** | B1 BUMPER OFF | 194-264 | 6.465-8.795 | 12-16 | 2.333 | comp_explode + bumper | the bumper slides off the nose | user: "focus on the front bumper" |
| 5 | **front bumper removed (hero)** | B2 BEHIND THE BUMPER | 264-421 | 8.795-14.036 | 16-25 | 5.240 | comp_explode ("Front Bumper Off") | the beam, headlamp housing and mounts behind the bumper | parent C: move IN and hold long enough to read |
| 6 | engine bay | B3a HOOD OPENS | 421-561 | 14.036-18.696 | 25-33 | 4.660 | comp_explode + hood4 | the hood opens over the "Hood Open" bay | one shot covers the breakdown with no cut on n=29-32 |
| 7 | engine bay | B3b HOOD OFF | 561-701 | 18.696-23.355 | 33-41 | 4.660 | comp_explode + hood4 | the hood lifts off **ON the drop**, then the push into the bay ("Hood and Bumper Removed") | The second-richest region gets the biggest musical moment. |
| 8 | rear | REAR | 701-840 | 23.355-28.014 | 41-49 | 4.660 | comp_explode + lid4 (front parts held off) | the lid opens on its hinge, then the move IN to the trunk interior and the lid's inner face | front, then rear; the only rear sequence |
| 9 | top / reassembly | END | 840-1015 | 28.014-33.838 | 49-59 | 5.823 | comp_explode + 3 parts, then car4 | high top view: every removed state at once → everything flies home → clean car → fade | Temerario ending; the top view appears only here |
| 10 | logo | LOGO | 1015-1140 | 33.838-38.000 | 59-end | 4.167 | logo_card.mp4 | small logo | ends with the music |

Beats: 6+3+3+4+9+8+8+8+10 = 59 beats, plus the logo tail. Every cut lands on a kick (n = 6, 9, 12, 16, 25, 33, 41, 49, 59).
None falls on n=29-32. Section changes fall on bar lines where possible (n=9, 25, 33, 41, 49). The drop (n=33) is
a hard cut, and the hood lifts in the same frame.

The first clip is one frame short (lessons). The parent's notes call for a cut-only assembler: use
`projects/honda-s2000/tools/concat_assemble.py` with exact `frames:` per clip, or check the cut-hold-frame behaviour
of `ive assemble`.

## 3. Diff against v1 and the v2 draft

| shot | v1 | v2 draft | v2 final | why |
|---|---|---|---|---|
| s1_front turntable | 0-4.7 | dropped | dropped | user: rotations wasted |
| s2_rear orbit | 4.7-8.8 | dropped | dropped | rotations; s1~s2~s9 repeated whole-car 3/4 |
| s1p_front | none | specced r 5.0→4.1 | **OPEN, re-specced** | The old spec crops the rear at r 4.1 (s1_front at r 4.7 already fills 100 % of the width). The new spec sits wider and starts moving on frame 1. |
| s2p_rear | none | specced | **dropped** | a second whole-car 3/4 (s1~s2 flag); the rear now has one sequence |
| s3_wheel / s4_lamp | 1.17 s each | 3 beats | **kept** (reuse old_v1, 21 frames each) | label-backed details; they come before any part moves, so the bumper they show is correct |
| s5_hood | 11.1-14.0 | 6.5-9.4 | **dropped** | The bumper is still ON while the hood opens, so the engine bay would be split across two sequences (s5 and the hood-off shot), and it is flagged s4~s5 and s5~s6. Replaced by B3a. |
| s6_trunk | 14.0-16.3 | 11.7-14.0 | **dropped** | The plate is legible, the rear-left 16° drift is an orbit, the car's front is cropped by accident, and the front parts are ON (continuity). Replaced by REAR. |
| s7_top / s7p_top | rotating top-down / straight track | track | **dropped** | The top appears only in END. |
| s8_explode | wide orbit, all parts at once, bumper flip | dropped | dropped | user note 2 |
| s8a_front | none | 16.4-23.4 | **frames 1-35 kept as B1** | The bumper slide (0.35-2.1 s) is correct and framed on the front. The hood lift-off at 2.33 s render time is cut off, because the engine bay comes later in its own sequence. |
| s8b_rear / s8c_home | none | 23.4-30.3 | **dropped** | The lid lifts off (invalid: there is no lid-removed scan). |
| s9_hero | 30.3-33.8 | 30.3-33.8 | **dropped** | a repeated whole-car 3/4 (s1~s9, s2~s9 flags); END ends on the clean car instead |
| logo | 4.17 s | 4.17 s | 4.17 s | ends with the music; see open question 6 |

The v1 repeated-view flags are all resolved. Only one whole-car 3/4 remains (OPEN); END is a top view. s4 (a lamp
close-up) has no front-3/4 neighbour, because s5 is gone. Nothing from the rear-left 3/4 remains.

## 4. Per-shot plan: focus, camera, part keys

Scan frame: metres, nose = -Y, car's right = -X, Z up; the car spans y -1.99..+1.99, x ±0.93, z 0..1.18. Bearings
use the shots.py convention (0 = front, -90 = car's right, 180 = rear). Sensor 20.25 mm, 9:16, 15 fps, res 75 %,
12 spp, persistent data OFF (already set in shot.py). Every move is a straight dolly or push (no orbit, no turntable).
Eases come from shot.py (inout|in|out|lin).

Shared part poses (new constants in shots.py):
- `BUMP_OFF  = (0, -0.85, -0.02), rot 0` (as in s8a: where B1 leaves it)
- `BUMP_PARK = (+1.60, -0.85, -0.05), rot 0`: slid sideways to the car's left, into clear black, out of the B2 frame
- `HOOD_OPEN = loc 0, rot (-55, 0, 0)` about HOOD_PIVOT (as in s5)
- `HOOD_UP   = (0, +0.35, 0.85), rot (-8, 0, 0)` about HOOD_PIVOT: lifted off, up and back over the windscreen
- `LID_OPEN  = rot (+74.27) about HINGE_LID["axis"] at HINGE_LID["p"]` (hinge only; the lid never translates)

| # | section | shot | focus | camera (loc → loc, target → target, focal) | part action (shot time, s) | earns its seconds because | source |
|---|---|---|---|---|---|---|---|
| 1 | whole car | OPEN | the whole car, front-right 3/4 | `push(3.2, ang=-35, r 6.6→5.9, h 1.15→1.05, c=(0,-0.1,0.5), tz=0.45, focal 30)` with **ease "out"** (moving on frame 1; the v2 spec's "inout" starts at rest). The car should cover about 70→80 % of the width, with margins on both bumpers, the roof and the wheels. If the first/mid/last check shows clipping, raise r by 0.3. | none | the only whole-car view before END; it sets the subject | **NEW**, 48 f (3.2 s) |
| 2 | wheels | WHEEL | the front-right wheel | unchanged (s3 spec, slides forward along the flank) | none | label FENDER SCOOP; it shows the wheel data the scoop project used | **REUSE** old_v1/s3_wheel 21 f; src_fps ≈ 20/(1.767+0.1) = 10.7 |
| 3 | front exterior | LAMP | the headlight | unchanged (s4 spec, slides across the nose) | none | label HEADLIGHT PROJECT | **REUSE** old_v1/s4_lamp 21 f; src_fps ≈ 10.9 (see open question 2: left vs right lamp) |
| 4 | bumper removed | B1 BUMPER OFF | the front bumper | as rendered: bearing -58, r 4.1→3.7, h 2.5 (s8a) | bumper slides 0.85 m straight out of the nose, 0.35-2.1 s; the hood is still closed | the user's own note: framed on the front while the bumper comes off | **REUSE** final/s8a_front **frames 1-35 only** (render t 0-2.27 s; the hood starts moving at 2.33). src_fps = 34/(2.333+0.1) ≈ 14.0 |
| 5 | bumper removed | B2 BEHIND THE BUMPER | what the bumper covered: the beam, headlamp housing and mounts | loc (-0.55, -3.60, 1.05) → (-0.30, -2.65, 0.80), target (-0.15, -1.85, 0.45) → (-0.10, -1.80, 0.42), focal 32, inout. This is a straight push of about 1 m into the nose. At the end, the beam and the headlamp housing fill the lower two-thirds of the frame. | bumper BUMP_OFF → BUMP_PARK from 0.0 to 1.0 s, ease inout (continues B1's motion; it slides sideways into clear black and leaves the frame). It stays parked after that. Hood closed, lid closed. | **the hero beat** (parent note C): bumper off → move IN → hold about 3 s on real "Front Bumper Off" geometry while the camera keeps moving | **NEW**, 82 f (5.44 s render) |
| 6 | engine bay | B3a HOOD OPENS | the bay as the hood swings up | loc (-1.00, -3.40, 1.70) → (-0.75, -3.00, 2.15), target (0, -1.45, 0.60) → (0, -1.35, 0.55), focal 30, inout. The camera rises to look over the nose into the bay. | bumper held at BUMP_PARK. Hood: hold 0-0.6 s, then 0 → HOOD_OPEN from 0.6 to 2.9 s, ease inout ("Front Bumper Off (Hood Open)" bay). Open hood held from 2.9 to 4.66 s through the breakdown. | It covers the whole breakdown (n=29-32), so the shot needs no cut there. The 1.75 s on the open bay builds tension for the drop. | **NEW**, 73 f (4.86 s) |
| 7 | engine bay | B3b HOOD OFF | the engine bay, assemblies | loc (-0.55, -2.55, 2.45) → (-0.35, -2.15, 1.95), target (0, -1.25, 0.55) → (0, -1.15, 0.50), focal 32, inout. This is a high push down into the bay (engine, strut towers, intake). | hood starts at HOOD_OPEN and moves → HOOD_UP from 0.0 to 1.2 s, ease **out** (it moves on the drop frame and rises up and back, out of the top of frame, away from the lens). Bumper at BUMP_PARK. Lid closed. | the drop; "Hood and Bumper Removed" is the second removed state; the brief says to zoom into assemblies | **NEW**, 73 f |
| 8 | rear | REAR | the trunk lid, then the trunk interior | `push(4.86, ang=-145, r 3.6→2.9, h 1.90→2.15, c=(0,1.35,0.6), tz=0.6, focal 30)`, i.e. loc (-2.07, 4.30, 1.90) → (-1.66, 3.73, 2.15) | lid: hold 0-0.6 s, then 0 → LID_OPEN from 0.6 to 2.4 s, ease inout (2023 "Trunk Open"; the lid only hinges). The push then continues into the trunk interior and the lid's inner face. Front parts held (BUMP_PARK, HOOD_UP; off frame). | the only rear sequence; it moves in to show the inner face (brief) | **NEW**, 73 f. **Blocked on the deplate** (section 8) |
| 9 | top / reassembly | END (+ END_clean) | the whole car with every removed state, then whole again | Near-top view from behind, so the nose points to the top of frame (as in s7_top's end): loc (0, 1.20, 5.20) → (0, 1.30, 5.60), target (0, -0.30, 0.50) → (0, -0.25, 0.50), focal 30, ease lin (a slow rise). It looks down about 73°. The covered height is about 5.9 m, enough for the car plus the parked bumper and HOOD_UP, with margins. | 0-1.165 s: bumper at BUMP_PARK, hood at HOOD_UP, lid at LID_OPEN. **1.165-3.495 s (n=51 → n=55): all three return home**, ease inout (bumper to 0, hood to 0, lid hinges back to 0). **At n=55 (shot t 3.495, frame 945), cut to END_clean**: the same camera keys, base car4, no parts, frames 53-90 (lessons c5: swap to the clean car on a kick). The assembler fades to black over frames 1003-1015. | the Temerario ending: every real state at once, then reassembly, a fade and the logo. It is a new view, not a repeat of the opener. | **NEW**: END 0-3.5 s on comp_explode + parts (53 f) + END_clean 3.5-6.0 s on car4 (38 f) = 91 f |
| 10 | logo | LOGO | the logo | /home/user/media/work/miata/logo_card.mp4 (4.167 s, 1080×1920) | none | the music runs to 37.3 s | REUSE |

### Labels (ScanHUD; at most 2 items on screen, which in practice means one label (title + sub) at a time; enter after a cut and leave before the next)

| frames | shot | title / sub | position |
|---|---|---|---|
| 95-137 | WHEEL | FENDER SCOOP / WHEEL: STRAIGHT + STEERED OUT (approved) | x 0.08, y 0.80 (check the tyre is not under it) |
| 148-189 | LAMP | HEADLIGHT PROJECT / BUCKET REVERSE-ENGINEERED TO CAD (approved) | x 0.08, y 0.80 |
| 206-258 | B1 | FRONT BUMPER / SCANNED ON + OFF THE CAR (approved) | x 0.92, y 0.12, align right (top-right black) |
| 285-410 | B2 | **FRONT BUMPER REMOVED** / sub: none for now (see open question 1) | top of frame (y 0.10); keep it off the structure |
| 575-690 | B3b | HOOD / SCANNED OPEN + REMOVED (approved) | x 0.08, y 0.80 (the bay is upper-middle) |
| 720-830 | REAR | TRUNK LID / SCANNED OPEN + CLOSED (approved; no "lifts off") | x 0.08, y 0.80 |

No text appears on OPEN, B3a (the breakdown), END or LOGO. No numbers appear anywhere, so no data claims are needed.

## 5. Cut list (removed from v1 / the v2 draft)
- s1_front, s2_rear, s7_top and s8_explode: camera rotations (user note 1); the s8 wide orbit separated every part at once (user note 2).
- s2p_rear and s9_hero: whole-car 3/4 views that repeat OPEN (v1 flags s1~s2~s9).
- s5_hood: bumper on; it would split the engine-bay section (s4~s5 / s5~s6 flags).
- s6_trunk: legible plate, accidental crop, front parts on, and an orbit drift.
- s7p_top: the top appears only in END.
- s8a_front frames 36-108: the hood leaves before the bumper section is done. The engine bay is its own sequence (B3).
- s8b_rear and s8c_home: the lid lifts off, which has no scan.
- v2 draft cut 491 (n=29): a cut in the breakdown, where there is no kick.

## 6. Hold list (> 0.75 s with no part moving)
- OPEN 0-2.97: no part moves, but the push runs the whole time. This is the only whole-car establishing view.
- B2 1.0-5.24 (4.2 s): the hero hold that parent note C asks for. The camera keeps pushing for the whole shot. Label 285-410.
- B3a 2.9-4.66 (1.75 s): the open bay through the breakdown, with no cut allowed on n=29-32; it builds tension for the drop.
- B3b 1.2-4.66 (3.5 s): the push into the engine-bay assemblies (Hood and Bumper Removed).
- REAR 2.4-4.66 (2.3 s): the push into the trunk interior and the lid's inner face.
- END 0-1.165: the only frame that shows every removed state at once. END_clean 3.5-5.4: the clean car and the fade.
- LOGO 4.17 s, over the last six beats and the music tail.

## 7. Render budget (15 fps, about 12 s/frame, one Blender at a time, luma-scan every folder)

| shot | frames | new / reuse |
|---|---|---|
| OPEN (s1p_front, re-spec) | 48 | new |
| B2 | 82 | new |
| B3a | 73 | new |
| B3b | 73 | new |
| REAR | 73 | new (after the deplate) |
| END + END_clean | 53 + 38 | new |
| **total new** | **440** (about 88 min) | |
| WHEEL, LAMP, B1 (s8a f1-35), LOGO | 21 + 21 + 35 + 125 (logo frames at 30 fps) | reuse |

**Over the ≲350 target.** Only about 10 s of the existing renders shows correct content (WHEEL, LAMP, B1 and the logo).
Every other existing render is a rotation, is invalid, has a legible plate, or splits a section. Two ways to reach about
350, for the parent to choose from:
- (a) Render the three camera-led shots (B2, B3b and REAR, but not the hood or lid motions) at 12 fps with
  minterpolate. This saves about 45 frames.
- (b) Cut REAR to 2.9 s (n=41-46) and lengthen END. This saves nothing.
- (c) Accept 440 frames.

My recommendation is (c). Render order: REAR last, because it waits on the deplate.
Preview first: run `mode=frames` (first/mid/last at 30 %) for every new shot and check the cropping before any final
render. The parent's notes require first, middle and last frames to have nothing clipped. B2 must not show the parked
bumper after 1.0 s. END must keep the parked bumper and HOOD_UP inside the frame with margins.

## 8. Open questions / blockers (not guessed)
1. **B2 sub-label.** In s8a f_0040/f_0108 I can see a horizontal beam with lightening holes across the nose at bumper
   height and the exposed headlamp housing. I believe the beam is the crash beam (bumper reinforcement), but I have not
   seen it in a close render. Plan the generic "FRONT BUMPER REMOVED". Add "CRASH BEAM + HEADLIGHT HOUSINGS" only after
   the editor or user confirms it on the B2 preview frames.
2. **Which lamp is the Headlight Project?** The Drive files are named "Left Bucket". s4_lamp shows the car's **right**
   headlight (camera x < 0). If "Left" means the car's left lamp, the shot should be mirrored (x → -x, about 33 new
   frames) so the label sits on the lamp that was actually reverse-engineered. Until that is confirmed, the plan reuses s4.
3. **Plate (BLOCKER for REAR/END):** the plate is legible in s6 f_0001. Run a deplate pass (infiniti-g35 or
   subaru-sti-blobeye `tools/deplate.py`) on comp_explode and car4 before REAR, END or END_clean.
4. The hood's underside is the backface of its skin (hood4 is top skin only). Do not tip it toward the lens or claim it
   was scanned. HOOD_UP keeps the top skin facing the camera in B3b and END.
5. **Bumper inner face:** I chose a **translation only** (no flip), because the parent's later note C makes what is
   *behind* the bumper the hero. The bumper's scanned inside is seen briefly from above as it parks and flies home.
   If the user still wants the inside, add a +90° tip about X (A90 lesson) to the BUMP_PARK pose in B2/END. That adds
   no new frames, but check the sign on a preview.
6. Logo length: 4.17 s (the existing card ends with the music). Lessons suggest about 2.4 s. A shorter logo would need
   END to grow by 1.75 s of held clean car, which is worse. Keep it unless the user says the end drags.
7. Weak wheel data (holes in the spokes, ragged tyre bottom in s3). It is kept at 1.77 s because of the approved label.
   Drop it if the user prefers.
