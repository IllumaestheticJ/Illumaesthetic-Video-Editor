# MR2 Spyder v3 scene direction (scene-director, 2026-11-11)

Inputs: clips.md, project.yaml (v2 draft), project_v1.yaml, editlog, feedback, review.md, shots.py, director_report.md,
contact sheets of every render in `/home/user/media/work/renders/mr2/*` (first/middle/last frames + full-res crops of the
opened front and rear; bounding boxes measured on the PNGs). Applies the v2 brief from the parent session (items 1-9) and the
newer user feedback A-D, which overrides the brief where they conflict.

## 1. Feature inventory (from the scans, not from memory of the model)

| region | registered data | states (registered scan of THIS car) | parts (registered) | what the renders show | quality | richness |
|---|---|---|---|---|---|---|
| whole car | Full Car (hardtop on, car2.blend 2 mm, clean) | hardtop on | - | clean silver car, wheels captured | best | bookends only |
| front | composite front = roof-down car trimmed + 2023-06 Hood Duct Data (2.0 mm) | **hood open + front bumper off** (Hood Duct Data) | hood (diff, outer skin), front bumper (diff, outer skin, thin/ragged edges) | with bumper off and hood up: upper nose panel with emblem stays, front compartment with **strut tower top**, fluid reservoirs, upper cross member; under the headlights the lower front is ragged with black holes; no crash beam is readable | medium; lower nose weak | **highest: 2 parts + 1 state + hero data (feedback C)** |
| wheels | Full Car | - | - | s4: front wheel + arch fill the frame, spokes/caliper readable | good | 1 detail shot |
| side | Full Car / Full Car Top Down | - | - | door, side intake behind the door | good | no states; covered inside the top scene |
| top / cabin | Full Car Top Down (1.15 mm) | **hardtop off** (roof down) | hardtop (diff, outer skin only - its underside was never scanned) | seats, tube roll bar with diagonal behind the seats, console | good, clean | 1 part + 1 clean state |
| rear | Rear End trunk open (1.45 mm) | **rear lid open** | rear lid (diff, outer skin; hinge fit -66 deg, 11 mm median) | tail lamps, rear mesh grilles, blank plate; lid up reveals the mid-engine bay (engine, strut brace) | good | 1 part + 1 state |
| not usable | 2022 Front Bumper Data, Hood Open (Tab Ref), FrontEnd (not registered); Rear QuarterPanel, Trunk Open Cover On, Rear Interior Trim Removed (registered, not prepped) | - | - | - | - | never shown or implied |

Feedback D check: hood open (Hood Duct Data), rear lid open (Rear End trunk open), hardtop off (Full Car Top Down) are the
only openings in the plan. No doors open, no front bumper inner face (not scanned), no hardtop or lid underside held on screen.

## 2. Scene order (travel nose -> roof -> tail, one continuous trip, each section once)

| # | scene | scans used | section covered (feedback B) | feature shown | why here | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | OPENER `s1_wide` (reuse) | Full Car | whole car | the whole hardtop car in side profile, camera drifting toward the nose | whole car with motion from frame 1 (brief 4); the only existing render that holds the whole car with margins on every frame (66-69 % width, 84-186 px margins; s2_front34 clips the nose at the left edge up to f60) | 8 (fade up 1.0 s) | Temerario 0-3 s framing; the drift toward the nose hands over to the front |
| 2 | WHEEL `s4_wheel` (reuse) | Full Car 2 mm | wheels | front wheel + arch, extreme close-up | the front corner before the front comes apart (Temerario 11.5 s fly-in); cut ON the first strong hit | 4 | s4 as rendered |
| 3 | FRONT HERO `s12_front` (NEW) | composite + hood + fb, hardtop on | front (bumper, hood, front compartment) | bumper comes off, camera moves in on what is behind it, hood swings up on its fitted hinge, end looking down at the strut tower / front compartment; 3 labels | richest region (2 parts + the registered bumper-off/hood-open state) and the user's hero beat (C); longest scene | 12 | front-left high, rising 12 -> 44 deg el |
| 4 | SIDE + TOP `s13_top` (NEW) | composite + hardtop part, front stays open | side (door/intake) + top/cabin | hardtop lifts straight up out of frame, camera cranes from the door line to a look down into the roof-down cabin (1.15 mm scan) | middle of the car, next in the travel; clean data | 12 | -X side, crane 28 -> 66 deg el, az drifts only 12 deg (no orbit) |
| 5 | REAR `s14_rear` (NEW) | composite + rear lid, top gone, front open | rear (tail, lid, engine bay) | tail lamps/grilles, then the lid swings up on its hinge ON the second strong hit and the camera moves in over the engine bay | last section of the trip; one part + one state | 12 | rear-left 3/4, crane 16 -> 50 deg el |
| 6 | REASSEMBLY `s15_reassemble` (NEW) | composite + 4 parts -> clean car2 | whole car (bookend) | parts return front -> roof -> rear, clean full car takes over as the last panel lands, fade to black | Temerario ending; rear-right 3/4 so it repeats neither the opener (side) nor the rear scene (left, close) | 9 | wide, whole car in frame with margins |
| 7 | logo card (reuse `logo_card_v2.mp4`) | - | - | small logo on black on the final hit | | 3.1 s | |

Order rationale: brief 1 (front data first, then side, then rear) + scene-director travel rule. The opener is a side profile of
the whole car, but its camera moves toward the nose and the first data scene is the front; nothing returns to the front later.

## 3. Music map (kick grid, beat n at -0.0591 + 0.5357 n s; bar lines n = 6 + 4k)

**Music now starts at 3.155 s (bar n = 6, the track's first kick accent; v2's first cut).** Reason: feedback B removes the
duplicate shots that filled v2 (s2/s3 turntables, s5, s7a/s9a, s7b/s9b, s8, s10, s11 - see diff), and only two existing renders
pass feedback A. The remaining content with one sequence per section is 30.5 s, not 33.7 s. Trimming the 6-beat intro keeps
every v2 cut point, both strong hits and the final hit on the logo. (Fallback if the track must start at 0: see open questions.)

| reel t (s) | music t (s) | n | event |
|---|---|---|---|
| 0.000 | 3.155 | 6 | OPENER fades up (1.0 s) |
| 4.286 | 7.441 | 14 | **strong hit** - cut to WHEEL |
| 6.428 | 9.583 | 18 | FRONT HERO; bumper starts moving 0.26 s later |
| 9.643 | 12.798 | 24 | hood starts to swing up |
| 12.857 | 16.012 | 30 | SIDE + TOP; hardtop lifts at n 31 |
| 19.285 | 22.440 | 42 | REAR (tail first) |
| 21.428 | 24.583 | 46 | **strong hit** - rear lid starts to open |
| 25.714 | 28.869 | 54 | REASSEMBLY |
| 30.535 | 33.690 | 63 | **final hit** - logo |
| 33.635 | 36.79 | | end (logo 3.1 s) |

## 4. Diff against the v2 draft timeline

| v2 shot | v3 | reason |
|---|---|---|
| s1_wide | **kept as opener** (frames 1-54, 8 beats) | whole car in frame on every frame; Temerario opener |
| s2_front34 | dropped | nose clipped at the left edge f1-60 (feedback A); turntable that shows nothing new (brief 3) |
| s3_rear34 | dropped | turntable; rear clipped left then nose right; rear exterior merged into REAR |
| s4_wheel | **kept** (frames 1-36) | detail shot with its section filling the frame |
| s5_tail | dropped (content merged into REAR's first third) | hardtop is on in s5, so it cannot sit after the hardtop comes off; before it would be a ping-pong |
| s6_hardtop | replaced by s13_top | front is closed in s6 but must stay open after the FRONT scene; nose clipped at f68 |
| s7a_front + s9a_front | merged into s12_front | same subject in two shots (flagged IoU 0.73); s7a has the hardtop already gone |
| s7b_rear + s9b_rear | merged into s14_rear | same subject twice; s7b clips the open hood at the right edge; s9b clips the lid stack |
| s8_top | dropped | rotating top-down that repeats every section |
| s10_float | dropped | bumper clipped at the left edge on every frame; shows every part again |
| s11_reassemble | replaced by s15_reassemble | ends on the opener-like front 3/4; bumper clipped at the left edge at the start |
| s1_side, s7_open, s9_explode | stay unused | cropped strip / all parts at once in one wide orbit |

## 5. Open questions for the editor / parent

1. **Music start 3.155 s** shortens the reel 36.8 -> 33.6 s. If the parent wants the track from 0, add 6 beats to the FRONT
   scene instead (render ~+38 frames) - do not pad with reused turntables.
2. Label "ROLL BAR": the cabin scan shows a tube hoop with a diagonal behind the seats. Confirm on the s13 end frame before
   showing the label; if it is not clearly a roll bar, show no second label in that scene.
3. "ENGINE BAY": the file is named "Rear End trunk open", but the renders under the MR2 Spyder rear lid show the engine
   (mid-engine car). Confirm on the s14 end frame; fallback text "REAR LID OPEN" only.
4. No "CRASH BEAM" / "MOUNTING POINTS" labels: no beam or mounts can be read in the renders behind the bumper (lower nose is
   ragged). If the FRONT end frame clearly shows one, the director may add it; otherwise not.
