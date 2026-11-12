# Direction: Subaru Impreza GD trio (bugeye / blobeye / hawkeye), scan-only reel

Scene director pass, 2026-11-12. Nothing is rendered yet. Every camera below was checked by projecting the three
4 mm scans through a pinhole model of the house camera (sensor 20.25 mm horizontal, 1080x1920); that model reproduces
the existing `O1_open` frame 1 to the pixel in x (202..984 vs 202..984). Pixel extents quoted here are from that
projection, not from renders, so the first/mid/last contact sheet is still required before finals.

## 1. Concept

One shell, three faces. The three full-car scans sit in one frame, so one camera move rendered on each car gives a
pixel-aligned hard cut bug -> blob -> hawk where the roof, doors and glass stay locked and only the lamps, bumper,
scoop, wing and tail change. That cut is the whole reel: it is this reel's 1:1 cut, and it happens 10 times, always
on a kick, always in build order (bugeye, blobeye, hawkeye). The camera travels one way round the car's LEFT side
(front 3/4 -> front detail -> rear 3/4 -> rear detail -> up over the roof) and never returns. The intro gives each
car a full bar with its name; the drop halves the hold to two beats per car on the face, which is the feature the
three cars are named after; the reel ends on a top view where scoop, wing and roof vane all change in one frame, then
the logo on the last kick. 18.6 s, no state scans, no carved parts, no composites, no exploded view.

## 2. Feature inventory (from the scans, `clips.md` and `/home/user/media/work/gd3/chk/trio.jpg`)

| Scan | What it holds | Signature features | Weak data |
|---|---|---|---|
| Bugeye Full Car (bug4.blend) | whole car, closed, p50 2.4 mm to blob, 76 % overlap | round lamps, mesh grille (captured), plain trunk lid with NO wing, 5-spoke wheels | lowest overlap of the three; a few points below ground (bbox z min -0.034 m); lower rear bumper edge looks ragged in the splat |
| Blobeye Full Car (blob4.blend) | whole car, closed, reference frame | teardrop lamps, tall STI wing, STI scoop | grille and lower intake are open holes with a ragged edge; rear plate is legible |
| Hawkeye Full Car (hawk4.blend) | whole car, closed, p50 1.5 mm, 84 % overlap | slim lamps, three-part grille, tall wing, roof vane, different tail lamps; nose 50 mm longer (bbox y -2.251 vs -2.202) | grille openings are holes; stray fragment in the FRONT-RIGHT wheel arch |
| Blobeye state scans (engine bay, bumper removed, all removed, wing off, skirt off, hood removed) | partial captures of one car | - | sparse, frayed capture edges; these are what the user called "the wrong things" |
| Hawkeye engine Bay.stl | not fetched | - | one car only |

No open hood / trunk / door scan exists for any of the three, and no separate part scans. So the ladder is
exterior wide -> exterior detail -> top pass -> logo. No open state, no removal, no explode.

Region scores (what differs between the three cars x scan quality):

| Region | What changes across the three | Quality | Score | Decision |
|---|---|---|---|---|
| Front | lamps, grille, bumper, scoop: all three differ | good, holes in blob/hawk grilles | highest | opener (wide) and the drop (detail) |
| Rear | no wing -> wing -> wing + roof vane; three tail lamp designs | good, plate legible | high | 12 beats, wide then detail |
| Top | scoop shape, wing, vane, nose length, all in one frame | good | medium | 8-beat closing pass |
| Side | same shell; only wheels and skirts differ | good on the left, fragment on the hawk's right | low | no section of its own (visible in F1 and R1) |
| Wheels | bug 5-spoke vs multi-spoke | fine | low | not a generation feature, cut |
| Engine bay / interior / underside | no data for three cars | - | 0 | cut |

All cameras stay on the car's left (+X). The hawkeye's stray fragment is in the front-right arch, and the reusable
blobeye front renders were shot from the right, which is one reason they are not reused.

## 3. Music start and shot table

Music start: **8.630 s** into the track (beat 20, a kick). Video time = (beat - 20) x 0.42862 s. Intro = beats 20-31
(two bars of groove, then the kick on 28 and the 3-beat break), drop at beat 32 = video 5.143 s, last kick beat 60 =
video 17.145 s, music tail carries the logo, out by video 18.65 s. No cut falls on the kick-less break (29-31).

Frames are output frames at 30 fps, cut k at round(video_s x 30). Snap each cut to the measured kick attack on the
decoded audio before final assembly (lessons: grid fits drift; first clip one frame short).

| Shot | Section | Car | Start beat | Video s | Frame | Beats | Frames | Label |
|---|---|---|---|---|---|---|---|---|
| F1 | front, wide | bugeye | 20 | 0.000 | 0 | 4 | 51 | BUGEYE |
| F1 | front, wide | blobeye | 24 | 1.714 | 51 | 4 | 52 | BLOBEYE |
| F1 | front, wide | hawkeye | 28 | 3.429 | 103 | 4 | 51 | HAWKEYE |
| F2 | front, detail | bugeye | 32 (drop) | 5.143 | 154 | 2 | 26 | - |
| F2 | front, detail | blobeye | 34 | 6.001 | 180 | 2 | 26 | - |
| F2 | front, detail | hawkeye | 36 | 6.858 | 206 | 4 | 51 | - |
| R1 | rear, wide | bugeye | 40 | 8.572 | 257 | 2 | 26 | - |
| R1 | rear, wide | blobeye | 42 | 9.430 | 283 | 2 | 26 | - |
| R1 | rear, wide | hawkeye | 44 | 10.287 | 309 | 2 | 25 | - |
| R2 | rear, detail | bugeye | 46 | 11.144 | 334 | 2 | 26 | - |
| R2 | rear, detail | blobeye | 48 | 12.001 | 360 | 2 | 26 | - |
| R2 | rear, detail | hawkeye | 50 | 12.859 | 386 | 2 | 25 | - |
| T1 | top | bugeye | 52 | 13.716 | 411 | 2 | 26 | - |
| T1 | top | blobeye | 54 | 14.573 | 437 | 2 | 26 | - |
| T1 | top | hawkeye | 56 | 15.430 | 463 | 4 | 51 | - |
| LOGO | - | - | 60 (last kick) | 17.145 | 514 | 3.5 | 45 | logo card |
| end | | | | 18.645 | 559 | | | |

Screen time per car: bugeye 12 beats, blobeye 12, hawkeye 16 (it carries the break and the last bar).
Holds: 4 / 4 / 4 in the intro, 2 / 2 / 4 and 2 / 2 / 2 in the drop. 14 hard cuts between scan shots, all on kicks, plus the cut to the logo.

### Camera moves (prepped frame: metres, nose -Y, car's right -X, ground z 0)

Keys are (loc xyz, target xyz, focal mm). Every move is ONE straight `lin` segment from start to end, so there is no
ease to break at a cut and motion is present from frame 1 to the last frame of each shot.

| Shot | Start key | End key | Length | What the viewer should notice |
|---|---|---|---|---|
| F1 | (3.35, -5.55, 1.05) -> (-0.17, -0.25, 0.52), 32 | (1.80, -5.60, 1.20) -> (-0.12, -0.45, 0.52), 35 | 12 beats, 5.143 s | Whole car, front-left 3/4, arcing about 13 deg toward the nose with a slight push. On each bar the face changes (round -> teardrop -> slim lamps, bumper, scoop) while the cabin does not move; on the second cut the wing appears at the far end. |
| F2 | (1.25, -5.15, 1.75) -> (0.04, -1.20, 0.66), 36 | (0.30, -4.85, 2.25) -> (0.00, -1.20, 0.66), 38 | 8 beats, 3.429 s | High, near head-on, rising and swinging to the centre line. The front end fills the frame width: lamps, grille, bumper openings and the hood scoop swap on the drop. From this height the grille openings are foreshortened, so the scoop and lamps are the subject, not the holes. |
| R1 | (3.75, 4.95, 1.15) -> (-0.12, 0.35, 0.52), 30 | (2.45, 5.60, 1.35) -> (-0.06, 0.50, 0.52), 32 | 6 beats, 2.572 s | Whole car, rear-left 3/4, arcing toward the tail. Bare bugeye trunk, then the STI wing lands on a kick, then the hawkeye adds the roof vane and new tail lamps. |
| R2 | (1.10, 5.35, 1.80) -> (-0.03, 1.20, 0.72), 37 | (0.30, 5.00, 2.35) -> (-0.05, 1.20, 0.72), 38 | 6 beats, 2.572 s | High, near tail-on, rising. Tail lamps, trunk lid, wing and (hawkeye) roof vane at detail scale; continues R1's direction and climbs toward the top view. |
| T1 | (0.00, 1.75, 6.70) -> (0.00, 0.25, 0.60), 30 | (0.00, 1.67, 6.20) -> (0.00, 0.25, 0.60), 30 | 8 beats, 3.429 s | Top view from behind, about 14 deg off vertical, nose up, car length along the frame height, slow descent. Scoop shape, wing / no wing, roof vane and nose length change in one frame: the summary of the reel. |

Projected extents (px of 1080 x 1920, min/max over each shot, all three cars):

| Shot | x range | y range | Note |
|---|---|---|---|
| F1 | 49 .. 994 | 671 .. 1243 | whole car, 85-87 % of width, 49 px left / 86 px right margin |
| F2 | 30 .. 1012 | 405 .. 1493 | whole car still inside the frame (mirrors 30 px from the edges), front end about 90 % of width |
| R1 | 59 .. 1043 | 698 .. 1201 | whole car, 86-91 % of width |
| R2 | 53 .. 1023 | 521 .. 1456 | whole car inside the frame, tail about 88 % of width |
| T1 | 264 .. 816 | 374 .. 1528 | car 1060-1150 px tall of 1920, stays above the bottom caption zone (1536) |

F1 and R1 leave black above and below the car; that is the cost of showing the whole car in 9:16. The label fills
the lower band in F1. F2, R2 and T1 are the tall framings.

### Labels

Only in F1, one at a time, title only (ScanHUD `label`, `sub: " "` because an empty sub crashes), centred, in the
black band below the car at about y 1380 (car bottom is at y <= 1243, caption zone starts at 1536).

| Text | In (frame) | Out (frame) |
|---|---|---|
| BUGEYE | 2 | 45 |
| BLOBEYE | 53 | 97 |
| HAWKEYE | 105 | 148 |

Years are left off: see open question 1.

### Logo card

`remotion/public/illumaesthetic_logo.png` (6447 x 1434) at **720 px wide of 1080** (720 x 160), centred on black.
Hard cut in on beat 60, the last kick (frame 514). Hold 45 frames (1.5 s) over the music tail, fade the last 10 frames
with the audio. 280 px was called too small on the blobeye reel and 380 px on two other reels; 700-720 px is the size
those reels moved to.

## 4. Same camera on three cars: per-car segment boundaries

All five shots are the same camera rendered on bug4 / blob4 / hawk4. Because each move is a single linear segment,
each car's segment can be its own spec whose two keys are the boundary poses below; the pose at the end of one car's
segment equals the pose at the start of the next car's, so the move is continuous through the cut.

| Shot | Boundary (shot beat, shot s) | loc | target | focal |
|---|---|---|---|---|
| F1 | 0 / 0.000 (bug in) | 3.350, -5.550, 1.050 | -0.170, -0.250, 0.52 | 32.00 |
| F1 | 4 / 1.714 (bug -> blob) | 2.833, -5.567, 1.100 | -0.153, -0.317, 0.52 | 33.00 |
| F1 | 8 / 3.429 (blob -> hawk) | 2.317, -5.583, 1.150 | -0.137, -0.383, 0.52 | 34.00 |
| F1 | 12 / 5.143 (hawk out) | 1.800, -5.600, 1.200 | -0.120, -0.450, 0.52 | 35.00 |
| F2 | 0 / 0.000 (bug in) | 1.250, -5.150, 1.750 | 0.040, -1.200, 0.66 | 36.00 |
| F2 | 2 / 0.857 (bug -> blob) | 1.012, -5.075, 1.875 | 0.030, -1.200, 0.66 | 36.50 |
| F2 | 4 / 1.714 (blob -> hawk) | 0.775, -5.000, 2.000 | 0.020, -1.200, 0.66 | 37.00 |
| F2 | 8 / 3.429 (hawk out) | 0.300, -4.850, 2.250 | 0.000, -1.200, 0.66 | 38.00 |
| R1 | 0 / 0.000 (bug in) | 3.750, 4.950, 1.150 | -0.120, 0.350, 0.52 | 30.00 |
| R1 | 2 / 0.857 (bug -> blob) | 3.317, 5.167, 1.217 | -0.100, 0.400, 0.52 | 30.67 |
| R1 | 4 / 1.714 (blob -> hawk) | 2.883, 5.383, 1.283 | -0.080, 0.450, 0.52 | 31.33 |
| R1 | 6 / 2.572 (hawk out) | 2.450, 5.600, 1.350 | -0.060, 0.500, 0.52 | 32.00 |
| R2 | 0 / 0.000 (bug in) | 1.100, 5.350, 1.800 | -0.030, 1.200, 0.72 | 37.00 |
| R2 | 2 / 0.857 (bug -> blob) | 0.833, 5.233, 1.983 | -0.037, 1.200, 0.72 | 37.33 |
| R2 | 4 / 1.714 (blob -> hawk) | 0.567, 5.117, 2.167 | -0.043, 1.200, 0.72 | 37.67 |
| R2 | 6 / 2.572 (hawk out) | 0.300, 5.000, 2.350 | -0.050, 1.200, 0.72 | 38.00 |
| T1 | 0 / 0.000 (bug in) | 0.000, 1.750, 6.700 | 0.000, 0.250, 0.60 | 30 |
| T1 | 2 / 0.857 (bug -> blob) | 0.000, 1.730, 6.575 | 0.000, 0.250, 0.60 | 30 |
| T1 | 4 / 1.714 (blob -> hawk) | 0.000, 1.710, 6.450 | 0.000, 0.250, 0.60 | 30 |
| T1 | 8 / 3.429 (hawk out) | 0.000, 1.670, 6.200 | 0.000, 0.250, 0.60 | 30 |

Notes for the editor:
- Start each car's render exactly at its cut time so the first frame after every cut is a real rendered frame.
- Tail margin: render 3 source frames past each cut (lessons: minterpolate drops the tail and the assembler then
  clones a frame). Keep the camera moving through the margin by extending the same linear rate past the end key;
  a clamped end key freezes the margin frames.
- Same look on all 15 segments: -0.5 EV, 12 spp, 810 x 1440, 15 fps. Camera-only static scenes, so persistent data
  can stay on, with the per-frame luma scan afterwards.

## 5. New rendering

No existing blobeye render is reused (reasons in section 6), so every scan frame is new.

| Shot | Output frames | Source frames at 15 fps | + 3 tail frames x 3 cars |
|---|---|---|---|
| F1 | 154 | 78 | 87 |
| F2 | 103 | 52 | 61 |
| R1 | 77 | 39 | 48 |
| R2 | 77 | 39 | 48 |
| T1 | 103 | 52 | 61 |
| Total | 514 (17.13 s) | 260 | 305 |

Estimate at the 25-33 s per frame in `clips.md`: 260 frames = 1.8-2.4 h; with the tail margins, 305 frames =
**2.1-2.8 h, about 2.45 h at 29 s per frame**. Add about 10 minutes for the 45 preview stills (first / mid / last of
each segment at 30 %). This is at the edge of the 2.5 h budget. Time the F1 bugeye segment (29 frames) first and
project the total from it.

Pre-planned trim if the projection goes over: start the music on beat 24 (10.345 s) instead of beat 20 and make F1
8 beats (bugeye 24-25, blobeye 26-27, hawkeye 28-31). That saves 26 source frames (about 12 minutes) and gives a
16.9 s reel; the F1 keys stay the same, played over 8 beats. Everything from the drop on is unchanged. I did not
make this the default because it drops below the 18 s target and halves the time each name is on screen.

## 6. Left out, and why

- **All partial state scans** (blobeye engine bay, bumper removed, all removed, wing off, skirt off, hood removed;
  hawkeye engine bay): sparse captures of one car. The blobeye reel held 4.8 s on each and the user called it too
  long on the wrong things. In a three-car comparison a one-car state has nothing to cut against. See open question 2
  for the conflict with the standing bumper-removed rule.
- **Carved panels, composites, exploded view, reassembly**: no separate part scans exist; the user called the carved
  versions hallucinated.
- **Open hood / trunk / doors**: no open-state scan of any of the three cars.
- **A side section**: the flank is the same shell on all three; a cut there changes only wheels and skirts. It is
  already in frame in F1 and R1. A third whole-car pass would be the redundancy the user flagged.
- **Wheel close-up**: wheels are not what separates the three generations, and the hawkeye's front-right arch carries
  a stray fragment.
- **Dead-on low nose close-up** (the middle row of trio.jpg): it makes the blobeye and hawkeye grille holes the
  subject. F2 covers the same face from above.
- **Reusable blobeye renders** (s1_front34, O1_open / s2_rear34, R_wing, s8_wing, s4_light, s6_top, s3_wheel, H_a,
  E_bay, B_b): looked at on a contact sheet. The wides hold the car at about 58 % of frame width with dead black
  around it; the front shots are from the car's right; s6_top rotates; the details use 2 mm crops with their own
  cameras. A pixel-aligned cut needs the identical camera and light rig on all three cars, so mixing an old blobeye
  segment between new bugeye and hawkeye segments risks a visible step for a saving of under 10 minutes per shot.
- **Model years on the labels**: see open question 1.
- **Dissolves, turntables, a held ending, any second pass over a section**.

## 7. Risks to check on the contact sheets (first / mid / last of all 15 segments, before finals)

1. **Light rig per car.** `shot.py` places the studio lights from the base bbox, and the bboxes differ (bugeye has
   no wing and points at z -0.034; hawkeye nose is 50 mm longer). Compare mean luma on the roof and door either side
   of every cut; a step means the lights moved and the rig has to be pinned to one bbox for all three.
2. **Registration at the cut.** Bugeye is p50 2.4 mm with 76 % overlap. Check the frame pair at each cut (roof line,
   door shut lines, mirrors, glass edges) for a jump; `phaseCorrelate` on the cabin region should read under 1 px.
3. **Edge margins.** F2 has mirrors 30 px from the frame edges and R2 about 55 px. Run the edge-touch test (non-black
   pixels in the outer 3 px) on first / mid / last of every segment. T1 last frame: car bottom at y 1528.
4. **Bugeye below-ground points** (z down to -0.034): look under the tyres in F1 frame 0, the opening frame.
5. **Grille holes** in the blobeye and hawkeye in F2: ragged dark edge on the blobeye's lower intake. If it reads as
   damage, raise the F2 camera 0.2 m on all three cars rather than re-framing one.
6. **Hawkeye stray fragment** (front-right arch): F2 ends 3.5 deg off the centre line and T1 sees both sides.
7. **Bugeye rear bumper lower edge** in R1 / R2 looked ragged in the projection.
8. **Licence plates**: R1 and R2 show the rear plates, F2 the front. Standing rule is to keep plates as scanned
   (flatten only on the IS300). Flag to the user if any plate is legible; do not change it without being asked.
9. **Top view up-vector**: T1 is 14 deg off vertical with the offset along +Y, so nose-up is defined. Confirm no roll
   between segments.
10. **Lighting dropouts**: per-frame luma scan on every segment.
11. **Cut frames**: no cloned or blended frame at any of the 14 cuts (frame-diff check on the assembled file); the
    frame before each cut is the outgoing car, the frame after is the incoming car.
12. **Cut sync** on the delivered file's decoded audio, within half a frame. The drop kick (beat 32) has a weaker
    onset (2.1) than its neighbours, so measure it rather than trusting the grid. Beat 60 is the last full kick.
13. **Labels**: read the last frame of each label; check the band under the car is black for the whole window.
14. **`ive director`** will flag the same-camera car swaps as repeated views (intended: they are the 1:1 cut) and
    probably F1 against R1 (mirror silhouettes, different sections). Log both as reviewed, do not cut them.

Section of every shot, for the redundancy rule: F1 front, F2 front (adjacent to F1), R1 rear, R2 rear (adjacent to
R1), T1 top. Each section appears once.

## 8. Open questions

1. **Years on the labels.** `clips.md` gives 2002-03 / 2004-05 / 2006-07, which are the US model years for the three
   faces. Nothing in the scan files says what year or market these three cars are, so the plan shows names only.
   If the years are wanted, they fit as the label sub line with no other change.
2. **Bumper-removed rule.** The standing rule from 2026-11-11 says a bumper-removed scan gets its own labelled hero
   section, and the blobeye has one (render `B_b` exists). I left it out because the newer feedback on the blobeye
   reel was that those state scans were the wrong thing to dwell on, and this reel is a three-car comparison. This is
   a conflict between two user instructions and needs the user's call, not mine.
3. **Length.** 18.6 s as planned; 16.9 s with the pre-planned trim. The music cannot end earlier without an edit to
   the track, because the logo lands on its last kick.
4. **Hawkeye gets 16 beats to 12 each for the others** because it carries the break and the last bar. If equal time
   matters, F2 and T1 can run 2 / 3 / 3 beats (bugeye 12, blobeye 14, hawkeye 14), at the cost of two cuts landing
   off the bar line.
