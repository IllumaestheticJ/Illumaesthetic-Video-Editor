# A90 Supra scan-process reel v2 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/a90_scan_process_v2.2.mp4` — 1080×1920, 30 fps, yuv420p, H.264 + AAC, 28.17 s (845 frames).
Plan: `direction.md` (scene-director). Applies the user's two notes, the all-reels v2 brief and addendum A-D.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | the real Supra pulls up behind from frame 0; 1:1 transformation at 3.17 s on the bar downbeat |
| 2 | Beat sync | 5 | 5 cuts measured on the decoded audio of the delivered file: −14 / +2 / +15 / +2 / 0 ms vs kicks (3.181, 6.931, 8.185, 14.431, 16.933); bumper lands 9.43, inside faces lens 10.68, fender off on the 15.68 lift, bumper home 18.18, zoom-out 25.68, end on the 28.18 bar |
| 3 | 1:1 match | 5 | wider match (39.2 s, car ~67 % of the width, was ~95 %): cam_B LM-refined from cam_A, onion aligned on exhausts, emblem, recess, lamps, mirror, roofline; s1 frame 1 IoU 0.93 vs the solved render |
| 4 | Scan quality | 4 | front: Under Front Bumper replaces the full car's loose lip strips; Under Fender + arch Liners fill the corners; no ground; no wheels in any A90 scan |
| 5 | Story | 4 | rear → right side → front (bumper-removed hero: off toward camera, inside turned, push in on crash beam / radiator / ducts) → fender off (Under Fender) → x-ray whole car → listing. Each section once. Still no scanning/crew footage exists (option b) |
| 6 | Grade | 4 | HLG tonemapped; only the dusk street clips remain (shop clip dropped), so IRL warmth is consistent |
| 7 | Text | 5 | static labels (no 99.9 % counter), exact STL-header counts, feature names only where visible; subs ≤ 19 chars so they finish typing; scan shots only |
| 8 | Ending | 5 | x-ray arcs to the solved listing camera, morphs to the listing grey, 0.5 s dissolve; end card 5.2 s (was 7.4), title → logo → URL last, ends on the 28.18 bar with a 0.6 s music fade |
| 9 | Technical | 5 | no black frames; no duplicate frames at cuts (1-frame fades instead of `cut`, moves still running at each cut, src_fps tail fix); per-frame luma scan of every render: no lighting dropouts (persistent data off) |

## Rules applied (v2 brief)
- No implied data: rear bumper stays ON (no registered scan of the state under it: 2024 'Supra Rear' is bumper-on, 2021 fragments don't register); no trunk; shop bumper-off clip dropped.
- No cuts into nothing: every cut lands on a full frame (x-ray via same-pose switch).
- No repeated section, no reused shot, no wasted orbit (the only orbit is the x-ray arc that ends on the listing angle).

## Known issues
- The listing screenshot carries the 360 viewer's "Drag to rotate" hint during the dissolve.
- "What the scan is used for" labels not added: no file states it.
