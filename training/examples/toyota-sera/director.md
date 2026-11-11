# Toyota Sera v3 - director's shot plan

Stage 2 of direction.md (scene order kept as is). One focus per shot, no redundant frames, no text, every cut on the kick
grid t(b) = 0.0355 + 0.59999 b. Scan frame: nose -Y, car's right -X, z up, metres. Camera: sensor 20.25 mm horizontal
fit, focal 30 everywhere -> visible width = 0.675 x distance (checked per key below). Render 15 fps, 75 %, 12 spp,
EXPOSURE -0.35, persistent data off for every shot with moving parts. Each render = play length + 3 frames (minterpolate tail).

Notation for tools/shots.py: `orbit(t, r, ang, h, c, focal, ease, tz)` as defined there (ang 0 = in front, -90 = car's
right, +90 = car's left, 180 = behind). Explicit keys are `{"t", "loc", "target", "focal": 30, "ease"}`. Part keys:
`loc` offset, `rot` euler deg about the part's bbox centre (no pivot), or `ang` about the fitted hinge (`swing()`).

## Bases to build first (~2 min each, tools/explode_base.py restricted)
- `front_base`: car3 minus hood outer skin (hood_masks outer) minus car tris < 9 mm from front_bumper_3mm (+ bumper-bbox
  extras missing from the front-bumper-removed state, i.e. the plate rule) + fills: front_bumper_removed_3mm, hood_open_3mm
  (hood dropped), NEW 8 mm / KEEP_OUT 12 mm against hood_panel + front_bumper_3mm. Rear bumper and doors stay on.
- `rear_base`: car3 minus car tris < 9 mm from rear_bumper_only_3mm (+ plate rule against rear_bumper_removed_3mm) +
  fill rear_bumper_removed_3mm only (> 8 mm). Hatch stays shut (no hatch-open data).
- Existing: car4, car3 (s3_wheel), doors_base, explode_base.

## Shot table

| section | shot | beats / start-end (s) / frames@30 | focus | camera (scan frame) | part action (t from shot start) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | **S1_whole** | b0-8 / 0.036-4.835 / 145 (first clip, one frame short per lesson) | the whole Sera, front-right 3/4 | `arc(0, 4.8+0.2, r 7.2->6.3, ang -42->-30, h 1.25->1.05, c (0,-0.10,0.60)->(0,-0.35,0.55)*, n 8, ease lin)`; dist 7.3->6.4 m = width 4.9->4.3 m vs car 3.85->3.41 m projected = 79-84 % | none (car4) | brief 4: whole car, moving from frame 1; push-in hands over to the front corner | NEW, 75 fr (5.0 s) |
| front | **S2_wheel** | b8-12 / 4.835-7.235 / 72 | front-right tyre + rim + centre badge | as rendered (r ~1.3 m slide toward nose, 40 mm) | - | wheels are the cleanest detail; front corner of the travel | REUSE s3_wheel, first 39 frames (src_fps per lesson: (N-1)/(dur+3/30)) |
| front | **S3_front** | b12-24 / 7.235-14.435 / 216 | front assembly: hood -> engine bay, then front bumper inner face over the exposed crash structure | keys: t0 loc (-2.6,-4.3,2.0) tgt (0,-1.3,0.65) [4.2 m, 2.8 m wide]; t2.4 loc (-2.2,-4.6,2.3) tgt (0,-1.6,0.6) lin; t4.2 loc (-1.5,-4.9,2.9) tgt (0,-2.3,0.45) inout [3.8 m, 2.6 m wide]; t7.2 loc (-1.0,-4.66,2.97) tgt (0,-2.7,0.35) out2 [3.4 m, 2.3 m wide, 50 deg down so the bumper sits on black floor, not on the body] | hood: `swing("hood", 0.6, 2.4)` (opens b13-16, fully open ON 9.635 phrase). front_bumper_3mm: keys t0 loc 0 rot 0; t2.4 loc 0; t3.6 loc (0,-1.20,-0.10) ease out (slides toward camera, b16-18); t5.4 loc same, rot (90,0,0) inout (tips about X: inner face +Y -> up, faces the high camera, b18-21); t7.2 hold | richest region (2 states + part + hinge) gets the longest scene and the phrase downbeat. One held shot: hood + bumper, camera never leaves the front. Tip is justified: inner face + mounting tabs are scanned | NEW, 111 fr (7.4 s) |
| side | **S4_doors** | b24-32 / 14.435-19.235 / 144 | butterfly doors + cabin | keys: t0 loc (-4.0,-0.9,1.25) tgt (-0.3,-0.2,0.85) [3.8 m, 2.6 m wide - side section, nose/tail cropped]; t3.0 loc (-3.6,0.3,1.6) tgt (-0.2,-0.2,0.95) lin; t4.8 loc (-3.0,0.9,1.9) tgt (-0.1,-0.15,0.85) out2 [3.3 m, 2.2 m wide; from slightly behind so the forward-swung door doesn't block the cabin] | `swing("door", 0.6, 3.0)`, `swing("door2", 0.6, 3.0)` (open b25-29) | signature feature, real 'Door Open' interior; side-on = new angle (v2 s6 repeated the front 3/4) | NEW, 75 fr (5.0 s) |
| rear | **S5_rear** | b32-40 / 19.235-24.035 / 144 | rear bumper inner face + rear panel structure / lamp housings | keys: t0 loc (-2.5,4.1,1.1) tgt (0,1.5,0.6) [3.6 m, 2.5 m wide: tail, spoiler, lamps]; t1.8 loc (-1.9,4.5,2.2) tgt (0,2.2,0.5) lin; t4.8 loc (0.0,4.75,2.9) tgt (0,2.7,0.35) out2 [3.4 m, 2.3 m wide, straight behind, 50 deg down - symmetric, NOT a mirror of S3's 3/4] | rear_bumper_only_3mm: t0.6 loc 0; t1.8 loc (0,+1.20,-0.10) out (b33-35, toward camera); t3.0 rot (-90,0,0) inout (inner face -Y -> up, b35-37); hold to 4.8 | rear part + state; hatch shut (no data); end of the travel | NEW, 75 fr (5.0 s) |
| explode | **G1_front_lift** | b40-46 / 24.035-27.635 / 108 | front assembly stacking above the nose (hood, front bumper) | `arc(0, 3.6+0.2, r 4.6->4.3, ang +35->+50, h 2.9->2.7, c (0,-1.0,1.0), tz 1.1, n 8, lin)` - front-LEFT high, first time the left side is seen; 5.0 m, 3.4 m wide | global explode T = t (see keys below): hood lifts b40-42, front bumper b41-43, float through the kick break | progressive explode starts on the phrase; zoomed on one assembly, not the whole car | NEW, 57 fr, explode T 0-3.8 |
| explode | **G2_side_rear_lift** | b46-52 / 27.635-31.235 / 108 | doors + rear bumper layering above the car | `arc(0, 3.8, r 5.8->5.5, ang +80->+100, h 2.4->2.6, c (0,0.55,1.0), tz 1.15, n 8, lin)` - left side; frames y -1.0..+2.3 (3.3 m) in 3.9-3.7 m width; nose deliberately out (G1's subject) | door2 lifts b46-48, door b47-49, rear bumper b48-50 (T 3.6-6.0) | Temerario side view, panels in layers; new parts each beat | NEW, 57 fr, explode T 3.6-7.4 |
| explode | **G3_home** | b52-60 / 31.235-36.035 / 144 (fade to black over the last 36 frames, b58-60) | reassembly -> the clean closed car, rear-left 3/4 | `arc(0, 4.8+0.2, r 6.8->6.3, ang +140->+150, h 3.0->2.3, c (0,0.10,0.70), tz 0.9->0.6, n 8, out2)`; 6.7 m end = 4.5 m wide vs car 3.8 m = 84 % - whole car, other end/side/height from S1 | T 7.2-9.6: rear bumper home b52-54, doors b53-55 (ang -> 0), front bumper + hood home b54-56, everything LOCKS on b56 (33.635). Render G3a (T 7.2-9.6, explode_base + parts) and G3b (T 9.6-12.0, car4 only) with the SAME camera keys (t offset 2.4) -> swap to the clean car on the b56 kick (c5 lesson) | brief 7: reassembly, short, then fade - no long hold | NEW, G3a 36 fr + G3b 39 fr |
| end | **logo** | b60-end / 36.035-39.30 / 98 | logo | logo_card.py --width 480 (44 % of 1080), fade in 0.3 s, fades with the decay | - | small, short (brief 7) | re-make card (no Blender) |

*S1 arc: `arc()` takes one `c`; build the 9 keys with c and tz lerped linearly (or two arcs). Car centre offset keeps the
tail inside at 6.3 m (half-width 1.93 m < 2.13 m).

### Explode part keys (global T, seconds from b40 = 24.035; G1 renders T 0-3.8, G2 shifts keys by -3.6, G3a by -7.2)
Translate-only stack (brief 5: no spins here - the inner faces were shown in S3/S5). Base `explode_base`.
| part | home until | out (ease out) to | drift (lin) | home (ease in) |
|---|---|---|---|---|
| hood_panel | T 0.0 | T 1.2: (0, 0.05, 1.35) | T 7.2: x1.06 | T 8.4 -> 9.6 |
| front_bumper_3mm | T 0.6 | T 1.8: (0, -0.35, 0.75) | T 7.2: x1.06 | T 8.4 -> 9.6 |
| door2_panel (left) | T 3.6 | T 4.8: (0.45, 0.05, 0.65), ang -57.0 x 0.35 | T 7.8: x1.06 | T 7.8 -> 9.0, ang 0 |
| door_panel (right) | T 4.2 | T 5.4: (-0.45, 0.05, 0.65), ang 56.2 x 0.35 | T 7.8: x1.06 | T 7.8 -> 9.0, ang 0 |
| rear_bumper_only_3mm | T 4.8 | T 6.0: (0, 0.35, 0.85) | T 7.2: x1.06 | T 7.2 -> 8.4 |
Hood/front bumper: hold their drifted offset from T 7.2 to 8.4, then home; last lock T 9.6 = b56.

## Cut list (from v2)
- s1_turntable - cropped car (r 3.9 m) and a turntable: replaced by S1 whole-car push.
- s2_rear - rear shown in slot 2 then front again (ping-pong); orbit with nothing new; IoU 0.81 with s1.
- s4_nose - grille/vent scan holes; nose covered by S3.
- s5_hood - same subject as the bumper -> merged into one held S3; view repeated s1/s6 (IoU 0.65/0.72).
- s6_doors - front-right 3/4 repeated s1/s5 (IoU 0.80/0.72): re-rendered side-on (S4).
- s7_top - rotating top-down, nothing new; IoU 0.74 with s6.
- s8_explode / s8_explode_v1 - all 5 panels at once in one wide orbit: replaced by G1-G3, one assembly per angle.
- logo 760 px x 4.47 s -> 480 px x 3.27 s.

## Hold list (> 0.75 s without a part starting a new move)
- S1 whole 4.8 s: no part action by design; camera pushes 0.9 m + 12 deg the whole time (opener, brief 4).
- S3 b21-24 (1.8 s): camera keeps closing on the bumper's inner face and the exposed crash structure - the payoff of the section.
- S4 b29-32 (1.8 s): doors open, camera pushes into the cabin (real interior data).
- S5 b37-40 (1.8 s): camera rises to straight-behind over the rear bumper's inner face + rear panel.
- G1 b43-46 (1.8 s, the kick break): front panels drift x1.06 while the camera orbits 15 deg - the music drops out here.
- G3 b56-58 (1.2 s): clean car, camera still easing; then fade b58-60. Logo 3.27 s fading with the track's decay.

## Render budget (15 fps, 75 %)
S1 75 + S3 111 + S4 75 + S5 75 + G1 57 + G2 57 + G3a 36 + G3b 39 = **525 frames** (~35 s of footage, ~1.2-1.5 h at
8-10 s/frame) + 2 bases (~4 min). Reused unchanged: s3_wheel only. Preview first/mid/last of S3 and S5 at 30 % before the
finals (bumper clearance + clear background), one render at a time, luma-scan every folder (persistent-data dropouts).

## Timeline frames (concat assembler, exact frames)
S1 145 | S2 72 | S3 216 | S4 144 | S5 144 | G1 108 | G2 108 | G3 144 (fade last 36) | logo 98 -> cuts at 145, 217, 433,
577, 721, 829, 937, 1081; end 1179 (39.30 s).
