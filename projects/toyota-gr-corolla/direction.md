# Toyota GR Corolla - scene direction (v2 re-order, scene-director, 2026-11-11)

Brief: scan-only Temerario-style reel, 1080x1920, 30 fps, no IRL. Text is limited to short factual labels (the parent's
addendum C overrides the earlier "no text" brief). Music: `toyota-gr-corolla_track.mp3`, 140.0 BPM, beat 0.4286 s,
t0 0.0825. No-kick build 0-414, DROP 414 (13.798 s), break 800-812, DROP 2 825 (27.513 s), last kick 37.37, end 1146.
Beat n is at frame round((0.0825 + n*0.42857)*30). Cuts below are only on the agreed 4/8-beat candidate frames.

Applied: reviewer v1 notes + parent v2 brief + parent addendum A-D (cropping, one sequence per section, removed-state
data as the hero beat with labels, no faked openings) + all of `knowledge/lessons.md`. Where they conflict, the newest
note wins.

## 1. Feature inventory (what this car's scans really contain)

Frame: car4.json (front -Y, car's right -X, floor z 0, 4.40 x 1.98 x 1.42 m, centred). Every part/state below is in the
same Artec frame (identity, regcheck medians in clips.md/editlog). I checked new evidence with numpy (scratch splats and
face-orientation stats; nothing heavy):

| Region | Scan(s) | What it shows (checked) | Quality | Use |
|---|---|---|---|---|
| Whole car | GR Corolla Full Car (16.7M tris) -> car4w 4 mm / car2w 2 mm | Wide arches, 3-vent hood, roof spoiler, triple exhaust, real front wheels | Good. The rear-left wheel is spliced from 'rear'; the rear-right is partial, so frame the front from the car's right and the rear from its left | Opening, side, reassembly |
| Front wheel | car2w | Real front-right wheel + brake + arch (v1 s3 sheet: spokes crisp) | Good at 2 mm | Detail |
| Hood (top) | car2w | Three hood vents, cowl. No hood-open / separate hood scan in frame ('Core Hood Underside' is in another frame) | Good skin. No opening allowed | Detail only, hood stays shut |
| Nose | car2w | Headlights, grille mesh, emblem, lower intakes | Good (v1 s4 sheet) | Detail |
| **Front bumper (part)** | 'Bumper (1.2m)' (2023), 3.6 mm, 1.28M tris | Outer skin + **inner face appears scanned**: 3.33 m² of surface with 22 % facing forward and 19 % facing the car (rear outer skin alone = 1.08 m², 0 % facing the car). Not a hole-fill closure: 1.9 % boundary edges | Good. Confirm the inner face visually (open question 1) | Comes off on DROP 1 |
| Front under the bumper | 'Chassis Stripped' only (no 'front bumper removed' state) | Front splat: left and right frame-rail ends/apron uprights, strut towers, firewall. **No crash beam, radiator support or headlights**: mostly black void behind the bumper (b2 render) | **Weak**, and it is the fully stripped state, not a bumper-off state | Kept soft behind the bumper. No own shot, no component label |
| Side | car4w | Left flank, real rear-left wheel, wide rear arch | Good from the left only | One short shot |
| **Diffuser (part)** | 'GR Corolla diffuser', 3.0 mm (plate deplated) | Diffuser, both faces (37 %/37 %) | Good | Comes off first at the rear |
| **Diffuser removed (state)** | 3.0/1.9 mm | Rear bumper still ON, diffuser off: muffler, exhaust pipes, crash beam visible through the centre opening | Good. Contains a **jack** under the car | Hero rear beat 1 |
| **Rear bumper (part)** | 'GR Corolla bumper' outer (1.9 mm) + 'bumper inner side' (2.9 mm) | Outer skin (1.08 m², faces out) + separately scanned inner face (1.81 m², faces the car) | Good. Inner plate impressions blocky and unreadable | Comes off, tipped once to show the inner face |
| **Rear bumper removed (state)** | 2.2 mm | Diffuser also off. **Crash beam** (horizontal bar with holes), wiring harness across the rear panel, muffler, tail-lamp backs | Rich. Has a jack | Hero rear beat 2 |
| **Crash bar removed (state)** | 3.0 mm | Beam gone: rear panel with the two **beam mounting points** (box flanges about x ±0.45, z ~0.55), wiring, muffler | Rich. Has a jack | Hero rear beat 3 (state swap on DROP 2) |
| Hatch open | 'trunk open (removed)' 2.0 mm | Cargo area as captured | Capture holes. The hatch lid would be a skin cut from the car | **Cut** (addendum D + weak data) |
| Rear Crash Beam / Upper + Lower Bumper Beam / Front Bumper Ducts | other frames | Separate beam/duct parts | Not registered | Not used (open question 3) |

Region richness (states + parts + signature + quality): **rear 5** (2 parts + inner face, 3 removed states, triple exhaust,
wing) > front 3 (1 part, signature nose/hood, weak under-structure) > wheels 2 > side 1 > top 1.
So the rear gets DROP 2 and the most beats. The front bumper gets DROP 1 because the travel is front -> side -> rear.

Physical order at the rear (read from the states): **diffuser off (bumper still on) -> rear bumper off (diffuser already
gone) -> crash beam off**. The v2 b3/b4 renders do it the other way round (bumper off with the diffuser still on, then the
diffuser drops). That state was never scanned, so neither render can be used.

## 2. Scene list (frames at 30 fps; one section per continuous sequence)

| # | Frames (beats) | Section / focus | Scans | Why here (inventory) | Render |
|---|---|---|---|---|---|
| S1 | 0-105 (8) | Whole car, front-right 3/4 | car4w | Opens on the whole car with motion from frame 1, on the end where the travel starts. Real front wheels on this side | **Reuse a1_front** as is (3.4667 s, first clip one frame short = 104 fr). Spec not rendered yet: pull the end pose back ~8 % for margins (see notes) |
| S2 | 105-208 (8) | Front-right wheel + arch | car2w | Real wheel/brake, 2 mm. The slide forward leads the travel to the nose | **NEW a4L_wheel** (a4 extended to 3.4333 s) |
| S3 | 208-311 (8) | Hood vents (top of the front) | car2w | Signature 3-vent hood. Hood stays shut (no open scan) | **NEW a7_hood** |
| S4 | 311-414 (8) | Nose: headlight -> grille | car2w | Ends square on the bumper that comes off next | **NEW a5L_nose** (a5 extended to 3.4333 s) |
| S5 | 414-568 (12) DROP 1 | Front bumper off, shown off (outer, then inner face) | xbase + fbumper | Only front part with a scan. Camera stays on the front, moves in, one tip to show the scanned inner face | **NEW b1L_fbumper** (5.1333 s) |
| S6 | 568-620 (4) | Side: left flank, rear-left 3/4 whole car | xbase + rb/rbinner/diffuser home | The travel passes the side once. Real rear-left wheel. Front bumper stays off (progressive) | **NEW a2x** (1.7333 s, a2 camera with the base swapped) |
| S7 | 620-723 (8) | Rear: diffuser off -> 'diffuser removed' | dbase (new composite) + diffuser | Rear removal 1 in physical order | **NEW b4x_diffuser** |
| S8 | 723-825 (8) | Rear: rear bumper off + inner face -> crash beam | xbase (rear = 'rear bumper removed') + rb + rbinner | Rear removal 2. The bumper's inner face is scanned. The camera ends close on the beam through the break | **NEW b3x_rbumper** (3.4 s) |
| S9 | 825-928 (8) DROP 2 | Rear: crash beam gone -> mounting points | cbrem composite | Richest state, biggest moment. Hard state swap on the drop from the same camera. No animated beam (no registered beam part) | **NEW b5_mounts** |
| S10 | 928-980 (4) | Reassembly, whole car from high rear-left | xbase + all three parts | Temerario reassembly, parts home on successive kicks, lock on b76 | **NEW c1x** (1.7333 s, replaces c1) |
| S11 | 980-1031 (4) | Clean car, same camera | car4w | Swap to the clean full car ON the lock (c5 lesson). The last frame before the logo is clean | **NEW c2x** (1.7 s, replaces c2), then a 0.5 s dip to black |
| S12 | 1031-1146 (~3.83 s) | Small logo | logo_card_small.mp4 | Short Temerario end: fade, small logo | **Reuse** (dur 4.3333 incl. dip overlap, as in project.yaml) |

Section check (addendum B), each in one continuous run: whole car S1 | wheel S2 | top/hood S3 | front S4-S5 | side S6 |
rear S7-S9 | reassembly S10-S11 | logo. "Whole car" returns only as the reassembly finale, from a new high angle; it is
not a repeat of the S1 view. Travel: front-right corner -> nose -> left flank -> rear-left -> rear -> overhead. No
front/rear ping-pong.

Pacing: 8/8/8/8 in the no-kick build (no extra cuts on the quiet build), 12 on DROP 1, 4 for the side, 8/8/8 on the rear
hero run, 4/4 into the logo.

### Camera + part notes (scan frame, metres; cam = location -> target, focal on the 20.25 mm sensor, ease inout unless noted)

Part home boxes (prepped): front bumper x -0.95..0.91, y -2.20..-1.42, z 0.14..0.73 (centre about (0, -1.81, 0.43)).
Rear bumper about y 1.57..2.24, z 0.2..0.85 (centre about (0, 1.91, 0.52)). Diffuser y 1.85..2.20, low.
Rear crash beam about y 2.0, z 0.55-0.62, x ±0.6. Keys are shot-relative seconds. "On beat n" = (frame(n) - shot start)/30.

- **S1 a1_front** (spec only, not rendered): keep the path `[-4.3,-6.3,1.55] -> [-3.85,-5.65,1.5]`, target `[0,-0.15,0.6]`,
  f30, but end at `[-4.15,-6.1,1.5]`. At the current end the 3/4 car is ~4.1 m in a ~4.5 m wide view, so the margins are
  too thin (addendum A). The whole car, both wheels and the spoiler stay in frame on first/mid/last.
- **S2 a4L_wheel** car2w, f38: `[-1.95,-0.25,0.42] -> [-1.95,-1.85,0.42]`, target `[-0.85,-0.95,0.36] -> [-0.85,-1.38,0.34]`.
  The front-right wheel centre is about (-0.82, -1.32, 0.33). Slide forward along the arch flare onto the wheel. The
  wheel stays whole in frame from mid-shot on.
- **S3 a7_hood** car2w, f32: `[-0.9,0.2,2.35] -> [-0.55,-1.0,2.0]`, target `[-0.1,-1.2,0.95] -> [0,-1.85,0.8]`. Look down the
  hood from above the cowl and push forward over the three vents. End with the hood's leading edge and grille top at the
  bottom of the frame.
- **S4 a5L_nose** car2w, f38: `[-1.75,-3.1,0.85] -> [0.0,-3.65,0.80]`, target `[-0.65,-1.95,0.72] -> [0,-2.0,0.62]`. Right
  headlight -> grille -> emblem, ending square on the centre of the bumper.
- **S5 b1L_fbumper** xbase + rbumper/rbinner/diffuser at home. Camera f30 -> 32: `[-2.9,-5.6,1.5] -> [-1.5,-4.9,1.65]`, target
  `[-0.1,-1.7,0.7] -> [-0.05,-2.55,0.85]`. The front half fills the frame (both headlights and the front wheels in, nothing
  clipped) and it is not the whole-car view.
  Bumper `fb` keys:
  - home at 0 and at 0.0667 (DROP 414).
  - At 1.7 s `loc [0,-1.05,0.55]`, ease out: forward of the nose into clear black, toward the camera but below the lens line.
  - Hold to 2.4 s.
  - At 3.6 s `rot [160,0,0]` about its own bbox centre: a tip about the width axis, no Z spin. It turns the inner face
    (normal +Y) toward the camera (computed: 157 deg). The lowest edge stays near z 0.68 and swings away from the car.
  - Hold the inner face while the camera finishes its move-in (3.6-5.13 s). The frame-rail ends of the stripped front stay
    soft behind it; don't frame on them.
  - Fallback if the inner face is ragged: translate only.
- **S6 a2x** xbase (no front bumper object) + rbumper, rbinner and diffuser at home. Second half of a2:
  `[4.08,5.98,1.58] -> [4.15,6.1,1.75]` (pulled back like S1), target `[0,0.18,0.6] -> [0,0.2,0.6]`, f30. The whole car is in
  frame. Check the stripped front-left corner at distance; it should read as "bumper off", not as a hole.
- **S7 b4x_diffuser** **New base `dbase`** = car4w with the diffuser zone replaced by 'diffuser removed' *as captured*
  (surface-distance splice, ferrari-296 composite.py; drop the jack: z < 0.10 and the lift-pad box). Deplate check. Rear
  bumper stays on.
  Camera f30: `[1.9,5.3,0.55] -> [1.2,4.3,0.6]`, target `[0,2.05,0.35] -> [0,2.0,0.4]`.
  `df` keys: home at 0 and at 0.0667 (beat 48). Then `loc [0,0.75,-0.30]` by 1.8 s, ease out: toward the camera and
  down, out of the bottom of the frame into clear black. No spin.
  The camera then rests on the opening: muffler, pipes, the beam through the centre.
- **S8 b3x_rbumper** xbase (rear = 'rear bumper removed'; **no diffuser object** - it is already off). Camera f30 -> 32:
  `[2.2,6.4,0.95] -> [1.1,4.1,0.75]`, target `[0,2.3,0.95] -> [0,2.05,0.6]`. The camera is low, so a lifted bumper sits
  above the roof-spoiler line on black, not across the body.
  `rb` and `rbinner` share one explicit `pivot [0,1.91,0.52]`. Otherwise each uses its own bbox centre and the two skins
  split.
  - home at 0 and at 0.0667 (beat 56).
  - At 1.4 s `loc [0,0.9,1.25]`, ease out (y 2.5-3.1, z 1.45-2.1).
  - From 1.5 to 2.6 s `rot [165,0,0]`: a tip about the width axis that turns the inner face (normal -Y) toward the camera
    (computed: 167 deg).
  - From 1.7 s the camera pushes in and down. The tipped bumper leaves through the top of the frame, and the shot holds on
    the crash beam + wiring through the break (frames 800-825).
  - Replaces b3. b3 also has black frames 37-52 (mean luma 6), which are moot once it is dropped.
- **S9 b5_mounts** **New composite `cbrem`** = car4w minus the rear bumper/diffuser/beam zones + 'crash bar removed' as
  captured (cbrem.blend is already prepped; drop the jack). Start on **exactly S8's end camera**, so the cut on DROP 2 is a
  pure state swap: the beam is gone and the mounting points show.
  Camera: `[1.1,4.1,0.75] -> [-0.35,4.25,0.85]`, target `[0,2.05,0.6] -> [-0.1,2.0,0.6]`, f32. A slow slide across the rear
  panel with a slight pull-back. Keep the partial rear-right arch out of frame.
- **S10 c1x** xbase + all three parts, f28: `[4.0,3.8,7.3] -> [3.85,3.65,7.0]`, target `[0,-0.1,0.6]`. The whole car plus
  the parts are in frame (about 10 m tall x 5.7 m wide view at 8.5 m).
  Start poses match where each part was left:
  - fb `loc [0,-1.05,0.55] rot [160,0,0]`
  - rb/rbinner `loc [0,0.9,1.25] rot [165,0,0]` (same pivot as S8)
  - df `loc [0,0.75,-0.30]`
  Home, ease "in", staggered on kicks:
  - rb/rbinner 0.0667 -> 0.87 (b74 = 954)
  - df 0.43 -> 1.30 (b75 = 967)
  - fb 0.87 -> 1.70 (b76 lock = 980)
- **S11 c2x** car4w (clean). Same camera, continuing `[3.85,3.65,7.0] -> [3.75,3.55,6.8]`, 1.7 s. 0.5 s dip from about frame
  1016 into the logo at 1031.

All renders: persistent data off for animated parts, then a per-frame luma scan, then contact-sheet first/mid/last for
cropping (addendum A).

### On-screen labels (addendum C)

House text style (style-guide): Inter Display, tracking +6, `#e8ecf2`. At most two items on screen, each enters on a beat
and leaves before the cut, ≥80 px inside the frame edges, never over the car silhouette, and never in the bottom 20 %
caption zone. "Top band" = y 150-330 px. "Low band" = y 1300-1500 px, used only when the car and part are clear of it.
Before keeping any label, the editor checks the render frame to confirm the named thing is visible.

| Scene | Text | In (beat/frame) | Out | Band | Backed by |
|---|---|---|---|---|---|
| S5 | FRONT BUMPER REMOVED | b35 / 452 | 555 | low band (the bumper rises into the top) | Bumper (1.2m) part scan |
| S7 | DIFFUSER REMOVED | b50 / 645 | 712 | top band | diffuser + 'diffuser removed' |
| S8 | REAR BUMPER REMOVED | b58 / 748 | 790 | low band while the bumper is up | rear bumper outer + inner + 'rear bumper removed' |
| S8 | CRASH BEAM | b62 / 800 | 820 | top band (the bumper has left the frame) | beam visible in 'rear bumper removed' (splat-checked) |
| S9 | CRASH BEAM REMOVED | b65 / 838 | 920 | top band | 'crash bar removed' |
| S9 | MOUNTING POINTS | b67 / 864 | 920 | top band, second line | box flanges visible in 'crash bar removed' (splat-checked); drop the label if they don't read in the render |

There are no labels in S1-S4, S6 or S10-S12, and no numbers (no triangle counts are claimed). There is no front
component label because the structure behind the front bumper is the stripped chassis, not a bumper-off state.

## 3. Diff vs the draft v2 timeline (project.yaml)

| Draft shot | Fate | Why |
|---|---|---|
| a1_front | **kept** S1 (pull the end pose back ~8 %) | Whole-car opener on the starting end |
| a2_rear 105-208 | **moved/shortened** -> S6 a2x 568-620 on xbase | Ping-pong front->rear->front in the build. Its job (side + rear establish) belongs between the front and the rear |
| a3_top | **dropped** | Third whole-car view in the build. S10's high rear-left overhead covers the top. Reviewer: no wasted top-downs |
| a4_wheel (1.73 s) | **replaced** by a4L_wheel 3.43 s at 105-208 | Same content, needs an 8-beat slot in the no-kick build (no extra cuts on a quiet build) |
| a5_nose (1.73 s) | **replaced** by a5L_nose 3.43 s at 311-414 | Same, and it now hands straight to the bumper on the drop |
| (new) a7_hood | **added** S3 | 3-vent hood is a signature feature. No opening |
| b1_fbumper (rendered) | **replaced** by b1L | Car small in frame, outer face only, no move-in (contact sheet). Reviewer wants the move-in and the inner face |
| b2_front_detail (rendered) | **dropped** | Weak data: a slide over a black void with two uprights under a shut hood (contact sheet). There is no 'front bumper removed' state, only Chassis Stripped |
| b3_rbumper (rendered) | **replaced** by b3x | Wrong physical order (bumper off with the diffuser still on = an unscanned state), Z spin, black frames 37-52 |
| b4_diffuser (rendering) | **replaced** by b4x | Wrong order: the diffuser comes off first, on the 'diffuser removed' state with the bumper on |
| (new) b5_mounts | **added** S9 on DROP 2 | Crash bar removed state = the richest data. The addendum asks for it |
| c1_explode (5.17 s) | **replaced** by c1x 1.73 s | Starts with every part out over the whole car (the "all at once" look). Too long for the back half (honda-s2000 "held too long") |
| c2_hero (low front-left) | **replaced** by c2x (same camera as c1x, clean car) | A separate whole-car view repeats the opener. The clean swap on the lock gives the clean last frame without a new angle |
| hood opening / hatch opening (v1) | **stay cut** | No registered hood-open or separate hood scan. The hatch's open state has capture holes and the lid would be a cut skin (addendum D) |

**Render queue now** (render_v2.sh order: b4 running, then c1, c2, a1, a2, a3, a4, a5): only **a1_front** is still needed (with
the pulled-back end pose). **Skip c1, c2, a2, a3, a4, a5** (~45 min of CPU saved).
New renders, in order of story risk: b3x, b5_mounts (+ cbrem composite), b4x (+ dbase composite), b1L, c1x, c2x, a2x,
a5L, a4L, a7_hood. At 15 fps: 52+52+52+77+26+26+26+52+52+52 ≈ 467 frames.

`python -m ive director projects/toyota-gr-corolla/project.yaml` fails now (ffmpeg on the missing a1_front PNG dir). Run it
after the renders land.

## 4. Open questions for the editor / parent

1. **Front bumper inner face**: the numbers say it is scanned (forward- and car-facing areas about equal, 3.3 m², not
   watertight), but nobody has looked at it. Render one low-res frame of fbumper.blend from +Y before S5's tip. If it is
   ragged, S5 translates only and holds on the outer face.
2. **Front reveal honesty**: behind the front bumper the composite shows the *Chassis Stripped* front (no beam, radiator
   or headlights) under a shut hood and fenders. That state never existed on the car. Is that acceptable for the parent and
   reviewer? This plan keeps it soft and unlabelled. The alternative is to keep S5's camera above the opening.
3. 'GR Corolla Rear Crash Beam.stl' and the Upper/Lower Bumper Beam scans are in other frames. If the rear beam
   registers (FPFH+RANSAC+ICP, overlap checked against 'rear bumper removed'), S9 could lift the beam off instead of the
   state swap. Until then: state swap only, per the standing rule.
4. The 'diffuser removed', 'rear bumper removed' and 'crash bar removed' state scans all contain a **jack** under the car.
   Confirm the dbase/xbase/cbrem composites drop it (and any floor) before rendering S7-S9.
5. Licence plate: dbase is a new composite from 'diffuser removed'. Check its plate area at full res (the 'rear' state
   shows a legible plate in the splat; car4w and the diffuser are already deplated).
6. Labels: the parent's addendum adds them although the original brief said "no text". Proceeding with the table above
   unless the parent says otherwise.
