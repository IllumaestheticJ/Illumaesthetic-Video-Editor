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
