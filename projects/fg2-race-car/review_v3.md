# FG2 #806 race car reel v3 — self-review (training/rubric.md)

Output: `/home/user/media/work/out/fg2_race_car_v3.mp4` — 1080x1920 TikTok, 30 fps, 20.67 s. Earlier: review_v1.md, review_v2.md.

v3 change (user): the CGI layer is the Epsilon lookbook game model, not Ecky's red-painted scan and not the
wing-configurator glb (a decimated scan). Source: lookbook frames JSON `lb-honda-civic-fg2-5ec63ee519.json`
-> `eps-honda-civic-fg2-v10.glb` on the Shopify CDN. Placed in the scan frame (lip-to-lip fit, then body ICP: 15.7 mm
median, scale 0.990) so every existing camera solve applies unchanged.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Unchanged: tight on the painted lip, real→scan 1:1 at 1.60 s. |
| 2 | Beat sync | 5 | 16 cuts within ±17 ms; drop on the 6.37 s angle change. |
| 3 | 1:1 match | 4 | Game model sits on the photos within the game-vs-scan tolerance (~1-2 cm); intra-angle cut blends are single images. |
| 4 | Scan quality | 3 | Unchanged LQ scan (before-state). |
| 5 | Story | 5 | Scan (data) → modelled CGI (design, painted lip) → real car now reads as three distinct states. |
| 6 | Grade | 4 | CGI lit by Ecky's sky on his dark ground, black background like his CGI→real reference. |
| 7 | Text | 5 | None. |
| 8 | Ending | 4 | Epsilon+ wordmark on the downbeat. |
| 9 | Technical | 4 | Specs met; P1/P2 photo resolution caveat as in v2. |

## Choices to confirm with the user
- Paint Rallye Red R513 gloss (the lookbook's default for this car, and the #806 colour); lip part painted to match.
- Rims switched from the model's dark finish to silver (the #806 runs silver Enkei RPF1s; Ecky's CGI also silver).
- Lookbook kit includes the TC wing; hidden (standing rule: no wing unless configurator-exact; #806 runs the GT wing).
