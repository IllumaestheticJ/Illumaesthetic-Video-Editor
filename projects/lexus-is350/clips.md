# Lexus IS350 (2026 facelift) — sources

## Deliverable
Scan-only Temerario-style reel, 1080x1920, no IRL footage, no text. ILLUMAESTHETIC logo end card.

## Scan data (engineering Drive `Lexus 4is`, 1RI5YIMmHU9GC1ziv7P6u5ZQJoU0Bnhsv)
**Two different cars in this folder.** The root `Lexus 4IS IS350 Full Car.stl` (1IOKNZ0p..., 2026-08-18) is an OLDER IS350
(badge inside the spindle mesh, plate 9JTY488, its own wheels). The `2026 IS350 Facelift/` scans are the facelift car
(badge on a horizontal bar, new mesh, empty dealer plate frame, different wheels) - aligned in Artec onto the old car's
unchanged panels. The reel uses the **facelift scans only** (editlog). Media: /home/user/media/lexus-is350/{lev,fl,prep}.

The facelift set is a **front clip**: bumper -> A-pillar base (prepped y -2.37..-0.76 m), nothing above 1.02 m.
Registration vs its own base (`Front End Hood Closed`, regcheck 150k pts, median): see table.

| Scan (facelift) | Drive id | What it is | Reg. median | Used as |
|---|---|---|---|---|
| Front End Hood Closed | 1SbKXbrvzKi8CS6hQyDLtTdEtFS732DaX | bumper, grille, lamps, fenders, wheels; **no hood skin** | base | base of every shot |
| Hood Open | 1O3NLYsxzG3ySzcgnBILwiXPXPMR0n_M1 | the hood alone, propped open (+ struts) | 0.94 mm | hood panel; closed by inverse fitted hinge (hinge.json, fit 2.4 mm) |
| Bumper and Hood Removed | 1HA67RPGn4wvYar9IsHgH-PQBe9jzyOSK | crash beam, radiator, headlamp housings, engine bay | 1.84 mm | bay / structure fill under hood and bumper |
| Bumper Removed | 1BT47s_jPE8o6NcBcW3rOOyv0pFKyh8dt | the removed bumper (complete) | 1.93 mm | trim only |
| Bumper (Duct and Fogs Removed) | 1CEU-UVmnNLo6PRvZf8uTtAtWF5kY1o6g | bumper shell without ducts/fog covers | 7.29 -> 3.29 mm after ICP (shell_icp.json) | explode: shell |
| Fog Covers | 1vnZ5brXkBKtk_W53Qd6gV9hsxxSIuPZP | L+R fog covers | 2.40 mm | explode (split L/R) |
| Bumper Ducting | 1vJlNTZ9ggdRT7vEo3W_6v2icKDZW35gr | L+R ducts | 2.80 mm | explode (split L/R) |
| Bumper Top Bracket | 11dRl4zQ6h1fUonwrVNFSgxRwlm2q5Bgp | upper bumper bracket | 6.28 mm (ICP = sliding) | explode |
| Radar Unit + Radar Bracket | 1EFah2_..., 1_wLC3ic... | hidden behind grille (low overlap, identity) | - | explode |
| Front Grille | 17iMQRczVq4f5Pz5veUsxM_2iUEoH8pxc | grille alone | 2.82 mm | not used (in the shell) |
| Wheelwells | 1FGXsxK3qgZJVsezNRuqA53wzoaN14Qdt | front end with wheel-well liners/suspension | ~1.7 mm | not used |
| Not used | Bumper Stripped (Warped, Warped2), Top Mounting Tabs, Radar Removed, IS500 Front End, 2025 reflector scans | | | warped / other car |

Weak data: hood top is speckled (dusty glossy capture) - keep it out of close-ups; dealer plate frame
("SWICKARD / LEXUS OF FREMONT", no plate) legible up close; deep bay behind the radiator unscanned; clip ends at the
A-pillar (no cabin, sides end at the front doors), so no rear/side/trunk scenes.

## IRL footage (not used in this reel — for a future 1:1-cut version)
Dropbox `/2. Illumaesthetic Videos/1. Video dumps/IS350 scanning Speed run` — 15 Sony FX30 clips
FX30541–FX30555.MP4 (+ M01.XML sidecars), shot 2025-07-12 01:14–01:44 UTC, total ~21 GB.
Big takes: FX30541 (5.6 GB), FX30542 (3.8 GB), FX30547 (2.1 GB), FX30544 (2.0 GB), FX30545 (1.7 GB),
FX30552 (1.6 GB), FX30551 (1.5 GB), FX30546 (1.0 GB); short: 30543/48 (200 MB), 30549 (134 MB), 30550 (537 MB),
30553 (604 MB), 30554/55 (470 MB).
**Caution for the 1:1 version:** this footage is dated 2025-07-12, i.e. the 2025 "4IS" session (reflector scans
2025-07-17), a year before the 2026 facelift scans. Check the car's front end in the footage matches the facelift
scan state before solving a match cut; it may be the pre-facelift car. Not downloaded or watched (scan-only brief).
