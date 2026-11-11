# Nissan 400Z: director's shot plan v2 (stage 2, keeps the scene order from direction.md)

Inputs:
- lessons.md, especially:
  - mazda-miata-nc: don't separate every part at once; rotations are wasted.
  - ferrari-296: hold the section and show the part off.
  - gt3rs: move parts into clear background.
  - c5: spin only for a useful backside.
  - honda-s2000: last scenes held too long.
- The Temerario notes, project.yaml, editlog, cues.json, tools/shots.py.
- The contact sheets `/home/user/media/work/z400/check/dir_*.jpg`.
- The `ive director` report on v1, which flagged:
  - s1~s2~s8b are the same view (IoU 0.77-0.80);
  - s8a has 1.3 s of dead frames;
  - the logo holds 3.3 s with nothing on screen;
  - no shot has a focus tag.
- The parent's v2 brief and addendum (A-D). There is no feedback.jsonl yet.

Scan frame (metres): nose at -Y (y -2.17), tail at +Y (2.23), car's right = -X, ground z = 0, height 1.32.
All new shots:
- 1080x1920 at 75 %, 12 spp, 15 fps;
- **persistent data off**;
- a per-frame mean-luma scan before assembly;
- a 3-frame preview (first/mid/last, 30 %) before the final, checked against the framing rule (whole car fully in for
  wides; the named section fills the frame for details; nothing clipped by accident).

Rendered seconds follow `N = (slot+4)/2` frames, so `src_fps = 30*N/(slot+4) = 15`.

**Stack pose** = v1 explode offsets x1.06, which is s8b's first frame. N2 and N3 leave their parts in it, and the
front parts are placed there (off-frame) in N2/N3:
- hood (0,-0.053,1.537) rot(-8,0,0)
- bumper_shell (0,-0.233,0.657)
- p_grille (0,-0.318,1.081)
- p_wing (0,0.265,1.219) rot(14,0,0)
- p_mirror_r (-0.477,0,0.371) rot(0,0,-20)
- p_mirror_l (0.477,0,0.371) rot(0,0,20)

Use the v1 `PARTS` pivots.

## Prep (light jobs, run before the renders, one at a time)
1. **comp_hoodopen**: comp_hood + the Hood Open scan's own captured open-hood triangles (the faces above the car's top
   surface inside the open-hood bbox). The composite.py "drop z above the car" step is skipped for this one box. This
   is what H shows open: real data, no hinge animation.
2. **Bumper and hood removed at ≤2 mm**: decimate the raw Drive file (5.0M tris) to 2 mm or use it as-is, then
   `ive prep --like car.json`.
3. **comp_front2_bhr**: front2 (2 mm) minus the bumper/hood zone + step 2, built the same way as comp_explode.
   Close-ups need ≤2 mm (style guide), and the 3 mm state scan is too soft at 1.2 m.

## Shot table

| section | shot | start-end (s) / frames | focus | camera | part action (edit time) | why it earns its seconds | source |
|---|---|---|---|---|---|---|---|
| whole | **N0_open** | 0.000-3.700 / 111 (dur one frame short) | the whole car | `arc(3.8, r 7.8→7.2, az -24→-32, h 1.10→1.20, c0=(0,-0.10,0.55), focal 30, n=8, ease_out=False)`: the car fills 67 % → 81 % of the width, never touches an edge; fade in 1.2 s | none | whole car with motion from frame 1 (s1 clips the nose from ~f25) | **NEW**: 3.8 s = 58 f |
| front | **H_hoodopen** | 3.700-7.430 / 112 | engine bay under the captured open hood | loc (-1.00,-4.05,2.35) tgt (0,-1.00,0.75) f30 → loc (-0.60,-3.35,2.00) tgt (0,-0.95,0.70) f30, inout: push down into the bay; the captured hood flaps are a deliberate partial crop at the top; the bay fills the middle | none (static state scan) | the real Hood Open state, no animated closed hood (addendum D); the engine bay's only appearance | **NEW**: 3.8 s = 58 f; base comp_hoodopen |
| front | **N1a_bumper_off** (HERO, drop) | 7.430-11.128 / 111 | grille, then bumper shell, leave the nose | loc (-2.25,-4.70,1.30) tgt (-0.10,-1.70,0.55) f30 (nose to A-pillar + front-right wheel, with margins) → loc (-1.25,-3.55,0.80) tgt (-0.10,-1.95,0.50) f30, inout | **grille**: home to 0.70; out to (0,-0.45,0.35) by **1.30** (≈ 8.243 kick + motion), ease-out (forward out of the bumper opening, toward the lens into black); drift to (0,-0.48,0.40) by 1.80; rise to (0,-0.40,2.0) by 2.40, ease-in (exits the frame top). **bumper_shell**: home to 1.80 (**9.282 kick** ≈ 1.85); to (0,-0.85,0.15) rot(±60,0,0) by 2.60, ease-out (the sign turns the inner face to the lens; **rot 0 if the inside is not scanned**); drift to (0,-0.88,0.18) by 3.10; rise to (0,-0.60,1.8) by 3.75, ease-in (exits the top). Static: p_wing and mirrors at home; hood not loaded (already off). Base comp_explode | the hero beat on the biggest musical moment: each front part comes off in turn, toward the lens and out into black, while the camera moves in on what was behind it. Grille first is backed by the Bumper Grille Removed scan | **NEW**: 3.8 s = 58 f |
| front | **N1b_structure** (HERO hold) | 11.128-16.666 / 166 | the structure behind the bumper: beam with bolt holes, headlamps from behind, wiring/hoses at the right lamp, lower lip | loc (-1.05,-3.30,0.80) tgt (-0.50,-2.00,0.45) f35 → loc (0.20,-3.40,0.85) tgt (0.05,-2.00,0.45) f35, linear-ish (inout, gentle): a 1.3 m lateral slide from the right lamp to the beam centre. Frame top stays below the ragged radiator-support top; black below the lower lip carries the labels | none (no parts: they are off and out of frame) | holds long enough to read the hero data; the slide reveals new structure every second | **NEW**: 5.6 s = 85 f; base comp_front2_bhr |
| side | **N2_mirror** | 16.666-19.319 / 80 | right mirror off, then the door mount | loc (-1.75,0.95,1.40) tgt (-0.90,-0.30,1.00) f40 (mirror upper third, door shoulder below, margins) → loc (-2.30,0.45,1.45) tgt (-1.10,-0.35,1.05) f35, inout | **p_mirror_r**: home to 0.25; to stack pose by **1.00** (17.666), ease-out (outboard/up into black toward the lens; ±20 deg yaw only); then still while the camera settles on the scanned mount (**18.512 kick**). **p_mirror_l**: mirrored keys (off-screen). Front parts at stack pose, p_wing home. Base comp_explode | one-part section: part off, then the Side Mirrors Removed mount it came off; short | **NEW**: 2.733 s = 42 f |
| rear | s5_tail | 19.319-22.198 / 86 | badge + tail-lamp bar centre | as rendered | none | rear detail before the rear part; borderline exhaust-tip clipping noted in direction.md §2 | reuse f1-46, src_fps **15.33** (native) |
| rear | **N3_wing** | 22.198-26.703 / 135 | duck-tail off, then the deck mounts | loc (-0.60,3.60,1.00) tgt (-0.25,2.15,0.85) f38 (= s5's last pose) → loc (-1.10,4.15,2.25) tgt (0,1.80,1.05) f35, inout (rise + pull back over the deck) | **p_wing**: home to 0.30; to stack pose by **1.846 (24.044 kick)**, ease-out (straight up/back into black; 14 deg tilt, no flip); then still while the camera rises to frame the wing above the Rear Wing Removed deck. Mirrors + front parts at stack pose. Base comp_explode | rear section: the part, then the scanned mounts; the wing ends in the pose s8b starts from | **NEW**: 4.6 s = 70 f |
| whole | s8b_explode | 26.703-33.286 / 198 | all panels home → closed car | as rendered, **scaled to 78 % and centred on black** (`scale=iw*0.78:-2,pad=1080:1920:(ow-iw)/2:(oh-ih)/2`), because from ~f65 the nose and tail touch the edges | panels LOCK on **30.395** (f≈56); rest; `fade=t=out:st=4.725:d=1.858` → black at 33.286 | the one all-parts moment is the reassembly (allowed), from an angle used nowhere else | reuse **f1-101**, src_fps **15** |
| end | logo | 33.286-38.400 / 153 | ILLUMAESTHETIC | 0.8 s black; logo fades in on **34.087**; it fades with the track tail from 36.97 | none | small Temerario logo | re-make: `projects/ferrari-296/tools/logo_card.py --width 340` (~31 % width; was 540) with a 0.8 s black lead, 5.1 s |

Cut frames: 111, 223, 334, 500, 580, 666, 801, 999; end 1152 = 38.4 s. The first clip is one frame short (house rule).

## Labels (N1b only; addendum C)
Remotion `ScanHUD`, label items only (no counters, no numbers). Style:
- Inter Display, tracking +6, `#e8ecf2`, cap height ~40 px.
- Left-aligned at x = 80 px, baseline y ≈ 1300 px: over the black below the lower lip, outside the silhouette, above
  the bottom-20 % caption zone.
- 6-frame fade/slide in on the kick; out 6 frames before the stated end.

| label | in (kick) | out | backed by |
|---|---|---|---|
| FRONT BUMPER REMOVED | 11.935 (0.99) | 14.700 | scan files "Bumper Only" / "Bumper and hood removed" |
| CRASH BEAM + MOUNTING POINTS | 14.826 (0.64) | 16.450 (before the 16.666 cut) | the beam and its bolt holes are visible in the frame. Read the final N1b frames: if the holes don't read, use "MOUNTING POINTS" |
Never more than one label at a time.

## Cut list (removed from v1)
| v1 | reason |
|---|---|
| s1_front34 | not a whole-car opener (nose clipped from ~f25) |
| s2_rear34 | repeats a whole-car wide (IoU 0.77); ping-pong |
| s3_haunch | framing: right third dead black, subject unclear, seam slivers, mirror on the edge |
| s4_lamp | lamp and grille clipped by the edges; redundant with the bumper hero |
| s6_hood | animates the closed hood scan open (addendum D) |
| s7_top | the closed whole car again; no top data |
| s8a_explode | all parts at once in a wide orbit; dead 1.3 s; f30-51 black |
| s8b f102-112 | after the fade; also edge-clipped |
| logo 50 % width, 3.3 s still | smaller card on black |
| queued `s8a_fix` (22 f) | no longer used; cancel before it starts |

## Hold list (> 0.75 s)
| hold | span (s) | reason |
|---|---|---|
| H on the open bay | 3.70-7.43 (3.73) | a static state scan, but the camera pushes in for the whole slot. The quiet intro gives time to read the real open bay |
| N1b structure slide | 11.128-16.666 (5.54) | the hero data: read the beam, mounts, lamps and wiring; the camera slides the whole time; carries the labels |
| N2 mount | 17.67-19.32 (1.65) | the camera moves from the part to the scanned mount, so the subject changes |
| N3 deck | 24.04-26.70 (2.66) | the camera rises from the wing to the deck mounts; a new subject |
| s8b after lock | 30.395-33.286 (2.89) | 1.03 s rest, then a 1.86 s fade (Temerario "assembled, fade"); the camera is still moving |
| logo | 34.087-38.40 (4.3) | music tail; small logo on black |

## Render budget (one Blender job at a time, after s8b finishes)
| order | shot | seconds | frames | est. @ 15-25 s/f |
|---|---|---|---|---|
| 1 | N1a_bumper_off | 3.8 | 58 | 15-24 min |
| 2 | N1b_structure | 5.6 | 85 | 21-35 min |
| 3 | H_hoodopen | 3.8 | 58 | 15-24 min |
| 4 | N0_open | 3.8 | 58 | 15-24 min |
| 5 | N3_wing | 4.6 | 70 | 18-29 min |
| 6 | N2_mirror | 2.733 | 42 | 11-18 min |
| | **Plan A total** | | **371** | **~93-155 min** |

**Plan B, ~271 frames (≈ the 250 aim).** N0, H and N1b have no moving parts, so render them at 7.5 fps and let
minterpolate do x4:
- N0: 29 f
- H: 29 f
- N1b: 43 f

This saves 100 frames. First test it: render 10 frames of N1b at 7.5 fps, interpolate, and check the scan grain for
warping/shimmer at 100 %. If it shimmers, use plan A.

Reused unchanged: s5_tail and s8b_explode (only trim, src_fps, scale and fade).
The parent/user should pick A or B; the hero shots (N1a, N1b) are first in either case.

## Checks for the editor after rendering
- Per-frame mean luma on every new shot and on the finished s8b (lighting dropout).
- First/mid/last frame of every shot against the framing rule (addendum A), and frames ±2 around every cut.
- 22.198: base swap from rear2 (2 mm) to comp_explode (3 mm) at the identical pose. If it reads as a glitch, start N3
  5 % closer.
- One still from behind of each of bumper_shell, p_mirror_r and p_wing before keeping any tip. Hollow means translate only.
- Cut timing against the decoded audio and frame diffs at every cut (src_fps above follows `30*N/(slot+4)`).
- Final frames of N1b at full res, to choose the label 2 wording.
