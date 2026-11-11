# Porsche Macan (Electric) - scene direction (v1 -> v2)

Scene director, 2026-11-11. Rules applied, newest first:
- **Coordinator addendum A-D:**
  - framing: whole car with margins in wides; the named section fills the frame in details;
  - each section in ONE continuous sequence;
  - **bumper-removed is the hero beat**, with short factual labels;
  - only states that were scanned.
- **User v2 rules:**
  - travel FRONT -> SIDE -> REAR with no ping-pong;
  - focus on sections, with a progressive per-section explode and no all-at-once wide orbit;
  - no wasted rotations or repeats;
  - the opener shows the WHOLE car;
  - spin a part only to show a scanned back;
  - never imply missing data;
  - a short ending: reassembly, fade, SMALL logo;
  - cuts on kicks; never reuse a shot.
- **User rule:** "shot order comes from the car's scan features" (subaru-wrx-va); all of `knowledge/lessons.md`.
- **Brief:** scan only (no IRL), satin silver on black, 1080x1920, ends on the ILLUMAESTHETIC logo cut to the music.
  The brief's "no text" is **overridden by addendum C**, so labels are allowed over scan shots only. Every shot here is a scan shot.

Checked:
- project files: `clips.md`, `editlog.jsonl`, `project.yaml`, `timing.json`, `tools/shots.py`, `tools/build.py`, `tools/shot.py`. There is no `feedback.jsonl` (v1 has no reviewer notes yet).
- Contact sheets I made with PIL:
  - finals `s3_wheel` (40 frames), `s4_lightbar` (40), `s5_open` (82), `s7_top` (65 of ~67; rendering);
  - previews `s1_front_v2/v3`, `s2_rear_v2/v3`, `s5_open`, `s7_top`, `s8_explode`.
- Coordinator sheets: `chk/explode_base.jpg`, `chk/explode_pose.jpg`, `chk/hatchchk.jpg`, `chk/s12v3.jpg`, `chk/behind_bumpers.jpg`.

The `s8_explode`, `s1_front` and `s2_rear` finals don't exist yet. `python -m ive director` therefore fails on the missing `final/s1_front`, so this plan is built from the sheets.

## Step 1 - feature inventory

| Scan / data | What it shows (looked at) | Registered? | Role |
|---|---|---|---|
| Macan Full Car (car4 4 mm / car3 3 mm) | whole car, clean skin; rear plate blanked to a slab; tyre bottoms ragged | base | wides, details |
| **Front Bumper (Warped)** + **Front Bumper Off** | bumper skin. Behind it (behind_bumpers frames 1-2): a **horizontal crash beam across the nose**, the cooling module and air ducts behind it, a wiring harness, brackets, and the lower air-guide lattice | 4.4 mm (covers the bumper, no offset) / 2.0 mm | **HERO: front bumper removed** |
| **Rear Bumper (Warped)** + **Rear Bumper Removed** | bumper skin (speckly up close). Behind it (frames 3-4): a **tubular crash beam on end mounts**, the blank plate on its bracket, lower structure | 2.7 / 4.1 mm | **HERO: rear bumper removed** |
| Hood + Hood Removed + Doors and Hood Open | hood panel; a dense, real bay under it (s5_open frames 12-33) | 2.4 / 1.8 / 1.2 mm; hinge -54.9 deg fitted to the captured open hood (2.2 mm) | **engine bay**: hood opens on its real hinge |
| Fender (car's left) + Fenders Removed (x>0) | left front fender; arch/strut structure under it (explode_base frame 1) | 1.7 / 2.0 mm | **side** (left, front end): fender off |
| 4 doors + Doors and Hood Open | door cards = scanned inner face (FL also has a full outer skin; FR/RL/RR skins rebuilt from the car's skin); cabin, seats and B-pillar through the openings (explode_base frame 3) | FL 1.4, FR 2.0 mm; RL/RR cards inside the outline | **side**: left doors off, cards turned to the lens |
| Rear Hatch (extracted) + Rear Hatch Fully Open | hatch lid; boot interior (s5_open frames 66-82) | 1.3 / 1.4 mm; hinge +69.8 deg (3.7 mm) | **rear**: hatch opens on its real hinge |
| Front-right wheel/brake (car3) | 3 mm spokes; caliper and disc through the spokes (s3 final) | car | **wheels** |
| Front face (car3) | lamps in the body, intakes, crest (s1 v3 preview: clean at distance) | car | **front** exterior detail (lenses not yet checked up close) |
| Rear light bar, PORSCHE lettering, Macan script (car3) | the signature exterior feature (s4 final: crisp, plate out of frame) | car | **rear** exterior detail |
| Headlights / Tail Lights (parts), Interior Doors Open | strand, mostly inside the body / 12 % overlap | not usable | not used |
| Top / roof | no state, no part (v1 s7: roof + door slivers) | - | **no section** |

Weak data:
- The rear plate is a slab: keep it small, or below the frame.
- The warped rear bumper is speckly: no close-up on it and no tip; it leaves the frame.
- The tyre bottoms are ragged: cameras stay at h >= 0.7 m, and no frame edge sits on a contact patch.
- The lamp parts and Interior Doors Open are not used.

Region scores:

| Region | Parts | States | Hinge | Signature | Quality | Score |
|---|---|---|---|---|---|---|
| **Front** | 2 (hood, front bumper) | 3 (Hood Removed, Doors and Hood Open, Front Bumper Off) | 1 | face + wheel | good | **richest** -> drop |
| **Rear** | 2 (hatch, rear bumper) | 2 (Fully Open, Rear Bumper Removed) | 1 | **light bar** | plate slab, speckle | second |
| **Side (left)** | 3 (fender, FL, RL doors) | 2 (Fenders Removed, Doors and Hood Open) | 0 | - | skins rebuilt | third |
| Wheels | 0 | 0 | 0 | 3 mm spokes | ragged tyre bottoms | 1 short shot |
| Top / interior | 0 | 0 | 0 | - | - | none |

## Step 2 - scene order (one pass: front -> side -> rear; every section once)

| # | shot | section (addendum B) | scans | feature shown | why here | music | frame |
|---|---|---|---|---|---|---|---|
| 1 | O_whole | whole car (front 3/4) | car4 | the whole car with margins | opener on the end with the most data; whole car per rule 4 | 0-4.109 (8 beats) | wide |
| 2 | N_face | front exterior | car3 | lamp, intakes, crest (bumper still on) | front detail next to its wide; shows the bumper before it comes off | 4.109-8.176 (8) | detail |
| 3 | W_wheel | wheels | car3 | front-right wheel and brake | front corner, reached by sliding off the face to the right | 8.176-9.701 (3) | detail (reuse s3) |
| 4 | F1_bay | engine bay | comp_open + hood | hood opens on its fitted hinge; push into the real bay | the front's first state; one continuous move over the hit-less build | 9.701-16.310 (13) | front-half wide -> detail |
| 5 | **F2_fbumper** | **front bumper removed (HERO)** | comp_explode + parts | bumper lifts off and flips its inner face to the lens; camera moves in on the crash beam, ducts, harness and brackets and holds | richest region on the **DROP**; addendum C | 16.310-20.377 (8) | 3/4 -> straight-on detail |
| 6 | S1_side | side (left) | comp_explode + parts | fender off (arch structure), then FL, then RL door off, cards turned to the lens; cabin through the openings | side after the front, trucking front -> rear; 3 parts on 3 kicks | 20.377-24.440 (8) | detail track |
| 7 | L_lightbar | rear exterior | car3 | light bar, PORSCHE, Macan script | rear detail before the rear opens (the signature) | 24.440-25.459 (2) | detail (reuse s4, trimmed) |
| 8 | **R1_rbumper** | **rear bumper removed (HERO)** + boot | comp_explode + parts | hatch opens on its hinge (boot); bumper slides back and down out of frame; camera moves in on the tubular crash beam and its end mounts and holds | rear states; addendum C | 25.459-28.511 (6) | 3/4 -> detail |
| 9 | X_reassemble | whole car (reassembly) | comp_explode -> car4 | every part flies home and locks; the clean car; fade out | the only shot where all parts are in view at once, and only on the way home; high near top-down from the nose (an angle not used elsewhere) | 28.511-30.544 (4) | wide |
| 10 | logo | - | logo_card | small ILLUMAESTHETIC logo | the pad tail | 30.544-33.600 | ~320 px wide |

**Section continuity (B):**

Sections in order: whole -> front exterior -> wheels -> engine bay -> front bumper removed -> side -> rear exterior -> rear bumper removed (incl. boot) -> whole (reassembly).
- Each appears once.
- The bumper-removed sections are separate sections, as addendum C asks.
- The front exterior (N) shows the bumper on. Its removal comes 1.5 sections later, after the wheel and the bay that sit between them physically.
- The two "whole" shots are the opener (low front-right 3/4, closed car) and the reassembly (57 deg down from the nose, parts flying home). They show different subjects and are never the same view.

**Not cast:**
- **v1 s7 top-down spin:** a rotation; the roof has no data.
- **v1 s2 rear 3/4 turntable:** a second closed-car wide, and the rear would come before the front.
- **v1 s5_open:** opened the front and then the rear in one side-on orbit, and cropped the car side-on mid-shot.
- **v1 s8:** every part out at once in a wide orbit, cropped side-on.
- **Right doors and right fender:** no right fender part exists, and the right doors stay shut. No camera looks at the right side after the explode starts.
- **Interior:** no registered interior scan.

## Labels (addendum C; plain, factual, from the scan files)

Remotion `ScanHUD`, `label` items only, no numbers:
- one label on screen at a time;
- enters on a kick and leaves at least 0.1 s before the cut;
- top third, 80 px inside the edges, outside the car silhouette;
- above the bottom 20 % caption zone.

| text | shot | in -> out (s, reel time) | backed by |
|---|---|---|---|
| FRONT BUMPER REMOVED | F2 | 17.327 -> 18.800 | "Front Bumper Off" state scan (2.0 mm) + the warped bumper part |
| CRASH BEAM | F2 | 18.851 -> 20.250 | horizontal beam visible in comp_explode (chk/behind_bumpers frames 1-2) |
| REAR BUMPER REMOVED | R1 | 26.477 -> 27.430 | "Rear Bumper Removed" state scan (4.1 mm) |
| MOUNTING POINTS | R1 | 27.494 -> 28.400 | the tubular beam's end mounts, visible in behind_bumpers frames 3-4; the shot ends framed on them |

## Music map (kick grid t = 16.3099 + 0.50836 n; cuts on round(t*30))

| Cut | Time (s) | Frame | Note |
|---|---|---|---|
| | 0 | 0 | fade up 1.2 s |
| v1 | 4.109 | 123 | |
| v1 | 8.176 | 245 | |
| v1 | 9.701 | 291 | |
| v1 | **16.310** | **489** | **drop** |
| v1 | 20.377 | 611 | |
| measured accent | 24.440 | 733 | n=16 |
| kick | 25.460 | 764 | n=18 |
| phrase | 28.511 | 855 | n=24 |
| v1 | 30.544 | 916 | the groove stops |
| end | 33.600 | 1008 | |

In-shot hits:
- 11.226: the hood starts to open (the v1 cut becomes a motion hit, so there is no cut in the build).
- 17.327: the front bumper is clear.
- 21.393: FL door.
- 22.41: RL door.
- 25.969: the rear bumper starts to move.
- 26.99: the rear bumper is clear.
- 29.527: the lock.

The v1 cut at 11.226 is dropped. The 25.460 cut is a grid kick, not a measured accent; see question 4.

## Diff vs the v1 timeline

| v1 | v2 | change |
|---|---|---|
| s1_front 0-4.109 (final queued, not rendered) | O_whole 0-4.109 | **re-spec**: wider, whole car with margins (the v1 framing crops the car) |
| s2_rear 4.109-8.176 (queued) | - | **dropped**; **stop the queued final** |
| s3_wheel 8.176-9.701 | W_wheel, same slot | **reuse as-is** |
| s4_lightbar 9.701-11.226 | L_lightbar 24.440-25.459 | **reuse, moved and trimmed** to 1.033 s (`in` 0.95 s) |
| s5_open 11.226-16.310 | F1_bay / R1_rbumper | **dropped**: hood and hatch open in their own sections; it cropped the car side-on |
| s7_top 16.310-20.377 | F2_fbumper | **dropped** (rotating top-down) |
| s8_explode 20.377-30.544 (queued) | S1_side, L, R1, X | **dropped**: all parts at once in a wide orbit, cropped; **stop the queued final** |
| - | N_face 4.109-8.176 | **new** |
| logo, 860 px | logo, ~320 px | re-run `tools/logo_card.py --width 320 --secs 3.0667` (ffmpeg only) |
| no overlays | 4 labels | Remotion ScanHUD |

Reused unchanged: s3_wheel; s4_lightbar (trimmed).

New Blender renders: O_whole, N_face, F1_bay, F2_fbumper, S1_side, R1_rbumper, X_reassemble. That is 459 frames, about 2.6 h at 20 s/frame; the budget is in director.md.

Wasted if the queue isn't stopped: s8 (159 frames), s1 at its old framing (73), s2 (67), about 1.7 h. The s5_open and s7_top renders are finished but unused.

## Open questions for the editor (check; don't guess)

1. **Front bumper inner face.**
   - Render `x_fbumper` alone from behind (one still). If the inside is scanned, F2 flips it (-160 deg about X) so the inside faces the lens.
   - If it is empty, keep it unrotated and only lift it above the nose.
2. **Fender inside.** It is translate-only as planned. If the inside is scanned, a 90 deg tip about Y is allowed.
3. **N_face: are the lamp lenses scan holes?** (Ferrari lesson.)
   - Check the preview's first/mid/last frames.
   - If there are dark blotches, aim lower at the intakes and the crest.
   - Check for a front plate and deplate if one exists.
4. **Kick at 25.460 (n=18).**
   - Check its kick strength. If it is weak, cut L/R1 at 25.969 (n=19).
   - Then R1 becomes 2.54 s: the hatch opens 0-0.5 and the bumper moves on 26.477.
   - Move the labels one kick later: REAR BUMPER REMOVED 26.99-27.9, MOUNTING POINTS 27.99-28.40.
5. **Seams.** Look at one full-res still of comp_explode with every part at home (F2 frame 1).
   - If a seam shows, build a subset base with `tools/build.py`: hood + front bumper off.

## v3 (scene director, 2026-11-11)

User feedback on v2 (feedback.jsonl): "Hide/Blur/remove the rear plate, show the interior and exploded views".
- Plate: done (editlog 18:58; deplated meshes, plate carried with the rear bumper part).
- Interior and exploded view: this section.

Music is fixed (33.6 s, kick grid t = 16.3099 + 0.50836 n). Every cut and part event below sits on that grid or on an intro hit.

Looked at:
- `chk/fc_{O_whole,N_face,F1_bay,S1_side,R1_rbumper,X_reassemble}.jpg`
- `reg/interior/sheet.jpg`: no-seats shell plus 5 seat parts and the dash, in colour.
- `reg/interior_in_car/sheet.jpg`: the shell inside the car.

### Inventory additions (v3)

| Scan | What it shows (looked at) | Registered? | Role |
|---|---|---|---|
| Interior No Seats | cabin shell without a roof: floor, door-opening frames, dash/console. It fills the four door openings exactly (interior_in_car frames 1-2). | yes (in car frame) | **cabin base** for S1/R1/X. It replaces the old cabin fill from Doors and Hood Open, which has seats baked in and would give **double seats**. |
| Interior with Seats | the same shell with the seats in | yes | registration reference only. The "seats in" look = the No Seats shell + seat parts at rest. |
| Driver Seat (red in reg frame 2) | full seat part. It is the seat nearest the left-side camera, so it sits on the car's left (+X), which is the camera side in S1. | sits correctly | **S1**: out through the FL opening. **X**: apart. |
| Pass Seat (cyan) | full seat part, car's right (-X, far side) | sits correctly | **X only** (see below) |
| Rear Bench Bottom / Two Thirds Top / Third Top (green / yellow / magenta) | cushion plus split backrests | each sits correctly | **S1**: out as ONE group through the RL opening. **X**: the three pieces separate. |
| Dash Separate | dash; registers loosely (9-11 mm); it protrudes in reg frames 1/3 | loose | **not used** (the No Seats shell already carries the dash area) |

Region scores after the interior data:
- **Side (left)** goes from third to second: 3 exterior parts, plus 2 interior part groups, plus the no-seats state.
- Front is still the richest, so the drop stays on F2.
- Interior has no exterior signature, so it rides inside the side section (it is reached through the side openings). That keeps the side to one continuous sequence (rule B).

### Critique of the proposal and the changes made

1. **S1 event order would ping-pong.**
   - Proposed: fender, FL door, RL door, then driver seat, then bench. The v2 truck reaches the rear door by 22.41, so the camera would have to come back to the front opening for the driver seat at 23.427.
   - **Changed to strict front -> rear:** fender 20.377, FL door 21.394, **driver seat 22.41**, RL door 23.427, **rear bench 24.44**.
   - Each opening empties right after its door comes off, and the camera trucks one way only.
2. **The parked doors block the openings.**
   - In v2 the doors park 1 m straight out from their openings (x +1.0), right in the seats' exit path and between the lens and the cabin.
   - **Changed:** each door goes out and **up**, parking above and slightly outboard of its own opening, card turned and tilted to the lens. This is the "stack panels above the car in 9:16" lesson.
   - The seat then slides out beneath it. The door's top edge must keep a margin inside the frame on the first, middle and last frame.
3. **No push "into" the cabin.**
   - The car keeps its roof, so pushing through the opening fills the lens with B-pillar and roof edge (lesson: cabin / over-the-roof views are a trap).
   - **Changed:** the camera eases from about 3.4 m to about 2.6 m off the side and drops to about 1.1 m over the last 2 s. It ends square to the RL opening, holding the **empty rear floor** through the opening with the bench parked outside it, both fully in frame.
4. **The bench moves as one group in S1, not three pieces.**
   - There is one kick left for it, and three pieces through one opening crowd it.
   - The split into cushion, 2/3 back and 1/3 back is saved for X, so X shows something S1 didn't.
5. **R1 cannot reuse the old cabin.**
   - R1's camera sees through the open hatch into the cabin, and the bench is in place in the v2 base. After S1 removed it, that is a continuity error.
   - R1's camera is rear-left, so the parked left doors, driver seat and bench can enter the frame-left edge.
   - **R1 must be rendered on the v3 base** (No Seats shell, with driver seat and bench in their S1 end poses), moves unchanged. If the plate-only R1 re-render already ran on the old base, it is superseded.
   - Also re-check the open hatch clipping the top edge in the push-in (fc_R1 tiles 11-13). It is acceptable only if the frame reads as a beam detail; if not, lower the end target 0.1 m.
6. **X lock stays at 30.544, as proposed.**
   - The parts land as the groove stops, so the stop-time works as the punctuation.
   - Apart and orbiting 28.511-29.527 (2 kicks to read the full exploded view), flying home 29.527-30.544, clean car plus fade 30.544-31.56.
   - The fallback, if the lock reads late against the music, is to lock on the last kick 30.035 and hold 1.5 s.
7. **Agreed:**
   - s4_lightbar dropped. The light bar still shows on R1's opening frames, and s4 was the most "v1" moment.
   - O/N/s3/F1/F2 unchanged.
   - A small logo of 2.03 s.

**Passenger seat:** **X only.**
- In S1 the right doors are shut, and the seat is on the far side behind the body. Sliding it out would mean passing through a closed door (rule D) or across the cabin out the left opening (not how it comes out, and crowded).
- Leaving it in place in S1 is honest: it stays visible through the FL opening once the driver seat is out.
- In X the FR/RR doors (scanned parts, FR 2.0 mm) come off to -X and the passenger seat parks between them and the body, so it comes out through its own opening.

**Label on the interior beat:** one label.
- Title **INTERIOR**, sub `" "` (ScanHUD crashes on an empty sub).
- In at 24.44 (bench kick), out at 25.36 (0.92 s, the same length as the R1 labels).
- Place it in the black band below the sill (not the top band, where the parked doors sit). Check 4 samples across the window.
- Backed by the Interior No Seats / Interior with Seats file names.
- Not "SEATS REMOVED": the passenger seat is still in during S1.
- No other names (rails, mounts) unless a still of the No Seats floor shows them.
- No labels in X.

### v3 scene list (cuts on frames round(t*30))

| # | shot | section | reel time (frames) | dur | events (beat) | camera holds on | render |
|---|---|---|---|---|---|---|---|
| 1 | O_whole | whole | 0-4.109 (0-123) | 4.0667 | fade up 1.2 s | the whole closed car, front-right 3/4, linear arc | **reuse** |
| 2 | N_face | front ext. | 4.109-8.176 (123-245) | 4.0667 | - | lamps, intakes, crest (bumper on) | **reuse** |
| 3 | s3_wheel | wheels | 8.176-9.701 (245-291) | 1.5333 | - | front-right wheel and brake | **reuse** |
| 4 | F1_bay | engine bay | 9.701-16.310 (291-489) | 6.6 | hood opens 11.226 (hit) | the open bay | **reuse** |
| 5 | F2_fbumper | **front bumper removed** | 16.310 DROP-20.377 (489-611) | 4.0667 | bumper clear and flipped 17.327 | crash beam, ducts, harness | **reuse** (labels as v2) |
| 6 | **S1 v3** | **side (left) + interior** | 20.377-25.460 (611-764) | 5.1 | fender 20.377 (n8); FL door out+up 21.394 (n10); **driver seat** slides out +X through the FL opening 22.41 (n12), yaw about 35-45 deg toward the lens so the cushion and back read (full part, every side scanned); RL door out+up 23.427 (n14); **rear bench (3 pieces, one group)** slides out +X through the RL opening 24.44 (n16), translate only (wide part: a yaw sweeps into the C-pillar), clear by 24.95 | truck front -> rear, easing from 3.4 to about 2.6 m off and down to h about 1.1. Ends square to the RL opening on the empty rear floor plus the bench outside it. Passenger seat visible, still in place, through the FL opening. | **new**: base comp_explode with the cabin box cut and int_noseats in; parts: fender, 4 doors, 5 seat parts, hood (open), fbumper (parked z 4.5), hatch, rbumper |
| 7 | R1_rbumper | **rear bumper removed** + boot | 25.460-28.511 (764-855) | 3.0333 | hatch open by 25.969 (n19); bumper clear 26.99 (n21) | crash beam and end mounts; cabin through the hatch now without the bench | **re-render**: v2 moves, v3 base, deplated, left-side parts in S1 end poses (in frame fully or out) |
| 8 | **X v3** | whole (exploded view) | 28.511-31.560 (855-947) | 3.0667 | apart plus slow orbit 28.511-29.527 (n24-n26); fly home 29.527 -> **lock 30.544** (groove stops); hood and hatch close on their hinges; clean car, fade st 2.55 d 0.5 | high, about 55-60 deg down, car length along the frame height, slow orbit of about 10 deg. Layout: hood up and forward, fbumper ahead of the nose, hatch and rbumper behind the tail, inner ring of seats at about +-1.5 m (driver / passenger, bench split in 3 on the left), outer ring of doors and the fender at about +-2.4 m. Every part fully inside the 9:16 margins on the first, middle and last frame. | **new**: frames after the lock render on base car4 with no parts (c5 lesson) |
| 9 | logo | - | 31.560-33.600 (947-1008) | 2.0333 | - | small logo (about 320 px) over the pad tail | `tools/logo_card.py --secs 2.0333 --width 320` |

**Sections in order:** whole, front exterior, wheels, engine bay, front bumper removed, side + interior, rear bumper removed (incl. boot), whole (exploded / reassembly).
- Each section appears once.
- Right-side doors and the passenger seat appear only in X.
- No shot is reused, and O_whole and X differ in angle and subject (closed car low front 3/4 vs exploded top-down).

**Labels:**
- v2's four labels, unchanged: F2 17.327-18.800 and 19.360-20.250; R1 26.477-27.430 and 27.494-28.400.
- New: INTERIOR 24.44-25.36.
- Re-check R1's labels against the new left-side parked parts.

### Music map v3

| Event | t (s) | frame | grid |
|---|---|---|---|
| cut N | 4.109 | 123 | intro hit |
| cut s3 | 8.176 | 245 | intro hit |
| cut F1 | 9.701 | 291 | intro hit |
| hood opens | 11.226 | 337 | intro hit |
| **cut F2** | **16.310** | **489** | drop, n0 |
| cut S1 / fender | 20.377 | 611 | n8 |
| FL door | 21.394 | 642 | n10 |
| driver seat | 22.410 | 672 | n12 |
| RL door | 23.427 | 703 | n14 |
| bench + INTERIOR label | 24.440 | 733 | n16 |
| cut R1 | 25.460 | 764 | n18 |
| cut X (exploded) | 28.511 | 855 | n24 phrase |
| parts start home | 29.527 | 886 | n26 |
| **lock** | 30.544 | 916 | n28, groove stops |
| cut logo (out of black) | 31.560 | 947 | n30 (pad tail) |
| end | 33.600 | 1008 | |

### Diff vs v2

| v2 | v3 | change |
|---|---|---|
| O, N, s3, F1, F2 | same slots | **reuse as-is** |
| S1_side 20.377-24.440 | S1 v3 20.377-25.460 | **new render**: +1.02 s, interior base, seats out, doors park up, event order front -> rear |
| s4_lightbar 24.440-25.460 | - | **dropped** |
| R1 25.460-28.511 | same slot | **re-render** on the v3 base (deplated) |
| X_reassemble 28.511-30.544 (reassembly only, lock 29.51) | X v3 28.511-31.560 | **new render**: a real exploded view held for 2 kicks, incl. right doors, passenger seat and the split bench; lock 30.544 |
| logo 30.544-33.600 | 31.560-33.600 | logo card re-run at 2.0333 s |
| 4 labels | 5 labels | + INTERIOR |

Render the 30 % preview of S1, R1 and X (first, middle and last frame) before the finals. Persistent data stays off, and run a per-frame luma scan on every final.

### Open questions for the editor (check; don't guess)

1. **Driver side.**
   - Confirm with a labelled top-down still that Driver Seat sits at +X (car's left). Reg frame 2 suggests it does.
   - If it is at -X (RHD), swap: the passenger seat comes out in S1 and the driver seat goes to X only.
2. **Bench split.** Which backrest (1/3 or 2/3) is on the left? This sets the X layout only.
3. **Cabin cut.**
   - Cut the old Doors-and-Hood-Open cabin fill out of comp_explode by the No Seats shell's box (lessons: cut by part box, not proximity), or the seats appear twice.
   - Look at a still with the seats out.
4. **Roofless shell edge.** Check that no seam or shell top edge shows through the door openings under the car's roof line in S1's last frame.
5. **Seat undersides and rails.**
   - If the seat bottoms are ragged, keep the camera at or above seat-cushion height while they are out.
   - Name nothing on the floor unless the still shows it.
6. **R1.** Did the plate-only R1 re-render already run on the old base? If so, it needs this v3 re-render.
