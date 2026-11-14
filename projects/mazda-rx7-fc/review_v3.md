# Mazda RX-7 FC3S scan reel v3 — self-review (training/rubric.md)

Output: `/home/user/media/work/rx7/out/mazda_rx7_fc_v3.mp4` — 1080x1920, 30 fps, 48.0 s (1439 frames). v1/v2: review_v1.md, review.md.
User request: "use every scan i have for this car, re-edit to this music, add the call-to-action since this should have had
every panel replaced". v3 = the HertLife printed time-attack widebody (Drive Projects_/HertLife Fc3s) replaces every stock panel
of the S5 scan, set to the user's T-Pain "Hert Baby Got Brap" upload, ending on a mobile CTA for the FC3S scan listing + logo.

Order (direction_v3.md / director_v3.md): whole stock car over the 2-bar lead-in -> ON the drop the hood opens (Hood Up) ->
captured hood lifts off over the bay (Hood Off Bumper Off) -> stock front bumper (Front Face part) off -> radiator support /
crash beam -> kit front (bumper + headlights, splitter, canards, vented hood closes on the hinge) -> both overfender skins +
side splitters slide in (high front view, the car widens) -> stock rear bumper off -> rear crash beam / mounts -> kit rear
(bumper, diffuser, tips, GT wing) -> finished widebody orbit -> the listing's own scan orbits into the listing viewer's camera
and shrinks 1:1 into the phone -> ILLUMAESTHETIC 760 px.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole stock car turning from frame 1; the first change (hood opens) lands ON the drop at 5.333. Lead-in is soft by design (song). |
| 2 | Beat sync | 5 | Decoded delivered file, broadband kick half-rise: 10 of 11 cuts within -11..+20 ms; 21.333 is on a weak hit (x2.9) at -45 ms. Every cut's first new frame = planned frame (1-frame fades, no duplicate frame before cuts). |
| 3 | 1:1 match | 4 | CTA: listing scan render on the solved viewer camera (IoU 0.959 solve) overlays the phone listing; internal joins s6->s9 and c8->c9 are continuous moves. |
| 4 | Scan quality | 4 | Real removal states only (Hood Up, Hood Off Bumper Off, Front Face, Rear Bumper Removed); plate flattened; stock wheels sit inside the wider kit arches (no wide-wheel data). |
| 5 | Story | 5 | Stock -> every panel replaced -> finished car -> "scan data available" for the same model. Every scan in the RX-7 FC3S folder + the HertLife design scan used (Hood Down Bumper Off duplicates Hood Off Bumper Off's role - registered, not shown). |
| 6 | Grade | 4 | Silver stock scan, satin cherry kit skins, gunmetal aero, -0.5 EV; pads/cards on the measured render black (4,4,5). |
| 7 | Text | 4 | 12 plain part-name labels (no numbers), max 2 on screen, over scan shots only; CTA text from the listing (title, "SCAN DATA AVAILABLE", ILLUMAESTHETIC.COM). |
| 8 | Ending | 5 | Finished car on the bar-14 downbeat, CTA on 42.667, logo on 46.0, music fades 1.2 s. |
| 9 | Technical | 4 | Specs met; every render folder luma-scanned (no dropouts); all-frames edge check: three shots padded to 94 %; parked parts re-rendered out of frame. |

## Known limits / user calls
- Kit colour is a choice (red/gunmetal) to make "replaced" read; the real car's paint is not in the data.
- Stock wheels in the widebody arches leave a gap (no wider wheel scan).
- The listing dataset is "Exterior Only (S4)" (the 2025 stock FC3S scan), not the HertLife S5 - the CTA says "scan data available", nothing more.

## For the next agent
- KeyShot OBJ exports use RELATIVE (negative) face indices; parse them or every part's bbox spans the whole car.
- A kit design file without a car: look for a review/OBJ that stores the kit WITH the scan (here Review/OLD/FC3S_TA_with scan.obj).
- PCA splats can flip an axis: confirm "upside down" against a real overlay before flipping a scan.
- After padding a shot (scale < 1) re-check parked parts: they move back into frame.
