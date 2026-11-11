# Director plan - Honda Civic FE1 Si scan reel, v2 (director, stage 2)

Keeps the scene order in `direction.md` (whole -> front -> right side -> rear -> reassembly -> logo). No text anywhere.
Inputs: lessons.md, style-guide, Temerario notes (training/references/README.md), v1 project.yaml/editlog, `ive director`
report on v1 (saved outside the repo; flags: s1~s2 same view IoU 0.74, s5~s6 IoU 0.64, s7 3.5 s dead, s1 0.8 s dead,
no focus tags), v1 frames, and user notes 1-9 + A-D for v2.

Scan frame (prepped, metres): front = +Y, car's LEFT = -X, right = +X, floor z = 0, length 4.82 m (nose ~+2.4, tail ~-2.4).
`orbit(r, ang, h)` as in tools/shots.py: ang 0 = in front, +90 = car's left, 180 = behind, -90 = car's right.
Sensor 20.25 mm wide, 1080x1920, renders at 15 fps, res_pct 75, 12 spp, **persistent data OFF** for N2-N4 (animated parts).

## Shot table

Times are on the kick grid t(k) = 0.2899 + 0.41794 k. Output frames @30 = round(t*30). Local t = seconds from the shot's in-cut.

| section | shot | start-end | focus | camera | part action (beats) | why it earns its seconds | source |
|---|---|---|---|---|---|---|---|
| whole | **N1_open** | 0.000-7.395 (0-k17), 222 f | the whole car, front-left 3/4 | orbit r 9.2 -> 8.2, ang 30 -> 34, h 1.0 -> 1.3, centre (0, 0.3, 0.6), focal 30, lin -> out2. Car ~64 % -> ~75 % of width, centred vertically; a push + rise, not a turntable (4 deg) | none | Note 4: the whole car, moving from frame 1, over the quiet intro; sets up the front section | **NEW** 114 f (7.6 s incl. 0.2 s tail) |
| front | **s3_wheel** | 7.395-10.320 (k17-k24), 88 f | front-left rim + brake caliper | as rendered, **played reversed** (f_0034 -> f_0001): slides forward along the flank toward the nose | none | the best-captured wheel (left side; RR is a tyre ring) | reuse all 34 f, src_fps 33/(2.933+0.1) = **10.88** |
| front | **s4_lamp** | 10.320-13.246 (k24-k31), 87 f | headlight + grille corner | as rendered: slide across the nose toward the centre/right | none | ends the front run travelling toward the right side | reuse all 41 f, src_fps 40/(2.9+0.1) = **13.33** |
| right side | **N2_doors** | 13.246-17.843 (k31 DROP - k42), 138 f | right door jambs + sill (Door Open scan) as the doors come out | start (3.6, 2.6, 1.35) -> target (0.85, 0.0, 0.70); end at 4.6 s (2.8, 1.2, 1.15) -> target (0.85, -0.25, 0.60); focal 32, inout. Front-right 3/4 at door height: the door span foreshortens to fill the 9:16 frame from A-pillar to C-pillar, sill at the bottom third | front door: k31 (t 0) -> out (+0.80, +0.30, +0.20) by k33 (t 0.84), ease out. Rear door: k34 (t 1.25) -> (+0.80, -0.30, +0.20) by k36 (t 2.09). Translate only, **no yaw/flip** (inner faces are the full car's shell, no scanned data). Then drift +3 % to the end | the side section on the drop; the doors move toward the lens into black and split at the B-pillar so the striker, hinge mounts and sill (real Door Open data) are seen, then the camera pushes to the B-pillar jamb | **NEW** 72 f (4.8 s) |
| rear | **N3_trunk** | 17.843-30.381 (k42-k72), 376 f | trunk lid on its hinge -> lid inner trim + goose-necks -> trunk interior (Trunk Open scan) | 0 s: (-0.5, -5.6, 1.5) -> target (0, -1.9, 0.85), focal 35 (tail fills the width). 4.18 s (k52): (-0.4, -4.6, 1.9) -> (0, -1.8, 0.8). 8.36 s (k62): (-0.4, -4.4, 2.4) -> (0, -1.7, 1.3) (lid stacked above the opening, 9:16). 12.54 s (k72): (-0.25, -3.3, 2.1) -> (0, -1.5, 0.55) (down into the interior and the body-side hinge boxes). All inout. Stay left of centre (RR wheel weak) | lid CLOSED t 0-0.84 (k42-k44) -> opens on the fitted hinge to OPEN by k49 (t 2.93), ease inout (v1 s5 keys). Holds open k49-k52 while the camera pushes in. **k52 (t 4.18): lifts off** the hinge: translate (0, -0.35, +0.75) from OPEN and tip +20 deg about X (width axis) so the inner trim + goose-necks face the lens, by k54 (t 5.02), ease out; drift +3 % to the end. Up and toward the camera into black, never across the body | richest region (real state + real part with a real inner face): one continuous rear run carries the k44 and k52 kicks and the whole breakdown | **NEW** 191 f (12.74 s). Lid mesh **deplated** first |
| whole | **N4_reassemble** | 30.381-37.068 (k72-k88), 201 f | all scanned parts returning to the car, then the clean car | orbit ang -145 -> -140, r 6.4 -> 5.8, h 4.3 -> 4.0, centre (0.2, -0.3, 0.5), focal 30, out2: high right-rear 3/4 looking down ~45 deg (hides the RR tyre ring), whole car + floating parts in frame, car ~75 % width | starts with doors at N2's end pose and lid at N3's end pose; drift to k76 (t 1.67); return k76 -> k80 (t 1.67-3.34), ease in; **LOCK on k80 (t 3.34, render frame 50)**. Base = explode_base for frames 0-50, **clean car4f (no parts) from frame 51** (c5 lesson: clean car after the lock). Slow push continues; **fade to black k86 -> k88** (36.232-37.068) in assembly | the Temerario reassembly; the only wide that shows all parts together, used for the return only | **NEW** 104 f (6.89 s), rendered as 2 frame ranges (0-50, 51-103) |
| - | **logo** | 37.068-39.800 (k88-end), 82 f | small ILLUMAESTHETIC logo | on black, fade in over ~0.3 s | - | note 7 | **remake** the card at ~30 % frame width (current logo_card.mp4 = 79 %); no Blender |

Cut frames @30: 222, 310, 397, 535, 911, 1112; end 1194. Assemble with `projects/honda-s2000/tools/concat_assemble.py`
(`frames: [222, 88, 87, 138, 376, 201, 82]`), or with `ive assemble` and the first clip one frame short (dur 7.3667).
New-shot src_fps = (N-1)/(dur + 3/30) (STI lesson). Verify every cut against the decoded audio's kick peaks, |err| <= 1/2 frame.

## Frame checks (note A) - do these on 30 % previews (first/mid/last) before each final, and again on the finals

| shot | first | mid | last |
|---|---|---|---|
| N1 | whole car with margin on all sides (nose, rear bumper, both left wheels, roof) | still whole; no edge contact | whole car, <= ~75 % width; silhouette bounds > 3 % from both edges (measure, as for v1 s1 which touched x=0 from frame 6) |
| s3 (rev) | wheel + arch fill the frame, tyre not clipped at the bottom | brake visible through spokes | wheel front edge, fender line; no crop seam of the 2 mm block |
| s4 | headlight + grille corner fill the frame | - | no 2 mm crop seam on the hood (v1 kept it left of the seam) |
| N2 | closed right side, A- to C-pillar, sill at bottom third; **RR wheel out of frame or under the sill edge** | both doors out in black, B-pillar striker + sill visible between them; **no black holes above the beltline** (Door Open reaches ~0.85 m - if holes show, re-aim so the top of frame sits at the beltline) | B-pillar jamb large; doors not clipped at the frame edge more than half their width |
| N3 | tail fills the width, lid closed, **plate flattened** (full-res check) | lid above the open trunk, inner trim + goose-necks facing the lens, interior visible below | interior + body-side hinge boxes fill the frame, no dead black in the lower half |
| N4 | whole car + doors + lid in frame, RR tyre ring not readable | lock frame 50: panels seated, no z-fight flashes; frame 51 (car4f) identical silhouette | clean car, still whole, before the fade |
| logo | small (~30 % width), centred | - | black at 39.80 |

Also: per-frame mean-luma scan of every new render folder before assembling (Cycles black-frame lessons).

## Cut list (v1 material not used, and why)
- **s1_front34** (all 114 f): nose clipped from frame 6, both ends clipped by frame 84 (note 4/A); turntable (note 3); 0.8 s dead tail.
- **s2_rear34** (all 91 f): rear section would appear twice (s2 + trunk) (note B); same silhouette as s1 (IoU 0.74); legible plate.
- **s5_trunk** (all 66 f): content is right but the lid plate is legible; replaced by N3's first 4.18 s so the rear is one continuous run.
- **s6_top** (all 66 f): rotating top-down that shows only the filled hood/rear glass (note 3, weak data); repeats s5's opening view (IoU 0.64).
- **s7_explode** (all 166 f): one wide orbit with all panels separating at once (note 2), car ~60 % width in the lower half with
  dead black above (note A), plate legible on the floating lid, 3.5 s dead after the lock, frames 91-165 black. Its re-render
  of 91-165 is **no longer needed** - stop it if it hasn't finished, to free the machine for N1-N4.

## Hold list (> 0.75 s)
| where | length | reason |
|---|---|---|
| N2 doors out, k36-k42 | 2.5 s | camera keeps pushing to the B-pillar jamb - the real Door Open data is the point of the shot |
| N3 lid open on its hinge, k49-k52 | 1.25 s | camera pushes into the real trunk interior before the lid lifts off on the k52 kick |
| N3 lid floating, k54-k72 | 7.5 s | not static: camera rises to stack lid over the opening (k52-k62), then descends into the interior and hinge boxes (k62-k72) |
| N4 after lock, k80-k86 | 2.5 s + 0.84 s fade | the clean, whole car after reassembly (Temerario 34-35 s); slow push continues |
| logo | 2.73 s | end card to the end of the audio |

## Render budget
| shot | frames @15 fps | ~time @12 s/f |
|---|---|---|
| N1_open | 114 | 23 min |
| N2_doors | 72 | 14 min |
| N3_trunk | 191 | 38 min |
| N4_reassemble | 104 (2 ranges) | 21 min |
| previews (3 per shot @30 %) | 12 | ~1 min |
| **total** | **481 (+12 preview)** | **~96 min** |

Reused unchanged (order/speed only): **s3_wheel** (reversed, 34 f) and **s4_lamp** (41 f).
Why not more reuse: every other v1 render breaks a v2 note or a standing lesson (cropped opener, rotations, a section shown
twice, all-at-once wide explode, legible plate). Cheaper fallback if the budget is too high: render N1 at 10 fps (75 f; it is
a slow, near-linear push) - saves 39 f (~8 min). Screen time is fixed by the track, so the only other saving would be to bring
back a v1 render that breaks a note; I would not.

Render order (one at a time, background): deplate lid.blend -> N3 preview -> N3 -> N2 preview -> N2 -> N4 preview -> N4 -> N1.
