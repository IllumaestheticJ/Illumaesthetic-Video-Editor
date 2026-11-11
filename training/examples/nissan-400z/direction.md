# Nissan 400Z: scene direction v2 (scene-director, 2026-11-11)

Brief: scan only, satin silver on black, 1080x1920, Temerario-style (training/references/README.md `v_jul22_1047_58`).
Inputs read: CLAUDE.md, knowledge/lessons.md (all of it), style-guide.md, workflow.md "Scene direction", clips.md,
project.yaml, cues.json, editlog.jsonl, tools/shots.py, hinge.json. There is no feedback.jsonl yet.
Parent v2 brief and its addendum are folded in. Where they conflict, the addendum wins:
- travel front → side → rear;
- section-focused explodes;
- no wasted rotations;
- whole-car opener;
- spin a part only when its back is worth showing;
- never reuse a shot;
- a short ending with a small logo;
- deliberate 9:16 framing;
- one continuous sequence per section;
- **the bumper-removed data is the hero beat, with short factual labels**;
- **the hood is shown open only as the real Hood Open scan**;
- no trunk or gas-door beat.

Sheets I looked at (all in `/home/user/media/work/z400/check/`): `fin_a.jpg`, `dir_s1_front34.jpg`, `dir_s1_early.jpg`
(f1/13/25), `dir_s1_crop.jpg` (f30/40/48), `dir_s2_rear34.jpg`, `dir_s6_hood.jpg`, `dir_s7_top.jpg`, `dir_s8a_explode.jpg`,
`dir_s8b_explode.jpg`, `dir_fml_all.jpg` (first/mid/last of s3, s5, s8b), `dir_s8b_tail.jpg` (s8b f70/f97),
`dir_keyframes.jpg`, `dir_states.jpg` (solo renders: Hood Open, Bumper and hood removed, comp_hood, comp_explode,
Bumper Only, Bumper Grille Removed), `dir_bhr_zoom.jpg` (Bumper and hood removed, front zoom), `dir_front_struct.jpg`
(s8a f80, front crop).
v1 `ive director` report: `/tmp/claude-0/-home-user-Illumaesthetic-Video-Editor/7fb2e21b-fa3b-5a1c-abba-9b3f48ec7a09/scratchpad/director_report.md`.

## 1. Feature inventory

| Region | Scans (identity, p50 1.4-1.7 mm; bumper 3.8 mm) | States (registered) | Parts (diffed, registered) | What the renders actually show | Weak data | Richness |
|---|---|---|---|---|---|---|
| **Front** | Full Car, Bumper Only, Bumper Grille Removed, **Bumper and hood removed**, Hood Open | hood open (as captured), grille removed, bumper + hood removed | p_hood, bumper_shell, p_grille | Bumper and hood removed (`dir_bhr_zoom.jpg`): a **horizontal beam across the nose behind the bumper with bolt holes**, both **headlamp units from behind**, the **lower lip/undertray**, hoses and wiring beside the right lamp and wheel arch, and radiator/condenser rows behind the beam. Bumper Only: the full bumper with the rectangular slatted grille. Teardrop headlights. | the upper radiator support and the top edge of the core are ragged fragments; behind-grille detail is sparse | **4 states + 3 parts: richest by far** |
| **Engine bay** | Hood Open (+ visible in Bumper and hood removed) | hood open | none | V6 top, intake, strut towers (s6 f70, comp_hood) | the **captured open hood is two ragged flaps** (`dir_states.jpg` 1st image); bay edges partial | with Front |
| **Side** | Full Car, Side Mirrors Removed (Rear Gas Door Open: partial, skipped) | mirrors removed (door mounts) | p_mirror_r, p_mirror_l | sculpted shoulder, mirrors | black shut-line slivers at the door/quarter seams (s3); rims hollow up close | 1 state + 2 small parts |
| **Rear** | Full Car, Rear Wing Removed | wing removed (deck mounts) | p_wing (duck-tail lip) | full-width tail-lamp bar, badge, Z script | plate area shows mounting marks, no legible characters (s5 f46) | 1 state + 1 part |
| Top | Full Car | none | none | roof silhouette only | nothing new beyond a whole-car wide | none, so skipped |
| Wheels | Full Car | none | none | none | hollow spoke fragments up close | none, so skipped |
| Trunk / doors / interior / gas door | **no usable scans** | none | none | none | Rear Gas Door Open is a partial quarter | **not planned** |

Conclusions:
- Front + engine bay is the richest region. It opens the travel, and the **bumper-removed structure is the hero beat on
  the drop (7.43 s)**.
- The hood can only appear open via the real Hood Open scan. State order forces hood open before bumper off:
  - "Bumper and hood removed" has both panels off.
  - No "bumper off, hood closed" scan exists.
- Side and rear each have one part, so each gets a short scene.
- There is no top-down, wheel, trunk or door beat.

## 2. Existing renders vs the framing rule (addendum A)

| render | first / mid / last | verdict |
|---|---|---|
| s1_front34 | whole car only to ~f10; the right margin is gone by f13; the nose is clipped from ~f25 | **fails** as a whole-car opener: replace (N0) |
| s2_rear34 | whole car, small | repeats a whole-car wide (IoU 0.77 vs s1/s8b): drop |
| s3_haunch | the car fills the left ~2/3 and the right third is dead black; the subject is unclear (fender, door and windscreen all clipped arbitrarily); black seam slivers; the mirror sits on the frame edge | **fails**: drop; the side becomes one framed new shot (N2) |
| s4_lamp | the headlamp is clipped at the left edge and the grille cut at the right; reads as a fragment of the front | borderline; also redundant with the bumper hero (it shows the grille that comes off); drop |
| s5_tail | badge + centre of the lamp bar fill the frame (good detail); exhaust tips half-clipped at the lower corners at f1/f23/f46; trunk edge clipped at the top at f46 | **borderline pass** as a detail of the badge/lamp bar: keep. If the reviewer flags the exhaust tips, fold the rear into a new N3 that starts on a framed tail (+70 f) |
| s6_hood | framing fine, but it **animates the closed hood scan open** | **fails rule D**: drop; replaced by the real Hood Open scan (H) |
| s7_top | whole closed car | no new information: drop |
| s8a_explode | every part separates at once, wide; f30-51 black | **fails** the section-focus rule: drop |
| s8b_explode | f1-56 fine (parts stacked above, then home); **from ~f65 the nose and tail touch the frame edges, and both are clipped by f97** | keep as the reassembly, f1-101, **scaled to 78 % with a black pad** in the edit (no re-render). The car then fits with ~8 % margins at f97. Fade from 31.428 |

## 3. Section map (addendum B: each section in one continuous sequence)

| order | section | shots | t (s) |
|---|---|---|---|
| 1 | whole car | N0_open | 0.000-3.700 |
| 2 | **front + engine bay** (one sequence) | H_hoodopen → N1a_bumper_off → N1b_structure | 3.700-16.666 |
| 3 | side (right mirror) | N2_mirror | 16.666-19.319 |
| 4 | rear | s5_tail → N3_wing | 19.319-26.703 |
| 5 | reassembly (all parts, whole car) | s8b_explode | 26.703-33.286 |
| 6 | logo | logo card | 33.286-38.400 |

There are no duplicates. The engine bay is seen in H and behind the structure in N1a/N1b, all inside the single front
sequence. The whole car appears at the opener and the reassembly only. The reassembly is the one all-parts moment,
which the rule allows because it bans all-at-once *separation*. Wheels and top are never a subject.

## 4. Scene list (v2)

| # | scene | scans used | feature shown | why here (inventory) | slot / beats | camera note |
|---|---|---|---|---|---|---|
| 1 | **N0_open** (new) | car 3 mm | whole car, front-right 3/4 | opener frames the richest end; whole car with margins on every frame | 0.000-3.700, 8 beats (quiet intro) | slow push-in, fade up |
| 2 | **H_hoodopen** (new) | comp_hood + Hood Open **as captured** (incl. the captured open hood) | hood open, engine bay | the real open state; must precede bumper off (state order) | 3.700-7.430, 8 beats | high front, push down into the bay |
| 3 | **N1a_bumper_off** (new) | comp_explode (Bumper and hood removed) + p_grille, bumper_shell | grille out (state: Bumper Grille Removed), then the bumper shell out, revealing the structure | **HERO on the DROP**: richest data, biggest musical moment, front first | 7.430-11.128, 8 beats (kicks 8.243 / 9.282) | low front-right 3/4 framed on the nose, pushing in |
| 4 | **N1b_structure** (new) | Bumper and hood removed at ≤2 mm + front 2 mm | beam with bolt holes, headlamps from behind, wiring/hoses at the right lamp, lower lip | hold long enough to read the hero data; labels | 11.128-16.666, 12 beats | slow lateral slide across the beam |
| 5 | **N2_mirror** (new) | comp_explode + p_mirror_r/l | right mirror out; scanned door mount | side: one part, short | 16.666-19.319, ~6 beats | framed on the mirror, swings outboard |
| 6 | s5_tail (reuse) | rear2 2 mm | badge + lamp bar centre | rear detail before its part | 19.319-22.198, ~6 beats | as rendered, native speed |
| 7 | **N3_wing** (new) | comp_explode + p_wing | duck-tail lifts; scanned deck mounts (Rear Wing Removed) | rear: one part | 22.198-26.703, ~10 beats | starts on s5's last pose, rises over the deck |
| 8 | s8b_explode (reuse) | comp_explode + all parts | everything flies home, LOCK on 30.395 | reassembly; new high rear-left angle | 26.703-33.286 | as rendered, scaled 78 %, fade |
| 9 | logo (re-made smaller) | logo card | ILLUMAESTHETIC ~30 % width | Temerario ending | 33.286-38.400 | logo in on 34.087 |

On-screen labels are allowed by the addendum, over scan shots only. They go in N1b only:
- "FRONT BUMPER REMOVED": 11.935 → 14.700.
- "CRASH BEAM + MOUNTING POINTS": 14.826 → 16.450.

Both are factual: the first comes from the scan names "Bumper Only" / "Bumper and hood removed", the second from what
is visible (the beam and its bolt holes). If the beam's holes don't read clearly in the 2 mm frame, use
"MOUNTING POINTS" alone. No numbers. Details are in director.md.

## 5. Music map (measured kicks: tools/kicks.py, strength ≥ 0.5)

| cut | t (s) | frame | kick | scene starting |
|---|---|---|---|---|
| - | 0.000 | 0 | - | N0_open (fade up) |
| 1 | 3.700 | 111 | intro bar 3 (v1) | H_hoodopen |
| 2 | 7.430 | 223 | 0.75 **DROP** | N1a (grille 8.243 = 0.93, bumper 9.282 = 0.62) |
| 3 | 11.128 | 334 | 0.71 | N1b (label 1 on 11.935 = 0.99, label 2 on 14.826 = 0.64) |
| 4 | 16.666 | 500 | 0.64 | N2 (mirror out on 17.5, mount on 18.512 = 0.51) |
| 5 | 19.319 | 580 | 0.87 | s5_tail |
| 6 | 22.198 | 666 | 0.86 | N3 (wing up on 23.011 = 0.91) |
| 7 | 26.703 | 801 | 0.91 | s8b (LOCK 30.395 = 1.00) |
| 8 | 33.286 | 999 | 0.57 | logo (in on 34.087 = 0.90) |
| end | 38.400 | 1152 | track tail | - |

Kept from v1: 3.70, 7.43, 11.128, 16.666, 19.319, 26.703. Dropped: 9.282, 12.974, 34.087 (they are now motion hits
inside shots or the logo entry). New cuts, all on measured kicks: 22.198, 33.286.

## 6. Diff against v1

Removed:
- **s1, s2, s3, s4, s6, s7, s8a.** Reasons are in §2.
- **The queued `s8a_fix` render** (22 frames, waiting on `RENDERS_DONE` in /tmp/claude-0/render2.log). It is no longer used, so cancel it.

Reused:
- **s5_tail**: moved from slot 5 to slot 7; plays at native speed.
- **s8b_explode**: kept as the reassembly, frames 1-101, scaled to 78 %, then fade.
- **The logo**: re-made smaller.

New (shots and frame counts are in director.md):
- **N0, H, N1a, N1b, N2, N3.**
- **Light prep jobs**, not renders:
  - a `comp_hoodopen` composite;
  - a ≤2 mm prep of Bumper and hood removed, using `--like car.json`.

## 7. Open questions
1. **Bumper inner face**: is the inside of "Bumper Only" scanned (mounting tabs)? Render bumper_shell alone from behind
   (one still) before keeping N1a's tip. If it is hollow or ragged, translate only. Do the same for p_mirror_r and p_wing.
   Those two are cut from the full car, so their backs are probably open, and the plan does not flip them.
2. **Captured open hood**: two ragged flaps. Framing H on the bay keeps the flaps as a deliberate partial crop at the
   top. If the reviewer still reads them as "broken", the fallback is to show the Hood Open bay with the hood cropped
   out completely (camera lower, target z 0.6).
3. **Hood disappearance**: the hood is open in H and gone in N1a. This is a state cut at the drop, backed by the
   "Bumper and hood removed" scan, with a camera change. Accept, or add an "HOOD REMOVED" label? (I recommend no extra label.)
4. **Frame budget**: 371 new frames (~1.5-2.5 h) vs the ~250 aim. The cheaper plan B (270 frames) is in director.md
   and needs a 10-frame interpolation test first. **The parent/user needs to choose.**
