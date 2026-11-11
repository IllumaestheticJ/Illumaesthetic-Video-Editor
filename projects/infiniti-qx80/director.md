# Infiniti QX80 v2 - shot plan (director, stage 2; keeps the scene order in direction.md)

Frame: prepped metres, nose +Y, car's right +X, z up; car x +-1.08, y +-2.68, z 0..1.94. Hood hinge pivot
[0.0609, 1.2197, 1.2671], rotation about +X, open = +37.19 deg. Music t = video t + 0.66. Cut frame = round((t-0.66)*30).
`ive director` (director_report.md) on v1 flagged: no focus tags, s1~s2 and s1~s5 same view, 2.1 s dead in s7, 3.8 s
static logo. All addressed below; tag every clip with `section:` and `focus:` in project.yaml v2.

## Shot table
| section | shot | music in-out (video frames) | focus | camera | part action (music t) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | **N0_open** | 0.66-5.962 (0-158, 158 f, first clip 1 f short) | whole car | orbit about car centre: r 7.6 -> 7.0 m, az 48 -> 30 deg (0 = +Y), z 1.05 -> 1.00, target (0,0.2,0.9) -> (0,0.5,0.9), 32 mm, eased; whole car in frame every frame | - | the only whole-car exterior; nose turns toward camera across the intro | NEW 82 f (secs 5.47), src_fps 15.09 |
| front | s3_grille | 5.962-8.562 (159-236, 78 f) | grille fins + badge | as rendered | - | signature feature at a scale N0 can't show | reuse, src_fps 11.85 (32/2.7) |
| front/side | s4_wheel | 8.562-11.162 (237-314, 78 f) | RF wheel + fender vent | as rendered | - | wheel spokes resolve; vent planted for N1 | reuse, src_fps 15.19 (41/2.7) |
| front | s5_hood | 11.162-16.362 (315-470, 156 f) | hood -> under-hood capture | as rendered | hood opens 11.812 -> 13.762 (render keys 0.65 -> 2.6) | the one real state scan | reuse unchanged, src_fps 15 |
| front | **N1_front** | 16.362-24.162 (471-704, 234 f) | RF corner parts, then the front stack | key0 t0: loc (2.9, 4.2, 1.1) tgt (0.75, 2.2, 0.75) 35 mm; hold-drift to t4.55: loc (2.75, 4.0, 1.15) tgt (0.8, 2.1, 0.8) (slow 6 % push on the corner); t4.55 -> t7.8 eased pull-back+rise: loc (3.6, 5.2, 2.6) tgt (0.4, 1.8, 1.3) 30 mm | (render t = music - 16.362; all translate-only, ease out, then hold) bumper duct t0.65-1.30 (17.012-17.662) -> (+0.25,+0.45,+0.05); right vent t2.60-3.25 (18.962) -> (+0.30,0,0), left vent same time -> (-0.30,0,0); fender t4.55-5.20 (20.912) -> (+0.40,+0.05,0); hood (pivot as s5, rot 37.19 held whole shot) t5.20-6.50 (21.562 lift) loc -> (0,+0.15,+0.90) | one part per hit, camera stays on the RF corner (items 2/5); every part moves toward the lens so it covers its own hole (item 6); hood is the only part with real data under it, so it gets the big lift; pull-back reads the stack | NEW 120 f (secs 8.0), src_fps 15.06; base x_base_explode.blend |
| rear | **N2_rear** | 24.162-28.062 (705-821, 117 f) | roof spoiler, exhaust trims | t0: loc (-2.9, -5.0, 1.5) tgt (-0.2, -2.2, 1.15) 30 mm -> t4.1: loc (-2.55, -4.55, 1.45) tgt (-0.1, -2.3, 1.1) (12 % push-in), eased | front parts held at N1's end offsets; wing t0.65-1.30 (24.812) -> (0,-0.30,+0.30); exhaust cover t1.30-1.95 (25.462) -> (0,-0.35,0) | the rear's two parts, framed on the rear only; camera below roof height so the spoiler's mount isn't the subject | NEW 62 f (secs 4.1), src_fps 15.25 |
| whole | **N3_reassemble** | 28.062-34.562 (822-1016, 195 f) | everything returns; clean car | t0: loc (-5.2, 5.6, 3.4) tgt (0,0.3,1.0) 32 mm -> t6.7: loc (-6.0, 4.4, 2.2) tgt (0,0.1,0.9), eased (front-left, high -> lower; side never seen before) | all parts start at N1/N2 end offsets. Home (offset -> 0, ease in): exhaust t0.65-1.30 (28.712), wing t1.30-1.95 (29.362), bumper duct + both vents t1.95-2.60 (30.012), fender + hood loc t2.60-3.25 (30.662; hood keeps 37.19), hood rot 37.19 -> 0 t3.25-3.90 = **lock 31.962**. From render frame 60 (t >= 3.93) render base = car4.blend only, no parts (same camera) | reassembly travels rear -> front and ends on the hood shutting on the 32.00 step; clean car hides seams (c5 lesson); front-left view keeps the RF holes on the far side | NEW 100 f (secs 6.7) as two specs: frames 1-59 parts, 60-100 car4; src_fps 15.0 |
| end | fade + logo | fade N3 to black 33.262-34.562 (frames 975-1016); logo 34.562-39.5 (1017-1164, 148 f) | logo | logo_card.py --secs 4.9333 --width 360 | - | small logo after a fade (item 7) | re-make logo card (cheap) |

Total 1164 frames = 38.80 s, cuts at 159 / 237 / 315 / 471 / 705 / 822 / 1017 (all on round(beat*30)).

Implementation notes for shots.py: N0 = `orbit((7.6,7.0), 48, 30, 1.05, 1.0, (0,0.2,0.9), (0,0.5,0.9), 32, 32, 5.47)`.
N1-N3 part keys use shot.py's {t, loc, rot, ease} with a hold key at the start of each move (as xpart does); the hood
keeps `pivot` = HOOD pivot and `rot [37.19,0,0]` from t0 in N1/N2 and until t3.25 in N3. Side Vents: split the prepped
mesh by x sign into x_side_vent_r / x_side_vent_l before N1. Persistent data stays off (animated parts); scan every
frame's mean luma after each render and re-render dark ranges in fresh processes. Run `shots.py <N> --check` first and
look: N0 whole car inside the frame at first/mid/last (target ~65 % width, nothing clipped); N1 hood top at t7.8 inside
the frame; no black void reading as the subject at the end of each part move (else halve that offset).

Optional (only if direction.md open question 1 shows a scanned inner face): N1 fender add rot (0,0,-20) about its rear
edge during t6.5-7.8 so the inside turns toward the lens; N2 exhaust cover none. Otherwise translate only (item 5).

## Cut list (from v1)
- s1_front34 (all 158 f): rear cropped for the whole shot; same view as s2/s5 (IoU 0.76). Replaced by N0.
- s2_rear34 (98 f): front cropped, repeat of s1's view, forced front->rear->front ping-pong.
- s6_top (78 f): rotating top-down, roof clips, no feature; rotation for its own sake.
- s7_explode (390 f): all parts at once in one wide orbit, parts ~small in 9:16, black holes at fender/bumper corner,
  2.1 s dead after lock.
- logo 720 px wide: too big; now 360 px after a fade.

## Hold list (> 0.75 s with nothing new)
- N1 t0-0.65 (0.65 s) and t1.30-2.60 (1.3 s): camera pushing on the RF corner with the bumper corner out - the viewer reads
  the pulled corner and duct; t6.5-7.8 (1.3 s): camera still pulling back to reveal the whole front stack (moving).
- N2 t1.95-3.9 (1.95 s): push-in on the rear with spoiler + trims out - the only look at those two parts.
- N3 t0-0.65 (0.65 s): establishes the full exploded state from the new angle; t3.9-5.2 (1.3 s): clean car settles while
  the camera descends, then 2-beat fade. No static hold anywhere.
- s5 13.762-16.362 (2.6 s): open hood, camera easing in on the under-hood capture (the state's payoff).

## Render budget
NEW: N0 82 + N1 120 + N2 62 + N3 100 = **364 frames** at 75 % / 12 spp / 15 fps. N0 is car-only (~10 s/f, ~15 min);
N1-N3 carry 6-7 parts (~25-35 s/f, ~2-2.7 h). Render one at a time in the background: N1 first (biggest moment), then
N3, N2, N0. Reused unchanged: s3_grille (33 f), s4_wheel (42 f), s5_hood (81 f).
