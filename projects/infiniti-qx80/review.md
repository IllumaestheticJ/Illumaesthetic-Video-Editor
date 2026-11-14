# Infiniti QX80 v7 - self-review (training/rubric.md)

Output: /home/user/media/infiniti-qx80/out/infiniti_qx80_v7.mp4 (not in git), tools/build_v7.py. 1080x1920, 30 fps, yuv420p,
AAC, 1462 frames = 48.73 s. v6 review: review_v6.md. Reviewer notes on v6 (feedback.jsonl, 2026-11-14): theme colours to
match the website; floating motoIQ badge piece; add the GT-R brakes (scans + footage, in the files with the adapters).

Changes:
- Theme = illumaesthetic.com :root vars read with Playwright: bg #0b0c0b, accent #619f73, text #f2f3f1; Fjalla One titles,
  green JetBrains Mono eyebrows above them, answer card in the site hero pattern (HERE'S white / HOW. green). Kit parts in
  site green (were Ecky's viewport cyan). Render blacks lifted to #0b0c0b.
- Floating piece = Ecky's Fender_Vent_With_Logo_Left parked 0.5 m outside the car's right side; moved onto the K2 left vent
  (kitgroups.py FIX, 2.0 mm median). Checked on G_final360 frames 60-80: nothing off the body.
- GT-R BRAKES section (beats 42-48): scanned GT-R ring + caliper, our CAD 8288 hat + caliper adapter (Drive Brake/),
  exploded, landing one per beat. Same brake on the car in the final render (replaces preview.blend's generic Brembo models),
  caliper gold at the trailing side as in photos 1701/1702. Placement by geometry: caliper bridge arc R 232.7 concentric
  within 6 mm of the hub axis; ring 25.3 mm inboard of the hat from the scanned ring+hat pair. Front brake on all 4 corners.
- Timeline: scan day 2 stills, concepts 6 beats / 12 images, drop unchanged at 30.000 s (frame 900).

| # | Criterion | Score | Evidence |
|---|---|---|---|
| 1 | Hook | 4 | unchanged article hook, answer card on beat 8 |
| 2 | Beat sync | 4 | decoded cut frames = planned beat frames (all 14); grid measured vs audio in v6 (-23..+39 ms) |
| 3 | 1:1 match | 4 | 50/50 blend 899/900 still aligned (wheels, grille, roof) |
| 4 | Scan quality | 4 | floating vent fixed; brakes are real scans; tyres darkened (spec cut) |
| 5 | Story | 5 | scan day -> scan -> concepts -> panels -> brakes -> final render -> real car |
| 6 | Grade | 3 | photos as delivered |
| 7 | Text | 4 | site type/colours; eyebrows auto-fit (the first brake eyebrow clipped at the edge - caught on the frame, fixed) |
| 8 | Ending | 4 | wordmark only, fade over 2.2 s |
| 9 | Technical | 5 | ffprobe 1080x1920 h264 yuv420p + aac, 1462 frames |

Limits: no brake footage exists in the WhatsApp export or Dropbox (only the gold calipers behind the spokes in the finished
photos), so the brakes are renders; rear corners use the front brake; brake assembly placed by geometry, not a CAD assembly.
