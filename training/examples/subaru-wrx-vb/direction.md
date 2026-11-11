# Subaru WRX VB (2022+) scan reel v2: scene direction

Scene director pass, 2026-11-11. Inputs read: `CLAUDE.md`, `knowledge/lessons.md` (all of it), `knowledge/style-guide.md`,
`knowledge/workflow.md` ("Scene direction"), `training/references/README.md` (Temerario), and this project's `clips.md`,
`project.yaml`, `timing.json`, `editlog.jsonl`, `review.md` and `tools/shots.py`. There is no `feedback.jsonl` yet. I looked at
these contact sheets: `final_q1.jpg`, `final_s5.jpg`, `final_s7.jpg`, `s5big.jpg`, `s7big.jpg`, plus full-resolution crops of
s5 f64 and s7 f41/f76 (the front and rear with the bumpers off). I also ran `python -m ive director` (its report is
`director_report.md`).

The v2 brief changed during this pass (coordinator notes relayed from the user). These rules are binding:
- Travel goes front, then side, then rear, with no ping-pong.
- Each section appears in ONE continuous sequence.
- When a part comes off, the camera stays on that section, moves in, and shows the part's inner face. Never separate
  every part at once in one wide orbit.
- No wasted rotations or repeated views, and no shot is used twice.
- The opener shows the WHOLE car, framed to fill 9:16 with deliberate margins and nothing clipped.
- Spin or flip a part only when its backside is scanned. A part that comes off moves into clear background.
- The bumper-removed data is the hero beat, with short factual labels (text is now allowed, but only names of what the
  scan visibly shows).
- No faked openings: the trunk stays shut.
- End with reassembly, a fade, and a SMALL logo.
- Render budget is under about 2.5 h at about 20 s per frame.

## Step 1: feature inventory

All entries are verified against `clips.md` and `editlog.jsonl` (regcheck: % of points within 10 mm of the car, and the
median distance). Scan frame: front = -Y, car's right = -X, Z up, metres. Front axle y -1.36, rear axle y +1.31.
Car size: 4.663 x 1.889 x 1.458 m.

| region | signature features (seen in renders) | registered states (fills) | registered parts | weak data | richness |
|---|---|---|---|---|---|
| **Front** | Hood scoop (WRX signature), hex grille, headlights, lower garnish/intakes | Front Removed (all), Front Bumper Parts Removed, Bumpers Removed (1.5-2.2 mm). These are dense scans of the structure behind the bumper; s5 f64 shows the horizontal members, the radiator/condenser face and the lamp backs | Front Bumper (inside, parts included: outer + inner + grille) 62 % / 3.9 mm; front plate (blank, flattened); Lower Garnish 74 % / 3.6 mm | Scoop mouth and wiper cowl are ragged black holes (s4, v1 s6). Headlight lenses are dark and ragged. Bumper inner edges are ragged in flight | **Richest**: 2 parts + 3 state fills + signature scoop |
| **Right side** | Black wheel-arch cladding (the VB's most distinctive styling), side skirt | Side Skirt Off Doors Open (4.3 mm): the sill under the skirt | Front Flare, Door Flare, Rear Flare (83-92 %, 2.5-3.3 mm); Side Skirt Only (41 %, 2.2 mm). **Right side only** | Glass is not captured (dark windows) | High: 4 parts + 1 fill |
| **Wheels** | Rims with spokes plus brake discs and calipers, scanned (v1 s3, 2 mm) | none | none (wheels stay on) | The far wheel shows under the car in close-ups | Medium (detail only) |
| **Rear** | Rear bumper with diffuser shape and exhaust openings | Rear Bumper Removed, Duckbill Scan (1.3-1.5 mm): the structure under the rear bumper (s7 f41/f76: brackets and corner structure, lamp box) | VB Rear Bumper (Updated) 84 % / **1.9 mm** (best fit of any part); its inner face is scanned (ribs visible from behind in s7 f41) | Rear plate flattened. Trunk-open family **rejected** (hinge fit 10.8 mm, holes in the tub capture) | Medium: 1 part + 2 fills |
| **Top** | Roofline, scoop from above | none | none | Glass holes and cowl holes read as black from above (v1 s6) | **Weakest** |
| Engine bay / interior / doors / hood / trunk | - | no hood-open state; door states are fragments only; trunk rejected | none | - | **None** (no rung) |

Not usable: the headlight-project scans (`hl_*`) and VB Bumper Inside (own frame, 0 % on the car). Front Bumper Inside
(Parts removed) and Rear Bumper Only are superseded by the versions used above. Front Grille is already part of the
bumper part.

The base for every part shot is `prep/base_xnp.blend`. It is the car minus the front bumper, garnish, rear bumper, right
flares and right skirt, filled from the removed-state scans. Parts reseat exactly where they were cut (`chk/xb.jpg`).
`car4np.blend` is the clean, plate-flattened full car.

## Step 2: scene order (from the inventory)

- **Opener.** The front carries the strongest features (scoop, grille) and the richest data. So the first wide shot is a
  near-frontal, elevated **front-right** 3/4 of the whole car. It is on the right side because the cladding parts exist
  only there, so the reel's travel continues down that side.
- **Biggest musical moment.** The front is the richest region, so the front bumper comes off ON the drop (11.191 s).
  The camera stays on the front until the crash structure has been read.
- **Travel.** Front (whole car, then scoop, then bumper and structure), then the right side (wheel and arch close, then
  flares and skirt, front to rear), then the rear (bumper off and the structure behind it), then a wide reassembly from
  the rear 3/4. Fade, then a small logo. Each section is shown once.
- **Leave-outs.** Top-down is cut: weakest data and a rotation. Trunk, hood and doors: no registered state. Left side:
  no left-side parts.

| # | scene | section | scans used | feature shown | why here (inventory) | beats | camera note |
|---|---|---|---|---|---|---|---|
| 1 | **Opener** (NEW) | whole car (front-led) | car4np | Whole car: scoop, grille, right cladding | Front = richest + signature region. The opener must show the whole car, unclipped, with motion from frame 1 | 0-5.224 (ambient, to swell 1) | Elevated near-frontal front-right 3/4, focal 28, slow 9° drift plus descent. Car fills about 80 % of the width |
| 2 | **Hood scoop** (reuse s4) | front | front2np (2 mm) | Hood scoop, top of the grille, headlights | The VB's signature detail, next to the front wide | 5.224-8.707 (swell 1 to swell 2) | v1 s4 high slide across the nose, played at 0.80x |
| 3 | **Front bumper off** (NEW, hero) | front | base_xnp + bumper/plate + garnish (+ other parts home) | Intact bumper, then bumper off and flipped to show its scanned inside, then garnish off, then the crash structure behind with labels | Richest region gets the drop. The bumper part includes its inner face. Three dense state fills under it | 8.707-16.775 (pre-roll, then drop at 11.191, then 4 bars) | Low front-right 3/4 on the nose. The camera follows the bumper up, then pushes in on the exposed structure |
| 4 | **Wheel + cladding off** (NEW) | right side + wheel | base_xnp + 3 flares + skirt (front parts at their off poses) | Front-right wheel/brake and arch, then front, door and rear flares lift one per bar, then the skirt slides out to show the sill | 4 right-side parts plus the sill fill. The scanned wheel is merged here so the arch is shown once | 16.775-22.360 (4 bars) | Tracks rearward along the right side, framed on each part as it lifts |
| 5 | **Rear bumper off** (NEW) | rear | base_xnp + rear bumper (others at their off poses) | Rear bumper off and flipped (inner ribs scanned), then the structure behind it with labels | Best-fit part (1.9 mm) plus two rear fills. A one-part region gets a shorter, tight scene | 22.360-27.944 (4 bars) | Low rear-right 3/4, then push in on the structure |
| 6 | **Reassembly + fade** (NEW) | whole car | base_xnp + all parts, then car4np on the lock | Parts return rear to side to front. The clean car locks home, then fade | Temerario ending: reassembly, fade, small logo. Swap to the clean car on the lock (lesson from the C5 reel) | 27.944-32.132 (3 bars; lock 30.736) | High rear-right 3/4, whole car plus the floating parts in frame, settling closer |
| 7 | Logo | - | logo card | Small ILLUMAESTHETIC | Brief | 32.132-35.432 | Logo about 380 px wide (about 35 %) |

## Music map (corrected broadband grid)

Downbeats are `11.1910 + 1.39609 n`, beat 0.349 s, from `/home/user/media/work/music/broadband_grid.json`. The intro has
no transients. v1 cut on the two soft swells and measured them at 5.224 and 8.707. Frame numbers are at 30 fps.

| t (s) | frame | grid | measured kick | event |
|---|---|---|---|---|
| 0.000 | 0 | - | - | Opener (motion from frame 1) |
| 5.224 | 157 | swell 1 | - | cut: hood scoop |
| 8.707 | 261 | swell 2 | - | cut: front bumper pre-roll (bumper still on) |
| 11.191 | 336 | n0 DROP | 11.193 | bumper leaves (in-shot, no cut) |
| 12.587 | 378 | n1 | 12.598 | bumper flipped, inner face held; garnish goes |
| 13.983 | 419 | n2 | 13.982 | both parts exit upward; camera turns to the structure |
| 14.681 / 15.379 | 440 / 461 | beat / n3 | 15.376 | label "FRONT BUMPER REMOVED" / second label |
| 16.775 | 503 | n4 | 16.772 | cut: right side; front flare lifts |
| 18.171 / 19.568 / 20.964 | 545 / 587 / 629 | n5 / n6 / n7 | 18.181 / 19.562 / 20.957 | door flare / rear flare / skirt |
| 22.360 | 671 | n8 | 22.352 | cut: rear; rear bumper leaves |
| 23.756 | 713 | n9 | 23.746 | rear bumper inner face held |
| 25.152 | 755 | n10 | 25.146 | rear bumper exits; push in on the rear structure |
| 25.850 / 26.548 | 776 / 796 | beat / n11 | 26.540 | rear labels |
| 27.944 | 838 | n12 | **27.976 (+32 ms)** | cut: reassembly (check against the decoded audio; it may need frame 839) |
| 30.736 | 922 | n14 | 30.749 | front bumper locks home; swap to the clean car |
| 31.434-32.132 | 943-964 | - | - | fade to black |
| 32.132 | 964 | n15 | 32.125 | small logo, rides the music fade |
| 35.432 | 1063 | - | - | end |

## Diff against v1

| v1 shot | v2 | why |
|---|---|---|
| s1_front34 (left front 3/4 turntable) | **dropped**: replaced by the new opener | Projected bbox: x -0.36 to 0.97 at the start and -0.37 to 1.25 at the end, so both ends of the car are clipped. The car is a small band (cover 22-24 %). It is on the left side, away from the right-side travel |
| s2_rear34 | **dropped** | Flagged by `ive director` as a repeat of s1 (IoU 0.83). It is a rotation that adds no new data. The rear is now covered by scene 5 |
| s3_wheel | **dropped**: the wheel is merged into scene 4 | Rendered with the bumper ON; after the front-off it would contradict the state. Before the front it would split the front sequence. The wheel and arch are shown once, in the side sequence |
| s4_scoop | **reused**, moved to 5.224-8.707, played at 0.80x | Right content. The signature detail sits next to the front wide |
| s5_front | **dropped**: replaced by scene 3 | The bumper slides ACROSS the body to the car's left and leaves the frame. Its inner face is never shown. The car is small (cover 19-23 %). The bumper ends on the ground at the left, which no later shot can continue from |
| s6_top | **dropped** | Top is the weakest data (glass and cowl holes). It is a rotating top-down and it showed the bumper back ON after s5 (a state error) |
| s7_explode | **dropped**: replaced by scenes 3-6 | Every part separates at once in one wide orbit (cover 13-16 %), plus 1.7 s of dead frames. This breaks the binding rule directly |
| logo (860 px) | shrink to about 380 px | "Small logo" (Temerario about 25-35 % of the width) |

Reused as-is: **s4_scoop** only. New renders: opener, front_off, side_off, rear_off, reassemble. The frame budget is in
`director.md` (436 frames, about 2 h 25 min at 20 s per frame).

## Open questions for the editor (don't guess)

1. **Labels must name only what the scan shows.** "FRONT BUMPER REMOVED" and "REAR BUMPER REMOVED" are safe: the states
   are scanned and registered. The second labels ("CRASH BEAM" at the front; "REAR BEAM" or "EXHAUST" at the rear) go
   on screen only after a full-resolution still of base_xnp at the final push-in pose shows that member clearly. s5 f64
   shows a long horizontal member behind the bumper, but at 75 % resolution I cannot swear it is the reinforcement
   rather than the radiator support. "MOUNTING POINTS" goes on only if the bumper brackets read in that still.
   Otherwise use one label.
2. base_xnp is about 4 mm-class (4.04 M faces). The style guide asks for ≤ 2 mm on close-ups. v1 s5 looked acceptable at
   this distance; a 2 mm front or rear crop of the composite is not in the budget.
3. The music starts at 0 with an 11 s ambient intro, per the caller's fixed 35.5 s plan. Lessons (C5, FG2) prefer
   starting a kick-less intro later. That needs the user's OK because it changes the length.
4. The cut at 27.944: the kick measured 27.976 (+32 ms, about 1 frame). Measure on the decoded audio and use frame 839
   if that is closer.
5. Flare inner faces: if a preview shows scanned mounting clips, tilt them toward the lens. Otherwise translate only.
   They are translate-only in this plan.
