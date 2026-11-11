# Porsche 911 GT3 RS (992) - sources

Scan-only Temerario-style reel: no shop footage, no text. Engineering Drive folder `Porsche 911 GT3 RS (992)`
(11lseSQnQHuYzyaaZk_sdVS_RaZSiI1qE), listed recursively with the service account, fetched with `ive fetch-drive` to
`/home/user/media/porsche-gt3rs-992/scans/` (+ `scans_ub/` for two underbody scans).

Frame: the raw Artec frame had the ground tilted 3.4 deg and the car diagonal. `tools/level.py fit` (copied from
huracan-evo) on the 4 mm car -> `level.json` (ground normal -> +Z, long axis -> Y); the same transform is applied to
every part STL, then everything is prepped `--like car4.json`. Prepped frame: front = -Y, car's left = +X, z=0 ground.
Car 4.58 m x 1.98 m (incl. mirrors) x 1.32 m (wing top) - matches the RS.

| Scan | Tris | What it is (looked at) | Used for |
|---|---|---|---|
| gt3 rs Full Car (1.25 GB) | 25.0M | whole car + ground | 4 mm (`car4`, 3.3M) wide shots; 2.5 mm (`car2p5`, 7.7M) close-ups |
| Front Lower Lip | 0.1M | splitter lip | lift + explode |
| Front Bumper Strake | 0.4M | both bumper-corner strakes | lift + explode |
| Front Grille Trim | 0.3M | centre intake trim (grille bars partly holes) | lift + explode |
| Fender Vent | 0.4M | right front fender louvre panel | explode |
| Hood Vent Top (Warped) | 3.9M | left hood nostril top | lift + explode |
| hood vent interface assembled (left) | 5.4M | left nostril duct | stays on the car (reads as a bracket when moved) |
| Side Skirt (upper) / Sideskirt (lower) / Side Skirt Strake | 1.0M / 1.0M / 4.5M | car's left sill pieces | explode |
| Rear QPanel Intake 1 / 2 | 0.45M each | right / left rear quarter intakes | explode |
| Rear Bumper Strake | 3.8M | left rear bumper fin | explode |
| Rear Diffuser 1 (2 = second capture, same bbox) | 1.1M | diffuser fins + undertray | explode |
| Rear Diffuser Trim-Outer (Inner = same zone) | 1.6M | lower rear bumper trim | explode |
| Rear Bumper | 2.5M | rear bumper skin | not used (removing it opens the hollow car) |
| Hood Vent Interface Right / no Fins, Hood Vent Fins | 3.9-5.8M | duct + fins | not used: centred under the hood in another frame, invisible over the car |
| Porsche 911 GT3 (992) Rear Diffuser | 7.0M | 350 mm off in another frame, non-RS name | not used (brief: our RS scan data only) |
| Underbody DRS Closed / DRS Open Rear | 3.0M each | underside captures | not used: own frame (ICP 2-4 cm off); open vs closed wing differs < 8 mm |
| Alex / GT3RS Full Assembly.blend | 4.6 GB | assembly file | not used |

Registration sheets: `/home/user/media/work/gt3/reg_all_*.jpg` (part red over grey car | close | part alone).
Defects seen: hood nostrils are dark holes in the car scan, small dark blotch on the hood near the windscreen,
grille bars partly missing - close-ups avoid the hood top.

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from www.illumaesthetic.com (Shopify CDN; the bare domain returned a
429 bot check, the www host with a browser UA worked), saved to `remotion/public/illumaesthetic_logo.png` (gitignored).
