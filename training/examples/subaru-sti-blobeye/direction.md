# Direction v2: Subaru Impreza STI GD "blobeye" scan reel

Scene director plus stage-2 director, 2026-11-11. This file is the whole plan (scene order and the per-shot table). The editor implements it in `tools/shots.py` + `cues.json` + `project.yaml` and does not need to ask about anything except the **Open questions** at the end.

Inputs read: lessons.md (all), style-guide, references README (Temerario), clips.md, project.yaml, cues.json, editlog, director_report.md, tools/shots.py, contact sheets `chk/v3_sheet.jpg`, `fin_s5.jpg`, `fin_s7a.jpg`, `fin_s7b.jpg`, `ov2.jpg`, `bo.jpg`.

Frame conventions (shots.py): metres, nose −Y (nose at y ≈ −2.20, tail y ≈ +2.20), car's right = −X, car's left = +X, ground z = 0. `orbit()` angle 0 = in front, −90 = car's right, +90 = car's left, 180 = behind. Part offsets are `pk(u, loc, rot)` deltas from the seated pose.

## User rules applied (v2 notes 1-8 + addendum A-D; the addendum wins on conflicts)
- **Travel order:** rear → left side → front-left wheel → front (hood/engine bay → bumper). The camera never goes back to a region it has already left.
- **Sections appear once (B):** each section (rear/wing, side/skirt, wheel, engine bay, front bumper) is one continuous sequence. The whole car is only a bookend: opener and finale (note 7), from different angles and in different states.
- **Bumper-removed is the HERO (C):** the bumper clears to reveal the intercooler **on bar 16 (25.32 s)**, the brightest bar. It is also the longest section (5 bars, 7.9 s) and the only one with labels.
- **No faked openings (D):** the hood **lifts off** (translates). It does not hinge. No trunk, door or interior shots. All four removals have a registered "without" scan underneath. No part spins or flips, because none of the carved panels has a scanned inner face.
- **Progressive disassembly:** parts come off one per section, stay off, and park at fixed **park offsets** that every later shot uses (see table below). The finale shows the full exploded state from two new angles, then reassembles it, fades to black, and shows a small logo.
- **Text:** only the labels in the bumper section (C), with at most 2 on screen. No other text (note 8 still holds everywhere else).
- **Cropping (A):** in wide shots the whole car and every parked part stays inside the frame with at least 80 px margin. In detail shots the named section fills the frame.

## 1. Feature inventory

| Region | Scan data (registered) | Signature features | State / part | Weak data | Richness |
|---|---|---|---|---|---|
| Front, bumper zone | Full car 23M; **'bumper removed'** 1.8-2.1 mm: front-mount intercooler core (finned, fills the bumper opening width), intercooler piping (pipe running low from the core end round the corner, ov2 bottom-right), brackets/mounts behind the core; headlights stay on the car | blobeye headlights, bumper lip, fog openings | bumper_skin (outer surface only → translate, no flip) | grille openings are holes; fog-light openings dark | **5: hero** |
| Front, hood/engine bay | **'GD Scan Engine Bay'** p50 1.6 mm (engine, intake, piping) + **'hood removed'** (radiator support) | hood scoop | hood_skin (outer surface only → **lift off**, no hinge per D) | wiper/strut slivers at the cowl | 4 |
| Wheels | full car: spokes + calipers scanned | 5-spoke-pair wheels, calipers | none | none on wheels | 2 |
| Rear | **'Rear Wing data'** wing-off rear 1.7 mm (trunk lid with wing mount pads) | big STI wing | wing (no flip) | tail-light lens speckle; plate flattened (deplate) | 3 |
| Left side | **'Sideskirt removed'** 2.1 mm (bare sill), car's left only | side skirt | skirt (translate) | none | 2 |
| Right side / top / interior / trunk open / doors | none extra | none | none | none | 0: no dedicated scene |

## 2. Park offsets (state carried across shots)

| Part | Seated → park path (offsets in m) | Park offset | Why |
|---|---|---|---|
| WING | straight up | **(0, +0.10, +0.75)** | Rises into black above the trunk. It never crosses the body. |
| SKIRT | (+0.35, 0, +0.05) → park | **(+0.75, 0, +0.10)** | Moves out toward the left-side camera, low over the black ground, below the sill in frame. |
| HOOD | (0, 0, +0.30) → park, rot 0 | **(0, +0.25, +1.15)** | Lifts straight up off the opening, then back over the cowl. It stays clear of the windshield (z ≈ 1.0-1.4) by at least 0.7 m. |
| BUMPER | (0, −0.32, +0.03) → (0, −0.55, +0.06) → park | **(+1.55, −0.55, +0.10)** | Moves forward 0.32 m first, because the headlights stay on the car (v1 dog-leg). It then moves forward 0.55 m and out to the car's left (frame right in the S6 view), so it parks in front of the nose and outside the car's width. It stays clear of the piping, which is on the car's right. |

Base for every shot after the opener is `OPEN` (base_open.blend) plus each part either seated (`pk(0)`) or at its park offset. A part that is already off is keyed at its park offset for the whole shot. Never omit a removed part from a wide shot: it must be visible where it parked. Turn off persistent data for every animated shot (lesson). Render heavy shots in 40-frame processes and check every frame's luma before assembly.

## 3. Scene list, in order (scene director)

| # | Scene | Section | Scans used | Feature shown | Why here (inventory) | Bars / time |
|---|---|---|---|---|---|---|
| S1 | Opener | whole car (bookend) | full car (car4_dp) | whole car, STI wing, all parts on | The wing is the rear's signature, so a rear 3/4 opener starts the rear → front travel. It shows the whole car with motion from frame 1 (notes 4, 1). | 0-2 · 0.00-3.22 |
| S2 | Wing off | rear | OPEN + Rear Wing data fill, WING | wing, then the trunk lid's wing mount pads | Rear richness 3: one part plus its state. It shows the part, then what is under it. | 2-5 · 3.22-7.95 |
| S3 | Skirt off | left side | OPEN + Sideskirt removed fill, SKIRT | skirt, then the bare sill | One part, so a short 2-bar scene. Travelling forward along the side. | 5-7 · 7.95-11.11 |
| S4 | Front-left wheel | wheels | OPEN (+HOOD, BUMP seated) | spokes, caliper, disc | Scanned spokes and calipers. It is the bridge from the side to the front. | 7-8 · 11.11-12.69 |
| S5 | Hood lifts off → engine bay | engine bay | OPEN + hood removed + GD Scan Engine Bay, HOOD | hood scoop, then engine, intake and piping | Second richest. Starts on the bar-8 lift. Hood lifts on bar 9. Long held move. | 8-14 · 12.69-22.17 |
| S6 | **Front bumper removed (HERO)** | front bumper | OPEN + bumper removed, BUMP | bumper, then intercooler core and piping | Richest region and addendum C. The reveal lands on bar 16. Longest hold. Labels. | 14-19 · 22.17-30.06 |
| S7a | Exploded state, angle 1 | whole car (finale) | OPEN + all four parts parked | every removal at once (cumulative) | Note 7: the progressive explode seen from several angles. New angle: high left. | 19-20 · 30.06-31.64 |
| S7b | Exploded angle 2 → reassembly → fade | whole car (finale) | same | parts fly home and lock on bar 21, then the whole car | Note 7: reassembly, then fade to black. Kept short (note 7: "don't hold"). | 20-22 · 31.64-34.80 (fade 34.01-34.80) |
| Logo | small logo on black | none | logo png | none | Note 7: small logo. | 35.20-39.27 |

## 4. Per-shot table (stage-2 director)

Times are video seconds. "u" is the shot fraction for shots.py. Cut frames are round(t·30).

| Shot | Section | Start-end (frames) | Focus | Camera (prepped frame, m; focal mm) | Part action (beat times) | Why it earns its seconds | Render |
|---|---|---|---|---|---|---|---|
| **S1_open** | whole car | 0.00-3.22 (0-97) | whole car from the rear 3/4, wing against black | **Reuse v1 `s2_rear34`**: orbit 158°→136°, r 5.6→5.3, h 0.95→1.35, c (0, 0.55→0.45, 0.65), 30 mm. Whole car inside the frame with margin (v3_sheet frames 6-8). | all parts on | Hook: the whole car, moving from frame 1, with its signature wing. | **reuse** 48 fr (v1 slot was 3.1667 s, same) |
| **S2_wing** | rear | 3.22-7.95 (97-239), T 4.737 | wing, then the trunk-lid mount pads | u0 loc (0.70, 3.55, 1.85) → tgt (0.20, 2.00, 1.25), 40 mm. The wing fills the frame width. u .33 (bar 3) loc (0.62, 3.35, 1.95), same target. u1 loc (0.40, 3.00, 2.10) → tgt (0.10, 1.80, 1.00), 40 mm: tilted down onto the trunk lid and mount pads, so the trunk fills the frame. Tail light only at the frame edge (speckle). Plate out of frame. | WING: pk(0) to **u .333 (4.80, bar 3 lift)**; pk(.5 = 5.59, (0,+0.10,+0.40), out). Float/drift to pk(.667 = 6.38, (0,+0.10,+0.50), lin). Then pk(.833 = 7.17, park (0,+0.10,+0.75), inout) and out the top of frame. HOOD, BUMP, SKIRT seated. | One bar on the intact wing ("show the part"). It lifts on the brightness lift. The camera moves in on what was under it. The wing leaves before the cut ("moves on"). | new 73 fr @15 (OPEN 4 mm) |
| **S3_skirt** | left side | 7.95-11.11 (239-333), T 3.158 | side skirt, then the bare sill | u0 loc (2.30, 1.70, 1.55) → tgt (0.95, 0.10, 0.20), 35 mm: high rear-left looking down and forward along the sill. The skirt fills the frame diagonally. u1 loc (2.00, 0.50, 1.25) → tgt (0.95, −0.70, 0.22), 35 mm: travels forward toward the front wheel. | SKIRT: pk(0) to u .125 (8.35); pk(.25 = 8.74, (+0.35,0,+0.05), in2) to clear the sill lip; pk(.5 = 9.53, park (+0.75,0,+0.10), out). It drops below the frame as the camera tracks forward. WING parked (out of frame above). HOOD, BUMP seated. | One part and one state, so 2 bars. The camera tracks forward, which sets up the next shot. | new 49 fr @15 |
| **S4_wheel** | wheels | 11.11-12.69 (333-381), T 1.579 | front-left wheel: spokes, caliper, disc | u0 loc (1.60, −2.60, 0.45) → tgt (0.85, −1.25, 0.36), 40 mm. u1 loc (2.00, −1.95, 0.40) → tgt (0.82, −1.25, 0.36), 40 mm. A slow arc from the front-left. The wheel fills the frame. The parked skirt may show softly in the background behind the tyre; that is correct state. | SKIRT, WING parked. HOOD, BUMP seated. | Wheels with scanned spokes and calipers are a signature feature. Arriving at the front. | new 26 fr @15 (4 mm OPEN; see Q2) |
| **S5_hood** | engine bay | 12.69-22.17 (381-665), T 9.474 | hood scoop, then the engine bay (radiator support, engine, intake, piping) | u0 loc (−1.05, −4.30, 2.10) → tgt (0, −1.55, 0.95), 35 mm: high front-right. The hood and scoop fill the frame. u .167 (bar 9) loc (−0.85, −3.95, 2.08), same target. u .333 (bar 10) loc (−0.70, −3.55, 2.00) → tgt (0, −1.40, 0.80). u .667 (bar 12) loc (−0.35, −2.85, 1.75) → tgt (0, −1.30, 0.68): over the radiator support. u1 (bar 14) loc (+0.20, −2.45, 1.55) → tgt (0, −1.05, 0.60), 32 mm: a glide across the intake/engine toward the cowl. The engine bay fills the frame. | HOOD (translate only, **no hinge**): pk(0) to **u .167 (14.27, bar 9)**; pk(.25 = 15.06, (0,0,+0.30), out), straight up off the opening; pk(.333 = 15.85, park (0,+0.25,+1.15), inout), up and back. It exits the top of frame as the camera tilts down. WING, SKIRT parked. BUMP seated. | One bar showing the intact hood and scoop, the lift-off, then a long held descent into the engine bay. Every second shows new engine-bay geometry (Temerario "long held move"). | new 116 fr **@12 fps** (slow move; src_fps from 12) |
| **S6_bumper** HERO | front bumper | 22.17-30.06 (665-902), T 7.895 | bumper, then **front-mount intercooler core**, then **intercooler piping** | u0 loc (1.20, −4.70, 0.55) → tgt (0.05, −2.10, 0.48), 35 mm: low front-left. The bumper fills the frame width, with headlights at the top edge. u .2 (bar 15) loc (1.05, −4.45, 0.55). u .4 (bar 16) loc (0.70, −4.00, 0.55) → tgt (0, −2.05, 0.45). u .6 (bar 17) loc (0.30, −3.25, 0.55) → tgt (0, −2.00, 0.42), 38 mm: the core fills the frame width. u .8 (bar 18) loc (−0.20, −3.15, 0.50) → tgt (−0.30, −1.98, 0.38). u1 (bar 19) loc (−0.60, −3.05, 0.42) → tgt (−0.62, −1.95, 0.30), 38 mm: slides to the piping at the core's end (car's right; confirm, Q3). The car sits in the upper ~70 % of the frame, with black ground below for the labels. | BUMP: pk(0) to **u .2 (23.74, bar 15)**; pk(.3 = 24.53, (0,−0.32,+0.03), in2) to clear the headlights; pk(.35 = 24.93, (0,−0.55,+0.06), lin); pk(**.4 = 25.32, bar 16**, park (+1.55,−0.55,+0.10), out). It exits frame right; the core is fully clear exactly on bar 16. HOOD, WING, SKIRT parked (hood is above the frame). | Hero (C): the reveal lands on the brightest bar. 3 bars of hold and move-in let the viewer read the core, then the piping. Labels name what is visible. | new 121 fr @15 (bumper-removed scan close-up) |
| **S7a_explode** | whole car | 30.06-31.64 (902-949), T 1.579 | the whole exploded car: wing, hood and bumper floating; skirt on the ground; trunk, sill, engine bay and intercooler all exposed | orbit u0 (r 6.2, ang 118°, h 3.80, c (0.25, 0.10, 0.95)) → u1 (r 6.0, ang 95°, h 3.60, c (0.25, 0.0, 0.95)), 30 mm: high left side. **The whole car and all parked parts are inside the frame with ≥ 80 px margin** (check the preview; if anything clips, raise r in 0.2 m steps, never crop). | All four parts parked with a slow common drift of +0.04 m z (lin) so nothing is dead. | Note 7: the progressive explode from a new angle. It is the only frame that shows all states at once. | new 26 fr @15 |
| **S7b_reassemble** | whole car | 31.64-34.80 (949-1044), T 3.158 | parts fly home and lock; then the whole car | orbit u0 (r 6.0, ang 42°, h 1.70, c (0.30, −0.35, 0.80)) → u1 (r 5.6, ang 28°, h 1.35, c (0, −0.25, 0.65)), 30 mm: front-left at mid height, a different height and side from S5/S6. Whole car with margins. | Reverse order, 2.5-beat flights (0.987 s, ease in) staggered half a beat. HOOD 31.64→32.63 (u 0→.313) straight down. BUMP 31.84→32.82, back via (0,−0.55,+0.06) then (0,−0.32,+0.03) then home. SKIRT 32.03→33.02, via (+0.35,0,+0.05). WING 32.23→**33.22 (bar 21, last lock, u .5)**. Assembled car with the camera still moving through 34.01; **fade to black 34.01→34.80** (2 beats, on the moving frames). | Reassembly is the payoff. The assembled car is held for only 1.2 s before the fade (note 7: don't hold). | new 49 fr @15 |
| **Logo** | none | black 34.80-35.20; logo fades in 35.20-35.59, holds through the final hit 37.95, fades out 38.97-39.27 (1056-1178) | Illumaesthetic logo, **small**: 280 px wide (26 % of 1080), centred | none | none | Note 7: small logo on black. | existing png |

**Video ends at 39.27 s (frame 1178).** That keeps the total length, the bar-line cuts and the silence point.

### S6 labels (the only text in the reel)
Use the house HUD style (the Remotion `ScanHUD` text layer): white #F2F2F2, about 40 px caps, letter-spacing 0.12 em, no box, no lines or arrows. Each label fades in and out over 0.20 s. Position: left-aligned at **x = 80 px**, in the black band below the car (the S6 camera keeps the car in the top ~70 %). Nothing goes inside 80 px of any frame edge, over the car silhouette, or in the bottom 20 % caption zone (y > 1536).

| Label | Text | In → out (s) | Frames | Position (top-left of text box) |
|---|---|---|---|---|
| L1 | `FRONT BUMPER REMOVED` | 25.32 → 29.66 | 760 → 890 | x 80, y 1330 |
| L2a | `FRONT-MOUNT INTERCOOLER` | 25.72 → 27.90 | 772 → 837 | x 80, y 1400 |
| L2b | `INTERCOOLER PIPING` | 28.48 → 29.66 | 854 → 890 | x 80, y 1400 |

There are never more than 2 labels on screen. All labels are out before the 30.06 cut. Before assembling, the editor checks frames 760, 800, 860 and 885: if a label touches the car, move the S6 target down by 0.05 m so the car rises in the frame. Do not move the text onto the car. The text is factual and has no numbers. Both components are visible in `ov2.jpg` (bottom-right) and `bo.jpg`. "Crash structure" is not labelled because its outline is not clear in the state scan.

## 5. Music map (152 BPM, beat 0.39473 s, bar b = 0.06 + 1.57892·b)

| Bar | t (s) | Frame | Musical event | Picture |
|---|---|---|---|---|
| 0 | 0.00 | 0 | start | S1 opener (moving) |
| 2 | 3.22 | 97 | none | cut → S2 wing |
| 3 | 4.80 | 144 | **lift 1** | wing lifts off |
| 5 | 7.95 | 239 | none | cut → S3 skirt |
| 7 | 11.11 | 333 | none | cut → S4 wheel |
| 8 | 12.69 | 381 | **lift 2** | cut → S5: arrive at the front, hood and scoop |
| 9 | 14.27 | 428 | none | hood lifts off |
| 14 | 22.17 | 665 | none | cut → S6 bumper intact |
| 15 | 23.74 | 712 | none | bumper starts out |
| 16 | 25.32 | 760 | **brightest bar** | **intercooler fully revealed + L1** |
| 19 | 30.06 | 902 | none | cut → S7a exploded, high left |
| 20 | 31.64 | 949 | none | cut → S7b; reassembly starts |
| 21 | 33.22 | 997 | none | last part locks (wing) |
| 22 | 34.80 | 1044 | none | black (fade 34.01-34.80) |
| 24 | 37.95 | 1139 | final hit | logo holding |
| none | 39.27 | 1178 | silent | end |

Assembly: whole-frame `dur`s, first clip one frame short. Use the `src_fps = (N−1)/(dur + 3 frames)` rule (v1 editlog), and set S5's rate from its 12 fps source. Measure the cuts on the delivered file.

## 6. Cut list vs v1

| v1 shot | Fate | Why |
|---|---|---|
| s1_front34 | **dropped** | The opener moves to the rear so the reel travels one way (note 1). The director report flagged it as repeating s2 (IoU 0.76). |
| s2_rear34 | **kept as S1 opener** (timing unchanged, now from t = 0) | Whole car, motion from frame 1, wing. Rendered from car4_dp (plate flattened). |
| s3_wheel (front-right) | **dropped**, replaced by new S4 front-left | The right side is off the travel path. Its bumper is on, which would break continuity after removal if placed later. |
| s4_light (headlight → scoop crane) | **dropped** | Right side, so off the path. It repeated s5 and s8 (report). The scoop is now in S5 and the headlights in S6. |
| s8_wing | **dropped**, merged into S2 | Same subject as the wing removal; one section, one sequence (B). |
| s5_hood | **dropped**, re-rendered as S5 | It hinged the closed hood open, which addendum D forbids. Its base also had wing, skirt and bumper on (continuity). |
| s6_top | **dropped** | A rotating top-down that shows nothing new (note 3). |
| s7_explode | **dropped**, replaced by S2/S3/S5/S6 (progressive) + S7a/S7b | All parts separated at once in one wide orbit (note 2), with 4.3 s dead. |
| logo 34.80-39.27 (big) | **changed** | Small 280 px logo after a fade to black, from 35.20. |

## 7. Hold list (> 0.75 s without a new subject)

| Where | Length | Reason |
|---|---|---|
| S2 wing floating 5.59-6.38 | 0.79 s | Shows the part off while the camera moves in on the mount pads (C/note 2). The wing drifts and is not static. |
| S5 intact hood 12.69-14.27 | 1.58 s | The camera is moving in on the scoop (signature). This is the only scoop shot in the reel. |
| S5 bay glide 18.48-22.17 | 3.7 s | Constant camera motion over new engine-bay geometry. Every frame shows new components. |
| **S6 core + piping 25.32-30.06** | 4.74 s | The hero hold (C): time to read 2 labels. The camera keeps pushing, then slides to the piping. |
| S7b assembled car 33.22-34.01 (+ fade to 34.80) | 0.79 s (+0.79 fade) | The reassembled car is the payoff. It is kept short (note 7). |
| Black 34.80-35.20 | 0.40 s | Breath before the logo. |
| Logo 35.20-39.27 | 4.07 s | Covers the final hit and the music tail to silence. A small logo, like Temerario (~5 s). |

## 8. Render budget

| Shot | Seconds | fps | Frames | Est. s/frame | Est. time |
|---|---|---|---|---|---|
| S1 (reuse s2_rear34) | 3.22 | none | 0 | none | 0 |
| S2_wing | 4.74 | 15 | 73 | 15 | 18 min |
| S3_skirt | 3.16 | 15 | 49 | 14 | 11 min |
| S4_wheel | 1.58 | 15 | 26 | 30 | 13 min |
| S5_hood | 9.47 | **12** | 116 | 20 | 39 min |
| S6_bumper | 7.89 | 15 | 121 | 20 | 40 min |
| S7a_explode | 1.58 | 15 | 26 | 15 | 7 min |
| S7b_reassemble | 3.16 | 15 | 49 | 15 | 12 min |
| **Total new** | | | **460** | | **≈ 2.3 h** |

This is about 2 % over the ~450 guideline. If it must come in under 450, render S3 at 12 fps (−10 frames). Do not cut S6. Render one shot at a time in the background. Run 30 % previews (first/mid/last) of S6, S7a and S7b first to check margins and label space before the finals.

## 9. Open questions for the editor (do not guess)
1. **Inner faces:** do wing.blend, skirt.blend or hood_skin.blend have any scanned underside? This plan assumes none, so nothing flips (note 5). If the wing underside is scanned, S2 may tip it 20° toward the camera at u .5. Confirm by rendering it from below first.
2. **Close-up resolution:** S4 (wheel) and S6 (core) are close-ups on `OPEN`. Is base_open 4 mm? If spokes or fins look soft on the preview, build a 2 mm front crop of base_open with the same carve and fills (`tools/fill.py`), using `--like` (never re-normalise).
3. **Piping side:** ov2 bottom-right appears to show the pipe on the car's right (−X), running from the core end. Confirm on an S6 preview frame. If it is on the left, mirror the S6 u .8-1 camera to +X and move the bumper park to (−1.55, −0.55, +0.10).
4. **Seam between fills:** S5 ends low over the radiator support, where 'hood removed' and 'GD Scan Engine Bay' meet. Check the S5 preview for a step or duplicate surface; if there is one, end the glide 0.2 m higher.
5. **Opener vs finale:** both are whole-car bookends (allowed by note 7). If the reviewer reads S7a as "car twice", shorten S7a to half a bar, but keep S7b.
