# FG2 #806 race car — source media

Media is never committed. Local paths under `/home/user/media/fg2/` (sources) and `/home/user/media/work/fg2/` (renders/layers).

## Finished photos (epsilon.plus product pages, Shopify CDN)
Same car throughout: Honda Civic Si coupe FG2 #806 (806 on hood; #19 door numbers at a WTCC event).

| Used | Angle | File (epsilon.plus) | Size | Lip | Notes |
|---|---|---|---|---|---|
| P1 | front 3/4, car left side | `civic-coupe-fg2-front-lip-race-car-front-quarter.jpg` (Front Lip FG2 page) | 2048x1365 | painted red | wing visible, shop lot; f≈28 mm-equiv |
| P2 | low front 3/4 profile | `civic-coupe-fg2-front-lip-red-race-car.jpg` | 2048x1366 | painted red | tele (f≈67 mm-equiv), wing visible |
| D | side 3/4 | `civic-coupe-fg2-gt-wing-motorsport-front-quarter.jpg` (GT Wing FG2 page) | 4096x2731 | painted white | 806 door number, stock mirror |
| E | rear 3/4 | `honda-civic-coupe-fg2-gt-wing-red-race-car-rear-quarter.jpg` | 4096x2731 | not visible | Epsilon GT wing hero |
| no | front 3/4 | `civic-coupe-fg2-front-lip-front-on.jpg` | 4032x3024 | **black unpainted** | solved (match/ in work dir) but dropped per user feedback |
| no | straight front | `civic-coupe-fg2-front-lip-red-front-view.jpg` | 2048x1366 | black unpainted | dropped per user feedback |
| no | front 3/4 | `...-livery-front-quarter.jpg`, `...-red-meet.jpg` | 4032x3024 | black unpainted | |
| no | rear close | `civic-fg2-gt-wing-race-number-806-rear-view.jpg` | 4096x2731 | – | too close: wing cut off |
| no | blue FG2 photos | `...-blue-*.jpg` | | | different car |

Drive `Honda FG2 F1..R3.jpg` (owner 96ronald, folder 1FtdGVM5uP8XEbRDxcSkuuxF4khv987iq) are **not** IRL photos: 13854x9167
scan-product renders (solid / x-ray / exploded). Useful later as scan-look references only.

## Scan (engineering Drive `Honda Civic FG2/Scan Data`)
- `Civic FG2 Full Car (LQ).stl` 1-WqSI5VbZkXIp1tzoGuLibSjB0DC97YH — 4,866,098 tris, mm. **Used.** Same raw frame as Ecky's .blend (identity transform, /1000).
- `Civic FG2 Full Car (HQ).stl` 1-WA9LSCzGhIqNEuq2AHeKFETBbrt8maa — 47.75 M tris; **different coordinate frame** (bbox x −311..4090 mm vs LQ −2335..2411) so not used; decimated copy at work/fg2/scan/fg2_3mm.stl if someone aligns it.
- Stock-state car with plate, stock spoiler, glass not captured (windshield is a hole).

## CGI (Ecky)
- `74 - Civic FG2 Race Lip/FG2 Race Lip.blend` 1m-e2MyW1BUEomNnXmGenRnlraom0fG0m — LQ scan + CAD `Front Lip` (mirror+subsurf+booleans) + tyre models, red Material.003, black ground plane, Nishita sky. **Used for all CGI layers.** Tyre image textures are missing (render magenta) → dropped in render.
- `FG2 Race Lip.stl` 1yJIGKWd53DhUMKKmkBHk1Z7wWz7wraqd — full-width lip in the scan frame; **added to every scan render** (user: include the lip in the scan shots).
- `71 - Civic FG2 Race Car Body Kit/Civic FG2 Bodykit for turn10.blend` — bumper + skirts, no wing. Not used.
- `FG2 Si/GT wing FG2.stl` (engineering, 1rQ-WLy5VCaAy2c3VRmfAXtqUwYhIara1 / sales copy 1-y23InUV-WMWm6ao9CxeVcAiIxf1igFt) — blade + endplates in the scan frame; added to the E CGI with stand-in uprights.
- `FG2 Lip CGI-Real.mp4` 1itRtubjAyFciRvZC0IKNiRUqHEoOTuET — Ecky's CGI→real reference (1080x1920 60 fps, 52 s): CGI on black/dark ground cut to the same pose IRL.

## Music
User upload `Macarena_Los_del_rio_--_Slowed_and_Reverb.mp3` (417 s). Opening only: sound starts 1.93 s, drop 13.874 s, 75.34 BPM (0.7964 s beat).
Audio placed from 7.503 s so the drop hits video 6.371 s.

## Logo
Drive `IllumaestheticLogoColor-01.png` 1cZJj521P88T_vC2YZDJVVUCctGyNoukR (6447x1434 RGBA).
