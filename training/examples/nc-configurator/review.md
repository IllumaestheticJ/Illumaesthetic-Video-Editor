# NC wing configurator demo v1 - self-review (training/rubric.md)

Output: `/home/user/media/work/nc/out/nc_configurator_v1.mp4` - 1080x1920, 30 fps, 29.17 s, h264 yuv420p + AAC.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 3 | Page scroll starts at frame 2, but the transformation is at 12.5 s: the brief fixed the order (website first). |
| 2 | Beat sync | 5 | 19 cuts measured from frame diffs, all on round(beat*10.428). 1:1 cut on the drop. |
| 3 | 1:1 match | 4 | Edge overlay of frame 374 on 375: tail light, plate, emblem, bumper, wing blade and upright foot coincide. Real car has a hardtop (model: soft top), real endplates are larger than the configurator's, uprights black vs yellow. |
| 4 | Scan quality | n/a | Configurator's own low-poly view (grey on light grey), not a house scan render. |
| 5 | Story | 4 | Site -> listing -> configure -> cart -> 3D -> real -> install -> finished. Install footage is an Integra, not an NC. |
| 6 | Grade | 3 | Sony clips lifted (contrast 1.2, gamma 1.3) but still darker/greyer than the iPhone photos. |
| 7 | Text | 5 | None added; only the site's own UI. |
| 8 | Ending | 4 | Epsilon+ card on the downbeat (26.43 s), 0.9 s fade. Not the Illumaesthetic card. |
| 9 | Technical | 4 | Specs met. Tutorial clips are 608 px-wide windows upscaled 1.78x. |

## Known gaps
- Checkout stops at the cart popup (Add to cart -> "Added to your cart" -> tap on Checkout); Shopify's checkout pages were not entered.
- Music is the CML preview file; when posting, attach the same sound in TikTok so it is credited (drop = 24.9 s of the track, video starts at 12.4 s).
- Native select menus do not render in headless capture: the model change on the home page shows as tap -> value changes.
