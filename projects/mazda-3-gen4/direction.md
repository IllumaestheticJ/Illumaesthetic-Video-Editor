# Mazda 3 (gen 4) hatch - scene direction v2 (scene-director, 2026-11-11)

Stage 1 of 2 (stage 2 = `director.md`, the shot plan). Sources read: CLAUDE.md, knowledge/lessons.md (all),
style-guide, training/references/README.md (Temerario), clips.md, project.yaml / project_v1.yaml, editlog, feedback,
director_report_v1.md, tools/shots.py + shots_v1.py, and contact sheets of every render in
`/home/user/media/work/m3/renders/final{,2}/` (scratch sheets made with tools/sheet.py), `checks/reg/wo2_0.png`.

## 1. Feature inventory (from the scans, not from the model name)

Scan frame (prepped car4.json, metres): nose = -Y, car's LEFT = +X, body x -0.97..0.97, y -2.23..2.23, z 0.08..1.53.

| region | what the data holds | states | registered parts | quality | richness |
|---|---|---|---|---|---|
| Whole car | Full Car.stl 58.4M tris -> car4 (4 mm, 3.4M) + 2 mm crops c2_front / c2_left / c2_rear | - | - | clean after jack/floor removal; tyres are rings ~10 cm off the floor (car on jacks) | base for every shot |
| Front (y < -0.6) | Kodo face: headlamps, bonnet folds, grille | none | none | grille mesh is holey (dark gaps); small gaps at headlamp top edge | low: 1 shot, whole car, grille off-centre |
| Left side (+X) | door surfacing / reflection lines, mirror, sill | "Side Skirt Door Open" = sill/jamb only below 0.86 m, no door, no cabin -> NOT a usable state | none | clean | low: 1 shot, translate only |
| Right side (-X) | same surfacing | - | - | **right rear quarter has scan ribbing**, jack-pad remnant on sill | never shown |
| Rear (y > 0.8) | tail lamps (crisp in v1 s5_tail), SKYACTIV badge, hatch, plate frame (frame only, no plate characters) | - | - | good; plate frame text is a dealer frame, no plate | medium: rear arrival + lamps |
| **Hatch top / rear wing** | Rear Wing part (Artec, y 1.33..1.69, z 1.25..1.46, ~1.18 m wide) | **Wing Removed** state (registered, median 1.05 mm) -> `comp_wingoff.blend` shows the real mounting holes/bosses on the hatch (`checks/reg/wo2_0.png`) | **Rear Wing** at identity (median 4.2 mm, 97 % within 15 mm) | wing scan is a closed shell: 49 % of its area faces down (scanned underside / mounting face) - **verify visually before planning a reveal** | **highest: the only real part-off in the data** |
| Top | roof/hatch from above | - | - | fine, nothing new | no own scene |
| Wheels / engine / interior | tyre rings only, no bay, no cabin | - | - | no data | no scene |

Not usable / not shown:
- **Hatch Upper Trim Panel** = the Rear Wing (fit 0.964, 93 % coverage) -> shown once, as the Rear Wing scan.
- **OEM Aero Kit Spoiler**: DROPPED. It does not register to this car (fitness <= 0.45, a different 1123 mm design,
  every pose intersects the hatch). Floating it over this Mazda implies it is this car's part / fits it - that is
  implied data (lesson: never imply data). With it gone there is no "stack"; the explode is the wing alone.
- **Side Skirt Door Open**: no door part, no cabin -> no door opening.
- Front/side have no parts or states -> no "panel off" at the front; nothing is removed there.

## 2. Scene order (travel front -> side -> rear, end on the rich region; no ping-pong)

Opener exception noted: the signature feature (wing) is at the rear, but the brief and the reviewer demand the WHOLE car
first and a front -> side -> rear travel, which naturally *arrives* at the wing and gives it the drop.

| # | scene | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | Whole car, front 3/4 | car4 | the whole standard car, Kodo face | reviewer: "standard full car scan - show the whole car"; brief: whole car + motion from frame 1 | b0-b8 (8) | low front-left 3/4, straight push-in, no orbit |
| 2 | Left flank | car4 | side surfacing / reflections | travel step 2; clean +X side; no states -> one short-ish scene | b8-b16 (8) | lateral track toward the rear (translation, not a turntable) |
| 3 | Rear arrival | car4 | rear end: tail lamps + hatch shape | travel step 3; tail lamps are the best rear detail; puts us behind the car for the wing | b16-b28 (12) | rear-left 3/4 swinging behind + pushing in until the rear end fills the width |
| 4 | Wing off -> mounts | comp_wingoff + rwing | wing seated, lifts ON THE DROP, real mounting holes exposed | the only registered part + state = richest region -> biggest musical moment (kick drop b36) | b28-b42 (14) | high behind-left, framed on the hatch top, pushes in on the mounts after the lift |
| 5 | The part | comp_wingoff + rwing | wing's scanned underside / mounting face | brief: show the part's inner face; underside is scanned (49 % down-facing) | b42-b52 (10) | low behind-left looking up; wing translates back over clear black (no spin) |
| 6 | Reassembly, whole car | comp_wingoff + rwing (car4 after lock) | wing returns and seats; whole car from above | Temerario: reassembly -> fade -> small logo; a high angle no other scene uses | b52-b64 (12; fade b62-b64) | high (~60 deg down) from behind-left, slow push, no orbit |
| 7 | Logo | logo card | small ILLUMAESTHETIC logo | brief: fade, then SMALL logo; music decays to ~38.2 | b64-b70 (6) | ~320 px wide (30 % width) on black |

No top-down rotation, no wide explode orbit, no text.

## 3. Music map (beat k = 0.050 + 0.5453 k; 110 BPM; frames = round(t*30))

| scene | start | beat / accent | music there |
|---|---|---|---|
| 1 | 0.000 | b0 | ambient intro, plucks every 2 beats |
| 2 | 4.412 (f132) | b8 phrase | intro |
| 3 | 8.775 (f263) | b16 phrase | intro; build starts ~11.4 (inside scene 3) |
| 4 | 15.319 (f460) | b28 phrase | build; **wing lifts on b36 = 19.682 KICK DROP (inside the shot)** |
| 5 | 22.954 (f689) | b42 kick | kicks |
| 6 | 28.408 (f852) | b52 kick | kicks; wing locks on **b60 32.770** phrase |
| 7 | 34.951 (f1049) | b64 kick | last kick b67 36.587, decay, end b70 38.223 (f1147) |

The drop is not a cut: the part comes off on the kick inside the held section shot (brief: frame the section and stay
on it; lesson 240SX: let the shot keep going into the next story beat). The cuts around it (b28, b42) are phrase/kick lines.

## 4. Diff vs v1 (project_v1.yaml) and v2-whole-car (project.yaml)

| v1 / v2 shot | v2-scan-feature plan | why |
|---|---|---|
| s1_front34 (v1 cropped turntable / v2 whole-car turntable 24->52 deg) | -> scene 1, **re-render** as straight push-in | rotations flagged as wasted (sibling Mazda note); v1 too cropped |
| s2_rear34 (rear-left orbit) | **dropped** (content folded into scene 3) | ping-pong: v1/v2 went front -> rear -> front -> side -> rear; director_report_v1: s1~s2 same view (IoU 0.7) |
| s3_lamp (v1) / s3_front (v2) | **dropped** | front shown twice; front has no parts/states; v1 70 mm close-up = "too cropped" |
| s4_flank (v1) / s4_side (v2 14 deg drift) | -> scene 2, **re-render** as lateral track | translate, not rotate; travel direction toward the rear |
| s5_tail (v1) / s5_rear (v2) | -> merged into scene 3 (new render) | one rear-end shot, not two |
| s6_wing (whole car wide, wing lifts b30-b34 in the build) | -> scene 4 (new render, section framing), lift moved to the drop | brief: frame the removed section and stay on it; richest region gets the drop |
| s7_top (rotating top-down) | **dropped** | rotation, nothing new (no top state) |
| s8_explode (wide orbit, wing + unregistered spoiler) | **dropped** -> scenes 5 + 6 | too wide; spoiler not registered (implied data); final2 render is a stopped partial (25/186 frames) |
| logo (820 px, 3.27 s) | scene 7, **re-make at ~320 px** after a fade to black | brief: fade, then small logo |

Reuse: no existing render matches (every one is an orbit, a duplicate subject, or a v1 crop). The only reusable
asset is the pipeline (car4/comp_wingoff/rwing blends, tools/shots.py helpers, logo_card.py). Fallbacks if render time
runs out: scene 2 <- `final2/s4_side` played **reversed** (camera then drifts toward the rear), src_fps = 37/4.46.

## 5. Open questions for the editor (check, don't guess)
1. **Wing underside**: render `rwing.blend` alone from below (one still, 30 %). If the underside is ragged/empty rather
   than a real mounting face, cut scene 5: scene 4 runs b28-b46 and scene 6 runs b46-b64 (wing returns from scene 4's end pose).
2. Mount close-up resolution: comp_wingoff is 4 mm + Wing Removed fill. If the holes read soft at scene 4's end pose,
   stop the push ~0.3 m earlier rather than building a 2 mm composite (c2_rear ends at y 0.8 and would show a cut edge).
3. Seams: check scene 6 frames at the lock (b60) - if comp_wingoff + seated wing shows trim lines, render the frames
   from the lock on with `car4.blend` and no part (same frame, invisible swap; c5-corvette lesson).
