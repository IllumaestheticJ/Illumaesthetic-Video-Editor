# Nissan 400Z: scene direction v2 (scene-director, 2026-11-11)

Brief: scan only, no IRL, no text, satin silver on black, 1080x1920, Temerario-style (training/references/README.md
`v_jul22_1047_58`). Inputs read: CLAUDE.md, knowledge/lessons.md (all of it), style-guide.md, workflow.md "Scene direction",
clips.md, project.yaml, cues.json, editlog.jsonl, tools/shots.py, hinge.json. There is no feedback.jsonl yet.
Parent v2 brief, folded in: travel front → side → rear; each section explodes on its own close camera; no wasted
rotations; the opener shows the whole car; spin a part only when its back is worth showing; never reuse a shot; the
ending is not held long (progressive explode → reassembly → fade → small logo).

Renders reviewed (sheets in `/home/user/media/work/z400/check/`): `fin_a.jpg` (s1-s5), `dir_s1_front34.jpg`,
`dir_s2_rear34.jpg`, `dir_s6_hood.jpg`, `dir_s7_top.jpg`, `dir_s8a_explode.jpg`, `dir_s8b_explode.jpg` (60/112 frames
done when sheeted), `dir_keyframes.jpg` (last frames of s3/s5/s6, s1 f1/f56, s8b f1), `dir_s1_crop.jpg` (s1 f30/40/48).
`python -m ive director` report on v1: `/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/7fb2e21b-fa3b-5a1c-abba-9b3f48ec7a09/scratchpad/director_report.md`.

## 1. Feature inventory

| Region | Scans (all at identity, p50 1.4-1.7 mm; bumper 3.8 mm) | States (registered) | Parts (diffed, registered) | Signature features seen in renders | Weak data | Richness |
|---|---|---|---|---|---|---|
| **Front** | Full Car, Bumper Only, Bumper Grille Removed, Bumper and hood removed, Hood Open | hood open (fitted hinge -40.4 deg, 5.6 mm), bumper + hood removed (front structure), grille removed | p_hood, bumper_shell, p_grille | Z-style rectangular grille with slats, teardrop headlights, engine bay (Hood Open: real V6, intake, strut towers, see s6 f70) | grille slats have small dark gaps; behind-grille detail is sparse | **4 states + 3 parts + 2 signature features: richest** |
| **Side** | Full Car, Side Mirrors Removed (Rear Gas Door Open: partial, unused) | mirrors removed (door mounts) | p_mirror_r, p_mirror_l | sculpted shoulder from the door to the rear haunch, mirror on the door | black shut-line slivers at the door/quarter seams (s3 f46); rims are hollow spoke fragments up close (editlog) | 1 state + 2 small parts |
| **Rear** | Full Car, Rear Wing Removed | wing removed (deck mounts) | p_wing (duck-tail lip) | full-width tail-lamp bar, NISSAN badge, Z script | plate area: no legible characters in s5 f46 (only mounting marks); exhaust tips fine | 1 state + 1 part + 1 signature feature |
| Top | Full Car only | none | none | roof / long-hood silhouette | nothing new beyond the whole-car wide | low |
| Wheels | Full Car | none | none | none | hollow rims, so no close-up (editlog) | none |
| Engine bay | Hood Open | (open state above) | none separate | V6 top end | partial capture in the open scan (hinge fit used fragments) | with Front |
| Interior / trunk / doors | **no scans** | none | none | none | not planned | none |

Conclusions:
- The front is by far the richest region, so it opens (whole car, front 3/4), gets the drop and gets the longest
  section explode.
- The side has one state with two small parts, so it gets a short scene. The rear also has one part, so it gets a
  short scene too.
- Top-down: the full car alone holds no top data that the opener does not already show, and a closed car cannot sit
  inside a progressive explode. I drop this rung. The reassembly is a high 3/4 that looks down on the car instead.
- No door, trunk or interior beat: we have no scans of those states.

## 2. Scene list (v2, in order)

Travel: front (whole → detail → hood → front explode) → right side (shoulder → mirror off) → rear (tail → wing off) →
high rear-left reassembly → fade → small logo. There is one direction of travel and no ping-pong.

| # | scene | scans used | feature shown | why here (inventory) | slot (s) / beats | camera note |
|---|---|---|---|---|---|---|
| 1 | **N0_open** (new) | car (3 mm) | the whole car, front 3/4 | opener frames the richest end; the whole car is in frame for the full slot (v1 s1 crops the nose from ~f30) | 0.000-3.700, 8 beats (intro) | slow push-in, fade up from black, motion from frame 1 |
| 2 | s4_lamp (reuse) | front2 (2 mm) | headlight + grille | detail of the front before its parts come off; it introduces the grille and bumper | 3.700-7.430, 8 beats (intro) | extreme close-up slide toward the centre, played 0.79x |
| 3 | s6_hood (reuse, trimmed) | comp_hood + p_hood (hinge) | hood opens, engine bay from Hood Open | first state reveal lands ON THE DROP | 7.430-11.128, 8 beats | high front-right 3/4 easing in |
| 4 | **N1_front_explode** (new) | comp_explode + p_hood, p_grille, bumper_shell | hood lifts off its hinge, grille pops out, bumper shell slides toward the lens and tips to show its inner face, front structure from "Bumper and hood removed" | richest region gets the longest section and the heavy kicks 11.935/12.974/14.826/15.627 | 11.128-16.666, 12 beats | starts on s6's last pose (one held move), descends and pushes into the exposed front structure |
| 5 | s3_haunch (reuse) | side2 (2 mm) | right shoulder glide to the mirror | travel moves to the side; the glide runs forward and ends on the mirror | 16.666-19.319, ~6 beats | as rendered (native speed) |
| 6 | **N2_mirror** (new) | comp_explode + p_mirror_r/l | mirror moves out into black; scanned door mount (Side Mirrors Removed) | one-part region, so a short scene | 19.319-22.198, ~6 beats | starts on s3's last pose, swings outboard/forward |
| 7 | s5_tail (reuse) | rear2 (2 mm) | tail-lamp bar + badge | travel moves to the rear; detail before the rear part | 22.198-24.044, 4 beats | as rendered, slide ends car-right |
| 8 | **N3_wing** (new) | comp_explode + p_wing | duck-tail lifts off; scanned deck mounts (Rear Wing Removed) | one-part region, so a short scene; parts leave in travel order | 24.044-26.703, ~6 beats | starts on s5's last pose, rises and pulls back |
| 9 | s8b_explode (reuse, frames 1-99) | comp_explode + all parts | every panel flies home, LOCK on 30.395 (loudest kick), car rests, fade | reassembly is the one all-parts moment (allowed: the rule bans all-at-once *separation*); its high rear-left angle is unused elsewhere | 26.703-33.286 | as rendered; fade out 31.428 → 33.286 |
| 10 | logo (re-made smaller) | logo_card | ILLUMAESTHETIC, ~30 % width | Temerario ending | 33.286-38.400 | black, logo in on 34.087 |

## 3. Music map (measured kicks: tools/kicks.py, strength ≥ 0.5)

Cut frames are round(t*30). The first clip is one frame short.
| cut | t (s) | frame | kick strength | scene starting |
|---|---|---|---|---|
| - | 0.000 | 0 | - | N0_open (fade up) |
| 1 | 3.700 | 111 | intro bar 3 (v1 cut) | s4_lamp |
| 2 | 7.430 | 223 | 0.75 **DROP** | s6_hood |
| 3 | 11.128 | 334 | 0.71 | N1 (hood lift lands 11.935 = 0.99) |
| 4 | 16.666 | 500 | 0.64 | s3_haunch |
| 5 | 19.319 | 580 | 0.87 | N2 (mirror fully out on 20.358) |
| 6 | 22.198 | 666 | 0.86 | s5_tail |
| 7 | 24.044 | 721 | 0.61 | N3 (wing out on 25.902) |
| 8 | 26.703 | 801 | 0.91 | s8b reassembly (LOCK 30.395 = 1.00) |
| 9 | 33.286 | 999 | 0.57 | logo (fade-in on 34.087 = 0.90) |
| end | 38.400 | 1152 | track tail | - |

Durs (frames): 111(110), 112, 111, 166, 80, 86, 55, 80, 198, 153 = 1152 = 38.4 s. Kept from v1: 3.70, 7.43, 11.128,
16.666, 19.319, 26.703. Dropped from v1: 9.282, 12.974, 34.087 (34.087 is now the logo's entry, not a cut). New cuts,
all on measured kicks: 22.198, 24.044, 33.286.

## 4. Diff against v1

| v1 | v2 | why |
|---|---|---|
| s1_front34 (slot 1) | **replaced by N0_open** | brief item 4: the opener must show the whole car. s1 crops the nose from ~frame 30 (dir_s1_crop.jpg), and v1 needs frames 1-55 |
| s2_rear34 (slot 2) | **dropped** | an orbit that repeats a whole-car wide (director report: IoU 0.77 vs s1 and vs s8b); rear covered by tail + wing; front→rear→front ping-pong |
| s3_haunch (slot 3) | moved to slot 5 | it belongs to the side section, between front and rear |
| s4_lamp (slot 4) | moved to slot 2 | front detail sits next to the front wide |
| s5_tail (slot 5) | moved to slot 7 | rear detail, just before the wing |
| s6_hood (slot 6) | moved to slot 3 (the drop) | first state reveal on the drop; continues into N1 |
| s7_top (slot 7) | **dropped** | closed whole car again, no top-specific data; a rising/rotating overhead that shows nothing new (brief 3) |
| s8a_explode (slot 8) | **dropped** | every part separates at once in one wide orbit (standing user rule, mazda-miata-nc); 1.3 s dead; f30-51 black |
| s8b_explode (slot 9) | kept as the reassembly, frames 1-99 + fade | the parts' start pose = the v1 stacked pose; N1-N3 end in that same pose, so the cut is continuous |
| logo 4.3 s, 50 % width | small logo (~30 % width) on black, 0.8 s black first | Temerario: small logo; sibling notes say "small logo" |

Reuse as-is (only position/speed change): s4_lamp, s6_hood, s3_haunch, s5_tail, s8b_explode.
New renders: N0_open, N1_front_explode, N2_mirror, N3_wing (236 frames total; budget and specs in director.md).
Not needed any more: the queued `s8a_fix` re-render (22 frames, waiting on render2.log). Cancel it to save CPU.

## 5. Open questions for the editor
1. **Bumper inner face**: does `bumper_shell` (from "Bumper Only") have a scanned inside with mounting tabs? Render it
   alone from behind (one still) before keeping N1's tip. If the inside is hollow or ragged, translate it only (no tip).
2. Mirror and wing parts are cut from the full car, so their mounting faces are probably open shells. Plan: no spin
   beyond the ±20 deg yaw that s8b's start pose needs. Check one still of each from behind.
3. N2/N3 start on the exact last pose of s3/s5, but the base changes from 2 mm crops to the 3 mm comp_explode. Look at
   the frames either side of 19.319 and 24.044. If the density jump reads, nudge the new shot's first key
   ~5 % closer so it reads as a cut, not a glitch.
4. Rear plate: s5 f46 shows no legible characters. Check N3's last frame anyway.
