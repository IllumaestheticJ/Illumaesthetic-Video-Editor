# Toyota GR Corolla - sources (scan-only Temerario-style reel, WIP)

Drive folder `Toyota Corolla Hatchback (E210)/GR Corolla` (16SiY5GVJJHCmoJxwSKIOx-82zJmqHayw; the brief's two IDs are the
same folder). Fetched with `ive fetch-drive` to `/home/user/media/toyota-gr-corolla/scans/`. Full listings:
`/home/user/media/toyota-gr-corolla/drive_*.tsv`. Prepped frame = car4.json (front -Y, car's right -X, floor z 0).

| Scan | Reg. to car | Used for |
|---|---|---|
| GR Corolla Full Car.stl (17j3c0hl..., 16.7M tris) | canonical | car4w (4 mm) / car2w (2 mm), rear wheels added |
| GR Corolla rear.stl (2025-04) | 1.9 mm | real rear-left wheel (+ partial rear-right) -> tools/wheelfill.py |
| GR Corolla Chassis Stripped.stl (ARA, 1.2 GB) | 2.0 mm | exploded/opening base: stripped shell + cage |
| Bumper (1.2m).stl (2023 front bumper) | 3.6 mm | exploded part |
| GR Corolla bumper .stl / bumper inner side.stl | 1.9 / 2.9 mm | rear bumper part (outer + inner) |
| GR Corolla diffuser.stl | 3.0 mm | exploded part |
| ... trunk open (removed).stl (2023) | 2.0 mm | cargo-area fill under the opening hatch (tools/cargofill.py) |
| rear bumper removed / diffuser removed / crash bar removed | 2.2 / 1.9 / 3.0 mm | registered, looked at; not needed (chassis covers the rear) |
| Front Clip (16M) | 1.33 mm, 0 corr. | crop of the full car - nothing new |
| Mirror, Car No Mirror, Core Hood Underside, Facelift Front Only, Engine Bay Stripped, beams/ducts, ARA Rear Crash Beam | other frames | not used |

Skipped: WRC wing iterations / prototype wings, off-road light pods/roof/skid plates (accessory prototypes), CAD.
Scan defects: full car has no rear wheels (fixed left; right-rear partial -> rear views from the left);
cargo floor under the hatch has capture holes.
Logo: IllumaestheticLogo_V2COMPLETE_1.png from illumaesthetic.com -> remotion/public/illumaesthetic_logo.png (gitignored).
