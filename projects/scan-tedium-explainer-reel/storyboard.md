# Storyboard - scan-tedium explainer reel

1080x1920, 30 fps. Frame numbers are reel frames (0-based, cut at the first frame of the next shot). Part A shot lengths are the
planning grid; the editor snaps every cut to a measured kick of the chosen music piece (lessons: cut on measured onsets, first clip
one frame short), and the Part A -> B cut sits on the drop.

## Look of Part A (as built in stage 1 look development, `tools/partA_scene.py`)
- **World:** cartoon shop: warm-grey floor with two light bay lines either side of the car, warm beige walls with a brand-sage band,
  a light grey roll-up door, pegboard with generic tools, workbench with a laptop, tyre stack, a wall clock with 12 tick marks and
  NO numerals. Diffuse-only materials, bright warm world + one soft sun, Standard view transform (brand hexes land as authored),
  near-black inverted-hull outlines (no Freestyle).
- **Palette:** illumaesthetic.com theme: near-black #0b0c0b (outlines, GUS's coveralls), sage #619f73 (GUS's cap, wall band, props),
  light sage #77ac87 (PIP's hoodie, scanner light, lit dot rings), off-white #ecefec (dots, eyes, headlights); car blue #2a4fb5; warm
  neutrals for floor/walls. Red only for the clock's second hand (the "pain" colour) and a tiny window-control dot on the laptop UI.
- **Car:** blocky sedan in the IS350's blue: bevelled body box, tapered cabin, dark glass with two cartoon glints, four wheels with
  off-white hubs, door seams and handles, off-white headlight slabs, near-black grille. No badge, no brand.
- **Characters (our own cuboid design, bevelled toy-block parts, no textures):** body, head, two-part arms with block hands, legs with
  shoes. Faces: round disc eyes with round pupils and a glint, skin-coloured block lids, block brows, a block mouth that scales open/shut
  (tongue block shows when open).
  **PIP** (customer): small (1.1 m), oversized head and eyes, near-black hair with a fringe and one tuft, light-sage hoodie, dark shorts,
  white shoes. **GUS** (scanner guy): big (2.1 m), tiny head with permanently half-lowered lids, near-black coveralls with an off-white
  chest patch (no text), sage cap.
- **Props:** marker dots = white centre on a black ring, one mesh, scattered by Poisson-disc sampling with 7 cm minimum spacing
  (typical neighbour ~8 cm, matching the on-screen "~8 CM"), random and never in rows, kept off glass, lights, grille and wheel arches
  (934 dots on the car); dot roll (white tape on a sage core) with a strip of dots; generic handheld scanner (grey body, dark grip,
  sage lens) with a translucent sage light cone; laptop whose screen shows car-section jigsaw pieces, the roof piece being dragged,
  three colour-coded pin pairs (sage / off-white / blue, no numerals) joined by dashed lines, and a generic arrow cursor; stool; a pile
  of peeled dots.
- **Text in Part A:** chunky white sans on a near-black plate (Inter Display), max two items, enters on a beat. Made in Remotion as a
  transparent overlay so wording can change without re-rendering 3D. The stage-1 animatic only shows grey placeholder plates.

## Character talk (animation plan; voices not cast yet)
Mouths and bodies are keyed from **per-line time windows** (script.md version A, mirrored in `LINES_A` in `tools/partA_scene.py`), not
from audio amplitude, so the animation can be built before the voices exist.
- **Mouth:** inside the speaker's window, each word gets its syllables (vowel-group count) spread evenly over the word's share of the
  window (share proportional to syllables); each syllable = open 2-3 frames (0.6-1.0 open, wider on long vowels "dots", "car", "no")
  then 1-2 frames shut, keyed with CONSTANT interpolation (snappy cartoon flaps). Punctuation holds the mouth shut: "..." 6 frames,
  "." / "?" 4 frames. Outside the window the mouth is shut.
- **Body:** each line starts with a 4-6 frame anticipation (head tilt/nod 4-8 deg, hips 2 deg) and lands one accent gesture on the
  stressed word (GUS: roll up on "Dots", head turn per word on "Front. Side. Roof. Back.", flat "No." with no movement; PIP: a 2-3 cm
  hop per stressed syllable in S1, slump deeper on "done yet"). Bezier easing, settle 6 frames after the line. GUS's head lags his body
  by 3-4 frames (slow); PIP leads (fast).
- **Listeners:** eyes track the speaker, blink every 2-4 s (lid 0 -> 1 -> 0 over 4 frames), no mouth movement.
- **When real voice takes exist (Higgsfield):** measure each take's speech start/end (ffmpeg `silencedetect`, -35 dB, 80 ms) and word
  times (faster-whisper `word_timestamps=True`), then replace each `LINES_A` window with the measured one (placed in reel time) and the
  even syllable spread with per-word timings. A take longer than its window: pick a shorter take, or tempo-stretch at most 8 %, or slide
  the following lines and let the cut grid move (cuts still snap to measured kicks). Mouth keys are regenerated from the timings, so
  only the affected shots are re-keyed and re-rendered; nothing is hand-animated.

## Part A shot list (465 frames = 15.5 s)

| shot | frames | dur | framing / camera | action | props | text (A / B differences in script.md) |
|---|---|---|---|---|---|---|
| S1 | 0-57 | 57 f (1.9 s) | Wide 3/4 of the shop, car centred, characters in front; slow 5 % push-in | PIP bounces up to GUS and asks; GUS turns his head slowly | car, clock (normal speed), bench | title **HOW DO YOU 3D-SCAN A WHOLE CAR?** from frame 0 (hook) |
| S2 | 57-110 | 53 f (1.77 s) | Medium on GUS (waist up), PIP's head at frame edge; static | GUS lifts the dot roll; the strip unrolls to the floor with a bounce | dot roll | **THE USUAL WAY** |
| S3 | 110-162 | 52 f (1.73 s) | Close on the front door, GUS's hand enters; static, tiny shake on each slap | Hand slaps a dot on per syllable; each dot pops (scale 0 -> 1.2 -> 1) at a random spot | dots | **A DOT EVERY ~8 CM** / **RANDOM, NEVER IN ROWS** |
| S4 | 162-200 | 38 f (1.27 s) | High angle (~29 deg off vertical; 12 deg made GUS an unreadable blob from above), car's length up the frame | Time-lapse: dots appear in random bursts until the car is speckled; GUS zips around as a blur | dots, clock (now turning fast in a wall inset) | - |
| S5 | 200-237 | 37 f (1.23 s) | GUS in profile at the front fender (stage 1: over-the-shoulder put his back between camera and cone) | GUS holds the scanner close; the cyan cone lights exactly 4 dots (green rings). Version B: scanner screen flashes red, "NEED MORE DOTS" | scanner, dots | **SCANNER NEEDS 4+ DOTS IN VIEW** |
| S6 | 237-283 | 46 f (1.53 s) | Side-on orthographic-ish view of the car | Car sections light up one at a time as separate grey patches (front, side, roof, rear) with visible overlap bands; GUS crouches/stretches between them | dots, section patches | **OVERLAPPING SECTIONS** |
| S7 | A 283-330 / B 283-360 | A 47 f / B 77 f | Over GUS's shoulder onto the laptop, then push into the screen | Cursor drags a puzzle-piece mesh; three numbered pins (1-2-3) on each piece connect with lines and snap. Version B: a door piece sits on the roof first, then gets nudged | laptop, mesh pieces, cursor | **MATCH 3+ POINTS PER PIECE** |
| S8 | A 330-375 / B 360-390 | A 45 f / B 30 f | Medium wide on the wall clock, PIP on a stool below it | Hands spin up to a blur; PIP slumps (B: block beard pops on) | clock, stool | - |
| S9 | A 375-423 / B 390-426 | A 48 f / B 36 f | Medium wide: GUS at the car, PIP slumped on a stool (version B: block beard) | GUS peels dots one by one, a pile grows on the floor | dots, pile, stool | **THEN PEEL EVERY ONE OFF** |
| S10 | A 423-465 / B 426-465 | A 42 f / B 39 f | Close on PIP, to camera; a 2-frame camera shake on the last word | PIP says the faster-way line; HARD CUT on the beat | - | - |

Frames are for version A; where version B's dialogue needs a different split (S7-S10) both are given. The editor moves each cut to the nearest measured kick.

Total Part A = 465 frames. Ten shots; each covers a different step, so nothing repeats (redundancy rule).

## Part B: reuse of the IS350 reel assets (no new renders)

Sources (all exist): IRL spans in `projects/lexus-is350-reels/spans.json` (graded 9:16 intermediates in
`/home/user/media/work/is350-reels/src/`), vertical scan renders in `/home/user/media/work/is350-reels/renders/<id>/<id>_preview.mp4`
(ids from `projects/lexus-is350-reels/scan_shots.md`). Use the clean renders, never frames of the finished R1-R3 mp4s (R2's V_RES_FULL
carries the "32 MIN FROM GO" line baked in).

| shot | frames | dur | source | notes | text |
|---|---|---|---|---|---|
| P1 | 465-510 | 45 f (1.5 s) | FX30541 front spray (R3_M1 region, 98.4-99.1 s used in R3; extend to ~97.9-99.4 after checking frames), x0 1000 -> 1180 | real car, first frame after the hard cut from S10 | caption of the VO line (safe area) |
| P2 | 510-558 | 48 f (1.6 s) | R1_SCAN: FX30541 322.0-323.6, x0 600 -> 650 | handheld scanning, no markers | caption; top band **NO MARKERS** only if the owner approves |
| P3 | 558-606 | 48 f (1.6 s) | R2_P2: FX30541 ends on frame 5641, x0 850 (3D agent's window) | IRL lead-in to the first 1:1 cut | version B caption "Wait, that's it?" |
| P4 | 606-660 | 54 f (1.8 s) | V_PAIR_2 (rear-right quarter) | hard 1:1 cut on a beat; cut stays on the upper body (lower-right wheel well is the known weak spot) | - |
| P5 | 660-708 | 48 f (1.6 s) | R2_P3: FX30542 ends on frame 5401, x0 150 | hood lead-in | - |
| P6 | 708-762 | 54 f (1.8 s) | V_PAIR_3 (hood, headlamp) | hard 1:1 cut on a beat | - |
| P7 | 762-804 | 42 f (1.4 s) | R2_FRONT: FX30554 ends on frame 264, x0 531 | front walk-out lead-in | - |
| P8 | 804-864 | 60 f (2.0 s) | V_MATCH_FRONT | strongest match (RMSE 0.4 px), hard 1:1 cut | - |
| P9 | 864-954 | 90 f (3.0 s) | V_RES_FULL 0-3.0 s | full scan, slow push | **LEXUS IS350 · FULL SCAN** (no time sub-line) |
| P10 | 954-1020 | 66 f (2.2 s) | logo card (logo >= 720 px wide) | on the last downbeat | **SCANS AVAILABLE AT ILLUMAESTHETIC.COM** |

Total = 1020 frames = 34.0 s. Order rear quarter -> hood -> front (R2's order minus the rear bumper pair, whose lower 40 % is black and
reads badly after a cartoon). V_MATCH_REAR is the spare if a pair has to be swapped. Each car section appears once; no shot repeats.

## How it would be built

### Option 1 (recommended): Blender 5.3, Cycles CPU, flat toon look + Remotion text overlay
- One Python script builds the shop, car, characters and props from primitives (boxes, bevel modifier, cylinders), keys the action per shot,
  and writes one camera per shot. Outlines with the inverted-hull trick (solidify modifier, flipped normals, black material, backface
  culling) - free at render time, unlike Freestyle (adds 1-3 s/frame).
- Materials: plain diffuse colours + bright world, 1 sun. Render settings: 1080x1920, 4-8 samples + OpenImageDenoise, max bounces 2,
  no caustics, no motion blur, persistent data **off** for animated shots (lessons: lighting dropouts with keyed parts), per-frame
  luma scan before assembly.
- Lip flap: keyed from per-line time windows and word timings, not the RMS envelope (see Character talk).
- Text, captions, NO MARKERS band, logo card: the existing Remotion `ReelGfx` / caption components, one transparent overlay for the whole reel.
- Assembly: frame-exact concat like `projects/lexus-is350-reels/tools/build.py` (Part B reuses its intermediates and windows unchanged).
- **Measured (stage 1, 2026-11-14):** 10 full-res stills at 8 spp + OIDN, 4 threads, persistent data off: 21-33 s each, mean 27.3 s,
  ~550 MB RSS. At that rate the 465 frames take **~3.5 h** (465 x 27.3 s), not the earlier 25-45 min guess; 4 spp or fewer
  transparent bounces (outline shells) would be the first things to test to bring it down. Earlier, untested estimate: a ~20k-triangle scene with flat
  materials at 4-8 spp on 4 cores should take roughly 3-6 s per frame at 1080x1920, so **465 frames ~ 25-45 min** of rendering, plus ~5 min
  of Remotion overlay and ~3 min assembly. The dot time-lapse (S4, a few hundred instanced discs) is the heaviest shot. First step of the
  build: render 3 test frames (S1, S4, S7) to replace this estimate with a measured one.
- Why: true cuboid 3D characters with real perspective camera moves, matching the "block-style" ask; Blender is the house 3D tool
  (setup and lessons exist); text stays editable in Remotion.

### Option 2: Remotion only (2D / pseudo-3D)
- Characters drawn as isometric SVG cuboids (three visible faces), camera moves as 2D zoom/pan; or `@remotion/three` with toon materials.
- Rendering would be faster (likely ~2-8 min for 465 frames; `@remotion/three` depends on headless WebGL via a software renderer, which is
  untested in this container), but every shot's angle has to be drawn by hand and the result reads as flat motion graphics, not block
  characters in a shop. Choose this only if the owner prefers a flat 2D explainer look.

### Not recommended
- Eevee / Workbench: both need an OpenGL context; this container has no GPU, so they would need a software GL stack that has not been
  checked here. Cycles CPU at low samples gets the same flat look without that risk.

## Audio
- Voices: piper-tts, cast and licences in `script.md`; 3-5 takes per line, keep the cleanest transcription; ducked music under every line.
- Foley (free/CC0 or synthesised): sticker slaps, a dot "pop", scanner beep, clock whirr, a cartoon "boing" on the Part A -> B cut
  (or a hard silence + the drop). Part B: music only apart from the VO lines.
