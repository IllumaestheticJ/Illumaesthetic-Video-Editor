# Infiniti G35 coupe - director's shot plan (v2)

Stage 2 (`.claude/agents/director.md`). Keeps the scene order of `direction.md`; adds one focus per shot, exact cameras, cut
list, hold list and render budget. Scan only, no text, satin silver on black, 1080x1920 @30.
`python -m ive director projects/infiniti-g35/project.yaml` ran on the v1 timeline (report written to the scratchpad, not the repo):
every v1 clip lacked a `focus`; s1 had 2.8 s of dead frames; s1~s2 (IoU 0.86) and s4~s5 (IoU 0.93) were repeated views.
Re-run it on the v2 project.yaml after assembly, with `focus:` set on every clip as below.

Frame (shots.py): metres, nose -Y, +X = car's left, -X = car's right; car z 0.17-1.57, length 4.63 m (y about -2.31..+2.31).
Read off `reg/ortho_sideR.png` / `ortho_rear.png` (5.4-5.6 mm/px): front wheel centre (-0.82, -1.52, 0.53); rear wheel centre
(-0.82, 1.33, 0.60); right mirror ~(-1.00, -0.61, 1.15); right door-glass hole ~(-0.80, 0.0, 1.29-1.37); fuel door (-0.90, 1.71, 0.94);
exhaust tips (+/-0.45, 2.28, 0.36); spoiler y 2.0-2.2, z ~1.18-1.25, |x| < 0.70; tail lamps z 0.92-1.11. The ortho renders predate
the rake correction (3.7 deg), so the rear points can be ~5 cm off: check every preview before final.

## Shot table
Track time = video time + 13.363 (music starts at the measured kick 13.363 s). Camera keys in `orbit()`/`shots.py` key form:
`loc`, `target`, `focal` (mm on the 20.25 mm sensor), ease `inout` unless noted. All new shots use `car25.blend` (2.5 mm).

| section | shot | video (track) | frames | focus | camera | part action | why it earns its time | render |
|---|---|---|---|---|---|---|---|---|
| whole | s1_turntable | 0.000-2.667 (13.363-16.030) | 80 | whole car, front-right 3/4, mesh wheels | existing wide orbit (8.0 m, -24 -> -46 deg, h 1.2 -> 1.4, 30 mm); use in 0, out 80 | none | V2 rule 4: whole car, moving from frame 1 | reuse `renders/final/s1_turntable` (new wide render, 84 f) |
| front | g1_lamp | 2.667-5.333 (16.030-18.697) | 80 | right headlamp | t0: loc (-2.04, -2.80, 1.20) target (-0.65, -2.00, 0.97) 65 mm -> t 2.667: loc (-1.78, -3.13, 1.15) target (-0.65, -2.02, 0.97) 65 mm (arc 60 -> 45 deg off the nose at 1.6 m) | none | lamp shape at 2.5 mm; grille (x within +/-0.35) projects >= 0.43 m off-axis vs 0.25 m half-width -> out of frame; lower intake (z < 0.5) below frame | NEW, 42 f |
| front | g2_wheel | 5.333-8.000 (18.697-21.370) | 80 | front-right mesh-spoke rim + arch lip | t0: loc (-2.05, -1.15, 0.80) target (-0.86, -1.45, 0.60) 60 mm -> t 2.667: loc (-2.05, -1.95, 0.80) target (-0.86, -1.58, 0.60) 60 mm (slide forward 0.8 m at 1.2 m) | none | best-captured detail on the car. Deliberate extreme close-up: the rim (dia ~0.46 m) fills the 0.39 m frame width (rim edge cropped a few cm on purpose); frame spans z ~0.26-0.95, so the contact-patch speckle (< 0.30) sits at most at the bottom edge | NEW, 42 f |
| side | g3_side | 8.000-13.333 (21.370-26.697) | 160 | right side: mirror -> door line/handle -> fuel door + rear quarter | t0: loc (-2.85, -1.05, 1.05) target (-0.92, -0.62, 1.00) 55 mm; t 2.667: loc (-2.85, 0.35, 0.85) target (-0.92, 0.30, 0.65) 55 mm; t 5.333: loc (-2.80, 2.15, 1.05) target (-0.90, 1.70, 0.92) 55 mm (parallel track rear-ward, ease `lin` on the middle key) | none | the only side shot; dips to target z 0.65 while passing y 0 so the door-glass hole (z >= 1.29) stays above frame; ends on the rear quarter leading into the rear | NEW, 82 f |
| rear | g4_exhaust | 13.333-16.000 (26.697-29.370) | 80 | right exhaust tip in the bumper | t0: loc (-1.35, 3.25, 0.50) target (-0.45, 2.28, 0.38) 70 mm -> t 2.667: loc (-0.85, 3.45, 0.55) target (-0.45, 2.28, 0.40) 70 mm (low push-in/arc at 1.35 m) | none | opens the rear section on the climax kick; half-width 0.19 m keeps the plate (x within +/-0.17, 0.28 m away) and rear-corner shreds (x -0.85) out | NEW, 42 f |
| rear | g5_spoiler | 16.000-18.667 (29.370-32.030) | 80 | aftermarket spoiler on the trunk lid | t0: loc (-1.55, 3.75, 2.10) target (-0.25, 2.05, 1.22) 30 mm -> t 2.667: loc (0.00, 3.75, 2.65) target (0.00, 1.95, 1.20) 30 mm (rising arc rear-right -> centre, ~40 deg down; end half-width 0.81 m vs spoiler half-span 0.70 m, so both spoiler tips stay in frame with margin) | none | the car's mod, the rear's signature; looking down foreshortens the tail lamps; rising move hands off to the top shot | NEW, 42 f |
| top | s7_top | 18.667-21.333 (32.030-34.697) | 80 | fastback planform, ends straight top-down | existing: (2.4, -4.6, 4.0) -> (0, -0.25, 7.0), 30 mm; use in 41, out 121; fade to black over its last 12 frames (628-640) | none | top rung, continues the rise; trim skips the grille-hole frames | reuse `renders/final/s7_top` |
| end | logo | 21.333-24.633 (34.697-38.000) | 99 | ILLUMAESTHETIC logo, small | `projects/infiniti-g35/tools/logo_card.py <logo> /home/user/media/work/g35/out/logo_card.mp4 --secs 3.3 --width 380` (was 860 px; 380 px = 35 % of width, the Temerario logo is ~25-35 %) | - | the ending the brief asks for; fades in after the black | re-make card (ffmpeg/PIL, no Blender) |

Preview checks (`shots.py preview <shot>`, first/mid/last at 30 %), before any final:
- g1: no grille or intake hole visible; if the grille edge shows on the right edge, swing t0 to 65 deg / end to 50 deg.
- g2: rim centred and filling the width, no speckle at the bottom edge; if speckle reads, raise both targets by 0.04 (keep the hub in frame).
- g3 mid frame: door-glass hole above the frame; if not, lower the middle target to z 0.60. Rear wheel bottom must not show shreds at the end; if it does, raise the end target to z 0.98.
- g4: plate slab and the underbody shreds out of frame; tip centred. If the tip position is off (rake), re-aim the target at the tip seen in the first preview.
- g5: both spoiler tips in frame with margin; lamp lenses at most a thin sliver at the bottom; if the dark holes read, raise both cameras by 0.3 m.
- Every final: per-frame mean luma scan for dropouts (render with `use_persistent_data` off - spec `"persistent": false` - for all
  new shots), and a frame diff before each cut to catch the 3-frame minterpolate freeze.

Assembly notes for the editor: `concat_assemble.py` with exact `frames:` (80, 80, 80, 160, 80, 80, 80, 99), `src_fps: 15`,
`interpolate: true`; first clip one frame short if the measured cuts land late (lesson); music `start: 13.363`; set `focus:` on
every clip as in the table. Log each decision with `ive log ... --why`.

## Framing (V2 addendum A)
- Wide shots (s1, s7): whole car fully in frame in every used frame (checked on `preview_wide.jpg` and `final_s7_top.jpg`: wheels, bumpers, spoiler, mirrors inside the frame).
- Detail shots (g1-g5): the named section fills the frame. The only intentional crops are g2 (rim edge, extreme close-up) and the
  bottom of g3's last frames (rear tyre below the quarter panel, kept out because of contact-patch speckle). Anything else clipped in a
  preview is a framing error: fix the camera, not the edit.
- `ive director` was run on the v1 timeline; it flagged two repeated views (s1~s2, s4~s5) and both are gone in v2. It could not be run
  on v2 because project.yaml is not updated yet (not mine to edit); the editor runs it after updating project.yaml and fixes every flag.

## Cut list (removed from v1)
| v1 shot / frames | reason |
|---|---|
| s1_turntable frames 81-160 | dead: ease-out end, 2.8 s with almost no motion (`ive director`) |
| s2_rear (all) | redundant: same whole-car 3/4 view as s1 (IoU 0.86, corr 0.90); also a rotation that adds nothing (mazda-miata-nc rule) |
| s3_wheel (all) | off-data: tyre contact-patch speckle in every frame; replaced by g2_wheel framed above it |
| s4_lamp (all) | off-data: open grille hole grows to a third of the frame; replaced by g1_lamp |
| s5_tail (all) | off-data: tail-lamp lens holes are the subject; s4~s5 IoU 0.93; replaced by g4_exhaust + g5_spoiler |
| s6_trunk (all) | implied data: trunk opens onto car-shell back faces and black void; no trunk-open scan (V2 rule 6, honda-s2000 user rule) |
| s7_top frames 0-40 | off-data: grille hole is the brightest detail in the first frames |
| s8_explode (all) | implied data: panels carved from the closed car leave empty door openings/bay; and one wide orbit of every part at once (mazda-miata-nc, mr2-spyder rules) |
| logo 860 px | too big (V2 rule 7); remade at 380 px |

## Hold list (> 0.75 s without a cut)
Every shot moves continuously; there is no static hold. The only shot over 4 beats is g3_side (5.33 s): it is a tracking move
that shows three new subjects in order (mirror, door line, fuel door/rear quarter), so no frame repeats. The logo card (3.3 s)
holds by design: it is the ending, fades in from black and runs to the end of the track (silent at 38.3 s).

## Render budget (15 fps, 75 % res, 12 spp, car25)
| shot | secs (G35_SECS) | frames | estimate |
|---|---|---|---|
| g1_lamp | 2.6667 | 42 | ~22 min |
| g2_wheel | 2.6667 | 42 | ~22 min |
| g3_side | 5.3333 | 82 | ~44 min |
| g4_exhaust | 2.6667 | 42 | ~22 min |
| g5_spoiler | 2.6667 | 42 | ~22 min |
| **total** | | **250** | **~2.2 h** at the ~32 s/frame measured for the v1 car25 close-ups (s3 -> s4 -> s5 render timestamps); less if they render like car4 (~15 s/frame) |
Reused unchanged: `renders/final/s1_turntable` (new wide, frames 0-80 @30) and `renders/final/s7_top` (41-121 @30).
Not needed: the s2_rear re-render in progress and the queued s6_trunk re-render - stop them to free the CPU (~35 min).
Order of renders, one at a time: g3_side (no other side coverage) -> g2_wheel -> g1_lamp -> g5_spoiler -> g4_exhaust.
If the budget runs out: drop g4_exhaust and start the music one bar later (16.030 s); g5_spoiler then takes the 26.697 climax
entry and every later cut moves 80 frames earlier (reel 21.97 s).
