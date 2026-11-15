# Toyota MR2 Spyder scan-process reel v3 - agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/mr2_scan_process_v3.mp4` - 1080x1920, 30 fps, yuv420p, AAC, faststart, 24.60 s (738 frames).
v3 answers the v2 note ("a mess - more scanning footage, more of the car, the other scans"): built around the printed hardtop
and the scans made at this shoot. v2's review is kept in review_v2.md.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | crew carrying the scanner to the car from frame 0, live scanner screen at 1.07 s; the 1:1 transformation waits for the drop (4.27 s) |
| 2 | Beat sync | 5 | 8 hard cuts; on the decoded audio the strongest attack is within 0-25 ms of every cut (music start +80 ms after the first build read 7 of 8 cuts ~80 ms early). cutcheck's half-rise detector mislabels 321/385 (double hits) - verified with a rise-rate scan |
| 3 | 1:1 match | 4 | cut B re-solved from 10 landmarks (camB2, rms 44 px @1728): hardtop piece opening, tail lamp, lid edge, plate recess line up (match/checkB2.jpg). The old silhouette solve was ~12 deg rolled. Wing + scooped lid exist only in footage |
| 4 | Scan quality | 4 | silver on black; piece is the registered shoot-day "hardtop revision 1" (3.6 mm rms); some ragged edges on the piece rim and the deck seam behind it; no lighting dropouts (per-frame luma steps < 2.3) |
| 5 | Story | 5 | one continuous hardtop sequence: scanning -> 1:1 scan of the piece -> scanner sweep -> real lift -> scan lift (translate only, hardtop-off state = Top Down scan) -> piece on the floor -> full hardtop lands on the whole car -> listing |
| 6 | Grade | 4 | DJI bt709 untouched; FX3A S-Log3 through the project LUT; the two FX shots are 3:4 windows on blurred fill |
| 7 | Text | 5 | 3 labels, scan shots only, clean black band; names from the Drive files (Mr2 hardtop revision 1, Full Car); no counts, no brackets |
| 8 | Ending | 4 | Full Car hardtop lands, orbit to the solved listing pose, silver -> listing grey, 0.5 s dissolve into the WebZoom listing; logo + URL last, music fades with it |
| 9 | Technical | 4 | exact-frame concat (no duplicated cut frames); 24->30 pulldown repeats inside IRL clips |

## Known issues / for the reviewer
- irl_wide (first 1.07 s) crops the car at both ends: native handheld framing, the only shot of the crew bringing the scanner over.
- The hardtop's printed underside is not scanned, so the scan lift never turns the piece over (it is seen only in irl_down).
- No front section this time: no shoot-day front scan registers to this car (see clips.md).
