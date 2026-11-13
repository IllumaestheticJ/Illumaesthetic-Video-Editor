# Lamborghini Revuelto scan reel v4 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/lamborghini_revuelto_v4.mp4` — 1080x1920, 30 fps, 44.57 s (1337 frames), h264 yuv420p + AAC.
Earlier versions: review_v3.md, review_v2.md (v2.1), review_v1.md. v4 answers the reviewer's notes on v3: add the rear-wing-removed
section; the rear bumper clipped the tail lights and wing on its way off; exhaust sections after the bumper; some parts left the
screen; music re-edited to the supplied track ("Sector Shift").

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Whole car pushing in under the two-bar lead-in; first transformation at 3.4 s on drop 1 (front bumper off). |
| 2 | Beat sync | 4 | Every cut on a bar downbeat of the 140 BPM grid (frames 103/206/309/463/566/617/669/771/926/1080/1234). On the delivered audio the nearest 40-120 Hz onsets are -25..+22 ms from the cuts, except 30.87 s (-48 ms) and 36.0 s (-32 ms) in the half-time passage where the kick is softer. Parts lock at frame 1131 (-8 ms) on drop 2, logo two bars later. |
| 3 | 1:1 match | n/a | Scan-only format. |
| 4 | Scan quality | 4 | Exhaust-session scans corrected by one shared offset (20.7 mm, 0.6 deg) to 2.0-3.3 mm of the car frame, cropped to the bay and de-islanded. Engine-bay states are ragged at the crop edge; scan-noise specks under the open front lid remain. |
| 5 | Story | 5 | Front -> front bumper alone + its pieces -> side -> rear wing (wide, then close on the wing-removed scan) -> rear bumper and tail lights off -> exhaust: tips, catback, cats, bare bay (1:1 state swaps) -> rear bumper alone + its pieces -> everything flies home on drop 2 -> logo. |
| 6 | Grade | 4 | AgX silver on black, consistent; bumper-only and exhaust shots are darker overall (small subject on black). |
| 7 | Text | 4 | Eleven short labels, one at a time, only over scan shots, none crossed by a part (checked on the delivered frames). Triangle counts from STL headers; names from the scan file names. |
| 8 | Ending | 4 | 0.5 s fade, 720 px logo on the downbeat two bars after the lock, 2.2 s audio fade. |
| 9 | Technical | 5 | Spec met; per-frame luma scan of every render: no dropouts; no black or frozen frames at cuts (one repeated frame at 462, the static end of the bumper-pieces hold). |

## Checks made on the picture
- Measured edge margin of every shot over all frames: all parts stay in frame (min 8 px, reassemble fly-in). v4_side first
  measured 0 px (tail on the right edge) and was re-rendered 1 m further back (27 px). v4_wingin is a deliberate close-up that
  crops the car body, not a moving part.
- tools/pathcheck.py: rear bumper no longer passes through the tail lights (v3: 13 % of tail-light points inside the bumper path).

## Known weaknesses
- "Exhaust after the bumper" is read as: right after the rear bumper comes off the car, before the bumper-pieces shot.
  Swapping those two blocks needs no re-render.
- Only one tail light is visible leaving in the rear wide (the other is hidden behind the car from that side).
- The wide wing shot sits high-left in frame.
- 44.6 s is 10 s longer than v3.
