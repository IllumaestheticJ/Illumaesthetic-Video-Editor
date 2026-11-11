# Subaru WRX VB v2: shot plan (director)

This plan keeps the scene order from `direction.md`. Inputs were `knowledge/lessons.md`, the style guide, the Temerario
notes, the coordinator's relayed user rules (v2 notes 1-8 and A-D), `project.yaml`, `editlog.jsonl` and `review.md`. There
is no `feedback.jsonl` yet. The `ive director` report is `director_report.md`. It flagged:
- s1~s2 as a repeated view (IoU 0.83);
- 1.74 s of dead frames in s7;
- no `focus` on any clip;
- low coverage: s5 19-23 %, s7 13-16 %, s1/s2 22-25 %.

All of those shots are gone in v2. The renders I looked at are listed in direction.md.

Conventions:
- Scan frame: front = -Y, car's right = -X, Z up, metres.
- Cameras are written as `loc -> target, focal` (sensor 20.25 mm, 1080x1920).
- Part keys are offsets from home `(dx, dy, dz)` with rotation `(rx, ry, rz)` in degrees. Times are seconds from the
  shot start, in the `projects/subaru-wrx-vb/tools/shot.py` key format (the ease applies to the segment ending at the key).
- Renders: 15 fps, 75 % resolution, 12 spp, persistent data OFF.
- Every animated shot: per-frame luma scan before assembly.
- Previews first, at 30 % resolution: first / mid / last frame plus each event frame.

Framing targets come from projecting the car's bbox (and the parts' off poses) through each camera:
- Wide shots: the car is 80-86 % of the frame width with ≥ 6 % side margins, and nothing clipped.
- Detail shots: the named section fills the width.

The editor must confirm margins on the preview frames. My projection used a box model of the car.

## Part off poses (shared by every shot after a part comes off, and the start of the reassembly)

| part (blend) | off pose | rot | where it sits |
|---|---|---|---|
| front bumper + plate_xnp (`p_front_bumper_inside_parts_included`) | (0, -0.55, +2.00) | (0,0,0) | Above and in front of the nose, on black |
| lower garnish (`p_front_bumper_lower_garnish`) | (0, -0.45, +1.45) | (0,0,0) | Under the bumper, above the nose |
| front / door / rear flare | (-0.45, 0, +0.90) | (0,-8,0) | Above each right arch, tilted to the lens (as in v1 s7) |
| side skirt (`p_side_skirt_only`) | (-0.60, 0, -0.12) | (0,0,0) | Outboard and slightly down, on the black floor |
| rear bumper (`p_rear_bumper_updated`) | (0, +0.40, +1.70) | (0,0,0) | Above and behind the trunk, on black |

Parts not yet removed in a shot stay home (in place on base_xnp). Parts already removed sit at their off pose in every
later shot, even when they are out of frame, so nothing pops.

## Shot table

| section | shot id | start-end (s) | focus | camera | part action (reel time) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|
| whole car | **v2_opener** | 0.000-5.224 | Whole car, front-led (scoop, grille, right cladding) | t0 `(-1.10,-5.90,2.80) -> (0.40,-0.30,0.60)` f28 (front-right, 15° off the nose, about 19° down) to t5.224 `(-2.15,-5.89,2.40) -> (0.25,-0.50,0.60)` f28, ease in-out. Box projection: x 0.16-0.83 at the start, 0.12-0.90 at the end; height 0.36-0.75 | none | The only whole-car view before the ending. The move starts on frame 1. It is elevated and near-frontal, so the length stacks into the 9:16 height (v1 s1 was a clipped band) | NEW, 80 frames (5.224 s + slack) |
| front | **s4_scoop** | 5.224-8.707 | Hood scoop | v1 as rendered: high slide across the nose, `(-1.35,-3.25,1.55)` to `(0.85,-3.3,1.6)`, f38, 2 mm | none | The WRX signature detail, shown once, inside the front sequence | REUSE all 43 frames; `src_fps 11.94` (= 30·43/(104+4)), 0.80x |
| front | **v2_front_off** | 8.707-16.775 | Front bumper, then what is behind it | Keys (shot time): t0 `(-2.10,-5.30,1.20) -> (-0.10,-2.00,0.75)` f30 (low front-right 3/4, bumper fills the width). t2.484 `(-1.90,-4.90,1.10) -> (-0.10,-2.00,0.80)` (slow push on the intact bumper). t3.880 `(-1.90,-5.60,1.40) -> (-0.10,-2.95,1.35)` (pull back and tilt up with the bumper, so the 1.85 m bumper fits: about 3.2 m away, about 2.2 m horizontal span). t5.276 `(-1.70,-5.20,1.40) -> (-0.10,-2.95,1.40)` (ease in on the inner face). t8.068 `(-1.50,-4.10,0.90) -> (-0.10,-2.05,0.50)` **f28** (down and in on the exposed structure, about 1.8 m across, filling the width) | Bumper + plate (identical keys): still to 11.191. To `(0,-0.75,+0.25)` at 11.715 (ease out: forward, clear of the car). To `(0,-0.85,+0.95)` rot `(-160,0,0)` at 12.587 (rises and flips about the width axis, so the scanned inner face looks at the low camera). Drift to `(0,-0.85,+1.03)` same rot at 13.983. To off pose, rot 0, at 14.681 (rises out of frame top). Garnish: still to 12.587. To `(0,-0.60,-0.02)` at 13.285 (forward along the black floor, translate only). To `(0,-0.65,+0.60)` at 13.983. To off pose at 14.681 | The hero beat (richest region, on the drop). The part leaves into black (toward the lens, then up), never across the body. The inner face is shown because it is scanned (bumper "inside, parts included"). The camera then stays on the front and reads the scanned crash structure for 2 s with labels | NEW, 122 frames (8.068 s + slack) |
| side + wheel | **v2_side_off** | 16.775-22.360 | Right-side cladding (front, door, rear flare, skirt), opening on the front wheel | t0 `(-2.70,-0.30,1.45) -> (-0.95,-1.30,0.55)` f30 (looking forward and down onto the front-right wheel and arch, about 2 m away; brake through the spokes; a different view from v1 s3, which was low and from the side). t1.396 `(-3.00,-0.90,1.10) -> (-0.90,-0.60,0.70)`. t2.792 `(-3.20,0.40,1.10) -> (-0.90,0.40,0.65)`. t4.188 `(-3.00,1.60,1.05) -> (-0.90,1.25,0.60)` (rear arch). t5.585 `(-4.60,1.00,1.60) -> (-0.90,0.30,0.55)` (pull back to a rear-right side 3/4: all four parts out, sill exposed). Linear keys with in-out ease at the ends | Front flare: go 16.775 to `(-0.35,0,+0.10)` at 17.124 to off pose at 17.822. Door flare: go 18.171 to `(-0.35,0,0.10)` at 18.520 to off pose at 19.218. Rear flare: go 19.568 to `(-0.35,0,0.10)` at 19.917 to off pose at 20.615. Skirt: go 20.964 to off pose at 21.662 (ease out). All translate plus the 8° tilt; no spins (inner faces not confirmed scanned). Front parts at their off poses throughout | 4 parts, one per bar, each framed as it lifts. Travel runs front to rear. Parts go out, then up into black above the arches, not across the doors. The skirt drops onto the black floor. The wheel is shown here, once | NEW, 85 frames (5.585 s + slack) |
| rear | **v2_rear_off** | 22.360-27.944 | Rear bumper, then what is behind it | t0 `(-1.80,5.02,0.85) -> (-0.05,1.95,0.60)` f30 (low rear-right 3/4, about 30° off the tail; rear about 2.36 m span, filling the width). t1.396 `(-1.90,5.60,1.30) -> (-0.05,2.75,1.30)` (follow the bumper up, about 3.2 m away so it fits). t2.792 `(-1.70,5.30,1.35) -> (-0.05,2.75,1.35)`. t5.584 `(-1.30,4.20,0.75) -> (-0.10,2.15,0.45)` **f28** (down and in on the rear structure) | Rear bumper: still to 22.360. To `(0,+0.70,+0.20)` at 22.884 (ease out, back toward the lens, clear of the body). To `(0,+0.80,+0.90)` rot `(+160,0,0)` at 23.756 (flip: scanned inner ribs face the camera). Drift `+0.08 z` to 25.152. To off pose `(0,+0.40,+1.70)`, rot 0, at 25.850 (rises out of the frame top). Every other part at its off pose | Best-registered part (1.9 mm), with its scanned inside. The rear-removed fills are real (Rear Bumper Removed + Duckbill, 1.3-1.5 mm). Same grammar as the front, so the viewer reads the pattern | NEW, 85 frames (5.584 s + slack) |
| whole car | **v2_reassemble** | 27.944-32.132 | All parts home, then the clean car | t0 `(-1.79,6.32,3.40) -> (0.40,0.30,0.90)` f28 (high rear-right 3/4, 20° off the tail; projection with parts: x 0.08-0.94, y 0.26-0.77). Ease to t4.188 `(-2.75,5.61,2.60) -> (0.20,0.50,0.60)` f28 (assembled car x 0.07-0.92) | Rear bumper home 27.944 to 28.642. Rear flare 28.642 to 29.340; door flare 28.817 to 29.515; front flare 28.991 to 29.689; skirt 28.817 to 29.515. Garnish 29.689 to 30.387. Front bumper + plate 30.038 to **30.736 lock** (ease in). From the lock frame on, render **car4np** alone with the same camera (clean car, no composite seams). Fade to black 31.434 to 32.132 in the edit | Temerario ending: progressive return in reverse travel order, the front locking last on a kick, a short settle, then the fade. A different view from the opener (rear, high) | NEW, 64 frames: frames 1-43 with base_xnp + parts, frames 43-64 with car4np |
| - | **logo** | 32.132-35.432 | Logo | `projects/ferrari-296/tools/logo_card.py ... --secs 3.3 --width 380` | - | Small logo on black, rides the music fade | REUSE the tool, new card (seconds) |

Labels (ScanHUD `kind: "label"`; JetBrains-mono or Inter title, off-white; no numbers; outside the silhouette, at least
80 px from the edges, above the bottom 20 %; enter on a beat, leave before the cut; at most 2 on screen):

| shot | label | in to out (s) | position | condition |
|---|---|---|---|---|
| v2_front_off | `FRONT BUMPER REMOVED` | 14.681 to 16.425 | x 0.08, y 0.72, left (black floor under the structure) | always: the state is scanned |
| v2_front_off | `CRASH BEAM` | 15.379 to 16.425 | x 0.08, y 0.77, left | Only if a full-resolution still of base_xnp at the t8.068 pose shows the reinforcement clearly. If the bumper brackets read instead, use `MOUNTING POINTS`. If neither reads, show no second label |
| v2_rear_off | `REAR BUMPER REMOVED` | 25.850 to 27.595 | x 0.92, y 0.72, right | always: Rear Bumper Removed is scanned and registered |
| v2_rear_off | (verified name, e.g. `REAR BEAM`) | 26.548 to 27.595 | x 0.92, y 0.77, right | Only what the t5.584 still visibly shows. Otherwise none |

## Cut list (removed from v1)

- **s1_front34**: both ends of the car are clipped (projected x -0.36 to 1.25). It is a small band, a rotation, and on
  the wrong side for the travel. Replaced by v2_opener.
- **s2_rear34**: the same view as s1 (IoU 0.83, flagged). It is a rotation with no new information.
- **s3_wheel**: the bumper is ON (a state conflict after the front-off), and it would split the front sequence. The
  wheel is folded into the opening of v2_side_off.
- **s5_front**: the bumper slides across the body and out of frame, its inner face is never shown, and the car is small
  (19-23 %). Its end pose cannot continue into anything.
- **s6_top**: weakest data (glass and cowl holes), a rotating top-down, and it showed the bumper back on after s5.
- **s7_explode**: every part separates at once in one wide orbit (13-16 %), plus 1.74 s of dead frames.
- Old 860 px logo: replaced by the 380 px small logo.

## Hold list (holds > 0.75 s)

| when | shot | length | reason |
|---|---|---|---|
| 8.707-11.191 | front_off pre-roll | 2.48 s (slow push, not static) | Establishes the intact bumper, grille and garnish before they leave on the drop. Moving camera |
| 12.587-13.983 | front_off | 1.40 s | The flipped bumper's scanned inner face. Camera eases in; the garnish moves under it |
| 14.681-16.775 | front_off | 2.09 s (camera still pushing) | Read the scanned structure and the two labels (user: "hold long enough to read it") |
| 23.756-25.152 | rear_off | 1.40 s | Rear bumper inner ribs; camera eases |
| 25.850-27.944 | rear_off | 2.09 s (camera still pushing) | Rear structure plus labels |
| 30.736-32.132 | reassemble | 0.70 s settle + 0.70 s fade | Clean car locked; the camera keeps settling; the fade is the ending. Down from v1's 1.4 s dead hold |

## Render budget

| shot | frames @15 fps | at 20 s/frame |
|---|---|---|
| v2_front_off (render first: hero) | 122 | 40.7 min |
| v2_rear_off | 85 | 28.3 min |
| v2_side_off | 85 | 28.3 min |
| v2_reassemble (43 + 21 car4np) | 64 | 21.3 min |
| v2_opener | 80 | 26.7 min |
| **total** | **436** | **≈ 2 h 25 min** (at 18 s: 2 h 11; at 25 s: 3 h 02) |

- Previews (30 %, 6 spp, about 4-6 frames per shot) come before each final: about 10 min total.
- Reused unchanged: **s4_scoop** (43 frames, re-timed only).
- Every other v1 render is unused.
- If the first final measures above about 21 s per frame, tell the coordinator before starting the next one. The shots
  are ordered by importance; the opener is last and is the one most easily simplified (for example a 2-key move at
  10 spp).

Assembly notes:
- Cut frames (30 fps): 157, 261, 503, 671, 838 (or 839, see direction.md Q4), 964. End 1063.
- First clip one frame short, or use honda-s2000 `concat_assemble.py` with exact frames.
- Per-clip `src_fps = 30·N/(slot+4)`.
- Fade to black inside v2_reassemble from 31.434. Logo fades up on 32.132.
- Check every cut against the decoded audio (≤ ½ frame).
- Tag each clip's `focus` in project.yaml so `ive director` stops flagging them.
