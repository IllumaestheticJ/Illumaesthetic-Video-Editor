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
