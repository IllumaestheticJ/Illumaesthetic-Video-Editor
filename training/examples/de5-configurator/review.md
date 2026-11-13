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

# v2 (user's Drive photo set)

Output: `/home/user/media/work/de5/out/de5_configurator_v2.mp4` - 1080x1920, 30 fps, 28.90 s. Same grid and music as v1; shots B, C, D, E, G1, G2 rebuilt.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 2 | Beat sync | 5 | 17 cuts on the grid from frame diffs; drop at 13.10 s on the cut. No jump inside the orbit (max frame diff 1.6). |
| 3 | 1:1 match | 4 | match/check_v2.jpg (frames 392/393): trunk, emblem, tail lights, plate, diffuser, exhaust, glass coincide. The real wing sits a little lower and to the right of the configurator's default wing, so the blade and left endplate shift at the cut. |
| 5 | Story | 4 | Listing shot now shows the new hero; 1:1 and payoff are the pro photos. Install clips are still the Sport Wing shoot. |
| 6 | Grade | 4 | Pro photos at native resolution (no upscale); install clips unchanged. |
| 9 | Technical | 5 | Orbit sweeps ~75 deg with the car centred throughout. |

# v3 (user feedback on v2: install before the transition, end on the photo, brighter photo)

Output: `/home/user/media/work/de5/out/de5_configurator_v3.mp4` - 1080x1920, 30 fps, 21.80 s (654 frames).
- Beat sync 5: 14 cuts on the grid from frame diffs; audio drop 17.47 s = cut frame 524.
- Story 4: the 1:1 is now the ending. No end card or logo at all (user asked to end on the photo) - flag if a brand tag is wanted.
- Hook 2: the transformation is the last beat; first real footage at 8.7 s.
- Listing removals requested by the user (two driveway photos, first two blue renders) NOT done: blocked by the session's permission check; Shopify connector needs re-auth.
