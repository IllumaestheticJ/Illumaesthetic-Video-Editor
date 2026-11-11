# Mazda RX-7 FC3S — shot plan v2 (director, stage 2, 2026-11-11)

Keeps the scene order in `direction.md` (travel front -> side -> rear, each section once, progressive explode, reassembly,
fade, small logo). Sources: lessons.md, style-guide, Temerario notes (training/references/README.md), sibling v1 feedback,
user v2 brief + addendum, contact sheets of every render, `ive director` report (`/tmp/rx7dir/director_report.md`: s1~s2
repeated view, dead frames in s1 and s8, no `focus` tags).

Frame: prepped scan frame in metres, front = +Y, car's right = +X, z up; car x +-0.895, y +-2.152, z 0.04-1.38.
Portrait width at focal f (20.25 mm sensor) = 20.25/f x distance (30 mm: 0.675 d, 32 mm: 0.633 d, 40 mm: 0.506 d).
Part keys follow tools/shot.py: `loc` offsets in m, `rot` XYZ degrees about the part's pivot, `ease` applies to the segment
ending at that key, times in seconds from the shot start. Hood rot uses the **hood.blend convention** (closed skin about
`hinge.json` p, open = +44.42 deg); for the captured Hood Up panel subtract 44.42.

## Shot table

| section | shot | start-end (s) | focus | camera | part action (absolute beat times) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| WHOLE | c1 `s1_front34` | 0.000-4.533 | whole car, nose leading | low front-right 3/4 turntable 18 -> ~30 deg, f30 (v1 spec). Frames 1-41 only (t <= 2.67 s; nose touches the edge from 2.93 s). **Post reframe:** scale 0.88 (810x1440 -> 713x1267), pad back to 810x1440 at x=5, y=86 -> car 56 % width at frame 1, 76 % at frame 41, ~12 % margin both sides, vertically centred | — | addendum A/brief 5: whole car, deliberate margins, moving from frame 1 | **reuse** (window + pad, no Blender) |
| FRONT | c2 `s4_nose` | 4.533-9.067 | pop-up lids (down), indicators, bumper face | v1 slide across the nose, f38 | — | the Front Face on the car before it comes off; section fills the frame | **reuse**, slowed |
| HOOD / BAY | c3 `s6_hood` | 9.067-12.463 | hood opening on its hinge | v1: orbit r3.9 -> 3.4, 34 -> 18 deg, h 2.0 -> 2.4, f30 | hood 0 -> 44.42 deg 9.63 -> 11.90 (k1 -> k5 snares) | real Hood Up end pose; drums enter | **reuse** 0-3.40 s |
| HOOD / BAY | c4 `s9_hoodoff` | 12.463-16.426 | hood lifts off; engine bay from above | t0 = s6's camera at 3.40 s: loc (1.076, 4.331, 2.391) target (0, 1.098, 0.60) f30; hold to t0.567; t3.963 loc (0.70, 3.70, 2.75) target (0.0, 1.25, 0.85) f30 inout; hold to 4.2. End: d 3.1 m -> 2.1 m wide, bay (1.6 m between fenders) fills ~76 %; lifted hood sits ~25 deg above centre, against black above the roofline | base comp_hood; part **hood_up panel** (see prep), pivot hinge p. Keys (hood.blend convention): t0 rot (44.42,0,0) loc 0; t0.567 same (13.030); t1.699 loc (0,-0.10,0.60) rot 44.42 ease out (14.162); t2.831 loc (0,-0.18,1.00) rot (25,0,0) inout (15.294); t4.2 loc (0,-0.20,1.05) rot (23,0,0) lin. Translate/settle only (skin-only part, no flip). | hood off is a captured state; the move into the bay replaces the top-down with real data; joins s6 seamlessly (same camera, same hood pose) | **NEW** 64 fr |
| FRONT BUMPER REMOVED | c5 `s10_fbumper` | 16.426-18.691 | front bumper coming off, inner face | t0 loc (1.25, 5.70, 1.30) target (0.0, 2.30, 0.55) f30 (d 3.7 -> 2.5 m wide, car front 72 %); t2.265 loc (0.75, 5.10, 1.85) target (0.0, 2.85, 0.45) f30 inout (d 2.75 -> 1.86 m wide, bumper 83 %); hold to 2.4 | base comp_explode; part fbumper (pivot = bbox centre ~(-0.03, 1.98, 0.53)). t0 home; t0.10 home; t1.133 loc (0, 0.55, 0) ease out (17.559, straight off its mounts toward the lens); t2.265 loc (0, 1.27, -0.18) rot (-110, 0, 0) inout (18.691): inner face turns up to the camera; ends in clear black below/in front of the car (sightline behind it passes under the car). | inner face IS scanned (93 % bins) -> the flip shows real data | **NEW** 37 fr |
| FRONT BUMPER REMOVED | c6 `s11_fsupport` | 18.691-21.521 | radiator support + lower crash beam + brackets | t0 loc (1.15, 3.95, 1.05) target (0.10, 1.88, 0.62) f30 (d 2.36 -> 1.6 m wide); t2.83 loc (0.45, 3.45, 0.95) target (0.30, 1.90, 0.58) f30 inout (push onto the right upright + beam bracket, d 1.6 -> 1.1 m wide); hold to 3.0 | same scene: fbumper parked t0 loc (0, 1.27, -0.18) rot (-110) -> t3.0 loc (0, 1.30, -0.20) rot (-112) lin (out of frame below: 35 deg under the view axis) | hero beat (addendum C): what is behind the bumper, held 2.8 s with labels | **NEW** 46 fr |
| WHEELS | c7 `s3_wheel` | 21.521-23.220 | tyre sidewall, rim face, arch | v1 slide toward the nose, f48 | — | travel off the front corner; speckled-hub frames (t < 1.47) skipped | **reuse** in 1.47 |
| SIDE | c8 `s5_mirror` | 23.220-24.352 | mirror, A-pillar, door | v1 glide, f40 | — | only side detail; cowl/glass speckle frames skipped | **reuse** in 2.27 |
| REAR BUMPER REMOVED | c9 `s12_rbumper` | 24.352-28.881 | rear bumper off, then crash beam + mounting points | t0 loc (2.60, -4.60, 1.15) target (0.10, -1.55, 0.62) f30 (rear-right 3/4, d 4.0 -> 2.7 m wide, rear end fills); t2.264 loc (2.30, -4.55, 1.05) target (0.10, -1.75, 0.60) inout; t4.30 loc (1.10, -4.45, 0.80) target (0.10, -2.05, 0.55) f30 inout (d 2.6 -> 1.76 m wide; beam x -0.79..0.85 fills ~93 %); hold to 4.7 | base comp_explode; part rbumper (pivot ~(0.04, -1.845, 0.56)). t0 home; t1.132 home (25.484); t2.264 loc (0, -0.60, 0) ease out (26.616, straight back off its mounts toward the lens); t3.396 loc (0.30, -1.15, -0.42) inout (27.748, down and right, 0.37 m under the sightline to the beam, black behind it); t4.7 loc (0.31, -1.18, -0.44) lin. **Translate only** (skin-only part). | the rear's only state; crash beam held ~2.1 s to read | **NEW** 71 fr |
| WHOLE (reassembly) | c10 `s13_reassemble` | 28.881-33.409 | all three parts fly home, clean car, fade | high rear-right, car length runs up the frame. t0 loc (2.20, -7.00, 5.00) target (0.0, 0.30, 0.50) f40 (d 8.85 -> 4.5 m wide; car 66 %, parked parts inside +-19 deg of the 24 deg half-height); t4.53 loc (1.60, -5.90, 3.90) target (0.0, 0.0, 0.45) f40 inout (d 7.0 -> 3.55 m wide, car 2.86 m = 81 %, ~9.5 % margins); hold to 4.7 | base comp_explode + parts from their parked poses. rbumper: t0 (0.30,-1.15,-0.42) hold to t0.566 (29.447) -> home t1.698 (30.579) inout. fbumper: t0 loc (0,1.30,-0.20) rot (-112) hold to t1.132 (30.013) -> t2.264 loc (0,0.55,0) rot 0 (31.145) -> home t2.830 (31.711). hood (hood.blend, hinge pivot): t0 loc (0,-0.20,1.05) rot (23) hold to t1.698 -> home loc 0 rot 0 at t3.396 (**32.277 lock**, the v1 lock hit). Frames t >= 3.40 render with base **car4.blend only** (clean car, c5 lesson). Post: fade to black 32.843 -> 33.409. | Temerario: reassembly after the progressive explode, then fade; rear-first order = we are at the rear | **NEW** 71 fr |
| — | c11 `logo` | 33.409-37.400 | ILLUMAESTHETIC | rebuild card (tools/logo_card.py) at ~35 % frame width (378 px of 1080), centred; fade in 0.4 s from black; music fades by 37.4 | — | small logo (v1 card is 82 % width) | rebuild (no Blender) |

All new renders: house silver look, exposure -0.5, 15 fps, 1080x1920 @ res_pct 75, samples 12, **persistent data off**
(every animated-part lesson), per-frame mean-luma scan after each. Preview each first (first/mid/last at 30 %) and check:
nothing clipped, parts against black, label zones empty.

### Prep before rendering (no Blender render involved)
- `hood_up.blend`: the captured open hood = hup triangles within 8 mm of hood_v2 rotated by the hinge (axis/angle from
  hinge.json), largest island; pivot = hinge p. Used only in c4. Red-over-silver still at t0 against s6's last frame to confirm
  the swap is invisible.
- s1 reframe: ffmpeg `scale=713:1267,pad=810:1440:5:86:black` over f_0001-f_0041 into renders/s1_front34_pad.
- Optional, see open question 1 in direction.md: deplate rbr before c9.

### On-screen labels (addendum C; ScanHUD `label`, Inter Display +6 tracking, #e8ecf2, max two on screen, 80 px inside the
edges, in the black outside the silhouette, above the bottom 20 %; enter on a beat, leave >= 0.2 s before the cut)
| shot | label | in -> out (s) | where |
|---|---|---|---|
| c4 | ENGINE BAY | 14.728 -> 16.200 | top-left black (check against the frame at 15.5 s; the lifted hood is upper centre-right) |
| c5 | FRONT BUMPER REMOVED | 16.992 -> 18.450 | top-left |
| c6 | RADIATOR SUPPORT | 19.257 -> 21.300 | top-left, line 1 |
| c6 | CRASH BEAM | 19.823 -> 21.300 | top-left, line 2 |
| c9 | REAR BUMPER REMOVED | 26.050 -> 27.100 | top-left |
| c9 | CRASH BEAM | 27.182 -> 28.650 | top-left, line 1 |
| c9 | MOUNTING POINTS | 27.748 -> 28.650 | top-left, line 2 (the four slotted mounts + end brackets on the beam) |
No labels on c1-c3, c7, c8, c10, logo. Each label names only what the splats show (`/tmp/rx7dir/hobo_front.png`,
`rbr_rear.png`); no numbers on screen. The finned unit on the car's left is not named.

### Timeline (frames = round(t*30); first clip one frame short; total 1121 + hold frame = 1122 = 37.4 s)
| clip | src | src_fps | in | dur | frames | cut at |
|---|---|---|---|---|---|---|
| c1 | renders/s1_front34_pad (41 fr) | 8.70 | 0 | 4.5000 | 135 | 136 |
| c2 | renders/s4_nose (54 fr) | 11.44 | 0 | 4.5333 | 136 | 272 |
| c3 | renders/s6_hood | 15 | 0 | 3.4000 | 102 | 374 |
| c4 | renders/s9_hoodoff | 15 | 0 | 3.9667 | 119 | 493 |
| c5 | renders/s10_fbumper | 15 | 0 | 2.2667 | 68 | 561 |
| c6 | renders/s11_fsupport | 15 | 0 | 2.8333 | 85 | 646 |
| c7 | renders/s3_wheel | 15 | 1.47 | 1.7000 | 51 | 697 |
| c8 | renders/s5_mirror | 15 | 2.27 | 1.1333 | 34 | 731 |
| c9 | renders/s12_rbumper | 15 | 0 | 4.5000 | 135 | 866 |
| c10 | renders/s13_reassemble | 15 | 0 | 4.5333 | 136 | 1002 |
| c11 | logo_card (small) | — | 0 | 4.0000 | 120 | end 1122 |
All `interpolate: true` except the logo. src_fps for stretched clips = (N-1)/(dur+0.1) (minterpolate tail lesson). Tag every
clip with `section`/`focus` as in the shot table so `ive director` reports coverage. Measure cuts on the delivered file.

## Cut list (v1 -> v2)
- s2_rear34 (4.53-9.07): repeated view of s1 (`ive director` IoU 0.75 / corr 0.81); the rear gets c9.
- s7_top (18.69-21.52): rotating top-down; most of the frame is the rear-glass hole; nothing new.
- s8_explode (21.52-33.41): all three parts separate at once in a wide orbit (car 60-93 % width, 0.9 s dead frames, ~5.7 s of
  drift orbit); replaced by c4, c5, c6, c9, c10.
- s1 frames 42-75: nose clipped by the frame edge; also 0.8 s of dead frames flagged by `ive director`.
- s3 frames 1-21 (speckled hub/tread), s5 frames 1-33 (cowl/windscreen holes), s4 middle-only trim removed (whole render used).
- v1 logo card at 82 % width.

## Hold list (> 0.75 s)
| where | length | reason |
|---|---|---|
| c1 (whole clip, slowed turntable) | 4.5 s | opener: the whole car must read; slow motion over the soft intro, it never stops |
| c4 15.29-16.43 | 1.13 s | hood parked in black, camera still drifting over the bay; ENGINE BAY label read time |
| c6 whole shot | 2.83 s | slow push onto the radiator support/crash beam; hero beat, two labels |
| c9 26.62-28.88 | 2.26 s | push onto the crash beam and mounting points; two labels |
| c10 32.28-33.41 | 1.13 s | clean car locked, then fade to black (0.57 s each) |
| c11 | 4.0 s | logo over the music tail (last hit 36.10, quiet 36.6) |

## Render budget
New frames at 15 fps: c4 64 + c5 37 + c6 46 + c9 71 + c10 71 = **289 frames ~ 58 min** at ~12 s/frame, one job at a time,
in this order (c4, c5, c6, c9, c10). Chain them in one script, wait on the PID. Reused unchanged: s3, s4, s5, s6 (time windows
only) and s1 (window + pad). Not used: s2, s7, s8.
