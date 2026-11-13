# Honda Civic EK scan-process reel v5 — agent self-review (training/rubric.md)

Output: `/home/user/media/work/out/civic_ek_scan_process_v5.mp4` — 1080×1920, 30 fps, 31.40 s, H.264 + AAC. Earlier: review_v1..v4.md.
v5 = feedback on v4: "THE DEATH" (CML library track) was awful -> user's track "The Real Motorious City" (Gran Turismo 2 soundtrack).
Visuals as v4 (travel order front -> left -> rear -> top/hero -> listing); every cut re-timed to the new song.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 5 | powdering + the song's drumless break -> 1:1 cut to the scan on the phrase hit (3.20 s, -16 ms vs kick) |
| 2 | Beat sync | 5 | cutcheck: -16, 0, -8, -28, -26, -6, -2 ms vs kick peaks; cut B and the sweep each land on a phrase hit after a break |
| 3 | 1:1 match | 5 | unchanged from v4 (cam_A 18.3 mm, cam_B2 24 mm); rear wide slowed 0.81x but still ends on the match frame |
| 4 | Scan quality | 4 | as v4; right mirror touches the edge at the rear push-in peak (~15 s) |
| 5 | Story | 5 | as v4; software beat now runs into the song's break and the sweep starts on the next hit |
| 6 | Grade | 4 | HLG tonemapped; software beat is an upscaled viewport crop |
| 7 | Text | 5 | 24,997,508 TRIANGLES CAPTURED (STL header) on the front scan; EXTERIOR SCAN on the rear scan; nothing over IRL |
| 8 | Ending | 5 | dissolve to the listing on a hit (26.73 s); URL last; video ends in the drumless break just before the next phrase hit |
| 9 | Technical | 4 | music is a 128k YouTube rip (user-supplied) - fine for review, get a licensed/high-quality file before posting |

## Learned this round
- Library "trending" tracks (TikTok CML) read as stock music to this reviewer - ask for or offer real songs; the user supplies audio.
- Map a new song by onset flux + phrase novelty, not a fixed BPM grid: this track's accents sit on a 1.176 s half-bar with
  9.41 s phrases ending in breaks, which gave natural drop / cut B / sweep points.
- Slow-mo (setpts + minterpolate) in the assembler's `vf` path adds frames past `dur`; pre-render slowed IRL clips instead.
