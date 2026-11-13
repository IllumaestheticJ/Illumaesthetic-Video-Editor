# IS350 reels: vertical scan shots

Progress note (auto, 2026-11-13 13:27 UTC). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable; queue in tools/queue.json).
1080x1920 from 810x1440 renders (75 %), 8 spp + denoise, 15 fps; `<id>_src.mov` = ProRes 422 HQ 15 fps, `<id>_preview.mp4` = H.264 minterpolated to 30 fps (use this). PNG frames are deleted after encoding (disk). Folder: `/home/user/media/work/is350-reels/renders/<id>/`.

Pairs: frame 1 = EXACTLY the 9:16 window of the solved 16:9 camera (sensor cropped + lens shift, not re-solved; projects/lexus-is350-scan-process/tools/portrait.py). Window = 607.5 x 1080 px at x0 in the 1920x1080 frame = 1215 x 2160 at 2*x0 in the 3840x2160 original, full height. Each pair: 2.5 s + 0.3 s handle, slow push after frame 1. IRL side must use the same window on the Rec709-graded frame. Checks (IRL window | render frame 1 | onion | edges: red IRL, cyan scan, white both): `match/check_<id>.jpg` (cams: `match/cam_<id>.json`).

| id | IRL match frame | x0 (1920) | x0 (3840) | part | fit | verdict | status | frames | luma |
|---|---|---|---|---|---|---|---|---|---|
| V_MATCH_FRONT | FX30554 frame 264 = 11.011 s | 531 | 1062 | front walk-out: grille, both headlamps, plate | 16:9 solve RMSE 0.4 px (6 pts); 9:16 frame-1 edge check median 3.6 px / p75 9.4 px @1080x1920 | GOOD | done | 42/42 | frames 42 mean 100.64..112.88 max_step 0.49 dark_frames [] |
| V_PAIR_3 | FX30542 frame 5401 = 225.267 s | 150 | 300 | hood front, grille corner, front-left headlamp; host + scanner at left | 16:9 edge fit median 3.0 / p75 7.4 px @1080p; 9:16 check median 10.4 / p75 21.4 px @1080x1920 (inflated by host/shop edges in the window; car edges coincide) | GOOD | done | 42/42 | frames 42 mean 82.88..103.70 max_step 0.77 dark_frames [] |
| V_MATCH_REAR | FX30542 frame 1135 = 47.339 s | 480 | 960 | rear bumper: plate, emblem, IS350 badge, scanner in hand | 16:9 solve RMSE 5.9 px (10 pts, focal 31.1 fixed); 9:16 check median 4.0 / p75 9.0 px @1080x1920 | GOOD | done | 42/42 | frames 42 mean 84.34..86.17 max_step 0.09 dark_frames [] |
| V_PAIR_2 | FX30541 frame 5641 = 235.277 s | 850 | 1700 | rear-right quarter: tail lamp tip, C-pillar, side glass, rear door handle | 16:9 edge fit median 7.7 / p75 19 px @1080p; 9:16 check median 14.6 / p75 32.4 px @1080x1920 | GOOD (roof edge ~15 px off at top, outside most of this window) | todo | 0/42 |  |

| id | what | status | frames | luma |
|---|---|---|---|---|
| V_RES_FULL | 4.0 s + 0.3 s handle. Full car from the front-LEFT 3/4 (clean wheel; ragged rear-left well small and far), slow push/orbit. Car spans 70-80 % of the width, 39-63 % of the height: top 22 % and bottom 25 % stay black for text/UI. | todo | 0/64 |  |
