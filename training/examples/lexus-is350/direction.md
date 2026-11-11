# Lexus IS350 2026 facelift: scene direction (V2)

**Scene director, 2026-11-11.** This plan includes the V2 brief (8 points) and the newer feedback A-D. Where they disagree, A-D wins: there are labels on scan shots now.

What I looked at before deciding:
- Contact sheets of the final renders: s1, s2, s3, s4, s5, and s6 frames 1-16.
- Previews of s7_explode and s8_hero at 30 %.
- chk/inside/inside_sheet.jpg and the per-part inside stills.
- Full-resolution crops of s2 (its edges), s5 f46 (the bay) and s7 preview f105 (the structure after the bumper comes off).

There is no feedback.jsonl yet. `ive director` fails because s7 has no final folder.

## 1. Feature inventory (facelift scans only)

The scans cover a front clip: bumper back to the A-pillar base, nothing above 1.02 m.

| Scan / region | What the renders show | Data quality | Registered | Role |
|---|---|---|---|---|
| Front End Hood Closed (base) | New spindle mesh. **Badge on a horizontal bar** (the facelift signature). Headlamps, corner and fog intakes, fenders, front wheels | Crisp at 2 mm. **Hood top speckled** (s3, s4, s6). Far lower bumper corner is ragged in every 3/4 view. Wheel centres are hollow. A-pillar stub at the rear cut edge. Dealer frame "SWICKARD" is readable up close | base | All exterior shots |
| Hood Open (state) + hinge.json | Hood propped at 60 deg. Struts and underside captured (s5 f28-46) | Good | 0.94 mm, hinge 2.4 mm | **State: the hood opens (allowed, D)** |
| Bumper and Hood Removed (state, "BHR") | Seen in s5 f46: upper radiator support bar across the bay, airbox/intake tube, battery and fuse box (right), headlamp housing tops. Seen in s7 pv f105: lower structure behind the bumper, but at 30 % it is too soft to name individual parts | Good on top. Behind the radiator is unscanned | 1.84 mm | **State: front bumper removed.** Fill under the hood and the bumper |
| Bumper shell (Duct and Fogs Removed) | Bumper + grille. **Inner face (inside_sheet): mounting tabs along the top and bottom edges, grille back, a centre mount with a box on it.** Back sheet on 92 % of the scan | Good | 3.29 mm (ICP) | Part: the bumper |
| Top bracket | Long bracket with tabs (inside_sheet) | Good | 6.28 mm (identity) | Part |
| Radar unit + bracket | Small box with a mounting face (inside_sheet) | OK, small (14 cm) | identity, behind the grille | Part |
| Fog covers L/R, ducting L/R | Back sheet on 99-100 % of the scan (my nearest-normal measurement). The editor's inside stills missed them (bad framing), so **nothing has visually confirmed them yet** | Good (numbers) | 2.40 / 2.80 mm | Part (no label until a still confirms them) |
| Wheelwells | Ragged liners, half missing (chk/fe) | **Weak** | ~1.7 mm | Not used |
| Side / rear / top / cabin | Nothing behind the A-pillar. The top view is all speckled hood | **None / weak** | n/a | No side, rear, trunk or door scenes (D). No top-down |

Richness, highest first:

| Rank | Region | What it has |
|---|---|---|
| 1 | **Bumper removed / bumper assembly** | Removal state + 6 registered parts with inner faces. **Hero (C)** |
| 2 | Hood / engine bay | One real state + fitted hinge |
| 3 | Fascia | The signature, 2 mm detail |
| 4 | Flank | Weak |
| 5 | Top | Weak |

Inner faces (rule 5): the camera moves **behind** the floated bumper to see them. **No part spins or flips. Every part only translates.**

## 2. Scene order and section map

Travel order:
1. Whole clip.
2. Fascia, left to right.
3. Up into the hood/engine bay.
4. The bumper comes off on the drop, and the camera goes IN on what was behind it.
5. Behind the bumper to its inner face.
6. Reassembly.
7. Fade, then a small logo.

### Section table (B: each section appears in one continuous sequence, no duplicates)

| Shot | Section covered | Continuous sequence |
|---|---|---|
| s2_front34L | Whole front clip (only the closed exterior wide) | 1 |
| s3_grille | Front-left corner (grille corner + fog intake) | 2 Fascia |
| s8_badge | Fascia centre (badge bar + centre mesh) | 2 Fascia |
| s4_lamp | Front-right corner (headlamp + corner intake) | 2 Fascia |
| s5_hood (from frame 7) | Hood opening | 3 Hood / engine bay |
| s5b_bay | Engine bay under the open hood | 3 Hood / engine bay |
| X1_bumper_off | Bumper pulled off (the transition into the structure) | 4 Bumper removed |
| X1b_structure | Structure behind the bumper (BHR, lower front, below the radiator support bar) | 4 Bumper removed |
| X2_inner | Bumper inner face + its parts (ducts, fogs, radar, top bracket) | 4 Bumper removed |
| X3_reassembly | Bumper parts returning (the end of the bumper sequence) | 4 Bumper removed |
| logo | — | — |

Notes:
- **Dropped as duplicates:**
  - s1 repeats s2's subject, mirrored, and crops the near fender.
  - s6_top repeats the hood section, closed again, all speckle.
  - s8_hero is a third whole-face view with the plate dead centre.
- **Trimmed:** s5's first 6 frames (closed hood, whole clip). They repeat s2.
- **Framing in sequence 4:**
  - X1b stays below the radiator support bar so it does not repeat the bay.
  - The hood stays open and is **not** closed again, so the hood section is not repeated.

### Scene list

| # | Scene | Scans | Focus | Why here | Slot (s) | Beats | Framing / camera (prepped metres: nose -Y, car's left +X) |
|---|---|---|---|---|---|---|---|
| 1 | **s2_front34L: RE-RENDER (framing only)** | CLIP | Whole front clip | Opener: whole clip, moving from frame 1 (brief 4, A). The current render puts the rear edge on the right frame edge in **every** frame (car x 84-809 of 810 px). It is cut off, so scaling down cannot fix it | 0.000-4.064 | 8 | Same move (+52 to +36 deg, h 1.15 to 1.0). r 3.3/3.15 becomes **3.85/3.65**. Centre y -1.75 becomes **-1.65**. Target: the clip spans ~80 % of the width, with ≥ 8 % black each side, and the A-pillar stub inside the frame. The subject sits about 1/8 above the frame's vertical centre |
| 2 | s3_grille (reuse) | CLIP2 | Left grille corner + fog intake | Starts the fascia sequence next to the opener's side | 4.064-5.564 | 3 | As rendered. The section fills the frame (detail) |
| 3 | **s8_badge: NEW** (replaces the queued s8_hero) | CLIP2 | Badge bar + centre mesh (the facelift signature) | Centre of the fascia | 5.564-8.064 | 5 | Nose-on push-in. Camera moves from (0.25,-3.30,0.78) to (0.12,-3.00,0.76). Target (0,-2.34,0.66). Focal 55, ease out. Badge bar in the upper third. **Plate frame below the bottom edge. Hood speckle above the top edge** (check a preview still) |
| 4 | s4_lamp (reuse) | CLIP2 | Right headlamp + corner intake | Ends the fascia sweep. Cut on the 8.064 phrase peak | 8.064-9.564 | 3 | As rendered |
| 5 | s5_hood (reuse, **in-point frame 7**) | fl_comp_hood + HOOD | Hood opens on the fitted hinge to the captured pose | Real state (D). The camera picks up on the right side | 9.564-12.564 | 6 | As rendered, frames 7-46 (40 frames = 2.67 s) at 0.89x to fill 3.0 s. The hood moves from the first frame |
| 6 | **s5b_bay: NEW** | fl_comp_hood + HOOD (open) | Engine bay: radiator support bar, intake, battery/fuse box, hood underside | Stays on the section and moves in (brief 2). Holds through the 2-beat break | 12.564-16.063 | 7 | Starts on s5's last pose: (-0.96,-5.01,2.15), target (0,-1.65,0.55). Pushes to (-0.45,-3.20,1.75), target (0,-1.45,0.75). Focal 30 to 35, ease in-out. Hood underside across the top. Stay off the unscanned gap behind the radiator |
| 7 | **X1_bumper_off: NEW** | fl_comp_explode + HOOD (open, static) + bumper group G | Whole bumper pulls straight off **on the DROP** | Hero section starts on the biggest musical moment (C). The bumper came off as one piece ("Bumper Removed" scan) | 16.063-18.063 | 4 | Front-left close 3/4: centre (0,-2.30,0.45), angle +30, r 2.8, h 0.6, focal 32. The bumper fills ~85 % of the width. G slides forward then **up out of the top of the frame** into black. The camera starts creeping in |
| 8 | **X1b_structure: NEW** | same | What was behind the bumper: lower structure, mounts, lamp housings (BHR) | C: "move IN and hold long enough to read detail". Longest hold in the reel | 18.063-22.063 | 8 | Slow push. Camera (0.90,-3.60,0.55) to (0.55,-3.15,0.50). Target (0.05,-2.10,0.42). Focal 35. Frame from just below the radiator support bar down to the lowest structure (the open hood stays out of the top). The structure fills the frame, with no dead black where the bumper was |
| 9 | **X2_inner: NEW** | same | Bumper inner face. Starts on the left corner (duct L pulls toward the camera, fog L out the front), tracks to the centre (radar pulls toward the camera, top bracket lifts) | Section close-ups of the bumper's own parts. All really removed and scanned | 22.063-26.063 | 8 | Behind the floated bumper, the car below and behind the camera. Camera (0.95,-2.15,1.85) to (0.20,-2.20,1.80). Target (0.65,-3.30,1.35) to (0,-3.30,1.35). Focal 40. Inner face on black |
| 10 | **X3_reassembly: NEW** | same | Bumper parts return to the shell, then the bumper drops back onto the car | Ends the bumper sequence. Only whole-clip view in the "hood open" state, from a new angle | 26.063-30.063 | 8 (fade over the last beat) | Front-left high 3/4: centre (0,-2.10,0.60), angle +25 to +15, r 3.6 to 3.9, h 1.7 to 1.6, focal 30. Whole clip + open hood inside the frame with ≥ 6 % margins. Lock at 28.563, hold with a slight pull-back, **fade to black 29.563-30.063** |
| 11 | logo | logo card | **Small** logo (~35 % width) | Brief 7 | 30.063-33.600 | ~7 | Fades in 30.06-30.56, fades out with the track |

### Explode master animation

One part timeline. X1, X1b, X2 and X3 each render a window of it.
- **T = 0 at the drop (16.063).** Each shot shifts the keys by its own -t0.
- **G** (the bumper group) = fl_shell, x_fog_L/R, x_duct_L/R, x_bracket, x_radar.
- **No rotations.**
- **The hood is held at rot (open_deg,0,0) about the hinge.json pivot for the whole explode.** It continues from s5/s5b and never closes. The lock frame is therefore fl_comp_explode + parts + open hood. Do not swap the base to the closed CLIP.

| T (s) | abs (s) | Part action |
|---|---|---|
| 0.0-0.8 | 16.06-16.86 | G to (0,-0.60,+0.05), ease-out: pulled straight forward off the car |
| 0.8-2.0 | 16.86-18.06 | G to (0,-1.30,+1.00), ease in-out: up and forward, out of X1's top edge |
| 2.0-6.0 | 18.06-22.06 | G drifts to (0,-1.35,+1.02), linear. Off screen during X1b |
| 6.5-7.5 | 22.56-23.56 | duct L/R to (±0.12,-1.00,1.02): toward the X2 camera. fog L/R to (±0.18,-1.60,1.02): out the front. Ease-out |
| 8.0-9.0 | 24.06-25.06 | radar to (0,-0.95,1.02): toward the camera. bracket to (0,-1.35,1.30): up. Ease-out |
| 10.0-11.0 | 26.06-27.06 | ducts, fogs, radar and bracket back to the G pose, ease in-out |
| 11.0-12.5 | 27.06-28.56 | G home to (0,0,0): down and back, ease-in |
| 12.5 | **28.563** | lock (kick). Hold 1 s, then fade |

## 3. Labels (C)

On-screen labels apply to scan shots only, at most two items at once. Each one:
- enters on a kick and leaves ≥ 0.25 s before the cut;
- uses plain factual wording;
- names only what the renders above show.

| Shot | Label | In | Out | Evidence |
|---|---|---|---|---|
| s5b_bay | ENGINE BAY | 12.564 | 15.064 | s5 f46: bay contents captured (radiator support, intake, battery box) |
| X1b_structure | FRONT BUMPER REMOVED | 18.563 | 21.563 | Registered "Bumper and Hood Removed" state + removed-bumper scans |
| X1b_structure | CRASH BEAM **(conditional)** | 19.563 | 21.563 | Named in clips.md for BHR, but **not readable in any existing render** (s7 pv f105 is 30 % and soft). Use it only if the X1b preview still clearly shows the beam. Otherwise drop it. No substitute word |
| X2_inner | MOUNTING POINTS | 22.563 | 25.563 | inside_sheet: tabs along the shell's inner top/bottom edges and the top bracket |
| X2_inner | RADAR UNIT | 24.063 | 25.563 | inside_sheet x_radar + its own registered scan, behind the grille |

- **No labels** on s2, s3, s8_badge, s4, s5, X1, X3 or the logo.
- No numbers anywhere: there is no sourced spec to show.
- Labels are not used on the drop shot X1, so the action reads clean.

## 4. Music map

120 BPM kick grid, t0 0.064. Cut frame = round(t*30).

| t (s) | Frame | Event | Cut into |
|---|---|---|---|
| 0.000 | 0 | start | s2 (dur 4.0333, first clip one frame short) |
| 4.064 | 122 | bar 3 | s3 (1.5) |
| 5.564 | 167 | kick | s8_badge (2.5) |
| 8.064 | 242 | phrase / flux peak | s4 (1.5) |
| 9.564 | 287 | kick | s5 f7-46 (3.0) |
| 12.564 | 377 | kick | s5b (3.5) |
| 15.06-16.06 | — | break (no kick): s5b holds | — |
| **16.063** | **482** | **DROP** | **X1 (2.0)** |
| 18.063 | 542 | bar | X1b (4.0) |
| 22.063 | 662 | bar | X2 (4.0) |
| 26.063 | 782 | bar | X3 (4.0, fade 29.563-30.063) |
| 30.063 | 902 | last phrase | logo (3.5333) |
| 33.600 | 1008 | end | — |

- Every cut is on a kick or bar line.
- Render each new shot 3 frames longer than its slot (minterpolate tail).

## 5. Diff vs the current project.yaml

| v1 | V2 | Why |
|---|---|---|
| s1_front34R 0-4.064 | **Dropped** | Crops the near fender (A). Same subject as s2 (B) |
| s2 4.064-8.064 | **Opener, re-rendered wider** | Rear edge clipped (A) |
| s3 8.064-9.564 | 4.064-5.564 | Fascia sequence, left to right |
| — | **s8_badge added**, 5.564-8.064 | Signature centre, in place of s8_hero |
| s4 9.564-11.064 | 8.064-9.564 | Fascia sequence |
| s5 11.064-14.063 | 9.564-12.564, in-point frame 7 | Its first 0.4 s repeats s2 |
| s6_top 14.063-16.063 | **Dropped** | Speckled hood, cut edge. Hood shown closed after it opened. A rotation that shows nothing new |
| — | **s5b_bay added** | Move in on the bay. Hold through the break |
| s7_explode 16.063-26.063, one wide orbit | **X1 / X1b / X2 / X3** | Progressive, section by section. Hero hold on the removed-bumper structure (C). Parts move into black. No spins |
| s8_hero 26.063-30.063 | **Dropped** | Third whole-face view, plate centred |
| logo 30.063-33.6 | Same slot, **small logo, fade in from black** | Brief 7 |

## 6. Reuse vs render

**Reuse:**

| Shot | Frames used |
|---|---|
| s3_grille | 24 |
| s4_lamp | 24 |
| s5_hood | 40 (frames 7-46) |
| logo card | rebuilt smaller with logo_card.py, no Blender |

**Bench (rendered, not used):**
- s1_front34R
- s6_top, which is running now. Let it finish or kill it.

**Cancel:**
- The queued s7_explode and s8_hero. render_queue.sh (pid 10241) re-reads shots.py for each shot and starts s7 when s6 ends.

**Render.** Settings: 15 fps, 75 %, 12 spp, persistent data OFF, a per-frame luma scan after each shot, one Blender job at a time. Preview stills (30 %, first/mid/last) before each final, especially to confirm:
- X1b: the beam, and that there is no hole;
- X2: the ducts and fogs are in frame;
- s8_badge: the plate stays out of frame.

| Order | Shot | Frames |
|---|---|---|
| 1 | X1 | ~33 |
| 2 | X1b | ~63 |
| 3 | X2 | ~63 |
| 4 | X3 | ~63 |
| 5 | s2 (re-render) | ~63 |
| 6 | s5b | ~55 |
| 7 | s8_badge | ~41 |
| | **Total** | **~380** |

At ~14-19 s/frame the total is about 1.5-2 h. The old s7 + s8 would have been 212 frames.

**Fallback if time runs out** (drop the new renders in this order):
1. **s8_badge:** give its 2.5 s to s3 and s4 instead, about 3 s each from 1.5 s renders, which is too slow. Better to keep the badge.
2. **s5b:** play s5 at 0.5x from 9.564 to 16.063 instead. The hood opens slowly and holds open through the break.

## 7. Open questions for the editor

1. **What was removed on the car itself, versus on the bench?** I assumed the whole bumper came off, then the fogs/ducts/radar/bracket came off on the bench (from the "Bumper Removed" complete-bumper and "Duct and Fogs Removed" scans). If the fogs/ducts came off on the car, they move before X1.
2. **CRASH BEAM label:** confirm the beam is actually visible in the BHR scan in the X1b preview, or drop the label.
3. **Hole check:** does fl_comp_explode leave a hole or frayed trim where the bumper was (s7 pv f023 looked frayed low)? If it does, raise the X1b framing to the lamp housings and mounts.
4. **Lock frame:** check X3's lock frame for composite seams (c5 lesson). There is no clean closed-hood base to swap to, because the hood stays open by design.
5. **Label component:** does ScanHUD have a plain label component with max 2 items and beat-timed in/out? If not, build the minimal one. White sans on the render black. Labels go in empty black areas only, never over the subject.
