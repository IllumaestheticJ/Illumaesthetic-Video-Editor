# L1 rough assembly v1 - editor self-review (training/rubric.md)

Output: /home/user/media/work/is350-long/out/is350_long_v1_rough.mp4 (5:06.81, 7356 f @ 23.976, H.264 crf 18, AAC 320k),
mix WAV + stems (dialogue / music / fx_room, float32) in out/, QA in out/qa/. Rebuild: `python projects/lexus-is350-speedrun-long/tools/assemble_long.py`.

- Story/structure: EDL followed; E41 dropped (no cabin geometry), E71 = conclusion Version A. 4/5
- 1:1 cuts: E32|E33 and E66|E67 hard, last IRL frame = solved frame, crop_y 0; preview first frames align with the onion (outline overlay checked). Final renders pending. 3/5 until finals land.
- Pacing/music: 40/74 cuts on measured kick attacks; the rest are sync-word-bound, room-tone or anchors. Lift on the front 1:1 cut. Downbeats chosen from accent strength, not by ear. 3/5
- Blur: tracked plates in E12, E15, E21, E22, E32, E45, E61, E66; crop hides plates in E50 and CON_03. Checked frame by frame on tracker sheets plus final-file sheets out/qa/blur_*.jpg. 4/5
- Audio: -14.0 LUFS integrated, -1.8 dBTP, LRA 4.0; dialogue lines -10.4 to -15.3 LUFS each after the bus (E13 hottest); no silence over 0.3 s below -50 dB. 4/5
- Placeholders: every scan shot is a 4-key preview slideshow with a red PLACEHOLDER tag (no render done yet). 2/5 (expected)
- Known defects: see editlog / final report.
