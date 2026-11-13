# IS350 speed-run long-form: scan shots (v2)

Progress note (auto, 2026-11-13 03:33 UTC). Rendered by the 3D agent with `projects/smart-450-hellkitten/tools/chain.py` (resumable, queue in tools/queue.json).
Sequences: 8 fps rendered, 1440x810 (75 %), 8 spp + denoise, upscaled to 1920x1080; +0.5 s handle past each duration.
Files per shot in `/home/user/media/work/is350-long/renders/<id>/`: `png/`, `<id>_src.mov` (ProRes 422 HQ, 8 fps), `<id>_preview.mp4` (H.264 minterpolated to 23.976 fps: use this in the timeline).

v2 dropped (not rendered): SC_TITLE, SC_RES_MESH, SC_RES_REFLECTOR, SC_INS_ROOF, SC_INS_WHEEL, SC_INS_SILL. SC_INS_CABIN: the STL is a closed shell, no cabin.
Plates: the scan mesh keeps the flattened plates (owner: renders stay as delivered); the IRL footage is not blurred.

1:1 solves: SC_MATCH_REAR on FX30542 f1135 (47.339 s), focal 31.1 mm fixed, RMSE 5.9 px; SC_MATCH_FRONT on FX30554 f264 (11.011 s), focal 29.2 mm, RMSE 0.4 px.

## End-montage pairs

| pair | IRL clip, match frame | IRL lead-in (2-3 s ending on the match frame) | part of the car | fit | verdict |
|---|---|---|---|---|---|
| SC_PAIR_2 | FX30541 frame 5641 = 235.277 s | 232.78-235.277 (host scanning the rear deck with the Leo; the camera pans onto the car in the last ~1 s, a moderate pan, not a whip) | rear-right quarter, C-pillar, trunk lid, tail lamp | 6-pt PnP RMSE 11 px, then edge fit: median 7.7 px, p75 19 px (p75 inflated by powder-pattern edges), focal 26.9 mm | GOOD: windows, both door handles, mirror, tail lamp, trunk shut line coincide; roof / rear-window top edge ~15 px off at upper left |
| SC_PAIR_3 | FX30542 frame 5401 = 225.267 s | 222.80-225.267 (host scanning the hood with the Leo, steady, host at the left edge) | hood, windshield base, front-left headlamp and fender | edge fit: median 3.0 px, p75 7.4 px, focal 22.9 mm | STRONG: hood silhouette, hood/fender shut line, cowl, headlamp and grille edges coincide; no ghosting |

Not shipped (honest): FX30544 130.0 s (rear-right quarter + wheel, scanner in the foreground) repeats SC_PAIR_2's part of the car; FX30545 8-16 s (rear corner from the 4K rotated clip) is blown out by sun in the 16:9 band and the editor's crop is not fixed, so no reliable 1:1. FX30552 / FX30547 floor shots are jacked or outside the v2 free ranges. Per script_v2 rule 7 (two new pairs): drop PAIR_4, PAIR_3 = 2.5 s. Ordered worst first (PAIR_2 then PAIR_3).
IRL frames for the cut must be the full-frame 1920x1080 Rec709 grade (fx3a_slog3cine_to_709.cube); the scan's frame 1 equals that frame. Evidence: `match/onion_SC_PAIR_*.jpg`, `match/edges_SC_PAIR_*.jpg` (red = IRL edges, cyan = scan, white = both), cams `match/cam_SC_PAIR_*.json`; refiner `tools/edgefit.py`.

| id | status | frames | luma | what |
|---|---|---|---|---|
| B5_front34_hero | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_front34_hero_alpha.png` |
| B5_side_profile | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_side_profile_alpha.png` (rear-left well is ragged; crop it or prefer the 3/4) |
| B5_halfhalf_FX30554 | done | 1 | - | 3840x2160 RGBA (transparent bg), `/home/user/media/work/is350-long/renders/B5_stills/B5_halfhalf_FX30554_alpha.png` |
| SC_MATCH_REAR | done | 40/40 | frames 40 mean 58.04..59.60 max_step 0.07 dark_frames [] | v2 montage, use 0-3.0 s (render is 4.5 s + 0.5 s handle). Frame 1 = solved FX30542 f1135 (47.339 s), full 16:9; slow push on the rear bumper. |
| SC_MATCH_FRONT | done | 44/44 | frames 44 mean 46.20..58.89 max_step 0.47 dark_frames [] | v2 cold open: 0-5.0 s (title from +2.0 s, lower third clean); not reused in the montage. Frame 1 = solved FX30554 f264 (11.011 s), full 16:9; slow push. |
| SC_PAIR_2 | todo | 0/26 |  | 2.75 s + 0.5 s handle. Frame 1 = solved FX30541 f5641 (235.277 s): rear-RIGHT quarter, C-pillar, trunk lid, tail lamp; then a slow push (10 % of 2.4 m). |
| SC_PAIR_3 | todo | 0/24 |  | 2.5 s + 0.5 s handle. Frame 1 = solved FX30542 f5401 (225.267 s): hood, windshield base, front-LEFT headlamp and fender; then a slow push. |
| SC_RES_FULL | todo | 0/60 |  | 7.0 s. From above-left, one continuous dolly side -> front-left 3/4 (not a turntable). The ragged rear-left well is visible only in the first ~2 s, small. |
| SC_CON_HERO | todo | 0/68 |  | 8.0 s + 0.5 s handle (v2). Front-LEFT 3/4 (the front-right well is a ragged hole), one slow continuous pull-back; lower-left band clear for the CTA. |
