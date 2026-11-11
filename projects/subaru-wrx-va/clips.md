# Subaru WRX VA (Impreza VA) — scan reel sources

Scan-only reel (no IRL footage, no text). Engineering Drive folder `Subaru Impreza VA`
(1-gWQoPNq_G2dBYjOzi-mmVq4vkQvQU2N), listed recursively with the service account.
Media: `/home/user/media/subaru-wrx-va/` (dec = decimated raw frame, lvl = levelled, clean = ground removed,
comp = composites, blend = prepped; all prepped `--like blend/car.json`).

## Used (same Artec frame as the full car — tools/regcheck.py, then red-over-silver renders in regcheck/)
| key | Drive file | session | what it is | registration |
|---|---|---|---|---|
| car | VA WRX Full car Exterior.stl (1bhdDkjESTDKAI1J66YO7VbDCm-A_SOZJ) | 2024-03 | whole car, wheels, STI wing; 25M tris | base; level.json |
| hoodopen | Fog Bezel and Hood Scoop Scans/VA WRX Hood Open .stl | 2024-01 | whole car, hood propped, engine bay | median 1.7 mm |
| fbumpremoved | …/VA WRX Front End Bumper Removed.stl | 2024-01 | front end, bumper off (hood also propped) | 2.1 mm |
| fbump | …/VA WRX Front Bumper Only.stl | 2024-01 | front bumper, outside + inside | 2.9 mm |
| scoop / scoopremoved | …/VA WRX Hood Scoop.stl, …Hood Scoop Removed.stl | 2024-01 | scoop part / front end without scoop | 5.7* / 1.7 mm |
| fogL / fogR | …/VA WRX Front Left/Right Fog Bezel.stl | 2024-01 | bezels | 2.5 mm |
| trunkopen / rear | Trunk/Trunk open.stl, Trunk/Rear.stl | 2024-04 | rear, lid open / closed | 1.9 / 1.8 mm |
| wing | Trunk/Wing.stl | 2024-04 | uprights + blade underside | 1.9 mm |

*scoop: small curved part, 89 % within 15 mm; red-over-silver render sits on the hood.

## Not used
- Headlight Project / Project 29 * (2023-09): own frame; global registration lands it on the front (3.5 mm) but it
  is a different car (different wheels) and front-end only. Print Files = headlight design parts (not scan states).
- Rear Bumper Scan/VA Bumper Back.stl (2025-09): own frame, rear end with bumper on (not a part).
- Production/WRX VA base spoiler.stp: CAD, not scan data (brief: scan data only).
- 15-17 / 18-21 Front End, Facelift VA front quarter (2022): older front-end sessions, own frames.

## Composites
- `comp/explode_base_4mm` — car − bumper − scoop (+ new geometry of scoop-removed, bumper-removed) − wing (tools/wing_split.py)
- `comp/fbump_nofog_2mm` — bumper with bezel zones carved; `comp/wingfull_2mm` — car's wing skin + Wing.stl
- `comp/trunk_4mm` — tools/trunk_comp.py
