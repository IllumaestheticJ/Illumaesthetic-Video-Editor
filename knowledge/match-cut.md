# 1:1 perspective cut: IRL frame → scan data

Goal: on the cut frame, the scan render shows the car at **exactly** the pixel size, position and
perspective it has in the real footage. Worked example: `projects/240sx-scan/match/`.

## 1. Pick the cut frame (most important decision)
Good frames:
- the whole car (or the hero part) is visible, unobstructed by people
- the camera is momentarily slow (handheld drift is fine; whip pans are not)
- **the car's state matches a scan state** (bumper on/off, hood open/closed, headlights up/down).
  Engineering usually scans several states (`S13 Hatchback Full Car`, `... Front Bumper Mounting
  (Chassis)`, `... Headlights Up`…). Pick the frame whose state you have a scan for.
- strong rigid features spread in depth: rear emblem, panel seams, spoiler tips, mirrors,
  roof corners. A frame of only a flat face (e.g. just the radiator support) cannot solve focal length.

Lesson (240SX): the bumper-removal frame looked like the obvious cut, but pop-up headlights
and the hood were at different positions in the scan session → no rigid landmarks matched.
The rear ¾ frame of the car during powder scanning matched the full-car scan perfectly.

## 2. Get the frame
`python -m ive frame <clip> <t> frame.png` (tonemaps HLG). Note `t` — the clip in the timeline must
end on exactly this frame (`out` = t + 1/fps).

## 3. Reference render + landmarks
1. `python -m ive lookat cam_guess.json --loc x,y,z --target x,y,z --focal 26` roughly from the same side.
2. Render it: `python -m ive render --scene scan.blend --camera cam_guess.json --out ref.png --look clay`.
3. Make zoomed grid crops of both images (see `ive/check.py` helpers or the session log) and pick
   **8–10** features visible in both. Write the frame pixel (`px`) for each.
4. Turn the reference-render pixels into 3D scan points:
   `python -m ive render --scene scan.blend --camera cam_guess.json --out /tmp/x.png --raycast "emblem:490,928;mirror_R:807,800"`
   Validate: re-projecting a hit with the guess camera must land on the same pixel.
   **Rays fall through scan cracks** (panel gaps render as black lines = holes). Nudge 2–3 px off seams.
   A hit whose depth is far from its neighbours is wrong — drop it.

## 4. Solve
`python -m ive solve points.json cam.json` → reports focal, RMSE, dropped outliers, and writes
`cam.overlay.png` (green = picked, red = reprojected).
- Use `sensor_width_mm` = the sensor size across the frame **width**. iPhone portrait 16:9 video: **20.25**.
- iPhone 16 Pro 1× main lens solved to **≈28 mm** on that sensor (24 mm-equiv + stabilisation crop).
  If the free solve is wildly off (e.g. 190 mm), your points are coplanar: fix `focal_mm: 28`.
- Target RMSE ≤ 3 px at 1080 wide. 240SX: 3.0 px after dropping 2 outliers.

## 5. Verify
Render the scan with `--camera cam.json` at the frame's resolution and run
`python -m ive check frame.png render.png check.jpg`. **Look at the overlay** (cyan = scan
silhouette, orange = IRL edges). The numeric score is pessimistic on night footage because dark
car-on-dark-background edges are weak; the overlay is the ground truth.

## 6. Render the scan shot
The scan shot must **start** at `cam.json` exactly; any move (`--move push|orbit`) begins from it.
In `project.yaml` put `transition: {type: cut}` between the IRL clip (ending on the cut frame) and
the scan clip. Cut on a beat.

## Never change the scan's normalisation after solving
`cam.json` is in the coordinates of the prepared `.blend`. Re-running cleanup can move the lowest
point and shift the whole car. Always re-prep with `--like <first prep>.json` to pin the transform.

## Glasses POV (Ray-Ban Meta) — Lola reel
Close, steep top-down views from the glasses (e.g. standing over a rear deck/wing) did not
converge; pick frames where the car fills ≤70 % of the frame with roofline + one wheel visible.

## Matching a film/trailer shot (Lola v6)
- Long-lens side profiles: the silhouette refine is degenerate in camera height/offset. A free refine can match
  the outline from below ground and still render wrong (far-side wheels under the car). Pin the height
  (`proj.py refine --fix-h 0.7`), fix a long focal, and look at a one-frame render before the full render.
- 2.39:1 footage in a 9:16 reel: show it as a band on black so the whole car fits; the scan's black background
  takes over at the 1:1 cut and captions go in the bars (never on footage).
