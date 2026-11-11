# Honda Civic 11th gen (FE1 Si sedan) — sources

Scan-only Temerario-style reel: no IRL footage, no text. Media lives in `/home/user/media/honda-civic-11/`
(raw + decimated scans, prepped .blend) and `/home/user/media/work/civic/` (specs, renders, checks). Nothing is committed.

## Drive folder `Honda Civic (11th Gen)` (10Ci7sUypOlHypCK7lW2bsSPSAsazcH14)
Full recursive listing: `/home/user/media/honda-civic-11/drive_list.txt` (service account, `ive.fetch._drive_session`).
Three bodies: `Honda Civic FL5 Type R/`, `Honda Civic Si (FE1)/`, `Honda Civic Sport (FL2)/`.

### Used (FE1 Si sedan, one Artec frame)
| File | Drive id | Role |
|---|---|---|
| `civic Facelift FE1 Full Car.stl` (1.25 GB, 2025-10-22) | 1RIThsxwQgD_KB-58-JiL0y6x1HycU8LZ | base car (4 mm, ground-cropped, holes filled) |
| `civic PreFacelift FE1 Full Scan.stl` (2025-10-23) | 1pz9b0U7U4Mw47kUjSACcYEhOl9aXENul | same car before the bumper swap; donor for hood/rear-glass hole fill only (ICP 0.2 deg / 4 mm) |
| `civic Trunk Open.stl` (2.9 GB, 2025-10-22) | 1GWuGnnesqLPSifi7-tw0M3jxWRZ0uMty | open trunk lid + trunk interior (37 % within 6 mm of the car = registered) |
| `civic Trunk Open no trim.stl` (2025-10-31) | 1_PwSlgh20XSV4ArEAY1ngPMZ1A7vls6q | lid with the inner trim off (34 % within 6 mm) |
| `civic Door Open.stl` (2025-10-24) | 1tx_topVcYMblnSs9hNvBOmqTpcq5gKzb | right side with both doors open: sill, A/B/C jambs up to ~0.85 m, NO door panels (30 % within 6 mm) |

### Looked at, not used
- `FL2 Full Car.stl` (suggested) + `Full Car Hatchback FL2_1..5` (= sections of it, all within 3 mm) + `civic Civic Hatch Rear End` (= FL2_5):
  hatch, same shop frame, but rear wheel broken and a hole in the roof. FE1 is the cleaner capture and owns the state scans.
- `Honda Civic Sport (FL2)/Trunk Wing Scans/civic Trunk Open.stl` = the same sedan trunk scan as FE1 `civic Trunk Open` (identical stats).
  `civic Trunk Closed` fits FL2 at 71 % within 6 mm. Wing / drill-template / HPD-hole scans are wing-product work, not used.
- `Civic Si Si rear end.stl`, `Civic Si Si trunk open.stl` (2024): different frame (1 % within 6 mm), older session.
- `CHB Round 4 Rear Bumper (lip installed)`, `CHB Round 4 Rear Lip (Printed)`: printed prototype lip — skipped per brief.
- `civic Civic Pre-FL Front Lip (Unwarped)`, FL5 Type R folder, Hybrid hatch: other products / other cars.

## Scan defects (measured, see editlog)
- Hood + rear-glass see-through holes (dark paint dropout) → filled (tools/patch_holes.py + tools/fill_top.py).
- Right-rear wheel = tyre ring only, no rim, in both FE1 captures → hero angles from the car's LEFT side.
- Prop sheet under the rear-left bumper + floor scraps under the front axle → removed (tools/deground.py).

## Dropbox `/2. Illumaesthetic Videos/1. Video dumps/Civic 3D Scanning Short`
9 clips, Oct 30–31 2025 (`Video Oct 30 2025, 7 55 14 PM.mov` … `2025-10-31 14-29-30.mp4`). The dates fall inside the
FE1 scan sessions (Full Car Oct 22, Door Open Oct 24, Trunk Open no trim Oct 31), so the dump shows the **FE1 Si sedan**.
Not watched: the Dropbox preview/download hosts are blocked by this environment's network policy (proxy 403), as the
sibling sessions also found. Not needed — this reel is scan-only.
