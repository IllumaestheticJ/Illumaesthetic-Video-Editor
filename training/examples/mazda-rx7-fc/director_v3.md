# Mazda RX-7 FC3S - shot plan v3 (director, stage 2, 2026-11-13)

Keeps the scene order of `direction_v3.md` (stock opener -> real removals from the drop -> HertLife kit on, front -> sides ->
rear -> finished widebody on the bar-14 downbeat -> mobile CTA -> logo). Music `music_v3.json`: 90 BPM, beat 0.6667, bar
2.6667, excerpt 48.0 s, drop at 5.333; snares on beats 2 and 4 (downbeat + 0.667, + 2.000).

Frame: prepped scan frame, m, front = +Y, car's right = +X, z up. Keys follow tools/shot.py: part `loc` = offset in m,
`rot` = XYZ deg about the pivot (default bbox centre), `ease` applies to the segment ENDING at that key, `t` in s from the
shot start. Parts listed with no keys are loaded static at home. Hood/k_hood pivot = hinge.json `p`
(0.6076, 0.6348, 0.9749), open = rot X +44.42 (hood.blend convention). Render specs for all NEW shots: house silver,
exposure -0.5, 15 fps, 1080x1920 res_pct 75, samples 12, persistent data OFF, seconds 5.533 (80 frames to the cut + 3).

## Prep before any render (no Blender render)
1. Split `k_canards` and `k_sidesplit` by the sign of x into `k_canards_l/_r`, `k_sidesplit_l/_r` (two disconnected halves
   each; no new geometry) so each half leaves/arrives along its own side. Kit in silver (house look; direction_v3 Q6).
2. Kit-on-base clash checks (red-over-silver stills, regcheck.sh style): (a) stock pop-up lids in comp_explode_dp vs k_hood
   closed - if lids poke through, remove base triangles inside k_hood's footprint above z 0.70 that are within 40 mm under
   k_hood; (b) stock exhaust in comp_explode_dp vs k_diffuser/k_exhaust; (c) stock rear bumper corners vs k_side tails (c7).
3. `pathcheck.py` (lamborghini-revuelto) on every NEW shot's part paths; fallbacks are given per shot.
4. Re-capture the listing with the broken "Marker" widget hidden (it shows bottom-right in listing_mobile.png), same viewport.
5. Solve the listing viewer's camera (mazda-miata-nd/tools/solve_listing.py, search all 360 deg az) against the c10 scene
   (comp_explode_dp + all kit). Expected: rear-left 3/4, slightly high (~az -135, el ~15-20 deg).

## Shot table
| section | shot | start-end (s) | focus | camera | part action | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| WHOLE (stock) | c1 `s1_front34_pad` | 0.000-5.333 | whole stock car, nose leading | v2 low front-right turntable, frames 1-41 (scaled 0.88 + padded, 12 % margins), src_fps 7.36 | - | whole stock car moving from frame 1 over the 2-bar lead-in | REUSE |
| HOOD / BAY | c2 `s6_hood` | 5.333-8.000 | hood opens on its hinge | v2 orbit; `in` 0.733 (hood started at 0.567 -> moving at the cut), src_fps 15 | hood 0 -> 44.42 deg, open at 7.600 | the transformation starts ON the drop with real data (Hood Up) | REUSE |
| HOOD / BAY | c3 `s9_hoodoff` | 8.000-10.667 | captured open hood lifts off; engine bay | v2; `in` 0.533 (= s6's end pose, invisible join), src_fps 15 | hood lifts 8.034, out of the top by 10.27 | real Hood Up panel + Hood Off bay | REUSE |
| FRONT BUMPER REMOVED | c4 `s10_fbumper` | 10.667-13.333 | front bumper off its mounts, scanned inner face | v2 low front-right; all 36 frames, src_fps 12.65 | bumper off + tip, completes at the cut | rule C; inside is scanned | REUSE |
| FRONT BUMPER REMOVED | c5 `s11_fsupport` | 13.333-16.000 | radiator support, crash beam, brackets | v2 push; `in` 0, src_fps 15, keep v2 vf pad shift (down 20 %) | stock bumper sinks out below | hero hold with labels | REUSE |
| FRONT (kit) | c6 NEW `k_front` | 16.000-21.333 | headlights, front bumper, splitter, canards, vented hood go on | front-LEFT 3/4 mid-high. t0 loc (-3.05, 5.25, 1.75) target (-0.05, 1.45, 0.62) f32; t5.533 loc (-2.35, 5.15, 2.45) target (0.00, 1.40, 0.62) f32 inout. Front section 83-85 % of width | see c6 keys | richest region's payoff; each part lands on a beat; not s10/s11's front-right | NEW 83 fr |
| SIDES (kit) | c7 NEW `k_sides` | 21.333-26.667 | both overfender skins + side splitters; the car widens | high front-centre, car length up the frame. t0 loc (0.00, 6.40, 5.40) target (0.00, -0.30, 0.50) f50 (el ~36 deg, d 8.3); t5.533 loc (0.45, 5.90, 5.00) target (0.00, -0.35, 0.50) f50 inout. Kit front ~80 % width at the end | see c7 keys | no side removal data -> kit over stock; only a centred high view shows both sides widening | NEW 83 fr |
| REAR BUMPER REMOVED | c8 NEW `k_rbumper_off` | 26.667-32.000 | rear bumper off, then crash beam + mounting points | s12's path re-timed: t0 loc (2.60, -4.60, 1.15) target (0.10, -1.55, 0.72) f30; t1.333 (2.35, -4.55, 1.05) -> (0.20, -1.75, 0.70) inout; t3.333 (1.10, -4.45, 0.80) -> (0.30, -2.05, 0.68) inout; t5.533 (0.95, -4.30, 0.78) -> (0.30, -2.05, 0.66) lin | see c8 keys | rule C hero; s12 can't be reused (shows stock fenders after the kit sides went on) | NEW 83 fr |
| REAR (kit) | c9 NEW `k_rear` | 32.000-37.333 | rear bumper, diffuser, tips, GT wing | t0 = c8 t5.533 pose (invisible join); t2.0 loc (2.10, -5.00, 1.60) target (0.15, -1.60, 0.72) f30 inout; t4.667 loc (2.90, -5.40, 2.30) target (0.05, -1.20, 0.78) f30 inout; hold to 5.533. Rear section fills; the nose runs out of the left edge deliberately (detail shot) | see c9 keys | build completes on the 36.667 snare | NEW 83 fr |
| WHOLE (kit) | c10 NEW `k_reveal` | 37.333-42.667 | the finished widebody, every replaced panel | rear-left orbit about (0, -0.10): t0 loc (-1.71, -6.48, 1.10) target (0, -0.10, 0.60) f34 (az -165, r 6.6); t5.067 loc (-5.23, -5.33, 2.30) target (0, -0.10, 0.55) f30 inout (az -135, r 7.4) = PLACEHOLDER for the solved listing pose (prep 5); hold to 5.533. If the solved az differs, start = solved az - 30 deg, same r/h start. Car 76 % -> ~86 % width | none (all static) | final reveal on the bar-14 downbeat; rear-left = never the opener's low front-right; ends on the listing pose for the CTA | NEW 83 fr |
| CTA | c11 | 42.667-46.000 | FC3S scan listing on a phone | tools/cta_card.py: c10 last frame -> listing 360 viewer, `--secs 3.333`, title = listing h1 "MAZDA RX7 (FC3S) 3D SCAN", URL illumaesthetic.com/products/mazda-rx7-3d-scan-1985-1992 | - | user request; see direction_v3 Q2/Q3 | card |
| - | c12 logo | 46.000-48.000 | ILLUMAESTHETIC | tools/logo_card.py at 760 px wide, centred, on the render black (4,4,5); fade in 0.3 s | - | newest lesson (760 px) | card |

### c6 `k_front` - base comp_explode_dp; static: rbumper.blend (stock rear stays until c8)
Drops come from above, fully out of the top of frame, in front of the nose (clear black), then slide back onto the mounts
along -Y (the direction they bolt on). 16.000 + t:
- k_lights: t0 (0, 0.70, 3.60) -> t0.667 (0, 0.70, 0) out -> t1.333 (0, 0, 0) inout [lands 17.333]
- k_fbumper: t0 (0, 1.00, 3.60) hold to t0.667 lin -> t1.333 (0, 1.00, 0) out -> t2.000 home inout [18.000 snare]
  (lights first, then the bumper slides over them: no housing passes through the openings)
- k_splitter: t0 (0, 1.10, 3.60) hold to t1.333 -> t2.000 (0, 1.10, -0.15) out -> t2.400 (0, 0, -0.15) inout -> t2.667 home out
  [18.667 downbeat] (passes UNDER the bumper's lower lip, then rises 0.15)
- k_canards_r / _l: t0 (+-1.00, 0.40, 3.60) hold to t2.000 -> t2.500 (+-1.00, 0.40, 0) out -> t3.333 home inout [19.333 snare]
- k_hood (pivot hinge p): t0 loc (0, 0, 3.60) rot (44.42, 0, 0) hold to t2.667 -> t3.667 loc 0 rot (44.42, 0, 0) out ->
  t4.667 loc 0 rot (0, 0, 0) inout [closes on the 20.667 snare] -> hold to 5.533 lin. Fallback if the kit hood does not sit on
  the stock hinge (check the closed pose against k_hood's own home): drop straight to home, no rotation.

### c7 `k_sides` - base comp_explode_dp; static: k_lights, k_fbumper, k_splitter, k_canards_l/_r, k_hood, rbumper.blend
Halves come in along +-X from fully outside the frame (rear half-width at start ~2.0 m). 21.333 + t:
- k_sidesplit_r / _l: t0 (+-1.60, 0, 0) hold to t0.667 lin -> t2.000 home inout [23.333 snare] (strip y -0.85..0.88 runs
  between the tyres; pathcheck)
- k_side_r / k_side_l: t0 (+-1.60, 0, 0) hold to t2.000 lin -> t3.333 home inout [24.667 snare] -> hold to 5.533
- Fallback if pathcheck hits the canards: via (+-1.60, -0.25, 0) -> (+-0.0, -0.25, 0) at t3.0 -> home t3.333.

### c8 `k_rbumper_off` - base comp_explode_dp; static: all front kit, k_side_l/_r, k_sidesplit_l/_r
- rbumper.blend (stock, outer skin -> translate only): t0 home -> t0.667 home lin -> t1.333 (0, -0.60, 0) out [28.000] ->
  t2.000 (0.10, -1.00, -1.20) inout [28.667 snare, below the frame] -> t5.533 (0.10, -1.02, -1.25) lin.
- Checks: the right overfender (now 10 cm wider) inside the right edge at t0 (>= 20 px; else pull the t0 camera back 0.3 m
  along its ray); at t3.333+ the k_side_r tail must not hide the beam's right bracket (else camera x 1.10 -> 0.70).

### c9 `k_rear` - base comp_explode_dp; static: all front kit, sides, side splitters
Rear parts arrive from below-behind (out of frame, the stock bumper's exit pose mirrored) and slide +Y onto their mounts.
32.000 + t:
- k_rbumper: t0 (0.10, -1.00, -1.20) -> t1.333 (0, -0.60, 0) out -> t2.000 home inout [34.000 snare]
- k_diffuser: t0 (0, -1.00, -1.30) hold to t2.000 lin -> t2.667 (0, 0, -0.35) out -> t3.333 home inout [35.333 snare]
  (slides in under the bumper at -0.35, then rises: a straight +Y slide at home height would cut through the bumper)
- k_exhaust: t0 (0, -1.00, -1.30) hold to t2.667 lin -> t3.333 (0, -0.45, 0) out -> t4.000 home inout [36.000] (tips slide
  forward through the diffuser exits; pathcheck tolerance on the exit openings)
- k_wing: t0 (0, 0, 3.40) hold to t3.333 lin -> t4.667 home inout [36.667 snare] (straight down onto the hatch mounts; fully
  above the frame until 3.333) -> hold to 5.533

### c10 `k_reveal` - base comp_explode_dp + all kit parts static (k_lights, k_fbumper, k_splitter, k_canards_l/_r, k_hood,
k_side_l/_r, k_sidesplit_l/_r, k_rbumper, k_diffuser, k_exhaust, k_wing). Nothing moves; the camera carries the reveal.

## On-screen labels (ScanHUD `label`, plain names only, no numbers, max two, top-left black 80 px in, non-empty sub)
| shot | label (sub) | in -> out (s) |
|---|---|---|
| c3 | ENGINE BAY | 9.333 -> 10.450 (check against the leaving hood at 10.0) |
| c4 | FRONT BUMPER REMOVED | 11.333 -> 13.100 |
| c5 | RADIATOR SUPPORT | 14.000 -> 15.800 |
| c5 | CRASH BEAM | 14.667 -> 15.800 |
| c6 | FRONT BUMPER (HEADLIGHTS / SPLITTER) | 18.000 -> 19.267 |
| c6 | VENTED HOOD (CANARDS) | 20.000 -> 21.133 |
| c7 | OVERFENDERS (SIDE SPLITTERS) | 24.667 -> 26.433 |
| c8 | REAR BUMPER REMOVED | 27.333 -> 28.567 |
| c8 | CRASH BEAM | 29.333 -> 31.800 |
| c8 | MOUNTING POINTS | 30.000 -> 31.800 |
| c9 | REAR BUMPER (DIFFUSER) | 34.000 -> 35.267 |
| c9 | GT WING | 36.000 -> 37.133 |
No labels on c1, c2, c10, CTA, logo. No kit brand name until the user confirms it (direction_v3 Q4).

## Timeline (frames = round(t*30); cut-only; use honda-s2000 tools/concat_assemble.py with exact frames, or ive assemble
with the first clip one frame short; measure every cut on the decoded file)
| clip | src | src_fps | in | frames | cut at frame |
|---|---|---|---|---|---|
| c1 | renders/s1_front34_pad (41) | 7.36 | 0 | 160 | 160 |
| c2 | renders/s6_hood | 15 | 0.733 | 80 | 240 |
| c3 | renders/s9_hoodoff | 15 | 0.533 | 80 | 320 |
| c4 | renders/s10_fbumper (36) | 12.65 | 0 | 80 | 400 |
| c5 | renders/s11_fsupport (+ v2 vf shift) | 15 | 0 | 80 | 480 |
| c6 | renders/k_front | 15 | 0 | 160 | 640 |
| c7 | renders/k_sides | 15 | 0 | 160 | 800 |
| c8 | renders/k_rbumper_off | 15 | 0 | 160 | 960 |
| c9 | renders/k_rear | 15 | 0 | 160 | 1120 |
| c10 | renders/k_reveal | 15 | 0 | 160 | 1280 |
| c11 | CTA card | - | 0 | 100 | 1380 |
| c12 | logo card 760 px | - | 0 | 60 | end 1440 (48.0 s) |
All renders `interpolate: true` (minterpolate). Tag every clip with `section` / `focus` as in the shot table; run
`python -m ive director` on the v3 project.yaml after assembly. Expected, intended pairs: c2~c3 (one move split at the hood
swap) and c8~c9 (one move split at the bumper change) - log them; anything else flagged gets cut.

## Cut list (v2 -> v3)
- s4_nose, s3_wheel, s5_mirror: stock details with no place in a 2-bar lead-in / not changed by the kit; wheel hub holes.
- s12_rbumper: shows stock fenders after the kit sides are on -> re-rendered as c8 with the kit present.
- s13_reassemble: puts the STOCK panels back - contradicts the request; replaced by c10.
- v2 small logo (378 px) -> 760 px.

## Hold list (> 0.75 s)
| where | length | reason |
|---|---|---|
| c1 | 5.33 s | the whole stock car, slow turn over the soft lead-in (moves throughout) |
| c5 | 2.67 s | push onto the radiator support / crash beam, two labels (rule C) |
| c7 24.667-26.667 | 2.0 s | finished front + widened sides read while the camera keeps pushing; OVERFENDERS label |
| c8 28.667-32.000 | 3.33 s | push onto the crash beam + mounting points, two labels (rule C) |
| c10 | 5.33 s | the finished car; orbit into the listing pose, never static |
| c12 | 2.0 s | logo |

## Checks before assembly (lessons)
- Preview each NEW shot first/mid/last at 30 % (~15 s) before finals; then per-frame luma scan of every folder (dropouts).
- Edge margin over ALL frames >= 20 px for every part (bright-pixel bbox); parked/arriving parts fully in or fully out.
- Pathcheck all c6/c7/c9 part paths (ignore hits within 10 cm of home).
- c4 (s10) uses comp_explode_dp: confirm the missing stock rear bumper is not visible behind the car in any used frame (v2 passed).

## Render budget
NEW: c6, c7, c8, c9, c10 = 5 x 83 = **415 frames ~ 2.3 h** at ~20 s/frame, one job at a time, resumable, in shot order.
Reused unchanged: s1_front34_pad, s6_hood, s9_hoodoff, s10_fbumper, s11_fsupport (windows/speed only). Not used: s2, s3, s4,
s5, s7, s8, s12, s13.
