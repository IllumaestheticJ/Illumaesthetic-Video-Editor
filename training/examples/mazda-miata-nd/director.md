# Mazda Miata ND v2 - director's shot plan (stage 2)

Scene order from `direction.md` (not changed). One focus per shot; every section appears in one continuous run.
Frame: prepped metres, front = -Y, car's right = -X, ground z = 0. Camera `loc`/`target` are absolute.
Part keys are offsets from home (`loc` m, `rot` deg XYZ about the pivot; pivot = part bbox centre unless "hinge").
Times are in **beats b from the shot start** (seconds = b x 0.51721). Ease names as in `tools/shot.py`.
All renders: 75 %, 12 spp, `persistent: false`, 15 fps, sensor 20.25. After every render: per-frame mean-luma scan
(dark-frame lesson), first/mid/last frame framing check against the "framing" column, re-render bad ranges in fresh processes.

Hinges: hood pivot (-0.1237,-0.458,0.8887), open rot (-43.67,0,0); trunk pivot (-0.1237,1.3358,0.9865), open rot (85.69,0,0).
Neither panel has an inner face: **no camera may see the underside of x_hood or x_trunk** (constraints are in the shots).

## Shot table

| # | Section | Shot id | Frames (30 fps) | Focus | Camera | Part action (beats) | Framing first / mid / last | Why it earns its seconds | Source |
|---|---|---|---|---|---|---|---|---|---|
| 1 | whole | **v2_a_open** | 0-62 (2.07 s) | the whole car | `arc(r 7.8->7.2, a -50->-38, h 1.55->1.35, c (0,-0.2,0.6)->(0,-0.25,0.6), focal 30, n=8)` = slow push + 12 deg orbit toward the nose, moving from frame 1 | - | car 75-85 % of width, nose and tail >= 60 px from the edges, wheels and roof whole, car centred at ~55 % height / same / same | hook: the whole car, front end forward (richest end) | NEW, car4np |
| 2 | front | s4_lamp | 62-124 (2.07 s) | right headlight + grille | v1 | - | v1 (nose fills width) | 2 mm signature detail | REUSE as-is |
| 3 | front | **v2_f_bumper** | 124-248 (4.14 s) | front bumper -> its inner face -> crash beam | b0 loc (-1.75,-4.35,1.35) tgt (0,-1.60,0.45) f30; b4 loc (-1.68,-4.22,1.30) tgt (0,-1.62,0.42) f30 inout; b4.5 same as b4; b7.5 loc (-0.85,-3.25,0.85) tgt (0,-1.75,0.45) f28 inout; b8 same loc, f29 lin | x_fbumper: b0-0.5 home; b0.5->2 loc (0,-0.45,0) `out`; b2->4 loc (0,-1.0,-0.62) rot (150,0,0) inout (inner face turns to the lens, ends below the nose in black); static after | nose incl. both lamps ~76 % width / bumper fully in frame below the nose, inner face to the lens, >= 60 px margins, not over the body / crash beam + brackets ~85 % width, bumper fully OUT of frame (bottom) | hero beat 1: the part off + what was behind it, held long enough to read | NEW, comp_front + x_fbumper |
| 4 | front (engine bay) | **v2_f_bay** | 248-341 (3.10 s) | hood to its captured open pose -> engine bay | b0 loc (-1.10,-2.50,3.30) tgt (0,-1.00,0.60) f30; b6 loc (-0.80,-2.05,2.75) tgt (0,-0.95,0.62) f30 inout (~55 deg down: keeps the open hood's underside away from the lens) | x_hood (hinge): b0-2 home; b2->4 rot (-43.67,0,0) inout, **lands on n16 = frame 310** (the lift); x_fbumper static at v2_f_bumper's end pose (out of frame) | hood + front structure fill width / hood mid-swing, top skin facing camera / bay ~fills width, open hood whole at the top | the registered hood-open state, on the music's lift | NEW, comp_front + x_hood |
| 5 | wheels | s3_wheel **reversed** | 341-403 (2.07 s) | front-right wheel, brake, tyre | v1, frames played f_0032 -> f_0001 (camera now slides rearward) | - | v1 | the only wheel shot; reversed it carries the travel toward the side | REUSE (reversed copy `s3_wheel_rev/`, symlinks) |
| 6 | side | **v2_s_side** | 403-497 (3.13 s) | right mirror's mount plate + harness, then the sill skirt | b0 loc (-2.15,-1.05,1.30) tgt (-0.85,-0.08,0.85) f50; b3.5 loc (-2.35,-1.00,1.28) tgt (-1.05,-0.10,0.95) f50 inout; b6 loc (-3.35,-1.25,0.95) tgt (-0.85,-0.05,0.45) f30 inout | x_mirror_r: b0.5->2 loc (-0.38,-0.05,0.18) `out`; b2->3.5 + rot (0,0,-135) inout (mount plate + harness face the lens; small part, clear of the body); static after. x_skirt: b3.5->5 loc (-0.32,0,-0.06) inout, **no rotation** (single skin). Static: x_hood at rot (-43.67) on its hinge, x_fbumper at its v2_f_bumper end pose, x_rbumper / x_trunk / x_mirror_l home | mirror + A-pillar + fender top, mirror ~35 % width / mirror backside whole, centred / skirt ~90 % width, frame edges inside the arches (no half tyre at an edge; if a sliver shows, focal +2), mirror whole in the upper third | the side's only real parts; mirror backside is real data | NEW, comp_explode + parts |
| 7 | rear | **v2_r_bumper** | 497-590 (3.10 s) | rear bumper -> inner face -> exhaust / rear structure | b0 loc (-1.65,4.60,1.45) tgt (0,1.75,0.50) f30; b3.5 loc (-1.58,4.48,1.40) tgt (0,1.77,0.47) f30 inout; b5.5 loc (-0.75,3.55,0.85) tgt (0,1.95,0.42) f28 inout; b6 same loc, f29 lin | x_rbumper: b0.5->2 loc (0,0.45,0) `out`; b2->3.5 loc (0,1.0,-0.62) rot (-150,0,0) inout (ribs/brackets to the lens, below the tail in black); static after. x_trunk home | tail incl. both lamps + rear arches ~78 % width / bumper fully in frame below the tail, inner face to lens / exhaust tips + rear panel ~85 % width, bumper fully out (bottom) | hero beat 2: best-registered part (2.8 mm, inside + outside) and the real rear structure | NEW, comp_rear + x_rbumper + x_trunk |
| 8 | rear (trunk) | **v2_r_trunk** | 590-652 (2.07 s) | trunk lid to its captured pose -> trunk interior | b0 loc (-2.25,1.00,2.95) tgt (0,1.55,0.72) f30; b4 loc (-1.75,1.25,2.60) tgt (0,1.60,0.68) f30 inout. Camera stays at y < 1.33 (in front of the open lid's plane) so only the lid's outer skin is ever visible | x_trunk (hinge): b0.5->2.5 rot (85.69,0,0) inout (ends at the captured pose); x_rbumper static at v2_r_bumper's end pose (fully in or fully out of frame, never cut by an edge) | rear deck + tail ~80 % width / lid edge-on, top skin / interior fills the lower half, lid whole at the top | the registered trunk-open state | NEW, comp_rear + x_trunk + x_rbumper |
| 9 | explode | **v2_x_front** | 652-714 (2.07 s) | the front assembly rising into layers above the nose | `arc(r 4.4->4.0, a +38->+52, h 3.4->3.2, c (0,-0.7,1.1), focal 30, tz 1.1, n=8)` (high front-LEFT 3/4) | finale clock T = beats from n38; this shot renders T 0-4 (see finale keys) | nose + stack fill width, rear of the car deliberately cut through the cabin / layers separated, none crossing the body / same | progressive explode, angle 1, zoomed on the front assembly | NEW, comp_explode + 7 parts |
| 10 | explode | **v2_x_rear** | 714-776 (2.07 s) | the rear assembly in layers, return begins | `arc(r 4.4->4.1, a +142->+128, h 3.4->3.2, c (0,0.9,1.1), focal 30, tz 1.1, n=8)` (high rear-LEFT 3/4) | renders T 4-8 | tail + stack fill width / rear bumper inner face up, trunk lid top skin / rear bumper starts home (T7 = frame 760) | angle 2, zoomed on the rear assembly | NEW |
| 11 | reassembly | **v2_x_home** | 776-819 (1.43 s) | everything returns: the whole car | `arc(r 7.6->7.3, a +96->+104, h 2.6->2.3, c (0,0,0.6), focal 30, n=4)` (left side profile, slightly high so no lid underside is seen) | renders T 8-10.77. Parts lock at T10 = **frame 807, the last hit**. Two specs: (a) comp_explode + parts, 16 renders (t 0-1.0 s); (b) **car4np only**, camera keys shifted by -16/15 s, 7 renders, renumbered f_0017-f_0023 (clean car swap ON the hit, c5 lesson) | car 72-78 % width, stack in frame above / parts landing / clean whole car | reassembly -> fade (assembler: linear fade to black over frames 807-819) | NEW, comp_explode + parts, then car4np |
| 12 | - | logo | 819-885 (2.2 s) | small logo | `projects/ferrari-296/tools/logo_card.py <logo> logo_card_v2.mp4 --secs 2.2 --width 300` (28 % of 1080; v1 860) | fade in 8 frames, out with the audio | logo centred | end card | re-make |

### Finale part keys (shared clock T in beats from n38; each explode shot renders its window by subtracting its T0 x 0.51721 s from every key t)
Hood and trunk start **closed** in the finale and lift off flat (an open lid seen from these high/rear cameras would
show its missing underside). All layers sit above the car, tilted toward the lens; no part crosses the body.

| Part | T0 | Rise (inout) | Drift (lin) | Return (`in`, lands T10 = last hit) |
|---|---|---|---|---|
| x_hood (hinge pivot) | home | T0->2: loc (0,-0.15,0.85) rot (8,0,0) | T4->7: loc x1.06 | T7.25->10: home |
| x_fbumper | loc (0,-0.55,0) | T0.5->2.5: loc (0,-0.45,1.35) rot (90,0,0) (inner face up) | T4->7: loc x1.06 | T7->10: home |
| x_mirror_r | loc (-0.38,-0.05,0.18) | T1->3: loc (-0.45,0,0.75) | T4->7: loc x1.06 | T7.5->10: home |
| x_mirror_l | loc (0.38,-0.05,0.18) | T1->3: loc (0.45,0,0.75) | T4->7: loc x1.06 | T7.5->10: home |
| x_skirt | loc (-0.32,0,-0.06) | T1->3: loc (-0.55,0,0.40) | T4->7: loc x1.06 | T7.5->10: home |
| x_trunk (hinge pivot) | home | T1.5->3.5: loc (0,0.10,0.80) rot (-8,0,0) | T4->7: loc x1.06 | T7.25->10: home |
| x_rbumper | loc (0,0.55,0) | T2->4: loc (0,0.45,1.30) rot (-90,0,0) (inner face up) | T4->7: loc x1.06 | T7->10: home |

Rotations are translate-only for the mirrors, skirt, hood and trunk (no backside worth showing in the finale); the
bumpers tip 90 deg about the width axis because their scanned insides are the point.

## On-screen labels (feedback C; Remotion ScanHUD `label`, title only, no sub, no numbers)
Plain wording, only what the renders visibly show. Max 2 on screen, 80 px inside the edges (x 0.074 / 0.926), never over
the car or a part: check frames `from` and `from + duration` of each in the final render before burning in.

| Shot | Text | Beat in-out (n) | Frames from-to | Position |
|---|---|---|---|---|
| v2_f_bumper | FRONT BUMPER REMOVED | 6-8 | 155-186 | x 0.074, y 0.12, left |
| v2_f_bumper | MOUNTING POINTS | 6.5-8 | 163-186 | x 0.074, y 0.17, left (bumper's inner tabs are on screen) |
| v2_f_bumper | CRASH BEAM | 9-11.75 | 202-244 | x 0.074, y 0.12, left |
| v2_f_bay | ENGINE BAY | 16.5-17.75 | 318-337 | x 0.074, y 0.10 if that area is black; else y 0.88 |
| v2_r_bumper | REAR BUMPER REMOVED | 30.5-32 | 535-559 | x 0.074, y 0.12, left |
| v2_r_bumper | EXHAUST | 32.5-33.75 | 566-586 | x 0.074, y 0.12, left |
| v2_r_bumper (conditional) | REAR CRASH BAR | 32.5-33.75 | 566-586 | x 0.074, y 0.17; only if the bar reads clearly in the last frames (open question 1) |

No labels in the opener, side, trunk, explode or logo.

## Cut list (removed from v1)
| v1 shot (v1 frames) | Removed because |
|---|---|
| s1_turntable (0-124) | cropped nose (rule 4 / feedback A); 4.1 s of rotation on the pad intro. Replaced by v2_a_open (2.07 s, whole car) |
| s2_rear (124-248) | same view as s1 (IoU 0.79, corr 0.82); a rotation with no new subject; the rear has its own section later |
| s5_front (372-497) | too wide; bumper outer face only; open hood's empty underside faced the lens (camera ~22 deg down < 44 deg limit) |
| s6_rear_open (497-621) | too wide, car cropped at the frame edge; bumper inner face not shown; the open lid's empty underside faced the lens |
| s7_top (621-683) | rotation onto the hood's speckle holes (weakest data); "top" section dropped |
| s8_explode (683-869) | every part separating at once in one wide orbit (rule 2) |
| logo (869-972, 860 px, 3.43 s) | too big and too long (rule 7) |

## Hold list (> 0.75 s)
| Where | Length | Reason |
|---|---|---|
| logo 819-885 | 2.2 s | end card; rides the track's decay to the end |
| v2_f_bumper b4.5-8 (frames 186-248) | 2.07 s, camera moving | not a hold: the push-in onto the crash beam is the reading time for the label CRASH BEAM |
| v2_f_bay b4-6 (frames 310-341) | 1.03 s, camera moving | slow push into the engine bay after the hood lands; reading time for ENGINE BAY |
| v2_x_rear T4-7 (frames 714-760) | 1.55 s, parts drifting + orbit | the full stack is visible; nothing static |
No static frame (camera and parts both still) longer than 0.5 s anywhere before the logo.

## Render budget (15 fps renders, `N` = renders; spec `seconds` = (N-1)/15)
| Shot | Slot frames | N renders | src_fps = 30N/(slot+4) | Base | Est. s/frame |
|---|---|---|---|---|---|
| v2_a_open | 62 | 32 | 14.5455 | car4np (4 mm) | 13 |
| v2_f_bumper | 124 | 63 | 14.7656 | comp_front (2.9M tris) | 15 |
| v2_f_bay | 93 | 47 | 14.5361 | comp_front | 15 |
| v2_s_side | 94 | 48 | 14.6939 | comp_explode (3.1M) | 15 |
| v2_r_bumper | 93 | 47 | 14.5361 | comp_rear | 15 |
| v2_r_trunk | 62 | 32 | 14.5455 | comp_rear | 15 |
| v2_x_front | 62 | 32 | 14.5455 | comp_explode + 7 parts | 15 |
| v2_x_rear | 62 | 32 | 14.5455 | comp_explode + 7 parts | 15 |
| v2_x_home | 43 (31 + 12 fade) | 16 + 7 = 23 | 14.6809 | comp_explode + parts, then car4np | 14 |
| **total new** | | **356** | | | **~85 min serial** |
| s4_lamp (reuse) | 62 | 32 | 14.5455 | - | 0 |
| s3_wheel reversed (reuse) | 62 | 32 | 14.5455 | - | 0 |

356 is ~2 % over the ~350 target; nothing left to trim without cutting a hero beat. Preview every new shot first
(`frames: first, mid, last` at 30 %) and check the framing column before the final render.
Assemble with the concat assembler (`projects/honda-s2000/tools/concat_assemble.py`, exact `frames:` per clip; slots above).
Music: `mazda-miata-nd_track.mp3` from **6.2672 s**, 0.3 s fade-in, length 29.5 s, 0.4 s fade-out. Verify cut-to-kick
error on the delivered file (|err| <= half a frame).
