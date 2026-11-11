# Nissan 400Z: director's shot plan v2 (stage 2, keeps the scene order from direction.md)

Inputs: lessons.md (incl. mazda-miata-nc "don't separate every part at once", "rotations are wasted"; ferrari-296 "hold
the section and show the part off"; gt3rs "move parts into clear background"; c5 "spin only for a useful backside";
honda-s2000 "last scenes held too long"), the Temerario reference notes, project.yaml/editlog/cues.json,
tools/shots.py, contact sheets in `/home/user/media/work/z400/check/dir_*.jpg`, and the `ive director` report on v1.
There is no feedback.jsonl yet. The parent's v2 brief is folded in.
v1 report findings this plan fixes: s1~s2~s8b are the same view (IoU 0.77-0.80), s8a has 1.3 s of dead frames, the logo
holds 3.3 s with nothing on screen, and no shot has a focus tag.

Scan frame (metres): nose at -Y (y -2.17), tail at +Y (2.23), car's right = -X, ground z = 0, height 1.32.
`arc()`/`slide()` are the helpers in tools/shots.py. All new shots: `seconds` as listed (frames = seconds*15 + 1),
1080x1920 at 75 %, 12 spp, 15 fps, **persistent data off**, and a per-frame mean-luma scan before assembly.
"Stack pose" = v1 explode offsets x1.06 = the pose s8b starts from. Every new shot ends its moving parts there, so the
reassembly cut is continuous:
hood (0,-0.053,1.537) rot(-8,0,0) · bumper_shell (0,-0.233,0.657) · p_grille (0,-0.318,1.081) · p_wing (0,0.265,1.219) rot(14,0,0) ·
p_mirror_r (-0.477,0,0.371) rot(0,0,-20) · p_mirror_l (0.477,0,0.371) rot(0,0,20). Use the same part pivots as v1 `PARTS`.

## Shot table

| section | shot | start-end (s) / frames | focus | camera | part action (edit time) | why it earns its seconds | source |
|---|---|---|---|---|---|---|---|
| whole | **N0_open** | 0.000-3.700 / 110 | the whole car, front 3/4 | `arc(3.8, r 7.8→7.2, az -24→-32, h 1.10→1.20, c0=(0,-0.10,0.55), focal 30, n=8, ease_out=False)`: slow push-in, the car fills 67→81 % of the width, whole car in frame on every frame; fade in 1.2 s | none | the opener shows the whole car with motion from frame 1 (s1 crops the nose from f30) | **NEW**: seconds 3.8 = 58 f, src_fps 15 |
| front | s4_lamp | 3.700-7.430 / 112 | headlight + grille slats | as rendered (front2, 2 mm slide toward centre) | none | sets up the grille/bumper that come off in N1; an extreme close-up at Temerario's slow pace in the quiet intro | reuse f1-46, src_fps **11.9** (0.79x) |
| front | s6_hood | 7.430-11.128 / 111 | hood → engine bay | as rendered (high front-right 3/4 easing in to r 3.4, az -20) | hood starts on the drop (7.55) and is fully open 9.56 (hinge, Hood Open data); bay held to 11.128 | first state reveal ON THE DROP; the bay is the richest captured state | reuse **f8-70** (drops the static lead), src_fps **16.4** |
| front | **N1_front_explode** | 11.128-16.666 / 166 | front assembly: hood off the hinge, grille, bumper shell inner face, front structure | key 0.0: loc (-1.163,-4.345,2.40) tgt (0,-1.15,0.65) f30 (= s6's last pose, so the cut reads as one held shot); key 2.8: loc (-1.55,-4.25,1.55) tgt (0,-1.70,0.58); key 5.6: loc (-1.35,-3.85,1.30) tgt (0,-1.75,0.58); smooth (sample ≥ 8 keys), inout | **hood** (v1 pivot): start in the hinge-open pose = rot(-40.37,0,0), loc = Rx(-40.37)(c−p)+p−c with p = hinge pivot (-0.065,-0.560,0.833), c = the hood's v1 pivot; hold to 0.10, lift to stack pose by **0.81 (11.935 kick)**, ease-out. **grille**: home to 0.81; out to (0,-0.42,0.45) by **1.85 (12.974)**, ease-out; drift to (0,-0.46,0.52) by 3.70; rise to stack 3.70→5.30 inout. **bumper_shell**: home to 1.85; to (0,-0.80,0.12) rot(±65,0,0) by **3.70 (14.826)**, ease-out, sign chosen so the inner face turns to the lens (only if the inside is scanned, else rot 0); drift to (0,-0.84,0.16) by 4.50 (15.627); rise to stack, rot 0, by 5.40 inout. Static: p_wing and both mirrors at home (0). Base comp_explode | the section explode the brief asks for: the camera stays on the front while three parts come off in turn, toward the lens into black, and pushes into the real "Bumper and hood removed" structure; the heavy kicks drive each part | **NEW**: seconds 5.6 = 85 f, src_fps 15 |
| side | s3_haunch | 16.666-19.319 / 80 | right shoulder line → mirror | as rendered (side2, glide forward, ends on the mirror) | none | moves the travel to the side; the shot already ends on the next subject | reuse f1-46, src_fps **16.4** (≈ native) |
| side | **N2_mirror** | 19.319-22.198 / 86 | right mirror off; scanned door mount | key 0.0: loc (-1.28,1.55,1.50) tgt (-0.75,-0.30,0.85) f35 (= s3's last pose); key 2.933: loc (-2.05,0.35,1.40) tgt (-0.85,-0.45,0.95) f35, inout | **p_mirror_r**: home to 0.25; to stack pose by **1.04 (20.358 kick)**, ease-out (outboard and up, into black beside the car, toward the lens); then still. **p_mirror_l**: same keys mirrored (off-screen, keeps the state). Static: front parts at stack pose, p_wing home. Base comp_explode | the side has one state, so one short focused move: the part, then the Side Mirrors Removed mount it came off | **NEW**: seconds 2.933 = 45 f, src_fps 15 |
| rear | s5_tail | 22.198-24.044 / 55 | tail-lamp bar + badge | as rendered (rear2 slide, ends car-right) | none | rear detail before the rear part comes off | reuse f1-46, src_fps **23.4** |
| rear | **N3_wing** | 24.044-26.703 / 80 | duck-tail spoiler off; scanned deck mounts | key 0.0: loc (-0.60,3.60,1.00) tgt (-0.25,2.15,0.85) f38 (= s5's last pose); key 2.733: loc (-1.10,4.15,2.25) tgt (0,1.80,1.05) f35, inout (rise + pull back) | **p_wing**: home to 0.20; to stack pose by **1.86 (25.902 kick)**, ease-out (straight up and slightly back into black above the deck; the 14 deg tilt turns its top toward the rising lens; no flip); then still. Static: front parts + mirrors at stack pose. Base comp_explode | the rear has one part; the camera rises with it and lands on the Rear Wing Removed deck | **NEW**: seconds 2.733 = 42 f, src_fps 15 |
| whole | s8b_explode | 26.703-33.286 / 198 | all panels home → closed car | as rendered (high rear-left 3/4) | panels fly home and LOCK on **30.395** (loudest kick, render f≈56); car rests; `fade=t=out:st=4.725:d=1.858` → black at 33.286 | the only all-parts moment is the reassembly, from an angle no other shot uses; it starts exactly in the stack pose N1-N3 leave | reuse **f1-101**, src_fps **15** (keeps the lock on 30.395) |
| end | logo | 33.286-38.400 / 153 | ILLUMAESTHETIC | 0.8 s black, logo fades in on **34.087** (0.90 kick), holds, fades with the track tail from 36.97 | none | Temerario ending: small logo on black | re-make card: `projects/ferrari-296/tools/logo_card.py --width 340` (~31 % width, was 540 = 50 %), 5.1 s with a 0.8 s black lead (no Blender) |

Total: 110+112+111+166+80+86+55+80+198+153 = **1152 frames = 38.4 s**. Cuts on frames 111, 223, 334, 500, 580, 666, 721, 801, 999.

## Cut list (removed from v1)
- **s1_front34**: crops the nose from ~f30, so it is not a whole-car opener. Replaced by N0.
- **s2_rear34**: a whole-car orbit that repeats the opener's view (IoU 0.77) and causes front→rear→front ping-pong. The rear is told by s5 + N3.
- **s7_top**: shows the closed whole car again with no top-specific data. A rising overhead adds nothing new, and a closed car cannot sit mid-explode.
- **s8a_explode**: every part separates at once in one wide orbit (user rule); 1.3 s dead; f30-51 black. Replaced by N1/N2/N3.
- **s6_hood f1-7**: static lead before the hinge moves.
- **s8b_explode f102-112**: car at rest after the fade; not needed.
- **logo**: the 50 %-width card with 3.3 s of stillness becomes a smaller card on black (the hold stays because the music tail runs to 38.4).
- **queued `s8a_fix` render** (22 f, waits on `RENDERS_DONE` in /tmp/claude-0/render2.log): no longer used. Cancel it before it starts.

## Hold list (> 0.75 s)
| hold | span (s) | reason |
|---|---|---|
| s6 engine bay open | 9.56-11.128 (1.57) | the camera keeps easing in; Hood Open is the richest captured state and needs time to read; N1 continues from the same pose |
| N1 grille drift | 12.97-14.83 (1.85) | the grille hangs in black while the bumper comes off under it; this is not a static frame (drift + camera descent) |
| N1 bumper inner face | 14.83-15.63 (0.80) | shows the bumper's scanned inside/mounting tabs (only if they exist, see open question 1) |
| N2 mirror out | 20.36-22.20 (1.84) | the camera moves on to the scanned door mount, so the subject changes from part to mount |
| N3 wing up | 25.90-26.70 (0.80) | the camera finishes rising to show the deck mounts |
| s8b after lock | 30.395-33.286 (2.89) | 1.03 s of rest, then a 1.86 s fade (Temerario "assembled car, fades to black"); the camera is still moving |
| logo | 34.087-38.40 (4.3) | the music tail; the logo is small on black |

## Render budget (one Blender job at a time, after s8b finishes)
| shot | seconds | frames | est. time @ 15-25 s/f |
|---|---|---|---|
| N1_front_explode | 5.6 | 85 | 21-35 min |
| N2_mirror | 2.933 | 45 | 11-19 min |
| N3_wing | 2.733 | 42 | 11-18 min |
| N0_open | 3.8 | 58 | 15-24 min |
| **total** | | **230** | **~58-96 min** (≤ 250 budget) |
Render order: N1 → N2 → N3 → N0. First render 3-frame previews (`frames: first/mid/last`, 30 %) of N1 and N3 to set
the bumper tip sign and check that the parts clear the lens and the frame. If CPU runs short, a fallback opener is
s1_front34 f1-25 at src_fps 6.8: the whole car is in frame, but the motion is very slow. Prefer N0.
Reused unchanged: s4_lamp, s6_hood, s3_haunch, s5_tail, s8b_explode (only trim/src_fps). Unused: s1, s2, s7, s8a.

## Checks for the editor after rendering
- Per-frame mean luma on N0-N3 and on the finished s8b (lighting dropout).
- Frames ±2 around 11.128, 19.319 and 24.044. These are base swaps at an identical pose (2 mm crop → 3 mm composite).
  If the swap reads as a glitch, start the new shot's camera ~5 % closer so it reads as a cut.
- Frame 801 vs N3's last frame: front parts, mirrors and wing must be in the same stack pose on both sides of the cut.
- Cut timing against the decoded audio (lesson), and frame diffs at every cut (no 3-frame freezes: src_fps above follows `30*N/(slot+4)`).
- Before keeping any tip/flip: one still of bumper_shell, p_mirror_r and p_wing from behind. A hollow back means translate only.
