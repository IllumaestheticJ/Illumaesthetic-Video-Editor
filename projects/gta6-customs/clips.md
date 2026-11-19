# GTA 6 mod-shop capture

Source: Dropbox `/5. Claude Training/GTA training/YTDown.com_YouTube_Media_Iorp17P06hs_GTA-6-Car-Customization-Is-Insane_001_1440p.mp4`
(id:ihAynaYnO_4AAAAAAAEJxQ), a third party's YouTube capture the user supplied. Local:
`/home/user/media/gta6-customs/capture/gta6_customization_1440p.mp4`, 2560x1440, 60 fps container with every frame
doubled (30 distinct fps), 116 s, stereo AAC. Game footage and UI are Rockstar's; the capture is the uploader's.

Frames (60 fps index):
- 0-276 Bodywork menu, front 3/4 camera ("M"). Row 2 "Spoiler" highlighted, yellow marker on it.
- 277-293 whip to the rear view (8 distinct frames: 278, 280 ... 292).
- 294-400 Spoiler screen, rear camera ("A"), option None 1/3 "Applied".
- 401-417 whip to a roof view (Small Spoiler); 479-497 back; 499 None > Small Spoiler in view A; 525-541, 557-573 whips.
- 574-616 and 876-1069 Custom Wing 3/3 ($790, "Not enough cash") in view A. Same camera as None: only the car changes.
- 1164-1180 whip back to the menu (distinct: 1165 ... 1181); 1181-1276 menu, row 2, no marker; 1277 row 3 "Front Bumper".
- 1400-1500 Cosmetics tab (uploader's cut). 1500-1890 Full Kits 1/4 (same camera as the menu), then kits 2-4 to ~2400.
- 2545-4080 Accessories (aerials), three more views. 4080+ leaving, driving.

Sound: room tone at -41 dB and one-frame menu ticks (high band -39 dB against -60) on every action; no music or
speech in the menu part. Engine and street sound from 68 s.
Cameras: f = 1757 px on 2560 in every view. Horizon row 394 (menu, kits), 75 (rear view).

## Second capture (user, 2026-11-19: "include the audio and sounds")
Dropbox same folder, `YTSave.to_YouTube_Media_VCyedol41Do_GTA-6-Vehicle-Customization-Looks-Amazing_001_1440p.mp4`
(id:ihAynaYnO_4AAAAAAAEJxg), 376 MB. Local `/home/user/media/gta6-customs/capture/gta6_customization_B_1440p.mp4`,
2560x1440, 60 fps, 391 s; audio `/home/user/media/work/gta6-customs/b.wav`. Same shop, same menu camera, overcast.
- 0-6 s title and the car standing in the shop, "Repair for free?" prompt; 8-55 s performance, kits, suspension (loud).
- 55-210 s menus (room tone and ticks). ~0.2 s bright sounds at 174.7, 237.2, 331.2, 347.8 s are select-into-submenu.
- **213.6 s (frame 12817): the only purchase** (free kit). Sound 213.84-215.3 s; lower-left block turns to "Applied"
  at frames 12824-12830; "Purchased" pop-up from frame 12836 to 12980, at x 2288-2515, y 549-592.
- 216-227 s respray previews with spray sounds; 228 s on, menus again.

## Frames used in v3
First capture: list 10-276; rear view 880-1038; option screen (Full Kits) 1510-1688 for the respray; UI-free exit 4086-4104.
Second capture: Exhaust 17946-17976 (camera creeps: only this half second matches the menu's reference frame 17960);
suspension ("Wheel Kits", lowered kit 3/3 with stat preview) 2072-2150, reference 2100; Rim Style 20258-20398, reference
20040; respray block from 5160 ("Admiral", Blue tab) against plain frame 2300; purchase sound 213.80-215.45 s.
Cameras: cam_E (exhaust, set by hand closer than the capture's), cam_S, cam_W: `tools/mancam.py`, values in the edit log.
