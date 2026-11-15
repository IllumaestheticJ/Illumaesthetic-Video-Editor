# Toyota MR2 Spyder (hardtop project) - scan-process reel - clip notes

Sources (Dropbox):
- `/2. Illumaesthetic Videos/1. Video dumps/MR2 HARDTOP/` - FX30 (Sony ILME-FX3A + FE 24-70 GM II, S-Log3/S-Gamut3.Cine,
  3840x2160 23.976, landscape) and DJI Osmo Pocket 3 clips, Jul 10-16 2025. `*REEL/` subfolder = an earlier hand-picked
  selection (hardtop print shop + Jul 16 fitment; no scanning).
- `/1. Epsilon Plus Videos/1. Video dumps/MR2 Hardtop/` - DJI 0001-0048 with `.LRF` proxies (1280x720) - used to sheet every
  DJI clip cheaply before downloading full res.
Local: /home/user/media/mr2/{dropbox,fx30,lrf}. Sheets: /home/user/media/work/mr2/sheets*.

| clip | len | content | used |
|---|---|---|---|
| FX30510-517, 559, 567-569, FX30_4585/4602 (*REEL) | 4-25 s | 3D-printed hardtop pieces / print shop, S-Log3 | no (no car, no scanning) |
| DJI_20250716 0036-0047 (*REEL) | 5-44 s | hardtop fitment on the car in daylight, Jul 16 | no |
| DJI_20250711-13 0002-0018 (LRF) | 1-6 min | engine bay / interior / print shop sessions | no |
| DJI_20250714 0019-0028 (LRF, Epsilon) | short | a different grey car | no |
| **DJI_20250715210710_0030** (Osmo Pocket 3, portrait 1728x3072, BT.709) | 98.8 s | night session: crew scans the red MR2 with the handheld scanner - deck/rear 20-56 s, front 70-80 s | **irl_scan_rear** (n1293-1343, 56.0 s = cut B), **irl_scan_front** (n1700-1775, 74.0 s = cut A) |
| DJI_20250715 0031-0043 (LRF) | 5 s-4 min | rear trim / roll-hoop work, grinding, lid open | reviewed; DJI_0035 (landscape 4K) lid-open frame tried for cut B, rejected (no full silhouette) |
| FX30633-649 (A-cam of the same Jul 15 night, 21:06-21:43) | 2.5-5.6 min | interviews, engine lid, hardtop lifted on/off by two crew | **irl_hardtop** = FX30636 18.6-21.8 s, LUT-graded, 9:16 crop x=1300 |

Scans (engineering Drive "Toyota MR2 Spyder" -> "MR2 Spyder Scan Data"):
- Full Car Top Down.stl (14,999,997 tris) - base for both 1:1 cuts and the x-ray (stock hood; footage hood has duct scoops).
- Full Car.stl (19,540,297), Hardtop Mounting/Hardtop Mounting Full Car.stl (18,547,676) - same Artec frame as Top Down.
- MR2 Spyder Rear End trunk open.stl (7,000,064) - other frame; FPFH+ICP registered (3.2 mm rms) -> lid-open state + lid part.
- Kouki and Undertray.stl (scooped hood), Rear Interior Trim Removed, Trunk Open Cover On, Rear QuarterPanel, Hood Duct Data - fetched/checked, not used.
- Front Bumper Data/front fully removed.stl (999,993) and hood open no bumper.stl (1,000,000), 2024: do NOT register to this car -
  FPFH+ICP fitness 0.11 @ 6 mm, fender-only sweep 0.05 @ 5 mm (match/reg_ffr.json, reg2_ffr.json); nose/fenders 50-70 mm off. Not used.
  FrontEnd.stl is ASCII (not inspected).

Music: original MR2 Spyder track (city-pop, 112.1 BPM), cloudfront link in the brief; /home/user/media/mr2/music/mr2_track.mp3.

## Footage + scan audit after v2 feedback ("a mess; more scanning footage, more of the car, the other scans") - 2026-11-13
Every clip in both dumps is now viewed (full res or LRF proxy), except FX30637 (3.7 GB) and FX30646 (4.4 GB) and the
Jul 10/11 + Jul 15 afternoon FX sets (their *REEL samples are all print-shop / hardtop parts, no car).
- **Handheld-scanner footage exists in ONE clip only: Epsilon DJI_20250715210710_0030** (98.8 s, portrait). Scanner on the car:
  ~20-36 s (rear deck with the printed hardtop rear section), 44-66 s (deck / hoop / scanner screen close-ups), 70-80 s (front, windscreen).
- Other car action (no scanner): main DJI_20250715 0029-0035 + Epsilon 0044-0048 (landscape 4K): door-sill / interior trim removal
  (e0044-47), locked-off wide side profile with engine lid open and crew at the rear (e0048, m0031, m0032, 15 min), hardtop test-fit on the
  car (m0034, m0035); FX30641-645 hardtop pieces on the floor, FX30647/648 header-latch close-ups from inside, FX30649 hardtop on the car.
- **The scans made at this shoot were not used in v1/v2** (Drive dates Jul 16-17 2025): Print Evaluation/Mr2 hardtop revision 1.stl
  (35,052,792 tris: printed hardtop rear section on the car with roll hoop, deck and louvres - what the crew scans at 20-66 s),
  Hardtop Mounting/Roof Front Edge (14,756,964), Roof Latch Reference (Closed) (16,835,345), Front Latch Roof Underside (12,399,862),
  Handle (520,439). They are in other Artec frames (voxel overlap with Top Down 0-13 % before registration) - registration not attempted yet.
