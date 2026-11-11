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
