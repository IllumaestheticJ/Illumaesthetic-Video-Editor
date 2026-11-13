# Lola (Drifter movie) scan-process reel v8 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/lola_scan_process_v8.mp4`. Specs: 1080×1920, 30 fps, yuv420p, AAC, 34.37 s (1031 frames). Earlier: `review_v1.md`–`review_v7.md`.

> ✅ **Posting permission confirmed:** the user confirmed on 2026-11-11 that the Drifter production is fine with
> the reel being posted. The reel uses footage from the film's public trailer and the user's own on-set driving
> clips, both supplied by the user.

v8 (user: "my life be like" must start the song; use the July 2025 driving footage for extra real/scan shots of the interior):
- **Music:** now starts at track 20.80 s, on the "my life be like" pickup. v7 started just after it. The beat drop moves to 5.87 s.
- **Opening (all film footage, letterboxed):** wheel cam → Lola 1 drifting at camera → parked side profile → 1:1 on the drop into the scan.
- **New 1:1 #3:** the user driving Lola on set (film rig and LED panel on the hood, Camera Uploads 2025-07-30) → the interior scan from the same driver's-eye camera (cam_D).
- **Removed:** the cabin-scanning clip and the Lola 2 rear scan shot. The driving match and the turntable cover those sections.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Film footage and the lyric hook from frame 0. The first transformation is on the drop at 5.87 s, later than v7 because the song now starts on the hook. |
| 2 | Beat sync | 5 | 11 cuts at −16 to +16 ms from kick onsets, measured on the delivered file's decoded audio. |
| 3 | 1:1 match | 5 | Three hard 1:1 cuts, each checked by blending the cut frames: movie → scan (body lines; the film car's wheels sit lower), scanner → scan, driving → interior scan (roof cut-outs, mirror, dash edge, vents, gauges). |
| 4 | Scan quality | 4 | The interior scan has ragged glass/void areas where the windshield is. That is honest scan data, kept. |
| 5 | Story | 5 | The film car → we scanned it → how → inside and outside → driving it on set → the same seat as scan → the second car → on screen → honoured. |
| 6 | Grade | 4 | The film clips keep their grade; the glasses footage is flatter. |
| 7 | Text | 4 | Three captions plus four data labels, all in black bars or on scan shots. This is more than the rubric's "≤2 items", at the user's request. |
| 8 | Ending | 5 | Movie tandem drift with the closing caption, then the logo with the fade. |
| 9 | Technical | 4 | Specs met. The interior scan shot was rendered at 10 fps (110 s per frame) and interpolated. |

## Notes / open
- **Where "my life be like" is:** speech-to-text was not available, so the line was located acoustically. The song's first vocal phrase (16.0 s) recurs every 4.85 s before each downbeat, and the reel starts on the 20.85 s occurrence. If the user hears a different word first, shift `music.start`.
- **Interior focal:** the driving clip solved with a free focal (1336 px), not the 1094 px measured on the scan-day glasses clips.
- **Length:** 34.4 s, up from 29.9 s in v7.
