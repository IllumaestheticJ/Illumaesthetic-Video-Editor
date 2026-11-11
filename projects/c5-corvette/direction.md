# C5 Corvette scan-only reel v2: scene direction (stage 1, scene-director)

2026-11-11. v1 reviewer: *"Same issue as the other first drafts. Need to focus more specifically on the removed areas and
where the useful data is."* This plan applies:
- **The parent's v2 brief:** order from this car's scan features; travel front → side → rear with no ping-pong. When a part comes
  off, the camera stays on that section and moves in on the part's inner face and mounts. Never separate everything in one
  wide shot. Zoom in (the v1 explode filled 10-12 % of the frame). No wasted rotations. Open on the whole car, moving from frame 1.
  Spin a part only when its scanned backside is worth showing, and move parts into clear background, often toward the
  camera. Only show states that have a registered state scan. End with reassembly, a fade, then a SMALL logo. No persistent
  HUD data, and Cycles persistent data off.
- **The newest user feedback, which wins where it conflicts** (lessons.md, bottom, from ferrari-296):
  - CROPPING: whole car in frame on wide shots, and the named section fills the frame on detail shots.
  - REDUNDANCY: each section appears in ONE continuous sequence.
  - BUMPER-REMOVED = HERO BEAT: own section, move in, hold, short factual label over scan shots. This replaces v1's
    "no text" brief, for labels only.
  - OPENINGS ONLY FROM DATA.
- **The re-measured kick-onset grid:** 4.117, 9.309 (drop), 13.689, 15.598 (weak), 17.024, 22.130, 26.471, 30.385, 33.314,
  34.402 (loud kick), 35.496 (biggest hit); music silent by ~39.4 s.

What I looked at: `/home/user/media/work/c5/v2/look/all.png` (state scans raw vs composite), the framing strips
`framing/v2_C.png` (A, B, F, G, H, I) and `framing/v2_A.png` (C, D, E), the v1 sheet `qc/sheet.png`, and the final-quality
frames of `renders/c5/v2_a_fb_off` and `v2_b_fb_inside`. Per-frame luma in both renders is smooth (21→31 and 19→29),
so neither has a lighting dropout.

## 1. Feature inventory (registered data only, one frame)

| region | parts (registered) | removed / open states (registered) | what the data shows (from the renders) | weak data | richness |
|---|---|---|---|---|---|
| **Front: nose / bumper** | `front_bumper` (inside AND outside, 3.8 mm) | `front bumper removed` (2.7 mm) | exposed nose structure behind the bumper (bar across the nose, radiator/headlight-pod area, wiring); the bumper's ribbed inner face | composite trim lines on the closed car at the hood/bumper seam (visible in A frame 1) | **high**: part with an inside, plus a state → hero section |
| **Front: hood / engine bay** | `hood_combo` (car hood skin + the scanned underside); hinge fitted to the open capture (front hinge, axis X at y=-2.01 z=0.86, 46°) | `C5 Supplement Hood Open` (own frame → 2.7 mm, captured 46°); `front bumper and hood removed` (9.9 % overlap, mostly newly exposed engine bay/structure) | hood opening on its real hinge, the scanned hood underside, engine bay from above | the open-hood scan alone looks patchy rotated shut (solved by hood_combo) | **highest**: part with an underside + 2 states + hinge |
| **-X side: front fender** | `Fender_outer` (-X only, **outer skin only**, 2.0 mm) | `fender and bumper removed` (4.1 mm) | inner wheelhouse, headlight bucket, fender mounting rails behind the panel | no +X fender part/state; the fender part has no scanned inside, so it is **translated only, never spun** | **medium**: the value is the exposed structure, not the panel |
| **Rear: bumper** | `rear_bumper_inside` (the only rear bumper part; it carries the inner face, 86-87 % within 15 mm) | `Rear bumper removed` (2.3-5.0 mm) | rear structure behind the bumper, the lamp buckets; the bumper's inner face with lamp and plate recesses | plate recess: check legibility at full res | **medium-high**: part with an inside + state → hero section |
| Top: targa | `targa_reg` (1.6 mm) | **none** (no roof-off scan) | - | - | **excluded** (openings only from data) |
| Trunk, doors | - | **none** (trunk-open scan marked "not useful"; no door-open scan) | - | - | **excluded** |
| Side skirt, lights, door card, interior, underside | own frames, unregistered | - | - | - | **excluded** |
| Exterior signature (quad round tail lamps, hood vents, 5-spoke wheels) | whole car | - | context in the opener and the end frame only | ground scraps under the sills (v1) | context only |

**Where the useful data is:** the front holds three of the four state scans and two parts with scanned insides, so it
gets the opener, the drop and the most seconds. The two **bumper-removed states are hero sections** (front and rear),
each with a move-in, a hold and labels. The fender's value is the structure behind it. The rear closes the travel.

## 2. Scene order (front → -X side → rear → reassembly). One continuous sequence per section

| # | shot id | **section (unique)** | reel time (s) | scans used | feature shown | why here (inventory) | beats | camera note | label (in → out, s) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `v2_a2_open` (NEW) | **front bumper removed** (opens on the whole car) | 0 – 4.117 | car (clean) → base + front_bumper | whole car with margins at frame 1, then the bumper slides out toward camera | opener = richest end (front); the whole car shows from frame 1 | intro | one straight push, front 3/4 -X, 7.2 → 3.0 m | - |
| 2 | `v2_b_fb_inside` (REUSE) | **front bumper removed** (continuous with 1) | 4.117 – 9.309 | base (`front bumper removed`) + front_bumper | bumper rises clear, turns its scanned inside to camera; nose structure readable below it for 5 s | hero beat 1; the bumper is the front part with both faces scanned | intro | head-on push 3.6 → 2.9 m | FRONT BUMPER REMOVED 4.39 → 6.20; FRONT BUMPER - INSIDE 7.73 → 9.15 |
| 3 | `v2_f2_hood` | **hood / engine bay** | **9.309 (drop)** – 17.024 | base (hood-open capture + `front bumper and hood removed`) + hood_combo | hood opens on the real hinge to the captured 46°, lifts off, flips its scanned underside to camera, push into the engine bay | richest region on the biggest moment | 14 | front 3/4 -X, rising push down into the bay | HOOD REMOVED 15.30 → 16.85 |
| 4 | `v2_c2_fender` | **-X side (front quarter)** | 17.024 – 22.130 | base (`fender and bumper removed`) + Fender_outer | fender moves out toward camera into black and exits the top by 20.0; push to the exposed wheelhouse / headlight bucket / mounts and hold | travel continues front → side; translate only (no scanned backside) | 9 | -X side push 3.9 → 1.9 m | FENDER REMOVED 20.05 → 21.95 |
| 5 | `v2_g2_rear` | **rear bumper removed** | 22.130 – 30.385 | base (`Rear bumper removed`) + rear_bumper_inside | bumper slides back toward camera, rises, camera moves in on the exposed rear structure and holds; on 26.471 the bumper turns its inside to camera | hero beat 2; the travel continues -X side → rear on the -X half (no line cross) | 15 | rear 3/4 -X squaring up to straight behind, 4.6 → 3.0 m | REAR BUMPER REMOVED 23.90 → 26.30; REAR BUMPER - INSIDE 27.20 → 30.20 |
| 6 | `v2_i2_home` | **whole car (reassembly)** | 30.385 – 35.496 | base + 4 parts → car (clean) | parts glide home (moving from frame 1), the rear bumper locks on 34.402, swap to the clean scan, fade | ladder end; the rear 3/4 continues the travel | 9 | rear 3/4 -X, pull back 6.6 → 8.4 m (whole car, margins) | - |
| 7 | `logo_small` | - | 35.496 – 39.40 | logo PNG | - | biggest hit; the music decays | - | ~28 % frame width | - |

The whole car appears in shot 1 (an establishing frame inside the front sequence) and shot 6 (the reassembly payoff). No
other section is repeated.

## 3. Music map (re-measured kick onsets)

| cut point | role |
|---|---|
| 0 | shot 1 (0.4 s fade-up; the push is already moving) |
| 4.117 | cut on action → shot 2 (bumper already off) |
| **9.309 drop** | shot 3: the hood starts opening on the kick |
| 13.689 | in shot 3: the hood is clear of the bay, starts flipping its underside to camera |
| 15.598 (weak) | in shot 3: the push into the engine bay is under way (not a cut) |
| **17.024** | shot 4: the fender starts moving on the cut |
| **22.130** | shot 5: the rear bumper starts sliding on the cut |
| 26.471 | in shot 5: the rear bumper starts turning its inside to camera |
| **30.385** | shot 6: reassembly |
| 33.314 | in shot 6: hood, front bumper and fender are home |
| 34.402 loud kick | in shot 6: the rear bumper locks home; swap to the clean car |
| **35.496 biggest hit** | small logo |
| ~39.40 | end (music silent) |

## 4. Diff against the current v2 draft timeline (project.yaml)

| v2 draft | v2 final | why |
|---|---|---|
| A `v2_a_fb_off` (reuse) | **re-render as `v2_a2_open`** | CROPPING: frame 1 clips the car's tail at the left edge (bright pixels in column 0; car x 0-596 of 810), so the whole car is not in frame. Composite seams also show on the "closed" car. New: start at 7.2 m on the clean car and end on A's exact end pose, so the cut into B is unchanged |
| B `v2_b_fb_inside` | **reuse unchanged**, 4.117-9.309 (5.192 s of the 5.75 s render) | content right, luma clean |
| C fender on the drop | **moved after the hood** to 17.024, merged with D | ping-pong (front → side → front); the drop goes to the richest region |
| D fender macro | **dropped (merged into C2's push)** | same section twice |
| E nose macro | **dropped** | same section as B |
| F hood | **moved to the drop**; the hood now flips its scanned underside to camera | richest data on the biggest moment; in the draft the hood floated skin-up (strip F), so the underside data was never seen |
| G rear off (az +152, +X) + H rear inside (az 178) | **merged into one held shot `v2_g2_rear`** on the -X half | same section twice; +X after a -X shot crossed the line |
| I home (front 3/4) | **`v2_i2_home`** rear 3/4 -X, parts moving at frame 1, fade 34.75-35.496 | continue the travel; the draft opened on every part off at once |
| logo `end_card.png` (52 % width, 3.9 s) | **small logo** ~28 % width, ~2.3 s at full | "small logo", "last scenes held too long" |
| no text | **6 labels** (above) | new user feedback (hero beat labels), scan shots only |

## 5. Open questions / checks for the editor
1. `tools/shot.py` line 209 hard-codes `sc.render.use_persistent_data = True`, so the `persistent=False` key that `v2shot()` writes is
   **ignored**. Change it to `spec.get("persistent", True)` before rendering (required: persistent data OFF).
2. Hood flip sign: verify with a 1-frame 30 % test at hood local t = 5.70 s. The scanned underside (dark backface, hinge brackets) must face the lens.
3. Rear plate: check the plate recess on the rear bumper inner face and the rear base at full res; deplate if any character is legible.
4. Label wording: only the file-backed phrases above. No component names: nothing in the renders identifies a crash beam
   with certainty, so "crash beam" is not used.
5. The hood scene shows the -X fender ON with the hood and bumper off, which is exactly the captured
   `front bumper and hood removed` state. That is why the hood comes before the fender.
