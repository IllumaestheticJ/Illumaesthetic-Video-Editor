# ditl-wrx-vb — self review (first cut v2, 2026-11-17)

Status: first cut for owner review, not final. v1 = first assembly; v2 = same picture, soundtrack re-timed.

## Measured checks (delivered mp4 `cut/ditl_wrx_vb_v2.mp4`)
| Check | Result |
|---|---|
| Format | 1080x1920, 30 fps, h264 yuv420p, AAC, faststart, 1005 frames, 33.50 s |
| Loudness | -14.0 LUFS integrated, peak -2.8 dBFS (target -14, < -1) |
| Cut timing | v1 FAILED: song is 149.8 BPM (bar 1.602 s) and the drop is at 32.25 s, not 152 BPM / 32.18 s as planned; cuts were 2.5 frames early at the drop and ~12 frames early by shot 14. v2 fix: song played 1.39% fast from 30.05 s (picture untouched). Drop now rises at frame 65-65.5 = the shot 1->2 cut; all 13 music cuts within about 1 frame of a beat (beat-tracker reading -0.0 to -1.7 frames, tracker hop 5 ms) |
| Picture cuts | frame-difference peaks at every planned cut frame (65, 113, 160, 208, 255, 302, 350, 445, 492, 539, 634, 682, 729, 776, 855) |
| Voice edges | source clips start/end at -38 dB or lower re peak (semper fi -57/-38, exchange -90/-77, ringlands -46/-53): no clipped phonemes. Music ducked to 0.3 under lines 1 and 2; line 3 is after the music stops. "...ringlands?" ends 3 ms before the end of the file: tight |
| Layout | picture 1080x1080 at y=420-1499 on all sampled frames (every 15th); bands black (max 12/255 = codec ringing at the edge); title bbox x 272-807, y 196-316 |
| Product | his car in shots 7, 8, 9, 15, 16 is the GLB with stock bumpers/side trim/duckbill hidden and front bumper, rear bumper, skirts and WRC wing shown; one paint material (0.02, 0.12, 0.55) in every shot |
| On-screen numbers | cart prices from live Shopify 2026-11-17: $2,000.00, $1,500.00, $800.00, $1,150.00, subtotal $5,450.00. $115,000 and 30% APR are the owner's character numbers |
| Ending | music stops dead at 25.87 s (Odyssey pass), mirror push-in, last word, file ends on picture = hard cut, no trailing frames, no end card |
| Not checked | I cannot hear audio: balance, comedy timing of SFX and voice intelligibility in the mix need the owner's ears |

## Rubric (training/rubric.md; scan-reel criteria adapted to this format)
| # | Criterion | Score | Note |
|---|---|---|---|
| 1 | Hook | 4 | form slaps start at frame 7 |
| 2 | Beat sync | 4 | within about 1 frame after the v2 re-time |
| 3 | 1:1 match | n/a | no IRL footage in this format |
| 4 | Scan quality | 3 | no floating objects or poke-through; G80 side-window cutout jagged (shots 11-12), van is a plain box, vape cloud small |
| 5 | Story | 4 | dropout -> recruiter -> cart -> debt -> kit car -> paranoia -> Beamer guy -> Odyssey -> ringlands |
| 6 | Grade | 4 | crunch and banding applied to every frame; dusk phone shots are dark by design |
| 7 | Text | 5 | true store prices, no text over footage, title in the band |
| 8 | Ending | n/a | owner asked for a hard cut to black with no logo |
| 9 | Technical | 5 | see table |

## Open
- Owner: dedicated vape scene? BMW colour? May review JPEG sheets be committed?
- Polish candidates: G80 window edge, Odyssey shape, vape cloud.

## v2.1 (parent follow-ups)
- Pitch: the 1.39% speed-up uses ffmpeg `atempo` (time stretch, pitch preserved), so there is no 24-cent shift; no change needed. Drop still rises at frame 65-65.5.
- Last line: "...ringlands?" moved 0.17 s (5 frames) earlier so the word's tail ends about 5 frames before the hard cut instead of 3 ms. The picture is unchanged; the horror face (frame 124 of shot 16) now lands during the word instead of at its start.
- Loudness re-measured on v2.1: see editlog.

## v3 (owner feedback round 1: dropout form, signing bonus, parts thrown at the car, mirror camera)
- 1080x1920, 30 fps, 1052 frames, 35.07 s. Shots 1, 2, 3, 7, 16 re-rendered (`render3`), the rest reused from `render2`.
- Loudness -14.3 LUFS, peak -2.7 dBFS.
- Picture cuts at 65, 113, 160, 208, 255, 302, 397, 492, 539, 586, 681, 729, 776, 823, 902; music cuts within about 1 frame of a beat (tracker reading 0.0 to -1.2); drop on the frame-65 cut. No dark frames (minimum picture mean 54/255).
- Looked at contact sheets of all five new shots: form and DROPPED OUT stamp readable, cash brick label readable, each of the four parts leaves the box and lands on the car, mirror shot starts in front of the seat.
- Still unheard by me: the new stamp, cha-ching and throw/land effects.
- Shot 7 landings, checked at full res on frames land-1 / land / land+3 for each part (front bumper 27, skirts 46, rear bumper 65, wing 84): the stock piece is visible on land-1 and gone on the landing frame, the kit part is present from the landing frame, so there is never a frame with both or neither. Each thrown part is a copy of the GLB mesh keyed back to its own world matrix (rotation 0, scale 1) by land+3; on the landing frame itself it is deliberately 14% oversize for a 3-frame impact bounce (most visible on the side skirts), then sits flush with no gap or offset.

## v4 (owner feedback round 2: signature on the paper, direct Accessport smack, boxer engine sound)
- 1052 frames, 35.07 s; shots 2, 10, 16 re-rendered (`render4`); -14.4 LUFS, peak -2.7 dBFS; cut frames and music timing unchanged from v3.
- Contact sheets checked: scribble sits on the form, the arm comes from the driver and ends on the Accessport in shots 10 and 16 (hand largely hidden behind the device at impact, arm briefly covers the screen), mirror shot unchanged otherwise.
- Engine sound is unheard by me; spectrum shows the strongest partial at 1.5x firing frequency (uneven-pulse boxer pattern).
