# Porsche 911 GT3 RS (992) - direction v2 (scene director + director, 2026-11-11)

Stage 1 (scene order from the scan inventory) and stage 2 (shot plan: focus, holds, redundancy cuts, render budget)
are both in this file. The editor renders and assembles; nothing here has been rendered yet.

Looked at before deciding: `out/sheet_v1.jpg`, 8-frame sheets of every `renders/final/s*` folder, full-res frames
s6 f73 / s8 f62 / s8 f90 (cut-outs), `reg_all_0..3.jpg`. Read lessons (all, incl. the 2026-11-11 user rules
A-D, "rotations wasted", "section at a time", "spin only if the backside is useful", "clear background",
"Temerario: progressive explode, fade, small logo"), style guide, Temerario timeline, clips.md, project.yaml,
timing.json, editlog, review, director_report, tools/shots.py.

Scan frame: front = -Y, car's left = +X, z up, metres, car 4.58 m. Camera numbers below are for
`tools/shots.py` (30 mm on the 20.25 mm sensor = 37.3 deg horizontal FOV: frame width = 0.675 x distance).

---------------------------------------------------------------------------------------------------------------
## 1. Feature inventory

### Scan files
| Scan | Region | What it shows (looked at) | Data | Use in v2 |
|---|---|---|---|---|
| gt3 rs Full Car (car4 4 mm / car2p5 2.5 mm) | all | whole car, wheels, centre-lock + drilled discs, swan-neck wing + end plates, fender louvres, deck louvres | 25M tris; **weak**: hood nostrils are dark holes, dark blotch on hood by the windscreen, grille bars partly missing, plate area blank box | every shot |
| front_lower_lip | front | splitter lip, mounting holes on its top face | thin add-on; cut-out under it is small (s6 f73: bumper edge stays closed) | **moves** (front) |
| front_grille_trim | front | centre intake trim | cut-out is a **hollow black opening** (s6 f73) | **moves only toward camera, 0.15 m, on the camera ray** (self-occludes its hole); stays home in wide shots |
| front_bumper_strake (both corners, one file) | front | bumper-corner strakes | cut-outs are **hollow** (v1 s6/s8) | **stays on** - no data behind it, moving it implies a hole |
| fender_vent (car's right front fender) | front-right | louvre panel; inner face textured | cut-out is a **ragged hole** in plain view (editlog, s8 f90) | **stays on**; louvres get a detail shot instead |
| hood_vent_top_warped (left nostril top) | front/top | thin nostril top blade | underneath was already a nostril hole + the interface duct (stays) | **moves** up into black above the roofline |
| hood_vent_interface_assembled_left | front | nostril duct | reads as a bracket when moved (editlog) | stays on |
| side_skirt_upper / sideskirt_lower / side_skirt_strake | left side | sill pieces (strake = blade at the front of the sill behind the FL wheel) | inner flanges are real data the car never saw; sill cut-out may be hollow (check) | **move** (side) |
| rear_qpanel_intake_1 (right) / _2 (left) | rear | intake surrounds with duct depth | rings, inner duct readable | **move** (rear) |
| rear_bumper_strake (left) | rear | rear bumper fin | cut-out likely hollow (same construction as front strakes) | **stays on** (see open question 2) |
| rear_diffuser_1 | rear | diffuser fins **+ undertray** | biggest piece of data the car scan never saw | **moves** (rear) - the best reveal in the set |
| rear_diffuser_trim_outer | rear | lower rear bumper skin | removing it leaves the bumper hollow | **stays on** |
| Rear Bumper, hood vent interface right/no fins, fins, 992 GT3 diffuser, underbody DRS | - | unusable (clips.md) | - | not used |

**States: none.** No hood/trunk/door open, no bumper-removed scan, DRS-open shows no wing change.
Rules C and D therefore mean: no opening, no bumper-off, no hero "bumper removed" beat, no labels claiming a removal.
Only separate registered part scans move, and only where the hole they leave is not blank (see "Moves" column).

### Region richness (parts that may move + signature + quality)
| Region | Moving parts | Signature | Quality | Score | Screen time |
|---|---|---|---|---|---|
| Front | lip, hood vent top, grille trim (small) | lip, strakes, nostrils | nostrils/blotch weak, grille holes | **high** | 8.5 s (front + right fender) |
| Rear | diffuser (+undertray), QP intake 1+2 | swan-neck wing, end plates, deck louvres, diffuser fins | good | **high** | 4.7 s |
| Side (left) | skirt lower, skirt upper, skirt strake | low sill aero | good | medium | 3.75 s |
| Wheels | none | centre-lock, drilled discs | good (2.5 mm) | medium, no parts | 1.8 s |
| Top | none | wing planform | hood defects | low alone -> used only as the "everything off" overview | 3.75 s |
| Engine bay / interior / underbody | none | - | no data | **0** | none |

---------------------------------------------------------------------------------------------------------------
## 2. Scene order (stage 1)

One clockwise lap of the car, one sequence per section, parts come off section by section **and stay off**
(progressive explode), then all removed parts together from above, then the stack + reassembly on the drop.

| # | Section | Scene | Scans | Feature shown | Why here (inventory) |
|---|---|---|---|---|---|
| 1 | whole | low front-left 3/4, whole car | car4 | whole car, nose aero + wing silhouette | opener on the richest end (front: most moving parts + strakes/lip); whole car in frame from frame 1 (user rule) |
| 2 | wheel | FL wheel close-up | car2p5 | centre-lock, drilled discs | next to the opener's camera position (travel, no jump); signature with no parts -> short |
| 3 | front | nose: lip off, grille trim toward camera, hood vent top up | comp + parts | front aero | richest region, gets the longest scene; camera stays on the nose while parts move |
| 4 | front | right front fender louvres (parts held off) | comp + parts | fender louvres | finishes the front section on the louvres (signature that can't move) |
| 5 | rear | swan-neck wing mounts + deck louvres | car2p5 | wing mounts | lap continues to the rear; wing is the strongest rear signature |
| 6 | rear | rear-right 3/4: diffuser + undertray slides back, both QP intakes out | comp + parts | diffuser, intakes | rear parts; diffuser undertray is the best hidden data |
| 7 | side | left sill dolly rear -> front: skirts drop/out, strake out | comp + parts | side skirts | lap closes at the front-left; 3 parts -> 8 beats |
| 8 | top | high rear over to near top-down, all removed parts around the car | comp + parts | everything off, wing planform | first view of the whole progressive explode; replaces v1's top-down (which repeated s8) |
| 9 | whole | drop: parts rise into layers above the car (side view), fly home, lock, rear-left 3/4 hero, fade | comp + parts | exploded stack, reassembly | the biggest musical moment for the payoff of all 9 moving parts (Temerario 25-35 s) |
| 10 | logo | small logo on black | - | - | Temerario ending: fade, then small logo |

---------------------------------------------------------------------------------------------------------------
## 3. Music map (measured onsets only)

Cut points come only from the editor's decoded-audio onsets (2026-11-11). v1's 9.40 / 24.40 cuts were 228 ms late
(swells), so they are gone. Big hits: 3.779 b8, 7.530 b16, 11.281 b24, 14.093 b30, 18.779 b40, 22.063 b47,
22.532 b48, **26.285 b56 drop**, 29.121 b62, 31.905 b68, 33.782 b72, 35.669 b76. Medium hits used: 5.565 (b12),
9.311 (b20), 16.807 (b36), 20.567 (b44). Part motions inside a shot may use grid times (they are not cuts).

| Cut | t (s) | frame | onset | into |
|---|---|---|---|---|
| start | 0.000 | 0 | - | Sh1 whole |
| 1 | 3.779 | 113 | big b8 | Sh2 wheel |
| 2 | 5.565 | 167 | medium b12 | Sh3 front nose |
| 3 | 11.281 | 338 | big b24 | Sh4 right fender |
| 4 | 14.093 | 423 | big b30 (early) | Sh5 wing |
| 5 | 16.807 | 504 | medium b36 | Sh6 rear parts |
| 6 | 18.779 | 563 | big b40 | Sh7 side |
| 7 | 22.532 | 676 | big b48 | Sh8 top overview |
| 8 | 26.285 | 789 | **drop b56** | Sh9 stack + reassembly |
| fade | 32.40 -> 33.30 | 972 -> 999 | after lock b68 | to black |
| 9 | 33.782 | 1013 | big b72 | logo fades in (0.4 s), holds through 35.669/36.1, fades out 37.4 -> 38.0 |
| end | 38.000 | 1140 | decay ~37.8 | - |

Assembly: use the Cappuccino workaround (`transition: {type: fade, duration: 0.0333}` + one extra real frame per
outgoing clip) instead of `type: cut` to avoid the duplicated frame before every cut (v1 review item 9).

---------------------------------------------------------------------------------------------------------------
## 4. Shot plan (stage 2)

Render settings as v1 (`res_pct 75`, 12 spp, 15 fps, minterpolate). Every new render: +3 tail frames (lesson:
15 fps freeze). Base for part shots = `comp_explode4` + every part that stays on (front_bumper_strake, fender_vent,
hood_vent_interface_assembled_left, rear_bumper_strake, rear_diffuser_trim_outer) as static blends; all moving
parts as `parts` with keys. **Parts that came off in an earlier section stay at their off offset in every later shot**
(keys = constant offset) until Sh9. Offsets below are metres relative to home; rot in degrees.

"Off offsets" (state after their section; used as constants in later shots):
| Part | off offset | rot | set in |
|---|---|---|---|
| front_lower_lip | (0, -0.30, -0.14) | (-12, 0, 0) | Sh3 |
| front_grille_trim | (0, -0.15, +0.035) | 0 | Sh3 |
| hood_vent_top_warped | (0, -0.20, +0.62) | 0 | Sh3 |
| rear_diffuser_1 | (0, +0.55, -0.06) | (+10, 0, 0) | Sh6 |
| rear_qpanel_intake_1 (right) | (-0.45, -0.25, +0.15) | 0 | Sh6 |
| rear_qpanel_intake_2 (left) | (+0.45, -0.10, +0.25) | 0 | Sh6 |
| sideskirt_lower | (+0.25, 0, -0.30) | 0 | Sh7 |
| side_skirt_upper | (+0.35, 0, -0.12) | 0 | Sh7 |
| side_skirt_strake | (+0.30, -0.05, -0.20) | 0 | Sh7 |

No part spins: only the lip tilts 12 deg (its top face carries the mounting holes) and the diffuser 10 deg (undertray
top) - lesson "spin only when the backside is useful". Moves go into clear black (below the nose, above the roofline,
past the silhouette, below the sill) or straight down the camera ray when the cut-out behind is hollow.

### Shot table
Times are reel seconds; "local" part times = reel time - shot start (shots.py keys are local).

| Sh | Section | Reel start-end (frames) | Focus | Camera (scan frame) | Part action | Source | New frames |
|---|---|---|---|---|---|---|---|
| 1 | whole | 0.000-3.779 (0-113) | whole car, nose-led | low front-left 3/4, **slide + 6 % push, no orbit > 8 deg**. t0 loc (3.9, -6.6, 1.05) tgt (0.15, -0.2, 0.5) f30 -> end loc (4.3, -6.0, 0.95) tgt (0.2, -0.15, 0.5) f30, ease out. Distance 7.6 -> 7.2 m (frame 5.1 -> 4.9 m wide vs car ~4.1 m projected) | none | **NEW** car4 | 57+3 = **60** wide (~14 s) |
| 2 | wheel | 3.779-5.565 (113-167) | FL centre-lock + drilled disc | v1 s3 path (slide back along the arch) | none (all parts home) | **REUSE s3_wheel** f1-f28 (`dur` 1.80, src_fps 15) | 0 |
| 3 | front | 5.565-11.281 (167-338) | nose aero | low front-left 3/4 swinging to dead-ahead front, slight rise; keys at local 0 / 2.0 / 5.72: loc (2.0, -5.2, 0.75) tgt (0.25, -1.9, 0.45) -> (0.9, -5.5, 0.9) tgt (0.1, -1.95, 0.5) -> (0.0, -5.6, 1.05) tgt (0, -1.95, 0.55), f30, inout. Distance ~3.7 m: nose 1.9 m in a 2.5 m frame | lip: home until 7.530 (b16), out to its off offset by 9.311 (b20 medium), ease inout. grille trim: 8.465 -> 9.311. hood vent top: 9.311 -> 10.340, rises above the roofline (clear black from this camera height). Hold 10.34-11.28 while the camera finishes its last 0.3 m | **NEW** comp + 3 parts | 86+3 = **89** (~16 s) |
| 4 | front | 11.281-14.093 (338-423) | right front fender louvres | right-front, looking down onto the fender, slide rearward: loc (-2.35, -2.45, 1.35) tgt (-0.82, -1.20, 0.72) -> loc (-2.45, -1.35, 1.45) tgt (-0.84, -1.05, 0.74), f30, inout. Keep the hood top (blotch) out of frame: crop at the hood shut line | lip/grille/hood vent held at off offsets (lip visible lower-left = continuity) | **NEW** comp + parts | 42+3 = **45** (~18 s) |
| 5 | rear | 14.093-16.807 (423-504) | swan-neck mounts + deck louvres | v1 s5 high behind, sliding across | none visible (front parts are out of view from behind) | **REUSE s5_wing** f5-f45 (`trim_start` 0.27, `dur` 2.71) - the centred part; wing tips leave frame deliberately (mount detail) | 0 |
| 6 | rear | 16.807-18.779 (504-563) | diffuser + undertray, QP intakes | low rear-right 3/4, push-in: loc (-2.5, 5.4, 1.15) tgt (-0.2, 1.7, 0.55) -> loc (-2.15, 5.0, 1.05) tgt (-0.15, 1.75, 0.5), f30. Whole rear incl. wing end plates in frame (frame ~3 m wide) | diffuser: 16.807 -> 17.60 back toward camera into black below the bumper (undertray top shows). QP 1 (near, right): 17.10 -> 17.90 out past the near silhouette; QP 2 (far, left): 17.10 -> 17.90 out past the far silhouette. Hold to 18.78 | **NEW** comp + parts | 30+3 = **33** (~16 s) |
| 7 | side | 18.779-22.532 (563-676) | left sill aero | **dolly** along the left side, rear -> front, no rotation: loc (3.3, 1.4, 0.55) tgt (0.85, 0.9, 0.28) -> loc (3.3, -0.95, 0.55) tgt (0.85, -0.6, 0.28), f30, inout. Sill at frame centre, black below | lower skirt 18.779 -> 19.718 (drops into black + out); upper 19.249 -> 20.187; strake 20.567 (b44 medium) -> 21.40. Hold to 22.53 (the 22.063 hit lands on the held, fully off sill) | **NEW** comp + parts | 56+3 = **59** (~16 s) |
| 8 | top | 22.532-26.285 (676-789) | all 9 removed parts around the car + wing planform | crane from high rear-left to **11 deg off vertical** (lesson: never key straight down), nose at top of frame: loc (2.0, 4.4, 4.4) tgt (0, 0.2, 0.5) -> loc (0.9, 1.6, 6.8) tgt (0, 0.1, 0.45), f30, inout. Wing nearest the lens; hood (defects) far and small | all parts static at off offsets | **NEW** comp + parts (static) | 56+3 = **59** (~14 s) |
| 9 | whole | 26.285-33.30 (789-999) | exploded stack -> reassembly | left side profile, slow rise + max 45 deg drift to a rear-left 3/4 hero. local keys: 0 loc (7.8, 0.1, 1.9) tgt (0, 0.05, 1.3); 3.75 (=30.03) loc (6.9, 3.6, 2.6) tgt (0, 0.2, 1.2); 5.62 (=31.905) loc (5.2, 5.6, 1.4) tgt (0, 0.3, 0.6); 7.0 loc (5.0, 5.4, 1.35) same tgt. f30. Whole car + stack in frame at every key (frame >= 5.1 m wide) | **drop 26.285**: parts rise from off offsets into 3 layered columns above their own homes (absolute z): front col lip 1.75 / grille trim 2.05 / hood vent top 2.35; mid col skirt lower 1.75 / upper 2.00 / strake 2.25; rear col diffuser 1.75 / QP intakes 2.10 (x,y back to home +-0.1). Staggered starts 26.285, +0.12 per part, lower layers first, top layer lands on **29.121 (b62)**. Hold/drift 29.12-30.03. Fly home 30.033 -> **31.905 lock (b68)**, ease in. Assembled hold 31.9-32.4, fade 32.40 -> 33.30 (in assembler) | **NEW** comp + parts | 105+3 = **108** (~16 s) |
| 10 | logo | 33.782-38.000 (1013-1140) | logo | - | - | **NEW card** (tools/logo_card.py, not Blender): logo at **~28 % frame width** (v1 card was ~85 %), fade in 33.78 -> 34.2, hold, fade out 37.4 -> 38.0 | 0 |

Section of every shot: Sh1 whole, Sh2 wheel, Sh3-4 front, Sh5-6 rear, Sh7 side, Sh8 top, Sh9 whole, Sh10 logo.
Each section appears once and its shots are adjacent. Sh1 and Sh9 are both "whole" but from different sides with
different content (closed car front-left 3/4 vs exploded stack side / rear-left 3/4); keep them apart in ive director.

### Render budget (one CPU box, serial)
| Shot | frames | s/frame | time |
|---|---|---|---|
| Sh1 | 60 | 14 | 14.0 min |
| Sh3 | 89 | 16 | 23.7 min |
| Sh4 | 45 | 18 | 13.5 min |
| Sh6 | 33 | 16 | 8.8 min |
| Sh7 | 59 | 16 | 15.7 min |
| Sh8 | 59 | 14 | 13.8 min |
| Sh9 | 108 | 16 | 28.8 min |
| **total** | **453** | | **~118 min (within ~2 h)** |
Reused unchanged: s3_wheel (f1-28), s5_wing (f5-45). v1 lighting check: no dropouts, reuse is safe; still run the
per-frame luma scan on every new render (lesson).
Render order (most important first, in case the queue dies; RESUME=1 keeps finished frames): Sh9, Sh3, Sh1, Sh6,
Sh7, Sh8, Sh4. If the budget overruns, Sh4 is the one to cut: then Sh3 runs to 14.093 (its camera continues to a
front-right 3/4 ending on the louvres, +42 frames) - same section, no other shot moves.

Before finals: 30 % previews of first / middle / last frame of every new shot (rule A) **plus** the frame where
each part is fully off (to judge its cut-out). Kill criteria at preview:
- Sh1/Sh9: any wheel, nose, wing end plate or stacked part within 5 % (54 px) of the frame edge -> increase distance.
- Sh3: black hole visible around the grille trim -> reduce its move to 0.08 m; never move it sideways.
- Sh7: a through-hole in the sill where the upper skirt was -> change its offset to (+0.15, 0, -0.02) (down the
  camera ray) and drop it later in Sh9 only.
- Sh6: hollow area under the bumper visible after the diffuser slides -> raise camera to z 1.35.

---------------------------------------------------------------------------------------------------------------
## 5. Diff vs v1

| v1 shot | v2 | Why |
|---|---|---|
| s1_turntable (low FL 3/4 turntable) | **dropped**, replaced by Sh1 (new) | nose clipped in every frame (sheet f1-f91); turntable = wasted rotation (lesson); ive director: s1~s2, s1~s8 |
| s2_rear (rear-right orbit) | **dropped** | wing tip clipped at left in all frames; same silhouette as s1 (IoU 0.83); rear section is now Sh5+Sh6 |
| s3_wheel | **reused** as Sh2, moved right after the opener | content right; FL wheel sits next to the opener's camera (travel) |
| s4_vent | **replaced** by Sh4 (new) | first frames dwell on the hood blotch + nostril holes; fast slide at midpoint; continuity needs the front parts held off |
| s5_wing | **reused** as Sh5 (trimmed f5-f45) | content right; only position changes |
| s6_lift (front 4 parts lift in a wide) | **replaced** by Sh3 | grille trim + strakes left hollow black openings (s6 f73); strakes now stay on, grille trim moves only along the camera ray; camera closer on the nose |
| s7_top (whole car to top-down) | **replaced** by Sh8 | repeated s8 (IoU 0.79); now shows the removed parts, hood far from the lens |
| s8_explode (13 parts at once, one wide orbit) | **replaced** by Sh3/4/6/7 (section by section) + Sh8 + Sh9 | user: all parts at once in one wide orbit; too wide; holes under strakes/fender vent/grille |
| logo (~85 % width, 4.2 s) | **re-made small** (~28 % width) | user: fade out, then small logo |

New parts that do not move any more: front_bumper_strake, fender_vent, rear_bumper_strake, rear_diffuser_trim_outer
(13 -> 9 moving parts) - each leaves a blank/hollow cut-out because no removed-state scan exists (user: no blank
space, never imply data).

---------------------------------------------------------------------------------------------------------------
## 6. Hold list (> 0.75 s without part motion)
| Shot | hold | reason |
|---|---|---|
| Sh2 | whole shot 1.8 s | camera slides along the arch; the disc/spokes parallax is the content |
| Sh3 | 10.34-11.28 (0.94 s) | three parts off at once in frame: let the viewer read the lip's mounting face; camera still moving |
| Sh6 | 17.90-18.78 (0.88 s) | diffuser undertray readable; push-in continues |
| Sh7 | 21.40-22.53 (1.1 s) | dolly continues to the strake / FL wheel; parts off |
| Sh8 | whole shot 3.75 s | crane is the motion; new information = every removed part seen together |
| Sh9 | 29.12-30.03 (0.9 s), 31.9-32.4 (0.5 s) | full stack readable before flying home; assembled car on the lock hit, then fade - kept short (user: don't hold last scenes) |

---------------------------------------------------------------------------------------------------------------
## 7. Text / labels - recommendation
The original brief says **no text**; rule C asks for short factual labels **only for bumper-removed data**, which this car
does not have. Recommend **no labels** in v2. If the user wants labels anyway, the only honest wording is part names
from the scan files over the scan shots (e.g. "REAR DIFFUSER + UNDERTRAY" in Sh6, "FRONT LIP" in Sh3), never
"REMOVED" and no numbers that are not in the files. Ask before adding.

## 8. Open questions for the editor / user
1. Is the side_skirt_upper cut-out hollow? (decide at the Sh7 mid preview; rule above.)
2. rear_bumper_strake: if a 30 % render of the car with it cut out shows a closed bumper surface, it may join Sh6
   (offset (+0.25, +0.20, 0)) and the Sh9 rear column; otherwise it stays on (default).
3. Labels: confirm "none" (section 7).
4. Sh5 reuse keeps v1's crop on the wing mounts with the end plates leaving the frame; if the reviewer reads that as
   accidental cropping (rule A), re-render it wider (~40 frames close-up = 24 min) - over budget, so v3.
