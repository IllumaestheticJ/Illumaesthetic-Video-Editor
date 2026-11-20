# Captures and views (MR2 Spyder mod-shop reel)

Same two captures as `projects/gta6-customs/clips.md` (third parties' YouTube captures the owner supplied; game footage and UI are
Rockstar's). Local: `/home/user/media/gta6-mr2-spyder/capture/gta6_customization_1440p.mp4` (A, Dropbox id:ihAynaYnO_4AAAAAAAEJxQ, 116 s,
sunny, no watermark) and `..._B_1440p.mp4` (B, id:ihAynaYnO_4AAAAAAAEJxg, 391 s, overcast, uploader's watermark bottom right).
Both 2560x1440, 60 fps. Contact sheets at 0.5 fps: `$W/sheets/`.

## Capture B: every camera view (time, 60 fps frame, what it shows)
| View | Time | Frames held | Shows | Used for |
|---|---|---|---|---|
| Engine bay | 0:06-0:16, 5:10-5:24 | | bonnet open, from the front right | - |
| Menu camera (as capture A's) | 0:18-2:58 | | front 3/4 left; paints, liveries | - (A's is sunny and clean) |
| Low front quarter ("Wheel Kits") | 0:30-0:36 | 2083-2151 | front wheel, sill, door | **D** side skirts, **S** suspension |
| Plates (rear, low) | 3:00-3:12 | | tailgate close | - |
| Hood | 3:18-3:26 | 11916-11952 | from the front, above, down on the bonnet | **H** hood vents (new camera) |
| Front bumper / Lights | 4:02-4:08, 4:48-4:54 | 14706-14748 | dead front, low | **F** front bumper, eyelids |
| Rear bumper / Exhaust | 4:12-4:16, 4:58-5:00 | 17951-17970 (creeps) | dead rear, low | **E** spats, diffuser |
| Towing (side) | 4:22 | | left side close, car fills the frame | - |
| Windows | 4:26-4:30 | | front 3/4 from above | - |
| Rear bed | 4:32-4:40 | 16582-16695 | from behind and above, whole cab roof | **T** hardtop (new camera) |
| Roof | 4:44 | | front left from above, car across two thirds of the frame | - (cannot be covered by the MR2) |
| Spoiler (B) | 3:50-3:58 | | rear 3/4 from above | - (A's rear view used) |
| Rim style | 5:32-5:52 | 20258-20398 | front-left wheel close-up | **W** wheels |
| Interior | 5:56 on | | cabin | - |
The only purchase is at 3:33.6 (frame 12817): sound, "Applied", "Purchased" pop-up; the mechanic's line follows inside the same clip.

## Capture A
Menu list 10-276 (**M**), rear view 874-1070 (**A**, duckbill), option screen 1510-1700 (**P**, respray), UI-free exit frame 4096 (**X**).

## Cameras (car frame: Z up, nose -Y; f = 1757 px on 2560)
`cam_<view>.json`, found by `tools/camsearch.py` from the Civic reel's cameras (H and T from a guess), see the edit log for the numbers.
Game-car masks: `$W/frames/masks0.npz` (M from four paint builds on the same camera; T by GrabCut on the yellow car; H, A, E, F, S, W polygons).
