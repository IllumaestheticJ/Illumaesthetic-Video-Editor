# Porsche 911 GT3 (992): scene direction v1 -> v2

Written by the scene-director agent on 2026-11-11, following `.claude/agents/scene-director.md` and then
`.claude/agents/director.md`. It includes the v2 brief for all reels and the user's addendum A-D (sent by the
coordinator). Where the user's newest notes conflict with older rules, the newest notes win: travel
front -> side -> rear, the opener shows the whole car, section explodes replace the one wide explode, and short
factual labels are allowed (addendum C overrides "no text").

Sources I looked at: chk/reg_sheet.jpg, state_sheet.jpg, alone_sheet.jpg, states2.png, trunkstate.png,
hoodstate.png, cx_*.png, chk/final/all16.jpg, s7.jpg, and the final PNG key frames. I also made my own numpy
orthographic splats (no Blender) of comp_x.stl (front and rear), Front_Hood_Open, Rear_End_No_Diffuser and
rear_wing_mounting_reference, saved in the session scratchpad. I also read `ive director` (director_report.md).

## 1. Feature inventory

All scans come from one Artec session (2023-11-23) and one levelled frame. Registration figures are from clips.md
and the regcheck renders.

| Region | Signature features (seen in the scans) | Real states (registered) | Registered parts | Weak data | Richness |
|---|---|---|---|---|---|
| **Rear** | Swan-neck wing with its uprights, ducktail engine lid with louvres, PORSCHE/GT3 lettering, twin centre tailpipes, diffuser fins | **rear_wing_mounting_reference = rear with the bumper skin off** (wing on; the splat shows a horizontal member behind the bumper line, two round silencer-type cans, mounting points; 1.16 mm). **Rear_End_No_Diffuser** (diffuser off: twin tailpipes, silencers, exhaust pipes, rear suspension links, 1.42 mm). Rear_End_Trunk_Open_Lights_Out (1.17 mm) | Rear Wing 1.10, Rear Bumper 1.99, Rear Diffuser 1.13, Rear Lip 1.89, rear duckbill 1.42 | The engine-lid-open state has many holes, so **do not open or remove the duckbill**. comp_x straight from behind has a large black hole in the centre behind the bumper line, so frame the rear from **rear 3/4 (right or left)**, never dead-centre. Rear Cover M is not registered. Plate recess is blank (no legible plate). | **Highest**: 4 movable parts + a real bumper-off state + a diffuser-off state + the signature wing |
| **Front** | Front lid with NACA ducts, round headlights, GT3 front bumper | **Front_Hood_Open** (frunk tub, 1.32 mm). The captured lid is only a ragged sliver plus the gas strut at the windscreen end. It cannot be shown as a raised lid. | Front Bumper (4.98 mm / 0.5 deg, the weakest), hood lid = full car minus the open state (tools/lid.py) | **No front-bumper-removed state exists.** With the bumper off, comp_x shows only the frunk tub's front wall, partial radiator fins at the left corner and a **black hole at the right corner**. So the front bumper stays on. Frunk floor hole (hidden from the high front-left angle) | Medium: 1 real state |
| **Wheels** | Cross-drilled brake disc, caliper, coil spring (FR) | **FR wheel well** (wheel off, 1.36 mm, 1.5 mm render) | none | The full-car wheels have fragments in the spokes. The top and front edges of the wheel-well scan are ragged (v1 s3 still shows them; the re-render is tighter) | Small: 1 state, 1 close-up |
| **Side (right)** | Sill line, mirror, door | **SideSkirt_Removed** (1.43 mm). The upper boundary is ragged, but the sill is clean | SideSkirt (2.27 mm median; ICP slides 24 mm along the sill) | Left/Right side bumper trims are not registered (113-281 mm off), so never animate them | Small: 1 part + 1 state |
| **Top** | Roof, lid ducts, wing plan view | none | none | none | Low: no data beyond the full car |
| Interior / engine bay | none | engine bay only via the trunk-open state (holes) | none | holes | Not shown |

**Hood decision (addendum D):** the open state is real and registered, but it holds the frunk, not the lid. Keep
v1's method: the lid cut from the closed car (full car minus the open state) hinged -62 deg about its rear edge over
the real frunk scan. That is not a faked opening, because the frunk under the lid is the real open-state capture.
Showing the raw open state would show a car with no lid. Open question 2 asks for a check of the end angle.

**No trunk, engine lid or front-bumper-removal shot.** There is no usable data for any of them.

## 2. Scene order (front -> side -> rear, each section in ONE continuous sequence)

Reasons for the order:
- **Opener:** user rule 4 (whole car, motion from frame 1) and rule 1 (travel front -> side -> rear). So the reel
  opens whole on the front-left 3/4 and the front sequence follows without a cut (one render).
- **Rear explode on the drop:** the rear is the richest region (4 parts, a real bumper-off state, a diffuser-off
  state, the signature wing), so it gets the drop and all three flux accents. The travel puts the rear last, which
  matches the music.
- The camera keeps moving one way round the car: front-left -> nose -> front-right wheel -> right sill ->
  rear (right 3/4 -> low right -> left 3/4) -> rises to top-down. There is no return to an earlier section.

| # | Section | Shot | Music (s) | Frames @30 | Scans / blend | Focus (one) | Why here (inventory) | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | FRONT | **N1_front** | 0.000-8.022 | 240 (one frame short) | comp_hood + hood_lid1 | whole car -> front lid opens -> frunk | The opener must show the whole car (rule 4). The front's real state is the frunk. It is one shot so the front appears once (B). | **NEW** |
| 2 | WHEEL | s3_wheel | 8.022-9.956 | 58 | frww15 (FR wheel-off state, 1.5 mm) | FR brake disc + caliper + spring | Front-right wheel: the travel continues past the nose to the right. This is the only wheel data. | REUSE (the tighter re-render in progress) |
| 3 | SIDE | **N2_side** | 9.956-11.894 | 58 | comp_side + x_skirt | right side skirt comes off, sill underneath | 1 part + 1 state = short scene (4 beats) | **NEW** |
| 4 | REAR | s4_wing | 11.894-13.830 | 58 | rear_2mm | wing uprights + ducktail + PORSCHE lettering, assembled | The rear arrives on the signature detail before it comes apart | REUSE all 30 frames |
| 5 | REAR | **N3_rear_off** | 13.830-19.739 | 177 | comp_rear + x_wing, x_rbumper, x_diffuser, x_rlip | rear comes apart: wing lifts (13.83), then **bumper, diffuser, lip on the DROP 15.552** | Richest region on the biggest moment; progressive (wing first, then the bumper group) | **NEW** |
| 6 | REAR | **N4_exhaust** | 19.739-23.621 | 117 | same scene, parts held out | what is behind the bumper: tailpipes, silencers, exhaust pipes, rear structure | Hero beat C: move in on the real bumper-off / diffuser-off data and hold to read it | **NEW** |
| 7 | REAR | **N5_rear_home** | 23.621-27.503 | 116 | same scene | parts fly home (lock 26.72 on a kick), pull back to the whole car, ending on s6's first camera | Reassembly (rule 7) seen from the rear-left, continuing the travel | **NEW** |
| 8 | TOP | s6_top | 27.503-30.906 | 102 | car4 | rises from rear-left 3/4 to straight top-down; **fade to black 29.935-30.906** | Top-down from the brief as the closing whole-car pass. N5 ends on s6's frame-1 camera, so the cut on 27.503 is invisible. | REUSE all 64 frames |
| 9 | - | logo | 30.906-33.000 | 63 | logo_card | small ILLUMAESTHETIC logo | Rule 7: fade, then a SMALL logo | re-make card: `--width 300` (about 28 % of the frame), 0.3 s fade-in |

Cut frames: 240/241, 299, 357, 415, 592, 709, 825, 927, end 990. Beats in project.yaml become
`[8.0333, 9.9667, 11.9, 13.8333, 19.7333, 23.6333, 27.5, 30.9]`, and the drop 15.5667 falls inside N3.
Seconds per section: front 8.0, wheel 1.9, side 1.9, **rear 15.6**, top 3.4 (including the fade), logo 2.1.

### Tags for project.yaml (`section:` / `focus:`)
N1 front / "front lid + frunk"; s3 wheel / "FR brake"; N2 side / "side skirt + sill"; s4 rear / "wing mounts + lettering";
N3 rear / "rear parts separating"; N4 rear / "exhaust behind the bumper"; N5 rear / "rear reassembly"; s6 top / "whole car top-down".

## 3. New renders: exact specs

Scan frame (prep, metres): front = -Y, car's right = -X, ground Z = 0, car centred. Bumpers sit at about y = ±2.28,
the front axle at y ≈ -1.35, the rear axle at y ≈ +1.1, the wing top at about z 1.25 (y ≈ 1.95), the tailpipes at
about y 2.2, z 0.35. Every render is 15 fps, 1080x1920 at 75 %, 12 spp, with **persistent data OFF** (lessons).
Each one gets 3 extra tail frames. Key the cameras with `shots.arc`-style dense keys so the camera does not cut a
chord through the car. All times below are **seconds within the shot**.

**Composite bases to build first** (numpy, `tools/composite.py`, then `ive prep --like car4.json`):
- `comp_side` = car4 minus the SideSkirt region + fill **SideSkirt_Removed** only. comp_x would show the missing
  bumpers in frame.
- `comp_rear` = car4 minus x_wing, x_rbumper, x_diffuser, x_rlip + fills **rear_wing_mounting_reference**
  (bumper off) and **Rear_End_No_Diffuser**. **Not** Trunk_Open, and the duckbill stays on the car. Check for black
  holes at the wing-upright feet on the lid. Look at a silver preview from the N4 camera before the final render.

**N1_front**: 8.033 s, 124 frames. Base comp_hood. Part hood_lid1, pivot (0, -0.87, 0.86).
- Lid rot X 0 until 4.151, then -62 deg by 6.093 (ease in-out, 4 beats, starting on the 4.151 accent).
- Camera:
  - t0: loc (4.4, -6.0, 1.5), target (0, -0.2, 0.55), f30. This shows the whole car front-left 3/4 with margins
    (about 75 % of the width). Check that the wing tip at the right edge has at least 5 % margin.
  - Arc toward the nose and in by t 6.09: loc (1.2, -4.2, 2.2), target (0, -1.25, 0.6).
  - Slow push to t 8.03: loc (0.9, -3.7, 2.15), target (0, -1.3, 0.55), f30.
  - The camera moves from frame 1. It stays high front-left (about 20 deg) so the frunk-floor hole stays hidden.
    The front section fills the frame at the end.

**N2_side**: 1.933 s, 33 frames. Base comp_side. Part x_skirt translates out (-0.45, 0, -0.06): toward the camera
into clear background, no spin (the inner face is unverified). Timing: 0.10 -> 0.95 s, ease-out, then hold.
- Camera, low on the right, sliding rearward:
  - start: loc (-3.0, -0.5, 0.45), target (-0.85, 0.0, 0.30), f35
  - end: loc (-2.6, 0.3, 0.42), target (-0.85, 0.15, 0.28)
- Keep the ragged upper edge of the state scan out of the top of the frame. Lower the target if it shows.

**N3_rear_off**: 5.909 s, 92 frames. Base comp_rear. Shot t = music - 13.830; the drop is at t = 1.722.
Translate only (no spins; nothing here has a verified inner face worth turning):
- x_wing: (0, +0.15, +0.90), t 0.10 -> 1.55, ease-out. The swan-neck uprights read against black above the deck.
- x_rbumper: (0, +0.70, +0.75), back and UP so it later clears N4's view. Timing t 1.72 -> 2.80.
- x_diffuser: (0, +0.90, -0.35), t 1.80 -> 2.90.
- x_rlip: (0, +1.15, -0.45), t 1.86 -> 3.00.
- All ease-out. After that, linear drift to 1.03 x the offset by the shot's end.
- Camera, rear-right 3/4, pulling back as the parts come toward it:
  - start: loc (-2.2, 5.6, 1.45), target (0, 1.7, 0.75), f35
  - end: loc (-2.9, 6.6, 1.25), target (-0.1, 2.3, 0.65), f30
- The rear section fills the frame, and every part stays inside the frame and off the lens. The parts move
  toward the camera into black, never across the body.

**N4_exhaust**: 3.882 s, 62 frames. Same base and parts, held at N3's end pose with continued drift
(1.03 -> 1.05 x offset).
- Camera, low rear-right, pushing in:
  - start: loc (-1.25, 4.0, 0.55), target (0.05, 2.05, 0.42), f35
  - end: loc (-0.75, 3.55, 0.50), target (0.05, 2.00, 0.42)
- The tailpipes, silencers and pipes fill the frame (about 1.3 m wide). The bumper is above the frame, and the
  diffuser and lip are below it, outside the 54 deg vertical FOV. Check the preview, and if a part enters the frame
  push its offset further, not the camera.
- Avoid the dead-centre view (black hole behind the bumper line).

**N5_rear_home**: 3.882 s, 61 frames. Same scene. Shot t = music - 23.621.
- Parts go from their drift pose to home with ease-in, one group after another:
  - diffuser + lip: t 0.23 -> 1.38
  - bumper: t 0.68 -> 2.13
  - wing: t 1.68 -> 3.10, the **lock at music 26.72** (a kick, 23 beats after the drop)
- Camera, rear-left (the travel continues right -> centre -> left):
  - start: loc (1.4, 4.2, 1.9), target (0, 1.9, 0.8), f30
  - end (ease in-out), **exactly s6_top's first camera**: loc (2.3, 4.4, 3.6), target (0, 0.3, 0.5), f30. The
    whole car is in frame by about t 3.0.

Render budget: 124 + 33 + 92 + 62 + 61 = **372 new frames**, one Blender at a time. Scan every folder's per-frame
mean luma before assembly. Reused unchanged: s3 (its re-render), s4, s6.

**Assembly src_fps** = (N-1)/(dur + 0.1):
- s3: 29/2.033 ≈ 14.3 (if it stays at 27 frames: 12.8)
- s4: 29/2.033 ≈ 14.3
- s6: 63/3.50 ≈ 18.0 (a 1.2x faster rise is fine)
- The new shots are rendered at their slot length, so they play at 15.

## 4. On-screen labels (addendum C; overlay rendered by the coordinator)

The wording is plain and factual, and every label names only what the scan visibly shows. White, small caps,
upper-middle of the frame, above the bottom 20 %. There are no numbers. There is no label on the reassembly, the
top-down or the logo.

| Text | Shot | In | Out | Visible in the scan |
|---|---|---|---|---|
| FRUNK | N1 | 6.30 | 7.85 | the Front_Hood_Open tub under the raised lid |
| FRONT BRAKE | s3 | 8.25 | 9.80 | the disc, caliper and spring of the FR wheel-off state |
| SIDE SKIRT REMOVED | N2 | 10.45 | 11.80 | the skirt part out, the sill from SideSkirt_Removed |
| SWAN-NECK WING | N3 | 14.10 | 15.45 | the wing with its uprights lifting clear |
| REAR BUMPER REMOVED | N3 | 16.20 | 19.55 | bumper, diffuser and lip out; the bumper-off state behind |
| EXHAUST | N4 | 20.30 | 23.35 | twin tailpipes, silencers and pipes (Rear_End_No_Diffuser + bumper-off state) |

I did **not** use "CRASH BEAM" or "MOUNTING POINTS". The bumper-off state shows a horizontal member and mounting
holes, but I could not confirm what it is from my splats. Add a label only after the editor's silver close render
of N4 shows it clearly (open question 1).

## 5. Diff against v1 (cut list)

| v1 shot | v2 | Why |
|---|---|---|
| s1_front34 | **dropped** | The car is cropped at frame right (A). `ive director`: same view as s2 and s6 (B). It is a turntable that adds nothing (Mazda rule). N1 replaces it as the uncropped opener. |
| s2_rear34 | **dropped** | Cropped (A); same view as s5. The rear is now one continuous sequence (s4, N3-N5). |
| s3_wheel | kept (8.022-9.956) | The only wheel data. The tighter re-render fixes the ragged edge. **Check that the empty bottom third is gone**; if it is not, lower the target 6 cm. |
| s4_wing | kept, moved to 11.894-13.830 | The rear's signature detail on the assembled car, before it comes apart |
| s5_hood | **replaced by N1** | The wing is clipped at frame right from frame 1 (A). `ive director`: s5~s7 and s2~s5. The same hinge/lid data, merged with the opener so the front is one shot. |
| s6_top | kept, moved to the end (27.503-30.906) with a fade | Top-down from the brief. It now follows the reassembly on an invisible cut. Flag s1~s6 is resolved because s1 is gone. |
| s7_explode | **dropped** | All 8 parts in one wide orbit (rule 2). It lifted the duckbill over the weak trunk-open data and pulled the front bumper over a hole. `ive director`: 1.5 s of dead frames. Replaced by section explodes N2 (side) and N3-N5 (rear). The front gets the real lid opening instead of a bumper pull. |
| logo 2.1 s, 620 px | 2.1 s, about 300 px, after a 1 s fade | Rule 7: small logo after the fade |

## 6. Hold list (> 0.75 s with no new subject)

- N1 6.09-8.02 (1.9 s): the lid is open and the camera keeps pushing in on the frunk. That is the front's only
  state, and the FRUNK label needs reading time.
- N4 whole shot (3.9 s): the hero hold on the data behind the bumper. The camera pushes in throughout.
- N5 26.72-27.50 (0.78 s): the locked car while the camera settles onto s6's start. This makes the reassembly read.
- Fade 29.94-30.91 and logo 30.91-33.0 (the music's tail).

## 7. Open questions for the editor (don't guess)

1. **rear_wing_mounting_reference** is the rear with the bumper skin off. My numpy splat shows the wing on, no
   bumper skin, a horizontal member and two round cans. Confirm with a silver Blender render before N3. If it is not
   a bumper-off capture, N4 must frame only the Rear_End_No_Diffuser exhaust, and the REAR BUMPER REMOVED label
   becomes DIFFUSER REMOVED.
2. Hood end angle: v1 used -62 deg. Compare it with the gas strut and lid sliver captured in Front_Hood_Open, and
   match the end angle to the strut if they differ.
3. Rear bumper inner face: if a back-side preview shows a clean scanned inside, N4 could tip the bumper 90 deg about
   X to show its mounting side. The default is translate only (spin lesson).
4. s3 re-render: confirm it is 30 frames and that the lower third is filled.
