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

Music: original MR2 Spyder track (city-pop, 112.1 BPM), cloudfront link in the brief; /home/user/media/mr2/music/mr2_track.mp3.
