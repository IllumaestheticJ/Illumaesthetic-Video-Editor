# A90 Supra "240SX-style" scan-process reel - sources

Status: first stop (no scan-process footage) -> user: "Try a, but skip to b if scanning doesn't exist".
(a) A wider Dropbox search found no Supra scanning footage, so this is (b): real rolling/shop footage + 1:1 cut to the scan.

Brief: real crew scanning the Supra with the handheld scanner, then removing a bumper / tail light,
with 1:1 cuts to the matching part-state scans (240SX format). The footage needed for that does not exist in Dropbox.

Source: Dropbox `/1. Epsilon Plus Videos/1. Video dumps/Supra Tail Light Footage/` (shared mount, ns 14789573699),
downloaded to /home/user/media/a90-supra-scan-process/dropbox. All iPhone, 3840x2160 HEVC HLG, rotated -90 (portrait).
Contact sheets in /home/user/media/a90-supra-scan-process/sheets (not committed).

| local name | Dropbox name | len / fps | content |
|---|---|---|---|
| v_0707_1613_13 | Video Jul 07 2026, 4 13 13 PM.mov | 7.1 s / 30 | shop, rear 3/4 close: **rear bumper already off**, custom heart tail light fitted, flashing (lamp test) |
| v_0707_1634_11 | Video Jul 07 2026, 4 34 11 PM.mov | 31.5 s / 30 | static: both heart tail lights on cardboard on the floor, wired to a bench controller, cycling red/amber; bumperless rear above |
| v_0707_1635_00 | Video Jul 07 2026, 4 35 00 PM.mov | 19.1 s / 30 | handheld close-up of the same bench test, then pulls back to both lamps + bumperless rear |
| v_0713_1939_54 | Video Jul 13 2026, 7 39 54 PM.mov | 13.2 s / 60 | car-to-car rolling, car driving away on a street, heart tail lights on |
| v_0713_1940_51 | Video Jul 13 2026, 7 40 51 PM.mov | 15.9 s / 60 | rolling, rear then rear 3/4 close (bronze wheels), tail lights |
| v_0713_1941_33 | Video Jul 13 2026, 7 41 33 PM.mov | 30.0 s / 60 | rolling chase, sequential amber indicators, roundabout |
| v_0713_1944_44 | Video Jul 13 2026, 7 44 44 PM.mov | 49.4 s / 60 | rolling chase; 39-41 s very close rear shot, amber sequentials |

None shows a handheld scanner, scanning powder, the crew, or a bumper / tail light being removed.
The rear bumper is already off in the Jul 7 clips (state matches "Rear Bumper removed"-type scans only loosely:
the bumper-less A90 scan states were judged unusable by the a90-supra session - 2021 fragments, FPFH fitness 5-8 %).

Other Dropbox hits for "Supra" (search "Supra", "A90", "supra scan"):
- `/2. Illumaesthetic Videos/1. Video dumps/SEMA Reels/Supra350z GT Wing/` IMG_3270.mov, IMG_3271.mov (SEMA show, GT wing; not scan footage by folder/name, not downloaded)
- `/2. Illumaesthetic Videos/1. Video dumps/*Posted Raw Videos/2024 Finished Video/Supra PCB Video/` (2024 tail-light PCB reel + screen recording - finished edit)
- `/2. Illumaesthetic Videos/3. Finished Short form/Posted/supra tails.MOV` (posted reel)
- `/2. Illumaesthetic Videos/8. Photoshoots/Supra Tailights/PCB` (photos)
"A90" and "supra scan" return nothing.

Wider search for (a): all Dropbox video-dump folders listed (Illumaesthetic + Epsilon Plus), searches "scanning"
(240SX, MR2 SW20, Beat, Civic, Lola, IS350, NB Miata, R33/CRX/Integra/STI posted reels), "toyota", "Video Sep 2026"
(Laguna GLTC), "Video Oct 2026" (240SX, Mazda 3) and all video files modified since 2026-08-15: nothing of the A90 being scanned.

## Used in v1 (option b)
| clip | in-out (s) | role |
|---|---|---|
| v_0713_1944_44 | 37.25-40.417 | opener: Supra pulls up behind the camera car; **match frame 40.400 s** (cam_A) |
| v_0707_1613_13 | 2.05-3.317 | real car, rear bumper off, heart lamp flashing (after the scan rear bumper explodes) |
| v_0713_1940_51 | 10.0-11.233 | rolling rear 3/4 pan past the wheel |
| v_0713_1941_33 | 18.6-19.233 | 1-beat sequential-amber insert |

## Scans (engineering Drive "Toyota A90 Supra > A90 Scans", Artec mm, one frame; +X nose, -Y right side)
| file | Drive id | tris (STL header) | use |
|---|---|---|---|
| Chassis_(8.4m).stl | 1wAw6utLKcGwAt2ryfaiq3z-mDyHUvcs7 | 8,400,496 | base (4 mm), prep `--drop-islands 3000` -> car.json (the frame for everything) |
| Supra Rear Bumper Outside / Inside | 1_zR2NPi... / 1D5S8X1o... | 2,992,547 / 2,992,597 | one object `rbump` (2 mm), exploded in s1 |
| Supra Front Bumper Outside / Inside | 1-HOV6RT... / 1jBrX6Jb... | 1,989,952 / 1,991,743 | one object `fbump` (2 mm), exploded in s2 |
| Supra Fender | 1iof_P7D... | 999,568 | in place (s1/s2), x-ray reassembly |
| Supra Under Front Bumper | 1S2nmZf3... | 3,995,589 | spliced into the explode base |
Explode base = car_4mm with rear/front bumper + fender zones carved (12 mm, projects/a90-supra/tools/carve.py) + Under Front Bumper.
Tail light scans and the Bomex CAD not used (no tail-light removal footage; brief).

## Website
illumaesthetic.com/products/toyota-gr-supra-3d-scan-a90-2019 ("TOYOTA GR SUPRA (A90) 3D SCAN (2019+)"), Playwright
screenshot 1440x820 @2x -> remotion/public/web_a90_listing.png (gitignored). Hero = 360 viewer grey render of this scan
(rear-right 3/4) - the x-ray end pose is solved against it (match/cam_listing.json).
Logo: Drive IllumaestheticLogoColor-01.png (1cZJj521P88T_vC2YZDJVVUCctGyNoukR).

## Music
Original Supra track (cloudfront hf_20261111_051328_...mp3), 96.0 BPM by kick-peak LSQ fit (tools/kicks.py), kicks at
0.682 + 0.625k s, bars every 2.5 s, ends hard ~29.75 s.
