# Lamborghini Revuelto - direction v2 (scene director + director, both stages)

Stage 1 = `.claude/agents/scene-director.md`, stage 2 = `.claude/agents/director.md`. Inputs read: CLAUDE.md, lessons.md
(all), style-guide.md, training/references/README.md (Temerario), clips.md, project.yaml, cuts.json, shots.py,
tools/shot.py, hinge.json, editlog.jsonl, review.md, `ive director` report (director_report.md). No feedback.jsonl yet.
Looked at: v1_sheet.jpg, first/mid/last frame of every render dir in /home/user/media/work/renders/revuelto/, s6 last
frame and s8 frame 36 at full res.

Format stays: scan only, no IRL, silver on black, Temerario-style, 34.6 s, fixed track (102.52 BPM,
b(m) = 0.5222 + 0.58525 m). Labels only on the two bumper-removed holds (rule C).

Scan frame (prepped m): ground z 0, nose -Y (y -2.46), tail +Y (2.46), roof 1.03, half-width 1.08, car's LEFT = +X.
Camera az 0 = front, +90 = car's left, 180 = rear (tools/shot.py keys: az/el/dist/target/lens, smoothstep per key).

## 1. Feature inventory

All scans are from the 2026-07-26 session, one Artec frame, levelled with one transform, registration 1.5-2.6 mm
median (editlog) and visually checked (chk/reg_overlay.jpg).

| Region | Data (this car) | States (registered) | Parts (registered) | Signature | Weak data | Richness |
|---|---|---|---|---|---|---|
| Front | raw 3 mm car + 2 mm parts; s6 shows the exposed front end: frunk tub, lower structure, radiators/brackets either side | Hood Open (front lid, hinge fitted 1.5 mm, -67.8 deg); Front End Bumper & Headlights Removed | front bumper, headlights | Y headlights, front lid | intake grilles/dark trims are holes in the raw car (s4 close-up shows big black patches under the headlight) | 5 |
| Left side | full side, mirror, doors | Fender Removed (Mounting); Side Skirts & Fin Removed | left upper fender, side skirt front, side skirt rear, side fin; mirror head (part only) | side fin, door line | **no mirror-removed state: the mirror never moves (rule D)**; right side has no part scans | 5 |
| Rear | tail, wing, tail lights; exposed rear end in s8 (structure behind the bumper) | Rear End Bumper Off (Tail Lights Off); Rear End Wing Removed | rear bumper (forced, 82 % overlap), rear wing, tail light L, tail light R | Y tail lights, rear wing | possible licence plate on the bumper (check at full res); ragged edges where state scan meets car | **6 (richest)** |
| Wheels | front-left wheel/disc/caliper captured fully (2 mm zone, s5 is clean) | - | (Wheels scan fetched, not used) | 20-spoke rims | none seen | 2 |
| Top | roof, engine deck from above | - | - | - | top-down v1 ran hot, spin showed nothing new | 1 |
| Engine bay / frunk interior | frunk only (via Hood Open) | counted in Front | - | - | no engine-cover state -> no engine bay scene | (Front) |

Not usable: 2024 full scan and VF exhaust set (other sessions), diffusers/top bumper halves (overlap rear bumper).

**Hood rule (D):** there is a Hood Open state but no hood-removed state. The lid may only swing on its hinge; it never
floats off the car. **v1 s8/s9/s10 broke rule D twice**: the mirror head flew off (no mirror-removed scan) and the hood
floated closed 1.7 m above the car (no hood-removed scan). v2 fixes both.

## 2. Scene order (travel front -> left side -> rear, then everything home)

Opener on the front: the front end opens on phrase B, and its 2 states + hinge make it the first big reveal. The rear
(most parts: bumper, wing, 2 tail lights, 2 states) is the richest region and gets the longest scene, on phrase C
(18.66). The climax taiko (27.93) carries the reassembly lock.

| # | id | section / focus | scans used | why here | start-end (s) | beats | reuse / render |
|---|---|---|---|---|---|---|---|
| 1 | v2_whole | whole car / entire car, front-left 3/4 | CAR (raw 3 mm + all parts at home) | rule A wide opener; front-left 3/4 points at where the action starts; quiet build gets one slow move | 0.000-6.960 | 12 (m0-11) | NEW 108 f |
| 2 | s6_frontopen | front / bumper + headlights out, lid up | WITH_CAR (v1) | front states; lid starts rising ~9.15, right at phrase B 9.30 | 6.960-10.471 | 6 (m11-17) | REUSE v1 s6 unchanged (53 f, same slot length 3.511 s as v1) |
| 3 | v2_frontin | front / structure behind the front bumper + frunk | EXPLODED_OBJS (base + parts) | rule C hero beat: move in and hold, labelled | 10.471-15.153 | 8 (m17-25) | NEW 74 f |
| 4 | v2_side | left side / fender, skirts, fin come off | EXPLODED_OBJS | side states; continues the travel from the front-left corner | 15.153-18.664 | 6 (m25-31) | NEW 56 f |
| 5 | v2_rear | rear / wing, tail lights, rear bumper off, move-in on rear structure | EXPLODED_OBJS | richest region on phrase C, longest scene; rule C | 18.664-25.687 | 12 (m31-43) | NEW 109 f |
| 6 | v2_reassemble | whole car / every scanned part flies home, lock on the climax, rear 3/4 hero | WITH_CAR | the only time all parts are seen together; lock on taiko 27.967 | 25.687-30.400 | 8 (m43-51) | RE-RENDER frames 1-35 (pre-lock); REUSE v1 s10 frames 36-70 |
| 7 | logo | - | logo card | loudest taiko hit 30.40, rides the decay | 30.400-34.600 | - | REMAKE small (no Blender) |

Cuts: 6 hard cuts (v1 had 10); holds 12/6/8/6/12/8 beats, Temerario-style long held moves.

### Diff against v1
- Dropped **s1_side** (both ends cropped at frame 1, rule A), **s2_front34 / s3_rear34** (cropped turntables, rotation for
  its own sake, director IoU 0.78-0.84 repeats).
- Dropped **s4_headlight**: black holes in the intake under the headlight (weak data), and it puts the front in front of the front section a second time.
- Dropped **s5_wheel**: the front-left wheel is framed under the fender at the start of v2_side; keeping s5 would show
  that corner twice. (It is clean data; if the editor needs 1.17 s anywhere, it is the only reusable alternative.)
- Dropped **s7_top** (spinning top-down, nothing new, hot roof), **s8_explode** (all panels at once in one wide orbit
  + mirror and hood removed without scans), **s9_float** (repeat of s8, IoU 0.65).
- Kept **s6_frontopen** as is. Kept the post-lock half of **s10**. Logo remade small.
- New: section-focused progressive disassembly (front -> side -> rear), each part leaves into clear black and stays off
  until the reassembly. Two labelled move-ins (front, rear).

## 3. Music map (b(m) = 0.5222 + 0.58525 m; frames = round(t*30), first clip one frame short)

| m | t (s) | frame | event |
|---|---|---|---|
| 0 | 0.000 (b0 0.522) | 0 | v2_whole fades up (1.5 s) |
| 11 | 6.960 | 209 | cut: s6 front opens (bumper moves ~7.07) |
| 15 | 9.301 | (279) | phrase B: lid begins to rise (~9.15-10.42 in s6) |
| 17 | 10.471 | 314 | cut: v2_frontin; label 1 |
| 21 | 12.813 | (384) | label 2 swaps in |
| 25 | 15.153 | 455 | cut: v2_side, fender lifts |
| 31 | 18.664 | 560 | phrase C, cut: v2_rear, wing lifts |
| 36 | 21.590 | (648) | rear bumper fully off; label 3 |
| 40 | 23.932 | (718) | label 4 |
| 43 | 25.687 | 771 | cut: v2_reassemble |
| - | 27.967 | (839) | every part home (ease-in slam) on the climax taiko attack 27.93 |
| - | 30.400 | 912 | cut: logo on the loudest taiko attack |
| - | 34.600 | 1038 | end (-45 dB) |

## 4. Shot specs (stage 2: one focus per shot)

New part layout `OFF` (replaces v1 EXPL; every part leaves into clear black, never across the body; translations only,
no spins: nothing here needs its back shown). Offsets in m from home:
- fb (0, -0.45, 1.00) above the nose; hl (0, -0.30, 1.40) above it
- hood: **stays on its hinge** at deg = 0.85 x open_deg (as s6 OPEN) until the reassembly closes it; never an offset
- fe (0.35, 0, 0.75); ssf (0.60, 0, 0); ssr (0.60, 0, 0) (out beside the sill on the ground, below the body line);
  fin (0.45, 0, 0.55)
- wing (0, 0.10, 1.25); tll (0.15, 0.20, 1.65); tlr (-0.15, 0.20, 1.65); rb (0, 0.30, 0.95)
- **mir: no key, ever (home).**
Parts already removed in an earlier section hold their OFF pose in later shots (front parts sit at OPEN in s6, then lift
to OFF in v2_frontin).

### 1 v2_whole - section: whole car; focus: entire car, front-left 3/4
- Camera: t0 az 50, el 7, dist 8.2, target (0, -0.2, 0.55), lens 40 -> t1 az 34, el 10, dist 7.2, target (0, -0.5, 0.55)
  (lin). Slow push + 16 deg drift toward the front; not a turntable. Ends near s6's first pose (az 38, el 12) so the cut
  into s6 is a cut-in on the same axis.
- Whole car inside the frame every frame: nose, tail, both visible wheels, roof, wing with >= 5 % side margins; car
  ~70 % -> ~85 % of width. If the first/mid/last sheet clips anything, add dist, do not crop.
- Objects: CAR (raw car + all parts at home). 6.960 s + 3 frames tail = 108 f.

### 2 s6_frontopen (reuse) - section: front; focus: front bumper and headlights coming off, lid rising
- Unchanged v1 render, dur 3.511 s, src_fps 15 as v1. Lid rise starts ~0.15 s before phrase B; nudge with src_fps
  only if the editor hears it early (lesson: src_fps, not speed).

### 3 v2_frontin - section: front; focus: structure behind the front bumper (frunk tub + lower front structure)
- Camera: t0 = s6's last pose (az 24, el 18, dist 5.0, target (0, -1.8, 0.65), lens 40) -> t 0.625 (13.40 s) az 12,
  el 14, dist 2.4, target (0, -2.1, 0.42) -> t1 az 6, el 13, dist 2.2, target (0, -2.12, 0.40) lin (slow drift = hold).
  Structure fills the frame width at the end (~1.8 m wide at 2.2-2.4 m).
- Parts: fb and hl rise from OPEN to OFF over t 0-0.25 (10.47-11.64 s) and leave the top of frame as the camera moves
  in (clears the view). Hood stays open on the hinge (keep it in frame top as context).
- Objects: EXPLODED_OBJS, light_ref base, persistent off. 4.682 s + 3 = 74 f.
- Labels: L1 10.471-12.813 `FRONT BUMPER & HEADLIGHTS REMOVED` (two lines: FRONT BUMPER & / HEADLIGHTS REMOVED);
  L2 12.813-15.153 `FRONT STRUCTURE`.

### 4 v2_side - section: left side; focus: left fender, then side skirts and fin
- Camera: t0 az 62, el 20, dist 4.0, target (0.85, -1.25, 0.55) (fender + front-left wheel fill the frame) -> hold
  to t 0.40 -> t1 az 96, el 16, dist 5.2, target (0.90, 0.10, 0.45) (whole left side sill to fin).
  Lateral track, motivated by following the parts; mirror head stays on and in frame.
- Parts: fe home -> OFF t 0.04-0.30 (15.29-16.21); ssf + ssr t 0.50-0.75 (16.91-17.79); fin t 0.58-0.83 (17.19-18.07);
  0.6 s settle before the cut. Front parts hold OFF (off frame).
- No label (labels are reserved for the bumper holds).
- 3.511 s + 3 = 56 f.

### 5 v2_rear - section: rear; focus: rear wing, tail lights, rear bumper off -> structure behind the rear bumper
- Camera: t0 az 145, el 14, dist 6.4, target (0, 1.5, 0.75), lens 40 (rear half + stacking space above) -> hold to
  t 0.417 (21.59) -> t 0.75 (23.93) az 162, el 12, dist 2.6, target (0, 2.2, 0.50) -> t1 az 168, el 12, dist 2.4,
  target (0, 2.22, 0.48) lin.
- Parts: wing home -> OFF t 0.00-0.167 (18.66-19.84, on phrase C); tll + tlr t 0.167-0.25 (19.84-20.42);
  rb t 0.25-0.417 (20.42-21.59), straight up (no flight toward the lens). They leave the top of frame during the push.
  Front + side parts hold OFF.
- Labels: L3 21.590-23.932 `REAR BUMPER & TAIL LIGHTS REMOVED` (two lines: REAR BUMPER & / TAIL LIGHTS REMOVED);
  L4 23.932-25.687 `REAR STRUCTURE`.
- 7.023 s + 3 = 109 f.

### 6 v2_reassemble - section: whole car; focus: all scanned parts returning, then the closed car rear 3/4
- Same JSON as v1 s10 (seconds 4.7, fps 15 -> 70 f, same LOCK fraction 0.4851, same visible windows, light_ref base)
  with three changes: start pose = OFF (+ v1-style 6 % drift), hood deg from 0.85 x open_deg -> 0 ease-in at LOCK,
  mir has no key; camera t0 az 128, el 16, dist 9.0, target (0, 0.4, 1.1) (tighter than v1's 11 m). LOCK and t1
  camera keys unchanged, so frames after the lock are identical to v1: render frames 1-35 only, reuse v1 f_0036-f_0070.
  Verify the splice: the new frame 35/36 must diff ~0 against v1's (if not, render to the first matching frame).
- 35 f new.

### 7 logo
- Same card, logo ~300 px wide (~28 % of 1080; Temerario 25-35 %), centred, short fade in, fades with the decay to 34.6.

## 5. Labels (exact wording, rule C)

| # | time (s) | text | backed by |
|---|---|---|---|
| L1 | 10.471-12.813 | FRONT BUMPER & / HEADLIGHTS REMOVED | state scan "Front End Bumper & Headlights Removed" + parts fb, hl |
| L2 | 12.813-15.153 | FRONT STRUCTURE | what the state scan shows behind the bumper (s6 last frame) |
| L3 | 21.590-23.932 | REAR BUMPER & / TAIL LIGHTS REMOVED | state scan "Rear End Bumper Off (Tail Lights Off)" + parts rb, tll, tlr |
| L4 | 23.932-25.687 | REAR STRUCTURE | state scan behind the bumper (s8 frame 36) |

Small caps, ScanHUD `label` style, upper third, inside 9:16 safe margins, never over a moving part. No numbers.
Generic "STRUCTURE" on purpose: the renders show the frunk tub and brackets but no part I could name with certainty.
Upgrade L2/L4 to a component name (e.g. CRASH BEAM) only if the final move-in frame shows it unmistakably.

## 6. Cut list (from v1)
s1_side (cropped), s2_front34 + s3_rear34 (cropped turntables, repeated views), s4_headlight (intake holes, front
shown twice), s5_wheel (corner shown again in v2_side), s7_top (spin, nothing new), s8_explode (all at once, wide,
mirror/hood without state scans), s9_float (repeat of s8), s10 frames 1-35 (mirror + floating hood), 760 px logo.

## 7. Hold list (> 0.75 s)
- v2_frontin 13.40-15.15 (1.75 s, slow drift): read L2 and the structure.
- v2_rear 18.66-21.59 camera holds while 4 parts leave (parts move = not dead); 23.93-25.69 (1.75 s drift): read L4.
- v2_side 15.15-16.56 camera holds while the fender lifts.
- logo 30.40-34.60: music decay.

## 8. Render budget (15 fps, 75 %, 12 spp, persistent data off on every animated shot)

| shot | frames | est. s/f | est. min |
|---|---|---|---|
| v2_whole | 108 | ~18 | 32 |
| v2_frontin | 74 | ~30 | 37 |
| v2_side | 56 | ~25 | 23 |
| v2_rear | 109 | ~28 | 51 |
| v2_reassemble 1-35 | 35 | ~25 | 15 |
| **total** | **382** | | **~2.6 h** |

Reused unchanged: s6_frontopen (53 f), s10 f_0036-f_0070 (35 f). Preview each new shot at 30 % on 3 frames before the
final; first/mid/last sheet of every shot (rule A) and per-frame luma scan of every dir (lighting dropouts) before assembly.
If time is short, cut v2_whole's lead frames first, never the move-ins.

## 9. Tags for `ive director` (add to project.yaml clips)
v2_whole `section: whole, focus: entire car` / s6 `front, front bumper + headlights off, lid up` / v2_frontin `front,
structure behind front bumper` / v2_side `side, left fender + skirts + fin` / v2_rear `rear, rear bumper off + rear
structure` / v2_reassemble `whole, parts home + rear 3/4`.

## 10. Open questions for the editor
1. Rear plate: is it on the rear bumper part or left in the base, and is it legible in the v2_rear close-up? Deplate if so.
2. If the s6 bumper clips the left frame edge on the first/mid/last sheet, re-render s6 (53 f, ~25 min) with dist 5.0 ->
   5.4. This would put the budget over.
3. ssf/ssr OFF on the ground beside the sill: check the side sheet. If they read as lying on the floor in black, lift them
   z +0.25.

---

## v3 direction (2026-11-11, scene director + director, both stages)

Feedback on v2.1: "This works well, the wheels are oddly cut flat. Also I want to do exploded views of the individual
parts removed from the front and rear bumpers as well." Wheels are fixed in geometry (blend3, tyres to z -0.18). v3 keeps
the v2.1 travel (whole -> front -> left side -> rear -> reassemble -> logo) and adds one bumper-only shot to the front
and to the rear section. Every shot is re-rendered. Looked at: test/sub_f.png, test/sub_r.png (outer + inner face of
both assemblies, tinted pieces), blend3/*.json bboxes, shots_v2.py (the camera/OFF values v2.1 actually shipped).

### v3.1 Inventory changes (everything else as the v2 table)

| Region | New data | Consequence |
|---|---|---|
| Front | FRONT bumper assembly = fb_stripped (bare skin) + 10 registered piece scans: fb_hl_trim (one Y-shaped piece, both sides), fb_markers (one object, both sides), fb_fog_l/r, fb_fogtrim_l/r, fb_center_cover, fb_center_carbon, fb_radar, fb_towhook (7 cm). Inner face scanned (brackets, ducts; sub_f.png bottom row). | richness 5 -> 7; gets a bumper-only explode shot |
| Rear | REAR bumper assembly = rb_top_half1 + rb_diffuser_forced (two big halves) + rb_trim_cover, rb_reflector_l/r, rb_corner_marker_l (left only: no right marker scan, none is shown). Inner face scanned (wiring loom, brackets; sub_r.png bottom row). | richness 6 -> 7; gets a bumper-only explode shot |
| Wheels / low body | full round tyres, bumper lips and lower structure down to z -0.18 | ground-level targets ~0.09 m lower; check tyre bottoms on every first/mid/last sheet |

Not used (editlog): reverse light (10 mm, 44 %), plate light (66 %). Exhaust tips are not bumper parts.
Rule D unchanged: mirror never keyed; lid only on its hinge; no right-side part moves.

### v3.2 Scene order and music map

Both bumper explodes need 8 beats (inner face, turn, explode, hold = 2 beats each). The time comes from the opener
(12 -> 8 beats), from merging v2's s6 + frontin into one front shot, and from the side (6 -> 4 beats). All cuts sit on bar
downbeats (m = 3 mod 4). The two new bumper shots are the new content, so the front one opens ON phrase B (9.30); at the
rear the bumper leaves the car into phrase C (18.665) and the camera surges in on it. Lock 27.967 and logo 30.40 unchanged.

| # | id | section | focus (one per shot) | scans | start-end (s) | beats | out frames (30 fps) | render f (15 fps, +3) |
|---|---|---|---|---|---|---|---|---|
| 1 | v3_whole | whole | entire car, front-left 3/4, round tyres | CAR (raw car + parts at home) | 0.000-4.619 | 8 (m..7) | 139 | 73 |
| 2 | v3_front | front | bumper + headlights off, lid up, move in on the structure behind the bumper | car -> base + fb(assembled), hl, hood | 4.619-9.301 | 8 (m7-15) | 140 | 73 |
| 3 | v3_fb | front | the front bumper alone: inner face -> outer face -> its 10 pieces come off | front_bumper, fb_stripped + 10 pieces (no car) | 9.301-13.983 | 8 (m15-23) | 140 | 73 |
| 4 | v3_side | left side | fender, side skirts, fin come off | base + side parts | 13.983-16.324 | 4 (m23-27) | 71 | 39 |
| 5 | v3_rear | rear | wing, tail lights, rear bumper off, move in on the rear structure | base + wing, tll, tlr, rb(assembled) | 16.324-21.006 | 8 (m27-35) | 140 | 73 |
| 6 | v3_rb | rear | the rear bumper alone: inner face -> outer face -> diffuser / upper half / small parts separate | rear_bumper_forced, rb_top_half1, rb_diffuser_forced + 4 pieces (no car) | 21.006-25.700 | 8 (m35-43) | 141 | 74 |
| 7 | v3_reassemble | whole | every part home on the climax, closed car rear-left 3/4 | WITH_CAR (assembled bumpers) | 25.700-30.400 | 8 | 141 | 74 |
| 8 | logo | - | small logo (as v2.1) | card | 30.400-34.600 | - | 126 | - |

Frame cuts: 139 / 279 / 419 / 490 / 630 / 771 / 912 / 1038. Total renders 479 frames (budget 520).
Why this order (inventory): front and rear are now tied richest (7); the rear still gets the bigger music (phrase C inside
its section, then the climax directly after its explode). Each section is one continuous sequence (rule B): front = shots
2+3, rear = shots 5+6. `ive director` will flag 2/3 and 5/6 as same-section and the bumper-only pair as similar
silhouettes: reviewed, they are car -> its removed bumper, keep.

Music map: 0 fade up 1.5 s | 4.619 cut, bumper starts sliding | 5.789 bumper lifts away, headlights + lid | 6.960 push in |
8.130 arrive, hold | **9.301 phrase B: cut to the front bumper alone** | 10.471 turn | 11.642 pieces come off | 12.813 hold |
13.983 cut side | 16.324 cut rear, wing lifts | 17.494 rear bumper starts | **18.665 phrase C: bumper is off, camera
surges in** | 19.835 hold | 21.006 cut to the rear bumper alone | 22.176 turn | 23.347 pieces separate | 24.517 hold |
25.700 cut reassemble | **27.967 lock** | 29.90 fade | **30.400 logo**.
Cuts 4.619 (v1 used frame 139), 9.301, 13.983, 16.324, 21.006 are new for v3: measure each on the decoded audio (1 ms
half-rise) and move by one frame if needed, as was done for 10.50 / 15.20 in v2. 25.70, 27.967, 30.40 stay.

### v3.3 Shot specs (absolute seconds; convert with `frac()` per shot; smoothstep unless `lin`)

Frame maths at 40 mm: visible width = 0.90 x dist, height = 1.60 x dist (checked against v2 framings).
OFF poses as shipped in v2.1 (shots_v2.py): fb (0,-0.6,1.6), hl (0,-0.4,1.9), hood 0.85 x open_deg on the hinge,
fe (0.35,0,0.75), ssf/ssr (0.60,0,0), fin (0.45,0,0.55), wing (0,0.10,1.25), tll (0.15,0.20,1.65), tlr (-0.15,0.20,1.65),
rb (0,0.35,1.75). Hide any part that is parked out of frame in later shots (edge-touch test first).

**1 v3_whole** (0-4.619). Camera: t0 az 50, el 7, dist 7.1, target (0, 0.10, 0.46), lens 40 -> t1 az 36, el 10, dist 6.5,
target (0, -0.15, 0.46) `lin`. Same move as v2.1 in 4.6 s instead of 7 (reads as motion, not static). Target z 0.55 -> 0.46
for the tyres. Whole car incl. tyre bottoms inside the frame at first/mid/last. No parts move.

**2 v3_front** (4.619-9.301). One shot replaces s6 + v2_frontin.
- Camera: 4.619 az 36, el 13, dist 5.2, target (0,-1.7,0.75) -> 6.960 az 24, el 18, dist 5.0, target (0,-1.8,0.65) `lin`
  -> 8.130 az 12, el 14, dist 2.4, target (0,-2.10,0.36) -> 9.301 az 6, el 13, dist 2.2, target (0,-2.12,0.34) `lin`.
- Parts: fb home -> (0,-0.60,0.12) over 4.70-5.79 (slides off the nose into clear black), then -> OFF (0,-0.6,1.6) over
  5.79-6.96 (out of the top of frame before the push). hl home -> (0,-0.30,0.25) over 5.20-5.79, -> OFF 5.79-6.96.
  hood deg 0 -> 0.85 x open_deg over 5.79-7.20, hinge only. Swap car -> base on the frame fb starts (4.70).
- Hold 8.13-9.30 (drift) on the structure behind the bumper + frunk.

**3 v3_fb** (9.301-13.983). Front bumper alone on black, at its HOME coordinates, car not rendered (keep the light rig
sized on the car: load base with `visible: [0,0]` or pass its bbox as light_ref, so exposure matches the car shots).
- Camera: 9.301 az 14, el 16, dist 3.0, target (-0.02,-1.98,0.28) -> 11.642 az 18, el 30, dist 3.3, target
  (-0.05,-2.10,0.30) -> 13.983 az 22, el 30, dist 3.15, same target `lin`. Looks down 30 deg so the pieces spread along
  the frame HEIGHT.
- Phase 1, 9.301-10.471: `front_bumper` (assembled, one object) shows its INNER face: spin [180,0,0,1] -> [162,0,0,1]
  `lin` (slow drift, brackets/ducts readable). Z turn is safe here: no car in the scene, sweep radius 1.13 m < 3 m.
- Phase 2, 10.471-11.642: spin [162,0,0,1] -> [0,0,0,1] (turns to its outer face, at home pose on 11.642).
- Swap on 11.642: `front_bumper` visible [start, 11.642), fb_stripped + 10 pieces visible [11.642, end]. Do it on the
  first frame the pieces move (fb_stripped's bbox is 3-4 cm larger than the assembled scan's, motion hides it).
- Phase 3, 11.642-12.813, offsets in m from home (start staggered 0 / 0.08 / 0.16 / 0.24 s in this order):
  fb_stripped (0,0,0) | fb_hl_trim (0,0,+0.95) | fb_markers (0,0,+0.45) | fb_fog_l and fb_fog_r (0,-0.45,+0.22) |
  fb_fogtrim_l and fb_fogtrim_r (0,-0.45,-0.25) | fb_center_cover (0,-0.55,0) | fb_center_carbon (0,-0.55,-0.55) |
  fb_radar (0,-0.95,+0.05) | fb_towhook (0,-0.95,+0.05). No x offsets (width is the limit) and no spins.
- Phase 4, 12.813-13.983: hold, camera drift only.
- Fit (computed from bboxes at az 18 / el 30 / dist 3.3): the exploded set spans ~76 % of frame width and ~52 % of the
  height, centred; nearest piece (radar) 2.5 m from the lens.

**4 v3_side** (13.983-16.324). Camera, one continuous track: t0 az 62, el 20, dist 4.0, target (0.85,-1.25,0.48) -> t1
az 96, el 16, dist 5.2, target (0.90,0.10,0.38). Parts: fe 14.05-14.75 -> OFF; ssf + ssr 14.75-15.45 -> OFF; fin
14.95-15.65 -> OFF; 0.65 s settle. Front parts stay off (hidden if out of frame); lid stays open; mirror not keyed.

**5 v3_rear** (16.324-21.006).
- Camera: 16.324 az 145, el 14, dist 6.4, target (0,1.5,0.70) -> 18.665 az 148, el 14, dist 6.2, target (0,1.55,0.70)
  `lin` -> 19.835 az 162, el 12, dist 2.6, target (0,2.20,0.42) -> 21.006 az 168, el 12, dist 2.4, target (0,2.22,0.40) `lin`.
- Parts: wing 16.40-17.20 -> OFF; tll + tlr 16.90-17.49 -> OFF; rb (assembled) 17.494-18.665 -> OFF, straight up and
  0.35 back, fully off on phrase C when the push starts. Hold 19.835-21.006 on the rear structure.

**6 v3_rb** (21.006-25.700). Rear bumper alone, home coordinates, no car (same light rule as shot 3).
- Camera: 21.006 az 166, el 16, dist 3.0, target (0.02,2.02,0.36) -> 23.347 az 162, el 30, dist 3.3, target
  (0.05,2.12,0.38) -> 25.700 az 158, el 30, dist 3.15, same target `lin`.
- Phase 1, 21.006-22.176: `rear_bumper_forced` spin [180,0,0,1] -> [162,0,0,1] `lin` (inner face: wiring loom, brackets).
- Phase 2, 22.176-23.347: spin -> [0,0,0,1]. Swap on 23.347 to the pieces (assembled visible before, pieces after).
- Phase 3, 23.347-24.517, offsets from home: rb_diffuser_forced (0,0,-0.35) | rb_top_half1 (0,0,+0.55) |
  rb_trim_cover (0,+0.50,+0.85) | rb_reflector_l and rb_reflector_r (0,+0.55,+0.05) (they sit in the gap between the
  two halves) | rb_corner_marker_l (+0.15,0,+0.25) (lags below its hole in the upper half). No spins.
- Phase 4, 24.517-25.700: hold, drift only.

**7 v3_reassemble** (25.700-30.400). As v2.1 with lower targets: 25.700 az 128, el 16, dist 9.6, target (0,0.3,1.4) ->
LOCK 27.967 az 146, el 9, dist 7.6, target (0,0.15,0.46) -> end az 158, el 7, dist 6.6, target (0,0.2,0.42) `lin`.
All v2 movers fly home from DRIFT with `ease: in`, staggered starts as v2, land on 27.967; lid closes on its hinge;
both bumpers return as the ASSEMBLED scans (no sub-parts in this shot); base -> car swap on the lock frame.
**Final shot shows:** the complete, closed car, rear-left 3/4, slow push, full round tyres with their bottoms in frame;
fade out 29.90-30.40; then the small logo on 30.40 riding the decay to 34.6.

### v3.4 Labels (max one on screen; wording backed by scan file names / STL headers in the editlog)

| # | time (s) | title | sub | position |
|---|---|---|---|---|
| L1 | 5.80-7.50 | FRONT BUMPER REMOVED | HEADLIGHTS REMOVED | y 0.72 (as v2.1) |
| L2 | 7.55-9.27 | FRONT STRUCTURE | FRUNK · MOUNTING POINTS | y 0.72 |
| L3 | 9.40-11.05 | FRONT BUMPER | SCAN · 14,996,520 TRIANGLES | top band y 0.12 |
| L4 | 11.70-13.95 | FRONT BUMPER PARTS | FOG LIGHTS · RADAR · TRIM COVERS | top band y 0.12 |
| L5 | 17.80-19.25 | REAR BUMPER REMOVED | TAIL LIGHTS REMOVED | y 0.72 |
| L6 | 19.30-20.97 | REAR STRUCTURE | EXHAUST · CRASH BEAM · MOUNTS | y 0.72 |
| L7 | 21.10-22.75 | REAR BUMPER | SCAN · 14,993,289 TRIANGLES | top band y 0.12 |
| L8 | 23.40-25.65 | REAR BUMPER PARTS | DIFFUSER · REFLECTORS · TRIM COVER | top band y 0.12 |

L2/L6 wording is v2.1's (named after looking at the renders). L3/L7 counts are the raw assembled-bumper STL headers
already used in v2.1. No label over the side or the reassembly. Bumper-shot labels go in the top band because the lowest
piece (centre carbon / diffuser) reaches ~75 % down the frame. Check 4 frames per label window for a part crossing it.

### v3.5 Diff against v2.1, holds, budget
- Moved: opener cut 6.967 -> 4.619; side 15.20-18.667 -> 13.983-16.324; rear starts 16.324 (was 18.667).
- Merged: s6_frontopen + v2_frontin -> v3_front. Added: v3_fb, v3_rb. Dropped: nothing. Reused renders: none.
- Holds > 0.75 s: v3_front 8.13-9.30 (read L2); v3_fb 9.30-10.47 (inner face) and 12.81-13.98 (read the pieces);
  v3_rear 19.84-21.01 (read L6); v3_rb 21.01-22.18 and 24.52-25.70; logo. All have camera drift.
- Budget: car shots 332 f x ~25-30 s = ~2.5 h; bumper-only shots 147 f x ~12 s (no car) = ~0.5 h. If time remains, render
  shots 3 and 6 at real 30 fps (lesson: minterpolate smears fast part moves; the 162 deg turn is the fastest move here).
- Before assembly: first/mid/last sheet + edge-touch per shot, per-frame luma scan, persistent data off.

### v3.6 Open questions for the editor
1. Spin direction/sign in shots 3 and 6: confirm on one preview frame that spin 180 shows the inner face upright to the
   lens and spin 0 equals the home pose (needed for the invisible swap).
2. If the 8-beat front shot reads rushed on the structure hold, take 2 beats from phase 1 of v3_fb (start the turn at
   once), not from the explode hold.
3. fb_markers and fb_hl_trim are single objects spanning both sides: they can only lift as one piece (planned so).
4. v2 question 3 still stands (skirts beside the sill): now that the sill/tyres are complete, check the side sheet.

---

## v4 direction (2026-11-13, scene director; checks the editor's draft `shots_v4.py`)

Reviewer on v3: add the rear-wing-removed section; rear bumper clips tail lights + wing on its way off; exhaust sections after the bumper; parts leave the screen; new song (Sector Shift edit, 140 BPM, bar n at 3.4286 + 1.7143 n s, frame = round(t x 30)).
Looked at: preview/v4_*.png (30 %, 6 frames each; only v4_rear and v4_exh post-date the 02:59 specs, the rest are one iteration old), v3_fb / v3_rb sheets, shots_v4.py, tools/pathcheck.py. Inventory change: rear gains 3 exhaust states + 4 exhaust part scans, so the rear is now clearly the richest region and holds bars 9-19.
Order is kept as drafted (travel front -> left side -> rear, one continuous sequence per section; exhaust directly after the bumper comes off = rule C "move in on what is behind it", same wide -> close -> bumper-alone pattern as the front). Four changes to bars / shots, marked CHANGE.

| bars | frames | id | section | single focus | must be in frame | label (one at a time, clear black, `shadow`) |
|---|---|---|---|---|---|---|
| -2..0 | 0-103 | v3_whole REUSE (72 f, src_fps ~20.2) | whole | entire car, front-left 3/4, push | whole car incl. tyre bottoms | none; fade-up <= 0.8 s |
| 0-2 | 103-206 | v4_front NEW | front | bumper off ON the drop, then headlights, then lid on its hinge | whole car + parked fb + hl, no part touching an edge | L1 bar 1-2: FRONT BUMPER REMOVED / HEADLIGHTS REMOVED |
| 2-4 | 206-309 | v4_frontin NEW | front | structure behind the bumper (frunk tub, lower structure) | full structure width, both corners; fb/hl not loaded | L2 bar 2.25-4: FRONT STRUCTURE / FRUNK · MOUNTING POINTS |
| 4-7 | 309-463 | v3_fb REUSE (73 f, src_fps ~13.9) | front | front bumper alone -> its 10 pieces | all pieces (as v3) | L3 bar 4-5.3, L4 bar 5.55-7: v3 wording, L4 at y 0.84 |
| 7-9 | 463-566 | v4_side NEW | left side | fender, then skirts, then fin | whole left side wheel to wheel + the 4 parts | none |
| 9-10 | 566-617 | v4_wing NEW (CHANGE 1) | rear | wing lifts straight up off the deck on bar 9 | whole rear half + parked wing | none |
| 10-11 | 617-669 | v4_wingin NEW (CHANGE 1) | rear | deck where the wing sat (state "Rear End Wing Removed") | mount area fills the width; wing not loaded | L5: REAR WING REMOVED / sub see Q1 |
| 11-13 | 669-771 | v4_rear NEW (CHANGE 2) | rear | tail lights out, then bumper slides back and clears | rear half + tll, tlr, rb parked; wing not loaded | L6 bar 12-13: REAR BUMPER REMOVED / TAIL LIGHTS REMOVED |
| 13-16 | 771-926 | v4_exh NEW (CHANGE 3) | rear | exhaust, one state per bar: Exhaust On -> Cats On -> No Exhaust | the capture fills ~80 % of width; every exhaust part parked in frame, none over the bay | L7 / L8 / L9, one per bar (below) |
| 16-19 | 926-1080 | v3_rb REUSE (74 f, src_fps ~14.05) (CHANGE 4) | rear | rear bumper alone -> its pieces | all pieces (as v3) | L10 bar 16-17.3, L11 bar 17.55-19: v3 wording, L11 at y 0.84 |
| 19-22 | 1080-1234 | v4_reassemble NEW (CHANGE 4) | whole | every part home through the fill, LOCK on bar 20 (frame 1131), then hero push | every mover inside the frame on every frame | none; fade 0.5 s into 1234 |
| 22-24 | 1234-1337 | logo (720 px card) | - | logo on a kick, rides the fade | - | - |

**CHANGE 1, wing (bars 9-11): split the draft's single push into wide + close.** The draft ends at 4.0 m with the wing hovering 0.6 m over the deck: in the preview the wing lies across the deck it is meant to reveal and the mounts never get big enough to read. Apply the draft's own rule: bar 9-10 wide (az ~152, dist ~6.0, wing home -> up over 3 kicks, 1 kick settle, wing ends in frame); bar 10 hard cut to a close shot of the deck (dist ~2.2-2.6, high rear 3/4, slow drift, wing not loaded), labelled. This is the "rear wing removed section" the reviewer asked for.

**CHANGE 2, rear wide (bars 11-13): the clipping note is a screen-space problem too.** pathcheck proves 3D clearance only. In the 03:00 preview the parked bumper (top right) still overlaps the hovering wing and sits on the right tail light on screen, which will read as the same clipping; the left tail light is within ~1-3 % of the left edge at frames 43 and 54. Fix: (a) do not load the wing here (it left in the previous section, same convention as fb/hl in v4_side); (b) tail lights 0.55 m out instead of 0.75, or pull back, so each keeps >= 5 % margin; (c) park the bumper where its silhouette overlaps neither tail light nor the body: alternative to "slide back then rise" is slide back ~1.1 m and lower it into the empty black under the tail (Miata ND v3 lesson). Test = mask overlap of each parked part against the others on every frame, plus the 3 px edge-touch test.

**CHANGE 3, exhaust (bars 13-16): retime and re-park, keep the 3 bars.** Draft swaps at 13.5 and 15, so each clean state is readable for only 2 kicks (0.86 s). Use 12 kicks as: k0-2 hold "Exhaust On" (L7) | k2-3 tip assembly off | k3-5 catback off | k5-8 hold "Cats On" (L8, swap frame stays the frame the tips start to move) | k8 (bar 15) swap, both cats off by k9.5 | k9.5-12 hold "No Exhaust" (L9). In the preview the catback (EX 0, 0.50, 0.62) ends directly in front of the bay and hides the No Exhaust state: park it clear of the bay silhouette (out the back, then down into the black below, or stacked above under the tip assembly), cats up-left / up-right. Start tighter (the capture is ~45 % of frame width at 3.8-3.9 m, with loose islands left and right in frame 1: crop the islands or frame inside them). Native 30 fps as drafted.
Labels (titles = state file names, subs = part file names): L7 EXHAUST ON / TIP ASSEMBLY · CATBACK; L8 CATS ON / LH CAT · RH CAT; L9 NO EXHAUST / ENGINE BAY. v3's "REAR STRUCTURE / EXHAUST · CRASH BEAM · MOUNTS" is dropped (its push-in shot no longer exists).

**CHANGE 4, bars 16-22: rear bumper alone 16-19 (was 16-18), reassembly 19-20 (was 18-20).** v3_rb is a 4.68 s four-phase render; in 2 bars it plays 1.37x fast (the 162 deg turn in 0.86 s, L11's 34-char sub gets ~50 frames, the Sera minimum) and it would speed up exactly where the music goes half-time. At 3 bars it plays 7 % slower than v3, the same as v3_fb at bars 4-7. The fly-home then takes the one-bar fill (stagger 0.06 s, native 30 fps for bar 19-20) and locks on the second drop. Camera: the 02:57 preview has the rear bumper cut by the right edge and the car by the left while parts are still out (push 12.5 -> 7.6 m before the lock). Hold wide (drift only) until the lock, then push 20-22. Fallback if the one-bar fly-home previews rushed: keep the draft's 18-20 and start v3_rb at render frame ~19 (drop the inner-face drift) so two bars play at native speed.

Smaller notes on the draft
- v4_front: whole (ends az 36, 7.6 m) -> front (az 34, 8.6 m) is a cut OUT on the same axis on the drop, and the car is ~60 % of frame width. Start closer (~6.6-6.8 m, target toward the nose) so the drop is a cut IN and car + parked parts fill ~85 %. pathcheck skips hinged parts: check the lid sweep against the parked bumper at kicks 5, 6, 7 (the older preview shows them overlapping on screen).
- v4_frontin: the 02:56 preview clips the right side of the structure in all 6 frames while the left has margin. Recentre / start ~3.6 m.
- v4_side at 9 m puts a 4.95 m car at ~61 % of width and the fender / skirts / fin read as slivers. ~6.3 m (85-90 %), low enough that the skirts read along the sill.
- v3_fb / v3_rb at linear retime put "pieces come off" on beat 3 of bars 5 and 17: confirm a kick there, nudge with src_fps (not speed).
- Bars 8 and 12 pass mid-shot (cuts on 7, 9, 11, 13). If the accent table shows a new layer / crash on bar 8 or 12, tell me before rendering.
- Length 44.57 s against the "scan-only reels near 20 s" lesson: accepted because the song edit is the user's and no shot holds on sparse data; nothing in bars 0-20 should sit still for more than 3 kicks.

Reuse vs render: reuse v3_whole, v3_fb, v3_rb (retime only). New: v4_front, v4_frontin, v4_side, v4_wing, v4_wingin, v4_rear, v4_exh, v4_reassemble (154 f, was 205).
`ive director` will flag whole/front, wing/wingin/rear, the three exhaust states (same-camera swaps) and fb/rb alone: intended, one sequence per section.
Before assembly: first/mid/last sheet + edge-touch per shot, EVERY frame of v4_rear / v4_exh / v4_reassemble for edge-touch and part-on-part overlap, 4 frames per label window, per-frame luma scan, cuts and the lock measured on the decoded kick band.

Open questions
1. L5 sub: use MOUNTING POINTS only if the 10-11 close render shows the mounts unmistakably; otherwise REAR WING · 7,235,817 TRIANGLES (STL header, clips.md). Also check that close-up for black holes where the wing sat (Mazda 3 thin-part fill lesson).
2. "Exhaust after the bumper" is read as after the bumper comes OFF. If the reviewer meant after the bumper-parts explode, swap the two blocks (v3_rb 13-16, v4_exh 16-19 with swaps on bars 17 and 18); nothing else moves.
3. Are the exhaust part scans' parked poses clear of each other (pathcheck covers clean3 STLs: are ex_* in clean3)?
