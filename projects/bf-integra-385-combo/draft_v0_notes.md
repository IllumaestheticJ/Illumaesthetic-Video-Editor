# bf-integra-385-combo: draft v0 (user said "go" in chat, 2026-11-17)

Output: /home/user/media/work/out/bf-integra-385-combo_v0.mp4 (1080x1920, 30 fps, ~22.1 s). Preview quality.

## What v0 is
| # | Frames (30 fps) | Content | Source |
|---|---|---|---|
| 1 | 0-96 | Eps (aiming scanner) + closed box; cyan sweep, lid flies off; title "WHAT $385 GETS YOU" on black | Blender (box), Higgsfield still |
| 2 | 97-166 | Sport Wing rises out of the box; receipt "SPORT WING $500" | lookbook GLB `part_sport_wing`, gloss black |
| 3 | 167-237 | Trunk lip rises; receipt adds "TRUNK LIP $100" | GLB `part_duckbill` |
| 4 | 238-308 | Del points at the receipt: "COMBO $600" struck, "$385" stamps in; "LESS THAN THE WING ALONE ($500)" | Higgsfield still |
| 5 | 309-379 | CGI Integra Type S (Platinum White), wing + lip drop on and seat | `eps-acura-integra-type-s-de5-v19.glb` |
| 6 | 380-449 | **hard 1:1 cut** to the full-car scan (silver), parts on, orbit toward rear-on | `Integra Type S Full Car.stl` (6 mm decimation), ICP to the GLB (median 5.8 mm) |
| 7 | 450-520 | real white Integra with the gloss-black Sport Wing (no text) | Dropbox Install Tutorial C0222, centre crop 9:16 |
| 8 | 521-662 | Epsilon+ wordmark 720 px, "SPORT WING + TRUNK LIP / $385 / BLACK FRIDAY / epsilon.plus" | Drive EPSILON+ Logos |
Cuts sit on the bar kicks of "Get Low" (101.7 BPM, bar 2.36 s), music from 0 s.

## Assumptions (defaults taken, list for the owner)
- CGI unboxing (no real unboxing footage exists). Parts gloss black (the $385 variant). Box is plain charcoal, no logos.
- Del & Eps: 3 Higgsfield GPT Image 2.6 stills from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`
  (jobs 749ddd8e, 692a55bb, 7157b202; 1.5 credits total), composited as stills with a fade/scale-in. No video generations.
  Characters never touch the parts.
- No dialogue, no 10 mm sting, no claim text on the scan shot.
- Prices from the BF liquidation sheet (PRICES.md): wing $500, lip $100, combo $600 -> $385. No stock, no dates.
- **Changed from the plan:** the end photo (listing `white-rear-quarter`) shows a **paint-matched white** kit, not gloss
  black, so v0 skips it and uses C0222 (a real gloss-black Sport Wing) instead. The scan -> real cut is therefore a
  plain hard cut, not 1:1.
- The scan is the stock Type S; the GLB parts are placed in the GLB frame (the scan registered to it), not from the
  engineering CAD/part scan. The factory trunk spoiler on the scan was not removed (check for clipping in v1).
- Renders: Cycles CPU, 50 % res, 16 samples, every 2nd frame, blended to 30 fps. Characters are flat stills.
