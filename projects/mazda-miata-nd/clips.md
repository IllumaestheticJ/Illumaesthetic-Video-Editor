# Mazda Miata ND - sources

Scan-only Temerario-style reel: no shop footage, no text. Engineering Drive folder `Mazda Miata ND`
(1BrKdyE8wZlAG-KgEFoUvkHe9dcQK2CIX) / `Scan`, listed recursively with the service account and fetched with
`ive fetch-drive` to `/home/user/media/mazda-miata-nd/scans/raw`, decimated to `.../dec`.

Frame: the raw Artec export is **upside down** (ground at +Z, long axis X). `tools/level.py` flips it 180 deg about X and
reuses the Huracan RANSAC levelling; one rigid transform (`/home/user/media/work/miata/level.json`) for every scan.
Levelled + `ive crop` + `ive prep` -> `car4.json` (front = -Y, car's right = -X, ground Z=0). Every scan prepped `--like car4.json`.
Car: 3,908 mm long (ND spec 3,915), 1,218 mm tall.

| Scan (Drive name) | Tris | What it is (looked at) | Used for |
|---|---|---|---|
| ND Miata ND Full Car (2026-11-10, 1.25 GB) | 25.0M | whole car on the ground, wheels scanned (6-spoke) | 4 mm wide shots, 3 mm, 2 mm front half for close-ups |
| Front Bumper | 0.59M (3 mm) | front bumper skin | s5 slides off; exploded part |
| Bumper Off Hood Open | 1.64M | engine bay + front structure, hood propped open (only a strip of the hood captured) | fill under hood/bumper; hood hinge fit |
| Front End Hood Open | 0.97M | front with bumper on, hood open, debris | not used (Bumper Off Hood Open covers it) |
| Rear Bumper Inside | 0.75M | rear bumper as a part | s6 slides off; exploded part |
| Rear bumper removed trunk closed | 1.05M | rear structure, crash bar, exhaust | fill under rear bumper |
| Rear End Trunk Open Bumper Removed | 0.79M | trunk interior, lid propped open | trunk fill; trunk-lid hinge fit |
| Rear End Trunk and Lights Removed | 1.34M | like above, lamps out | second hinge fit only (agrees: 79 vs 86 deg); not in shots |
| Side Skirt Off | 0.71M | right sill without skirt + jack stands | skirt extraction (diff) + sill fill (stands dropped) |
| Side Skirt Off, Door Open | 0.54M | door jamb / A-pillar / sill only - **no door captured** | not used (no door move) |
| Mirrors Only | 0.14M (2 mm) | both mirrors, registered | exploded parts (split L/R) |
| Mirrors Removed | 3 mm | car around the mirror mounts | fill under mirrors |
| Front Bumper Markers / Rear Markers / License Plate Lights | small | lamp parts | not used (too small to read) |
| ND Trunk Closed / Half Open / Open (2026-08-04) | ~0.6M each | trunk lid, **different frame** (2 % overlap) | not used |
| NDMiata*.png | - | product renders | not used |

Panels with no isolated scan were cut from the full-car skin: hood and trunk lid along their shut lines (`tools/extract.py`,
traced on a top render), side skirt by diffing against `Side Skirt Off` in a sill box. Hinges fitted from the panels captured
propped open (`tools/hinge.py`): hood -43.7 deg about pivot y -0.458 z 0.889 m (median 3.0 mm), trunk +85.7 deg about
y 1.336 z 0.987 m (7.6 mm). Composites via `projects/ferrari-296/tools/composite.py`.

Registration checks: `tools/regcheck.py` (median 1.2-4.8 mm for every 2026-10-29 scan) + red-over-grey renders in
`/home/user/media/work/miata/reg/` and closed/open composite checks in `/home/user/media/work/miata/chk/`.

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com/cdn/shop/files/ -> `remotion/public/illumaesthetic_logo.png` (gitignored).
Music: original track generated for this reel by the coordinating session (see project.yaml / editlog).
