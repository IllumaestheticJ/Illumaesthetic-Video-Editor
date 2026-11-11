# Scene direction - toyota-gr86 (BRZ gen 2 hero scan), v2

Scene director, 2026-11-11. Inputs: lessons.md (all), style-guide, clips.md, editlog, project.yaml (v1), contact sheets
`/home/user/media/work/gr86/out/sheet_*.jpg` (+ `sheet_s7_now.jpg`, made from the s7 frames 1-103 that existed then),
state renders `/home/user/media/work/gr86/reg/states/*.png` (zoom: `out/states_zoom.png`), s7 frame crops
(`out/s7_f100_crop.png`, `out/s7_f118_front.png`), `ive director` report (`/home/user/media/work/gr86/out/director_report.md`).
Rules applied on top of the brief: coordinator relays #1 (travel, per-section explode, no redundant rotations, whole-car
opener, small logo) and #2 (cropping A, one sequence per section B, bumper-removed hero beats + labels C, no faked
openings D). Where they conflict with the original brief (no text, Temerario ladder), the newer user rules win.

## 1. Feature inventory

| Region | What the data holds | States (registered to BRZ Full Car) | Parts (registered) | Weak data | Richness |
|---|---|---|---|---|---|
| **Front** | Horizontal-slat grille, LED headlights, corner intakes (s3 shows them crisp at 2 mm) | **Hood Open** (engine bay, 48 % / 3.8 mm); **Bumper Hood Removed** (radiator/heat-exchanger core with fins, intake piping, front structure below z 650 mm; 27.6 % / 3.9 mm) | **Front bumper** (part scan, ICP-pinned; **inner face scanned**: inward-facing area 0.24 m^2 vs outward 0.23 m^2, two skins >25 mm apart in 55 % of 20 mm cells); **hood** (cut from the car's own skin, outer surface only) | Open hood panel NOT captured (so no hinge swing); cowl/windscreen base of `comp_explode` has dark holes (seen in `reg/expl3c.jpg`, s7 f100) | **Highest**: 2 states + 2 parts + signature grille/lights |
| **Rear** | Ducktail lid, BRZ badge, twin exhaust tips, diffuser | **Rear Bumper Removed** (63 % / 3.2 mm): holed rear bumper beam across the full width, exhaust silencer + tips, lamp backs; **Trunk Open Bumper Off** (below 750 mm only) | **Rear bumper** (part scan, ICP-pinned; inner face scanned: inward 0.35 m^2 vs outward 0.28 m^2) | Trunk lid not cleanly captured (**never open the trunk**); **left tail lamp has a black scan hole** (s4, all frames - `out/s4_f60_crop.png`); plate area blank (fine) | **High**: 2 states + 1 part |
| Side | Profile, doors, aftermarket wheels | Side Mirrors Removed (not used) | mirrors (not used) | **Left mirror is a broken thin capture; wheels/tyres rough (dark broken tyre on s2 rear wheel)** | Low: no state, no part, weak wheels -> no own scene; the opener's 3/4 shows the right side |
| Top | Roof, glass | - | - | Glass is a sprayed surface, nothing new vs the 3/4s | Low on its own; useful only as the view of the *exploded stack* |
| Engine bay | Real Hood Open capture (boxer engine, intake, strut towers) | Hood Open | - | cowl holes (see Front) | Part of the front sequence |
| Interior / wheels | - | - | - | not scanned / rough | none |

## 2. Scene order (front -> rear -> top/stack -> reassembly -> logo)

| # | scene | scans used | section / feature shown | why here (inventory) | bars | camera note |
|---|---|---|---|---|---|---|
| A | `a_open` (NEW) | car4 | **whole car**, front-right 3/4 | Opener must be the whole car with motion from frame 1; front-right because the front is the richest end and the left mirror is broken | 2 | dolly-in 9.0 -> 7.7 m with 8 deg arc, car 72-80 % width |
| B | `s3_headlight` (reuse) | det_front 2 mm | **front detail**: right headlight + slat grille + intake | Signature front feature, best-quality close-up in the set | 1 | as rendered (in-point 2.4 s, past the rough wheel) |
| C | `d_front` (NEW) | comp_explode + hood_m + front_bumper | **front states**: hood lifts off -> engine bay (Hood Open) -> front bumper out, tips to show its scanned inside -> push in on the front structure (Bumper Hood Removed) | Richest region = longest scene (4 bars) and both front phrase kicks (9.860 hood, 14.758 bumper). Hood is LIFTED OFF (backed by the *Bumper Hood Removed* state), not hinged | 4 | front-right; rises above the bay, comes down low for the bumper, ends close on the structure |
| D | `g_rear` (NEW) | comp_explode + rear_bumper (+ hood, front bumper in their removed poses) | **rear states**: rear bumper out, tipped to show its inside -> push in on the rear bumper beam + exhaust (Rear Bumper Removed) | Second-richest region, its own sequence; bumper lands on the 19.656 phrase kick | 3 | rear-RIGHT (keeps the holed left lamp small/edge) |
| E | `s_stack` (NEW) | comp_explode + 3 parts | **top**: all three removed parts rise into a layered stack, seen top-down, then a crane down to high rear 3/4 to read the layers | The brief's top-down rung, but only where the top view adds information (the removed-part layout). Intact-car top-down (s6) is dropped | 3 | near top-down -> high rear-right 3/4, nose up in frame |
| F | `s7_explode` tail (reuse f111-185) | comp_explode + 3 parts | **whole car reassembly**: parts slam home on the 34.350 loud return | Biggest musical moment = all parts home at once; existing render already lands there | 2 | as rendered; fade to black 36.30 -> 36.80 |
| G | logo | logo card | small ILLUMAESTHETIC logo | Temerario ending | 1 | logo ~30 % frame width (v1 card is ~75 %: remake) |

Each section appears in ONE continuous sequence: whole (A, and F as the reassembly payoff), front (B+C), rear (D),
top (E). Side has no scene (weak data; seen in A).

## 3. Music map (measured: downbeats every 2.449 s from 0.064; double-kick phrase starts 9.860, 14.758, 19.656, 24.554, 29.452, 34.350; loud return 34.350; audible to 39.24)

| scene | start -> end (s) | frames @30 | lands on |
|---|---|---|---|
| A a_open | 0.000 -> 4.962 | 0 -> 149 | - |
| B s3_headlight | 4.962 -> 7.411 | 149 -> 222 | downbeat |
| C d_front | 7.411 -> 17.207 | 222 -> 516 | hood off on **9.860**, bumper out on **14.758** |
| D g_rear | 17.207 -> 24.554 | 516 -> 737 | rear bumper out on **19.656** |
| E s_stack | 24.554 -> 31.901 | 737 -> 957 | cut on **24.554**, stack formed on 27.003 |
| F s7 tail | 31.901 -> 36.799 | 957 -> 1104 | parts home on **34.350** (loud return) |
| G logo | 36.799 -> 39.248 | 1104 -> 1177 | final downbeat |

## 4. Diff against v1

| v1 clip | v2 | why |
|---|---|---|
| s1_front34 | **dropped** -> new A | crops the tail (not the whole car); turntable that `ive director` flags as the same view as s2 (IoU 0.75) |
| s2_rear34 | **dropped** | orbit (rule 3), crops the nose, rough black tyre on the rear wheel; side has no data worth a scene |
| s3_headlight | **kept**, in-point 2.4 s | best front detail; was flagged ~s4 (IoU 0.87) - s4 is gone |
| s4_tail | **dropped** | left tail lamp has a black scan hole in every frame (lessons: tail-lamp holes -> pick another detail); rear detail now comes from the bumper-removed beat |
| s5_hood | **dropped** -> lift-off inside C | swings the closed hood skin on a hinge; the open hood panel was never captured = a faked opening (user rule D). Lift-off is backed by the *Bumper Hood Removed* state |
| s6_top | **dropped** -> E | rotating top-down of the intact car shows nothing new (rule 3); top rung kept only as the exploded-stack view |
| s7_explode f1-110 | **dropped** | all three parts separate at once in one wide orbit (user rules: per-section explodes) |
| s7_explode f111-185 | **kept** as F | drift + slam home on 34.350 + settle; lands exactly where v1 put it |
| logo | remade smaller | user rule 7 (small logo) |

Reused unchanged: s3 frames 37-74, s7 frames 111-185. New renders: A, C, D, E (keys in `director.md`).

## 5. Open questions / checks for the editor
1. s7 must finish rendering to f_0186 (118/186 at 10:05) and pass the per-frame luma check before F is used (frames 111-185).
2. `comp_explode` cowl holes (dark patches at the windscreen base, `reg/expl3c.jpg`): C looks down into the bay. Render
   2 stills of C (t 2.45 and t 4.9) before the full run; if the patches read, fill the cowl from Hood Open triangles in
   the hood-mask zone or lower the C camera so the engine hides the cowl.
3. Front label names only the state ("FRONT BUMPER + HOOD REMOVED"); the finned core looks like radiator/condenser but
   I did not label it - confirm with the team before naming it.
4. Rear label "REAR CRASH BEAM": the holed full-width beam is clearly visible in `reg/states/Rear_Bumper_Removed.png`;
   confirm it is in frame on D's t 4.9 still before keeping the label.
