# Porsche 911 GT3 RS (992) scan reel v5 - self-review

File: /home/user/media/work/gt3/out/porsche_gt3rs_992_v5.mp4 (40.6 s). Reviewer on v4: "illumaesthetic logo too small; there is
a bunch of underbody/aero scans not highlighted/shown; attached is the audio, start after the ~2:50 mark".
- Music: user's track (Alkitran - Original Mix) from 171.651 s. 127.0 BPM; every cut on an even-beat kick, measured on the
  delivered file's kick band (40-120 Hz): all 9 cuts within +-0.49 frame. (tools/cutcheck.py's broadband onset locks onto the
  off-beat bass on this track and reads +225 ms - use the kick-band check for four-on-the-floor music.)
- Breakdown (kick out 22.7-25.5 s): FL wheel is off and the camera pushes into the scanned wheel house; the wheel seats on the
  kick return (25.51). Stack lands on b68 (32.13) and locks on b74 (34.96).
- New scans shown: Underbody Wheels (FL wheel), Underbody front and rear wheel house (FL arch, wheels-off state),
  Underbody underbody (floor scan from below, lit from below). Underbody session registered with one shared transform.
- Aero that cannot come off is spotlighted in place (mask pass dims the rest) with labels: FRONT BUMPER STRAKES, FENDER VENT,
  REAR DIFFUSER + DIFFUSER TRIM + BUMPER STRAKE.
- Logo 640 px wide (was 300).
- Still not used: Underbody steered left + DRS open, DRS open/closed (no wing change), hood vent fins / interface right /
  no fins and the 992 GT3 diffuser (other frames), Rear Bumper skin, Side Skirt (upper) duplicate, rear wheel house (same
  state as the front; one wheel scene only).

| # | Criterion | v5 | Notes |
|---|---|---|---|
| 1 | Hook | 4 | whole car moving from frame 1, first cut on b8 |
| 2 | Beat sync | 5 | 9/9 cuts within half a frame of a kick; part events on beats; breakdown used for the wheel house |
| 4 | Scan quality | 4 | wheel house / floor scans are raw (ragged liner edges); hood blotch remains; no clipping (wheel leaves along its axle) |
| 5 | Story | 5 | one lap, then inside the arch and under the car, then stack + lock |
| 7 | Text | 5 | 9 labels from file names, one at a time, in black; underbody shot scaled 85 % to give its label a clear band |
| 8 | Ending | 5 | lock on b74, fade, logo on b78, music fades over 1.6 s |
| 9 | Technical | 4 | 1080x1920 30 fps; wheel leaves the frame while the camera pushes in |

## v4 review
# Porsche 911 GT3 RS (992) scan reel v4 - self-review

File: /home/user/media/work/gt3/out/porsche_gt3rs_992_v4.mp4 (37.97 s). Reviewer on v3: "the parts clip into the car, and there
are two side skirts".
- Two skirts: "Side Skirt (upper)" and "Sideskirt (lower)" are two captures of the same left skirt (p50 3-4 mm apart). Only
  "Sideskirt (lower)" is used now; label reads SIDE SKIRT + SIDE SKIRT STRAKE.
- Clipping: new tools/clipcheck.py samples every part path at 120 Hz against the body. v3 stack shot had 8/9 parts passing
  through the body (up to 25 % of points within 8 mm). v4: every part leaves along its clear direction (found by a direction
  search: QP intakes forward + out along the duct opening, diffuser back + down, skirt down then out, strake out then down)
  and in the stack shot goes out past the silhouette, up, over, and back the same way. All v4 shots: 0 clipping parts
  (worst 0.7 % of points within 8 mm, at the seat). Grille trim no longer moves (no clear exit found), label line dropped.
- Unchanged: shot order, music, cut frames, small logo, sh1/sh2/sh4/sh5 renders.

| # | Criterion | v4 | Notes |
|---|---|---|---|
| 4 | Scan quality | 4 | no part passes through the body; one skirt; hood nostril holes / blotch remain (scan) |
| 5 | Story | 4 | 7 moving parts (was 9 with the duplicate skirt and the grille trim) |
Other criteria as v3 below.

## v3 review
# Porsche 911 GT3 RS (992) scan reel v3 - self-review

v3 = v2 + part-name labels (user: "GT3RS include the labels"). File: /home/user/media/work/gt3/out/porsche_gt3rs_992_v3.mp4.
Labels: FRONT LOWER LIP (+ FRONT GRILLE TRIM), HOOD VENT TOP, FENDER VENT, REAR WING, REAR DIFFUSER (+ UNDERTRAY, QUARTER PANEL
INTAKES), SIDE SKIRTS (UPPER, LOWER, STRAKE) - names from the scan files, no numbers, top black band, one at a time.
No FRONT STRAKES label: the strakes stay on (their removal leaves a hollow cut-out). Text score below re-rated for v3.

## v2 review (unchanged except text) (training/rubric.md)

File: /home/user/media/work/gt3/out/porsche_gt3rs_992_v2.mp4 (1080x1920, 30 fps, 37.97 s, h264 yuv420p + AAC).
Plan: projects/porsche-gt3rs-992/direction.md (scene-director agent; stage-2 shot table). v1 review: review_v1.md.

What changed from v1 (relayed user notes for all V1 reels + addendum A-D):
- Order from the scan inventory: one lap whole -> wheel -> front (nose aero off, louvres) -> rear (wing, diffuser +
  QP intakes off) -> side (skirts off) -> top (everything off) -> stack on the drop -> reassembly -> fade -> small logo.
- Turntables and the one-wide-orbit explode removed; parts come off section by section with the camera on that section
  and stay off (progressive explode); the stack + reassembly lands on the drop (26.285) and locks on 31.905.
- Parts whose removal leaves a hollow/ragged cut-out (front strakes, fender vent, rear strake, diffuser outer trim) no
  longer move; base comp_v2 cuts only the 9 moving parts. No openings/bumper-off: no such state scans exist.
- Whole car in frame on the opener with a visible slide from frame 1; logo shrunk to 300 px after a fade.
- Cuts on onsets measured from the decoded audio; 1-frame fade transitions (no cloned frame before cuts).
- Luma check on every render folder (no dropouts); new renders with persistent data off.

| # | Criterion | Score | Notes |
|---|---|---|---|
| 1 | Hook | 4 | Whole car, slide + push from frame 1 (re-rendered; ive director still reads 0.8 s of low motion on the small car); first cut on the 3.78 s hit. |
| 2 | Beat sync | 4 | 7 cuts on kicks within +-0.46 frame of the decoded-audio onset (3.779, 11.281, 14.093, 18.779, 22.532, 26.285 drop, 33.782 logo). Two cuts (5.633, 16.900) fall in bars with no kick - placed on the strongest local peak; the onset tool reads them ~0.22 s late. |
| 3 | 1:1 match | n/a | scan only |
| 4 | Scan quality | 4 | Clean silver on black; known defects: hood nostril holes and the hood blotch (visible at the top of sh4), grille bars partly missing (sh3). Cut-outs only under the 9 moving parts. |
| 5 | Story | 4 | Sections in one lap, each once; parts off where the camera is. ive director still pairs sh1~sh9 (closed car vs exploded stack from the other side) and sh3~sh6 (front vs rear silhouettes) - kept, different sections/content. |
| 6 | Grade | 5 | AgX, consistent. |
| 7 | Text | 5 | v3: six part-name labels from the scan file names, no numbers, max one on screen, in black off the car, enter after the part moves and leave before the cut. |
| 8 | Ending | 5 | Lock on 31.905, 0.9 s fade to black, small logo at 33.78 as the music ends, decays to 38.0. |
| 9 | Technical | 4 | Spec correct; no duplicate frame before cuts; the reused v1 wing close-up keeps the end plates out of frame (mount detail) - judge against rule A. |
