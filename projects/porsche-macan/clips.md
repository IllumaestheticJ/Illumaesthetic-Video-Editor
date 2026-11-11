# Porsche Macan (Electric) - sources

Scan-only reel: no shop footage, no text. Engineering Drive folder `Porsche Macan` (1O34yDfZ6VLdCfdJl3p69sHB_6d2OBJh7),
listed recursively with the service account, fetched with `ive fetch-drive` (raw STLs deleted after decimation;
work files in `/home/user/media/porsche-macan/{dec,lev,comp,prep}`).

Frame: one rigid levelling transform for every scan (`tools/level.py fit` on the full car, then `apply`; ground normal
0.038/0.038/0.999, plus a 180 deg yaw): front = -Y, car's right = -X, ground Z=0 - same convention as ferrari-296.
All `.blend`s prepped `--like car4.json`.

| Scan (Drive) | Tris raw -> used | What it is (looked at) | Registration (median to full car) | Used for |
|---|---|---|---|---|
| Macan Full Car | 25M -> 4.0M (4 mm) / 6.7M (3 mm) | whole car + ground | - | `car4` moves, `car3` close-ups, base of all composites |
| Front Left Door (Interior/) | 0.45M | full door: outer skin + card | 1.4 mm | exploded door (+ car skin) |
| Front Right / Rear Left / Rear Right Door (Interior/) | 0.3-0.4M | mostly door cards; outer skin patchy (RL almost none) | 2.0 mm / card sits inside / skin z-fights | exploded doors **with the car's own skin added** inside each door outline (tools/build.py) |
| Doors and Hood Open | 3.9M (4 mm) | doors + hood open, cabin + bay visible | 1.2 mm | hood hinge fit (open hood), fill for the door openings |
| Hood / Hood Removed | 0.98M / 1.26M | hood panel / bay under it | 2.4 / 1.8 mm | hood part / fill |
| Rear Hatch Closed / Fully Open | 1.4M / 1.2M | rear end, hatch shut / up | 1.3 / 1.4 mm | hatch panel extraction + hinge fit / boot fill |
| Fender / Fenders Removed | 0.26M / 1.6M | car's left front fender / front end with fenders off | 1.7 / 2.0 mm | exploded fender / fill (x>0 only) |
| Front Bumper (Warped) / Front Bumper Off | 1.7M / 2.2M | bumper skin / front end without it | 4.4 mm (ICP would move 10.7 mm) / 2.0 mm | exploded bumper / fill - visibly covers the car's bumper, used |
| Rear Bumper (Warped) / Rear Bumper Removed | 1.4M / 1.7M | bumper skin / rear without it | 2.7 / 4.1 mm | exploded bumper / fill |
| Headlights, Tail Lights | 0.6M / 0.1M | lamp units | 2.1 / 1.9 mm (headlights 17 % overlap: mostly inside the body) | not used (headlights scan has a stray strand) |
| Interior Doors Open | 4.7M | cabin with doors open | 5.0 mm, 12 % overlap | not used (Doors and Hood Open registers better) |
| Not fetched | | Chassis Headlights Removed, Dash, Underbody, Roof HD, Wheel Wells HD, airbags, seats, trim, "For Andy" template | | not needed for the shot list |

Registration renders: `/home/user/media/work/macan/reg/*/sheet.jpg` (parts in colour over the grey car).

Logo: `IllumaestheticLogo_V2COMPLETE_1.png` from illumaesthetic.com/cdn/shop/files -> `remotion/public/illumaesthetic_logo.png` (gitignored).
