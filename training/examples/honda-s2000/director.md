# Honda S2000 AP1 - director's shot plan (v6)

Director stage (`.claude/agents/director.md`); scene order from `direction.md` (unchanged). Overriding user notes A-D:
whole car fully in frame in wide shots, details fill the frame; each section in one run; Bumper Removed is the hero with
labels; **no hood animation, no hood/trunk in any explode - the front bumper is the only moving part.**

Frame: prep metres, nose -Y (bumper y -1.88), tail +Y 2.23, car's right = -X, width +-0.93, roof 1.33.
Grid: cut frame = round((0.0565 + n*0.43463)*30). Assemble with `tools/concat_assemble.py` (exact `frames:`).
Retime reused PNGs with `src_fps = (N-1)/(dur + 3/30)` (lesson), never `speed:`.

## Part animation (one master list, all front shots render windows of it)
`BUMPER` = `bonly.blend`, `pivot: [0, -1.75, 0.35]`, time origin **b32** (t = (beat-32)*B; shot `t0` = (start beat-32)*B).
| beat | loc offset (m) | rot (deg, X) | ease into key | what it reads as |
|---|---|---|---|---|
| 32.0 | 0,0,0 | 0 | - | bumper on the car at the drop |
| 33.0 | 0,-0.30,0 | 0 | out | pulled straight off the structure |
| 34.5 | 0,-0.55,-2.80 | 0 | in | drops forward/down out of the bottom of the frame (toward the lens, into black) |
| 60.0 | 0,-0.55,-2.80 | 0 | lin | parked off-screen (F2-F4 render WITHOUT the part) |
| 64.0 | 0,-1.35,0.25 | 120 | out | rises into clear black in front of the nose and tips forward: inner face up toward the high front camera |
| 66.5 | 0,-1.45,0.32 | 126 | lin | slow drift so the hold is never a freeze |
| 68.0 | 0,-0.90,0.00 | 0 | inout | un-tips, faces the car again |
| 69.5 | 0,-0.90,0.00 | 0 | lin | beat of stillness |
| 76.0 | 0,0,0 | 0 | in | slides home and **locks on b76** (33.088 s) |
If the editor's back render of `bonly` shows a ragged inside: replace the 64/66.5 rows by rot 0 and loc (0,-1.6,0.35) /
(0,-1.7,0.4) (translate only, toward the lens) - lesson: no flip unless the backside is worth showing.
Base for F1/F5/F6/F7 = `comp_front.blend` (car - bumper + Bumper Removed, hood closed). Keep the state-session bumper on
its own structure to the end (do not swap to car4 at the lock: its bumper sits 25 mm further back).
`persistent: False` for F1, F5, F6 (animated part); scan per-frame luma after each render (lesson).

## Shot table
| section | shot | beats / frames (30 fps) | focus | framing intent (editor checks first/mid/last) | camera (loc -> loc, target, focal) | part action | why it earns its time | source |
|---|---|---|---|---|---|---|---|---|
| whole | W1 | b0-8 / 0-106 (106) | whole car, long hood + badge side | whole car inside frame, >=6 % black each side, nothing clipped (nose, tail, mirrors, roof) | `arc(0, 3.6, r 6.4->6.1, ang 24->44, h 1.45->1.30, c=(0,0.17,0.55), focal 26)` | - | hook: moving from frame 1, approved opener move pulled back | **re-render** 56 fr |
| side | S1 | b8-12 / 106-158 (52) | S2000 badge -> mirror -> door handle | detail fill; must end before the black arch | as rendered | - | only side features; glides rearward = travel | reuse s4b_flank **frames 0-21**, src_fps 11.4 |
| rear | R1 | b12-16 / 158-210 (52) | ducktail, tail lamps, short deck | whole car with >=6 % margins | `arc(0, 1.95, r 6.0->6.0, ang 148->182, h 1.7->1.9, c=(0,0.35,0.55), focal 26)` | - | only rear wide; swing to dead behind continues the lap | **re-render** 30 fr |
| rear | R2 | b16-20 / 210-262 (52) | right tail lamp + ducktail edge | detail fill | as rendered | - | rear detail next to its wide | reuse s4_tail frames 0-26, src_fps 14.2 (check plate legibility) |
| top | T1 | b20-28 / 262-367 (105) | plan view: long hood/short deck, hardtop | whole car, measured clean (>=10 % margins all frames) | s7_top **reversed** (top-down -> high front-right 3/4) | - | carries us over the car to the front, one pass | reuse s7_top frames 41->0, src_fps 11.4 |
| front | F0 | b28-32 / 367-419 (52) | left headlight + bumper lamps | detail fill | as rendered | - | quiet ECU in the drums-out break; last look at the bumper on | reuse s3_lamp frames 0-26, src_fps 14.2 |
| front | F1 | b32-40 / 419-523 (104) | bumper comes off -> beam revealed | start: whole front end fender to fender, ~5 % margins; end: beam ~89 % of width | (-1.25,-5.05,1.35) t(0,-1.7,0.5) f28 -> hold-drift to (-1.15,-4.95,1.33) at 2.5B (lin) -> (-0.55,-3.95,1.15) t(0,-1.8,0.42) f28 at 8B (inout) | b32-34.5 off and out of frame bottom | the one real state lands on the drop; camera moves in on what is behind | **new**, t0=0, 56 fr |
| front | F2 | b40-48 / 523-628 (105) | bumper beam + radiator support, centre | detail fill: beam centre, uprights, lower crossmember | (-0.30,-3.45,1.00) t(0,-1.8,0.40) f32 -> (-0.12,-3.05,0.92) t(0,-1.8,0.38) inout | none (no part loaded) | hero hold to read the structure + labels | **new**, 56 fr |
| front | F3 | b48-54 / 628-706 (78) | car's-right beam end, bracket, duct/shroud | detail fill; keep the empty right arch out of frame (move target +X if it shows) | (-1.25,-2.95,0.55) t(-0.55,-1.8,0.35) f35 -> (-0.85,-3.10,0.50) t(-0.30,-1.8,0.35) inout | none | second angle, low, on the mounting hardware | **new**, 43 fr |
| front | F4 | b54-60 / 706-784 (78) | top of beam, support tie bar, headlight backs | detail fill, hood front edge at top of frame | (0.55,-2.75,2.35) t(0.15,-1.75,0.45) f28 -> (-0.55,-2.75,2.35) t(-0.15,-1.75,0.45) inout | none | third angle, from above, lateral slide | **new**, 43 fr |
| front | F5 | b60-68 / 784-888 (104) | the bumper part, inner face | bumper 70 -> 86 % of width on black, structure soft above it | (-0.90,-5.00,2.90) t(0,-2.90,0.55) f28 -> (-0.45,-4.75,2.55) t(0,-3.05,0.60) inout | b60-64 rise + tip 120, drift, b66.5-68 un-tip | part shown off in clear background (lessons) | **new**, t0=28B, 56 fr |
| front | F6 | b68-76 / 888-993 (105) | bumper slides home, lock | bumper + front end both in frame, no clipping of the bumper ends | (2.20,-5.10,1.00) t(0.10,-1.90,0.45) f28 -> (2.50,-4.40,1.30) t(0.15,-1.40,0.50) inout | b69.5-76 slide home, lock ON b76 | honest reassembly of the one part, slam on the outro accent | **new**, t0=36B, 56 fr |
| whole | F7 | b76-80 / 993-1045 (52) | assembled car | whole car, >=8 % margins, fade to black frames 1036-1045 | (2.70,-3.90,2.90) t(0,0.05,0.55) f26 -> (3.40,-4.90,3.50) t(0,0.10,0.60) out2 | locked (t0=44B) | Temerario end: assembled car, short, fade | **new**, 30 fr |
| - | logo | b80-end / 1045-1116 (71) | small logo | logo ~30 % width | - | - | end card through the hard stop | reuse logo_card_v4.mp4 |
Total 1116 frames = 37.2 s. Every angle is distinct: W1 low front-left far, R1 rear, T1 top->high front-right, F1 front-right
mid, F2 straight-on close, F3 low right close, F4 overhead, F5 high centre on the part, F6 low front-left, F7 high front-left far.

## Labels (user C; Remotion ScanHUD `label`, Inter Display caps, tracking +6, #e8ecf2, ~46 px, left-aligned x=80)
Only names the editor can see in the F1/F2 2 mm renders (fallback for L2/L3: "FRONT STRUCTURE"). Max 2 on screen. Top band
y 300-420 px (outside the subject, above the bottom 20 %). None on W1-F0, F3, F4, F6, F7.
| id | text | shot | in (beat / s / frame) | out (beat / s / frame) |
|---|---|---|---|---|
| L1 | FRONT BUMPER REMOVED | F1 | b35 / 15.268 / 458 | b39.5 / 17.224 / 517 |
| L2 | BUMPER BEAM | F2 | b41 / 17.876 / 536 | b47 / 20.484 / 615 |
| L3 | RADIATOR SUPPORT (2nd line, y +70) | F2 | b43 / 18.745 / 562 | b47 / 20.484 / 615 |
| L4 | FRONT BUMPER - INNER SIDE (or FRONT BUMPER if the inside is not shown) | F5 | b64 / 27.873 / 836 | b67.5 / 29.395 / 882 |

## Cut list (from v5)
- s1_front: v5 frames 21-74 clip the nose (left edge from frame 19) -> W1.
- s2_rear: clipped from frame 19, slow orbit = rotation for its own sake -> R1 (4 beats, purposeful).
- s4b_flank frames 22-29: dead black empty arch -> trimmed.
- s5_front_open: fake hood lift + left fender cropped -> F1.
- s6_structure: hood raised (fake) -> F2/F3/F4.
- e1..e8 / s8_explode (incl. v4_old): hood (and trunk lid) in a one-burst wide explode -> F5/F6 one-part show and return.

## Hold list (> 0.75 s)
- F1 b34.5-40 (2.4 s, part still, camera pushing): reveal of the real state + L1 read time.
- F2 whole shot (3.5 s, camera push only): hero detail read, L2/L3.
- F3, F4 (2.6 s each, camera slides): mounting detail read.
- F5 b64-66.5 (1.1 s, slow drift): inner face read + L4.
- F7 (1.7 s, locked car, camera pulling out): assembled car read, then fade.
- logo 2.37 s (through the hard stop and reverb).

## Render budget (15 fps, +3 tail frames each)
New: W1 56, R1 30, F1 56, F2 56, F3 43, F4 43, F5 56, F6 56, F7 30 = **426 frames**. Order: F2/F3/F4 (static, fast), then
F1, F5, F6, F7, W1, R1, one at a time; preview first/mid/last at 30 % for every shot first and check framing intent.
Reused unchanged: s4b_flank (0-21), s4_tail (0-26), s7_top (reversed), s3_lamp (0-26), logo_card_v4.mp4.

## IRL slot (when the S2000 scanning footage arrives)
b0-2 (frames 0-28, 0.93 s) real shop clip of the car being scanned -> hard 1:1 cut on b2 (frame 28) into W1 re-rendered from
the solved camera (first key = solved pose, then the same arc), W1 runs b2-8 (78 frames). Pick an IRL frame where the car is
in its scanned state (no wheels). No text over IRL.
