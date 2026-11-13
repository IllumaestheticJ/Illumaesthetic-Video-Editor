# Smart 450 short: scan shots

Progress note (auto, 2026-11-13 00:43 UTC). Rendered by the 3D agent with `tools/chain.py` (resumable: rerun it after a restart).
Renders: 15 fps, 810x1440 (75 %), 8 spp + denoise, silver on black, upscaled to 1080x1920. Each shot has +3 tail frames (handles).
Files per shot in `/home/user/media/work/smart-450/renders/<id>/`: `png/` frames, `<id>_src.mov` (ProRes 422 HQ, 15 fps, 1080x1920), `<id>_preview.mp4` (H.264, minterpolated to 30 fps). For a 30 fps edit, conform `_src.mov` with minterpolate or use the preview; at the A2 swap, freeze-replace the interpolated frames around the cut (blended swap frames).

Scans (all four Artec states share one frame, no re-registration needed): Full Car Assembled, Fully Stripped, Clam and Trunk Mounting, Door Card Top Edge. Triangle counts from the STL headers: 29,997,021 / 29,998,690 / 19,995,154 / 14,996,696.

Hellkitten = the team's design concept (Challenger-Hellcat-style body over this smart 450), not rendered (no scan of it exists).

1:1 match note: A1 solve RMSE 6.1 px on 7 points; ive check silhouette median 13 px, p90 61 px (FAIL by the tool's threshold, driven by the folded soft top and interior clutter which the scan holds differently). Door braces, sill, handle cup, fuel cap and rear arch line up within ~5-15 px at 1080 wide: see `match/check_str_v1852_56_26.0.jpg`. Use it as a hard cut on a beat; if it reads loose, cut on the brace line.

| id | status | frames | luma | what |
|---|---|---|---|---|
| a1_match_str | partial | 8/39 |  | 1:1 from v_1852_56 @ 26.0 s, 9:16 window x0=760 of the 1920x1080 frame (scale the IRL crop 607.5x1080 -> 1080x1920). Frame 1 = the solved camera; then a 16 cm drift toward the nose. Scan = Fully Stripped. |
| a2_body_on_off | partial | 17/75 |  | Front-right 3/4. Assembled scan 0.0-1.6 s, HARD same-camera swap to Fully Stripped at 1.6 s (source frame 25 @15 fps, 1.6 s into the shot), then push in to the door aperture + front structure. Lights pinned, no relight at the swap. |
| a3_detail | todo | 0/39 |  | 2 mm Stripped scan: front structure with clamshell, bumper and headlamps off; slow lateral slide. |
