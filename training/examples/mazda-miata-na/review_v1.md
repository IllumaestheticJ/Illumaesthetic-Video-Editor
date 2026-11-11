# Mazda Miata NA scan reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/miata/out/mazda_miata_na_v1.mp4` — 1080x1920, 30 fps, 36.13 s, H.264 High yuv420p + AAC, faststart.
Scan-only Temerario-style reel: turntable → rear orbit → wheel / tail-lamp close-ups → hood opens → trunk closed→half→open →
top-down → exploded view (bumper, hood, trunk lid) → ILLUMAESTHETIC logo. Track: mazda-miata-na_track.mp3 (80s synthwave).

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable moves from frame 1, but nothing *transforms* until the hood at 11.7 s; the track's intro is 16 calm beats, so the opening is deliberately slow (Temerario pacing). |
| 2 | Beat sync | 5 | Kick grid 0.6068 + 0.5555 n (1.7 ms rms). Delivered file: cut frames 152/285/318/352/418/485/551/951 exactly as planned; −18..+16 ms from the nearest kick (the drop cut sits on a .5-frame boundary). |
| 3 | 1:1 match | n/a | No IRL footage in this reel. Lid hinges verified the same way: rotated lid z-fights with the captured open lid. |
| 4 | Scan quality | 4 | Ground rails/strips removed, plate characters flattened (privacy), 2 mm close-ups. Engine bay and trunk well are real state captures. Minor: hood underside only covers the right 2/3 (partial capture; camera kept on that side); tail lamp lenses render as solid shells. |
| 5 | Story | 4 | Clear "what we scan": exterior detail → panels open (real open-state captures) → panels come off and go back. Only 3 removable panels were scanned, so the explode is lighter than the Ferrari/Temerario. |
| 6 | Grade | 5 | Silver on pure black, AgX, no IRL. |
| 7 | Text | 5 | None (brief). |
| 8 | Ending | 5 | Logo on the b56 phrase change (31.7 s), fades with the track's last kick/decay; video ends 36.13 s, audio below −30 dB at 35.9 s. |
| 9 | Technical | 4 | Specs met; no black/dup frames at cuts. s8 rendered black from frame 57 in one long render (persistent-data glitch) - re-rendered in fresh 25-frame processes, one chunk-end frame needed a second pass (tools/rerender.sh). |

## Known weaknesses / for the next pass
- Exploded orbit, ~45-75 % through: the trunk lid drifts off the left edge and the bumper is clipped at the right edge
  (car width + stacked parts in 9:16 from a front-right/side camera). Pull the camera back ~10 % or bring the bumper higher/back.
- Close-ups are 2 beats (1.1 s) each — short for "extreme close-ups"; the alternative was cutting off-phrase.
- 'NA Finish Panel' scan registered but unused (inner tail panel, would leave a hole).
