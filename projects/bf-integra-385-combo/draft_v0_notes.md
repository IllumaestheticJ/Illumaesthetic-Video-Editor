# v1.2 dropped (user, after the owner revised the rule to 1.8 s / +0.3 s per word / 2.2 s prices and asked that
# approved videos not be changed for it): "v1.1 only". Queued re-render cancelled; shots.py/composite.py back to v1.1.
# Under the revised rule v1.1 is slightly short on the lip line (1.9 s), RETAIL $600 (2.1 s), was/now (2.0 s) - accepted.

# v1.2 (user approved the slow-for-text fix: "yes")
- shots.py LEN S1 168 (closed box + title holds one more bar; sweep 109-141, lid 141-163), S3 141, S4 284.
- composite.py: timeline cuts 168 239 380 664 734 805 876 947, end 1089 (36.3 s); kick errors measured -6..+14 ms.
  Price card: RETAIL $600 f8-142 (4.5 s), loading f98-142, $385 + struck $600 f142-284 (4.4 s).
- render_hq12.sh: S1/S3/S4 at 1080x1920 32 spp true 60 fps, queued behind the v1.1 render (one Blender job at a time).
  1186 frames at ~22 s/frame, about 7 h.

# Text-timing audit (owner rule 2026-11-18 "slow down for text"; v1.1 60 fps as rendered, cuts 30 fps 97/168/239/380)
Readable = fully in -> cut/out. Minimum: 2.5 s for 1-3 words + 0.4 s/extra word; >= 3 s for any price or was/now pair.
| text | readable | min | result |
|---|---|---|---|
| S1 title "EPSILON+ BLACK FRIDAY / WHAT $385 GETS YOU" | 2.77 s (fr 14-97) | 3.0 s (price) | FAIL -0.23 s |
| S2-3 receipt "SPORT WING RETAIL $500" | 7.4 s (fr 16-239) | 3.0 s | ok |
| S3 receipt "TRUNK LIP RETAIL $100" | 1.9 s (fr 14-71 of S3) | 3.0 s | FAIL (repeated on the price card, but its own box is short) |
| S4 "COMBO RETAIL $600" before the strike | 2.1 s (fr 8-71) | 3.0 s | FAIL |
| S4 was/now "$600 struck -> $385" | 2.0 s (pop settles fr 80-141) | 3.0 s | FAIL |
| End card logo + SPORT WING + TRUNK LIP / $385 / BLACK FRIDAY / www.epsilon.plus | 4.3 s | 3.4 s | ok |
Proposed v1.2 fix (needs user approval; the v1.1 render was already in flight):
- S1: title fully in by fr 6 and the shot holds 1 bar longer (+71 fr) -> ~5.2 s.
- S3: + 1 bar (+71) with the parts rise slowed -> LIP line ~4.3 s.
- S4: + 1 bar before the strike and + 1 bar after (4 bars, 283 fr): RETAIL $600 ~4.5 s, was/now ~4.4 s; loading bar spans the extra bar.
- Cuts stay on measured kicks (bar = 70.7 fr); total grows 26.9 s -> ~36.3 s. Re-render S1/S3/S4 at 60 fps ~2.3 h.

# v1.0 (user: "the colors in the beginning are super unnatural - make it the color of an actual cardboard box" +
# "with an epsilon logo on it"; owner: Akira supplied)
- Box: kraft corrugated cardboard (procedural fibre noise + bump), clear tan packing tape along the lid seam, Epsilon+
  wordmark printed in matte black on the front face and on the lid. Neutral warm-grey studio backdrop, white/warm rims
  (violet stage, cyan band and coloured rims removed). Shots 1-4 re-rendered (render_v10).
- Fonts: Akira Expanded Super Bold for WHAT $385 GETS YOU and the $600/$385 card prices (file at
  assets/fonts/akira/, gitignored; Drive 1nrF80enolDd9HAu5807kv5XIx0cUSDya). Unbounded stays for labels and the end card.
- Price card made opaque (the box print ghosted through). 26.9 s; -13.4 LUFS; TP -1.8 dBFS; safezone_check OK.

# v0.9 (owner font rule, knowledge/fonts.md)
- Headlines/prices (WHAT $385 GETS YOU, $600, $385 on the price card): Akira -> **Unbounded 700 stand-in** (Akira file
  not supplied; 800-900 weights not in the repo). Swap `F_AK` in tools/composite.py when the owner uploads Akira.
- Receipt labels, item lines, LOADING bar text: Unbounded 400/500 (companion font, dense table).
- End card next to the Epsilon+ wordmark: Unbounded (SPORT WING + TRUNK LIP 400, $385 500, BLACK FRIDAY 400, URL 300).
- JetBrains Mono / Inter no longer used. Safe zones OK; timing/loudness unchanged.

# v0.8 (user: undiscounted prices labelled retail)
- Every undiscounted price carries a small grey RETAIL tag (SPORT WING RETAIL $500, TRUNK LIP RETAIL $100) in the
  unboxing receipts and the price card; the big $600 reads COMBO RETAIL. Safe zones OK; timing/loudness unchanged.

# v0.7 (user: "take out the 'less than wing alone', show that its retail price and then do a BF price loading")
- Price shot (frames 239-379, 2 bars): f0 receipt with SPORT WING $500 / TRUNK LIP $100 and big RETAIL $600;
  f27 (2nd kick) BLACK FRIDAY PRICE + loading bar (LOADING... + %) filling to the next downbeat; f71 (bar-2 downbeat,
  10.32 s) $385 stamps in and $600 is struck (pink); holds to the cut (~2.3 s). "Less than the wing alone" removed.
- Card x 250-849, y 915-1429 (safe zones OK, clears the trunk lip). Rest unchanged. 26.9 s; -13.4 LUFS; TP -1.8 dBFS.

# v0.6 (user: "have the numbers for deals a little longer so people can read it easier")
- Price shot (receipt $600 struck -> $385, "less than the wing alone ($500)") is now 2 bars, frames 239-379: $385 holds
  ~3.5 s (was ~1.2 s). Shot 4 re-rendered at 141 frames (render_v06).
- End card ($385, www.epsilon.plus) is now 2 bars, frames 664-805 (4.7 s), with a slow 3 % push-in.
- 26.9 s total. Cuts -6/+8/-13/0/+9/+13 ms vs kicks; -13.4 LUFS; TP -1.8 dBFS; safezone_check text boxes OK.

# v0.5 (owner, 2026-11-17): end-card URL reads www.epsilon.plus. safezone_check text boxes OK. Output bf-integra-385-combo_v0.5.mp4.

# v0.4 (owner safe-zone rule, 2026-11-17)
- All text, prices and logos inside x 48-920 / y 285-1440: shot-1 tag/title moved down (y 330-667), receipts in shots
  2-3 moved to y 330, shot-4 receipt to y 880-1415, end-card product line 54 -> 46 px (x 180-899).
- Car shots re-aimed (camera targets 0.3-0.6 m lower) so the car clears the bottom 480 px and reads in the 4:5 crop;
  shots 7-9 re-rendered (render_v04). C0240 panel moved to y 285-1435.
- `python scripts/safezone_check.py ... --text-boxes bf-integra-385-combo_v0.4_textboxes.json` -> text boxes OK (exit 0);
  tools/text_boxes.py exports the boxes from the overlays. Sheets: v0.3 (before) / v0.4 (after).
- Output /home/user/media/work/out/bf-integra-385-combo_v0.4.mp4; cuts and loudness unchanged (-13.8 LUFS, TP -1.8 dBFS).

# v0.3 (user feedback on v0.2, 2026-11-17)
User: "fix the camera shake at the end, smoother. If that doesn't work, use another video/roller" / "we should have a
wingless scan in the DE4 scan section (same trunk)" / "add color to the box and the beginning".
- **End shot:** C0240 11.8-15.2 s stabilised with ffmpeg vidstab (shakiness 10, smoothing 90). Jitter measured on tracked
  car features: 9.5/8.6 px -> 1.3/0.7 px (x/y at 1920 wide). Alternatives tried: car-locked cubic path (worse, 5.5 px);
  C0241 drive-out (1.9 px, mostly side-on, trunk lip barely visible). Kept C0240.
- **Deck fill:** DE4 A-Spec rear scan (`Integra ASpec Rear.stl`, Drive 1F3lfr0FnH6_S5VsyZ2uEy5WGXnICcp6e) - wingless, same
  trunk lid. Registered with open3d FPFH + RANSAC, then point-to-plane ICP on the trunk lid (3.2 mm RMS); residual
  per-x offset removed on the overlap ring (1.8 mm median). Its deck replaces the lookbook fill in the spoiler footprint
  (`tools/reg_aspec_global.py`, `tools/aspec_patch.py`). No lookbook geometry in the scan any more.
- **Colour:** opening in the Epsilon+ site palette (epsilon.plus theme: primary #5C59E8, secondary #01dee2, accent
  #E85995): violet box with a cyan band, violet glow backdrop, cyan/pink rim lights; title tag and $385 in cyan, strike in pink.
- Output /home/user/media/work/out/bf-integra-385-combo_v0.3.mp4, 22.13 s. Cuts -6/+8/+15/-5/0/+9 ms; -13.8 LUFS; TP -1.8 dBFS.

# v0.2 (user feedback on v0.1, 2026-11-17)
User: "this works, but the final video needs to have both parts on the car, and the scan section needs to show the
stock wing coming off".
- **Real-car shot** is now Install Tutorial **C0240** 12.3-14.7 s: the finished white Type S with the gloss-black Sport
  Wing AND the black trunk lip. (Correction: C0222 in v0.1 showed only a black trunk spoiler, not the Sport Wing.)
  Flat-profile footage, so graded (contrast 1.3, sat 1.2, gamma 0.9); 45 %-wide crop that follows the car, on a blurred
  fill of itself. No text on it.
- **Scan section** (2 shots): the stock Type S scan; the factory trunk spoiler (cut from the scan as one part,
  `tools/split_spoiler.py`: deck faces off the lookbook body surface, grown over adjacency, 16.3k faces, 1.25 m wide)
  lifts off and leaves; then the Epsilon trunk lip and Sport Wing seat on the scan. Then a hard 1:1 cut to the CGI
  car with both parts on (gloss black), orbiting toward rear-on. Then C0240, then the end card.
- **Known fill:** the deck strip under the factory spoiler was never scanned. It is filled from the lookbook body and
  the lookbook's low-poly shell (`deck_patch.ply`, sits ~15 mm low), visible for about a second before the lip covers
  it. For v1, check whether `TypeS Rescan typeS rescan.stl` (Drive 10eR0dVkan3A_2iPDbvO1AzjFXvjK_77I) has the deck
  without the spoiler.
- Timeline (frames @30): 0-96 box | 97-167 wing | 168-238 lip | 239-309 receipt | 310-379 scan: spoiler off |
  380-450 scan: parts on | 451-521 CGI kitted (1:1 in) | 522-592 C0240 | 593-663 end card. 22.13 s.
- Output /home/user/media/work/out/bf-integra-385-combo_v0.2.mp4. Checks: cuts -6/+8/+15/-5/0/+9 ms vs kick attacks
  (168 and 380 not frame-diff detectable; on the grid by construction); -13.8 LUFS, true peak -1.8 dBFS; render luma
  steady; contact sheet reviewed (spoiler lift shows minterpolate ghosting at preview frame rate).

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
