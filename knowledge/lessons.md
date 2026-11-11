# Lessons (standing rules)

Append-only. Reviewer feedback promoted with `python -m ive feedback <project> "<note>" --rule`
lands here automatically. Agents must read this whole file before editing.

## From the 240SX scan reel (2026-11-10, built by an agent)
- **[match-cut]** Choose the cut frame by *scan state*, not by drama. The bumper-pull frame had no
  rigid landmarks in common with any scan (pop-up lights and hood moved between sessions).
- **[match-cut]** Landmarks on one flat face can't solve focal length (solver returned 193 mm).
  Spread points in depth (emblem + spoiler tips + mirror) or fix focal to the lens (iPhone 1×: 28 mm
  on a 20.25 mm-wide portrait sensor).
- **[match-cut]** Raycasts on panel seams fall through scan cracks to the far side of the car.
  Nudge picks off seams and re-project to verify.
- **[technical]** Changing ground cleanup re-normalises the scan and silently breaks camera solves.
  Pin the transform with `--like`.
- **[technical]** Full-car Artec STLs (25M tris) OOM Blender on 15 GB. Decimate out-of-core first.
- **[technical]** Rendering while npm/Chrome run in parallel took 6× longer. Serialise heavy jobs.
- **[scan-look]** House scan look is satin metallic silver on pure black (Temerario), not white clay.
- **[text]** HUD numbers must come from the data: 24,991,097 triangles (STL header), length
  4,527 mm (scan footprint; spec sheet says 4,520 mm — good sanity check).
- **[technical]** `type: cut` is a 1-frame xfade; without compensation each cut shifts everything after it
  1 frame earlier (8 cuts = 0.27 s off the music). The assembler now adds the frame back; always give
  clips an explicit `dur` from the beat grid.
- **[technical]** When trimming the clip that ends on the match frame, move `in`, never `out`.
- **[scan-look]** "Tighter" in 9:16 does not mean "whole car fills the width" - a full side profile at
  100 % width still reads small. Tighten by cropping into the car (3/4 views, side tracks that
  crop bumpers) and keep exploded parts from flying at the lens (move them down/back too).
- **[technical]** Splice part-state scans into the full car over the *smallest* zone that changed.
  Swapping half the car exposed coverage holes in the partial scan.
- **[text]** Before putting a claim like "inside + outside scanned" on screen, render the part from
  the hidden side and look. 240SX: true for front skin, rear skin, rear beam; the front crash beam only
  exists on the car (chassis scan), so it was not claimed.
- **[scan-look]** Showing a part's inside: flip it about its long (car-width) axis (`x180` in
  `--explode`), not a Z spin - a 1.6 m bumper spinning about Z sweeps into the car and the lens.
- **[story]** Ending on a product listing: if the listing's hero image is a render of the same scan,
  end the scan shot on that angle and dissolve - it reads as one object. 240SX v3.
- **[technical]** Parts spinning about Z need clearance from the body: stack them (one below, one above
  the car) instead of pulling straight out toward the lens.
- **[technical]** A dissolve overlaps clips like a cut does; lengthen the incoming clip by the dissolve
  duration or the video ends short of the music.
- **[audio]** Need more length than the track? Repeat whole bars between two measured onsets 8 beats
  apart with a 12 ms crossfade; check `ive beats` shows an unbroken grid across the splice.
- **[pacing]** Cut on the music's *accents*, not just its beat grid: measure per-beat onset strength
  (240SX track: accents on alternate beats from the drop at 3.07 s) and put the 1:1 cut on the drop.
  Vary holds (1–8 beats) - the reviewer asked for "a little longer/shorter" instead of uniform shots.
- **[match-cut]** Handheld drift after the solved frame: measure it on static background with
  `cv2.phaseCorrelate` and absorb it as camera lens shift (`shift_x/shift_y` = px / long side) instead
  of re-solving. Lets the real action play out and still cut 1:1 later in the clip.

## From the FG2 #806 photo/CGI/scan reel (2026-11-11, built by an agent)
- **[story]** "Finished photos" on Drive may be scan-product renders (FG2 F1..R3.jpg were). Look before planning;
  the real finished-car photos were on the epsilon.plus product pages (`/products/<handle>.js` lists images).
- **[story]** Product reels: only use photos where the part is in its finished state - user rejected photos with
  the lip still black/unpainted. Check every candidate photo for the part's finish.
- **[scan-look]** Put the product (lip/wing CAD or part scan) on the scan in scan shots - user asked for the lip on the scan.
- **[match-cut]** A modified race car vs a stock-state scan shares few landmarks; landmark solves stalled at 15-50 px.
  Fix: rough landmark solve -> silhouette refinement against a GrabCut mask (projects/fg2-race-car/tools/refine.py),
  with ignore boxes on shadows, wings and aftermarket mirrors. Verify with an onion render, not the score.
- **[match-cut]** For photos (stills) the 1:1 device is: one Blender still per layer from the solved camera, then
  one shared Ken Burns window applied to photo, CGI and scan (tools/kenburns.py) - the car stays locked while moving.
- **[technical]** Same car, two scan exports can be in different frames (FG2 LQ vs HQ). Use the one the CGI .blend was built on.
- **[technical]** Beat-length `dur`s drift (+40..+119 ms over 16 cuts at 75 BPM). Give clips whole-frame durs so each cut
  lands on round(beat*fps), first clip one frame short; measure cuts from frame diffs.
- **[format]** "TikTok format" = 1080x1920 full-bleed; keep the hero part above the bottom ~20 % caption zone.
- **[match-cut]** Near-planar landmarks (bumper beam, horns) let PnP flip to a mirrored pose that fits the
  points but renders the car at the wrong size. Refine from a known-good nearby camera
  (`solvePnP(..., useExtrinsicGuess=True)`) and always confirm with an onion overlay.
- **[match-cut]** When real hands are carrying a part at the cut, start the scan part *at that position*
  (`--explode` 8th field = start offset) so the part matches across the cut too, then animate it.
- **[match-cut]** Camera *height* is unobservable from landmarks on one vertical face (bumper beam, horns):
  RMSE stays flat from 0.40 to 0.55 m while the free solve wandered to 0.16 m ("too low" - reviewer).
  Lock height (sweep a few values, render onions, pick by engine-bay depth / fender tops) and solve the rest.
- **[scan-look]** Part-state composites: use the state scan *as captured* (e.g. "bumper removed") over the
  full-car scan trimmed back - reviewer preferred that to slicing a thin zone out of the state scan.
- **[story]** Dissolving a scan render into a product image: solve the product image's camera (landmarks +
  silhouette IoU on the flat background), end the orbit exactly there, and morph the material/background
  to the image's grey (`--morph-to-clay`, tuned from median luma) before the dissolve starts.
- **[technical]** Verify alignment numerically (silhouette bounds / phaseCorrelate) - a hand-made side-by-side
  overlay with a different material can look mismatched when the geometry is right.

- **[story]** Do not add a wing to the photos/CGI unless it is from the wing configurator and matches exactly  _(from fg2-race-car @ 12.7s, 2026-11-11, user)_
- **[scan-look]** Landscape photos in a 9:16 reel: user wanted a gradual zoom OUT to the whole car, not a push-in.
  Render scan/CGI on an extended canvas (same focal, wider sensor, symmetric about the principal point) and put the photo
  on a blurred, darkened fill of itself (fg2-race-car/tools/canvas.py + kb_zoomout.py).
- **[text]** Epsilon product reels end on the Epsilon+ wordmark (Drive `EPSILON+ Logos`), not the Illumaesthetic logo.
- **[story]** "CGI model" = Ecky's modelled car (smooth panels, glass, light textures; usually a .glb), NOT a .blend that
  paints the scan. FG2 Race Lip.blend / Bodykit for turn10.blend are the LQ scan in red/orange - user rejected that.
  Compare a frame of the team's CGI reference video with your render before using any .blend as "the CGI".
- **[story]** Epsilon CGI cars come from the epsilon.plus **lookbook** (game models), not the wing configurator (its
  `ewc-*.glb` are decimated scans). Path: homepage lookbook config -> `lookbook-frames-*.json` -> `lb-<car>-<key>.json`
  -> `config.model.source` (`eps-<car>-v<N>.glb`) on cdn.shopify.com/s/files/1/0036/2250/2435/files/.
  Place it in the scan frame with the shared lip/part CAD, then body ICP (fg2-race-car/tools/align_game.py).
- **[story]** Wing rule clarified by the user: wings that are part of the Epsilon **lookbook** kit for that car (e.g. the
  FG2 TC wing in eps-honda-civic-fg2-v10.glb) are fine to render. Still never hand-build or borrow a wing from elsewhere.
- **[technical]** The lookbook GLBs are also on the Epsilon drive: `Website Files/Epsilon-final-GLBs-2026-10-15.zip`
  (Drive id 12NSEcFeO3aHGYho_bt1VZNd9VHEYkAg7, 31 cars). Same files as the CDN (sha matches the lookbook JSON).
- **[pacing]** Anchor the beat grid on the **kick peak** (40-120 Hz energy, librosa peak_pick + least-squares fit), not the
  first spectral-flux onset: FG2 v1-v4 cut ~70 ms early on every beat and the user heard it ("doesn't match the music").
  Verify on the delivered file: decode its audio, find kicks, compare with frame-diff cut times (target |err| <= 1/2 frame).
- **[pacing]** Don't place cuts on a quiet pre-drop build (no hits to land on): start the video 2 kicks before the drop on a
  real percussive hit and put the transformation ON the drop.
- **[story]** Never reuse a shot/photo in one reel (FG2 v4 finale repeated the opening angle - user flagged it).
- **[story]** A white/aftermarket splitter is not the Epsilon lip - check each photo shows the actual product before using it.

## From the Huracan Evo Temerario-style scan reel (2026-11-11, built by an agent)
- **[technical]** Artec full-car exports can be tilted (~7 deg here): fit the scanned ground plane (RANSAC) and the long axis
  once on the full car, then apply that ONE rigid transform to every part scan before crop/prep (huracan-evo/tools/level.py).
- **[technical]** Check part registration numerically before an exploded view: nearest-neighbour distance part->car at 8 mm
  (median 2.5-3.4 mm = registered) + an ICP dry run (huracan-evo/tools/regcheck.py). Hidden parts (cowls) check against
  the state scan that exposes them.
- **[technical]** "All Parts Removed" scans can be partial (no roof, hood propped). Base = full car minus triangles within
  6 mm of any part scan + APR triangles >6 mm from the trimmed car (tools/composite.py).
- **[scan-look]** Hood opening: fit the hinge (axis + angle) mapping the closed hood scan onto the captured open hood
  (tools/hinge.py, 2 mm median) - physically right motion for free.
- **[scan-look]** Dark rims are often not captured (tyre rings only). Don't frame a wheel close-up on them; use a
  wheel-off state scan (brake disc/caliper/hub) at 2 mm for the "extreme close-up" beat.
- **[scan-look]** Exploded views in 9:16 stack panels ABOVE the car (Temerario 25-31 s); flying bumpers along the car's
  length leaves the frame.
- **[technical]** Cycles `use_persistent_data` dropped ALL lights mid-sequence when objects animated (hinge AND plain
  translate). Off for animated-part shots; scan every frame's max luma before assembling.
- **[technical]** `minterpolate` turns N frames into 2N-3: set `src_fps = 30*N/(slot+4)` or every shot ends on 3-4 cloned frames.
- **[audio]** `alimiter` auto-levels by default (`level=disabled` to stop it silently lowering the whole mix).
- **[audio]** Voice-over requests that name a real narrator ("use the same lady's voice"): don't clone a real person's voice;
  use a preset voice in the same delivery and say so. Spec lines in narration follow the text rule: sourced numbers only.

## From the A90 Supra Temerario-style scan reel (2026-11-11, built by an agent)
- **[technical]** Registration check that works for state scans: render the part in red over the silver car (tools/regcheck.sh in
  projects/a90-supra). Red/silver z-fight patches = same surface = registered. Trimmed ICP that doesn't lower the residual means
  the part is already in frame (its "shift" is sliding along the skin) - don't apply it.
- **[technical]** Scans from other sessions/years are often in their own frame: FPFH+RANSAC+point-to-plane ICP (open3d,
  a90-supra/tools/globalreg.py) - trust it only when several tries return the same pose (2024 A90 trunk: 4/4, rmse 4.4 mm);
  fitness < 0.1 or a different pose per try = not usable (2021 A90 corner fragments, headlight units).
- **[scan-look]** Exploded view in 9:16: put the car's length along the frame height (high side camera ~60 deg down, up vector
  = nose) and *tip* bumpers 90 deg about the width axis so the scanned inside faces the lens. Z-spins of 1.8 m bumpers hit the car.
- **[technical]** Cycles can return a run of completely unlit frames mid-animation (A90 s08 frames 56-70, luma 5 vs 48); a
  stride contact sheet can miss it. Scan every frame's mean luma before assembling; re-rendering those frames fixed it.
- **[technical]** To nudge a motion hit by a few frames, change the PNG sequence's `src_fps`, not `speed:` - speed resamples
  after minterpolate and duplicates a frame. `ive strip` shows the frame after the requested time at a cut; use
  `ffmpeg -vf select=eq(n\,N)` for exact cut frames.

## From the Ferrari 296 GTB scan-only reel (2026-11-11, built by an agent)
- **[technical]** Cycles persistent data can silently render BLACK frames in long, heavy animated scenes (296 explode:
  8M tris + 7 moving parts, from frame 49 on; frames got 2x faster and showed only a dark silhouette). Scan every render
  for max luma before assembling and re-render in fresh 40-frame processes (`projects/ferrari-296/tools/shot.py` `frame_range`).
- **[technical]** In custom Blender scripts call `view_layer.update()` after linking objects from a .blend before reading
  `matrix_world`/bboxes - otherwise pivots land in raw-mm space and any rotation flings the part out of frame.
- **[scan-look]** Panels-off bodies from Artec state scans: delete car triangles within ~9 mm of each removed panel, then
  add only state-scan geometry > 7 mm from the car, inside that panel's own bbox, de-duplicated across fills
  (`tools/composite.py`). Drop z above the car where a state scan caught a propped-open hood.
- **[scan-look]** Tail-lamp lenses and grilles are often scan holes; check close-ups for dark blotches and pick another detail.

## From the MR2 SW20 scan-process reel (2026-11-11, built by an agent)
- **[technical]** Car on stands: huracan `level.py` RANSAC locked onto the cabin floor (~350 mm above the real ground).
  Check a z-histogram of up-facing tris before cropping; refit on the true floor (toyota-mr2-sw20-scan-process/tools/relevel.py).
- **[technical]** `ive prep --drop-islands` OOM-killed Blender on an 8M-tri mesh; do islands in numpy first (tools/islands.py) and prep plain.
- **[match-cut]** Pick the scan state per *clip*, not per day: the same afternoon had doors on/off and T-tops on/off in different clips.
  Diff two state scans (tools/diffparts.py) to get the removed panels, then add/remove them to build the exact part-state composite.
- **[match-cut]** Cabin / over-the-roof views of a stripped car are a trap (closed sprayed-glass box, near-planar, ambiguous openings);
  an exterior frame with fuel door, side intake and quarter window solved in minutes. An edge-chamfer pose fit on cluttered frames
  jumped to a wrong minimum - only use it with small local steps from a known-good pose.
- **[text]** Door scans can be inner-face only (render from outside: you see the inner panel mirrored). Claim "inner door panels", not inside+outside.
- **[technical]** With music starting mid-track the first clip still needs to be one frame short (measured: every cut +1 frame otherwise).
## From the C5 Corvette scan-process reel (2026-11-11, built by an agent)
- **[story]** Dropbox dumps can mix cars: 'Corvette Footage' Jul 15-16 clips are a red MR2. Sheet every clip and check the car before planning.
- **[story]** Footage may post-date every scan (C5: Jul 2025 widebody prototyping vs 2023/2024 stock scans). Use only the frames where the car is in a
  scanned state (here the Jul 17 outdoor teardown), and say plainly when a requested beat (handheld scanner) does not exist in the dump.
- **[text]** ScanHUD `counter` eases with Easing.out(exp) and stops at 99.9 % of the value (8,255,611 showed as 8,247,549). Until it is fixed,
  show exact counts with a `label`, and read the final frame of every HUD number.
- **[technical]** Part-state scans from a later session can still share the Artec frame (C5 2024 parts vs 2023 car: ICP moves <7 mm). Check
  before registering; FPFH global registration failed on a hood-open scan with little overlap.
- **[technical]** State-scan composites: drop state triangles above the full car's top surface (re-fitted panels duplicate as ragged shells),
  below ~100 mm (ground), and inside a box around any re-steered wheel.
- **[match-cut]** To end on a listing hero, fit the end pose by silhouette bbox/IoU against the WebZoom frame-0 image (render at 25 %, 4 spp,
  ~5 tries), then render the last frames in clay with exposure tuned to the hero's grey and crossfade x-ray -> clay before the dissolve.
- **[pacing]** Tracks with a long kick-less intro: start the music 4 beats before the drop rather than cutting on the empty intro.
## From the Honda S2000 AP1 scan-only reel (2026-11-11, built by an agent)
- **[technical]** `ive assemble` builds a hard cut as a 1-frame xfade over a cloned hold frame: the frame at every cut
  repeats clip A's last frame and drops clip B's first (frame diff 0.0 just before each cut). For cut-only reels use
  `projects/honda-s2000/tools/concat_assemble.py` (exact `frames:` per clip, plain concat, cut k = sum(frames[:k])).
- **[technical]** Cycles `use_persistent_data` lost all lighting mid-animation on a 4-object exploded shot (frames 17-211
  rendered as black silhouettes, 4.4 -> 1.7 s/frame); the same frame rendered alone was fine. Check every render dir for
  dark frames (median-luma test) before assembling; turn persistent data off for long multi-part animations.
- **[technical]** A `while pgrep -f render_all.sh` waiter matches its own command line and never fires. Chain queued jobs
  in one script instead.
- **[pacing]** Breakbeat tracks fool `ive beats`: it reported 92 BPM (0.650 s) for a 138 BPM track (kicks/sixteenths every
  0.217 s). Fit the grid to kick-band peaks (tools/music_grid.py) and check the period against the onset spacing.
- **[technical]** State scans in their own Artec frame with scanned floor: remove the floor plane first (tools/deground.py),
  then FPFH+RANSAC, then ICP restricted to rigid panels that did not move (hood/fender tops) - fitness went 7 % -> p50 1.5 mm.
  A bumper refitted between sessions sat 25 mm off: never splice the full car's bumper next to state-scan geometry.
- **[technical]** Cutting panels from a full car: trace the seams on a 2 mm near-ortho top render (focal 200 mm at 25 m) and
  cut by polygon + topmost-skin; for lids that are open in a state scan, keep only triangles missing from that scan.
  Diffing against a partial state scan alone grabs neighbouring panels.
- **[scan-look]** A car scanned without wheels: frame 3/4 at 1.2-1.6 m, not the reference's low side profile - low views make
  the empty arches the subject. Don't add wheels from single-corner state scans.
- **[scan-look]** Exploded panels seen from a level camera read as slivers; look down ~30 deg and tilt each panel toward the lens.
## From the GT3 RS (992) scan-process reel (2026-11-11, built by an agent)
- **[story]** Footage may arrive mid-session in a *different* Dropbox folder than the brief names (here `1. Video dumps/992 GT3RS scanning`,
  uploaded from the user's phone). Before stopping for "no footage", search Dropbox for `scanning` folders and re-list after the user uploads.
- **[technical]** Blender lens shift with sensor_fit HORIZONTAL is in units of the frame **width** (measured: shift 0.05 = 54 px on a
  1080-wide frame, both axes): cx = W/2 - shift_x*W, cy = H/2 + shift_y*W. Not the long side.
- **[match-cut]** iPhone shop clips can be the ultrawide lens: both solves landed on 16-18 mm (20.25 mm sensor), not 28 mm. Fix focal
  to the first good solve for the second clip from the same session.
- **[match-cut]** For a close, wide side shot, get 3D landmarks by raycasting a plain side-view render of the scan (easy to read), not a
  guessed perspective view; then PnP. Pick the frame that shows the most rigid features (wheel, intake, handle, mirror, wing tip).
- **[scan-look]** Car state at the cut: the car was on a lift with the front wheels off - remove the wheels from the scan (connected
  components) for every shot after the cut, and bring them back as parts in the reassembly if the end card shows them.
- **[technical]** Shell args like `--look-at -0.4,...` are parsed as flags by argparse: use `--look-at=-0.4,...`.
- **[pacing]** Measured: first clip one frame short (dur - 1/30) makes every cut land on round(t*30) exactly; without it all cuts were 1 frame late.
- **[story]** Don't show a part coming off (exploded bumper etc.) unless it was physically removed on the car AND we have a separate scan of it in that state - we never pulled the EK bumper  _(from honda-civic-11-scan-process @ 9.8s, 2026-11-11, reviewer)_
## From the GR Corolla scan reel (2026-11-11, built by an agent)
- **[technical]** Cycles animation renders (persistent data, many keyed parts) can go black from some frame on, deterministically,
  while the same frames render lit as stills (GR Corolla explode: frames 134+ after every part locked). Check per-frame mean
  brightness of every render folder; re-render a dark tail via the `frames` list in tools/shot.py.
- **[scan-look]** No separate panel scans? Cut hood/fenders/doors/hatch from the full car at seams read off mm-grid splats
  (projects/toyota-gr-corolla/tools/panels.py) and put a registered stripped-shell state scan underneath - lifting a panel
  then reveals real scanned structure. "Car minus stripped chassis" is not a usable split (the shell's skin differs).
- **[scan-look]** Missing wheels in the full-car scan: look for them in registered state scans (GR Corolla 'rear' had the
  real rear wheel) and splice only the wheel boxes (tools/wheelfill.py) before calling them unscanned.
- **[pacing]** Generated hyperpop track = 140 BPM; `ive beats` reports the half-time 69.8. A no-kick build can carry slow
  turntables on its phrase lines; put the transformations on the drops.
- **[audio]** Trending + licensed music: TikTok Commercial Music Library via the Higgsfield `tiktok_music_trending` tool
  (connected account). Phonk tracks (e.g. FREAKED OUT, 85 BPM) give a snare every 2 beats = a hard cut every 1.41 s.
  Fit the grid on snare hits, not the beat tracker (175 ms rms vs a few ms). Start right before a stop/silence so the
  drop lands just ahead of the first 1:1 cut. Attach the same sound in TikTok when posting (the export carries it as a guide).

- **[scan-look]** Don't spin or flip parts unless the move is there to show the viewer the backside; a spin for its own sake is pointless  _(from c5-corvette-scan-process @ 14.5s, 2026-11-11, reviewer)_
- **[technical]** (c5-corvette) scipy cKDTree queries for points far from the cloud are very slow (minutes) unless you pass
  `distance_upper_bound=<mm>`; any registration/segmentation script that queries a whole car against a part should bound it.
- **[technical]** (c5-corvette) Symmetric panels (removable roof, hoods) defeat FPFH+RANSAC (the targa slid down the
  windscreen). Seed ICP at the panel's approximate home with 8 yaw/flip variants, coarse->fine, keep the best fitness
  (`projects/c5-corvette/tools/fitpanel.py`). Check every part in red over the silver car before animating it.
- **[scan]** (c5-corvette) An "open hood" state scan rotated shut looks patchy; build the closed hood from the full car's own
  hood skin + the open scan's underside (`tools/hoodcombo.py`), and fit the hinge to the open state (`tools/hinge.py`).
- **[story]** (c5-corvette) Exploded views from "... removed" state scans leave a frayed composite (trim lines where the parts
  meet). Once the last panel is home, swap to the clean full car ON a kick (all scans share one frame) so the last frame before
  the logo is clean.

## From the NA Miata "Grimace" / stock NB chassis-scan reel (2026-11-11, built by an agent)
- **[story]** The car in the brief may not be the scanned car: Grimace's cage ruled it out of the flex test, so the team
  scanned a stock NB. Read the team's rough cut/PDF titles before planning; tell the parent/user and get the story OK'd.
- **[story]** When raw scanning clips are missing, a team rough cut can be the source (user approved), but only spans with
  no burned-in subtitles/section titles; slide the 9:16 crop window to dodge corner titles (crop x0 per shot).
- **[match-cut]** Landscape source -> 9:16: solve on the full 16:9 frame, then build a crop camera (fx scaled, lens shift).
  Blender lens shift is in units of the sensor-fit dimension (HORIZONTAL -> output WIDTH), not the long side
  (na-miata-grimace-scan-process/tools/cropcam.py).
- **[match-cut]** Very close ultra-wide frames (camera ~1 m from the bumper) didn't solve below ~27 px; pick a calmer frame
  with the car whole in view and normal perspective.
- **[scan-look]** A part that only exists in one state scan (strut bar) = ICP the two state scans (PCA coarse + trimmed
  ICP, 3.6 mm median) and keep triangles >12 mm from the other state, largest voxel cluster (tools/icp.py, diffpart.py).
  Silver part on a silver engine bay disappears: lift it above the bay so it silhouettes on black.
- **[technical]** `--morph-to-clay` with `--look silver` does not change the camera background (keys the studio env node);
  grade the end frames in post instead (tools/greygrade.py, medians: render bg 7/car 214 -> listing 57/148).
- **[technical]** Check ReadNotifications early and after each long step: the music and parent instructions arrived an
  hour before they were read.

## From the Mazda 3 (gen 4) scan reel (2026-11-11, built by an agent)
- **[pacing]** `ive beats` can lock onto 1.5x the beat on ambient tracks (Mazda track: 73.8 BPM reported, real 110). Check that the
  strong onsets sit on a lattice that divides the claimed period; fit the grid to kick peaks (projects/mazda-3-gen4/tools/music_grid.py).
- **[technical]** Part STLs in a car's "CAD" Drive folder can be scans in **inches** in their own frame (Mazda trim/spoiler: 44-50 units
  wide). Check the bbox before decimating (a 1.5 mm cell collapsed them to <1k tris); scale x25.4, then FPFH+RANSAC+ICP.
- **[technical]** A "panel" scan may be the same part as another scan (Mazda "Hatch Upper Trim Panel" = the Rear Wing, fit 0.96, 93 %
  coverage). Measure coverage both ways before showing two parts in an explode.
- **[technical]** Composite fills under a thin bolt-on part (wing on a hatch): compare the state scan against the car *with the part
  already removed* and use ~1.5 mm, not 6-7 mm against the uncut car - otherwise the mount surface comes out as black holes.
- **[technical]** Cars scanned on jacks: the jack is part of the scan and `ive crop` keeps it (inside the footprint). Drop tris below the
  sill height outside the wheel bands (projects/mazda-3-gen4/tools/clean_car.py) and check a low side render.
- **[technical]** To preview while a final render runs without overlapping heavy jobs: `kill -STOP` the Blender pid, preview, `kill -CONT`.
- **[pacing]** Rotations are again wasted: the turntables/orbits (s1 front turntable, s2 rear orbit, rotating top-down, the s8 orbit) spend screen time without showing anything new. Don't fill time with camera rotations  _(from mazda-miata-nc, 2026-11-11, user)_

- **[story]** If you do a front bumper removed shot, focus on the front bumper (camera framed on the front while it comes off), THEN move on to the rear. Don't show every part separating at once in one wide orbit  _(from mazda-miata-nc @ 18.7s, 2026-11-11, user)_

- **[scan-look]** Only spin an exploded part when its backside is useful (scanned inside / mounting side worth showing); otherwise just translate it  _(from porsche-gt3rs-scan-process, 2026-11-11, reviewer)_

- **[scan-look]** A part being removed is hard to see when the rest of the scan is behind it - move parts out into clear background, not across the body  _(from porsche-gt3rs-scan-process, 2026-11-11, reviewer)_
