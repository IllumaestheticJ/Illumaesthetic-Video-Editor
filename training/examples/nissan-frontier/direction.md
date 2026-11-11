# Nissan Frontier Pro-4X - scene direction v2 (scene-director, 2026-11-11)

Inputs read: CLAUDE.md, knowledge/lessons.md (all, standing rules A-D at the end), style-guide.md, Temerario notes
(training/references/README.md), clips.md, project.yaml, timing.json, editlog.jsonl, feedback.jsonl, review.md,
tools/shots.py, parts.py, composite.py, `ive director` report (director_report.md). Looked at chk/states.png, parts.png,
backs.png, bump_back.png, st_fbrhc.png, st_bhr.png, sheet_s1/s2/s34/s5/s6/s7, s5_crop.png, v1_sheet.png, v2_check.png.

Newest feedback (wins): **"Better. Highlight and label each unique scan section."**
Sections = FULL TRUCK, FRONT BUMPER, GRILLE, HOOD, FENDER FLARES, FRONT STRUCTURE (+ the bumper-removed hero state).
The v2_check draft (all sections highlighted one by one inside one wide explode) breaks the standing rule "never separate
every part at once in one wide orbit" and is replaced: one section per shot, the part comes off in its own shot and stays off.

## 1. Feature inventory

| scan | registers (median to full car) | what it actually shows (looked at it) | use in v2 |
|---|---|---|---|
| Full truck (`full`) | base | whole truck on a lift, NO wheels (empty arches show suspension), bed, tailgate with FRONTIER embossing, step rails, mirrors | opener (whole truck in frame), FULL TRUCK label at the end |
| Removed front bumper (`fbr`) | 6.3 mm | the bumper itself incl. grille + fogs. **Back side scanned** (backs.png / bump_back.png): ribs, mounting tabs, fog-lamp housings, grille mounting frame | FRONT BUMPER part (minus grille) - comes off, turns to show its inside |
| Front bumper removed, hood closed (`fbrhc`) | 1.3 mm | truck front with bumper off: radiator core fins behind, lower bar, lamp backs, hood shut | **hero state**: FRONT BUMPER REMOVED |
| Bumper and Hood Removed (`bhr`) | 3.7 mm | radiator support, radiator core, full-width lower horizontal beam, lamp housings, engine bay from above (s5_crop) | FRONT STRUCTURE (struct.blend) + base once the hood is off |
| Fender Flares Removed (`flares`) | 1.3 mm | body with all four flares off (both sides, front + rear arches) | FENDER FLARES (x_flares_r/l derived from full truck) |
| Grille part (`grille`) | 2.1 mm | stock grille; back side thin/dark (backs.png) | GRILLE part - translate only, no flip |
| Hood | derived (full truck minus `bhr`) | outer skin only, no underside | HOOD part - lifts OFF straight up; never hinged open (no hood-open scan) |
| Lower grille mounting bar (`mount`) | 2.6 mm | lower bar only, covered by bumper scan | unused |
| Rear (tailgate/bed/rear bumper) | - | only in the full truck, no states/parts | no rear removal; rear seen only in the wide reassembly |

Weak data: empty wheel arches (no wheels - keep cameras at 1.2-1.9 m, not low profile; v1 s4_arch lower half busy/dark),
grille back side, hood underside (outer shell only), bhr top edge has floating fragments (keep S6 framing below them).

Region richness: **front** = 2 states + 3 parts (bumper, grille, hood) + structure -> richest, gets the drop and most beats.
**side** = 1 state + flares part -> one 6-beat scene. **top** = no feature -> no scene. **rear** = full truck only -> only as
the reassembly angle (travel ends there), no rear scene of its own.

## 2. Scene order (travel front -> side -> rear, parts stay off once removed = progressive explode over several angles)

| # | scene | scans used | feature / section | why here | beats | camera note |
|---|---|---|---|---|---|---|
| 1 | Full truck wide | full | FULL TRUCK (no label yet) | front carries every scan feature -> open on front-right 3/4; whole truck incl. bed in frame (v1 s1 cropped the bed) | 8 (0-4.852) | slow arc from frame 1 |
| 2a | Grille detail | full (2 mm) | GRILLE | first detail of the front, outermost part comes off first | 4 (4.852-7.266) | **reuse v1 s3_grille** |
| 2b | Grille off | comp_fbrhc + x_bumper + x_grille | GRILLE (section 01) | continues 2a's last pose; grille slides out sideways into black, core behind it shows | 4 (7.266-9.681) | ends on the silent beat, cut on the drop |
| 3 | Bumper off + turn | comp_fbrhc + x_bumper | FRONT BUMPER (02) | biggest musical moment (drop 9.681) on the richest data: bumper with a scanned inside | 8 (9.681-14.509) | follows the bumper down into black, turns it to show ribs/tabs/fog housings |
| 4 | Bumper-removed hero | comp_fbrhc (fbrhc fill highlighted) | FRONT BUMPER REMOVED (hero state) | rule C: move in on what is behind the bumper and hold | 6 (14.509-18.130) | low straight-on push-in |
| 5 | Hood lifts off | comp_front + x_hood | HOOD (03) | hood-removed state exists -> hood lifts OFF (no hinge), lands on the b32 accent 19.337 | 4 (18.130-20.544) | high front 3/4, tilts up with the hood |
| 6 | Front structure | comp_front (struct highlighted) | FRONT STRUCTURE (04) | the deepest front state; closes the front sequence | 6 (20.544-24.166) | high push-in over radiator support into the bay |
| 7 | Flares off | comp_explode + x_flares_r/l | FENDER FLARES (05) | travel front -> side; only side data | 6 (24.166-27.787) | right side, both arches in frame |
| 8 | Reassembly + full truck | comp_explode -> clean car4 | FULL TRUCK (06) | travel ends at the rear; parts fly home on the 27.787 crash, one per beat | 10 (27.787-33.822) | high rear-right 3/4, whole truck, descends |
| 9 | Logo | logo_card | - | small logo, ~2.4 s visible, fades with the track | 33.822-38.37 | - |

## 3. Music map (kick grid 0.6035 s, phase 0.024; b_n = 0.024 + 0.6035 n)
| t | beat | event |
|---|---|---|
| 0.000 | - | S1 starts, moving |
| 4.852 | b8 phrase | cut -> S2a grille detail |
| 7.266 | b12 | cut -> S2b, grille starts moving 7.266, GRILLE label 7.870-9.380 |
| 9.080 | silent beat | grille parked, held still |
| 9.681 | b16 DROP | cut -> S3, bumper moves on the cut |
| 10.887 / 12.095 | b18 / b20 | FRONT BUMPER label 10.887-12.700; turn starts 12.095 |
| 14.509 | b24 | cut -> S4 hero |
| 15.716-17.830 | b26 | FRONT BUMPER REMOVED label; 16.923 (b28) second label RADIATOR CORE (only if visible in the render) to 17.83 |
| 18.130 | b30 | cut -> S5, hood lifts 18.433, lands 19.337 |
| 19.337 | b32 accent | HOOD label 19.337-20.240 |
| 20.544 | b34 | cut -> S6; FRONT STRUCTURE 21.751-23.260 (+ RADIATOR SUPPORT 22.959-23.860 only if visible) |
| 24.166 | b40 | cut -> S7, flares out 24.770-25.373; FENDER FLARES 25.373-27.480 |
| 27.787 | b46 CRASH | cut -> S8, parts fly home one per beat, lock 30.201 (b50), clean-car swap on 30.201 |
| 31.408 | b52 | FULL TRUCK label 31.408-33.220, fade to black 33.22-33.822 |
| 33.822 | b56 | logo card (fade in 0.3 s, fully gone with the track ~37.4), black to 38.37 |

## 4. Diff against v1
| v1 shot | v2 | why |
|---|---|---|
| s1_front34 | **dropped -> new S1** | crops the bed; opener must show the whole truck |
| s2_rear34 | **dropped** | `ive director`: same view as s1 (IoU 0.84); no rear scan data; ping-pongs front->rear->front |
| s3_grille | **reused unchanged** as S2a (49 frames, cut at 2.414 s) | right content, right section, now first detail of the front |
| s4_arch | **dropped** | busy/dark lower half (review.md), arch is covered by the flares scene; no reused-section |
| s5_open | **dropped -> new S2b/S3/S4/S5/S6** | showed hood HINGED open (no hood-open scan = fake opening, rule D); bumper+grille+hood in one wide shot |
| s6_top | **dropped** | rotating top-down shows no scanned feature (wasted rotation rule) |
| s7_explode (+ v2 label draft) | **dropped -> S8 reassembly only** | all parts separating at once in one wide orbit (standing rule) |
| logo | kept card, shown shorter (~2.4 s visible) | "last scenes held too long" sibling notes |

Sections per shot (rule B): S1 whole, S2a/S2b grille, S3 bumper, S4 front (bumper-off state), S5 hood, S6 front structure,
S7 side/flares, S8 whole (reassembly from rear 3/4). The front is one continuous sequence S2a-S6; nothing is shown twice.

## 5. Open questions (do not guess)
- Second labels (RADIATOR CORE in S4, RADIATOR SUPPORT in S6): the coordinator's backs.png check confirms radiator support,
  radiator core, a full-width lower horizontal beam and lamp housings in `bhr`. Use them only if that exact component is
  readable in the final S4/S6 frames; otherwise one label per shot. Do NOT call the lower beam a "crash beam" (not proven).
- Is S2b's composite (grille removed, bumper on, fbrhc core visible through the grille opening) acceptable? No scan of
  "grille off, bumper on" exists; the core shown is from the fbrhc state (bumper off). Fallback: grille and bumper come off
  together on the drop and the grille separates from the bumper in clear space in S3 (then S2b = highlight + label only).
