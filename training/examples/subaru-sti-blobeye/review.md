# Self-review — Subaru Impreza STI GD "blobeye" scan reel (v3)

Deliverable: `/home/user/media/work/sti/out/subaru_sti_blobeye_v3.mp4` — 1080×1920, 30 fps, 39.27 s, scan only, no text.
Order: front 3/4 turntable → rear 3/4 orbit → wheel / headlight→scoop / wing+tail-light close-ups (1 bar each) → hood opens over
the engine-bay scan → top-down spin → exploded view (hood, bumper, wing, left skirt float up, hold, slam home) → logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Turntable moving from frame 1, but no transformation in the first 1.5 s (Temerario style is a slow open; there is no IRL→scan cut in a scan-only reel) |
| 2 | Beat sync | 5 | 8 cuts on bar lines of a kick-anchored 152 BPM grid; measured from frame diffs on the delivered file, max error 12 ms (< ½ frame). Hood opens 1 beat after the 12.69 s lift; separation on the brightest bar (25.32 s), lock on bar 21 (33.22 s) |
| 3 | 1:1 match | n/a | No IRL footage in this brief. Panel seating is exact by construction (panels carved from the full car) |
| 4 | Scan quality | 4 | Clean full scan (no ground, wheels/calipers captured), -0.5 EV satin silver on black (car median luma 199 / p90 236 vs Temerario 200/231). Rear plate flattened. Minor: thin wiper/strut slivers near the cowl in hood/explode shots, scan speckle on the tail-light lens, tyre-arch hole visible through the wheel at extreme close-up |
| 5 | Story | 4 | Reads turntable → detail → open → top → apart → together. Only four panels exist as state-scan pairs (no doors/trunk-open data), so the explode is lighter than the Temerario's |
| 6 | Grade | 5 | All renders, one look, AgX, no colour |
| 7 | Text | 5 | No text (brief) |
| 8 | Ending | 4 | Logo card cut in on bar 22 (34.80 s), holds through the final hit (37.95 s), fades with the music to silence at 39.27 s |
| 9 | Technical | 5 | 1080×1920, 30 fps, yuv420p, AAC, faststart (moov before mdat); no black frames; the 3-frame end-of-clip freezes of v1 were removed (src_fps slack) - only the assembler's 1-frame cut hold remains |

## Known weaknesses (first things to fix if the reviewer asks)
- Full-car shots hold the car at ~55-60 % of the 9:16 width (lots of black above/below). Lesson from 240SX says tighten by
  cropping into the car; I kept the whole car in for the turntables. Easy re-render: r 5.4 → 4.6 m.
- Explode float (≈26-31.6 s): the bumper sits partly off the left edge. Fix: bumper float at x +0.3 m or start the orbit at 45°.
- Close-ups are slowed up to 9.8 % (s8) to beat the minterpolate tail freeze; invisible on a slow slide, but next time render
  each shot 3 frames longer than its cue (keys over the cue length, extra frames extrapolated) instead.

## Data honesty
- Every panel is from our scans: hood/bumper/wing/skirt carved from `Blobeye Full Car.stl`; openings filled with the
  `bumper removed`, `hood removed`, `GD Scan Engine Bay`, `Rear Wing data` (wing-off rear) and `Sideskirt removed` scans as captured.
- Not used: the separate STi bumper and GD Sideskirt part scans (different session/fit), GD Scan Hood (fragment), game model, print CAD.
