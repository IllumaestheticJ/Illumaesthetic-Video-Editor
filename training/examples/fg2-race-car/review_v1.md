# FG2 #806 race car reel v1 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/fg2_race_car_v1.mp4` — 1080x1920 (TikTok 9:16), 30 fps, 20.67 s, h264 yuv420p + AAC, faststart.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Real car with a moving push from frame 0; first 1:1 transformation (real→scan) at 1.60 s. Not < 1.5 s. |
| 2 | Beat sync | 5 | 16 cuts measured from frame diffs: all within ±17 ms of `beats` (after whole-frame durs). Drop lands on the 6.37 s angle change (bass +26 dB at 6.4 s). |
| 3 | 1:1 match | 4 | Onion checks: emblem/headlights/wheels/roof/trunk coincide on all 4 angles; intra-angle cut blends are single images. `ive check` scores read FAIL/SOFT (P1 6.5, P2 3.6, D 4.3, E 8.9 px median) — inflated by shadowed sills, the race car's lowered stance and modified lower bodywork vs the stock-state scan; overlay is the truth. Lip CAD sits ~10 px (at 1080 w) below the real painted lip on P1. |
| 4 | Scan quality | 3 | House silver on black, lip attached. LQ scan (4.9 M tris) softer than the HQ; glass is a hole (interior visible); scan carries the old plate and stock spoiler (it is the before-state). |
| 5 | Story | 4 | Each angle: scan → CGI → real, so the viewer reads data → design → finished. No exploded/part beat (no part-state scans used). |
| 6 | Grade | 4 | Daylight SDR photos, no tonemap needed; two locations (shop lot / fence) differ in warmth — native to the photos. |
| 7 | Text | 5 | None. Nothing over IRL; no numbers claimed. |
| 8 | Ending | 4 | Official logo on black, hard cut on the downbeat at 19.10 s, audio fades 0.8 s. Logo card is new (no approved card for this project). |
| 9 | Technical | 4 | Specs met. Photos P1/P2 are only 2048 px wide: the 9:16 window (768x1365) is upscaled 1.4x → softer than D/E. P1/finale lip sits at ~80–82 % frame height, at the edge of TikTok's caption zone (photo has no room below the lip). |

## Could not verify / known gaps
- Wing uprights in the E CGI are stand-in plates (the GT wing STL has blade + endplates only).
- CGI is Ecky's lip scene re-rendered (missing tyre textures removed, sky hidden from camera, black ground kept); it is not his finished CGI from `FG2 Lip CGI-Real.mp4` (that scene, with tinted glass/headlights, was not found in Drive).
- HQ scan is in another coordinate frame; not aligned (would sharpen scan close-ups).
- Music is the user's upload; timing measured from the file, not cross-checked with the version on Instagram/TikTok's library.
