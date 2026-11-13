# Toyota GR Corolla - scene direction v3 (scene-director, 2026-11-12)

Scan-only reel, 1080x1920, 30 fps, about 24 s. User on v2: "we have a significant amount of underbumper data in the front,
under jackson racing or CSF. please add that. also take what you learned from the other videos, and apply it here."
Music: Le Castle Vania "Blood Code", `/home/user/media/music/grc_bloodcode.m4a` (176.6 s; no other reel uses it).
120 BPM, kicks on x.105 / x.605. `music.start` = 114.605, so track = video + 114.605.
Build kicks are at video 0, 2.0, 3.0, 4.0, 4.5 and 5.0, with a stop + riser at 5.4-5.9. The DROP is video 6.0
(track 120.605). After the drop there is a kick every 0.5 s.
Sibling lessons applied: cut on kicks, ONE 0.4-1.0 s action per shot, part moves rendered at native 30 fps, whole car at
~85-90 % width on wides, removed-state data as labelled hero beats (labels in clear black), parts never pass through
the body (out past the silhouette first, then away), a part that has left is not loaded again, no spins unless they show
a scanned backside, plates NOT flattened (only IS300), logo 720 px, 2.5 s logo.

## 1. Feature inventory
Frame car4.json: front -Y, car's right -X, floor z 0. The front parts are prepped `--like` and their registration was
checked in colour (`/home/user/media/work/grc/chk/under_*.png`). Boxes are in prepped metres.

| Region | Scans | What it holds | Quality / limits | Richness |
|---|---|---|---|---|
| Whole car | car4w 4 mm / car2w 2 mm | Wide arches, 3-vent hood, roof spoiler, triple exhaust | Rear-right wheel is partial: front views from the car's right, rear views from its left | opener + finale |
| Front wheel | car2w | Real front-right wheel, brake, arch, fender vent | Good at 2 mm (v2 s2 sheet) | 1 |
| **Front, under the bumper** (May 2023 "Front Bumper Underbody Data") | Bumper (1.2m) y -2.20..-1.42 | Bumper with a scanned inner face (grille back, mounts: chk/inner.jpg) | Good | **12 parts = richest** |
| | Upper Bumper Beam y -2.18..-1.93, z .35-.51 / Lower Bumper Beam z .20-.29 | Beams right behind the bumper face, across the grille | Registered (colour check) | |
| | Front Bumper Ducts (beam ends, x ±.55) / Radiator Ducts (z .21-.62) / Radiator Diverter Duct (z .33-.44) | Ducts at the beam ends and around the intercooler | Registered | |
| | Intercooler (1.5M tris prepped) y -1.99..-1.80, z .20-.35 | Core behind the lower grille, visible through the mesh with the bumper on | Registered, dense | |
| | Hood Latch x ±.1, z .30-.71 | Sits INSIDE the upper beam's box | Must move with the upper beam | |
| | Plastic Pipe, Steel pipe, S Hose, Small 90 Hose (17-58k tris) | Small pipes at the intercooler end tanks (x ±.4), y -1.84..-1.36 | Small; read unproven | |
| | fbase (car minus the front-bumper zone + Chassis Stripped fill), Engine Bay Stripped | What stays behind once the parts are out | Never looked at with every part out. Keep it soft, no label | |
| Rear | diffuser, rear bumper outer + inner parts; diffuser removed / rear bumper removed / crash bar removed states (dbase / xbase / cbase) | Physical order diffuser -> bumper -> beam. Crash beam, wiring, beam mounting flanges | Rich. Rear bumper inner face is ragged (chk/inner.jpg), so no tip | 3 parts + 3 states |
| Openings | none register | - | No hood/hatch open, no front-bumper-removed STATE scan | none |

Ranking: the **front underbumper** stack (12 registered parts) is now richer than the rear (3 parts + 3 states).
So the front gets the drop and 8.5 s, and the rear gets 5 s. The travel runs front-right -> nose -> rear-left, with no ping-pong.

## 2. Scene list (cuts only on kicks; frames = video s x 30)
| # | Video in-out (track) | Section: single focus | Scans | Action, camera, exits | Render |
|---|---|---|---|---|---|
| A1 | 0.0-2.0 (114.605-116.605) | whole: car, front-right 3/4 | car4w | Real push, ~72 -> 88 % of width, elev ~10 deg, f40, target (0,-0.2,0.55). Wheels, spoiler, nose and tail in frame with margins on first/mid/last | NEW 15 fps |
| A2 | 2.0-4.0 (116.605-118.605) | front: front-right wheel + arch | car2w | Slide forward along the arch (v2 s2 camera) | REUSE v2 s2_wheel, retimed window (below) |
| A3 | 4.0-6.0 (118.605-120.605) | front: lower grille, intercooler visible through the mesh | car2w + ic, raddu, raddiv, fbducts, beams, latch at home | Low push from front-right (z ~0.45) toward the lower grille, ending near square on the nose, through the riser | NEW 15 fps |
| B1 | 6.0-8.0 DROP (120.605-122.605) | front: bumper off, inner face | fbase + fbumper + all front parts | 6.0-6.35: bumper straight forward 0.9 m (wings clear the fenders/wheels). 6.35-6.9: up ~0.6 m + tip ~160 deg about X (v2 FB_TIP) = inner face to the lens, parked above-forward of the nose on black. Camera front-right 3/4, z ~0.9, push 6.9-8.0. Front half + parked bumper fully in frame | NEW 30 fps |
| B2 | 8.0-10.0 (122.605-124.605) | front: bumper beams | fbase + parts (no fbumper) | 8.0: upper beam + hood latch (one rigid group) forward 0.35 m, then up out the top. 8.5: lower beam forward 0.35 m, then down out the bottom. Camera ~15 deg right of square, z ~0.5, beams fill ~80 % of the width | NEW 30 fps |
| B3 | 10.0-11.5 (124.605-126.105) | front: ducts | fbase + ducts, ic, pipes | 10.0: front bumper ducts forward 0.3 m, then out to their own sides. 10.5: radiator ducts + diverter (one group) forward 0.35 m, then down out of frame. Camera tighter, z ~0.4 | NEW 30 fps |
| B4 | 11.5-13.5 (126.105-128.105) | front: intercooler | fbase + ic, pipes | 11.5-12.3: intercooler forward 0.45 m + down 0.3 m, parked in clear black under the nose, core square to the lens (no turn: the core already faces it). Camera square, z ~0.3, pushes in until the core fills ~70 % of the width | NEW 30 fps |
| B5 | 13.5-14.5 (128.105-129.105) | front: pipes + hoses | fbase + 4 pipes/hoses | 13.5-14.1: the 4 pieces forward 0.4 m together, out of the empty intercooler opening. Camera into the opening. **Gate**: preview one frame. If they don't read as pipes on the bay, cut B5 and run B4 11.5-14.0 and C1 14.0-16.0 | NEW 30 fps |
| C1 | 14.5-16.0 (129.105-130.605) | rear: diffuser off | dbase + diffuser | 14.5-15.2: diffuser back (+Y) 0.4 m, then down out of the bottom. Camera rear-left 3/4, low, rear half fills the frame, front axle out of frame (dbase still has its front bumper) | NEW 30 fps |
| C2 | 16.0-18.0 (130.605-132.605) | rear: rear bumper off -> crash beam | xbase + rbumper + rbinner (shared pivot 0,1.91,0.52) | 16.0-16.8: bumper straight back +0.75 m (past the tail lamps), then up out the top. No tip. Camera pushes onto the beam and ENDS exactly on v2 s8's end camera [1.1,4.1,0.75] -> [0,2.05,0.6], f32 | NEW 30 fps |
| C3 | 18.0-19.5 (132.605-134.105) | rear: crash beam removed, mounting points | cbase | Hard state swap on the 18.0 kick from the same camera, then a slow slide across the rear panel | REUSE v2 s9_mounts, frames 1-30 at src_fps 20 |
| D1 | 19.5-21.5 (134.105-136.105) | whole: clean car, high rear-left 3/4 | car4w | Swap to the clean car on the kick (c5 rule). Elev ~30 deg (not overhead), whole car at ~85 % width, 8-10 % push. Shows the roof spoiler, hood vents and wide arches. Fade to black 21.0-21.5 | NEW 15 fps |
| Logo | 21.5-24.0 (136.105-138.605) | end card | logo 720 px | 0.3 s fade in, hold, music fade_out 0.3 | rebuild the card at 720 px |

Cut frames: 60, 120, 180, 240, 300, 345, 405, 435, 480, 540, 585, 645; end 720 (24.0 s). The first clip is one frame
short. Snap each cut to the MEASURED kick onset of the decoded output (gr86 / c5 lessons), within half a frame.
Sections (rule B): whole A1 | front A2-B5 (wheel -> grille -> under-bumper stack, one continuous run) | rear C1-C3 |
whole D1 (finale, opposite corner + high angle; log the expected director silhouette flag A1~D1). C2->C3 is a same-camera
state swap, also expected to be flagged; keep it.

### Part paths and parking (run porsche-gt3rs-992 `tools/clipcheck.py` on every keyed part before final)
- Every front part first moves straight forward (-Y) until its rear face is at y < -2.25 (forward of the bumper line,
  free space), and only then turns up, down or sideways. The latch overlaps the upper beam's box, so they move as one group.
  The intercooler goes only after the lower beam, radiator ducts and diverter have left (each sits in its forward path).
- Rear parts: straight back (+Y) past the tail lamps, then down (diffuser) or up (bumper). Never a diagonal from home.
- A part that has left the frame is not loaded in later shots. Parked parts in their own shot (bumper in B1, intercooler
  in B4, pipes in B5) must be fully inside the frame on the last frame (3 px edge-touch test). Parts move over black,
  not across the body.
- A3 uses car2w (no seams) with the hidden parts at home. B1-B5 use fbase from frame 0 (the bumper moves at once).
- Persistent data off for every shot with keyed parts. Per-frame luma scan on every render dir. First/mid/last contact
  sheet per shot. The reused A2 window must pass the edge test on its own first frame (the v2 s2 first frame touched the
  right edge): start the window at about frame 18 of 52 and set src_fps so it fills 2.0 s; otherwise re-render.

## 3. Labels (ScanHUD label, `shadow: true`, title + short sub, never an empty sub, one item at a time, 80 px inside)
Band: top = y 150-330 px, low = y 1300-1500 px. The window must be clear black on 4 samples (gr86 v3 / gt3-992 v2).
If the band isn't black, use the other band. If neither is black, drop the label.

| Shot | Title / sub | Window (video s) | Band | Backed by |
|---|---|---|---|---|
| B1 | FRONT BUMPER / REMOVED | 6.5-7.9 | low (bumper parks high) | Bumper (1.2m) part + registered parts behind it |
| B2 | BUMPER BEAMS / UPPER + LOWER | 9.0-9.9 | top (upper beam is gone by ~8.7) | Upper/Lower Bumper Beam files |
| B3 | DUCTS / BUMPER + RADIATOR | 10.5-11.4 | top | Front Bumper Ducts, Radiator Ducts files |
| B4 | INTERCOOLER / BEHIND LOWER GRILLE | 12.0-13.4 | low (intercooler parks above it) | Intercooler file + colour registration |
| B5 | PIPES + HOSES / STEEL + PLASTIC | 13.5-14.4 | low | Steel pipe, Plastic Pipe, S Hose, Small 90 Hose files |
| C1 | DIFFUSER / REMOVED | 15.0-15.9 | top | diffuser + diffuser removed |
| C2 | CRASH BEAM / REAR BUMPER REMOVED | 16.5-17.9 | low (bumper exits the top) | rear bumper removed state |
| C3 | MOUNTING POINTS / CRASH BEAM REMOVED | 18.0-19.4 | top | crash bar removed state (flanges seen in v2 s9) |

No brand names (no folder or file says Jackson Racing or CSF), no numbers, no labels on A1-A3, D1 or the logo.

## 4. Open risks / questions
1. **Bumper vs car nose**: Bumper (1.2m) is from 2023 and the full car is a later session. Before A3/B1, overlay it in red over
   car2w at the nose. If the grille/lip differ, A3 must not imply that it is the same bumper (render A3 on fbase + fbumper).
2. **Double intercooler in A3**: car2w may carry its own partial capture behind the mesh. Preview A3 and look for ghosting.
3. **fbase after the parts leave** (end of B4, B5): the Chassis Stripped / Engine Bay Stripped fill has never been looked
   at. Keep the background soft and unlabelled. If it reads as a hole, frame tighter on the parked parts.
4. **Pipes/hoses** may be too small to read, so B5 is gated (fallback in the table). Clipcheck their forward path past the
   frame-rail ends.
5. Close-ups B2-B5 sit on the 4 mm fbase. The parts themselves are dense, so frame on the parts.
6. User wording "Jackson Racing or CSF": the parent mapped it to the May 2023 underbody folder (CSF makes GR Corolla
   intercoolers). Confirm with the user if the intercooler should be named. Until then, no brand on screen.
7. The intercooler's 3.7M source triangle count is in the file name only. Not shown (prepped mesh is 1.5M).

## v2 -> v3 diff
| v2 shot | v3 | Why |
|---|---|---|
| s1_whole (car ~55 % width) | A1 new | Too small. Siblings: ~85-90 % of width with a real push |
| s2_wheel | A2 reused, retimed window | Content right; only the timing changes |
| s3_hood | cut | Build has 3 slots. The hood can't open (no scan). Vents read again in D1 from high |
| s4_nose | A3 new | The intercooler must sit behind the mesh (new parts) |
| s5_fbumper (5.1 s, stripped void behind) | B1 new, 2.0 s | Same move, one action, with the registered under-bumper parts behind |
| (new) | B2-B5 | User: add the under-bumper data. Beams, ducts, intercooler, pipes on kicks with labels |
| s6_side | cut | Bridge shot with no data. The ~24 s budget goes to the front |
| s7_diffuser, s8_rbumper (3.4 s each, 15 fps, bumper tip) | C1, C2 new | 120 BPM timing, native 30 fps moves, straight-out paths, no tip (inner face ragged) |
| s9_mounts | C3 reused (first 1.5 s) | Same state swap. C2 ends on its start camera |
| s10_reassemble + s11_clean (small top-down) | D1 new | Small car, near-overhead. One clean whole-car beat instead |
| logo 540 px, 3.8 s | 720 px, 2.5 s | Logo-size and "held too long" lessons |
| v2 track (140 BPM) | Blood Code, 120 BPM | User-supplied |
