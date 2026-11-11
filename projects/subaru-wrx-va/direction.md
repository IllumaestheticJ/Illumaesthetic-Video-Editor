# Subaru WRX VA scan reel: scene direction v1 -> v2

Written by the scene-director agent (stage 1, `.claude/agents/scene-director.md`) on 2026-11-11.
Inputs: the user rule "order by scan features", the parent v2 brief (rules 1-8) and the user addendum (A-D: cropping,
one sequence per section, bumper-removed as the hero beat with labels, open states only where scanned).
Stage 2 (shot-by-shot camera, part keys, hold list and render budget) is in `director.md`.

What I looked at: `clips.md`, `project.yaml`, `editlog.jsonl`, `feedback.jsonl`, `review.md`, all of `knowledge/lessons.md`,
the regcheck sheets (`all_sheet`, `comp_sheet`, `hd_sheet`, `wb2_sheet`, `hoodopen_4mm_sheet`, `fbump_2mm_sheet`,
`scoop_2mm_sheet`, `eb_0.00.png`), 8-frame contact sheets of all nine renders, and first/middle/last frames of every
render I reuse. I also zoomed into the front structure that `s09_explode` frames 25-30 expose. The prep bboxes in
`blend/*.json` give part centres in metres.
`python -m ive director` on v1 flagged these repeated views: s01~s02 (IoU 0.78), s01~s07 (0.68), s01~s08 (0.72) and
s02~s08 (0.67). It also flagged 1.1 s of dead frames in s09 and "no focus" on every clip.

## 1. Feature inventory

Frame: nose +X (2.32 m), tail -X (-2.29 m), left +Y, ground z 0, roof 1.445 m.

| region | scans (registered to the car) | what the data really shows | richness |
|---|---|---|---|
| **Front: bumper** | `fbumpremoved` (2.1 mm), `fbump` bumper only (2.9 mm, inside + outside), `fogL`/`fogR` bezels (2.5 mm) | Bumper part with a scanned inner face. Brackets and fog housings are visible from behind (fbump sheet, frame 4). With the bumper off, the captured front end is exposed: headlight housings seen from below and behind, a horizontal member across the nose, a lower slatted/finned panel, and brackets at the corners. At 4 mm it is ragged at the bumper seam | **highest**: 1 state + 3 parts |
| Front: hood | `scoop` part (5.7 mm*, 89 % within 15 mm), `scoopremoved` state (1.7 mm) | Hood scoop part, plus the hood with the scoop opening as captured. In `s09` f25 the opening shows an upright box/duct | 1 state + 1 part |
| Engine bay | `hoodopen` (1.7 mm) + the propped hood from `fbumpremoved` -> `hood2_4mm` | Hood propped and engine bay captured (hd_sheet). The engine bay has dark holes and the hood underside is ragged | 1 state |
| Side | full car only | Doors, side skirts, both wheels (spokes read well at 2 mm). No state and no part | low |
| Wheels | full car only (`car_2mm`) | Front and rear wheels with spokes; the v1 s03 close-up reads well | low (subject, not a state) |
| Rear: wing | `wing` = uprights + blade underside (1.9 mm) + the car's own blade top (`wingfull_2mm`) | The STI wing is the car's single most recognisable silhouette, and its underside is scanned. **No "wing removed" state exists**: the lid's foot pads under the uprights are unscanned (wing_split note; black patches in wb2 frame 1) | signature + 1 part (fill scan) |
| Rear: trunk | `trunkopen` (1.9 mm), `rear` closed (1.8 mm) -> `trunk_4mm` | Lid open (lid underside scanned) and the cavity partly captured: the floor shows, but much of the cavity renders black or ragged (comp_sheet 3-4) | 1 state, weak interior |
| Top | full car | Roof, hood scoop and wing from above. No state | low |
| Weak data (keep off) | | Headlight lens edges are ragged, the grille mesh is ragged, the trunk cavity is black, the wing foot pads are unscanned, and the bumper-removed seam is ragged at 4 mm. The rear plate is deplated to a blank slab | |

\* scoop median is high because it is a small curved part; the red-over-silver render sits on the hood.

**Signature features:** the hood scoop, the front aero/fog bezels and the STI wing.
**Richest region:** the front, with 2 states (bumper removed, scoop removed) and 4 parts (bumper, two fog bezels, scoop),
plus the engine bay next to it.

## 2. Order (front -> side -> rear, one continuous sequence per section)

| # | beats | shot | section (one sequence each) | scans used | feature shown | why here (inventory) | label (HUD) |
|---|---|---|---|---|---|---|---|
| 1 | b0-b6 | `s01_front34` (reuse, src frames 0-41) | WHOLE CAR (front 3/4) | car_4mm | Whole car: scoop, grille, fog bezels, wheels | Rule 4 says to open on the whole car. The front carries the strongest data, so the opener frames that end (scene-director rule). Motion from frame 1 | none |
| 2 | b6-b12 | `s06_hood` (reuse) | ENGINE BAY | hood2_4mm (hoodopen + propped hood) | Propped hood, engine bay | A real captured open state (1.7 mm). It sits before the bumper so the progressive explode is never undone mid-front | `HOOD OPEN` b7-b11 |
| 3 | b12-b26 | **`n1_bumper` (NEW)** | FRONT BUMPER (**hero**) | explode_base_4mm (bumper-removed, as captured) + fbump_nofog_2mm + fogL/R_2mm (+ scoop, wing at home) | Fog bezels come out, then the bumper comes off forward into black and flips 180 deg to show its scanned inside. It then slides out of frame while the camera moves in on what the bumper-removed scan captured | Richest region, so it gets the longest scene (14 beats, 6.3 s). Addendum C | `FRONT BUMPER REMOVED` b13-b17 -> `BUMPER · SCANNED INSIDE + OUT` b17-b20 -> behind-bumper label b21-b25 (verified, see director.md) |
| 4 | b26-b30 | **`n2_scoop` (NEW)** | HOOD (scoop) | explode_base_4mm (scoop removed, as captured) + scoop_2mm | The scoop lifts straight up off the hood and silhouettes on black; the opening shows below | Second front state/part. It stays on the front before travelling | `HOOD SCOOP REMOVED` b27-b29 |
| 5 | b30-b34 | **`n_side` (NEW)** | SIDE (+ rear wheel) | car_2mm | Lateral track along the left side, door -> rear wheel -> rear quarter. Nose never in frame | Travel bridge front -> rear. Side data is thin, so it gets 4 beats | none |
| 6 | b34-b42 | **`n3_wing` (NEW)** | REAR: WING | car_2mm | Rising push from under the blade (scanned underside + uprights) to blade level; whole wing in frame | The section change at b34 moves to the rear. The wing is the signature feature, so it gets 8 beats. **No removal** (see open question 1) | none |
| 7 | b42-b46 | `s07_trunk` (reuse, src frames 0-27 only) | REAR: TRUNK | trunk_4mm (trunkopen state) | Lid open, cavity | A real captured state (1.9 mm), but weak data, so 4 beats, wide-ish and short. Closed -> open order (wing on the closed lid first, then the lid opens) | `TRUNK OPEN` b43-b45 |
| 8 | b46-b54 | **`n4a_reassemble` (NEW)** | TOP / WHOLE CAR (wide) | explode_base_4mm + bumper, fogs, scoop + wingfull at home | High overhead-side wide, nose up the frame, whole car. The front parts that came off in 3-4 fly home and the last one locks on the b54 kick | Temerario order: progressive explode -> wide -> reassembly. Lock on b54, the strongest kick of section 2. This is the only top-down view | none |
| 9 | b54-b58 | **`n4b_clean` (NEW)** | same shot, continued | car_4mm (clean full car) | Same camera continues; fades to black b56-b58 | C5 lesson: swap to the clean car on the lock kick so the last frame has no composite trim lines | none |
| 10 | b58-end | `logo` (rebuilt SMALL) | - | - | Small ILLUMAESTHETIC logo (~30 % width) fades in on black | Rule 7 | - |

Each section appears in exactly one continuous run: whole car (1), engine bay (2), front bumper (3), hood (4), side (5),
rear (6-7), top/reassembly (8-9). Wheels appear inside wide shots only and no longer have a shot of their own.

## 3. Music map (132.4 BPM, b_k = 0.0567 + 0.4533 k, cut frame = round(b_k*30))

| cut | beat | s | frame | what lands |
|---|---|---|---|---|
| open | b0 | 0.057 | (0) | whole car, fades up 0.6 s |
| 1 | b6 | 2.776 | 83 | hood open |
| 2 | b12 | 5.496 | 165 | bumper section begins; bezels move on b12.5-b13, bumper moves from b13.5 |
| 3 | b26 | 11.842 | 355 | scoop |
| 4 | b30 | 13.656 | 410 | side track |
| 5 | **b34** | 15.469 | 464 | **section change (half-time kicks): travel reaches the rear, wing** |
| 6 | b42 | 19.095 | 573 | trunk open |
| 7 | b46 | 20.909 | 627 | wide fully-exploded view, parts start home on b48 |
| 8 | **b54** | 24.535 | 736 | **last part locks home; swap to clean car** |
| 9 | b58 | 26.348 | 790 | small logo (track's last hit b64 29.07, ends ~30.77 s) |

Length is unchanged at 923 frames (30.77 s). Music is unchanged.

## 4. Diff against v1

| v1 shot | v2 | why |
|---|---|---|
| s01_front34 (b0-b8, 1.37x) | **kept**, b0-b6, speed 1.0, src frames 0-41 only | First, middle and last frames have the whole car in frame. Later frames (42-74) push the tail to the edge, so they are cut |
| s02_rear34 (b8-b16) | **dropped** | Director flags s01~s02 (0.78) and s02~s08. It is a turntable that repeats the opener's framing, and the rear section is now wing + trunk |
| s03_wheel | **dropped** | The front bumper corner is in frame (contradicts the bumper being off from b13). The wheel is cut at the frame edges, which reads as a clip. The side is now `n_side` |
| s04_front (grille/fog ECU) | **dropped, merged into n1** | Same subject as the bumper section (rule 3) |
| s05_wing | **dropped, replaced by n3_wing** | Cuts the car and wing at the frame edge (user example). The new shot keeps the whole wing in frame |
| s06_hood | **kept**, moved b28 -> b6, speed 1.32 | Real state; whole car stays in frame through its last frame |
| s07_trunk | **kept, trimmed** to src frames 0-27 (speed 1.0) | Later frames push the car off the right edge. The early frames are a straight high rear view, not the opener's front 3/4 (re-check the director flag on v2) |
| s08_topdown | **dropped** | Rotating top-down that shows nothing new; flagged against s01 and s02 |
| s09_explode | **dropped, replaced** by n1 + n2 (sectioned, close) + n4a/n4b (reassembly) | v1 separates every part at once in one wide orbit, Z-spins the bumper, and has 1.1 s of dead frames |
| logo (78 % width) | **rebuilt small** (~30 % width) with a fade-in | Rule 7 |

**Reusable as-is (order or speed only):** s01 (trimmed by dur), s06 and s07 (trimmed by dur).
**New renders:** n1_bumper, n2_scoop, n_side, n3_wing, n4a_reassemble and n4b_clean. That is 305 frames, about 61 min at ~12 s/frame,
plus two verification stills (~30 s). Full specs are in `director.md`.

## 5. Final v2 timeline (paste into project.yaml `timeline:`)

`beats:` for v2 = `[0.057, 2.776, 5.496, 11.842, 13.656, 15.469, 19.095, 20.909, 24.535, 26.348, 29.068]`

```yaml
timeline:
  - id: s01_front34      # b0-b6 WHOLE CAR, front 3/4, src frames 0-41 (later frames push the tail to the edge)
    section: whole car
    focus: whole car, front 3/4
    beat: 0
    src: /home/user/media/subaru-wrx-va/renders/s01_front34
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 2.7333          # 82 frames (first clip one frame short)
    vf: "fade=t=in:st=0:d=0.6"
  - transition: {type: cut, note: "b6 kick 2.776 (f83)"}
  - id: s06_hood         # b6-b12 ENGINE BAY, captured hood-open state
    section: engine bay
    focus: engine bay under the propped hood
    beat: 6
    src: /home/user/media/subaru-wrx-va/renders/s06_hood
    src_fps: 15
    interpolate: true
    speed: 1.32
    dur: 2.7333          # 82 frames
  - transition: {type: cut, note: "b12 kick 5.496 (f165)"}
  - id: n1_bumper        # b12-b26 FRONT BUMPER (hero): bezels out, bumper off + flip (inside), push in on the bumper-removed front end
    section: front bumper
    focus: front bumper, then the front end behind it (fbumpremoved)
    beat: 12
    src: /home/user/media/subaru-wrx-va/renders/n1_bumper
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 6.3333          # 190 frames
  - transition: {type: cut, note: "b26 kick 11.842 (f355)"}
  - id: n2_scoop         # b26-b30 HOOD: scoop lifts off, opening below
    section: hood
    focus: hood scoop and the scoop opening
    beat: 26
    src: /home/user/media/subaru-wrx-va/renders/n2_scoop
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 1.8333          # 55 frames
  - transition: {type: cut, note: "b30 kick 13.656 (f410)"}
  - id: n_side           # b30-b34 SIDE: lateral track door -> rear wheel (nose never in frame)
    section: side
    focus: left side and rear wheel
    beat: 30
    src: /home/user/media/subaru-wrx-va/renders/n_side
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 1.8             # 54 frames
  - transition: {type: cut, note: "b34 15.469 (f464) - section change, first half-time kick"}
  - id: n3_wing          # b34-b42 REAR: wing, rise from under the blade (scanned underside) to blade level, no removal
    section: rear
    focus: STI wing uprights and blade
    beat: 34
    src: /home/user/media/subaru-wrx-va/renders/n3_wing
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 3.6333          # 109 frames
  - transition: {type: cut, note: "b42 kick 19.095 (f573)"}
  - id: s07_trunk        # b42-b46 REAR: captured trunk-open state, src frames 0-27 (straight high rear)
    section: rear
    focus: open trunk lid and cavity
    beat: 42
    src: /home/user/media/subaru-wrx-va/renders/s07_trunk
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 1.8             # 54 frames
  - transition: {type: cut, note: "b46 kick 20.909 (f627) - wide fully exploded"}
  - id: n4a_reassemble   # b46-b54 TOP/WIDE: whole car, nose up; bumper/fogs/scoop fly home, last lock on b54
    section: top
    focus: whole car reassembling
    beat: 46
    src: /home/user/media/subaru-wrx-va/renders/n4a_reassemble
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 3.6333          # 109 frames
  - transition: {type: cut, note: "b54 kick 24.535 (f736) - swap to the clean car, same camera"}
  - id: n4b_clean        # b54-b58 same camera continues on the clean full car, fade to black
    section: top
    focus: whole car, assembled
    beat: 54
    src: /home/user/media/subaru-wrx-va/renders/n4b_clean
    src_fps: 15
    interpolate: true
    speed: 1.0
    dur: 1.8             # 54 frames
    vf: "fade=t=out:st=0.9:d=0.9"
  - transition: {type: cut, note: "b58 kick 26.348 (f790) - small logo"}
  - id: logo             # small ILLUMAESTHETIC (~30 % width) fading in on black; rebuild logo_card.sh with scale=324 + fade in 0.5 s
    beat: 58
    src: /home/user/media/subaru-wrx-va/logo_card.mp4
    dur: 4.4667          # 134 frames -> 923 total
```

HUD (Remotion `ScanHUD`, `kind: label`, frames are absolute output frames; x 0.08, y 0.74, align left. Keep them off the
silhouette and change y per shot after a still check):

| text (title / sub) | beats | frames (from, duration) | over |
|---|---|---|---|
| `HOOD OPEN` | b7-b11 | 97, 54 | s06_hood |
| `FRONT BUMPER REMOVED` | b13-b17 | 178, 55 | n1 (bezels out, bumper leaving) |
| `BUMPER` / `SCANNED INSIDE + OUT` | b17-b20 | 233, 41 | n1 (bumper flipped, inner face to camera) |
| behind-bumper label (text decided by the verification still, see director.md) | b21-b25 | 287, 55 | n1 push-in |
| `HOOD SCOOP REMOVED` | b27-b29 | 369, 27 | n2_scoop |
| `TRUNK OPEN` | b43-b45 | 586, 28 | s07_trunk |

No numbers are shown on screen. Every label names a captured state (from the scan file names, which were checked as
registered) or a surface you can see in the frame.

## 6. Open questions for the editor / user (not guessed)

1. **Wing removal.** The parent brief suggested lifting the wing at the rear. No "wing removed" state exists. `Wing.stl`
   holds only the uprights and the blade underside, and looks like a fill scan of the mounted wing. The lid's foot pads
   are unscanned, so lifting the wing would expose holes and imply a removal we have no scan of (lesson: honda-civic-11 /
   honda-s2000). v2 shows the wing as a held detail without removing it. If the user confirms the wing was physically off
   for `Wing.stl`, n3 can add a lift: wingfull_2mm keys up +0.6 m, then a 100 deg tip about Y. That costs no extra frames,
   but the lid pads stay black.
2. **Fog bezels.** Were they physically removed (own STLs in "Fog Bezel and Hood Scoop Scans"), or scanned in place?
   If in place, swap `fbump_nofog_2mm` + `fogL/R_2mm` for `fbump_2mm.blend` (bumper with bezels) in n1/n4a. The only cost
   is a re-render of n1/n4a if this is decided after they render.
3. **Behind-bumper label wording.** From v1 s09 f25-30 I can see the headlight housings from below and behind, a
   horizontal member across the nose and a lower finned panel. I could not confirm part names at 4 mm, 810 px. The
   verification still in director.md decides the label. If unsure, use the fallback, which names no part.
4. **4 mm close-up.** The n1 push-in on explode_base_4mm stops at ~2.2 m so the 4 mm facets don't show. A 2 mm front
   composite (`explode_base` rebuilt at 2 mm and cropped to x > 1.0 m) would allow a closer end. This is optional and the
   editor decides.
5. **Hood/trunk state jumps.** The hood is open in shot 2 and closed in 3. The trunk is closed in 6 and open in 7, then
   closed again in 8. These are separate captured states shown as states. No closed scan is animated open.
