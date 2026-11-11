# Subaru WRX VB (2022+) - scan-only Temerario-style reel: sources

No IRL footage (brief: scan only, no text). All geometry from the engineering Drive folder
`Subaru WRX VB (2022+)` (1Na7ti-IDQ-kCoT5p8iMf0pxaCxENAXaZ); full recursive listing in `drive_listing.tsv`.
Downloaded to `/home/user/media/subaru-wrx-vb/scans/`, decimated (out of core) to `dec/` (car 4 mm + 2 mm, parts 3 mm).
Only `Scan Files/` is scan data; `Print Files/`, `Production/`, `Front Lip/` are CAD/print files (not used), and the
F1 brake light / Hella fog light / reflector folders are aftermarket parts (not downloaded).

## Full car
| file | tris | notes |
|---|---|---|
| Scan Files/Full Car.stl (1Pk6kWYjMuQYaGGaxpG63dbePChVl-vLW) | 25,013,694 | Artec export, Z up, front -Y, car's right -X; 4,663 x 1,889 x 1,458 mm after ground crop. Wheels scanned (rims + brakes). Glass not captured (dark holes). Both licence plates embossed -> flattened (tools/flatten_plates.py). |

## Part / state scans (regcheck.py: % of points within 10 mm of the full car, median distance)
| scan | frame | use |
|---|---|---|
| Front Bumper (Inside, Parts included) | car, 62 %, 3.9 mm | front bumper part (outer + inner + grille) - s5, s7 |
| Front Bumper Lower Garnish | car, 74 %, 3.6 mm | part - s5, s7 |
| Front Grille | car, 90 %, 2.4 mm | (included in the bumper part) |
| Front Bumper Inside (Parts removed) | car, 60 %, 4.1 mm | not used (bumper shell only) |
| VB Rear Bumper (Updated) | car, 84 %, 1.9 mm | rear bumper part - s7 |
| Rear Bumper Only | car, 90 %, 2.2 mm | not used (Updated version preferred) |
| Front / Door / Rear Flare | car, 83-92 %, 2.5-3.3 mm | right-side wheel-arch cladding parts - s7 |
| Side Skirt Only | car, 41 %, 2.2 mm | right side skirt part - s7 |
| Front Removed (all), Front Bumper Parts Removed, Bumpers Removed | car, 1.5-2.2 mm | fills under the front bumper (crash beam, radiator support, lamp backs) |
| Rear Bumper Removed, Duckbill Scan | car, 1.3-1.5 mm | fill under the rear bumper (rear beam, exhaust) |
| Side Skirt Off Doors Open | car, 4.3 mm | fill under the skirt (sill) |
| VB Trunk, Inside Trunk, No Trunk, Rear Bumper Trunk Open, GT Wing Trunk Open, WRX Trunk Holes | car | trunk-open attempt (tools/trunk.py) rejected - hinge fit 10.8 mm, tub capture has holes |
| Side Skirt On Doors Opened | car | not used (door fragments only) |
| vb wrx headlight * (5 states), VB Bumper Inside | OWN frame (0 % on car) | not used |
| Print Analysis/VB lower Wing.stl | - | not downloaded (print analysis, not a scan state) |

## Composites (raw mm, then `ive prep --like car4.json`)
- `base_xnp` = full car minus front bumper, garnish, rear bumper, right flares x3, right skirt (projects/ferrari-296/tools/composite.py, cut 9 mm)
  + new geometry from the state scans above inside each removed panel's zone (+60 mm); plates split/flattened.
- Parts land back exactly where they were cut out (all in one frame) - checked with the colour overlay chk/xb.jpg.

## Logo
`remotion/public/illumaesthetic_logo.png` (gitignored) - IllumaestheticLogo_V2COMPLETE_1.png, 6135x1059 RGBA, from the
illumaesthetic.com header (Shopify CDN, fetched via headless Chromium because the site's bot check blocks curl).
