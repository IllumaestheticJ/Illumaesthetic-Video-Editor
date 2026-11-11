# Ferrari 296 GTB - scene direction (v4)

Scene director, 2026-11-11. Inputs: clips.md, project.yaml (v3), director.md (v3 plan), editlog, feedback.jsonl, lessons.md
(incl. the user's all-reels standing rules A-D at the end of `.claude/agents/scene-director.md`), Temerario notes, `tools/shots.py`
(PARTS_V3 already carries rule D: louvre home through x_side, lifted off for x_lock).
Looked at: 8-frame sheets of every reusable render and the v3 30 % previews
(`/tmp/claude-0/scene/{s1_wide,s3_wheel,s2_rear,s7_top,s6_engine,f5_front}.jpg`, `/tmp/claude-0/v3prev.jpg`,
`/tmp/claude-0/scene/prev_structure.jpg`).

Music is fixed: ferrari296_track.mp3, grid t = 0.435 + k*0.5803. Accents 5.077 (k8), 9.719 (k16), 14.361 (k24),
drop-out 12.04-14.36, 18.423 (k31), **23.066 (k39, lift, loudest)**, 27.708 (k47), **32.350 (k55, heaviest bass)**, fade from 36.75.

## 1. Feature inventory (from clips.md + renders; all parts registered, median 1.6-5 mm)

| region | scans (state / part) | what it shows | quality / weak data | richness |
|---|---|---|---|---|
| whole | Full Car 25M (car4/car3) | whole car, front-right 3/4 reads best (lamps, side intake) | clean; s1_wide whole car in frame with margins | base |
| wheel (front right) | Full Car | 5-spoke wheel, drilled carbon-ceramic disc through the spokes | arch liner a bit ragged at the top; Brake Disk scan = arches with wheel off, not used | 1 detail |
| **front** | Hood Combined (top + inner) = part; Front Bumper Outer + Inner = part (both faces scanned); **Front Fully Removed** = state (hood captured propped OPEN, bumper off) | hood opens (state exists -> rule D ok); frunk; front bumper inner face; **structure behind the bumper** | grille ragged; a few dark holes in the frunk -> pass over the frunk, don't dwell | 2 parts + 2 states (hood open, bumper removed) = high |
| side (right) | Fender 2 (part; Fender 1 = same panel), Side Skirt Right (part), **Sideskirt Removed** (state) | fender up/out, skirt down, sill under it; side intake | Fender Bracket too small to read | 2 parts + 1 state = medium |
| **rear** | Rear Bumper Outer + Inner (part), **Rear Bumper Removed** (state), Rear Diffuser Outer + Inner (part), **Rear End No Diffuser** (state) | rear bumper + diffuser off, **rear structure behind them** | tail-lamp lenses are holes (keep lamps small/out of close-ups); check plate area; Exhaust Tip scan unused | 2 parts + 2 states = highest |
| engine bay | Enginer Cover (louvre, part), **Engine Bay** (state, lid OFF) | louvre lifts straight off, bay underneath | **no lid-open scan** -> never hinge it open (rule D); s6_engine's 85 deg hinge is now invalid | 1 part + 1 state |
| top | Full Car only | planform | no data of its own | none -> no top-down scene |
| interior | - | - | - | none |

Rear (+ engine bay) is the richest region, front second. Travel front -> side -> rear puts the richest region on the two strongest
accents (23.066 lift, 32.350 bass). Opener = front-right 3/4 because the front carries the first hero data (hood open, bumper
removed) and that is where the travel starts.

## 2. Scene order (v4)

Cut frames round(t*30): 0, 152, 222, 483, 622, 762, 901, end of scan 1005 (fade), logo in ~1023, black 1170.

| # | scene | section | video s (frames) | beats | scans used | focus / feature | why here (inventory) | camera / action |
|---|---|---|---|---|---|---|---|---|
| 1 | s1_wide | whole | 0.000-5.077 (0-152) | intro+8 | full car | whole car, front-right 3/4 | opener: whole car fully in frame (v1 note "too cropped", rule A), motion from frame 1; front 3/4 starts the travel at the front | REUSE unchanged (slow orbit -36 -> -66 deg; the only orbit in the reel) |
| 2 | s3_wheel | wheel (front) | 5.077-7.399 (152-222) | 4 | full car | front-right wheel + disc | extreme close-up next to the front; ends looking forward along the fender = hand-off to the front | REUSE unchanged |
| 3 | f5_front | front | 7.399-16.103 (222-483) | 15 | hood combined, Front Fully Removed, front bumper outer+inner | headlamp -> hood opens and STAYS -> frunk -> bumper slides out -> turns 65-80 deg to show its scanned inner face -> push in | reviewer v2 verbatim (hold the hood shot, pull the bumper and show it off); both bumper faces scanned so the turn shows real data | RENDERING NOW, unchanged. Internal hits land: hood 7.97-9.13, bumper out **9.714 (accent 9.719)**, turn 11.46 into the drop-out, push-in hold 13.2-16.1 over the quiet bars |
| 4 | **F_hero** (new) | front (structure) | 16.103-20.746 (483-622) | 8 | **Front Fully Removed** composite (comp_explode with hood open, bumper out) | **FRONT BUMPER REMOVED**: what is behind the bumper - camera moves in on the exposed front structure and holds | rule C: bumper-removed data is the hero beat and gets its own close-up; same section as f5, so it follows it directly (rule B) | see 4a. Label at 18.423 |
| 5 | x_side | side -> rear | 20.746-25.388 (622-762) | 8 | Fender 2, Side Skirt, Sideskirt Removed, rear bumper, diffuser, Rear Bumper Removed | fender up/out 20.75, skirt down 21.33, **rear bumper off 23.04 (on the 23.066 lift)**, diffuser 23.62 | the travel continues front -> rear along the right sill; the biggest accent = the rear bumper (richest region) coming off | spec in shots.py (not rendered yet). Rear bumper key lands on frame 691 vs accent 692: nudge with src_fps if the check shows it |
| 6 | **R_hero** (new) | rear + engine bay | 25.388-30.030 (762-901) | 8 | **Rear Bumper Removed + Rear End No Diffuser** fills, Enginer Cover, **Engine Bay** | **REAR BUMPER REMOVED**: camera over the pulled bumper moves in on the exposed rear structure, then the louvre lifts straight off on **27.708** and the camera rises over the engine bay | rule C hero for the richest region, directly after its bumper came off (rule B: x_side's tail and R_hero are one rear sequence); rule D: louvre lifts OFF, no hinge | see 4b. Labels: REAR BUMPER REMOVED (25.6-27.5), ENGINE BAY (28.4-29.9) |
| 7 | x_lock | whole (explode) | 30.030-33.512 (901-1005) | 6 (trimmed) | all parts | first and only view of the whole exploded car, fly home, **LOCK on 32.350** | the reassembly the Temerario ends on; heaviest bass | spec in shots.py (not rendered yet) - **fix its framing first (see 4c)**. Use in 0 -> 3.48 s; fade to black 33.0-33.5 |
| 8 | logo | logo | ~34.1-38.5, black to 39.0 | - | logo png | small Illumaesthetic logo (~35 % width) | brief: fade out, then a SMALL logo (Temerario) | rebuild logo_card small if the current one is larger |

Section list (rule B, each once, contiguous): whole 5.08 -> wheel 2.32 -> front 8.70 + front structure 4.64 -> side 2.3 -> rear 2.3
+ rear structure/engine bay 4.64 -> whole explode 3.48 -> logo. No section returns. No turntable besides the opener; no top-down.

### 4a. F_hero (new render, 4.633 s + 1 frame = 71 fr)
- Parts static at f5's end state: hood rot X -58 (open - Front Fully Removed captured it propped open), front bumper at BUMP_FAR
  rot Z 80 (f5 end pose = x_side start pose), fender/skirt/rear parts home, louvre home.
- Camera (scan frame, front = -Y, right = -X; nose at y ~ -2.27): hard cut from f5's bumper push-in to the right side of the
  open nose, ~35 deg down. Start ~(-1.55,-3.20,1.55) -> 18.423 (local 2.32) ~(-1.10,-2.95,1.30) -> end ~(-0.85,-2.80,1.15);
  target ~(-0.25,-2.05,0.55) -> (-0.15,-2.10,0.50); focal 30 -> 36, ease inout, slow push the whole shot (the "hold to read").
  Aim at the structure that sat behind the bumper (below/ahead of the frunk tub), NOT into the frunk (dark holes).
- Cropping (rule A): detail shot - the exposed front structure fills the frame. The open hood is either fully above frame or
  fully in; never a sliver. The turned bumper sits on the centreline from y -4.4 to -2.5: if the 30 % preview shows it
  occluding the structure, frame the right half (the car is symmetric) or give the bumper one more translate-out key in
  PARTS_V3 (forward/down, e.g. (0,-2.4,-0.25)) at local 0-0.6 s and start x_lock's bumper keys from that pose. Do not spin it again.
- Label "FRONT BUMPER REMOVED" from 18.423 (accent) to ~20.4. A second label (e.g. CRASH BEAM / MOUNTING POINTS) only after
  you have looked at the final render and can see that component; I can't name parts from the 30 % preview.

### 4b. R_hero (new render, 71 fr)
- Parts at x_side's end pose (fender/skirt out, rear bumper (0,0.95,0.05), diffuser (0,0.75,-0.35), hood open, front bumper
  BUMP_FAR rot 80). Louvre: home until local 2.32 (= 27.708), lifts straight up to (0,0.10,0.80) by local 3.48 (ease out), stays -
  that is x_lock's frame-1 pose, so the cut into x_lock is continuous. In PARTS_V3 the louvre keys are in v3 time; give this shot
  its own local keys (or a window) - do not change x_side's (home) or x_lock's (lifted from frame 1).
- Camera: start behind-right and above the pulled bumper (tail at y ~ +2.3), looking down ~40 deg into the exposed rear structure:
  ~(-1.20,4.60,2.00) target (-0.20,2.15,0.55), focal 30; push in to ~(-0.95,4.05,1.85) by local 2.32; then rise and creep forward
  over the bay as the louvre lifts: end ~(-0.70,3.70,2.80) target (0,1.75,0.75), focal 32. The pulled bumper/diffuser stay in the
  lower foreground (their inner faces are scanned, so seeing them from above is real data) and must not cross the structure.
- Cropping: detail - the rear structure, then the bay, fills the frame; the lifted louvre fully in frame at the end (it must
  not leave the top edge). Keep tail-lamp lenses small (holes). Check the plate area at full res.
- This replaces s6_engine (assembled car with rear bumper on = continuity break after x_side, and its 85 deg hinge is now
  invalid under rule D) and the candidate's x_engine/x_rear.

### 4c. x_lock framing fix (before it renders)
v3 30 % preview frames 1-25 clip the pulled rear bumper/diffuser at frame-left (rule A: accidental clip). Before the queue reaches
x_lock (it builds the spec from shots.py when it starts), widen the start: arc r 7.6 -> ~8.6 for the first keys (or focal 30 -> 27
at start, back to 30 by the lock), or move the arc centre ~0.3 m toward the tail. Every part, including the rear bumper and the
front bumper, inside the frame with margin on frame 1. Same check for x_side: the preview cuts the skirt at the bottom edge and the
rear bumper at the left edge - acceptable only if those parts leave frame by motion, not on a held frame; look at first/mid/last.

## 3. Music map

| t | grid k | event |
|---|---|---|
| 0.000 | - | s1_wide, whole car, moving |
| 5.077 | 8 (accent) | cut -> s3_wheel |
| 7.399 | 12 | cut -> f5_front (lamp) |
| 9.714 | ~16 (accent 9.719) | front bumper slides out (hood already open) |
| 12.04-14.36 | drop-out | bumper turns, camera pushes in on its inner face (quiet hold) |
| 16.103 | 27 | cut -> F_hero |
| 18.423 | 31 (accent) | FRONT BUMPER REMOVED label; camera settles close |
| 20.746 | 35 | cut -> x_side, fender off |
| 23.04-23.066 | 39 (lift) | rear bumper comes off |
| 25.388 | 43 | cut -> R_hero, REAR BUMPER REMOVED |
| 27.708 | 47 (accent) | louvre lifts off -> engine bay |
| 30.030 | 51 | cut -> x_lock (everything out) |
| 31.19 / 32.350 | 53 / 55 (heaviest bass) | parts fly home / LOCK |
| 33.0-33.5 | - | fade to black |
| ~34.1-38.5 | - | small logo; black to 39.0 (music fades 36.75 -> ~39) |

## 4. Diff vs v3 timeline and vs the editor's candidate

| scene | v3 | candidate | v4 | reason |
|---|---|---|---|---|
| s1_wide | 0-5.07 | same | same | whole car, rule A ok |
| s2_rear | 5.07-9.73 | dropped | **dropped** | rear 3/4 orbit = rotation that shows nothing the rear hero doesn't; would split the rear section (rule B) |
| s7_top | 9.73-12.03 | dropped | **dropped** | rotating top-down, no data of its own |
| s3_wheel | 12.03-14.37 | 5.07-7.40 | 5.07-7.40 | front wheel next to the front |
| f5_front | 14.37-23.07 | 7.40-16.10 | 7.40-16.10 | moved, frames unchanged; bumper slide lands on 9.719 |
| F_hero | - | - | **NEW 16.10-20.75** | rule C front hero (Front Fully Removed) |
| s6_engine | 23.07-25.40 | dropped | **dropped** | assembled car after the side explode; hinge invalid (rule D) |
| x_side | 25.40-30.03 | 16.10-20.73 | **20.75-25.39** | moved so the rear bumper comes off on the 23.066 lift |
| x_engine | - | NEW 20.73-23.07 | **not made** | merged into R_hero (engine bay is part of the rear sequence; "louvre already open" is not in the data) |
| x_top | - | NEW 23.07-27.71 | **not made** | top-down of the exploded car repeats x_lock's subject (whole exploded car) and costs the 8 beats the heroes need; it also sat between two rear shots (rear -> whole -> rear ping-pong) |
| x_rear | - | NEW 27.71-30.03 | **not made** | its subject (rear bumper inner face) is the rear bumper a third time; rule C wants the structure BEHIND the bumper, which R_hero shows with the bumper's inner face in the foreground |
| R_hero | - | - | **NEW 25.39-30.03** | rule C rear hero + louvre lift-off + engine bay |
| x_lock | 30.03-34.67 | 30.03-33.51 | 30.03-33.51 | trimmed after 1.16 s post-lock hold; framing fix 4c |
| logo | 34.67-39.0 | ~34.1-38.5 small | same as candidate | small logo after a fade (Temerario) |

### Reuse / render list (15 fps)
- REUSE as-is: s1_wide (77 fr), s3_wheel (36 fr, uses 35), logo png.
- RENDERING (keep): f5_front 132 fr (unchanged).
- QUEUED, adjust spec before they start (no extra frames): x_side 71 fr (no change needed beyond the crop check),
  x_lock 71 fr (**camera widened at the start, 4c**; if F_hero adds a bumper translate-out key, x_lock's bumper keys start from it).
- NEW: F_hero 71 fr + R_hero 71 fr = **142 frames** (~50 min at ~20 s/frame), each in <= 40-frame fresh processes, luma-scan every
  frame afterwards. Preview each at 30 % first and Read first/mid/last frames (rule A) before the final.
- Retired: s2_rear, s7_top, s6_engine (plus all v1/v2 retirees). Keep the folders.

### Checks before assembly (rule A, per shot)
First / middle / last frame sheet for s1_wide, s3_wheel, f5_front, F_hero, x_side, R_hero, x_lock: whole car fully in frame on
s1_wide and x_lock frame 1; named section fills the frame on the details; no part clipped on a held frame. s3_wheel's first
frames crop the wheel's left third and the fender top - judged deliberate (extreme close-up, wheel fills frame); trim in by
~0.2 s only if it reads as an accident on the sheet.

## 5. Open questions for the editor
1. x_lock/x_side start rendering when f5_front finishes (v3.sh builds the spec from shots.py at that moment): get the 4c framing
   change into shots.py before then, or kill/re-run that part of the queue.
2. Labels: what is the label style in Remotion for scan shots (ScanHUD `label`?) - the reel had "no text" so far. Wording only from
   scan names (FRONT BUMPER REMOVED, REAR BUMPER REMOVED, ENGINE BAY); any component name only after looking at the final frame.
3. Does the F_hero preview show the turned front bumper blocking the structure? If yes, use the extra translate-out key (4a).
4. Is the current logo_card the small (~35 % width) version? If not, re-render it small with the fade from black.
