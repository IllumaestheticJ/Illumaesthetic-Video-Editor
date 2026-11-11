# Mazda 3 (gen 4) hatch - scan-only reel sources

No IRL footage (scan-only Temerario style). Media in /home/user/media/mazda-3-gen4/ (not in git).

## Scans (Drive "Mazda 3 (Gen4)" 1taMqlzL_RH6mVa0aWxMmNmVFeSGbzFHU)
| file | id | use |
|---|---|---|
| Scans/Full Car.stl (2.92 GB, 58.4M tris, Artec) | 1ax2oMSjUILM_e8RAKF450b_XTP5QjkuD | base car: 4 mm (3.8M) full shots, 2 mm crops for close-ups |
| Scans/Mazda 3 (Gen 4) Rear Wing.stl (Artec) | 1PBD6tUs_WT9Jd-a7H2AWn1ZnIvTcQPcF | roof wing part (lifts off in s6/s8), registered at identity |
| Scans/Mazda 3 (Gen 4) Wing Removed.stl (Artec) | 1Ki8z-P9LEs0VKnHU9U2GOlYX1BE6hNuG | state: hatch top with wing mounts -> wing-off base |
| Scans/Mazda 3 (Gen 4) Side Skirt Door Open.stl (Artec) | 1CGMA2OS0YibM_inyk1x6TYQuXsCvEeT6 | registered (1.1 mm) but sill/jamb only below 0.86 m - not used (no door part / cabin) |
| Mazda 3 CAD/Hatch Upper Trim Panel.stl (inches, own frame) | 1ag5bNKJpbKoHN20P0ZCRRnyCQXppSmPb | = the rear wing (FPFH+ICP to Rear Wing fit 0.964, rmse 3.3 mm, covers 93 %); not shown twice |
| Mazda 3 CAD/Hatch OEM Aero Kit Spoiler.stl (inches, own frame) | 1yje3JhcAqH_FtgNQbrFeqhn1A_C2M-Ah | does not register to this car (fit <= 0.45); floating part in the explode only |
| Scans/Floor Mats Only.stl | 1nmaGgXApy36rysxEHiRqI5_byt6748IK | skipped (interior mats) |
| Mazda 3 CAD/*.STEP | - | skipped (CAD, not scan data) |

## Scan facts (measured, for anyone adding text later)
- Full car STL header: 58,420,431 triangles. Levelled length 4,462 mm (spec 4,460), width 1,931 mm incl. mirrors.
- Car was scanned raised ~15 cm on scissor jacks; front-left wheel is a hub without tyre in parts; tyres end ~10 cm above the floor (contact patch not captured).

## Prep chain
decimate (4/2 mm) -> huracan-evo/tools/level.py (level.json) -> ive crop -> tools/clean_car.py -> ive prep (car4.json canonical) -> parts/crops --like car4.json.
Composite: tools/wingoff.py. Spoiler/trim: tools/scale_stl.py x25.4 -> a90-supra/tools/globalreg.py.
