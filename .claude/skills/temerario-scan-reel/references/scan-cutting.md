# Cutting, nesting and registering scans: methods that passed review

Every recipe below replaced one the user rejected. Paths are repo-relative. Read the tool before reusing it: they are
per-project and assume that project's frames and file names.

## First, look

- Before any cut, put three stills from ONE camera side by side:
  - the full car, with its shut lines visible;
  - the removed-state scan;
  - the loose part.

  The right cut is obvious there and not from distance numbers (a90-supra v3.1).
- Render every state scan alone at the planned framing before planning. Colour a composite by source scan to find stray
  fills (GR86 v7).
- Check full-res close-ups. 30 % previews and Workbench stills hide speckle, seam gaps and z-fighting.

## Shut lines (hood, trunk, hatch, fender, bumper)

- **Trace the groove.** Render near-orthographically along the panel's normal: camera = panel centre + 26 m x normal,
  focal 200-220 mm. Trace the gap, then map the pixels back to faces.
  - Tools: `projects/toyota-gr-corolla/tools/hoodtrace.py`, `hatchtrace.py`.
  - The alternative is a top-down height map (2 mm px), with groove depth = grey closing minus height, and a least-cost
    path through waypoints (`projects/suzuki-cappuccino/tools/panels.py`).
- Panels wrap. The Miata ND trunk lid includes the rear face between the tail lights, and the Cappuccino hood runs between
  the headlamps. Trace the front and rear views too, not only the top.
- The hood/bumper split is the visible seam in the front view, not the top of the bumper part scan: its flange tucks
  about 20 mm behind the hood lip (cappuccino v6).
- **Opening panels from an open-state scan:** the panel = car faces ABSENT from the open capture, as an exact complement.
  - Smooth it on the surface with a 20 mm majority vote.
  - Take the largest blob and close holes.
  - Mirror the clean half when one side's coverage is missing.
  - Tools: `projects/toyota-gr86/tools/lid_v6.py`, `projects/mazda-miata-nd/tools/lid_from_state.py`.
- A hood mask from "missing in Hood Open" also takes the lower windshield the open hood hides. Trim at the measured cowl
  gap (`projects/toyota-gr86/tools/hood_trim.py`), and take the cowl-side edge from the OPEN capture swung closed
  (`projects/toyota-sera/tools/hood_clean.py`).
- **Hinges:** measure the angle from the open-state scan's fragments of the propped panel (plane fit,
  `projects/nissan-frontier/tools/hinge.py`). Put the axis on the panel's real edge corners: a pivot behind the edge
  swings into the glass.

## Removed parts

- **When a loose part scan with a clean outline exists, that outline is the cut.**
  - Remove car faces within 4-5 mm of the part scan, closing pin-holes with a majority vote
    (`projects/a90-supra/tools/cut_v4.py`, `recut_v3.py`).
  - Use the removed-state scan only where the loose part can't decide, such as the flexible flanks of a bumper.
- **A removed part takes only its own skin.**
  - Never delete every face a stripped-shell scan lacks inside a bbox. Headlights and fenders vanish
    (`projects/toyota-gr-corolla/tools/frontcut.py`, `bumperline.py`).
  - Scrap islands near the panel stay on the body (a90 `STRICT`).
- **A removed part comes off whole.** Moving part = part scan + every car face the cut removed that the part scan doesn't
  cover (`projects/toyota-gr-corolla/tools/bumperfill.py`).
- **No leftovers.** Bumper skin = car faces that the bumper-OFF state lacks by more than 10 mm, inside the bumper zone. Move
  them with the bumper (`projects/toyota-gr86/tools/build_v4.py`; nissan-frontier `composite.py --remove-diff`).
- **State fills only fill their own opening.**
  - A state captured with a panel CLOSED refills that panel once it is carved out: bar it within about 12 mm (GR86 v7).
  - States carry unrelated changes, such as a card left on a fender: limit each fill to its region (Sera v5).
- **Fitted panels show the car's OWN skin** until the frame they start to move. The part scan takes over only while moving
  (`vis` windows, a90 `make_skins_v3.py`). Once a separately scanned part is back on, swap to the full-car version
  (Frontier v10): part scans are warped at their edges.
- **Fusing two different cars' parts at rest:** keep only part-scan surface clearly BEHIND the skin, at a signed distance
  along the outward normal below -8 mm (`projects/toyota-gr86/tools/fuse_v8.py`).
- **Never composite every state into one base.** Build one base per section from that section's own state
  (`projects/c5-corvette/tools/composite2.py`), and swap regions in-shot on a kick (`swapstate.py`).
- **A part with no file of its own** (a wing) can be cut by shape: take faces more than 4 mm above the fitted surface
  under it, grown forward only (`projects/toyota-sera/tools/wing_cut.py`).
- Parts that can't come off can still be highlighted: render a matte pass and dim the rest
  (`projects/porsche-gt3rs-992/tools/highlight.py`).

## Floors, wheels, artifacts

- A RANSAC "ground" plane can be the flat undertray. Plot the z-profile under a wheel: the tyres must hang below it. If no
  floor was scanned, clean by footprint + lowest tyre z (`projects/lamborghini-revuelto/tools/clean2.py`).
- If a capture missed a wheel, mirror a complete one across the centre plane (`projects/toyota-gr-corolla/tools/wheelmirror.py`).
- Clean the full car before showing it whole: ground scraps, tyre fringe, floating islands (c5 `carclean.py`). Use about 150
  as the island threshold, not 1500, which deleted lamp lenses.
- **Never grid-decimate hero meshes.** 3 mm clustering put stair-step contours on bumpers. Use full resolution near the camera.

## Registration

- Level once, then prep every scan `--like <full car>.json`.
- A second scanning session shares ONE rigid offset. Solve it on the scan with the most overlap and apply it to all of them
  (`scripts/xform.py`). Per-part ICP of pipes against a car is unreliable.
- Register small part scans (lamps) with `projects/toyota-gr86/tools/register_part.py` and check which way they face:
  ICP can fit a lamp backwards.
- Brake bench scans have no inside/outside. Render both faces before placing them (QX80: "the brakes are backwards").
- Engineering's car frame is NOT our prepped frame. First ICP their own car scan, exported from the reference .blend, to
  ours on the body above the wheels, then apply that transform to every one of their parts (GR Corolla v12). CAD in
  the scan frame lands on the stock part untransformed: print each solid's bbox first.
- Generations sharing a shell (GD bug/blob/hawk) register onto each other with globalreg + refine. Pin the light rig to one
  bbox for same-camera cuts (`projects/subaru-gd-trio/tools/shot.py` `light_bbox`).

## Kit parts and aftermarket CAD

- Lookbook GLBs ship `body_<part>_stock` for each `part_<part>`. Cut the scan by that piece's footprint (±30 mm along the
  normal, no lateral margin) and remove scan skin 2-20 mm in front of the part
  (`projects/toyota-mr2-spyder/tools/kit_nest2.py`).
- Clip every base mesh against a new part's back-face depth map, then check the removed faces in red
  (`projects/nissan-frontier/tools/grille_clip.py`).
- STEP to mesh: OpenCascade (`projects/toyota-gr-corolla/tools/step2stl.py`). gmsh can hang. CAD cores are smooth: model fins
  when the user asks.
- Check a part's orientation against the stock part's inlets and outlets, not just its envelope.
- Size parts from the 1:1 frame against the REAL part (Frontier badge).
