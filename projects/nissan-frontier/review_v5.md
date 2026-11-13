# Nissan Frontier Pro-4X -> RONIN reel v5 - self-review (training/rubric.md). Earlier: review_v4.md ... review_v1.md

Output: /home/user/media/work/frontier/out/nissan_frontier_v5.mp4 - 1080x1920, 30 fps, h264 yuv420p + AAC, 52.93 s, 1588 frames.
v5 = v4 unchanged to 33.83 s, then the RONIN section (user request): RONIN GRILLE -> WIDE FENDERS -> 35-INCH WHEELS -> LIFT KIT
-> RONIN LIVERY (sweep on the replayed crash) -> GT-R TWIN TURBOS label -> fade -> logo.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | unchanged |
| 2 | Beat sync | 5 | all cuts within +-15.1 ms of the decoded onsets (9 measured; 1162/1270 by arithmetic: -11/-15 ms) |
| 3 | 1:1 match | n/a | scan-only |
| 4 | Scan quality | 3 | grille + fenders are the team's CAD (registered, overlay-checked); wheels are a generic stand-in, lift is a 0.10 m wheel drop, turbo is a label only - none of those three are data |
| 5 | Story | 4 | stock scan -> sections -> reassembly -> Ronin upgrades one per beat -> livery reveal |
| 6 | Grade | 4 | livery teal from the PSD; side shots frame the whole truck so it reads small in 9:16 |
| 7 | Text | 4 | one label at a time; names from the user (35-inch Nissan off-road wheels, GT-R turbos under the truck); no specs invented |
| 8 | Ending | 4 | livery hero orbit, fade, 700 px logo; music = track with beats 32-56 replayed once |
| 9 | Technical | 5 | exact frames, luma clean, nothing clipped |

Known gaps: side shots in the Ronin section are wide (truck ~55 % of frame width); livery on hood/roof/front/rear is the topo tile
only (the PSD is a side view); bumper lower is teal not black as in the reference renders; no real wheel/suspension/turbo models.
