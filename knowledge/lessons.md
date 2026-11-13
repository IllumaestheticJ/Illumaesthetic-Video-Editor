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

## From the NC wing configurator demo (2026-11-11, built by an agent)
- **[story]** Product-UI demos: capture the LIVE epsilon.plus pages frame-stepped with Playwright (scroll + tap indicator scripted per
  frame, CSS animations advanced 1/30 s via `document.getAnimations()`), 432x768 @2.5x = 1080x1920. See projects/nc-configurator/tools/capWeb.cjs.
- **[match-cut]** 1:1 against a web 3D view: export the view's own meshes, solve the photo camera on them, then drive the view's camera
  (matrixWorld + an off-centre projection matrix for the 9:16 window) from a capture-only build; never commit that build to the site repo.
- **[match-cut]** Silhouette-only refinement can fit the outline with the car rotated (interior features ~40 px off). Add interior
  landmarks (emblem, plate, lights, fuel door) and judge with an edge overlay.
- **[audio]** Trending music: Higgsfield `tiktok_music_trending` lists TikTok's Commercial Music Library with preview files
  (host sf16-ies-music-sg.tiktokcdn.com). Find the drop from low-band RMS, fit the grid on low-band onsets, put the 1:1 cut on it.
- **[technical]** Dropbox download hosts are per-file and random; every new batch needs the hosts added to the environment.
- **[story]** Search Dropbox by the car AND the product before settling on footage ("TC wing", "NC", the model name), and list `2. Long Form`
  as well as `1. Video dumps`. v1 of the NC demo used the Integra tutorial because only "install tutorial" was searched; the NC's shoot
  was in `/1. Epsilon Plus Videos/2. Long Form/TC Wing Tutorial`. Never substitute another car's footage without asking.

## From the DE5 wing configurator demo (2026-11-11, built by an agent)
- **[story]** Check that the product in the brief exists for that car before building: list `https://epsilon.plus/products.json?limit=250` and look at what
  the live configurator defaults to. Brief said "DE5 TC wing"; the store only has a GT Wing and a Sport Wing for the DE5 and the real photos are GT Wing.
  Asked the user (they chose the GT Wing) instead of substituting.
- **[story]** A payoff shot must show the same part as the 1:1 photo. The Integra tutorial's finished-car clips show the Sport Wing, so the payoff used
  the listing's other real GT Wing photos.
- **[match-cut]** Landscape photo into 9:16: the window is at most the photo's height (1450 px -> 816 px wide). A wide part (66 in wing) will not fit;
  centre the window on the part and pan, and give capD.cjs the same window path.
- **[technical]** `update_environment` was rejected when adding 20 hosts to a ~125-host allowlist; removing 20 expired `uc*.dl.dropboxusercontent.com`
  hosts in the same call went through. Request Dropbox links with `expiration_in_sec: 900` and download in parallel right after approval.
- **[technical]** NC tools reuse: copy `wing-configurator` out of the site repo, add `window.__ewc3d = {THREE, camera, controls, renderer, scene, carGroup, kitGroup}`
  in `src/three/view3d.js` `mount()`, `node scripts/build.mjs --out dist`, serve on :8123 with a `product.html` carrying `data-car`/`data-wing`/`data-lock-car`.
- **[audio]** 'Time Back' (110 BPM) has pickup hits 0.5 s and 0.1 s before the drop; take the drop from the first frame where BOTH low band and full band
  jump (35.97 s), not the first full-band transient.
- **[match-cut]** Driving a web 3D camera to a solved pose: blend the solved orientation as an OFFSET from a plain look-at (`ql * slerp(I, inv(lookAt(eyeS,tgt)) * qS, w)`),
  blend the principal point with the same weight, and put the look-at point where the crop window's centre ray meets the car. Slerping to the absolute solved
  orientation while the eye still orbits threw the car out of frame with a 13 m tele camera (DE5 v2); the NC's 3 m phone camera hid the bug.
- **[match-cut]** Label left/right and front/rear landmarks from the photo, not from memory of the reference render: one swapped door handle cost 28 px RMSE.
  When RMSE is high, overlay first and look for a single mislabeled point before reaching for refinement.
- **[story]** Shopify listing images: stage with `stagedUploadsCreate` (host `shopify-staged-uploads.storage.googleapis.com` must be allowed), `productCreateMedia`,
  `productReorderMedia`; detach a replaced image with `fileUpdate(referencesToRemove)` so the file stays in Files. Images must be <= 5000 px / 20 MB.
  The store app credentials are in the environment (`SHOPIFY_CLIENT_ID/SECRET`, client-credentials grant on bmspec.myshopify.com). See projects/de5-configurator/tools/listing_photos.py.
- **[story]** DE5 v3 (user): install snippets go BEFORE the 3D-model -> real transition, and the video ends on the real photo (the 1:1 is the payoff, no montage after it).
- **[grade]** Shaded car against a bright sky: brighten with a gamma that follows blurred local luminance (0.6 in shade -> 1.0 in sky), not a flat lift.
- **[technical]** Replace a Shopify product image in place with `fileUpdate(files:[{id, originalSource: <staged url>}])`: same media id, position and alt text.
- **[pacing]** DE5 v4 (user): no push-in zoom on the final real photo ("hate the zoom"). Use a constant-scale slide that eases to rest on the hero part; give the
  3D camera the same slide speed at the cut. Check the resting frame holds the whole part before choosing the slide direction.
