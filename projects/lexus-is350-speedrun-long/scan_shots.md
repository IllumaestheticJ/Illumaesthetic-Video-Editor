# IS350 speed-run long-form: scan shots

Progress note (auto, 2026-11-13 02:25 UTC). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable).
Sequences: 8 fps rendered, 1440x810 (75 %), 8 spp + denoise, upscaled to 1920x1080; each has +4 frames (0.5 s) of handle past the EDL duration.
Files per shot in `/home/user/media/work/is350-long/renders/<id>/`: `png/`, `<id>_src.mov` (ProRes 422 HQ, 8 fps), `<id>_preview.mp4` (H.264 minterpolated to 23.976 fps: use this one in the 23.976 timeline). At SC_RES_REFLECTOR's 3.0 s swap, freeze-replace the blended frames.

Plates: both flattened in the mesh before rendering (tools/deplate.py), so every render is plate-free.

**SC_INS_CABIN: skipped.** The full-car STL is a closed shell (the sprayed glass was scanned as surfaces), so there is no cabin geometry. Drop E41 and let E40 run into E42.
SC_INS_FRONT / SC_INS_REAR: not rendered (no longer needed).

1:1 solves: SC_MATCH_REAR on FX30542 f1135 (47.339 s), focal fixed 31.1 mm, RMSE 5.9 px on 10 points; SC_MATCH_FRONT on FX30554 f264 (11.011 s), focal 29.2 mm, RMSE 0.4 px. Onions in `match/`. IRL frames must be the Rec709-graded 16:9 frames (fx3a_slog3cine_to_709.cube); the scan's first frame equals the IRL frame.

| id | status | frames | luma | what |
|---|---|---|---|---|
| B5_front34_hero | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_front34_hero_alpha.png` |
| B5_side_profile | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_side_profile_alpha.png` (rear-left well is ragged; crop it or prefer the 3/4) |
| B5_halfhalf_FX30554 | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_halfhalf_FX30554_alpha.png` |
| SC_MATCH_REAR | done | 40/40 | frames 40 mean 58.04..59.60 max_step 0.07 dark_frames [] | E33, 4.5 s. Frame 1 = solved FX30542 f1135 (47.339 s) camera, 16:9 1920x1080; slow push on the rear bumper. Plates flattened. |
| SC_MATCH_FRONT | todo | 0/44 |  | E67, 5.0 s. Frame 1 = solved FX30554 f264 (11.011 s) camera, 16:9; slow push. Plates flattened. |
| SC_RES_FULL | todo | 0/60 |  | E68, 7.0 s. From above-left, one continuous dolly side -> front-left 3/4 (not a turntable). The ragged rear-left well is visible only in the first ~2 s, small. |
| SC_CON_HERO | todo | 0/98 |  | CON_05, 11.76 s. Front-LEFT 3/4 (the front-right well is a ragged hole), one slow continuous pull-back; lower-left band clear for the CTA. |
