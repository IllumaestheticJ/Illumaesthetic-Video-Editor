# Porsche Macan (Electric) - director's shot plan, v2

Stage 2 of the scene direction. It keeps the scene order from `direction.md` unchanged:
- whole car
- front exterior
- wheels
- engine bay
- **front bumper removed**
- side (left)
- rear exterior
- **rear bumper removed** + boot
- reassembly
- logo

Inputs read:
- `knowledge/lessons.md` and `style-guide.md`;
- `training/references/README.md` (Temerario: a progressive explode over about half the reel, long held moves, extreme close-ups, a small logo);
- `project.yaml`, `editlog.jsonl`, `timing.json`, `tools/shots.py` / `shot.py` / `build.py`;
- contact sheets of every existing render (see direction.md), plus `chk/behind_bumpers.jpg`.

There is no `feedback.jsonl`. The coordinator relayed the user's v2 rules and addendum A-D; those are the notes this plan answers.

`python -m ive director projects/porsche-macan/project.yaml` fails because `final/s1_front` doesn't exist yet (the s1/s2/s8 finals were never rendered). This plan is built from the sheets, not from that report. Re-run the tool after v2 is assembled.

Every camera below was checked with a pinhole projection of the car's bbox: 20.25 mm sensor width, 1080x1920. The first, middle and last poses keep the subject inside 40-70 px margins, unless the subject is meant to fill the frame. A bbox is conservative, so **render the 30 % preview (first / mid / last frame) of each shot and look at it before the final**. That costs about 21 preview frames in total.

Scan frame: front = -Y, car's right = -X, metres, ground at z = 0. Part `loc` is an offset from rest, and `rot` is in degrees about the part's pivot: the bbox centre, or the fitted hinge for the hood and hatch. Times are seconds from the shot start; reel time is in brackets.

## Shot table

| section | shot | reel time | focus | camera | part action (shot time [reel time]) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole | **O_whole** | 0.000-4.109 | the whole car, closed | low front-right 3/4, orbit about c=(0,-0.3,0.6): angle -40 -> -30 deg, r 8.9 -> 8.4, h 1.3 -> 1.1, target z 0.62, 30 mm, easeout; car fills 76-80 % of the width with even margins | none; fades up 1.2 s | opener: the whole car with motion from frame 1, on the end with the most data | **re-render** (replaces the queued s1 final): 67 frames |
| front exterior | **N_face** | 4.109-8.176 | front face: left lamp -> intakes/crest -> right lamp | car3; slide at 0.95 m height, 2.4 m off the nose. loc (0.95,-4.75,0.95) -> (0,-4.8,0.95) -> (-0.95,-4.75,0.9); target (0.5,-2.3,0.72) -> (0,-2.3,0.70) -> (-0.5,-2.3,0.68); 40 mm, inout | none (bumper on, so the viewer sees it before it comes off) | the front detail; ends at the right corner, which leads to the wheel | **new**: 67 frames |
| wheels | **W_wheel** | 8.176-9.701 | front-right wheel and brake | as rendered (s3) | none | the only wheel shot; 3 mm spokes and caliper | **reuse s3 as-is** (same slot as v1) |
| engine bay | **F1_bay** | 9.701-16.310 | the bay under the hood (Hood Removed state, real) | high front-right 3/4, orbit: t0 angle -40, r 5.6, h 3.2, c=(0.2,-1.0,0.9) -> t3.3 angle -34, r 5.2, h 3.0, c=(0.1,-1.2,0.85) -> t6.6 angle -25, r 3.4, h 2.6, c=(0,-1.35,0.8); 30 mm, key 8x with smooth. First frame: front half of the car, nose in (deliberate mid-car crop). Last frame: the bay fills the width. | hood: rest until t1.525 **[11.226 hit]**, then open_deg (-54.9) on its fitted hinge by t3.3, inout | the front's first state; one continuous move over the hit-less build (lesson: no cuts in a build) | **new**: base `comp_open` + `x_hood` + `x_hatch` at rest; 103 frames |
| front bumper removed (HERO) | **F2_fbumper** | **16.310 (DROP)-20.377** | the bumper's inner face, then the **crash beam**, cooling ducts, harness and brackets behind it | t0 (2.5,-5.7,1.35)->tgt (0.2,-2.0,0.75), 32 mm: whole front incl. fender and open hood -> t1.017 (1.8,-6.4,1.25)->(0.1,-2.4,0.85), 28 mm: bumper above the nose in view -> t2.033 (0.9,-5.4,1.0)->(0.05,-2.3,0.7), 30 mm -> t4.067 (0.2,-4.6,0.78)->(0,-2.2,0.52), 30 mm: **the beam fills the width**; inout | hood open throughout. **fbumper** (see the spec below): forward 0-0.5, up + flip -160 deg about X by t1.017 **[17.327]** so its inside faces the lens; holds for the read; rises out of the top of the frame t2.033-3.0. Fender, doors, hatch and rear bumper at rest. | hero beat (addendum C) on the drop; the camera stays on the front and moves in on what is behind | **new**: base `comp_explode`; 67 frames |
| side (left) | **S1_side** | 20.377-24.440 | left fender, then FL door, then RL door: the scanned door cards, plus the arch structure (Fenders Removed) and cabin (Doors and Hood Open) behind them | left side truck front -> rear, 3.4 m off the side: t0 (4.4,-1.45,1.4)->tgt (1.0,-1.3,0.8) -> t2.033 (4.4,-0.55,1.4)->(1.0,-0.5,0.8) -> t4.063 (4.3,0.5,1.35)->(1.0,0.45,0.8); 28 mm, inout | fender: out on t0 **[20.377]** to (0.75,0.05,0.3) by t0.5, translate only. door_fl: out on t1.017 **[21.393]** to (1.0,-0.05,0.1) by t1.5, yaw 180 deg (card to the lens) by t2.2. door_rl: out on t2.033 **[22.41]** to (1.0,0.12,0.1) by t2.55, yaw 180 by t3.25. Front parts stay in their F2 end poses. | the side told front -> rear, one part per kick; the doors spin only because the card is the scanned inside (rule 5) | **new**: base `comp_explode`; 67 frames |
| rear exterior | **L_lightbar** | 24.440-25.460 | light bar, PORSCHE lettering, Macan script | as rendered (s4) | none | the signature detail, right before the rear opens | **reuse s4, trimmed**: `in: 0.95`, dur 1.0333 |
| rear bumper removed (HERO) + boot | **R1_rbumper** | 25.460-28.511 | hatch -> boot; then the **tubular crash beam and its end mounts** | t0 (1.9,5.6,1.85)->tgt (0.1,2.0,1.05), 30 mm: whole rear incl. the opening hatch -> t1.53 (1.3,5.6,1.3)->(0.05,2.1,0.65) -> t3.05 (0.95,3.95,0.8)->(0.45,2.2,0.48), 32 mm: **the left beam end + mount fill the frame**; inout | hatch: open_deg (+69.8) on its fitted hinge t0 -> t0.5 **[25.969]**. rbumper: back to (0,0.6,0.05) t0.51 -> t1.53 **[26.99]**, then slides to the car's right, out of frame, to (-1.7,0.7,0.05) by t2.3. No tip (speckly scan; rule 5). Left doors / front parts in their end poses. | hero beat (addendum C); the bumper leaves into clear black, so the camera's push-in reads the structure | **new**: base `comp_explode`; 51 frames |
| whole (reassembly) | **X_reassemble** | 28.511-30.544 | every part flies home and locks; the clean car | high, ~57 deg down from the nose: t0 (1.3,-4.9,8.1)->tgt (0.05,0.15,0.5) (all parts out, inside the margins) -> t2.033 (0.8,-4.3,7.0)->(-0.3,0.1,0.5) (assembled car centred, ~63 % width); 28 mm, inout | all parts go from their accumulated exploded pose to rest, ease "in", **lock at t1.0 [29.511, 16 ms ahead of the 29.527 kick]**; hood and hatch close on their hinges. Frames 17-37 render with base `car4.blend` and no parts (c5 lesson: clean car after the lock). | reassembly the reviewer expects (Temerario); the only moment with all parts in view, and they are going home, not separating | **new**: 37 frames, in 2 processes |
| - | **logo** | 30.544-33.600 | small ILLUMAESTHETIC logo | - | `vf` fade-out on X: `fade=t=out:st=1.63:d=0.4`; logo fades up | ends with the pad tail | `tools/logo_card.py ... --secs 3.0667 --width 320` (ffmpeg) |

### Labels (Remotion `ScanHUD`, `label` items; one at a time; top band y ~ 230-330 px, centred, 80 px inside the edges)

| text | shot | in -> out (reel s) | placement note |
|---|---|---|---|
| FRONT BUMPER REMOVED | F2 | 17.327 -> 18.800 | the bumper is mid-frame at t1.0, so the top band is black |
| CRASH BEAM | F2 | 19.360 -> 20.250 | enters after the bumper has left through the top (t >= 3.0) |
| REAR BUMPER REMOVED | R1 | 26.477 -> 27.430 | over the black above the open boot |
| MOUNTING POINTS | R1 | 27.494 -> 28.400 | the shot ends framed on the beam's end mount |

No numbers are on screen, and every word names something visible in the scan or a state scan's file name. Before delivery, read the last frame of each label.

## Concrete spec for `tools/shots.py`

The `orbit()`, `arc()` and `smooth` helpers already exist. `HOOD` / `HATCH` are `hood` / `hatch` from `hinge/*.json`.

Every part-moving shot uses **persistent data off**, which `shot.py` already does. After each final, scan every frame's mean luma (lessons: G35, A90, Miata).

```python
# timing.json -> secs
# "O_whole": 4.4, "N_face": 4.4, "F1_bay": 6.8, "F2_fbumper": 4.4, "S1_side": 4.4, "R1_rbumper": 3.3, "X_reassemble": 2.4
REST = {"loc": [0, 0, 0], "rot": [0, 0, 0]}
def k(t, loc=(0, 0, 0), rot=(0, 0, 0), ease="inout"): return {"t": t, "loc": list(loc), "rot": list(rot), "ease": ease}
def cam(t, loc, tgt, f, ease="inout"): return {"t": t, "loc": list(loc), "target": list(tgt), "focal": f, "ease": ease}
OPEN_H, OPEN_T = [HOOD["open_deg"], 0, 0], [HATCH["open_deg"], 0, 0]
# end poses carried forward (progressive state)
FB_END = ((0, -0.5, 1.70), (-160, 0, 0)); FENDER_END = ((0.75, 0.05, 0.30), (0, 0, 0))
FL_END = ((1.0, -0.05, 0.10), (0, 0, 180)); RL_END = ((1.0, 0.12, 0.10), (0, 0, 180)); RB_END = ((-1.7, 0.7, 0.05), (0, 0, 0))
hold = lambda pose: [k(0, *pose)]
rest = [k(0)]

SHOTS["O_whole"] = {"base": [CAR], "cam": arc(4.4, 8, 8.9, 8.4, -40, -30, 1.3, 1.1, c=(0, -0.3, 0.6), focal=30, tz=0.62, shape=easeout)}
SHOTS["N_face"] = {"base": [CAR_HI], "cam": [cam(0, (0.95, -4.75, 0.95), (0.5, -2.3, 0.72), 40, "lin"),
    cam(2.2, (0.0, -4.8, 0.95), (0.0, -2.3, 0.70), 40, "lin"), cam(4.4, (-0.95, -4.75, 0.90), (-0.5, -2.3, 0.68), 40)]}
SHOTS["F1_bay"] = {"base": [f"{P}/comp_open.blend"],
    "parts": [{"blend": f"{P}/x_hood.blend", "pivot": HOOD["pivot"], "keys": [k(0), k(1.525), k(3.3, rot=OPEN_H)]},
              {"blend": f"{P}/x_hatch.blend", "pivot": HATCH["pivot"], "keys": rest}],
    "cam": [orbit(6.8 * u, *(lambda e: (5.6 - 2.2 * e, -40 + 15 * e, 3.2 - 0.6 * e))(smooth(u)),
                  c=(0.2 - 0.2 * smooth(u), -1.0 - 0.35 * smooth(u), 0.9 - 0.1 * smooth(u)), focal=30, ease="lin", tz=None)
            for u in [i / 8 for i in range(9)]]}
#   (orbit signature is orbit(t, r, ang, h, c=...); unpack accordingly. Check t3.3 ~ angle -34, r 5.2.)
SHOTS["F2_fbumper"] = {"base": [f"{P}/comp_explode.blend"], "parts": [
    {"blend": f"{P}/x_hood.blend", "pivot": HOOD["pivot"], "keys": [k(0, rot=OPEN_H)]},
    {"blend": f"{P}/x_fbumper.blend", "keys": [k(0), k(0.5, (0, -0.55, 0.30), ease="out"),
        k(1.017, (0, -0.55, 0.95), (-160, 0, 0)), k(2.033, (0, -0.55, 1.0), (-160, 0, 0), "lin"),
        k(3.0, (0, -0.5, 1.70), (-160, 0, 0)), k(4.4, (0, -0.5, 1.75), (-160, 0, 0), "lin")]},
    {"blend": f"{P}/x_fender.blend", "keys": rest}, {"blend": f"{P}/x_hatch.blend", "pivot": HATCH["pivot"], "keys": rest},
    {"blend": f"{P}/x_rbumper.blend", "keys": rest}] + [{"blend": f"{P}/x_door_{d}.blend", "keys": rest} for d in ("fl", "fr", "rl", "rr")],
  "cam": [cam(0, (2.5, -5.7, 1.35), (0.2, -2.0, 0.75), 32), cam(1.017, (1.8, -6.4, 1.25), (0.1, -2.4, 0.85), 28),
          cam(2.033, (0.9, -5.4, 1.0), (0.05, -2.3, 0.70), 30), cam(4.4, (0.2, -4.6, 0.78), (0, -2.2, 0.52), 30)]}
SHOTS["S1_side"] = {"base": [f"{P}/comp_explode.blend"], "parts": [
    {"blend": f"{P}/x_hood.blend", "pivot": HOOD["pivot"], "keys": [k(0, rot=OPEN_H)]},
    {"blend": f"{P}/x_fbumper.blend", "keys": hold(FB_END)},
    {"blend": f"{P}/x_fender.blend", "keys": [k(0), k(0.5, FENDER_END[0], ease="out")]},
    {"blend": f"{P}/x_door_fl.blend", "keys": [k(0), k(1.017), k(1.5, FL_END[0], ease="out"), k(2.2, *FL_END)]},
    {"blend": f"{P}/x_door_rl.blend", "keys": [k(0), k(2.033), k(2.55, RL_END[0], ease="out"), k(3.25, *RL_END)]},
    {"blend": f"{P}/x_door_fr.blend", "keys": rest}, {"blend": f"{P}/x_door_rr.blend", "keys": rest},
    {"blend": f"{P}/x_hatch.blend", "pivot": HATCH["pivot"], "keys": rest}, {"blend": f"{P}/x_rbumper.blend", "keys": rest}],
  "cam": [cam(0, (4.4, -1.45, 1.4), (1.0, -1.3, 0.8), 28), cam(2.033, (4.4, -0.55, 1.4), (1.0, -0.5, 0.8), 28, "lin"),
          cam(4.4, (4.3, 0.55, 1.35), (1.0, 0.5, 0.8), 28)]}
SHOTS["R1_rbumper"] = {"base": [f"{P}/comp_explode.blend"], "parts": [
    {"blend": f"{P}/x_hood.blend", "pivot": HOOD["pivot"], "keys": [k(0, rot=OPEN_H)]},
    {"blend": f"{P}/x_fbumper.blend", "keys": hold(FB_END)}, {"blend": f"{P}/x_fender.blend", "keys": hold(FENDER_END)},
    {"blend": f"{P}/x_door_fl.blend", "keys": hold(FL_END)}, {"blend": f"{P}/x_door_rl.blend", "keys": hold(RL_END)},
    {"blend": f"{P}/x_door_fr.blend", "keys": rest}, {"blend": f"{P}/x_door_rr.blend", "keys": rest},
    {"blend": f"{P}/x_hatch.blend", "pivot": HATCH["pivot"], "keys": [k(0), k(0.5, rot=OPEN_T)]},
    {"blend": f"{P}/x_rbumper.blend", "keys": [k(0), k(0.51), k(1.53, (0, 0.6, 0.05), ease="out"), k(2.3, *RB_END)]}],
  "cam": [cam(0, (1.9, 5.6, 1.85), (0.1, 2.0, 1.05), 30), cam(1.53, (1.3, 5.6, 1.3), (0.05, 2.1, 0.65), 30),
          cam(3.3, (0.95, 3.95, 0.8), (0.45, 2.2, 0.48), 32)]}
SHOTS["X_reassemble"] = {"base": [f"{P}/comp_explode.blend"], "parts": [   # frames 1-16; frames 17-37: base [CAR], parts []
    {"blend": f"{P}/x_hood.blend", "pivot": HOOD["pivot"], "keys": [k(0, rot=OPEN_H), k(1.0, ease="in")]},
    {"blend": f"{P}/x_hatch.blend", "pivot": HATCH["pivot"], "keys": [k(0, rot=OPEN_T), k(1.0, ease="in")]},
    {"blend": f"{P}/x_fbumper.blend", "keys": [k(0, *FB_END), k(1.0, ease="in")]},
    {"blend": f"{P}/x_fender.blend", "keys": [k(0, *FENDER_END), k(1.0, ease="in")]},
    {"blend": f"{P}/x_door_fl.blend", "keys": [k(0, *FL_END), k(1.0, ease="in")]},
    {"blend": f"{P}/x_door_rl.blend", "keys": [k(0, *RL_END), k(1.0, ease="in")]},
    {"blend": f"{P}/x_rbumper.blend", "keys": [k(0, *RB_END), k(1.0, ease="in")]},
    {"blend": f"{P}/x_door_fr.blend", "keys": rest}, {"blend": f"{P}/x_door_rr.blend", "keys": rest}],
  "cam": [cam(0, (1.3, -4.9, 8.1), (0.05, 0.15, 0.5), 28), cam(2.4, (0.8, -4.3, 7.0), (-0.3, 0.1, 0.5), 28)]}
```

Notes:
- **F1_bay:** write its camera as 9 explicit `orbit()` keys if the lambda is awkward. The key poses: t0 = angle -40 / r 5.6 / h 3.2 / c (0.2,-1.0,0.9); t3.3 = -34 / 5.2 / 3.0 / c (0.1,-1.2,0.85); t6.8 = -25 / 3.4 / 2.6 / c (0,-1.35,0.8).
- **The bumper flips are conditional.** The -160 deg flip of the front bumper depends on its inside being scanned (direction.md Q1). If it is not, use rot (0,0,0) and the same translation.
- **Hood clearance.** The open hood's front edge sits near y -1.8, z 2.1. The raised bumper is at y -2.8, about 0.8 m clear of it.
- **Door spin clearance.** The doors spin about their bbox centres 1.0 m outboard, so the closest edge stays about 0.35 m outside the body.

### `project.yaml` timeline (whole-frame durs; the first clip is one frame short; cut k on round(t*30))

| id | src | dur (s) | frames | notes |
|---|---|---|---|---|
| O_whole | final/O_whole | 4.0667 | 122 | `vf: fade=t=in:st=0:d=1.2` |
| N_face | final/N_face | 4.0667 | 122 | |
| s3_wheel | final/s3_wheel | 1.5333 | 46 | unchanged |
| F1_bay | final/F1_bay | 6.6000 | 198 | |
| F2_fbumper | final/F2_fbumper | 4.0667 | 122 | cut on the DROP (489) |
| S1_side | final/S1_side | 4.0667 | 122 | |
| s4_lightbar | final/s4_lightbar | 1.0333 | 31 | `in: 0.95` |
| R1_rbumper | final/R1_rbumper | 3.0333 | 91 | |
| X_reassemble | final/X_reassemble | 2.0333 | 61 | `vf: fade=t=out:st=1.63:d=0.4` |
| logo | out/logo_card.mp4 | 3.0667 | 92 | `--width 320` |

Cut frames: 122+1 = 123, 245, 291, 489, 611, 733, 764, 855, 916; the reel ends on frame 1008 (33.6 s). Set `beats:` to [4.109, 8.176, 9.701, 16.310, 20.377, 24.440, 25.460, 28.511, 30.544]. Use `tools/concat_assemble.py`-style exact frames (S2000 lesson) or `ive assemble` with its cut compensation. Verify the cut-to-kick error on the decoded audio afterwards (|err| <= 1/2 frame).

## Cut list (v1 -> v2)

| v1 material | fate | reason |
|---|---|---|
| s1_front at the -42 -> -14 framing (final queued) | re-spec as O_whole | v1 framing crops the car (addendum A, rule 4) |
| s2_rear (final queued) | cut | a rear wide before the front would ping-pong; it repeats the whole-car opener; cropped |
| s4_lightbar 0-0.95 s and 1.98-2.6 s | trimmed | only the middle carries PORSCHE + Macan script; the rear section needs the time |
| s5_open (82 final frames) | cut | the front and rear states in one side-on orbit (two sections in one shot, cropped side-on mid-shot); replaced by F1 + R1 |
| s7_top (~67 final frames) | cut | a rotating top-down that shows only the roof and door slivers (rule 3) |
| s8_explode (final queued, 159 frames) | cut | every part separated at once in a wide orbit, cropped side-on (rule 2) |
| logo at 860 px | re-run at 320 px | Temerario small logo (rule 7) |

## Hold list (>0.75 s with no part moving)

| shot | span (shot t) | reason |
|---|---|---|
| O_whole | 0-4.07 | the opener: whole car, slow push and drift over the track's fade-in |
| N_face | 0-4.07 | detail slide; the camera crosses three features, with the 5.63 / 7.16 hits as passing points |
| W_wheel | 0-1.53 | detail slide (unchanged) |
| F1_bay | 0-1.525 | the approach before the hood opens on the 11.226 hit |
| F1_bay | 3.3-6.6 | push into the bay over the hit-less build; the bay is real Hood Removed data |
| F2_fbumper | 1.017-2.033 | reads the bumper's inside |
| F2_fbumper | 3.0-4.07 | **the hero read: crash beam / ducts / harness**, with the camera still moving in |
| S1_side | 3.25-4.06 | the RL card and the cabin through both openings |
| L_lightbar | 0-1.03 | detail |
| R1_rbumper | 2.3-3.03 | **the hero read: beam end + mount**. It is short; if the reviewer wants longer, take the time from L (cut L to 2 beats -> 1 beat) |
| X_reassemble | 1.0-2.03 | the clean assembled car, then the fade |

## Render budget (15 fps, ~20 s/frame on 4 cores; one job at a time)

| shot | secs | frames | approx. time |
|---|---|---|---|
| O_whole | 4.4 | 67 | 22 min |
| N_face | 4.4 | 67 | 22 min |
| F1_bay | 6.8 | 103 | 34 min |
| F2_fbumper | 4.4 | 67 | 22 min |
| S1_side | 4.4 | 67 | 22 min |
| R1_rbumper | 3.3 | 51 | 17 min |
| X_reassemble | 2.4 | 37 | 12 min |
| **total** | | **459** | **~2.6 h** |

- Previews come first: 7 shots x 3 frames at 30 % res, about 5 min.
- The comp_explode shots carry 9 parts with persistent data off. If they run at ~25 s/frame, the total becomes ~3 h.
- If time is short, drop **N_face** (-67 frames). Then O_whole runs 0-4.109, W moves to 4.109-5.63 (s3, same 46 frames), and F1 starts at 5.63 with the hood on the 7.16 hit. F1 becomes 10.7 s (161 frames, 2N-3 >= 162 -> 83 frames, +~17 min vs 103 frames). Net saving: about 50 frames.

Reused unchanged: s3_wheel; s4_lightbar (trimmed via `in`). Unused finished renders: s5_open, s7_top.

**Stop the queue now:** s7_top is finishing. The s8_explode (159 frames), s1_front (old framing, 73 frames) and s2_rear (67 frames) finals queued after it would waste ~1.7 h of the 4-core machine. Respec s1 as O_whole before it starts.

## Checks before the editor calls it done

- **Hero beats:**
  - In F2 and R1, the camera stays on its section until the cut.
  - The F2 read (~1.5 s of camera on the beam with no part moving) and the R1 read (~0.75-1.5 s) are long enough, judged from the frames.
- **States:**
  - Only scanned states appear: hood (Doors and Hood Open / Hood Removed), hatch (Fully Open), bumpers (Off / Removed), left fender (Fenders Removed x>0), and the left doors (Doors and Hood Open).
  - The right doors and right fender never move.
- **Frames:**
  - Extract round(t*30)±2 frames at every cut and confirm the framings above, first, mid and last.
  - Scan per-frame mean luma for dropouts.
- **Labels:** read the final frame of each label; each label is off by the cut.
