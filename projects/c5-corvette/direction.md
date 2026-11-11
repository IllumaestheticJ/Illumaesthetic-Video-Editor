# v3 direction

2026-11-11. Reviewer on v2 (verbatim): *"c5 planning is good, but there's a lot of artifacts. We also have gas cap and Doorsill
scans, as well as a trunk scan to show off. Delete/hide the artifacts from the full car scan when it cuts in"*.

What v3 keeps: the v2 structure. That is open whole, then one continuous sequence per section, removed-state hero beats with
title-only labels, part spins only where the backside was scanned, reassembly to the clean car on the 34.402 loud kick, and a small
logo on 35.496. What v3 changes:
- **Three new STATE-SWAP scenes**: LEFT DOORSILL, GAS CAP and TRUNK OPEN. No door, fuel-door or hatch part scan exists, so nothing
  swings or lifts. The section base swaps from the closed full scan to the captured open state in-shot, on a strong kick. Only that
  region changes.
- **Artifact fix (geometry, not grading)**: every shot gets its own base. Each base is the clean car trimmed ONLY under that
  section's part(s), plus ONLY that section's captured state, island-filtered. The v2 composite `base.blend` (all states in one,
  which caused the ragged trim lines in the bay, the fender macro and the rear structure; see the v2 sheet
  `/home/user/media/work/out/c5_corvette_v2.mp4` frames 300/480/880) is not used in v3.
- **Order: one loop around the car instead of a side-crossing.** The proposal went -X fender, then +X doorsill, which cuts across
  the line in the middle of the reel. v3 moves the -X fender to the end. The camera travels front (bumper, hood), then +X (doorsill,
  gas cap), then rear (trunk, rear bumper), then -X (fender), then back to the -X front 3/4 for the reassembly. That is one
  continuous lap with az always increasing (-28 → 0 → +22 → +115 → +160 → 180 → -75 → -40), no line cross and no ping-pong.
  The reassembly wide then continues from the fender shot instead of jumping from the rear to the front (the v2 draft I fault).
- **Hood keeps 5 kicks, reassembly gets 3** (proposal: 4 / 4). The hood is still the richest region: hinge, captured 46 deg,
  scanned underside, removed-state bay. Its open → lift → flip → bay sequence cannot be read in 4.36 s. The reassembly is the
  payoff, not data, and "last scenes held too long" was a v1 note.

Seen before writing: the v2 delivered sheet (scratch tile of frames 20-1040). It shows the small opener car (~45 % of the width in
frame 1), the ragged composite in the bay, fender and rear views, and labels at y 0.86 sitting over black in the hood, fender and
rear shots. There are no renders yet of the three new scans. Their targets below are estimates from the car frame. **Centre each
target on the state scan's own bbox** before the framing strip.

## v3.1 Feature inventory delta (v2 inventory below still holds)

| region | new registered data | what it must show (show-off) | weak data / risk | richness → length |
|---|---|---|---|---|
| +X door / sill | `C5 Left Doorsill` (1.7 mm): door swung open, sill, floor edge | the sill top and its step, the floor edge running inboard, the open door's inner face and jamb. The camera looks INTO the opening from behind and above, so the open door sits forward and does not cover the sill | trim seam where the state meets the closed body (B-pillar, roof rail, rocker); possible holes on the door's inner face | one state, no part → 3 kicks |
| +X rear quarter | `C5 Gas Cap` (1.5 mm): fuel door open | the open fuel door, the recess and the filler neck/cap, filling the frame at the end (macro). 1.5 mm is the best median in the project, so a close macro is justified | recess depth may be shallow or have holes; check that the cap itself is in the scan before using the word GAS CAP over it | one state → 3 kicks |
| top / rear | `trunk open` (1.9 mm): cargo tub from above, hatch glass absent, y 1.40..2.14, z 0.48..0.86 | looking down into the tub: the floor, the side walls and the rear wall, with depth readable. The hatch opening edge frames it | ragged edge where the glass was (weak data: keep high and look down, never a grazing view of the edge); editlog 2026-11-11 06:13 called a trunk scan "not useful" (see open questions) | one state → 3 kicks |
| +X (right) doorsill | did not register | - | - | **excluded** |

## v3.2 Section table (30 fps; cut frame = round(t*30); strong kicks only)

| # | shot id | section | cut in (s / frame) | cut out (s / frame) | kicks | swap / key event inside (s / frame) | label (frames, last frame inclusive) |
|---|---|---|---|---|---|---|---|
| 1 | `v3_open` | whole → front bumper | 0 / 0 | 4.10 / 123 | intro | fb starts off at 1.20 (36); base swap clean → BASE_FB on that frame | - |
| 2 | `v3_fb` | front bumper removed | 4.10 / 123 | 9.310 / 279 | intro | bumper turns inside 6.0 → 8.3 | FRONT BUMPER REMOVED 132-186; FRONT BUMPER - INSIDE 230-272 |
| 3 | `v3_hood` | hood / engine bay | **9.310 drop** / 279 | 14.769 / 443 | 5 | 46 deg on 10.400 (312); lifted on 11.496 (345); underside on 12.584 (378) | HOOD REMOVED 381-436 |
| 4 | `v3_sill` | +X door / sill | 14.769 / 443 | 18.040 / 541 | 3 | **swap: door open on 15.856 (476)** | LEFT DOORSILL 479-534 |
| 5 | `v3_gas` | +X rear quarter | 18.040 / 541 | 21.312 / 639 | 3 | **swap: fuel door open on 19.135 (574)** | GAS CAP 577-632 |
| 6 | `v3_trunk` | top / trunk | 21.312 / 639 | 24.585 / 738 | 3 | **swap: trunk open on 22.404 (672)** | TRUNK OPEN 675-731 |
| 7 | `v3_rear` | rear bumper removed | 24.585 / 738 | 28.946 / 868 | 4 | bumper clear on 25.676 (770); turn starts 26.773 (803), square 27.585 (828) | REAR BUMPER REMOVED 760-800; REAR BUMPER - INSIDE 829-861 |
| 8 | `v3_fender` | -X front quarter | 28.946 / 868 | 32.221 / 967 | 3 | fender out on the cut, gone above frame by 30.65 (920) | FENDER REMOVED 904-960 |
| 9 | `v3_home` | whole car (reassembly) | 32.221 / 967 | 35.496 / 1065 | 3 | rb home 33.314 (999); fb locks + **swap to clean car 34.402 (1032)**; fade 34.735-35.485 | - |
| 10 | `logo_small` (reuse card) | - | **35.496** / 1065 | 39.40 / 1182 | - | - | - |

Label rule check: every label starts ≥ 8 frames after its shot's cut and its last frame is ≥ 6 frames before the next cut
(tightest: FRONT BUMPER - INSIDE ends 272 vs cut 279 = 7; LEFT DOORSILL 534 vs 541 = 7; REAR BUMPER - INSIDE 861 vs 868 = 7;
FENDER REMOVED 960 vs 967 = 7). One label at a time. Fades are 0.2 s in and out. Entries sit 0.1 s after a kick or an event.
Style is the same as v2: Inter Display, tracking +6, `#e8ecf2`, x 0.08 left, **y 0.86 over black**, `sub: " "` (empty sub crashes ScanHUD).

Assembly `dur` (whole frames): open 4.1000 (123, `fade=t=in:st=0:d=0.4`) / fb 5.2000 (156) / hood 5.4667 (164) / sill 3.2667 (98) /
gas 3.2667 (98) / trunk 3.3000 (99) / rear 4.3333 (130) / fender 3.3000 (99) / home 3.2667 (98, `fade=t=out:st=2.514:d=0.75`) /
logo 3.9000 (117). The total is 1182 frames. `beats:` = [4.100, 9.310, 14.769, 18.040, 21.312, 24.585, 28.946, 32.221, 35.496]. After the
first assembly, re-read the 40-150 Hz 8 ms and broadband 1 ms envelopes around every cut and swap (lesson: double kicks).

## v3.3 Per shot

Conventions: az 0 = in front of the nose, -90 = -X, +90 = +X, 180 = behind. Ground z = 0, nose y -2.29, tail y +2.2. Keys are in
**shot-local seconds** (convert with t/sec, as `cam()`/`anim()` do). Render length = cut length + 0.4 s slack (≥ +3 source frames). Lens 30-35
on the 24 mm HORIZONTAL sensor (frame width ≈ 0.8·dist at 30 mm). Persistent data OFF on every shot (all have motion or a
visibility swap). "Full scan" = the untouched clean `car.blend`. Each BASE_x is built as stated and island-filtered (drop
disconnected components and state tris below 70 mm, as v1).

### 1 `v3_open` (0-4.10): whole car from frame 1 → front bumper starts off
- Camera: t0 az -28, el 11, dist **5.8**, target [0, -0.05, 0.58], lens 30. Then t 4.50 az -28, el 9, dist 3.7, target [0, -2.15, 0.40]
  (the v2 end pose). One straight push. v2 started at 7.2 m and the car read small (review.md; Cappuccino lesson). Set the start
  dist so the car spans 80-88 % of the width with ≥ 6 % margin each side on frame 1.
- Objects: full scan [0, 1.20 s). From 1.20: **BASE_FB** = car trimmed under the `front_bumper` footprint only + `front bumper removed`
  trimmed to that footprint. The `front_bumper` part slides straight out toward the camera, off [0,-0.9,0.05], spin 0. Hood, fender and rear are the full scan.
- Label: none.

### 2 `v3_fb` (4.10-9.310): FRONT BUMPER REMOVED, hero beat 1
- Camera: same as v2 B. az -6 → **0**, el 7, dist 3.6 → 2.9, target [0,-2.40,0.80] → [0,-2.35,0.72], lens 30. The az drift
  starts the lap toward +X.
- Objects: BASE_FB + `front_bumper`. Bumper: held at [0,-0.9,0.05] to 0.30, rises to [0,-1.1,1.0] by 1.90, then turns about vertical
  to spin [180,0,0,1] by 4.20 (scanned inside to the lens), parked to the end. The structure stays readable in the lower frame for 5 s.
- Labels: FRONT BUMPER REMOVED 132-186 (4.40-6.20); FRONT BUMPER - INSIDE 230-272 (7.67-9.07).
- Re-render (v2 B sits on the composite base). Keys unchanged except the az drift.

### 3 `v3_hood` (9.310 drop - 14.769): hood on its hinge → underside → engine bay
- Camera: front 3/4 **+X** (mirrors v2's -22 so the lap continues). t0 az +22, el 24, dist 3.8, target [0,-1.45,0.70], lens 30.
  t 3.27 az +22, el 30, dist 3.6, target [0,-1.35,0.95]. t 5.46 az +26, el 42, dist 2.6, target [0.10,-1.15,0.50], lens 32
  (the bay fills the frame).
- Objects: **BASE_HOOD** = car trimmed under the hood + front-bumper footprints + `front bumper and hood removed` trimmed to those two
  footprints. `hood_combo` on HINGES. `front_bumper` hidden (it is off in this captured state and came off in shot 2). The fender is the
  full scan (the captured state has it on).
- Hood (spin [0,1,0,0] on all keys before the flip): deg 0 at 0.05 → **deg 46 at 1.09 (10.400)** → hold to 1.60 → lift straight UP
  to off [0,-0.25,1.15] at **2.19 (11.496)** → flip to deg 0, off [0,-0.55,1.30], spin [-75,1,0,0] at **3.27 (12.584)**, with the
  scanned underside square to the lens → hold to 4.10 → rises out of the top, off [0,-0.20,3.60], at 5.46 while the camera pushes into the bay.
- Label: HOOD REMOVED 381-436 (12.70-14.53), with the hood clear and the bay exposed.
- The 46 deg opening (1.04 s) and the flip (1.08 s) are fast. Render real 30 fps in-betweens for local 0-3.4 s (honda-civic-11
  `merge30.py`) so minterpolate does not smear the hood edges.

### 4 `v3_sill` (14.769-18.040): +X door closed → **door-open state on 15.856** → sill macro
- Camera: from behind the door, outboard and above. Looking forward and in, the open door lands forward of the opening and does not cover the sill.
  t0 az +118, el 18, dist 3.0, target [0.80,-0.15,0.50], lens 30 (closed door and rocker in frame, door fully framed).
  t 1.09 (swap) az +116, el 22, dist 2.5, target [0.82,-0.15,0.42]. t 3.67 az +110, el 28, dist 1.8, target [0.85,-0.15,0.32],
  lens 35 (sill + floor edge fill the frame; the open door's inner face is in the upper-forward frame).
- Objects: full scan until local **1.087 s** (frame 476). Then **BASE_SILL** = car trimmed under the closed door skin + sill footprint
  only (a box from the door shut lines, rocker to roof rail) + `C5 Left Doorsill`. No parts move. Do not animate the door.
- Show-off: the hold from 16.4 to 18.0 is on the sill top and step, the floor edge, the jamb and the door's inner face. The camera is still pushing.
- Label: LEFT DOORSILL 479-534 (15.97-17.80). This is the file name; +X is the car's left.

### 5 `v3_gas` (18.040-21.312): rear quarter, fuel door closed → **fuel door open on 19.135** → filler macro
- Camera: t0 az +105, el 12, dist 2.6, target [0.85,0.95,0.72], lens 30 (the door's rear edge, the rear quarter and the closed fuel
  door, with the rear wheel arch for context). t 1.09 az +110, el 14, dist 1.8. t 3.67 az +118, el 16, dist **1.0**, target [0.90,0.95,0.72],
  lens 35 (recess, open fuel door and filler neck/cap fill the frame). **Take the target from the `C5 Gas Cap` bbox. Pick the az on the
  swap test frame so the open fuel door does not cover the filler.** Move toward the rear quarter, not across it.
- Objects: full scan until local **1.095 s** (frame 574). Then **BASE_GAS** = car trimmed under the fuel door + recess footprint
  only + `C5 Gas Cap`. Do not animate the fuel door.
- Show-off: the filler neck and cap inside the recess, with the fuel door open beside it. Hold the macro for ≥ 1.5 s (19.8-21.3).
- Label: GAS CAP 577-632 (19.23-21.07).

### 6 `v3_trunk` (21.312-24.585): rear 3/4 +X high, hatch closed → **trunk open on 22.404** → looking down into the tub
- Camera: t0 az +160, el 38, dist 4.0, target [0,1.60,0.80], lens 30 (the closed rear hatch and the tail; the whole rear half is in frame).
  t 1.09 az +165, el 46, dist 3.2, target [0,1.72,0.70]. t 3.67 az +172, el **58**, dist 2.4, target [0,1.77,0.62], lens 32
  (the tub fills the frame width).
- Objects: full scan until local **1.092 s** (frame 672). Then **BASE_TRUNK** = car trimmed under the hatch glass footprint only (x
  inside the hatch frame, y 1.35..2.20, z above 0.86) + `trunk open`. Nothing lifts. The glass is simply absent in the captured state.
- Show-off: the floor, the side walls and the rear wall of the tub, with depth readable from above. The hatch opening edge frames it.
  Never use a grazing angle on the glass edge (ragged).
- Label: TRUNK OPEN 675-731 (22.50-24.37). At el 58 the tail can reach the bottom band: frame so the car ends above y 0.80, or
  give the label a dark plate (nissan-frontier lesson).

### 7 `v3_rear` (24.585-28.946): REAR BUMPER REMOVED, hero beat 2
- Camera: from the trunk's high view, crane down and round through 180. t0 az +176, el 12, dist 4.6, target [0,1.95,0.55], lens 30.
  t 1.09 az 180, el 10, dist 4.2, target [0,2.25,0.72]. t 4.76 az **-172**, el 9, dist 3.8, target [0,2.40,0.85], lens 30
  (structure lower frame, bumper inside upper frame, as v2 G2).
- Objects: **BASE_RB** = car trimmed under the `rear_bumper_inside` footprint + `Rear bumper removed` trimmed to it. The hatch
  is the closed full scan again (the trunk state belongs to shot 6 only).
- Rear bumper: home spin 0 at 0.05 → slides straight back to [0,0.9,0.05] at 0.75 → rises to [0,1.3,0.95] at **1.09 (25.676)** →
  hold (camera moves in on the structure) → turn starts **2.19 (26.773)** → spin [180,0,0,1] at 3.0 (27.585) → parked to the end.
- Labels: REAR BUMPER REMOVED 760-800 (25.33-26.67); REAR BUMPER - INSIDE 829-861 (27.63-28.70).

### 8 `v3_fender` (28.946-32.221): -X front quarter, FENDER REMOVED
- Camera: v2 C2 keys, compressed. t0 az -82, el 10, dist 3.6, target [-0.70,-1.40,0.60], lens 30. t 1.09 az -76, el 12, dist 2.6,
  target [-0.70,-1.55,0.58], lens 32. t 3.68 az -70, el 14, dist 1.9, target [-0.70,-1.65,0.55], lens 35 (wheelhouse, headlight
  bucket and mounts fill the frame).
- Objects: **BASE_FE** = car trimmed under the `Fender_outer` + front-bumper footprints + `fender and bumper removed` trimmed to those.
  `front_bumper` hidden. **The hood is the full scan, ON**, because the captured state has the hood on. Do not reuse the hood-removed bay here.
- Fender (translate only, no scanned inside): home at 0.05 → off [-0.85,-0.05,0.80] at 0.85 → off [-1.20,0,1.70] at 1.70 (leaves the top
  of frame cleanly, out and UP into black).
- Label: FENDER REMOVED 904-960 (30.13-32.00).

### 9 `v3_home` (32.221-35.496): reassembly → clean car
- Camera: front 3/4 -X, continuing the lap from the fender. t0 az -55, el 18, dist 6.4, target [0,-0.30,0.70], lens 32 → t 3.67
  az -40, el 13, dist 7.0, target [0,-0.05,0.55]. A slow pull back. The whole car is in frame with ≥ 6 % margin on the first and last frames.
- Objects: **BASE_HOME** = car trimmed under the four part footprints. Each footprint is filled by exactly ONE state, trimmed to it:
  fb ← `front bumper removed`, hood ← `front bumper and hood removed`, fe ← `fender and bumper removed`, rb ← `Rear bumper removed`.
  Island-filtered. The swap-scene states are not in it (doors, fuel door and hatch closed). Start offsets are small (≤ 0.9 m) so
  little exposed base is on screen. All parts move from frame 1: rb [0,0.7,0.35] → home at 1.09 (33.314); fe [-0.6,-0.1,0.9] → home
  at 1.30; hood [0,-0.5,0.9] deg 0 → home at 1.60; fb [0,-0.8,0.35] (nearest the lens) → **locks at 2.181 (34.402)**. Visibility:
  BASE_HOME + parts [0, 2.181 s), full scan [2.181, end]. Land the swap on output frame 1032 by frame-matching and `speed:` (lesson).
- Fallback if seams show on the test frame: drop rb from the reassembly (rear on the full scan) and fill BASE_HOME from the three front footprints only.
- Label: none.

### 10 `logo_small`: reuse `/home/user/media/c5-corvette/logo/logo_small.png` and the v2 timing (35.496-39.40, gone by 38.6).

## v3.4 Diff against v2 (delivered)

| v2 | v3 | why |
|---|---|---|
| a2_open, b_fb_inside, f2_hood, c2_fender, g2_rear, i2_home on the composite `base.blend` | **all re-rendered** on per-section bases | artifacts (reviewer); each composite carried every state at once |
| open starts at 7.2 m | 5.8 m | the car read small in frame 1 |
| hood at az -22, 7.7 s | az **+22**, 5.46 s, same choreography, tighter | the lap continues to +X; room for three new scenes |
| fender 3rd (17.0-22.1) | **8th** (28.946-32.221) | no -X → +X line cross; it hands off into the -X front 3/4 reassembly |
| - | **+ sill, gas cap, trunk** (3 kicks each, swap on the 2nd kick) | reviewer: "gas cap and Doorsill scans, as well as a trunk scan to show off" |
| rear 8.3 s | 4.36 s, same moves, faster | time; both labels kept |
| reassembly rear 3/4, 5.1 s | front 3/4 -X, 3.27 s | follows the fender; shorter ending |
| logo | reused unchanged | - |

Render budget (15 fps, +0.4 s): 68 + 85 + 88 (+~50 in-betweens at 30 fps) + 56 + 56 + 56 + 72 + 56 + 56 ≈ 640 frames. At 12-23 s/frame
with persistent data off, that is ≈ 2.1-4.1 h, one at a time in one chained script (no `pgrep -f` waits). First run 30 % / 8 spp framing strips
(first / swap-1 / swap+1 / last) of all nine shots.

## v3.5 Risks to check on test frames
1. **Swap seams**: on the frame after each swap (476, 574, 672), the trim box must not leave a hole or a double surface where the state
   meets the full scan (sill: B-pillar and roof rail; gas cap: the recess rim; trunk: the hatch frame and the targa rear edge). Compare the
   swap-1 and swap+1 frames: only the region should change, and the rest of the car must not shift by a pixel (same scan, same lighting).
2. **Lighting/luma step at a swap**: `light_ref="base"`. If the base bbox changes, the light rig can move. Pin the light ref to the full
   car for the swap shots. Then the per-frame luma must be smooth across the swap.
3. **Artifacts on the full scan itself** ("when it cuts in"): check frame 1 of the opener and frame 1032 (clean-car swap) for floaters
   and ground scraps under the sills. If present, island-filter the full scan too (components only, no surface trim).
4. **Section bases**: the bay (shot 3), the fender macro (8) and the rear structure (7) must show no ragged edge from a foreign state.
   Each base is made of its own state only.
5. **Gas cap macro at 1.0 m**: scan noise and holes in the recess. If the cap is not in the scan, the label needs another file-backed
   wording. Ask, don't invent.
6. **Trunk**: ragged edge where the glass was. Keep el ≥ 50 at the end. The label band must be black at y 0.86 (luma < 20 at the label box on
   its first and last frames) or get a plate.
7. **Door**: the open door must not hide the sill at the end pose. Adjust az (+105..+125) on the strip.
8. **Hood flip sign** (spin -75 about X): the underside must face the +X front 3/4 lens at local 3.27. Test 1 frame.
9. **Reassembly**: union-base seams at the fb/hood/fender footprint borders, visible at 6.4 m for the first ~1 s. If they show, use the fallback.
10. Cropping per rule A: the whole car with ≥ 6 % margins on shots 1 (frame 1) and 9 (first and last frames). The named section fills the last
    frame of shots 2-8. Nothing clipped by accident (the open door, the parked bumpers, the hood at its peak).
11. `ive director` on the assembly: list the section per shot. The sill and the gas cap are both +X side views a second apart. They must read as
    different subjects (middle vs rear quarter, different el), not as a repeated view.

## v3.6 Open questions for the editor
1. The editlog (06:13, 06:47) excluded a trunk scan "marked not useful by engineering". Is the registered `trunk open` (1.9 mm) that
   file? The reviewer now asks for it, so v3 uses it. Confirm that it is the same car and capture.
2. Does `C5 Gas Cap` contain the cap/filler neck, or only the open fuel door and recess? This decides the shot 5 end framing and whether the
   label stays GAS CAP.
3. Should the full scan get an island filter (risk 3)? The brief says "untouched", but the reviewer asked to delete artifacts "from the full
   car scan".

## v2 (superseded)

### C5 Corvette scan-only reel v2: scene direction (stage 1, scene-director)

2026-11-11. v1 reviewer: *"Same issue as the other first drafts. Need to focus more specifically on the removed areas and
where the useful data is."* This plan applies:
- **The parent's v2 brief:** order from this car's scan features; travel front → side → rear with no ping-pong. When a part comes
  off, the camera stays on that section and moves in on the part's inner face and mounts. Never separate everything in one
  wide shot. Zoom in (the v1 explode filled 10-12 % of the frame). No wasted rotations. Open on the whole car, moving from frame 1.
  Spin a part only when its scanned backside is worth showing, and move parts into clear background, often toward the
  camera. Only show states that have a registered state scan. End with reassembly, a fade, then a SMALL logo. No persistent
  HUD data, and Cycles persistent data off.
- **The newest user feedback, which wins where it conflicts** (lessons.md, bottom, from ferrari-296):
  - CROPPING: whole car in frame on wide shots, and the named section fills the frame on detail shots.
  - REDUNDANCY: each section appears in ONE continuous sequence.
  - BUMPER-REMOVED = HERO BEAT: own section, move in, hold, short factual label over scan shots. This replaces v1's
    "no text" brief, for labels only.
  - OPENINGS ONLY FROM DATA.
- **The re-measured kick-onset grid:** 4.117, 9.309 (drop), 13.689, 15.598 (weak), 17.024, 22.130, 26.471, 30.385, 33.314,
  34.402 (loud kick), 35.496 (biggest hit); music silent by ~39.4 s.

What I looked at: `/home/user/media/work/c5/v2/look/all.png` (state scans raw vs composite), the framing strips
`framing/v2_C.png` (A, B, F, G, H, I) and `framing/v2_A.png` (C, D, E), the v1 sheet `qc/sheet.png`, and the final-quality
frames of `renders/c5/v2_a_fb_off` and `v2_b_fb_inside`. Per-frame luma in both renders is smooth (21→31 and 19→29),
so neither has a lighting dropout.

### 1. Feature inventory (registered data only, one frame)

| region | parts (registered) | removed / open states (registered) | what the data shows (from the renders) | weak data | richness |
|---|---|---|---|---|---|
| **Front: nose / bumper** | `front_bumper` (inside AND outside, 3.8 mm) | `front bumper removed` (2.7 mm) | exposed nose structure behind the bumper (bar across the nose, radiator/headlight-pod area, wiring); the bumper's ribbed inner face | composite trim lines on the closed car at the hood/bumper seam (visible in A frame 1) | **high**: part with an inside, plus a state → hero section |
| **Front: hood / engine bay** | `hood_combo` (car hood skin + the scanned underside); hinge fitted to the open capture (front hinge, axis X at y=-2.01 z=0.86, 46°) | `C5 Supplement Hood Open` (own frame → 2.7 mm, captured 46°); `front bumper and hood removed` (9.9 % overlap, mostly newly exposed engine bay/structure) | hood opening on its real hinge, the scanned hood underside, engine bay from above | the open-hood scan alone looks patchy rotated shut (solved by hood_combo) | **highest**: part with an underside + 2 states + hinge |
| **-X side: front fender** | `Fender_outer` (-X only, **outer skin only**, 2.0 mm) | `fender and bumper removed` (4.1 mm) | inner wheelhouse, headlight bucket, fender mounting rails behind the panel | no +X fender part/state; the fender part has no scanned inside, so it is **translated only, never spun** | **medium**: the value is the exposed structure, not the panel |
| **Rear: bumper** | `rear_bumper_inside` (the only rear bumper part; it carries the inner face, 86-87 % within 15 mm) | `Rear bumper removed` (2.3-5.0 mm) | rear structure behind the bumper, the lamp buckets; the bumper's inner face with lamp and plate recesses | plate recess: check legibility at full res | **medium-high**: part with an inside + state → hero section |
| Top: targa | `targa_reg` (1.6 mm) | **none** (no roof-off scan) | - | - | **excluded** (openings only from data) |
| Trunk, doors | - | **none** (trunk-open scan marked "not useful"; no door-open scan) | - | - | **excluded** |
| Side skirt, lights, door card, interior, underside | own frames, unregistered | - | - | - | **excluded** |
| Exterior signature (quad round tail lamps, hood vents, 5-spoke wheels) | whole car | - | context in the opener and the end frame only | ground scraps under the sills (v1) | context only |

**Where the useful data is:** the front holds three of the four state scans and two parts with scanned insides, so it
gets the opener, the drop and the most seconds. The two **bumper-removed states are hero sections** (front and rear),
each with a move-in, a hold and labels. The fender's value is the structure behind it. The rear closes the travel.

### 2. Scene order (front → -X side → rear → reassembly). One continuous sequence per section

| # | shot id | **section (unique)** | reel time (s) | scans used | feature shown | why here (inventory) | beats | camera note | label (in → out, s) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `v2_a2_open` (NEW) | **front bumper removed** (opens on the whole car) | 0 – 4.117 | car (clean) → base + front_bumper | whole car with margins at frame 1, then the bumper slides out toward camera | opener = richest end (front); the whole car shows from frame 1 | intro | one straight push, front 3/4 -X, 7.2 → 3.0 m | - |
| 2 | `v2_b_fb_inside` (REUSE) | **front bumper removed** (continuous with 1) | 4.117 – 9.309 | base (`front bumper removed`) + front_bumper | bumper rises clear, turns its scanned inside to camera; nose structure readable below it for 5 s | hero beat 1; the bumper is the front part with both faces scanned | intro | head-on push 3.6 → 2.9 m | FRONT BUMPER REMOVED 4.39 → 6.20; FRONT BUMPER - INSIDE 7.73 → 9.15 |
| 3 | `v2_f2_hood` | **hood / engine bay** | **9.309 (drop)** – 17.024 | base (hood-open capture + `front bumper and hood removed`) + hood_combo | hood opens on the real hinge to the captured 46°, lifts off, flips its scanned underside to camera, push into the engine bay | richest region on the biggest moment | 14 | front 3/4 -X, rising push down into the bay | HOOD REMOVED 15.30 → 16.85 |
| 4 | `v2_c2_fender` | **-X side (front quarter)** | 17.024 – 22.130 | base (`fender and bumper removed`) + Fender_outer | fender moves out toward camera into black and exits the top by 20.0; push to the exposed wheelhouse / headlight bucket / mounts and hold | travel continues front → side; translate only (no scanned backside) | 9 | -X side push 3.9 → 1.9 m | FENDER REMOVED 20.05 → 21.95 |
| 5 | `v2_g2_rear` | **rear bumper removed** | 22.130 – 30.385 | base (`Rear bumper removed`) + rear_bumper_inside | bumper slides back toward camera, rises, camera moves in on the exposed rear structure and holds; on 26.471 the bumper turns its inside to camera | hero beat 2; the travel continues -X side → rear on the -X half (no line cross) | 15 | rear 3/4 -X squaring up to straight behind, 4.6 → 3.0 m | REAR BUMPER REMOVED 23.90 → 26.30; REAR BUMPER - INSIDE 27.20 → 30.20 |
| 6 | `v2_i2_home` | **whole car (reassembly)** | 30.385 – 35.496 | base + 4 parts → car (clean) | parts glide home (moving from frame 1), the rear bumper locks on 34.402, swap to the clean scan, fade | ladder end; the rear 3/4 continues the travel | 9 | rear 3/4 -X, pull back 6.6 → 8.4 m (whole car, margins) | - |
| 7 | `logo_small` | - | 35.496 – 39.40 | logo PNG | - | biggest hit; the music decays | - | ~28 % frame width | - |

The whole car appears in shot 1 (an establishing frame inside the front sequence) and shot 6 (the reassembly payoff). No
other section is repeated.

### 3. Music map (re-measured kick onsets)

| cut point | role |
|---|---|
| 0 | shot 1 (0.4 s fade-up; the push is already moving) |
| 4.117 | cut on action → shot 2 (bumper already off) |
| **9.309 drop** | shot 3: the hood starts opening on the kick |
| 13.689 | in shot 3: the hood is clear of the bay, starts flipping its underside to camera |
| 15.598 (weak) | in shot 3: the push into the engine bay is under way (not a cut) |
| **17.024** | shot 4: the fender starts moving on the cut |
| **22.130** | shot 5: the rear bumper starts sliding on the cut |
| 26.471 | in shot 5: the rear bumper starts turning its inside to camera |
| **30.385** | shot 6: reassembly |
| 33.314 | in shot 6: hood, front bumper and fender are home |
| 34.402 loud kick | in shot 6: the rear bumper locks home; swap to the clean car |
| **35.496 biggest hit** | small logo |
| ~39.40 | end (music silent) |

### 4. Diff against the current v2 draft timeline (project.yaml)

| v2 draft | v2 final | why |
|---|---|---|
| A `v2_a_fb_off` (reuse) | **re-render as `v2_a2_open`** | CROPPING: frame 1 clips the car's tail at the left edge (bright pixels in column 0; car x 0-596 of 810), so the whole car is not in frame. Composite seams also show on the "closed" car. New: start at 7.2 m on the clean car and end on A's exact end pose, so the cut into B is unchanged |
| B `v2_b_fb_inside` | **reuse unchanged**, 4.117-9.309 (5.192 s of the 5.75 s render) | content right, luma clean |
| C fender on the drop | **moved after the hood** to 17.024, merged with D | ping-pong (front → side → front); the drop goes to the richest region |
| D fender macro | **dropped (merged into C2's push)** | same section twice |
| E nose macro | **dropped** | same section as B |
| F hood | **moved to the drop**; the hood now flips its scanned underside to camera | richest data on the biggest moment; in the draft the hood floated skin-up (strip F), so the underside data was never seen |
| G rear off (az +152, +X) + H rear inside (az 178) | **merged into one held shot `v2_g2_rear`** on the -X half | same section twice; +X after a -X shot crossed the line |
| I home (front 3/4) | **`v2_i2_home`** rear 3/4 -X, parts moving at frame 1, fade 34.75-35.496 | continue the travel; the draft opened on every part off at once |
| logo `end_card.png` (52 % width, 3.9 s) | **small logo** ~28 % width, ~2.3 s at full | "small logo", "last scenes held too long" |
| no text | **6 labels** (above) | new user feedback (hero beat labels), scan shots only |

### 5. Open questions / checks for the editor
1. `tools/shot.py` line 209 hard-codes `sc.render.use_persistent_data = True`, so the `persistent=False` key that `v2shot()` writes is
   **ignored**. Change it to `spec.get("persistent", True)` before rendering (required: persistent data OFF).
2. Hood flip sign: verify with a 1-frame 30 % test at hood local t = 5.70 s. The scanned underside (dark backface, hinge brackets) must face the lens.
3. Rear plate: check the plate recess on the rear bumper inner face and the rear base at full res; deplate if any character is legible.
4. Label wording: only the file-backed phrases above. No component names: nothing in the renders identifies a crash beam
   with certainty, so "crash beam" is not used.
5. The hood scene shows the -X fender ON with the hood and bumper off, which is exactly the captured
   `front bumper and hood removed` state. That is why the hood comes before the fender.

### 6. As delivered (v2 final)
| shot | frames | section | covers |
|---|---|---|---|
| v2_a2_open | 0-122 | whole | clean car from 7.2 m, push to the nose; front bumper starts off at 1.2 s |
| v2_b_fb_inside | 123-278 | front | FRONT BUMPER REMOVED: nose structure; the bumper rises and turns its scanned inside |
| v2_f2_hood | 279-507 | front | hood opens on the fitted hinge (46 deg), lifts, flips its underside, exits top; HOOD REMOVED bay |
| v2_c2_fender | 508-663 | side (-X) | FENDER REMOVED: wheelhouse / mounts macro |
| v2_g2_rear | 664-908 | rear | REAR BUMPER REMOVED: structure hold; bumper turns its scanned inside |
| v2_i2_home | 909-1064 | whole | everything returns; clean car on 34.402 (frame 1032); fade |
| logo | 1065-1180 | - | small logo on 35.496 |

Cut retime after the first assembly: 124/511/912 → 123/508/909 (double kick; see lessons.md). `ive director` repeated-view
pairs are silhouette false positives (every section appears once).
