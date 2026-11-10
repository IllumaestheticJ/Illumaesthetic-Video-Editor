# Scan data → Blender: what actually works on the work box

Machine reality: 4 CPU cores, 15 GB RAM, no GPU. Blender 5.3 headless, Cycles CPU only
(EEVEE aborts without a GPU).

## Where scans live
Engineering Google Drive, one folder per car, e.g. `Nissan S13 (Hatchback)` with one STL per
**state**: full car, bumper only, bumper removed (chassis), headlights up, etc. All states are
exported in the **same coordinate frame** (Artec), so they line up after the same normalisation.

The Drive connector's search misses these; the service account sees them:
`python -m ive fetch-drive <file_id> /home/user/media/<car>/scan` (streams GB files to disk).
Find IDs with the Drive API via the service account (see `ive/fetch.py`).

## Steps
| Step | Command | Why |
|---|---|---|
| decimate | `ive decimate raw.stl car_4mm.stl --cell 4` | 25M-tri (1.2 GB) STL OOM-kills Blender. Vertex clustering streams it: 25M → 3.3M tris in 14 s |
| crop | `ive crop car_4mm.stl car_clean.stl` (parts: `--footprint-from car_4mm.stl`) | removes scanned asphalt, paint lines, wheel stops |
| prep | `ive prep --scan car_clean.stl --out car.blend --units mm --drop-islands 3000` | mm→m, centre, sit on Z=0, delete debris islands |
| prep parts | `ive prep --scan bumper_clean.stl --out bumper.blend --like car.json --drop-islands 1500` | **same transform** as the car so parts line up |
| composite states | numpy: drop regions from the full car, add the part scan (see `projects/240sx-scan/editlog`) | e.g. "bumper off, hood open" |

## Ground-removal rules that survived (and one that didn't)
- keep triangles inside the car's XY footprint measured above wheel-hub height
- drop up-facing (n.z > 0.9) faces in the bottom 22 cm — the car's underside faces *down*
- drop anything below 12 cm beyond the bumper overhangs (paint welded to tow hooks)
- drop islands that never rise above 15 cm
- ✗ "delete everything near the local lowest point" — under the car there is no ground, so
  the exhaust and diff *are* the local minimum and got deleted.

## Render budget
- 1080×1920, 16 spp: ~25 s/frame. 75 % res, 12 spp: ~18 s/frame.
- Render scan shots at **15 fps** and let `assemble` interpolate (`interpolate: true`) → halves time.
  Smooth camera moves on black interpolate cleanly; fast part motion may ghost — render those at 30.
- `use_persistent_data` is on; still re-syncs per frame with animated objects.
- Don't run npm installs / Chrome renders concurrently with Blender: 110 s/frame instead of 18.
- Debug framing at `--res-pct 30 --samples 8` (≈3 s/frame) before queueing finals.

## Exploded views
`ive render ... --explode "part.blend:dx,dy,dz:start:end[:x180:rstart:rend]"` (repeatable, fractions of
the shot). Parts move first, then flip about their own centre. Stagger parts (skin, then beam) and
let each flip land on a beat. Pull the camera back 20–30 % (`--move pull`) only as much as needed
to keep parts in frame — the match shot must still start on the solved camera.

## Looks
`silver` (house), `clay`, `scan` (cyan rim + wire), `wire`, `points`, `xray`, `color`, `sweep`.
See `knowledge/style-guide.md` for when to use which.

## Vertical framing
Portrait frames are narrow: a whole car needs ~7 m camera distance at 26–30 mm. Side profiles
at <6 m crop the car. Check at 30 % res first.
