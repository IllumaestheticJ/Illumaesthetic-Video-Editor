# Direction: stock NB Miata scan-process reel v4 (scene director, 2026-11-11)

Format: 240SX-style scan-process. IRL scanning (rough cut, ONE shot per 1:1) -> hard 1:1 cut on the drop -> scan scenes
-> dissolve into the illumaesthetic.com NB 3D-scan listing. NB only, no Grimace. No bracing-test text (no control/jacked
widths, no deltas). HUD = triangle counts from STL headers and part/state names from scan files only, as `label` items
(the `counter` easing stops at 99.9 %).

What I looked at: lessons.md (all), style-guide.md, clips.md, project.yaml, editlog, feedback, review.md; contact sheets of
renders s1_ground, s2_jacked, s3_bar, s4_reassy, s5_end_graded (8 frames each); the editor's look renders
`/home/user/media/work/miata/look/fs_{car,tabs,stripped,bumper,sb,cb}.png`; rough-cut frames at 372.4-377.6 s.

## 1. Feature inventory

| scan / source | frame | what it shows (seen in renders) | weak data | use |
|---|---|---|---|---|
| Control Ground Scan (24,997,127 tris) | car | whole car, hood closed, hardtop on, bumper on. Front wheel captured (rim + tyre). | hood blotches; rear wheel ragged | end hero pass = listing render angle |
| Strut Tower Jacked Exterior (24,993,431) | car | whole car, front corner on a jack | rear wheel/arch ragged (s2 frames 20-75), wheel lip torn | side scene after IRL 1:1 #2 |
| Top Bumper Mounting Tabs (4,997,961) | car (ICP identity) | front end, hood open, bumper ON: bay, top of bumper, headlights | hood itself only shards at the cowl | "before" state of the bumper removal |
| Bumper Only (4,999,725), part, 2.9 mm median | car | front bumper skin with two mounting tabs on the top edge (fs_bumper.png) | inner face NOT yet checked | the removed part |
| Frontend Stripped (4,994,051) | car (ICP identity) | front end, bumper REMOVED + hood open: horizontal crash beam across the nose, its end brackets, headlights, lower front structure, radiator area, bay (fs_stripped.png) | front end only (ragged edge behind the front wheels, right fender lip), hood shards | HERO: bumper-removed section |
| Engine Bay Control (4,997,392) | own bay frame | hood open, bay with bumper on (badge at bottom of s3), no brace | cowl shards above the bay | 1:1 target from the IRL bay shot |
| Strut Brace Jacked Up -> strut bar part (28k tris, diff vs control, 3.6 mm) | bay frame | real scanned strut bar across the towers | thin; vanishes on the silver bay unless it silhouettes on black | engine-bay part beat |
| Fender Brace / Fender+Strut / Jacked Up Engine Bay | bay frame | other brace states | - | not used (same bay, no new view) |
| NB Trunk Closed / NB Trunk Open (50 MB each, just downloaded) | unknown | trunk states | registration NOT checked | rear scene only if they register (rule D) |
| Rough cut 372.33-375.67 | IRL | tech scanning the ENGINE BAY with the Artec, hood open, bumper on, intake/plug wires/badge/headlight/strut tower visible, moving camera | tech's back fills the left third; window must track the scanner | opener + 1:1 #1 |
| Rough cut 201.95-204.75 | IRL | tech + scanner at the right door, front corner on the jack | short | 1:1 #2 into the jacked scan |

Region richness (states + parts + features + quality):
- **Front end / engine bay: richest.** 3 states (bumper on hood open, bumper removed, bay control) + 2 real parts (bumper,
  strut bar) + the only IRL span that clearly shows scanning. Gets the opener, the drop and the hero beat.
- **Side: medium.** One state (jacked) + IRL 1:1 #2. Weak rear wheel.
- **Rear: none until trunk registers.** Hood-closed rear exists only inside the full-car scans.
- **Top / interior / wheels: nothing scanned in a state of its own.** No scenes.

## 2. Scene list (v4)

Travel: engine bay -> nose -> right side -> (rear) -> hero pass that lands on the listing's front-left angle. Each section
appears in one continuous run; the front/bay runs scenes 1-4 back to back.

| # | scene | scans used | section | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | irl_bay | rough cut 372.5 -> solved frame (~375.5, pick the sharpest frame with badge + bumper edge + headlight + intake filter + strut tower visible, before 375.67) | IRL, engine bay | the tech scanning the bay with the handheld Artec | user: v3 opener "too cropped, doesn't show the actual scanning". This is the only text-free span where scanner, hands AND the subject are all in frame. Front/bay = richest region, so the opener is there | 6 | 9:16 window (1215 px) keyframed to follow the scanner head and the bay it points at, easing onto the solve window over the last ~1 s. Scanner + hands + bay must be in the first/mid/last frame. If no window holds them, use the FG2 canvas (wider crop on a blurred fill) and render the scan on the same canvas. One shot only (rough-cut rule) |
| 2 | scan_bay | Engine Bay Control + strut bar part | engine bay | 1:1 bay, then the STRUT BRACE lifts straight up out of the bay onto black, holds, drops back onto the towers | same state as the IRL (hood open, bumper on, no bar). The bar lives in this frame, so the only bay part beat follows the bay 1:1 without a cut. One-part region = short | 8 (2 hold on 1:1, 2 lift, 2 hold, 2 drop) | 1:1 ON THE DROP. No spin (the bar's back face shows nothing new: GT3RS/C5 rule). Push up/back ~10 % so the lifted bar spans >= 70 % of the width on black. Labels: `ENGINE BAY` / `4,997,392 TRIANGLES` on the hold; `STRUT BRACE` while lifted. Keep cowl shards out of frame |
| 3 | scan_bumper_off | Top Bumper Mounting Tabs -> Bumper Only + Frontend Stripped | front end | front 3/4 of the hood-open nose, bumper on; bumper slides forward + down into clear black (tipped ~90 deg about the width axis ONLY if its inner face/tabs are scanned), base swaps Tabs -> Stripped as it clears | rule C: bumper-removed scan exists = its own section. Tabs scan is the real "before" state (no need to build it from Stripped + bumper). Cut on a kick from the bay (bay frame -> car frame) | 8 | Front 3/4 from the left at bumper height + ~25 deg down; nose fills the frame width with margins; nothing behind the front wheels in frame (Stripped ends there). Bumper never crosses the body or flies at the lens. Labels: `FRONT BUMPER REMOVED`; `MOUNTING TABS` on the bumper only if the tabs read in the render |
| 4 | scan_crash_beam | Frontend Stripped (2 mm) | front end (detail) | slow push-in on the exposed crash beam, its end brackets/mounts, lower front structure | hero beat (rule C), richest region -> biggest musical moment | 8 | Start where scene 3 ends (no new angle), push in 10-15 %, beam fills ~80 % of the width; hold >= 4 beats still enough to read. Labels `CRASH BEAM` then `MOUNTING POINTS`, only after the editor looks at a 2 mm still and sees them; drop a label that isn't visible. Optional `4,994,051 TRIANGLES` |
| 5 | irl_side | rough cut 202.70 -> 204.70 (if 201.95-204.75 is one continuous camera shot; else 203.75 -> 204.70) | IRL, side | tech with the scanner at the right door, front corner on the jack | second transformation, new section (side). Same rule: one shot, ends on the solved frame | 4 (2 if not continuous) | existing crop x0=660 / cam_C_crop; check the scanner is inside the window |
| 6 | scan_side | Strut Tower Jacked Exterior | side | 1:1 at the door, then pull back to the whole right side incl. the jacked front corner | only side state. v3 s2 ended on the ragged rear wheel with the car clipped (rule A) and never showed the jack | 8 | 1:1 ON AN ACCENT. Pull back + rise to a full-car right-side 3/4 with the whole car in frame (deliberate margins), jacked front corner visible; keep the rear wheel small. Label `24,993,431 TRIANGLES`. No "jacked / no bracing" text |
| 7 | scan_rear (CONDITIONAL) | NB Trunk Closed -> NB Trunk Open, only if both register to the car (median < ~3 mm, real overlap, red-over-silver check) | rear | trunk lid opens on a hinge fitted to the open scan, push in on the trunk | rule D. No registration = no scene (the reel is complete without it) | 8 | rear 3/4 continuing from scene 6's side; check the plate is unreadable at final res. Label `TRUNK OPEN` |
| 8 | scan_end | Control Ground | hero pass (full car) | lands on the listing's stock-front-left angle, grades to listing grey | listing hero is a render of this scan (240SX v3 / FG2 rule) | 4 | reuse s5_end_graded from ~frame 31 (front-left 3/4 onward); the first half is a straight-on front orbit = wasted rotation + a second front view |
| 9 | website | webzoom_nb.mp4 | listing | NB 3D-scan listing, title -> logo -> URL | ending | 12 (was 16) | 0.5 s dissolve from scene 8 ("last scenes held too long" rule) |

Totals: 58 beats (~29 s) without scene 7; 66 with it (then website starts on beat 54).

Sections, one run each: IRL bay | engine bay (2) | front end (3, 4) | IRL side | side (6) | rear (7, conditional) | hero
full car (8) | listing. The front-left 3/4 in scene 8 is the listing match, not a second front sequence (no detail, whole car).

## 3. Music map (track TBD; 1 beat ~ 0.5 s, beat 0 = first audible hit used)

| beat | scene | must land on |
|---|---|---|
| 0 | 1 irl_bay | a percussive hit (not a silent intro) |
| 6 | 2 scan_bay (1:1 #1) | **the drop**. Pick the music start so its drop is 6 beats in |
| 14 | 3 scan_bumper_off | phrase line (drop + 8) |
| 22 | 4 scan_crash_beam | **strongest section change after the drop** (drop + 16). If the track's big change is later (e.g. drop + 24), lengthen scene 2 or 3 by whole phrases so scene 4 starts on it; never stretch the bumper removal itself past 8 beats |
| 30 | 5 irl_side | phrase line |
| 34 | 6 scan_side (1:1 #2) | an accent (half phrase); 32 if the IRL side shot is only 2 beats |
| 42 | 8 scan_end (or 7 scan_rear) | phrase line |
| 46 | dissolve -> 9 website | phrase line; end on the last hit and let it ride the decay (50 with scene 7: 7 = 42-50, 8 = 50-54, website 54-66) |

Fit the grid to kick peaks (not `ive beats` BPM), first clip one frame short, verify cuts vs kicks on the delivered file.
Check projects/*/project.yaml + editlogs so the track isn't one another reel already used.

## 4. Diff vs v3 timeline

| v3 | v4 | why |
|---|---|---|
| irl_front (187.0-187.7) + scan_ground (s1_ground) | **dropped** | user: opener too cropped, no scanning visible; s1 starts with the car clipped on both sides and the front 3/4 would repeat scene 3's front (rule B) |
| - | **added** scene 1 irl_bay | shows the actual scanning; front/bay is the richest region |
| scan_bar (s3_bar) + scan_reassy (s4_reassy) | **merged** into scene 2 (new render from the bay 1:1) and **moved** to right after the drop | two shots of the same bay (rule B); s3 spins the bar for no reason; the bay is where the IRL opener already is, and the bay scan has the bumper ON, so it must come before the bumper removal (after it would put the bumper back on screen) |
| - | **added** scenes 3 + 4 (bumper removed) | rule C hero beat; Tabs + Bumper + Stripped all register in the car frame |
| irl_side + scan_jacked (s2_jacked) | kept, **re-rendered** pull-back | rule A (car clipped, ragged rear wheel last), jack never in frame |
| - | scene 7 rear | only if trunk scans register |
| scan_end (s5_end_graded) 4 s | kept, **trimmed** to the last 4 beats | removes the straight-on front orbit |
| website 8 s | 6 s | last scenes held too long |
| HUD hud_nb.mov (bracing numbers) | **rebuild** | user: no bracing-test text |

Renders:
- **Reuse as-is (trim only):** s5_end_graded (from ~frame 31), webzoom_nb.mp4.
- **New:** scene 2 scan_bay (new 1:1 solve on the 372-375 IRL frame into Engine Bay Control + bar lift/drop), scene 3
  scan_bumper_off, scene 4 scan_crash_beam, scene 6 scan_side (same cam_C_crop start, new pull-back), scene 7 if trunk registers.
- **Fallbacks if render time is short:** scene 6 = s2_jacked frames 1-~45 (6 beats, before the ragged wheel dominates);
  scene 2's drop-back = s4_reassy (check the bar's orientation matches at the cut: s3 had spun it 180).
- **Retired:** s1_ground, s3_bar, irl_front.mp4.
- Contact sheet of first / middle / last frame of every shot before assembly (rule A); per-frame luma scan of every
  animated-part render (persistent data off).

## 5. Open questions for the editor (don't guess)
1. Is the car in the 372-377 IRL shot on the ground and with no strut bar (= Engine Bay Control)? I see no bar across the
   towers in 372.4-375.6, but check at full res. If it is the brace or jacked state, cut 1:1 into that bay scan instead.
2. Can Engine Bay Control be ICP'd onto the Top Bumper Mounting Tabs scan (both hood open, bumper on)? If yes, scenes 2 -> 3
   can be one continuous camera move in one frame (bar lifts, camera drops to the nose, bumper comes off) and the bar can
   ride along in scene 3. If not, keep the kick cut between 2 and 3.
3. Is the Bumper Only scan's inner face captured? Render it from behind before tipping it or labelling `MOUNTING TABS`.
4. Do Frontend Stripped and Tabs differ only at the bumper? If Stripped also lost/moved anything else, use a composite
   (Tabs minus bumper zone + Stripped >7 mm from it) so the swap under the moving bumper doesn't pop.
5. Is rough cut 201.95-204.75 one continuous camera shot (no cut at ~203.72)? Sets scene 5 at 4 vs 2 beats.
6. Trunk Open/Closed: register to the car (red-over-silver + median) before scene 7 exists.
