# DE5 wing configurator demo v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/de5/out/de5_configurator_v1.mp4` - 1080x1920, 30 fps, 28.90 s (867 frames), h264 yuv420p + AAC.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Page scroll starts at frame 2; the transformation is at 13.1 s because the brief fixes the order (website first). |
| 2 | Beat sync | 5 | 17 cuts measured from frame diffs, all on 393 + round((beat-24)*16.36). Audio drop measured at 13.10 s = the 1:1 cut (frame 393). |
| 3 | 1:1 match | 5 | Edge overlay of frame 392 on 393 (match/check.jpg): endplate, both swan uprights, blade, emblem, plate, tail light, diffuser and exhaust coincide. Model uprights are yellow / bases purple vs black on the car; low-poly body. |
| 4 | Scan quality | n/a | Configurator's own view, not a house scan render. |
| 5 | Story | 3 | Site -> listing -> configure -> cart -> 3D -> real -> install -> finished. The brief said TC wing; video is the GT Wing (user's choice, no real TC photo exists). Install clips show the Sport Wing install, so the install section is a different wing than the one configured. |
| 6 | Grade | 3 | Sony flat clips lifted (contrast 1.32, gamma 1.18, sat 1.35) but still darker and softer than the phone photos; 608 px windows upscaled 1.78x. |
| 7 | Text | 5 | None added; only the site's own UI. |
| 8 | Ending | 4 | Epsilon+ card on beat 46 (25.10 s), 0.9 s fade. Not the Illumaesthetic card. |
| 9 | Technical | 4 | Specs met. Match photo is 1450 px tall, upscaled 1.32-1.37x; 66 in wing does not fit a 9:16 frame, so photo shots pan across it. |

## Known gaps
- Checkout stops at the cart popup (Add to cart -> popup -> tap on Checkout); Shopify checkout pages were not entered. The popup's own text overlaps on a 432 px viewport (site layout, not edited).
- Native select menus do not render in headless capture: Make/Model changes show as tap -> value changes.
- Music is the CML preview file; attach the same sound in TikTok when posting (drop = 35.97 s of the track, video starts at 22.87 s).
- Instagram was not reachable from this environment; photos are from the epsilon.plus listing only.
