# BF5 clearance-shelf-drop: draft v0 / v0.1 notes

**v0.1:** the owner said no Del & Eps ("just typical branding content").
- The v0 placeholder render was stopped part-way and never sent.
- v0.1 has no characters: an Epsilon+ wordmark lightbox in the aisle instead, and no placeholder label.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.1.mp4`.

v0 was rendered on 2026-11-17 because the parent session relayed the owner's request "have all the agents make a quick
short first draft". It is a preview: the plan (shotlist.md v4) still needs the owner's sign-off for the final.

- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.mp4` (media is not committed).
- Build:
  - shots: `tools/shots_v0.py` (EEVEE, 40 % res, every 2nd frame doubled to 30 fps), run through `tools/render_v0.sh`;
  - edit: `tools/assemble_v0.py`;
  - price tags: `tools/tags.py`, from `store_snapshot.json`;
  - placeholder characters: `tools/cutouts.py`.

## Assumptions and defaults (every one is open for the owner to change)
1. **Lips:** only the two most popular, the GR Corolla V1 front lip (31 sold in 12 months) and the Integra rear trunk
   lip (16), per the owner's "only focus on the most popular lips". The FG2 and VB lips are left out.
2. **Prices** come from the liquidation sheet / `projects/_blackfriday/PRICES.md`:
   - Integra trunk lip: ABS $100 -> $40, carbon $240 -> $96.
   - GR V1 lip: PU $215 -> $129, carbon $600 -> $330.
   - There is no "was" from the old compare-at prices, and no dates.
3. **Stock line:** "ONLY 14 LEFT IN CARBON" on the GR Corolla car shot.
   - Kept because the owner's concept asks for real "only X left" counts, and the owner only excluded backordered parts.
   - This is against PRICES.md's default (no counts unless the owner asks), and I've asked the owner. Removing it is a
     one-line overlay change.
   - The integra trunk lip (backordered) has no stock line.
4. ~~**Del & Eps are PLACEHOLDERS:**~~ (void in v0.1: the characters are removed) flat cutouts from `knowledge/characters/del-and-eps/del-eps-model-sheet.jpg`,
   stood up as billboards, and marked on screen as "v0 DRAFT - placeholder characters".
   - No Higgsfield credits were spent for v0. Generating real plates waits for the owner's OK on credits.
5. **Car shots** use the website lookbook GLBs in the house silver, not the engineering scans: `eps-acura-integra-de-v29`
   (DE4, stock duckbill hidden) and `eps-toyota-gr-corolla-v23` (V1 `part_front_lip`).
   - The GR Corolla full-car scan wasn't reachable from this session's Drive search, so the scan goes in for v1.
   - The car meshes are decimated to 500k tris for preview speed.
6. **Lips are silver**, like everything except the characters (the locked Del & Eps colour rule).
7. **Warehouse:** a CGI aisle (racking, boxes, pallets, lamp banks), dark and monochrome. The owner OK'd CGI.
8. **The 1:1 cuts** (shelf -> car) use one rigid transform per lip: the lip on the pallet has the same world matrix as on
   its car, and the car shot starts from the shelf shot's last camera.
9. **Music:** "LUXURY" by Baby thug (TikTok Commercial Music Library preview file, 107 s, full length), from 0 s.
   - 99.4 BPM, so a bar is 2.44 s. Cuts are on the bar kicks (2.56 / 5.00 / 7.44 / 9.88 / 12.32 s), and the tag flips
     are on the snares (3.11 / 8.01 s).
   - Claimed in `projects/_blackfriday/MUSIC.md`.
10. **Text and voice:** music only, with no voice line and no 10 mm sting.
    - The end card is the Epsilon+ wordmark (720 px) + "BLACK FRIDAY CLEARANCE" / "EPSILON.PLUS".
    - The overlays are PIL images standing in for the Remotion layer.
11. **Length:** 15.0 s (5 shots + the end card).

## Known v0 shortcomings (for v1)
- The character billboards are flat with keying fringes. Generated plates with contact shadows replace them.
- Scan lines on the lip, the Eps sweep and the tag flip are simple. There are no shadows under the billboards.
- Preview resolution (432x768 upscaled) and EEVEE on a CPU, so expect softness and noise.

## v0.1 checks (2026-11-17)
- 1080x1920, 30 fps, 450 frames = 15.0 s.
- Loudness -14.2 LUFS integrated, true peak -2.2 dBFS.
- The cuts measured from frame differences sit at 2.567 / 5.000 / 7.433 / 9.867 / 12.333 s. The kicks in the decoded
  audio are at 2.55 / 4.99 / (7.29-7.44 kick fill) / 9.88 / 12.32 s.
- 1:1 checks (frames 149/150 and 295/296): the lip keeps its place and size across both cuts.
- For v1:
  - the tag text is small at phone size;
  - the Integra car pull-back ends too small;
  - the shot 2 opening is a long push with a tiny pallet;
  - the scans should replace the lookbook cars.

## v0.2 (2026-11-17): owner feedback "make the signs easier to read, make the actual duckbill and the lip carbon"
- Tags redesigned (`tools/tags.py`): a black BLACK FRIDAY bar, bold 140 px sale prices, a struck-through was-price, fewer
  words. Each tag hangs close to the camera and fills most of the frame width. The aisle BLACK FRIDAY sign is bigger.
- The Integra duckbill and GR V1 lip are a gloss carbon twill (`carbon()` in `tools/shots_v0.py`), on the shelf and on
  the car, so the product contrasts with the silver scans.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.2.mp4`.
- Checks: 1080x1920, 450 frames = 15.0 s; -14.2 LUFS, true peak -2.2 dBFS; same cut frames as v0.1 (on the kicks).
  Contact sheet: the tags read at phone size, and the lip keeps its place and size across both 1:1 cuts (frames 149/150,
  295/296).

## v0.3 (2026-11-17): owner safe-zone rule (`knowledge/safe-zones.md`)
- In v0.2 the tag tops sat in the top UI bar (y < 220), and "ONLY 14 LEFT IN CARBON" (y 250) sat outside the 4:5 feed crop.
- Fix: the tags are scaled 0.40 -> 0.34 m and lowered (up 0.30 -> 0.23, right 0.06 -> 0); only s2 and s4 were
  re-rendered. The count text is at y 330.
- `scripts/safezone_check.py`: all text, prices and logos sit inside x 48-920 / y 285-1440.
- Two non-text elements still cross the right rail, and both are kept because the cameras carry the 1:1 cuts:
  - the end of the GR V1 lip (s4);
  - the Integra's flank in the s3 close-up.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.3.mp4`, 450 frames, -14.2 LUFS, true peak -2.2 dBFS.

## v0.4 (2026-11-17): owner rule "all agents should use www.epsilon.plus"
- The end-card URL reads WWW.EPSILON.PLUS (it was EPSILON.PLUS), at x 310-770 / y 1040-1090, inside the safe zones.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.4.mp4`, 450 frames, -14.2 LUFS, true peak -2.2 dBFS;
  safezone_check sheet reviewed.

## v0.5 (2026-11-17): owner font rule (`knowledge/fonts.md`)
- Headlines, prices, tag titles, the aisle BLACK FRIDAY sign and the stock line use **Unbounded 800, standing in for
  Akira**. The owner hasn't supplied the Akira file yet and has been asked for it.
- Beside the logo: the end card uses Unbounded 400 for BLACK FRIDAY CLEARANCE and 300 for WWW.EPSILON.PLUS.
- Labels and was-prices on the tags use Unbounded 500.
- The aisle sign was resized 1.0 -> 0.70 because the wider face clipped against the racks.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.5.mp4`, 450 frames, -14.2 LUFS, true peak -2.2 dBFS.
  The safezone_check sheet was reviewed: all text is inside x 48-920 / y 285-1440.

## v0.6 (2026-11-18): owner "the carbon pattern needs to be tighter and more glossy/realistic"
- The old look was a 45° checker with 14 mm cells and a slightly hazy coat.
- New 2x2 twill image tile (`tools/carbon_tile.py`):
  - 5 mm tows with a rounded cross-section, fibre striations and dark resin gaps;
  - warp and weft tows differ in tone and roughness (0.18 vs 0.55), so the weave shimmers as the camera moves;
  - the bump affects only the base layer, under a glass clear coat (roughness 0, IOR 1.55);
  - EEVEE ray-traced reflections are on.
- The weave doesn't resolve at 0.4 res, so s2-s5 now render at **0.6** (about 20-30 min a shot). s1 has no carbon and
  stays at 0.4.
- Output: `/home/user/media/work/out/bf-clearance-shelf-drop_v0.6.mp4`, 450 frames, -14.2 LUFS, true peak -2.2 dBFS.
  The safe zones are unchanged and pass.
