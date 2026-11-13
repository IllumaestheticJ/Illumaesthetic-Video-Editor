# Porsche 911 GT3 vs GT3 RS (992) - split-screen comparison reel (sources)

Splits off from `projects/porsche-gt3rs-992` (v5/v6). User: "make a version that splits off from this, that also showcases
the GT3 side-by-side. Since they are a similar platform, but the GT3 was far more stripped apart (tail lights, bumpers, etc)".
Scan only, no IRL footage. Layout: stacked split-screen, 1080x960 per car (RS top, GT3 bottom), same cut frames.

## Top panel - 911 GT3 RS (992)
Centre band of the 9:16 renders from `projects/porsche-gt3rs-992` (tools/shots_v6.py; see that project's clips.md):
v2_sh1, v6_sh3, v6_sh4, s5_wing, v3_sh6, v6_sh7, v6_wheel, v6_under, v6_sh9.

## Bottom panel - 911 GT3 (992)
Drive folder "Porsche 911 GT3 (992)" (1YeY5ba-6LeKsXQWDX6CCQApFHuuxBUlX), 2023-11-23 Artec session; ids and registration
figures in `projects/porsche-gt3-992/clips.md` (all registered at identity, re-checked here by red-over-grey renders:
/home/user/media/work/gt3vs/states.jpg). Media in /home/user/media/porsche-gt3-992 (not in git).
Levelled with `level.py fit` on the 4 mm car + `flip_y` (front = -Y, car's right = -X); 8 debris triangles below the ground
dropped before prep (they lifted the car 25 cm); everything prepped `--like car4.json`.

| Piece | From | Notes |
|---|---|---|
| base `comp_gt3` | full car minus the parts below + NEW geometry of the state scans | fills: Front Hood Open (frunk, z < 900 mm), FR wheel well, SideSkirt Removed, Rear End No Diffuser, rear wing mounting reference, Rear End Trunk Open Lights Out |
| hood lid | full car where the "Front Hood Open" state has no surface (tools/lid.py + biggest.py) | hinges -50 deg about its rear edge over the real frunk scan |
| tail-light bar | full car where "Rear End Trunk Open Lights Out" has no surface, minus the spoiler/bumper/wing zones | lifts off |
| FR wheel | full-car triangles inside the wheel cylinder (centre from the tyre contact patch, r 352 mm) | slides off its axle; "FR wheel well" state behind it |
| Rear Bumper, Rear Diffuser, Rear Lip, Rear Wing, rear duckbill, SideSkirt | part scans | exits from a direction search, checked with tools/clipcheck.py |

Known: the frunk floor has a scan hole (black opening); the bumper-off structure is fragmented above the exhaust.
Music: user's track (Alkitran - Original Mix) from 171.651 s, 127.0 BPM (see porsche-gt3rs-992 project.yaml).

## v3 additions
- `GT3-992-ExhaustOn-UWT.stl` (Drive 18jZHt8jP5OBeEsv4jh9ETOX39OfMPqRZ, Exhaust folder, 2026-06-08, ASCII STL): rear engine /
  exhaust from below. Own frame; registered with tools/multireg.py onto comp_gt3 (24 axis starts, best 0.53 fit at 8 mm),
  only its NEW geometry added (tools/addnew.py, >8 mm from the base, >14 mm from bumper/diffuser/lip) -> comp_gt3b.
  `GT3-992-ExhaustOn-WT` is the same capture made watertight (fake skin) and `GT3-ExhaustCavity-WithExhaust` a subset: not used.
- `Nikitas GT3 Full Underbody + Bumper Off.stl`: FRONT bumper off, rear bumper on; not used.
- Website end card: Playwright screenshots (1440x900 @2x) of /products/porsche-911-gt3-rs-3d-scan and /products/porsche-911-gt3-3d-scan
  (www host), "Drag to rotate" hint hidden; remotion/public/web_gt3rs_listing.png, web_gt3_listing.png; props in webzoom.json
  (composition WebZoomSplit). Viewer region [435,368,1060,942] px fills a 1080x960 panel at frame 0.
