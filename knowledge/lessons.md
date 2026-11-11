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

- **[story]** Same issues as the other first revisions - learn from them and make the same updates (sibling v1 notes: opening too cropped; exploded view too wide, doesn't zoom in on the part assemblies; last scenes held too long; follow the Temerario: progressive explode over several angles, fade, small logo)  _(from toyota-mr2-spyder, 2026-11-11, reviewer)_
- **[story]** Same issue as the other first drafts. Need to focus more specifically on the removed areas and where the useful data is  _(from c5-corvette, 2026-11-11, reviewer)_

## From the Mazda Miata NA scan reel (2026-11-11, built by an agent)
- **[technical]** A long single-process Cycles render with animated parts can go black mid-shot and stay black
  (Miata s8: luma 32 -> 6 from frame 57 on, persistent data). Check per-frame mean luma after every final render;
  re-render bad ranges in fresh processes (projects/mazda-miata-na/tools/rerender.sh, 25-frame chunks) and re-check.
- **[technical]** Fitting a lid hinge to a *partial* open capture: measure open -> rotated-closed distance (every captured
  point must lie on the lid) and keep the axis along X; a free axis with closed -> open cost tilted 19 deg. Verify by
  rendering the rotated lid over the open-state scan (tools/hinge.py, tools/lidfull.py).
- **[scan-look]** Scans can carry a real, legible licence plate - look at the tail close-up and flatten the characters
  onto the plate plane (tools/deplate.py) before rendering anything near it.
- **[pacing]** A kick pick can lock onto an off-beat bass phase. Fold the band energies (sub / snare / hats) over one beat
  period and anchor the grid where they coincide; verify cut-to-kick error on the delivered file.
- **[text]** ScanHUD counter (Easing.out(Easing.exp)) never reaches its value - it stops at 99.9 % (14,999,999 shows as 14,985,351; 240SX's 24,991,097 would show as 24,966,692). Use a label for exact counts or fix the easing  _(from toyota-sera-scan-process, 2026-11-11, agent)_

## From the Toyota Sera scan-process reel (2026-11-11, built by an agent)
- **[technical]** Sony FX30 footage is S-Log3 / S-Gamut3.Cine 4:2:2 10-bit (XML sidecar), not HLG - `ive` does not tonemap
  it. Grade with a generated LUT (projects/toyota-sera-scan-process/tools/slog3_lut.py: legal-range decode -> S-Log3
  inverse -> SGamut3.Cine->709 -> Hable -> 709 OETF) and crop 16:9 to a 9:16 window per clip (tools/irl.py --last N
  trims the START so the clip still ends on the solved frame). FX30 XMLs name the lens but record no focal length.
- **[technical]** The environment allowlist has a size cap; per-link Dropbox hosts fill it. Ask for `*.dl.dropboxusercontent.com`
  in Settings up front, and don't race sibling sessions editing the same environment.
- **[match-cut]** A cropped 9:16 window of a 4K frame is a telephoto camera (Sera front: ~14 deg FOV). A 1.6 m bumper
  cannot explode inside it and a pull-back with the large lens shift drifts the car out of frame - hold the 1:1 bay for
  2 beats, then cut on an accent to a wide 3/4 for the explode.
- **[match-cut]** Gradient-correlation pose refiners on a splat render will "improve" the score with a degenerate pose
  (14 deg roll, camera at 0.34 m). Constrain to small local steps or don't use; the onion is the judge.
- **[scan-look]** State scans can carry unrelated changes (Sera 'Rear Bumper Removed' was captured with the hatch open and
  tail lights out). For the x-ray reassembly, cut the bumper surfaces out of the clean full car instead (triangles within
  12 mm of the part scans, tools/trim_by_parts.py) so the end frame is the closed car the listing shows.
- **[story]** The listing hero may not be exactly recoverable from the scan (Sera: front/roof align but the rear wheel
  ghosts ~70 px whatever the camera). Score candidates by gradient NCC inside the car, not silhouette IoU (IoU was flat
  0.84-0.87 across very different cameras).
- **[scan-look]** Same issue as other first drafts: too much of the car is cropped. This is just a standard full car scan - show the whole car  _(from mazda-3-gen4, 2026-11-11, reviewer)_
## From the Infiniti G35 scan reel (2026-11-11, built by an agent)
- **[technical]** Blender 5.3 Cycles + `use_persistent_data` can silently drop every light partway through a long animation
  (G35 s8: frames 53-122 rendered as a black silhouette, frame time fell 10 s -> 6 s). Always scan each finished shot's
  per-frame mean luma for a step jump before assembling; re-render the bad range in a fresh process with persistent data off.
- **[pacing]** `ive beats` can report half tempo (G35 track: 60 BPM reported, 90 BPM real). Confirm from 40-120 Hz kick peaks.
- **[scan-look]** No part/"removed" state scans for the body? Cut panels from the full-car scan along the visible seams
  (near-orthographic renders at a known mm/px give the seam coordinates) and keep every piece in one `--like` frame.
- **[story]** A team long-form edit may be used only as the source of the IRL shot that cuts 1:1 into the scan - no other shots from it in the reel  _(from na-miata-grimace-scan-process, 2026-11-11, reviewer)_
- **[pacing]** (honda-s2000 reviewer: "beginning is great, last scenes held too long") A 13.9 s exploded view + 3.6 s logo
  after a front half of 1.7-3.5 s shots felt held. Keep the back half on the same 4-8 beat rhythm: cut the explode into
  angles that each render a window (`t0`) of ONE part animation so the panels stay continuous across cuts; logo ~2.4 s.
- **[pacing]** Shot lengths in frames must come from round(beat_time*fps) per cut, not a repeated 52/53 pattern - at
  138 BPM (13.04 frames/beat) hand-alternating drifted to +38 ms by the fourth cut.
## From the Nissan Frontier Pro-4X scan reel (2026-11-11, built by an agent)
- **[technical]** `ive crop` measures its footprint on the body and clipped both mirrors on a wide truck (|x|<991 mm vs mirrors
  at 1084). For a car on a lift (no wheels, pads under the frame) a plain height cut above the pads (z>200 mm levelled) +
  a generous |x| limit was cleaner (projects/nissan-frontier/tools/clean.py). Always compare bbox widths before/after a crop.
- **[technical]** State-scan names are ambiguous: Frontier "Front Bumper Removed" is the removed *bumper*, not the truck
  without it. Render every state in silver before planning.
- **[technical]** No part scan for a panel? Derive it: full-car tris far (>12 mm) from the "... removed" state, limited to
  the panel's shut lines (top heightmap). For thin add-ons (fender flares) also require the state to have geometry within
  ~90 mm (the body under the flare), else every small door/bed offset becomes "part" (tools/derive.py, parts.py).
- **[technical]** librosa is not installed; projects/nissan-frontier/tools/accents.py does the kick-peak grid, per-beat
  kick/flux/RMS table and the music-end level curve with numpy + ffmpeg.

- **[audio]** Don't reuse music other agents/reels already used - check projects/*/project.yaml and editlogs for the track (title / song_clip_id) before picking  _(from honda-civic-11-scan-process, 2026-11-11, reviewer)_

## From the Lexus IS350 scan-process reel (2026-11-11, built by an agent)
- **[technical]** Shop footage can be **Sony FX3A S-Log3 / S-Gamut3.Cine** (read the XML sidecar `CaptureGammaEquation`; the
  brief said FX30). `ive probe` reports it as plain Rec.709, so nothing tonemaps it. Build a .cube with colour-science
  (S-Log3 decode, S-Gamut3.Cine->709, Hable, 709 OETF) and apply it before cropping (projects/lexus-is350-scan-process/tools/irl.py).
- **[match-cut]** Sony XML/rtmd hold no focal length for the FE 24-70 GM II zoom. A free PnP with points spread in depth
  (plate corners + both mirror tips, or plate screws + exhausts + diffuser fins) solved 31-33 mm on the 35.6 mm sensor; verify with onions.
- **[match-cut]** 16:9 footage in a 9:16 reel: solve on the landscape frame, then make the crop camera (sensor = 35.6 x window/W,
  same focal, window offset as lens shift). **Blender shift is a fraction of the image WIDTH when sensor_fit is HORIZONTAL**
  (as in scan_render) - dividing by the long side left the scan 46-121 px off. Verify numerically (phaseCorrelate render vs crop).
- **[match-cut]** With a large lens shift, push/pull moves zoom toward the off-frame optical centre and slide the car out of
  frame; use rise/orbit or a custom two-camera path (tools/path_render.py) instead.
- **[scan-look]** A small part (11 cm reflector) is ~20 px in a full-car shot: start close (S2's last pose) and swoop out to the
  wide/listing pose while it flies home, and pop it into black space, not over the silver body.
- **[technical]** Artec full-car frames can be tilted/yawed (IS350: 3.5 deg, 9 deg): level with huracan-evo/tools/level.py
  before ive crop, or a ground flap survives in front of the bumper.
- **[technical]** Splicing a state scan by bbox+40 mm exposed a black coverage hole; splice by surface distance instead
  (drop full-car faces <8 mm from the part scan, add state faces >8 mm from the remaining car).
- **[story]** If the footage has no removal for the part-state scans, say so in the review; don't fake one.
- **[technical]** The listing's 360 viewer canvas has a flat dark background: a luminance-threshold mask + silhouette refine
  solves its camera to 0.3 px; GrabCut grabbed background there.
- **[text]** ScanHUD's `counter` eases with Easing.out(exp) and stops at 99.9 % of `value` (24,999,992 displayed as 24,975,578;
  the 240SX reel showed 24,966,688 for 24,991,097). Until the component is fixed, pass value/(1-2^-10) and check the final frame.
- **[technical]** A render queue that waits with `pgrep -f <shot name>` also matches your own watcher loops; wait on the PID.
## From the Infiniti QX80 scan reel (2026-11-11, built by an agent)
- **[technical]** Hood from a "hood open" state scan: fit the hinge (projects/infiniti-qx80/tools/hinge.py), then make the hinged
  part = state-scan panel rotated closed + the full car's own hood skin (tools/hood.py). The closed pose is then identical to
  the full car and opening reveals the state scan's real under-hood capture.
- **[technical]** Drive part names lie: QX80 "Fender Inner" is the clean full fender panel, "Front Bumper Duct" is a bumper corner.
  Render every part alone before choosing explode panels. A part with a small median distance but ~1 % overlap
  ("Rear Bumper Inner", floating mid-car) is NOT registered - check overlap %, not just the median.
- **[technical]** Render-queue waiters: `while pgrep -f render_queue.sh` also matches other waiters whose command line contains
  that string - two waiters deadlocked. Wait on a PID (`while kill -0 $pid`) or a log line instead.
- **[scan-look]** Large SUV in 9:16: a 3/4 turntable at 5.4 m / 30 mm cropped the grille; 6.2-6.6 m with the target moved
  ~1 m toward the end you want to show (nose for front 3/4, tail for rear 3/4) keeps the face in and crops the other end.
- **[story]** Lookbook models carry several versions of a part (GR Corolla: front_lip / front_lip_v2 / front_lip_2025,
  side_skirts / side_skirts_v2...). The lookbook's default kit is not necessarily what the photo car runs - match each
  part version to the photos (GR Corolla photo car = Front Lip V2) and confirm with the user when unsure.

- **[scan-look]** Rear trunk data is made-up. If there's no actual trunk open scan, don't cut it incorrectly  _(from honda-s2000 @ 15.7s, 2026-11-11, user)_
- **[story]** (honda-s2000) A file named like a state ("S2000 trunk.stl") is not proof of an open-state capture. v1-v4 opened
  the trunk and floated the lid from it; the reviewer called it made-up. Only animate a panel open/off when a scan of that
  exact state of THIS car exists and you have confirmed what it shows (ask if unsure); otherwise keep the panel shut.
## From the Subaru STI GD blobeye scan reel (2026-11-11, built by an agent)
- **[technical]** Look for an `Aligned ...` folder next to the scans: it may hold a level, nose-forward copy of the car
  (STI: `Front bumper/Aligned for Splitter`). Register the hi-res car onto it (FPFH+RANSAC+ICP, 1.4 mm) instead of hand-levelling.
- **[technical]** State scans from older sessions may carry a different bumper/lip: fit their ICP only on rigid shared panels
  (hood/fenders, `refine.py --box`) and use ONE correction for every scan of that session (cross-check the residual table).
- **[scan-look]** When a part scan doesn't match the car's own panel, carve the panel from the full car (car tris > 12 mm from the
  matching "removed" state, largest island) - it seats exactly on reassembly. Fill each opening only with its own state scan, in its own box.
- **[technical]** 15 fps renders + minterpolate leave a 3-frame freeze at the end of every clip (N frames carry (N-1)/15 s and the filter
  drops ~2 tail frames). Set `src_fps = (N-1)/(dur + 3/30)` or render 3 extra frames; check frame diffs before each cut.
- **[text]** Scans capture licence plates legibly - check rear/front plates at full res in every rear shot; flatten them with a deplate
  pass (infiniti-g35 / subaru-sti-blobeye tools/deplate.py) and frame close-ups to keep plates out.
- **[pacing]** Generated eurobeat with a constant rolling bass: no kick drop to cut on - find the lifts as per-bar brightness steps
  (2-6 kHz / 6-11 kHz band energy) and put the hood opening / separation on them.

- **[technical]** All V1 reels get the same edits: lighting-dropout check (per-frame luma scan, render with persistent data off) and cut timing measured against the decoded audio  _(from subaru-wrx-va, 2026-11-11, user)_

- **[story]** Shot order is determined by each car's scan features (what was scanned: parts, open/removed states, signature features), not by a fixed template; a scene-director agent (.claude/agents/scene-director.md) directs the scenes  _(from subaru-wrx-va, 2026-11-11, user)_

## From the Toyota Sera scan reel (2026-11-11, built by an agent)
- **[scan-look]** Opening panels from state scans: fit the hinge (any axis) that swings the full car's closed panel onto the
  open capture (toyota-sera/tools/hinge_fit.py; works for butterfly doors - the two door fits came out mirror-symmetric).
  The panel = car triangles that land on the open capture, plus the open capture's inner side swung back closed.
- **[scan-look]** When taking a panel's inner side from the open capture, keep only triangles that sit *below* the closed skin
  after the inverse hinge, and let closed-panel candidates land loosely (30 mm): otherwise the capture's own outer skin pokes
  through the closed hood and skin strips stay behind on the base as the hood lifts. Check frames mid-swing at final quality.
- **[scan-look]** A "door open" state may have BOTH doors open - fit and animate both, or the far door shows open in the closed frame.
- **[technical]** Drive state scans can be byte-identical under two names (Sera 'Rear Bumper Removed' = '... No Tail Lights'); md5 first.
- **[scan-look]** Licence plates aren't in bumper part scans: when removing a bumper for an exploded view, also drop car triangles
  inside the bumper's bbox that the bumper-removed state doesn't have, or the plate floats in the base.
## From the Mazda Miata ND Temerario-style scan reel (2026-11-11, built by an agent)
- **[technical]** Artec exports can be upside down (Miata: ground at +Z, car hanging below, long axis X). Look at three
  orthographic projections of the 6 mm decimation before levelling; flip 180 deg about X, then RANSAC-level (mazda-miata-nd/tools/level.py).
- **[scan-look]** No isolated hood/trunk scan? Cut the panel out of the full-car skin along its shut lines, traced on a
  near-orthographic top render (tools/extract.py), and fit the hinge from the state scan that captured the panel propped open
  (tools/hinge.py: the open panel = state triangles above the car's roofline; hood 3.0 mm median). Distance diffs vs state scans
  are NOT a clean panel mask: wheels/fenders differ by >12 mm when the car was on stands for the state capture.
- **[technical]** Never key a camera straight overhead: `to_track_quat('-Z','Y')` loses its up vector and the image rolls ~90 deg
  in one frame (Miata s7 v1, just before a cut). Approach top-down from one side, ~10-15 deg off vertical.
- **[story]** Check licence plates in close/rear shots at final res: the Miata scan's plate characters were readable. Flatten the
  embossing onto the plate plane in every scan that carries it (tools/flatten_plate.py) instead of blurring the video.
- **[pacing]** `ive beats` BPM can be off enough to drift a quarter second over 30 s (said 117.5, kicks are 116.01). Fit the
  grid to all kick peaks iteratively (index on current grid, least-squares refit; tools/music_scan.py) and check the residual (1.5 ms).
- **[pacing]** A generated track with an 8 s pad intro: start the music 8 beats before the first kick, carry the intro with one
  slow turntable and put the first cut ON the first kick; end the logo on the last hit and let it ride the decay.
## From the Suzuki Cappuccino scan reel (2026-11-11, built by an agent)
- **[technical]** Long sequential `shot.py` renders with keyframed part pivots can lose ALL lighting part-way (luma drops to 0 from
  one frame to the next, ~40-55 frames in; s06/s09/s10/s11). The same frames render fine with `--frames` in short runs.
  Scan every render dir for per-frame luma before assembling - first/mid/last contact sheets miss it.
- **[technical]** `type: cut` compensation in `ive assemble` clones the outgoing clip's last frame -> a duplicate frame before every
  cut. Workaround: `transition: {type: fade, duration: 0.0333}` (still a hard cut) and give each outgoing clip one extra real
  frame in `dur`. Same cut timing, no dup (verify with frame diffs).
- **[match-cut]** State scans with a lid propped open often capture only a sliver of the lid (Cappuccino hood 9k tris). Cut the closed
  lid from the full car (car tris the open state lacks, clipped at the shut lines) and fit a hinge to the sliver (one-sided distance,
  open-lid points -> moved lid); confirm with a side-view splat. Gives a real opening motion from partial data.
- **[pacing]** Generated tracks: `ive beats` reported 63 BPM for a 126 BPM track (half-time) - fit the grid to kick peaks; and
  measure the end from the RMS envelope (file 40.05 s, music gone by 38.9 s).

- **[scan-look]** CROPPING: frame every shot on its subject with deliberate margins in 9:16 - whole car fully in frame on wide shots, the named section filling the frame on detail shots; nothing clipped by accident (wheels, bumpers, wings, roof); no dead black where the subject should be. Check a contact sheet of the FIRST, MIDDLE and LAST frame of every shot before assembling.  _(from ferrari-296, 2026-11-11, user)_

- **[story]** REDUNDANCY: each section of the car (front, side, rear, top, engine bay, wheels...) appears in ONE continuous sequence only; two shots of the same section get merged or one is cut. Run python -m ive director, remove every repeated view it flags, and list in direction.md which section each shot covers.  _(from ferrari-296, 2026-11-11, user)_

- **[story]** BUMPER-REMOVED DATA IS THE HERO BEAT: where a bumper-removed / front- or rear-end-removed state scan exists, give it its own section - the bumper comes off and the camera moves in on what is behind it (crash beam, mounts, brackets, wiring, ducts), held long enough to read, with a short factual on-screen label (e.g. FRONT BUMPER REMOVED, CRASH BEAM, MOUNTING POINTS) over scan shots only, wording backed by the scan files.  _(from ferrari-296, 2026-11-11, user)_

- **[story]** OPENINGS ONLY FROM DATA: show a trunk, hood or door open (or a part removed) only if a scan of that state of THIS car exists and registers. Never fake an opening by animating the closed scan; no trunk-open scan means no trunk shot.  _(from ferrari-296, 2026-11-11, user)_
## From the Lamborghini Revuelto scan reel (2026-11-11, built by an agent; not yet reviewed)
- **[technical]** Low parts (side skirts) die in `ive crop` (bottom-22 cm up-facing rule) and in prep's "island never
  above 15 cm" rule - for those use only a floor cut (z < 8 mm in the levelled frame) and prep without --drop-islands.
- **[scan-look]** Part scans can carry big patches of the surrounding body (Revuelto "Side Mirrors" = mirror + door/window
  skin). Trimming the car with them leaves a jagged hole; crop the part to the part itself before compositing.
- **[scan-look]** At-home shots: render the raw full car + every part at home (coincident surfaces share one material,
  so no seams, and the part scans fill the car's uncaptured dark trims); switch to the trimmed base only on the frame the
  first part starts to move (`visible` windows in tools/shot.py).
- **[pacing]** `ive beats` BPM can be ~1 % off on generated tracks (103.4 vs 102.52 -> 85 ms drift in 16 s). Fit the grid
  to strong flux onsets on a 16th grid (projects/lamborghini-revuelto/cuts.json note) before placing cuts.

## From the Porsche 911 GT3 RS (992) scan reel (2026-11-11, built by an agent)
- **[technical]** The GT3 RS full-car STL came with the ground tilted 3.4 deg and the car diagonal in X/Y. Level once
  (huracan-evo `tools/level.py fit`) and apply the same `level.json` to every part STL before `prep --like`; the Artec
  part exports then z-fight with the car without any ICP.
- **[technical]** Drive "Underbody" scans are a separate session/frame (ICP shift 2-4 cm); "DRS Open" vs closed showed
  no wing change (<8 mm). Measure a state difference before planning an "opens" beat around it.
- **[technical]** Long serial render queues die when the session idles/disconnects. Render with
  `use_overwrite=False` (porsche-gt3rs-992 `tools/shot.py`, `RESUME=1 render_final.sh`) so a restart only fills missing frames.
- **[pacing]** `ive beats` / librosa kick grids disagreed by 50-110 ms on a generated industrial track; the attack
  (first 30 % of peak) of the big hits on the waveform gave an exact 8-beat spacing. Anchor on that when the methods disagree.
- **[technical]** Close-ups of a 7.7M-tri (2.5 mm) car render at ~36 s/frame at 75 % / 12 spp (vs 13-16 s for 4 mm wides):
  render only the seconds you will use.
- **[pacing]** (honda-s2000 v6) A beat grid fitted from 11.6 ms RMS windows sat 5-35 ms early and drifted; the delivered-file
  check (kicks decoded from the mp4) showed 0 % of cuts within half a frame. Detect kick attacks at <=1.5 ms hop and put each
  cut on its measured kick; use the grid only for bars that have no kick. Coarser hops pick later sub-peaks (+20-40 ms).

## From the Toyota Sera v3 delivery (2026-11-11)
- Cut timing on a track with a sustained bass under the kicks: a broadband half-peak envelope (cutcheck.py) fires on the
  bass ~110 ms early. Measure the kick's click on a >2 kHz high-band envelope of the decoded file before "fixing" cuts.
- Typewriter label sub-lines take ~0.9 frames/char after the title animates in: a 32-char sub needs >= 50 frames on
  screen to be read in full. Check the LAST frames of each label in the delivered file.
- `ive director` repeat flags compare silhouettes: a front 3/4 opening and a rear 3/4 ending at the same whole-car scale
  are flagged. Look at the pair before cutting; document reviewed false positives in direction.md.
## From the GR Corolla scan reel v2 (2026-11-11, built by an agent)
- **[technical]** `tools/shot.py` (toyota-gr-corolla): turn Cycles persistent data OFF whenever any part has >1 key - every v2
  moving shot then rendered luma-clean (no dark tails), at ~10 % render-time cost. Keep it on only for camera-only shots.
- **[scan-look]** Legible licence plate in a scan: delete the plate-face triangles and drop in a flat GRID panel
  (60x30, wound to face out) on the fitted plane (tools/deplate.py). A 2-triangle panel is removed by `--drop-islands`,
  and flattening the original faces leaves z-fighting blobs.
- **[story]** Rear removal order must follow the state scans that exist: diffuser -> rear bumper -> crash beam. A shot of
  "bumper off, diffuser on" has no scan behind it - check which combination each removed-state scan actually captures.
- **[text]** Part labels go in clear black, never on a part that is moving through the same band: re-check every label
  against the frames of its window (GR Corolla CRASH BEAM sat under the departing bumper at y 220; moved to the low band).
- **[pacing]** Measure cut sync on the delivered file with a zero-phase kick-band envelope (35-110 Hz, sosfiltfilt) and
  an onset = last sample < 30 % of the local peak. A causal low-pass or "biggest rise" picker reads 1-2 frames off and
  locks onto risers/snares in a build.
- **[pacing]** `ive director` flags same-camera state swaps (A removed -> B removed in one camera) as repeats; they are one
  continuous sequence - log the reason and keep them. Do fix its "dead frames" on the opening: a 2 % push reads as static.

## From the Mazda Miata ND v3 revision (2026-11-11, built by an agent)
- **[technical]** shot.py renders round(seconds*fps) frames with t=(f-1)/fps: for N renders give `seconds = N/15`, not (N-1)/15
  (Miata v3 got N-1 everywhere); set each clip's src_fps from the real PNG count at assembly.
- **[text]** ScanHUD `label` crashes Remotion when `sub` is empty ("inputRange must be strictly monotonically increasing [6,6]"):
  always give a short factual sub line.
- **[scan-look]** Bumper-off hero beat in 9:16: park the bumper on the camera's sight line below the nose/tail (inner face to the lens,
  fully in frame), then let it sink out of frame while the camera pushes in on the structure; leave parked parts out of later shots
  (steep cameras still see them). Check first/mid/last frames with an edge-touch test (non-black pixels in the outer 3 px).

### From the Infiniti G35 v2 (2026-11-11)
- To move cuts relative to the music, remember the sign: a LATER `music.start` makes kicks arrive EARLIER in the video. Shift `start` by +(mean cut-minus-kick error) and re-measure with the decoded audio.
- `ive director` "same view shown twice" uses silhouette IoU; close-ups that fill the frame all score IoU ~0.9 even when the subjects differ. Confirm a repeat on the contact sheet before cutting a shot.
- Background shell tasks are killed at 2 h. Chain long renders one shot per task, and resume a killed shot with a `frames:` list starting at its last (possibly partial) frame.
- **[technical]** Split shots (parts frames 1-59 + clean-car frames 60-100, same camera): when you change the camera keys,
  re-render BOTH halves - QX80 v3 re-rendered only the parts half and the luma scan caught a 37 -> 44 step at the swap.
- **[scan-look]** Whole-car wide in 9:16 at 32 mm needs ~9.5 m for a 5.4 m SUV at a 3/4 angle (projected ~5.4 m wide);
  anything closer clips the nose or tail. QX80 (2026-11-11).

- **[scan-look]** Licence plates: flatten/blur plates ONLY on the IS300 (user: "Only is300"). Every other reel keeps its scanned plate unless the user asks in that reel's chat. This supersedes the earlier 'flatten plates in every scan' lessons.  _(from mazda-miata-nc @ 28.0s, 2026-11-11, user (relayed by parent session))_
- (mr2 v2, agent-found) `projects/honda-s2000/tools/concat_assemble.py` composites the project's `overlays:` itself. Do not run a second label/HUD pass on its output, or every label renders twice (unnoticed while the copies line up exactly).
- (mr2 v2, agent-found) Verify every cut against the decoded audio's transients, not just the BPM grid: on the MR2 track the grid beat at 12.86 s had no transient and the real hit was 100 ms later.

## From porsche-gt3-992 v2 (2026-11-11, agent observations, not reviewer rules)
- Check labels over the actual frames across their whole window (4 samples per label), not only at mid-window: parts that rise or float (lids, wings, bumpers) move into a label set from a mid frame.
- A side-skirt part-off only reads from a low grazing camera along the sill; side-on it vanishes against the door.
- Bumper-off composites of a 992 rear are fragmented above the exhaust: frame tight and low on tailpipes/silencers.
- Cut timing: a cut 0.4 ms outside ±½ frame of the decoded onset is still a fail; move it one frame and re-measure.
## From the Lexus IS350 2026 facelift reel (2026-11-11, built by an agent)
- **[technical]** One Drive folder can hold two different cars that register to each other: the "Lexus 4is" root Full Car
  (older IS350) and the "2026 Facelift" scans were aligned in Artec on the unchanged panels (headlamps/fenders 0.8 mm) but the
  grille mesh sat 8-12 mm off and the wheels 13-32 mm. Low overall regcheck medians are not proof of one car - compare
  per-region (grille, wheels, plate) and look at the plates/badges side by side before compositing states onto a base.
- **[pacing]** Measuring kick onsets on generated tracks: take the half-rise of the 1 ms RMS envelope within ~60 ms *before
  the envelope peak*. A wider pre-window catches the sustained pad before each kick and reads 100-145 ms early; the 40-120 Hz
  peak grid read 38 ms late. projects/lexus-is350/tools/cutcheck.py.
- **[technical]** (ferrari-296 v4) Interpolated PNG clips cut to exactly 2N frames stall: minterpolate makes only
  (N-1)*30/r - 1 frames from N renders and `_render_clip` clone-pads the rest (2-3 frozen frames before the cut). Scan the
  final mp4 for near-identical consecutive frames; lower `src_fps` to (N-1)*30/(n+2) (see ferrari-296 `assemble_cuts.py`)
  or render one extra frame per shot.
- **[text]** Labels over bright silver scan are unreadable without a halo; ScanHUD `label` now takes `shadow: true`.
  Composite the HUD and look at every label frame - keep titles short (FRONT BUMPER + sub REMOVED) so they fit the dark area.
## From the Honda Civic 11 (FE1) scan reel (2026-11-11, built by an agent)
- **[pacing]** A generated track can drift 10-80 ms against a constant-BPM kick grid (Civic: +8..+76 ms). Fit the grid for
  planning, then put every cut on the MEASURED onset of the decoded audio (1 ms RMS half-rise) rounded to a frame.
- **[technical]** minterpolate (mci) smears fast part moves (a door lifting at the drop came out as blocks, a lid's edges doubled).
  Render real 30 fps in-betweens just for the fast windows and blend the slow, camera-only stretches
  (projects/honda-civic-11/tools/merge30.py); play the result with src_fps 30 and no interpolate.
- **[scan-look]** In 9:16 a door or lid lifted straight UP into the black above the car keeps the opening visible; moving it out
  toward the lens covers the very jambs the shot is about.
- **[technical]** The persistent-data dropout can strike late (Civic v1 s7: frame 91 of 166). Persist off roughly doubles the frame time
  (12.7 -> 23 s/frame); keep it on only for static-scene, camera-only shots and scan their luma.
- **[technical]** (porsche-gt3rs-992 v2) In bars with no kick (hi-hat texture every ~100 ms) the half-rise onset tool has no
  single answer: measured "medium hits" were 0.23 s late in the output check. Cut on big hits only, or on the strongest
  local peak and say so. Generated tracks: map which bars actually have kicks before placing cuts.
- **[technical]** (porsche-gt3rs-992 v2) minterpolate drops the tail of a 15 fps sequence (~0.3 s on a 58-frame shot) and
  `dur` then pads with frozen frames; render ~0.2 s more than the clip needs or the director report shows dead frames.
- **[technical]** (porsche-gt3rs-992 v2) For parts that stay on in a part-explode, rebuild the composite cutting ONLY the moving
  parts; overlaying a static part on a cut-out leaves a visible gap line around it.
## From the Nissan Frontier v2 (2026-11-11, built by an agent)
- **[technical]** A removed-part scan can carry its own copy of a neighbouring part (Frontier bumper scan includes the grille,
  6-30 mm off the separate grille scan). An 8 mm proximity cut misses it and the explode shows two grilles. Cut by the
  neighbour's bbox + a 40 mm distance, then render the part alone before animating it.
- **[text]** Section labels in close-ups need a dark plate (white text vanished on the white hood); put them in the black band
  above/below the subject. For a part whose centroid falls off the part (flares spanning both arches), anchor the leader on
  the largest highlighted blob in the render frame instead (projects/nissan-frontier/tools/labels.py anchor_pixels).
- **[pacing]** Broadband 1 ms onsets ran ~50 ms ahead of the 93 ms-STFT kick-band grid after this track's drop; measure every
  cut beat's onset (tools/onsets.py) and verify on the delivered file (tools/cutcheck.py) - v1 had cuts 40-60 ms late.

### Suzuki Cappuccino v2 (2026-11-11)
- Render margin: 15 fps renders that are minterpolated to 30 fps lose ~1.5 output frames at the tail. A margin of +2 source frames left s3/s5 one frame short, so `dur` padded it with a cloned frame right before the cut. Render **+3 source frames** past the cut.
- 9:16 whole-car shots are width-limited. Frame the car at ~85-90 % of frame width (dist ~5.5-6 m at 40 mm for a 3.3 m kei car at a 3/4 view). At 7 m it read at 70 % with dead black around it, a weak hook. Check the first and last frames: the az changes how long the car reads on screen.
- `ive director` flags a continuous move split across two clips (x2 starting on x1's end pose) as a repeat. When that is intentional, log why rather than cutting it.
## From the Subaru STI blobeye v2 (2026-11-11, built by an agent)
- **[pacing]** A fitted beat grid can be the wrong tempo: the STI track's grid fit (152 BPM, from onsets with only 20/49 kicks
  on-grid, 32 ms residual) was really 150 BPM (kick every 0.400 s); by 22 s the grid was 125 ms off the kick. A low on-grid
  ratio / high residual means the tempo is wrong - fit the period on the kick attacks themselves (40-120 Hz rise through 50 %
  of the peak, hop 32) and snap every cut to the nearest measured attack on the decoded delivered audio.
- **[framing]** Exploded state in 9:16: parts parked 2 m above the car read tiny from r 9 m; r 8.5 m with the orbit centre
  pulled ~0.4 m toward the part cluster keeps all parts in with margins. Check first/mid/last at preview res (15 s) before any final.
- **[text]** ScanHUD `label` crashes on an empty `sub` (typewriter interpolate range [6,6]); always give a short factual sub.
## From the Toyota GR86 / BRZ v2 (2026-11-11, built by an agent)
- **[pacing]** cutcheck.py's "largest rise in -120..+80 ms" can lock onto a later transient in the kick's tail and report a
  cut as 40 ms early when it is 40 ms late. Print the 1 ms envelope around each cut and take the first half-rise after the
  pre-kick dip: this track's kicks sat ~30 ms ahead of the accents.py downbeat grid, so every cut moved 1 frame earlier.
- **[text]** Remotion ScanHUD label with an empty `sub` crashes ("inputRange must be strictly monotonically increasing [6,6]");
  pass `sub: " "` for a title-only label.
- **[scan-look]** Read the newest lessons right before rendering, not only at the start: gr86 flattened its plate per the
  older lessons while the user's "only IS300" plate rule had already landed, and two shots had to be re-rendered.
  (If a plate IS to be flattened: a rear-bumper-removed state's base has no plate - the box there holds the real crash beam.)
- **[technical]** Lighting-dropout signature (persistent data on): from one frame on, render time halves and luma falls to
  ~6 (black silhouettes). Turning the key light's camera visibility off does not fix it; `use_persistent_data = False` does.
## c5-corvette v2 (2026-11-11)
- **Read the kick envelope around every cut; don't trust one onset number.** A ±0.15 s "strongest kick" search (c5 tools/kickcut.py)
  latched onto the second hit of a double kick and put cuts 2.5-3 frames late. Print the 40-150 Hz 8 ms envelope plus the
  broadband 1 ms envelope at 1-frame steps around each cut, cut on the first clear rise, then confirm with porsche-macan cutcheck.py.
- **To land an in-shot event (a swap) on a kick, measure it in the assembled file** by matching output frames to the render frames on
  either side of the event, then nudge with `speed:` (0.96 = +4 % slower, invisible). Shot-local maths was 2 frames off.
- **Background waits on `pgrep -f <name>` match their own command line** (`bash -c 'while pgrep -f x.json ...'` contains x.json) and
  never exit: c5 lost 2 h. Chain jobs in one script (`render_all.sh a b c`) or wait on a PID.
- **Remotion ScanHUD `label` crashes on an empty `sub`** (interpolate inputRange [6,6]). Use `"sub": " "` for title-only labels.
- **`ive director` "repeated views" is silhouette overlap**: small centred cars on black flag even front vs rear. Check the pairs by eye.

- **[text]** If the video shows a variant (Spyder), the narration must talk about that variant too  _(from huracan-evo @ 41s, 2026-11-11, reviewer)_

- **[text]** Narration units in imperial (hp, lb-ft, mph, 0-60)  _(from huracan-evo @ 4s, 2026-11-11, reviewer)_

- **[audio]** Narrator speaks faster, like the example video  _(from huracan-evo @ 4s, 2026-11-11, reviewer)_

- **[text]** Narration should cover quirks and unique facts about the car, not just the spec sheet  _(from huracan-evo @ 4s, 2026-11-11, reviewer)_
- **[story]** v2: the doors lifting off and the trunk lid lifting off are hallucinated - the scans show doors OPEN and trunk OPEN, so the parts must only open on their hinges, never detach  _(from honda-civic-11 @ 13.3s, 2026-11-11, reviewer)_

### Suzuki Cappuccino v3 (2026-11-11) - reviewer: "the lines where the front bumper and trunk were cut for the exploded view are not correct"
- **Never cut a panel out of the full-car scan with margins or distance thresholds.** The real shut line is in the scan as a groove. Make a top-down height map (2 mm px), groove depth = grey closing minus height, and trace the gap as a least-cost path through a few waypoints, inside a corridor (`projects/suzuki-cappuccino/tools/panels.py`). Edges that drop over the nose or tail are invisible from above: trace them in the front/rear view.
- Check where a panel really ends before cutting: the Cappuccino hood runs forward between the head lamps to the bumper seam and back to the screen corners; the trunk lid wraps over the tail down to the seam between the tail lamps. Compare the body-after-removal against the bumper-off state scan in the same view - any band of skin the state does not have is a wrong cut.
- Body-side cut for a removed bumper = car skin that the bumper-OFF state scan does not have, limited to a zone around the bumper part scan. The state decides the seam; a distance trim to the part scan leaves remnants and ragged fender edges.
- Logo card: 380 px wide on 1080 was "too small"; 720 px is the current size.

### Lamborghini Revuelto v3 (2026-11-11) - reviewer: "the wheels are oddly cut flat" + "exploded views of the individual parts removed from the front and rear bumpers"
- **A RANSAC "ground" plane on a full-car scan can be the flat undertray, not the floor.** On the Revuelto no floor was scanned; the level plane sat on the undertray and a z > 8 mm floor cut sliced 17 cm off every tyre (plus bumper lips and lower structure). Before any floor cut, plot the z-profile under a wheel: tyres must hang BELOW the plane you call ground. If no floor exists, clean by footprint + lowest tyre z instead (`projects/lamborghini-revuelto/tools/clean2.py`).
- Bumper sub-part explode (front and rear): cut to the bumper ALONE on black (car loaded hidden, only as the light reference), show the scanned inner face, turn to the outer face, then swap the assembled bumper for the stripped skin + each sub-part scan and move the pieces apart along the car's axes. Register every sub-part scan to the bumper scan first (tint overlay + median distance), leave out anything that is not a bumper part (reverse light, plate light, exhaust tips) and pull the camera back until the spread fits (3 m clipped; 3.8-4.1 m fits a 2 m bumper in portrait).
- Look at the FIRST frame of every wide after the final render, not only the 30 % preview of an earlier camera: the v3 opener had the nose clipped at the frame edge for its first half and needed a re-render.
## c5-corvette v3 (2026-11-11): artifacts from state scans
- Never composite every removed-state scan into one base. Duplicate skins (hood, cowl, glass) sit 3-10 mm off the car and show
  as shards. Build one base per section from that section's own state (`projects/c5-corvette/tools/composite2.py`: >15 mm from
  car and parts, island filter ≥4000 tris), and swap to it in the shot where it's used.
- Clean the full car before it is shown whole: ground scraps and tyre fringe (`projects/c5-corvette/tools/carclean.py`).
- Region states without a part scan (door open, fuel door, hatch) are shown by an in-shot swap of just that region
  (`projects/c5-corvette/tools/swapstate.py`) on a kick, with a label.
- minterpolate smears the frame between pre- and post-swap renders (a ghosted swap). After assembly, find each swap by frame
  differencing and replace the blend frame: `vf: split[fa][fb];[fa][fb]freezeframes=first=N:last=N:replace=N-1` (N is
  clip-local after fps). Do not move a swap with `speed:`: the fps resample adds a duplicate plus a blend. Use `hold_start` and
  shorten `dur` instead.
## From the Nissan Frontier v3 (2026-11-11, built by an agent)
- **[scan-look]** "Bumper removed" bases: trimming the truck within a few mm of the removed-part scan leaves bumper skin on the
  truck when that scan is misregistered (Frontier: 6-30 mm; the user saw leftover valance/corners). Remove truck tris inside
  the part's bbox that are > 10 mm from the bumper-OFF state scan instead (nissan-frontier/tools/composite.py --remove-diff),
  then drop state-fill islands not voxel-connected to the body (tools/attached.py).
- **[scan-look]** User wants hoods to open on their hinge and show the underside. State scans often contain fragments of the
  propped-open hood (points > 40 mm off the truck above the cowl): fit the hinge to them (nissan-frontier/tools/hinge.py) so
  the angle is from data, and say in the review when the underside itself was not scanned.
- **[scan-look]** Parts derived by distance-diff (flares) carry body strips. Look at a depth-coloured side splat and cut by
  geometry (arch annulus + protrusion |x|), one part per arch; move thin parts onto clear black before turning them.
- **[text]** Logo card: 380 px wide read as too small on this reel; 700 px was used for v3.
## toyota-gr86 v3 (user feedback on v2)
- [scan] A hood mask built from "car tris missing in Hood Open" also takes the lower windshield, because the open hood hides it. Trim hood parts at the measured cowl gap (projects/toyota-gr86/tools/hood_trim.py) and look at the windshield in a render.
- [scan] Before planning, list EVERY state/part scan in the Drive folder (trunk open, mirrors removed, individual lamps). The user flagged three we had missed. Small part scans (reverse light, plate lamp) are explodable beats: register them with tools/register_part.py and check the facing, because ICP can fit a lamp backwards.
- [scan] `--drop-islands` 1500 deleted tail-lamp lenses in composites. Use ~150 and check the lamps.
- [text] Measure the scan coverage under each label box over its whole window. Don't assume the top band is black on close-ups.
