# Toyota GR86 / Subaru BRZ (gen 2) - sources

Scan-only reel (no shop footage, no text). Engineering Drive folder `Toyota GR86 BRZ (Gen 2)`
(1iCTuuZ68NihMw2SA6jHswff9Wji09dWm), fetched with `ive fetch-drive` to `/home/user/media/toyota-gr86/scans/`.

**Hero car: `BRZ Full Car`** (18vYkgpx33dUKRo0FXPAmp80ynbVYck3z, 22.6M tris). All "GR86 Bomex ..." state scans are in
its raw Artec frame; `GR86 Full Car` (1zw3Rtk..., 20M tris) is a different capture/frame with 0 % overlap, so unused.
The car is a BRZ (BRZ badge on the trunk lid, slatted grille) with aftermarket wheels.

Frame: `tools/level2.py` -> `/home/user/media/work/gr86/level.json` (PCA axes, nose -Y from the Front Bumper Only scan,
tyre-contact plane z=0), applied to every scan with `tools/level.py apply`. Prepped with `--like car4.json`.

| Scan | Used for | Registration to BRZ Full Car (tools/regcheck.py) |
|---|---|---|
| BRZ Full Car | 4 mm `car4` (wide shots), 2 mm front/rear crops (close-ups) | - |
| Bomex Front Bumper Only | exploded part (ICP pinned: xf/front_bumper_icp.npy) | 78.6 % overlap, median 5.2 mm, ICP 0.43 deg (<= 6 mm move) |
| Bomex Rear Bumper | exploded part (ICP pinned: xf/rear_bumper_icp.npy) | 74.1 %, 5.1 mm, ICP 1.23 deg (<= 16 mm move) |
| Bomex Hood Open | engine bay under the opening hood / exploded hood | 48.0 %, 3.8 mm (no correction). Open hood itself not captured |
| Bomex Bumper Hood Removed | front structure fill (below z 650 mm) | 27.6 %, 3.9 mm |
| Bomex Rear Bumper Removed | rear structure fill | 63.2 %, 3.2 mm |
| Bomex Trunk Open Bumper Off | rear fill below z 750 mm | 35.8 %, 3.8 mm |
| Bomex Trunk Open | not used (lid not cleanly captured) | 74.2 %, 2.8 mm |
| Bomex Side Mirrors Removed | not used (left mirror on the car is a thin broken capture) | 92.3 %, 2.6 mm |

Panels: hood = car tris missing from Hood Open + filled top-view mask (`tools/hood_mask.py`); hinged at its rear edge
(pivot 0.0095, -0.6236, 1.0916 in Blender m). Checks: `/home/user/media/work/gr86/reg/*.jpg` (red/cyan/yellow over grey).

Not used: Bomex CAD, `BRZ-GR86.blend`, `BRZ.fbx`, `Juan BRZ.stl` (other car), aftermarket parts, GR86 Front Lip (product).

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com (Shopify CDN) -> `remotion/public/illumaesthetic_logo.png` (gitignored).

## v3 additions (user feedback on v2, 2026-11-11)
| Scan (Drive id) | What it is | Placement in the car frame |
|---|---|---|
| Bomex Reverse Light (1NjzGjVILnufEeFVD7vkc4ajDlLTvhS2f) | rear reverse-light bar, own capture; only the socket/back side is well captured | tools/register_part.py on rear_bumper (24 PCA hypotheses + ICP), flipped 180 deg so the sockets face into the car; sits in the lower slot, x 0, z ~300 mm (xf/reverse_light_flip.npy; median 9.8 mm - part is mostly hidden inside the bumper) |
| Bomex License Plate Light (1oHbDud2DL5qj9t7LW2wtuE5wv_Sjmb_9) | ONE plate lamp, own capture | register_part on rear_bumper: median 2.3 mm, 65 % < 4 mm; lamp recess above the plate (xf/plate_light.npy) |
| Bomex License Plate Lights Removed (1KQKw4Dlvia07gB51ogVDGYwZDi1AIB2v) | rear bumper with plate lamps out (partial capture) | 64 % overlap, ICP 75 mm |
| Bomex Side Markers (1CmLE_CsuaAdSjyun5h8VSQ_KezNBZKhR) | FRONT bumper side markers (y -1850..-1680 mm) | 82 % overlap, ICP 84 mm |
| Bomex Side Markers Removed (1j_9ZUKnY-QjGureHnEUUSCaAnGlZUlLe) | front bumper area, markers out | 90 % overlap, ICP 7 mm |
| Trunk Open (already fetched) | captures the cargo floor/opening only (z < 875 mm); the raised lid itself is NOT in the scan | - |

Hood fix: parts/hood_m.stl ran 100-230 mm up the windshield (Hood Open hides the lower glass, so the top-view mask
included it) -> tools/hood_trim.py cuts it at the measured cowl gap (y -1110..-820 mm) -> parts/hood_t.stl.
