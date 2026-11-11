# C5 Corvette scan process - clip notes
Sources (Dropbox):
- `/1. Epsilon Plus Videos/1. Video dumps/Corvette Footage/` - DJI (Osmo, 23.976 fps, SDR bt709). Jul 15-16 clips (0028-0054) are a red MR2 Spyder,
  NOT the C5. Jul 17 18:16-19:06 (0055-0080) = the stock yellow C5 outdoors being stripped. Jul 17 night (0090-0103) = black prototype
  widebody front being fitted (no scan matches that state).
- `/2. Illumaesthetic Videos/1. Video dumps/C5 Corvette/` - same Jul 17 21:53-22:15 clips (0096-0103) plus Jul 21-23 (0114-0144):
  hood mould / fibreglass layup, prototype kit fitting, tripod long takes (0121-0143 are 9-17 GB). No handheld-scanner footage found in either folder.
Downloaded: LRF proxies to /home/user/media/c5/lrf, full clips used to /home/user/media/c5/dropbox.

| clip | len | content |
|---|---|---|
| 0055 | 55.5 s 4K | stock C5 walk-around, hood up, outdoors |
| 0056 | 64.6 s 1728x3072 portrait | walk-around; 32-35 s close pass to the rear 3/4 (hood out of frame) -> **match A @ 35.035 s** |
| 0057 | 49.0 s 4K | walk-around, rear views (hood up visible over roof) |
| 0059 | 49.8 s 4K | crew kneeling, unbolting the LEFT front fender (25-48 s) |
| 0060 | 10.1 s 4K | front bumper pulled off the nose (4-7 s) |
| 0061 | 11.3 s 4K | right front stripped, bumper leaning on the wall |
| 0072-0074 | | removed fenders/bumper pieces on the ground; 0074 12-14 s fender inside showing |
| 0078 | 25.9 s 4K | camera walks to the stripped RIGHT front (fender + bumper off, hood up) -> **match B @ 10.010 s** (portrait window x760-1760, y140-1918) |
| 0096-0100 | | night, prototype black front kit test-fit (not used: no scan of that state) |
| 0114-0144 | | hood mould layup, kit fitting (not used) |

Scans (engineering Drive 'C5 Scans' 116EZqQF4KZDn6j2fCc6Q-97iIE9xvZaL), all Artec, mm, one shared frame:
- Scan Data/full car scan.stl (2023-08, 8,255,611 tris) - base. Ute Scans/full car scan.stl (2026-05, 11,173,967 tris, roof open) - not used.
- Scan Data/front bumper.stl (4,999,999), Fender outer.stl (2,580,796), Fender Inner.stl (3,712,324), fender and bumper removed.stl,
  front bumper removed.stl (2024-11) - registered to the full car within 7 mm / 0.3 deg (used as-is).
- C5 Supplement Hood Open.stl (2025-06, 24,999,999) - different session frame, FPFH registration failed; not used.
Music: original C5 track (cloudfront .../hf_20261111_055731_...mp3), 109.97 BPM, kick drop at 9.320 s, music ends ~36 s.
Listing: https://www.illumaesthetic.com/products/chevrolet-corvette-c5-3d-scan-1997-2004 (hero = grey 360 render of this scan).
