# bf-integra-385-combo: draft v0.1 (user said "go" in chat, 2026-11-17; characters removed per owner)

v0.1 = v0 without Del & Eps (owner: "not use del & eps, just typical branding content"). The 3 stills generated
earlier (1.5 credits) are not used. Stage shots 1-4 re-framed centred.

Output: /home/user/media/work/out/bf-integra-385-combo_v0.1.mp4 (1080x1920, 30 fps, 19.77 s, 593 frames). Preview quality.

## What v0 is
| # | Frames (30 fps) | Content | Source |
|---|---|---|---|
| 1 | 0-96 | closed box; cyan scan sweep, lid flies off; "EPSILON+ BLACK FRIDAY" + "WHAT $385 GETS YOU" on black | Blender (box) |
| 2 | 97-167 | Sport Wing rises out of the box; receipt "SPORT WING $500" | lookbook GLB `part_sport_wing`, gloss black |
| 3 | 168-238 | Trunk lip rises; receipt adds "TRUNK LIP $100" | GLB `part_duckbill` |
| 4 | 239-309 | receipt: "COMBO $600" struck, "$385" stamps in; "LESS THAN THE WING ALONE ($500)" | Remotion-style PIL overlay |
| 5 | 310-379 | CGI Integra Type S (Platinum White), wing + lip drop on and seat | `eps-acura-integra-type-s-de5-v19.glb` |
| 6 | 380-450 | **hard 1:1 cut** to the full-car scan (silver), parts on, orbit toward rear-on | `Integra Type S Full Car.stl` (6 mm decimation), ICP to the GLB (median 5.8 mm) |
| 7 | 451-521 | real white Integra with the gloss-black Sport Wing (no text) | Dropbox Install Tutorial C0222, centre crop 9:16 |
| 8 | 522-592 | Epsilon+ wordmark 720 px, "SPORT WING + TRUNK LIP / $385 / BLACK FRIDAY / epsilon.plus" | Drive EPSILON+ Logos |
Cuts sit on the bar kicks of "Get Low" (101.7 BPM, bar 2.36 s), music from 0 s.

## Assumptions (defaults taken, list for the owner)
- CGI unboxing (no real unboxing footage exists). Parts gloss black (the $385 variant). Box is plain charcoal, no logos.
- No characters (owner decision). No Higgsfield video; the 3 earlier stills are unused.
- No dialogue, no claim text on the scan shot.
- Prices from the BF liquidation sheet (PRICES.md): wing $500, lip $100, combo $600 -> $385. No stock, no dates.
- **Changed from the plan:** the end photo (listing `white-rear-quarter`) shows a **paint-matched white** kit, not gloss
  black, so v0 skips it and uses C0222 (a real gloss-black Sport Wing) instead. The scan -> real cut is therefore a
  plain hard cut, not 1:1.
- The scan is the stock Type S; the GLB parts are placed in the GLB frame (the scan registered to it), not from the
  engineering CAD/part scan. The factory trunk spoiler on the scan was not removed (check for clipping in v1).
- Renders: Cycles CPU, 50 % res, 16 samples, every 2nd frame, blended to 30 fps. Characters are flat stills.

## Checks run on the delivered file
- Cuts vs kick attacks in the decoded audio: -6, +8, +15, -12, -5, 0 ms (the 168 cut is not detectable by frame diff;
  it sits on the measured attack by construction). All within half a frame.
- Loudness -13.6 LUFS integrated, true peak -1.8 dBFS (loudnorm + limiter, measured after the AAC mux).
- Render luma per frame steady in every shot (no light dropouts). Contact sheet reviewed.
- No text over IRL (shot 7). Prices only from the BF sheet. No stock counts or dates.
- Known v0 issues: box lid crosses the title in the last ~4 frames of shot 1; stage parts read small; car sits low in
  frame in shots 5-6; characters removed so shots 1-4 are product-only; the scan->real cut is not 1:1.
