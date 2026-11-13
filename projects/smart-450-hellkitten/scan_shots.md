# Smart 450 short: scan shots

Progress note (auto, 2026-11-13 19:00 UTC). Rendered by the 3D agent with `tools/chain.py` (resumable: rerun it after a restart).
Renders: 15 fps, 810x1440 (75 %), 8 spp + denoise, silver on black, upscaled to 1080x1920. Each shot has +3 tail frames (handles).
Files per shot in `/home/user/media/work/smart-450/renders/<id>/`: `png/` frames, `<id>_src.mov` (ProRes 422 HQ, 15 fps, 1080x1920), `<id>_preview.mp4` (H.264, minterpolated to 30 fps). For a 30 fps edit, conform `_src.mov` with minterpolate or use the preview; at the A2 swap, freeze-replace the interpolated frames around the cut (blended swap frames).

Scans (all four Artec states share one frame, no re-registration needed): Full Car Assembled, Fully Stripped, Clam and Trunk Mounting, Door Card Top Edge. Triangle counts from the STL headers: 29,997,021 / 29,998,690 / 19,995,154 / 14,996,696.

Hellkitten = the team's design concept (Challenger-Hellcat-style body over this smart 450), not rendered (no scan of it exists).

1:1 match note: A1 solve RMSE 6.1 px on 7 points; ive check silhouette median 13 px, p90 61 px (FAIL by the tool's threshold, driven by the folded soft top and interior clutter which the scan holds differently). Door braces, sill, handle cup, fuel cap and rear arch line up within ~5-15 px at 1080 wide: see `match/check_str_v1852_56_26.0.jpg`. Use it as a hard cut on a beat; if it reads loose, cut on the brace line.

| id | status | frames | luma | what |
|---|---|---|---|---|
| a1_match_str | partial | 21/39 |  | 1:1 from v_1852_56 @ 26.0 s, 9:16 window x0=760 of the 1920x1080 frame (scale the IRL crop 607.5x1080 -> 1080x1920). Frame 1 = the solved camera; then a 16 cm drift toward the nose. Scan = Fully Stripped. |
| a2_body_on_off | todo | 0/75 |  | Front-right 3/4. Assembled scan 0.0-1.6 s, HARD same-camera swap to Fully Stripped at 1.6 s (source frame 25 @15 fps, 1.6 s into the shot), then push in to the door aperture + front structure. Lights pinned, no relight at the swap. |
| a3_detail | todo | 0/39 |  | 2 mm Stripped scan: front structure with clamshell, bumper and headlamps off; slow lateral slide. |
| a4_hellkitten | todo | 0/68 |  | Starts on A2's camera at t=4.8 s (end of A2's 4.8 s use, before its handle), stripped scan 0-0.4 s, HARD same-camera swap at 0.4 s (frame 7) to Ron's SmartHellkitten.blend in its own materials (red paint, gold wheels, cat decal), registered to the scan via the model's SmartBase body (similarity ICP: scale 0.9948, p50 19 mm; front axle within ~1 cm, rear axle 4-6 cm forward = the design's 1.778 m wheelbase). Pull back 0.4-1.7 s to the whole car with margin, then a slow push/orbit to 4.5 s. The first 0.4 s keep A2's close (clipped) framing on purpose for continuity. |
| a5_xray | todo | 0/45 |  | The reel's FIRST shot, 3.0 s incl. handle. Front-right 3/4, whole car in frame (>= 9 % side margin all through), top ~41 % black for the title (editor adds THIS IS A SMART CAR?). Hellkitten in its own materials 0-0.4 s, body turns to fresnel-edged red glass 0.4-1.0 s, the registered ASSEMBLED Smart scan (silver with a cool rim glow) stays visible inside for the hold; slow push-in. Same registration as a4 (SmartBase -> Assembled scan, similarity ICP, scale 0.9948, residual p50 19 mm / p75 56 mm). Ron's own SmartBase/Steering parts are hidden. |
