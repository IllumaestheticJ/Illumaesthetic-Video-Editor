# Ferrari 296 GTB - sources

Scan-only reel: no shop footage. Engineering Drive folder `Ferrari 296GTB` (1VDR0KInScExiNy8cKdG95XwLgJ8VkqWD),
fetched with `ive fetch-drive` to `/home/user/media/ferrari-296/scans/`. All Artec exports share one frame
(front = -Y, car's right = -X); prepped with `--like car6.json`.

| Scan | Tris | What it is (looked at) | Used for |
|---|---|---|---|
| Full Car (1.25 GB) | 25.0M | whole car, ground scanned | decimated 6/4/3 mm, cropped; `car4` wide shots, `car3` close-ups |
| Front Fully Removed_2 | 4.0M | front end with hood/bumper off; hood captured **propped open** | frunk under the hood (cropped below z 120 mm raw) |
| Front Bumper Outer wraped / Inner | 1.0M / 1.2M | front bumper skin, both sides | exploded part |
| Rear Bumper Removed | 4.5M | rear with bumper off (+ rear wheel, ground scraps) | fill under rear bumper |
| Rear Bumper Outer / Inner | 1.25M / 1.5M | rear bumper skin | exploded part |
| Rear End No Diffuser | 2.5M | rear with diffuser off (+ stray low piece) | fill under diffuser |
| Rear Diffuser Outer / Inner | 1.5M / 2.0M | diffuser | exploded part |
| Engine Bay | 2.0M | engine bay under the lid | fill under engine cover |
| Enginer Cover | 0.45M | louvred engine lid (0.66 x 0.34 m) | opens 85 deg; exploded part |
| Hood Combined / Top / Inner | 1.5M / 1.0M / 0.9M | front lid, top + underside | Combined = opening + exploded part |
| Sideskirt Removed | 1.5M | right sill with skirt off | fill under skirt |
| Side Skirt Right | 0.75M | right side skirt | exploded part |
| Fender 1 / Fender 2 | 0.6M / 0.54M | **same** right front fender, two captures (identical bbox) | Fender 2 exploded (cleaner) |
| Fender Bracket | 25k | small bracket | not used (too small to read) |
| Brake Disk | 2.2M | front wheel arches with the wheel off (not an isolated disc) | not used; wheel close-up uses the full car |
| Exhaust Tip | 0.19M | exhaust tip | not used (tail area has lens holes) |

Registration: every part rendered red over the grey car (`/home/user/media/work/f296/reg/sheet_*.jpg`) and measured
(nearest-surface median 1.6-5 mm, mean offset <= 2 mm for outer panels). No transform changes needed.

Scan defects seen: tail-lamp lenses are holes (dark blotches up close); a strap hanging under the front bumper (removed,
`tools/clean_car.py`).

Reference: Temerario reel (`Video Jul 22 2026, 10 47 58 AM.mov`) not downloaded - each Dropbox link comes from a new
random host; worked from `training/references/README.md`.

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com (Shopify CDN), copied to `remotion/public/illumaesthetic_logo.png` (gitignored).
