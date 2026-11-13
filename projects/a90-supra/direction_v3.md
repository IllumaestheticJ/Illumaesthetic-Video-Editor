# A90 Supra v3 - direction (scene-director stage, 2026-11-13)

Plan only. Nothing rendered, Blender not run. Sources read: lessons.md (all), plan_v2_sections.md, review.md (v2),
feedback.jsonl (v3 brief = last 4 entries), clips.md, editlog, build_v3.py/json, and these images (looked at, not
inferred from names): `v3/chk/cmp_0822_{front,side,rear}.jpg`, `off_0822_{front,rear}.png`,
scratchpad `under_car_low_1113.png`, `int_Interior_1113.png`, `int_Center_1113.png`.

Conventions: plan_v2 frame (m): nose +X, car-right -Y, up +Z, floor z=0; front axle x=+1.20, rear x=-1.25, half-track 0.80.
Camera `az`: 0 = dead ahead of the nose, -90 = right side, +-180 = behind the tail. `hb` = half-beat = 0.335 s = 10.05
frames, counted from the shot's first frame (hb0 = the bar line, hb8 = the next bar line). All camera numbers are
starting values to fit on 30 % previews; part offsets are from the assembled pose.

## 0. Feature inventory (what the data supports)
| Region | Scans | States (real) | Parts (real) | Weak data seen | Richness |
|---|---|---|---|---|---|
| Front end | body, part_fbump (+extra_fbump skin), Radar Cover, Radar Mounting Grille | Under Front Bumper; Front Bumper Duct Removed | bumper in+out, 2 sub-parts | torn hood lip, lamp seam fringe, floating lower bar (section 7) | **highest**: 3 parts, 2 states -> A->B entry, 4 bars |
| Front corner (right) | wheel, rotor, caliper, coilover (+ top/bottom halves, top hat) | none (bench parts on hardpoints) | 4-7 now, +7 IF PLACED | left side is a mirror; chassis scan may carry its own arms | high, 2 bars |
| Fender / side | fender section, door trim, upper + lower skirt, liners | Under Fender, Under Door Trim, Chassis Under Upper Skirt | 4 | ragged fender opening top edge, flat patch + tongue on the sill, trim/skirt tints interleave | medium, 2 bars |
| Interior | Interior, Center Console | none (no roof-off / door-open) | console (if the Interior scan has the console out) | ragged door-card strips at both sides, holes in the passenger dash | medium, 2 bars, camera-led |
| Rear corner (right) | wheel, rotor, caliper, spring, damper | none | 5, +10 IF PLACED | as front corner | medium, 1 bar |
| Rear end | part_rbump (+extra), (Reverse Light, unregistered) | Under Rear Bumper | bumper in+out | dark open slot under the trunk lip, frayed corners | high (hero 2), 2 bars |
| Underbody | body (chassis scan underside) | none needed (it is the car, seen from below) | none -> shown, never disassembled | speckled floor pans, voids at the nose and arches | medium, 2 bars, centreline only |
| Not usable | trunk-open, headlight units, Bomex CAD, hood/door/roof openings | - | - | - | no scenes |

## 1. Excerpt and bar table
- **Start on the downbeat at track 13.930 s** (0.535 + 5 x 2.679). Run straight to track 67.510 s. **20 bars = 53.58 s,
  no splice.** 3 bars of A, then **A->B at reel 8.037 s (frame 241) = front bumper leaves**.
- Why 3 A bars, not 4: first part motion at 8.0 s instead of 10.7 s (v1/v2 hooks scored 3); underbody still gets 2 bars.
- My own per-bar band check of track.m4a (4 bands, bar grid 0.535 + n x 2.679) agrees with your map and adds:
  A is a 4-bar loop; B is 8-bar phrases. The 500-2000 Hz band thins from B bar 9 (track 43.40) and a high-band
  (2-5.5 kHz) hit sits in B bar 16 (track 62.15-64.83), a new phrase starts at B bar 17 (64.83). With this excerpt:
  B bar 5 (crash-level highs) = front corner starts; **B bar 9 = interior x-ray entry** (texture change);
  **B bar 16 = reassembly lock + clean car; B bar 17 = logo bar**. Please confirm where inside 62.15-64.83 the
  high hit lies; if it is not on the downbeat nothing changes.
- The excerpt starts on riff bar 2 of 4. If the start sounds abrupt: use track 11.251-13.930 (riff bar 1) +
  16.609-21.967 (riff bars 3-4), one splice on a downbeat. Same length.
- Audio out: fade 52.2 -> 53.58 s (the track has no ending inside the excerpt).
- Grid is for planning. Put every cut and every lock on the measured kick attack of the decoded delivered file.

| Bar | Reel s | Frame | Track s | Shot | Section |
|---|---|---|---|---|---|
| 1 | 0.000 | 0 | 13.930 | s01_whole | whole car |
| 2 | 2.679 | 80 | 16.609 | s02_under_r | underbody (tail -> mid) |
| 3 | 5.358 | 161 | 19.288 | s03_under_f | underbody (mid -> nose) |
| 4 | 8.037 | 241 | 21.967 **A->B** | s04_fb_off | front |
| 5 | 10.716 | 321 | 24.646 | s05_fb_sub | front |
| 6 | 13.395 | 402 | 27.325 | s06_fb_beam | front |
| 7 | 16.074 | 482 | 30.004 | s07_fb_duct | front |
| 8 | 18.753 | 563 | 32.683 | s08_fc_brake | front corner |
| 9 | 21.432 | 643 | 35.362 | s09_fc_strut | front corner |
| 10 | 24.111 | 723 | 38.041 | s10_fender | side |
| 11 | 26.790 | 804 | 40.720 | s11_skirts | side |
| 12 | 29.469 | 884 | 43.399 | s12_int_xray | interior |
| 13 | 32.148 | 964 | 46.078 | s13_int_console | interior |
| 14 | 34.827 | 1045 | 48.757 | s14_rc | rear corner |
| 15 | 37.506 | 1125 | 51.436 | s15_rb_off | rear |
| 16 | 40.185 | 1206 | 54.115 | s16_rb_beam | rear |
| 17 | 42.864 | 1286 | 56.794 | s17_lineup | all (only shot with every section) |
| 18 | 45.543 | 1366 | 59.473 | s18_reasm | all |
| 19 | 48.222 | 1447 | 62.152 | s19_clean (3 beats) + logo in on beat 4 | ending |
| 20 | 50.901 | 1527 | 64.831 | logo | ending |
| end | 53.580 | 1607 | 67.510 | | |

All cuts are hard cuts on bar lines (no dissolves: the track hits on every beat). One exception: the 6-frame
crossfade inside s12 (shell -> interior).

## 2. Scenes
Travel: whole -> under (tail to nose) -> front -> front corner -> side -> cabin -> rear corner -> rear -> line-up -> home.
Each section is one run of adjacent shots; no section returns. Rules for every shot: persistent data OFF when a part is
keyed; every keyed path through `clipcheck.py`/`pathcheck.py` (numpy, no Blender) before rendering; first/mid/last
sheet + edge-touch test at 30 %; parts of other sections are hidden (`HIDE`), never half in frame.

### s01_whole (bar 1) - focus: the whole car, wheels on
- No part moves. Camera: front-right 3/4, az -35 -> -55, d 6.0 -> 5.4, z 1.5 -> 0.30, look (0.1, 0, 0.55) -> (0.3, 0, 0.35),
  lens 35. Car at ~88 % of the width with >= 40 px each end on first AND last frame. The drop to sill height is the motion
  from frame 1 and sets up "go under". Raw `car.blend` + 4 corners + interior fill (at-home rule, Revuelto lesson).
- Label: none.

### s02_under_r (bar 2) - focus: exhaust rear half, diff, rear subframe
- No part moves. Camera below the car looking up, nose toward the top of frame, tilted 12 deg off vertical toward the
  nose (never exactly vertical): position (-2.0, 0, -0.85) -> (-0.7, 0, -0.85), look 0.25 m ahead of the camera at
  z 0.2, lens 32 (about 1.2 m of car width across the frame). Passes tips -> rear muffler -> diff + subframe -> twin pipes.
  `underlight` 0.4. Linear travel, no ease (it continues in s03).
- Label: `UNDERBODY REAR` / `EXHAUST · DIFF · SUBFRAME`, x 0.08 y 0.80 (move to wherever the frames are black).

### s03_under_f (bar 3) - focus: resonator, transmission, front subframe
- Same camera continued: (-0.7, 0, -0.85) -> (1.55, 0, -0.80). Stop at x 1.55: the nose beyond it is voids (section 7).
  The last frame is still moving forward; the cut to s04 is the A->B hit.
- Label: `UNDERBODY FRONT` / `TRANSMISSION · SUBFRAME`. Confirm both sublines on a render before use.
- Entry/exit of the underbody: plain cuts on bar lines. It is the chassis scan seen from below - no state implied.
  Keep the frame on the centre 1.2 m: the outer floor pans are speckled and the arches are voids.

### s04_fb_off (bar 4, A->B) - focus: the front bumper comes off (HERO 1)
- Base: `body` + `fill_fbump`. Part: `part_fbump` + `extra_fbump` as ONE object, complete (not carved - Frontier v4).
- Motion, native 30 fps:
  - hb0 (the cut): already moving on frame 1. Straight forward +X 0.45 by hb2 (ease-out). It unbolts forward; do not
    lift or tip before +0.35 (headlamp tips, splitter, and the liners' front edges must clear).
  - hb2 -> hb5: via [0.75, 0, -0.10], then park at [1.05, 0, -0.55] with rot Y ~105 deg so the scanned INSIDE face
    turns up toward the lens (check the sign on one frame). Purposeful flip: both faces are scanned.
  - hb5 -> hb8: parked, fully in frame in the lower half; camera pushes.
- Camera: az -18, d 2.9 -> 2.5, z 1.8 -> 1.6, look (2.2, 0, 0.15) -> (2.5, 0, -0.05), lens 35. Nose section fills the
  upper ~45 %, the parked bumper the lower ~45 %, >= 30 px side margins (bumper ~70 % of width).
- Label (hb2 -> hb7): `FRONT BUMPER` / `INSIDE + OUTSIDE SCANNED` (true, verified in v1).

### s05_fb_sub (bar 5) - focus: how the radar cover and its mounting grille nest in the bumper
- Car hidden (kept only as the light reference). Bumper stays in its s04 park pose.
- Motion, native 30 fps:
  - hb0 -> hb2: no part moves; camera trucks along the inside face from the car-right end (the side rail that meets the
    fender) to the centre: clip tabs and mounting points. On hb2 swap the complete bumper for the carved bumper +
    Radar Mounting Grille + Radar Cover at home (same surfaces, invisible).
  - hb2: grille + cover leave together 0.20 m along the bumper-local normal toward the lens (inside), ease-out, done hb3.5.
  - hb4: the cover lifts a further 0.12 m off the grille, done hb5.5. Result: bumper / grille / cover stacked on one
    axis, all in frame. Hold hb6-8 with a 5 % push.
- Camera: az -30 -> -12, d 1.5 -> 1.2, z 1.2, look at the bumper centre (park pose), lens 40.
- Label (hb2.5 -> hb7): `RADAR COVER` / `+ MOUNTING GRILLE`.
- Checks first: which face the grille's clip flange sits on (decides the exit direction - if it mates from the outside,
  mirror the move away from the lens and show it from the outer face instead); the carved hole edge alone. If the
  carved edge is ragged, do not separate: keep the complete bumper and spend the bar on the inside-face truck.

### s06_fb_beam (bar 6) - focus: what the bumper hid (state: Under Front Bumper)
- No part moves; bumper hidden (fully out). Base `body` + `fill_fbump`.
- Camera, close: az -35 -> -5, d 1.25 -> 1.05, z 0.62, look (2.0, -0.45, 0.38) -> (2.0, 0.0, 0.38), lens 35: from the
  car-right crush can / beam mount, along the crash beam to the centre, radiators behind. Frame top stays BELOW the hood
  lip (torn edge, section 7); frame bottom above the floating lower bar unless it is confirmed real.
- Label: `FRONT BUMPER OFF` / `CRASH BEAM · RADIATORS` (wording confirmed on v2 full-res frames).

### s07_fb_duct (bar 7) - focus: second state, brake ducts removed (1:1 state swap)
- The cut at bar 7 IS the swap: same camera path continued, base `body` + `fill_fduct`. No flying part (no scan of the
  ducts exists). Two renders, plain cut, no interpolation across it.
- Camera: az -5 -> -28, d 1.05 -> 0.80, z 0.62 -> 0.50, look (2.0, 0.0, 0.38) -> (1.95, -0.55, 0.32): push into the
  car-right opening the duct left.
- Label: `DUCTS REMOVED` / subline = what is visible there. Look at the render before naming it; fallback subline
  `FRONT END · SECOND SCAN`.
- If the two fills differ outside the duct zones by more than noise, the swap will flicker: diff `fill_fbump` vs
  `fill_fduct` and take everything outside the duct boxes from ONE of them.

### s08_fc_brake (bar 8) - focus: wheel -> caliper -> rotor come off the hub, in job order
- Parts `p_FR_wheel`, `p_FR_caliper`, `p_FR_rotor`; axle axis from the tread normals (296 v5 lesson). Native 30 fps.
  - hb0 -> hb2: wheel + rotor spin 120 deg about the axle, decelerating to a stop on hb2 (caliper fixed).
    IF AVAILABLE: replace hb1-2 with a steer sweep (10 deg in, back to straight) about the strut-top/ball-joint axis.
  - hb2: wheel straight off along the axle (-Y) 0.30 by hb3, then on to -Y 0.95 by hb4.
  - hb4: caliper slides off the disc along its own radial direction (it sits ~20 deg above rear: up-and-back) 0.10,
    then -Y 0.55, done hb5.5.
  - hb6: rotor straight off the hub along the axle to -Y 0.35, done hb7.5.
  Parked result = one coaxial stack on the axle line: hub / rotor / caliper above the rotor / wheel.
- Camera: az -50, d 2.3 -> 2.1, z 1.5, look (1.2, -1.15, 0.30), lens 32: looking down ~35 deg so the axle runs diagonally
  down-frame and the whole stack is in frame with margins. Fender section still on.
- Label: `FRONT CORNER` / `WHEEL · CALIPER · ROTOR`.

### s09_fc_strut (bar 9) - focus: the strut and what the wheel hid
- Wheel, rotor, caliper hidden (fully out). Native 30 fps.
- Base version (works today):
  - hb0 -> hb2: push on the bare arch: strut, liner, hub area.
  - hb2: coilover drops 0.14 along its own axis (clears the tower), then out -Y 0.40, done hb4.
  - hb4: it separates along its axis into its three scanned pieces: top hat +0.10, top half stays, bottom half -0.14,
    done hb5.5. Hold hb6-8.
- IF PLACED (knuckle, bearing, dust shield, LCA, tension rod, tie rod, sway bar + link):
  - hb0 dust shield off along the axle 0.25; hb1 knuckle + bearing: down 0.06 off the strut clamp, then -Y 0.30;
    arms, tie rod and sway link stay on the subframe and are the picture; coilover moves shift to hb3 / hb5.
  - IF AVAILABLE bump travel: put it at hb0-2 instead of the push (knuckle +-40 mm with the lower coilover half sliding
    in the upper). Only if no mesh has to stretch.
- Camera: az -75 -> -68, d 1.25 -> 1.05, z 0.60, look (1.2, -0.80, 0.42), lens 35.
- Label: `FRONT STRUT` / `COILOVER · TOP HAT` (IF PLACED: `KNUCKLE · ARMS · COILOVER`).

### s10_fender (bar 10) - focus: fender section off, what is behind it (state: Under Fender)
- Base `body` + `fill_fender`. Part `part_fender` + `extra_fender` as one object. Corner parts hidden; arch liner stays.
  - hb0: unclips outward -Y 0.12 by hb1; via [0, -0.35, -0.15]; exits the bottom of frame at [0, -0.45, -0.95] by hb3.
    Translate only (no flip: its back is not the subject).
  - hb3 -> hb8: no part motion; camera pushes into the opening.
- Camera: az -90, d 1.6 -> 1.0, z 0.75, look (0.55, -0.90, 0.55) -> (0.60, -0.85, 0.50), lens 35.
- Label (hb3 ->): `FENDER SECTION` / `WASHER TANK · WIRING` - confirm on the render, else `UNDER FENDER`.
- hb0-3 native 30, hb3-8 can be 15 fps (camera only).

### s11_skirts (bar 11) - focus: skirts and door trim unclip from the sill; the mounting points
- Base `body` + `fill_skirts` + `fill_dtrim`. Low grazing camera along the sill (a side-on camera hides this move).
  - hb0 lower skirt, hb2 upper skirt, hb4 door trim. Each: straight out -Y 0.10 in half a hb (unclip), then away to
    [0, -0.90, -0.30] and out of frame on the outboard side within 2.5 hb. Order = outermost first; confirm with an
    overlap test of the three scans (whichever covers the other leaves first) and reorder if the data says otherwise.
  - hb6 -> hb8: push along the bare sill - the row of clip mounts visible in cmp_0822_side.
- Camera: position ~(1.05, -1.75, 0.45) -> (0.75, -1.55, 0.40), look (-0.55, -0.95, 0.24), lens 35.
- Label: `SIDE SKIRTS` / `UPPER · LOWER · DOOR TRIM`. Native 30 fps.

### s12_int_xray (bar 12, B bar 9) - focus: the cabin, entered without opening anything
- No part moves. Two layers from ONE camera: (a) body + interior for hb0-2, (b) Interior scan alone on black from hb0.
  6-frame crossfade a -> b ending on hb2. The shell never lifts and nothing opens; it fades as an x-ray.
  (A black dim material would hide the cabin - it must be a layer mix.)
- Camera: high over the right side, az -90, d 3.4 -> 2.2, z 3.0 -> 1.9 (about 55 deg down, 12 deg off vertical at most),
  look (-0.1, 0, 0.55) -> (0.25, 0.1, 0.60), lens 35, nose toward the top of frame: seats, dash, steering wheel.
  Keep the ragged door-card strips at both sides out of frame by hb4 (or trim them from the scan).
- Label (hb2.5 ->): `INTERIOR` / `SEATS · DASH · STEERING WHEEL`. 15 fps + interpolation (+ ~12 frames for layer a).

### s13_int_console (bar 13) - focus: centre console lifts off the tunnel, then the rear deck
- Interior alone on black. Part: Center Console scan.
  - hb0 -> hb1: push on the console.
  - hb1: unclips straight up +Z 0.08 by hb2; via [-0.10, 0, 0.25] (clears the dash end and the shifter); parks at
    [-0.15, 0, 0.50], done hb3.5, fully in frame. Translate only unless its underside is scanned and worth showing.
  - hb3.5 -> hb5: tunnel wiring and mounts under it.
  - hb5 -> hb8: camera glides aft over the seat backs to the rear deck: two speaker rings + electronics; the console
    leaves the frame behind the camera.
- Camera: (0.9, 0, 1.55) looking down-aft at the console -> (-0.6, 0, 1.45), look (0.2, 0, 0.55) -> (-1.35, 0, 0.55).
- Label: `CENTER CONSOLE` / `TUNNEL · WIRING`. Native 30 fps hb0-4, 15 fps after.
- GATE: only lift the console if the Interior scan has the console OUT under it (render console in red over the
  interior; int_Interior_1113 looks like a bare tunnel with wiring, int_Center_1113 looks like a carrier with cut-outs -
  not proof). If the Interior scan carries its own console: no lift (it would leave a copy behind); spend hb0-5 on a
  close pass dash -> wheel -> tunnel instead.
- Exit: plain cut on bar 14 to the exterior. From here on the console is home.

### s14_rc (bar 14) - focus: rear brake, spring and damper come out in job order
- Parts `p_RR_wheel/caliper/rotor/spring/damper`. Native 30 fps. No spin here (shown at the front; no repeats).
  - hb0 wheel off along the axle 0.30 then to -Y 0.95 (done hb2); hb2 caliper radial 0.10 then -Y 0.55; hb3 rotor
    -Y 0.35; hb5 spring drops 0.10 then out to [0.12, -0.42, -0.10]; hb6 damper drops 0.16 then out to
    [-0.12, -0.30, -0.16]; all still by hb7.5.
  - IF PLACED: arms, toe rod, knuckle stay on the car as the picture; one extra move only - CV axle slides 0.20 outboard
    along its axis at hb7. The full rear set is seen apart in the line-up.
- Camera: az -125 -> -118, d 2.3 -> 1.9, z 1.5 -> 1.2, look (-1.25, -1.10, 0.30), lens 32.
- Label: `REAR CORNER` / `BRAKE · SPRING · DAMPER`.

### s15_rb_off (bar 15) - focus: rear bumper comes off (HERO 2)
- Base `body` + `fill_rbump`. Part `part_rbump` + `extra_rbump`, one object, complete. Native 30 fps.
  - hb0: straight aft -X 0.45 by hb2. No drop or tip before -0.30: the exhaust tips sit in the bumper cut-outs.
  - hb2 -> hb5: via [-0.75, 0, -0.10], park [-1.05, 0, -0.55], rot Y ~-105 deg, inside face to the lens, fully in frame.
  - hb5 -> hb8: push onto the inside face (mounting rail, brackets).
  - OPTIONAL, only if the Reverse Light registers to the bumper (tint overlay + overlap %): hb6 it backs out of the
    bumper centre 0.12 toward the lens.
- Camera: az -165, d 2.9 -> 2.5, z 1.8 -> 1.6, look (-2.2, 0, 0.15) -> (-2.5, 0, -0.05), lens 35 (mirror of s04).
- Label: `REAR BUMPER` / `INSIDE + OUTSIDE SCANNED`.

### s16_rb_beam (bar 16) - focus: what the rear bumper hid (state: Under Rear Bumper)
- No part moves; bumper hidden. Camera close: az -155 -> 175, d 1.25 -> 1.0, z 0.62, look (-2.0, -0.45, 0.40) ->
  (-2.0, 0.25, 0.36), lens 35: right bracket + exhaust tip -> along the crash beam -> wiring loom.
  Frame top stays below the tail-lamp line (dark slot under the trunk lip, section 7).
- Label: `REAR BUMPER OFF` / `CRASH BEAM · WIRING · EXHAUST`. 15 fps + interpolation.

### s17_lineup (bar 17) - focus: everything that came off, at once
- All parts at line-up parks (separate from the section parks; the jump is never seen because each section shot hides
  the others): front bumper + grille + cover stack ahead of the nose (inside up), rear bumper behind the tail, both
  right-corner stacks outboard on their axle lines, coilover in its three pieces, fender / door trim / skirts in a strip
  along the right sill tilted 35 deg to the lens. Left corners: on the car (mirrored scans are not exploded).
  Console and interior stay home (nothing may appear to pass through the roof).
- Camera: v2 v08 (high over the right side, ~64 deg down, up = nose, lens 31), slow 6 % push. Refit: every part
  >= 20 px inside over ALL frames. No labels. 15 fps + interpolation.

### s18_reasm (bar 18) - focus: it goes back together in reverse order
- Native 30 fps. Each group returns on its exit path reversed (same via points) and SEATS on a half-beat:
  hb2 suspension pieces, hb3 rotors, hb4 calipers, hb5 wheels, hb6 fender + skirts + trim, hb7 rear bumper,
  **hb8 = bar 19 downbeat: front bumper (radar unit nested by hb6) locks.**
- Camera: az -55, d 7.0 -> 6.2, z 3.0 -> 2.3, look (0.2, 0, 0.45), lens 35: front bumper and right side both visible.

### s19_clean + logo (bars 19-20)
- Bar 19 downbeat: hard cut, same camera path, to the clean `car.blend` + corners (composite seams gone on the hit).
  Beats 1-2 drift; fade to black across beat 3 (frames 1487-1507).
- Logo from bar 19 beat 4 (frame 1507, 50.23 s): fade in 0.3 s, **700 px wide** (65 % of 1080), centred on black, full by
  the bar 20 downbeat (new phrase), fade out with the audio 52.2 -> 53.58 s. On screen 3.35 s.

## 3. Progressive state
| After shot | Off the car |
|---|---|
| s04-s07 | front bumper (+ grille, cover from s05); ducts by state swap in s07 only |
| s08-s09 | + FR wheel, caliper, rotor, coilover (+ IF PLACED pieces) |
| s10-s11 | + fender section, lower skirt, upper skirt, door trim |
| s12-s13 | cabin context (console up and back home) |
| s14 | + RR wheel, caliper, rotor, spring, damper |
| s15-s16 | + rear bumper |
| s17 | all of the above, line-up parks |
| s18 -> s19 | all home on the bar 19 downbeat, clean car |
State is defined once on the reel timeline (as plan_v2.py did) and windowed per shot.

## 4. Render budget (75 %, ~13 s/frame wides; close-ups cost more)
30 = native 30 fps. 15 = 15 fps + interpolation, +3 source frames past the cut.
| Shot | s | fps | Frames |
|---|---|---|---|
| s01_whole | 2.68 | 15 | 44 |
| s02_under_r | 2.68 | 15 | 44 |
| s03_under_f | 2.68 | 15 | 44 |
| s04_fb_off | 2.68 | 30 | 81 |
| s05_fb_sub | 2.68 | 30 | 81 |
| s06_fb_beam | 2.68 | 15 | 44 |
| s07_fb_duct | 2.68 | 15 | 44 |
| s08_fc_brake | 2.68 | 30 | 81 |
| s09_fc_strut | 2.68 | 30 | 81 |
| s10_fender | 2.68 | 30 (hb0-3) / 15 | 81, or 58 mixed |
| s11_skirts | 2.68 | 30 | 81 |
| s12_int_xray | 2.68 | 15 (+ layer a) | 56 |
| s13_int_console | 2.68 | 30 (hb0-4) / 15 | 81, or 64 mixed |
| s14_rc | 2.68 | 30 | 81 |
| s15_rb_off | 2.68 | 30 | 81 |
| s16_rb_beam | 2.68 | 15 | 44 |
| s17_lineup | 2.68 | 15 | 44 |
| s18_reasm | 2.68 | 30 | 81 |
| s19_clean | 2.0 | 15 | 33 |
| **Total** | 50.2 | | **1,207** (1,167 mixed) = ~4.4 h at 13 s/frame |
Cut first if over, in this order: (1) mixed fps on s10, s13, and the parked tails hb5-8 of s04/s15 (about -100 frames,
no content lost); (2) s19 to 1.34 s; (3) merge s06+s07 (swap on the half-bar) and start the track at 16.609 with
s02+s03 as one bar - the 16-bar / 42.9 s version also merges s08+s09 and s17+s18 (line-up hb0-3, fly home hb4-8).

## 5. Against v2
- Dropped: 0.3 s dissolves, 4-8 s section shots, rim-glow/dim highlight (close cameras and one part per beat do the
  highlighting), bumper parked above the hood (now below the nose/tail in clear black), fender in the corner shot,
  mirrored left corners in the explode, 270 px logo.
- Added: underbody (2), radar sub-part nest, duct-removed state swap, coilover split, interior x-ray + console, wheel spin.
- Moved: fender to the side section. No v2 render is reusable (bases rebuilt, new timing).
- Section of every shot is in the bar table. Expected `ive director` flags to review, not cut: s06/s07 (same-camera state
  swap), s02/s03 (one move in two clips), s04/s15 (mirrored framing, different ends).

## 6. Risks and assumptions
1. Length: 53.6 s is the top of your range and far above the ~20 s the GD-trio lesson asks for. The 16-bar version is
   in section 4.
2. First part motion is at 8.0 s. The opener relies on the camera drop for motion.
3. Chassis scan vs placed arms: `under_car_low_1113.png` shows arm-like members at both axles in the chassis scan itself.
   If the chassis carries its own arms, the bench-scanned arms will double them - check before any IF PLACED beat.
4. Console gate (s13) and radar exit direction / carved edge (s05) are unverified.
5. `extra_*` skins travel with the parts (fbump 103k tris, fender 27k, rbump 59k): render each part + extra alone from
   both sides. A ragged car-skin patch riding on a flipped bumper would be on screen for 2 bars.
6. Wheel spin, steer and bump are rigid moves of bench scans on hardpoints; steer and bump stay IF AVAILABLE.
7. Under-view lighting and density are untested at final quality (the check image is a splat). Preview s02 first.
8. Labels: 15 one-bar labels; sublines <= 26 chars to finish typing inside ~60 frames; check 4 frames per label for
   parts crossing the text band. Titles all <= 18 chars. Names only, no numbers.
9. Mirrored left corners are still on the car in wides.

## 7. Still reads as leftover or artifact (pixel positions in the named image)
Front, `off_0822_front.png` (1300x900):
- Long curved bar floating below the radiators, x 450-1000, y 560-630. Bumper lip left behind, or the real undertray
  edge? Compare with the Under Front Bumper scan; if the state lacks it, it must travel with the bumper.
- Hood leading edge torn into scallops with dark holes, x 480-950, y 345-375.
- Dashed dark fringe under the car-right headlamp, x 330-690, y 425-460.
- Car-left lamp area shredded with holes, x 880-1010, y 380-470.
- Thin hanging strips at the car-right fender corner, x 235-300, y 350-580 (sliver at x 250-275, y 540-580).
Side, `cmp_0822_side.jpg` (lower half; 1300x1790):
- Smooth flat patch between door bottom and sill clips, x 610-780, y 1425-1455: looks like surviving skirt skin.
- Flat tongue pointing at the front arch at sill height, x 790-975, y 1480-1515.
- Speckle fringe under the sill, x 170-330, y 1495-1510.
- Dark blob at the top of the door-trim opening, x 100-145, y 1185-1245.
- Fender opening: stair-stepped top edge x 800-1050, y 1200-1230; holes with loose fragments x 820-900, y 1290-1350.
- Flakes where the bumper corner met the arch, x 1210-1300, y 1215-1265.
- Upper half (assembled): door-trim and skirt tints interleave, x 130-330, y 395-520, and a skirt strip overlaps the
  door bottom, x 560-780, y 530-545: two scans own the same skin. Decide one owner per surface.
Rear, `off_0822_rear.png` (1300x900):
- Dark brown slot under the trunk lip with a wavy top edge and a diagonal sliver, x 365-640, y 315-335: an unfilled
  opening showing backfaces. Check the cut against the hatch shut line; fill from the state or keep the lid skin.
- Frayed edge under the car-left tail lamp, x 270-300, y 380-470; dotted lamp underside x 290-380, y 370-385.
- Dashed/stair-stepped strip at the car-right corner, x 960-1000, y 600-640; speckle x 860-940, y 670-685.
- Noisy mesh by the right exhaust tip, x 750-850, y 590-640, and on the left tip, x 275-340, y 570-610.
- Hanging sliver behind the rear arch, x 1020-1090, y 560-600.
Underbody, `under_car_low_1113.png`: nose voids x > 1280; arch voids; speckled pans x 560-700 (may be the splat).
Interior, `int_Interior_1113.png`: door-card strips y 60-110 and y 870-910; passenger dash holes x 1040-1150, y 470-640.

## 8. Open questions
1. Does the chassis scan include control arms / subframe links (risk 3)?
2. Is the Interior scan console-out (s13 gate)?
3. Front lower bar and rear trunk-lip slot: real structure or cut errors?
4. Which of lower skirt / upper skirt / door trim overlaps which (s11 order)?
5. Should the mirrored left corners stay on the car in wides?
