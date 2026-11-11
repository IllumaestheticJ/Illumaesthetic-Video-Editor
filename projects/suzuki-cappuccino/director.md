# Suzuki Cappuccino - director's plan v2 (stage 2, keeps direction.md's scene order)

Inputs: the user's v2 brief (1-9) + follow-up feedback A-D (A-D win on conflict: labels are now ON), lessons.md, Temerario
notes, director_report.md (v1 repeats: s01~s02~s03~s06~s11, s09~s10~s11), 6-frame contact sheets of all 11 v1 render
dirs, native-res crops of s06 f59 / s07 f45, shots.py + tools/shot.py (keys: `off`, hinge `deg`, `spin` = [deg, ax, ay, az]
about the part's own bbox centre, `visible` windows; camera `cam(t, az, el, dist, target, lens)`; sensor 24 mm wide).

## Diagnosis of v1 (from the sheets)
- Opener s01/s02 cropped: 24 mm sensor at 4.4-5.0 m shows only 2.6-3.0 m width; the car (3.28 m) is clipped. Fails A.
- s01, s02, s03 are three whole-car turntables (report IoU 0.73-0.82); s08 rotating top-down shows nothing new. Fails brief 3.
- Front opening (s06) and rear (s07) are wide 3/4s at 4.2-5.0 m: bumper, lamps and the structure behind them are small,
  the camera never moves in, and the lamps never leave the bumper. Fails brief 2 and C.
- Explode s09/s10/s11: everything rises at once, wide, three near-identical side views, 11.5 s + 2.7 s logo. Fails brief 7.
- Good and reusable unchanged: s04_wheel (detail fills the frame, ends looking down the right side).
- Hood/trunk stopped at 90 % of the captured angle; v2 lands them exactly on the captured slivers (feedback D).

## Shared definitions for shots.py (v2)
- Beat n = 0.033 + n x 0.47619 s. Cut frames = round(t x 30).
- Hinges unchanged (hinge_hood.json / hinge_trunk.json). HOOD_OPEN = -51.98 deg, TRUNK_OPEN = +62.93 deg (100 %, not 90 %).
- Bumper tips use `spin` about the part's own centre and the X (car-width) axis (lesson 240SX/A90: flip about the width
  axis, never a Z spin): front +95 deg turns its inner face (+Y) up toward an elevated front camera; rear -95 deg turns its
  inner face (-Y) up toward an elevated rear camera.
- Poses (offsets from home, m):
  - F_OUT (end of s2): fb off [0,-0.70,-1.00] spin 95; li off [0,-0.95,-0.90]; hood 0.
  - R_OUT (end of s5): rb off [0,0.75,-1.05] spin -95; trunk deg TRUNK_OPEN.
  - LAYERS (finale; each layer clear of the others in Y so nothing passes through a panel):
    hood off [0,0,0.85] deg 0; trunk off [0,0,0.85] deg 0; fb off [0,-0.45,1.20] spin 80; li off [0,-0.55,1.60];
    rb off [0,0.45,1.30] spin -80. LAYERS_DRIFT = LAYERS with z +0.04 (lin).
- Objects: s1 and s4 = CAR (car2). s2, s3, s5, x1, x2 = EXPLODED set (base, fb, li, rb, hood, trunk), light_ref base.
- Persistent data stays off; per-frame luma scan of every new dir before assembling (lessons).

## Shot table

| # | section | shot id | beats / seconds | focus | camera (scan frame; az/el deg, dist m, target m, lens mm) | part action (shot fractions) | why it earns its seconds | render |
|---|---|---|---|---|---|---|---|---|
| 1 | whole | s1_whole | b0-8, 0.000-3.843 | whole car, front-right 3/4, fully in frame (~65-70 % width, margins all round) | cam(0,-55,10,8.4,[0,-0.10,0.55],40) -> cam(1,-35,7,7.4,[0,-0.20,0.52],40); moving from frame 1; fade-in 0.5 s | none (car2) | the only whole-car exterior; establishes the car before the front story; v1 openers were cropped | NEW, 60 fr |
| 2 | front | s2_frontbumper | b8-28, 3.843-13.366 (9.52 s; every 2 beats = 0.1) | headlamp + bumper lamp in place -> bumper lamps -> front bumper inner face (mounting tabs) -> **structure behind the bumper** | cam(0,-30,8,1.6,[-0.42,-1.45,0.45],50) slow slide across the right lamp pair -> cam(0.15,-27,10,1.5,[-0.30,-1.50,0.42],50) -> cam(0.35,-22,22,3.6,[0,-1.75,0.25],40) (nose above, black below) -> cam(0.50,-18,40,2.0,[0,-2.16,-0.13],45) -> cam(0.66,-16,42,1.9,[0,-2.16,-0.13],45) (inner face, creep) -> cam(0.80,-12,12,1.5,[0,-1.45,0.35],45) -> cam(1,-4,10,1.3,[0,-1.40,0.38],45) (lin creep on the structure) | li: 0.15-0.30 -> [0,-0.75,0.00] (straight out toward the lens, translate only: lamp backs not verified). fb: 0.30-0.45 -> [0,-0.55,-0.45] (forward + down into black below the nose); spin 0 -> 95 over 0.38-0.55. 0.66-0.80: fb -> F_OUT, li -> F_OUT (both drop out of frame below so the structure is unobstructed). hood shut, rear home | hero beat 1 (C): bumper comes off, is shown off (scanned inner face), then the camera goes in on what is behind it and holds ~1.9 s to read. Merges v1 s05 + front half of s06 | NEW, 145 fr |
| 3 | engine bay | s3_engine | b28-40, 13.366-19.081 (5.71 s); drop b32 at t=0.333 | engine bay under the hood | cam(0,-24,24,3.2,[0,-0.95,0.70],40) -> cam(0.333,-20,30,2.9,[0,-0.95,0.65],40) (slow rise through the break, no cut) -> cam(0.55,-12,52,2.3,[0,-0.90,0.50],40) -> cam(1,-6,56,1.8,[0.05,-0.85,0.48],45). At el >= 52 the open hood is near edge-on (its unscanned underside is not the subject); hood may cross the top edge | hood: 0 until 0.333, swings to HOOD_OPEN over 0.333-0.45 (lands ON the drop, eases out), holds. fb/li hidden (`visible` [0,0]) - they left frame at the end of s2. rear home | the richest state gets the drop as a motion hit inside a held shot (no cut in the break); then a 2.6 s push into the bay | NEW, 88 fr |
| 4 | wheels (side) | s4_wheel | b40-44, 19.081-20.985 (1.90 s) | front-right wheel: 6 spokes, tyre | unchanged v1: cam(0,-60,8,0.95,[-0.66,-1.03,0.55],50) -> cam(1,-84,10,0.78,[-0.68,-1.03,0.55],50) | none | only side data worth a frame; ends looking down the right side = hand-off to the rear; weak lower rim -> 4 beats only | **REUSE** v1 s04_wheel (31 fr), src_fps to fit 1.905 s |
| 5 | rear | s5_rear | b44-62, 20.985-29.557 (8.57 s; every 2 beats = 0.111) | rear bumper corner -> rear bumper inner face -> **rear panel, wiring, exhaust behind it** -> trunk lid up, boot | cam(0,-150,10,2.0,[-0.35,1.45,0.50],45) -> cam(0.25,-165,24,3.6,[0,1.80,0.30],40) -> cam(0.36,-170,42,2.0,[0,2.00,0.00],45) -> cam(0.47,-172,44,1.9,[0,2.00,-0.03],45) (inner face) -> cam(0.58,-160,14,1.6,[-0.10,1.55,0.40],45) -> cam(0.68,-156,13,1.5,[-0.10,1.55,0.38],45) (structure hold) -> cam(0.85,-125,40,2.8,[0,1.30,0.70],40) -> cam(1,-118,46,2.4,[0,1.25,0.68],40) (side-high: lid edge-on, into the boot) | rb: 0.11-0.25 -> [0,0.60,-0.50] (back + down into black); spin 0 -> -95 over 0.20-0.36; 0.47-0.58 -> R_OUT (drops out of frame). trunk: 0 until 0.68, -> TRUNK_OPEN over 0.68-0.80, holds. front parts hidden, hood HOOD_OPEN (out of frame) | hero beat 2 (C): the Rear End All Removed data behind the bumper gets its own held look; trunk opening only because Rear End Trunk Open exists and registers (D); one continuous rear sequence | NEW, 131 fr |
| 6 | top (finale a) | x1_layers | b62-68, 29.557-32.414 (2.86 s) | rear assembly rising into layers, then the front layers entering frame | cam(0,150,32,3.6,[0,1.30,1.00],40) -> cam(1,115,62,6.0,[0,0.30,1.20],40) (high rear-left crane over the top; never straight down - Miata lesson) | from R_OUT / F_OUT (fb, li visible again): trunk 0.00-0.40 deg TRUNK_OPEN -> 0 and off -> LAYERS; rb t0.10 R_OUT -> t0.40 [0,0.75,1.30] spin -80 -> t0.55 LAYERS (up behind the car, then in); hood 0.30-0.70 -> LAYERS; fb t0.35 F_OUT -> t0.75 [0,-0.70,1.20] spin 80 -> t0.85 LAYERS; li t0.45 F_OUT -> t0.85 [0,-0.95,1.60] -> t0.95 LAYERS | progressive explode, rear first then front (Temerario), close on the assemblies; first left-side/top angle of the reel | NEW, 45 fr |
| 7 | whole (finale b) | x2_reassemble | b68-76, 32.414-36.224 (3.81 s); b74 at t=0.75 | whole layered car -> parts home -> clean car | cam(0,95,38,9.0,[0,0,1.00],40) -> cam(0.45,100,30,8.4,[0,0.05,0.80],40) -> cam(1,118,13,8.2,[0,0.15,0.55],40) (left side high -> left-rear 3/4, whole car ~73 % width) | 0-0.20 LAYERS -> LAYERS_DRIFT (lin). Home, outer layers last, each part straight down then sliding in: hood 0.20-0.45; trunk 0.25-0.50; fb 0.30-0.50 -> [0,-0.45,0] spin 0, 0.50-0.62 -> home; rb 0.35-0.55 -> [0,0.45,0] spin 0, 0.55-0.67 -> home; li 0.45-0.62 -> [0,-0.55,0], 0.62-0.72 -> home. `visible`: exploded set [0,0.75), car2 [0.75,1.01) = clean-car swap on b74 (C5 lesson). vf fade out st=3.31 d=0.5 | reassembly + fade; ends on a whole-car angle not used anywhere else (opener is front-right) | NEW, 59 fr |
| 8 | logo | logo | b76-end, 36.224-38.893 (2.67 s) | small logo ~35 % width | static | - | final hits 37.653 / 38.129 under it | RE-MAKE card smaller (tools/logo_card.py, no Blender) |

## Labels (feedback C; ScanHUD `label` items, Inter Display off-white, max two, outside the silhouette, above the bottom 20 %)
| shot | label | on screen | gate |
|---|---|---|---|
| s2 | MOUNTING POINTS | b18-b21.5 (8.605-10.271), next to the tipped bumper | confirmed (tabs visible in v1 s06 f59) |
| s2 | FRONT BUMPER REMOVED | b24-b27.4 (11.462-13.10), over black beside the structure | confirmed |
| s2 | CRASH BEAM | same window as above | **only** if the s2 hold frame shows a distinct horizontal reinforcement beam; v1 resolution can't tell it from the radiator core support -> default none |
| s3 | ENGINE BAY | b34-b38.5 (16.224-18.38) | confirmed (intake, cam cover visible) |
| s5 | REAR BUMPER REMOVED | b54-b56.6 (25.748-26.98) | confirmed |
| s5 | EXHAUST | same window | only if the pipe under the rear panel reads in the s5 hold frame (likely) |
| s5 | TRUNK OPEN | b58-b61.4 (27.652-29.27) | confirmed (state scan exists) |
None on s1, s4, x1, x2, logo. No numbers.

## Cut list (v1 -> v2)
- s01_side: cropped and repeats the whole-car view (IoU 0.82 vs s02). s02_front34 / s03_rear34: turntables; s03 is a rear
  exterior before the front story (ping-pong). s08_top: rotating top-down, nothing new. s09/s10/s11: wide, all parts at once,
  three repeats of one view. s05_lamp and s06/s07 are replaced by closer section shots (s2, s3, s5).
- Inside v2: no shot ends on a static hold of a finished state; no section is revisited (front s2, engine s3, wheel s4,
  rear s5, top x1; whole car only s1 and the exploded x2 from a different side).

## Hold list (> 0.75 s)
- s2 0.80-1.00 (1.9 s) lin creep on the front structure: hero data, label reading time (C).
- s3 0.55-1.00 (2.6 s) push-in on the engine bay while it fills the frame: label + detail.
- s5 0.58-0.68 (0.86 s) structure hold: labels; 0.85-1.00 (1.3 s) slow push into the boot.
- x2 0.00-0.20 (0.76 s) layers drifting: the one moment the full layered car reads before it collapses.
- logo 2.67 s: carries the last two hits; music ends 38.89.

## Render budget (15 fps, 75 %, 12 spp, ~12 s/frame)
New: s1 60 + s2 145 + s3 88 + s5 131 + x1 45 + x2 59 = **528 frames ~ 1 h 46 min**, one at a time, persistent data off,
then per-frame luma scan. Render one still per hero pose first (s2 t=0.55 and 0.9, s3 t=0.8, s5 t=0.45, 0.63, 0.95,
x1 t=1, x2 t=0.1) at 30 % to check framing (A), the bumper inner faces, lamp clearance against black and the label gates.
Reused unchanged: s04_wheel (31 fr). Not reused: every other v1 dir (wrong framing or content).

## Timeline for project.yaml
beats: [3.843, 13.366, 15.272, 19.081, 20.985, 29.557, 32.414, 35.271, 36.224]
s1 0-3.843 (first clip one frame short) | s2 -13.366 | s3 -19.081 | s4 -20.985 | s5 -29.557 | x1 -32.414 | x2 -36.224 | logo -38.893.
